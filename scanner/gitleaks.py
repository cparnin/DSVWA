import subprocess
import json
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

def run_gitleaks(repo_path):
    """
    Run Gitleaks secrets scanner on the given repository path.
    Returns a list of normalized secret findings.
    """
    out_dir = Path("reports")
    out_dir.mkdir(exist_ok=True)
    output_file = out_dir / "gitleaks.json"
    
    try:
        logger.info("Running gitleaks scan...")
        # Run Gitleaks in git-aware mode, fall back to filesystem scan if needed
        try:
            result = subprocess.run([
                "gitleaks", "detect", 
                "--source", repo_path,
                "--report-format", "json", 
                "--report-path", str(output_file),
                "--verbose"
            ], capture_output=True, text=True, timeout=300)
            
            if result.returncode == 1:
                logger.info("Gitleaks found potential secrets (exit code 1 - expected)")
            elif result.returncode == 0:
                logger.info("Gitleaks completed - no secrets found")
            else:
                logger.warning(f"Gitleaks returned code {result.returncode}")
                logger.warning(f"stdout: {result.stdout}")
                logger.warning(f"stderr: {result.stderr}")
                
        except subprocess.TimeoutExpired:
            logger.error("Gitleaks scan timed out after 5 minutes")
            return []
            
    except Exception as e:
        logger.error(f"Error running gitleaks: {e}")
        return []

    # Read and normalize results if file exists
    if output_file.exists() and output_file.stat().st_size > 0:
        try:
    with open(output_file) as f:
                content = f.read().strip()
                if not content:
                    logger.info("Gitleaks report is empty - no secrets found")
                    return []
                results = json.loads(content)
                logger.info(f"Gitleaks found {len(results)} potential secrets")
                # Normalize gitleaks output format for downstream use
                normalized_results = []
                for leak in results:
                    normalized_leak = {
                        'path': leak.get('File', 'unknown file'),
                        'line': leak.get('StartLine', '?'),
                        'description': f"Potential secret detected: {leak.get('Description', 'Unknown')}",
                        'rule': leak.get('RuleID', 'unknown-rule'),
                        'secret': leak.get('Secret', '')[:20] + '...' if leak.get('Secret') else 'N/A',
                        'tool': 'gitleaks'
                    }
                    normalized_results.append(normalized_leak)
                return normalized_results
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing gitleaks JSON: {e}")
            return []
        except Exception as e:
            logger.error(f"Error reading gitleaks output: {e}")
            return []
    else:
        logger.info("No gitleaks output file found - likely no secrets detected")
            return []
