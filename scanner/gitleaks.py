import subprocess
import json
from pathlib import Path

def run_gitleaks(repo_path):
    out_dir = Path("reports")
    out_dir.mkdir(exist_ok=True)
    output_file = out_dir / "gitleaks.json"
    
    try:
        print("🔍 Running gitleaks scan...")
        
        # Try git-aware scan first, fall back to filesystem scan
        try:
            result = subprocess.run([
                "gitleaks", "detect", 
                "--source", repo_path,
                "--report-format", "json", 
                "--report-path", str(output_file),
                "--verbose"
            ], capture_output=True, text=True, timeout=300)
            
            if result.returncode == 1:
                print("✅ Gitleaks found potential secrets (exit code 1 - expected)")
            elif result.returncode == 0:
                print("✅ Gitleaks completed - no secrets found")
            else:
                print(f"⚠️ Gitleaks returned code {result.returncode}")
                print(f"stdout: {result.stdout}")
                print(f"stderr: {result.stderr}")
                
        except subprocess.TimeoutExpired:
            print("⏰ Gitleaks scan timed out after 5 minutes")
            return []
            
    except Exception as e:
        print(f"❌ Error running gitleaks: {e}")
        return []

    # Read results if file exists
    if output_file.exists() and output_file.stat().st_size > 0:
        try:
    with open(output_file) as f:
                content = f.read().strip()
                if not content:
                    print("📄 Gitleaks report is empty - no secrets found")
                    return []
                    
                results = json.loads(content)
                print(f"📊 Gitleaks found {len(results)} potential secrets")
                
                # Normalize gitleaks output format
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
            print(f"❌ Error parsing gitleaks JSON: {e}")
            return []
        except Exception as e:
            print(f"❌ Error reading gitleaks output: {e}")
            return []
    else:
        print("📄 No gitleaks output file found - likely no secrets detected")
            return []
