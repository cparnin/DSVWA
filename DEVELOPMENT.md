# Development Guide

## Project Architecture

```
DSVWA/
├── scanner/               # Core scanner modules
│   ├── semgrep.py        # Semgrep integration
│   ├── gitleaks.py       # Secret scanning
│   ├── sca.py            # Software Composition Analysis (future)
│   ├── ai.py             # AI remediation logic
│   └── report.py         # Report generation
├── cli.py                # Main CLI interface
├── dsvw.py              # Vulnerable web app (test target)
├── .github/workflows/    # GitHub Actions
└── reports/              # Scan outputs
```

## Setting Up Development Environment

1. **Clone and install dependencies:**
```bash
git clone <repo-url>
cd DSVWA
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
```

2. **Install external tools:**
```bash
# Gitleaks (secret scanning)
wget https://github.com/gitleaks/gitleaks/releases/latest/download/gitleaks_linux_x64
chmod +x gitleaks_linux_x64
sudo mv gitleaks_linux_x64 /usr/local/bin/gitleaks

# Semgrep installs via pip (already in requirements.txt)
```

3. **Set up environment variables:**
```bash
# Create .env file
echo "OPENAI_API_KEY=your_openai_key_here" > .env
```

## Adding New Security Tools

To integrate a new security tool, follow this pattern:

### 1. Create scanner module
```python
# scanner/mytool.py
import subprocess
import json

def run_mytool(repo_path):
    """Run security tool and return normalized findings"""
    # Run tool
    result = subprocess.run(['mytool', '--json', repo_path], 
                          capture_output=True, text=True)
    
    # Parse and normalize output
    findings = []
    for item in json.loads(result.stdout):
        finding = {
            'path': item['file'],
            'line': item['line'], 
            'description': item['message'],
            'severity': item['severity']
        }
        findings.append(finding)
    
    return findings
```

### 2. Update CLI interface
```python
# In cli.py, add to main():
if args.scan in ["mytool", "all"]:
    print("▶️ Running MyTool scan...")
    results["mytool"] = run_mytool(repo_path)
```

### 3. Update GitHub Action
```yaml
# In .github/workflows/appsec-pr-comment.yml
- name: Install MyTool
  run: |
    # Installation commands for your tool
    npm install -g mytool
```

## Phase 2 Development Priorities

### 1. Software Composition Analysis (SCA)
- Implement `scanner/sca.py` with OSV/GitHub Advisory integration
- Add dependency vulnerability detection
- Generate automated upgrade PRs

### 2. Multi-language Support  
- Extend Semgrep rules for Java, Go, JavaScript
- Add language-specific scanner modules
- Update CI to handle different project types

### 3. Enhanced Reporting
- Add severity filtering and customization
- Implement dashboard data export
- Create client-specific report templates

## Testing Strategy

### Unit Tests
```bash
# Run scanner tests
python -m pytest tests/test_scanner.py

# Test individual tools
python -m pytest tests/test_semgrep.py
```

### Integration Tests
```bash
# Test full CLI workflow
python cli.py --repo . --scan all

# Test GitHub Action locally with act
act pull_request
```

### Test with DSVW
The included vulnerable web app serves as a perfect test target:
```bash
# Should find multiple vulnerabilities
python cli.py --repo . --scan semgrep
```

## Contributing Guidelines

1. **Branch naming:** `feature/tool-name` or `phase2/sca-integration`
2. **PR process:** All changes go through PR review with AppSec scanner
3. **Testing:** Ensure new tools work with the test vulnerable app
4. **Documentation:** Update this guide when adding new integrations

## GitHub Action Configuration

The workflow automatically:
- Installs all security tools
- Runs scans on PR changes
- Posts AI-generated remediation suggestions
- Stores detailed reports as artifacts

To add secrets:
1. Go to repo Settings → Secrets and variables → Actions
2. Add `OPENAI_API_KEY` for AI suggestions
3. Add tool-specific API keys as needed

## Deployment Strategy

### Phase 1 (Current): Single Repo
- Keep everything in DSVWA for easy team collaboration
- Use as demo and development environment

### Phase 2: Reusable Action
- Extract to separate `appsec-scanner-action` repository  
- Publish as GitHub Marketplace action
- Reference from multiple client repositories

### Phase 3: Enterprise Platform
- Deploy as standalone service
- Support GitLab, Bitbucket, and other platforms
- Add dashboard and management interfaces 