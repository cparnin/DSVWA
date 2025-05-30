#!/usr/bin/env python3
from dotenv import load_dotenv
load_dotenv()

import argparse
import os
import json
from pathlib import Path
import logging

from scanner.semgrep import run_semgrep  # Semgrep SAST scanner
from scanner.gitleaks import run_gitleaks  # Gitleaks secrets scanner
from scanner.sca import run_sca_scan  # SCA (dependency) scanner (stub for now)
from scanner.report import generate_html_report  # Report generator

import requests
import time

# Configure logging for the CLI
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def batch_suggest_remediation(findings, batch_size=10):
    """
    Batch findings and send them to OpenAI for AI-powered remediation suggestions.
    Adds the AI suggestion to each finding in-place.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        logger.error("No OpenAI API key found. Set OPENAI_API_KEY in your .env file.")
        for finding in findings:
            finding["ai_remediation"] = "No API key, unable to suggest fix."
        return

    def make_prompt(batch):
        # Build a prompt for the LLM with all findings in the batch
        prompt = "Suggest secure, actionable fixes for the following security findings. Answer as a numbered list matching each finding.\n\n"
        for idx, finding in enumerate(batch, 1):
            msg = finding.get("extra", {}).get("message") or finding.get("description", "No message")
            file_path = finding.get("path") or finding.get("file", "unknown file")
            line = finding.get("start", {}).get("line") or finding.get("line", "?")
            prompt += f"{idx}. [{file_path}:{line}] {msg}\n"
        prompt += "\nRespond as:\n1. Fix details for finding 1\n2. Fix details for finding 2\n..."
        return prompt

    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    endpoint = "https://api.openai.com/v1/chat/completions"
    model = "gpt-4o-mini"

    for i in range(0, len(findings), batch_size):
        batch = findings[i:i + batch_size]
        prompt = make_prompt(batch)
        logger.info(f"[OpenAI] Sending findings {i+1}-{i+len(batch)} of {len(findings)} (batch size {batch_size})...")
        try:
            data = {
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 1200,
            }
            r = requests.post(endpoint, headers=headers, json=data, timeout=60)
            r.raise_for_status()
            content = r.json()["choices"][0]["message"]["content"]
            # Try to split the results into numbered answers
            answers = []
            for line in content.split("\n"):
                if line.strip() and (line.strip()[0].isdigit() and line.strip()[1] in [".", ")"]):
                    answers.append(line[line.find('.')+1:].strip())
                elif answers:
                    answers[-1] += " " + line.strip()
            # Assign each AI suggestion to the corresponding finding
            for idx, finding in enumerate(batch):
                finding["ai_remediation"] = answers[idx] if idx < len(answers) else "N/A"
        except Exception as e:
            logger.error(f"[OpenAI] Batch failed: {e}")
            for finding in batch:
                finding["ai_remediation"] = "Error or rate limited from OpenAI."
            time.sleep(2)  # avoid slamming API if repeated errors

def main():
    """
    Main CLI entry point. Parses arguments, runs selected scanners, batches AI suggestions,
    and writes results to report files.
    """
    parser = argparse.ArgumentParser(description="Run Semgrep, Gitleaks, and SCA with AI remediation (batched, cheap!)")
    parser.add_argument("--repo", required=True, help="Path to the repo to scan")
    parser.add_argument("--scan", choices=["semgrep", "gitleaks", "sca", "all"], default="all")
    parser.add_argument("--output", default="reports", help="Directory to store reports")
    parser.add_argument("--ai-batch-size", type=int, default=10, help="How many findings per OpenAI call (default: 10)")
    args = parser.parse_args()

    repo_path = args.repo
    output_dir = Path(args.output)
    output_dir.mkdir(exist_ok=True)

    results = {}

    # Run selected scanners
    if args.scan in ["semgrep", "all"]:
        logger.info("Running Semgrep scan...")
        results["semgrep"] = run_semgrep(repo_path)

    if args.scan in ["gitleaks", "all"]:
        logger.info("Running Gitleaks scan...")
        results["gitleaks"] = run_gitleaks(repo_path)

    if args.scan in ["sca", "all"]:
        logger.info("Running SCA scan...")
        results["sca"] = run_sca_scan(repo_path)

    # Batch and send findings to OpenAI for remediation suggestions
    logger.info("Starting AI remediation suggestions in batches...")
    for tool, findings in results.items():
        if findings:
            batch_suggest_remediation(findings, batch_size=args.ai_batch_size)

    # Write findings to PR-safe text file for GitHub Action comment
    summary_lines = []
    for tool, findings in results.items():
        summary_lines.append(f"## {tool.capitalize()} Findings\n")
        if not findings:
            summary_lines.append("_No issues found._\n")
            continue
        for f in findings:
            msg = f.get("extra", {}).get("message") or f.get("description", "No message")
            file_path = f.get("path") or f.get("file", "unknown file")
            line = f.get("start", {}).get("line") or f.get("line", "?")
            ai_fix = f.get("ai_remediation", "N/A")
            
            # Handle SCA-specific fields
            if tool == "sca":
                vuln_id = f.get("vulnerability_id", "")
                severity = f.get("severity", "UNKNOWN")
                fixed_versions = f.get("fixed_versions", [])
                fix_info = f" | Severity: {severity}"
                if vuln_id:
                    fix_info += f" | Vuln ID: {vuln_id}"
                if fixed_versions:
                    fix_info += f" | Fixed in: {', '.join(fixed_versions[:3])}"
                summary_lines.append(f"- **{msg}**{fix_info} in `{file_path}:{line}`\n  - 💡 *{ai_fix}*")
            else:
                summary_lines.append(f"- **{msg}** in `{file_path}:{line}`\n  - 💡 *{ai_fix}*")
        summary_lines.append("")  # Add space

    with open("pr-findings.txt", "w") as f:
        f.write("\n".join(summary_lines))

    # Optional: generate an HTML report for human reading
    generate_html_report(results, output_dir)

    logger.info("Scan complete. Findings saved to 'pr-findings.txt' and HTML report.")

if __name__ == "__main__":
    main()
