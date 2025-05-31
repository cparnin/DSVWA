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
from scanner.ai import batch_suggest_remediation  # Import the consolidated AI remediation function

import requests
import time

# Configure logging for the CLI
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
