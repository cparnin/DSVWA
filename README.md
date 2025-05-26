# DSVWA + AppSec Scanner

![Sign](https://i.imgur.com/bovh598.png)

## Overview

This repository combines:
1. **Damn Small Vulnerable Web** (DSVW) - A deliberately vulnerable web application for testing.
2. **AppSec Scanner** - An AI-powered security scanner that finds and suggests fixes for vulnerabilities

The scanner demonstrates automated security analysis with:
- 🔍 **Semgrep** for OWASP Top 10 pattern detection
- 🔐 **Gitleaks** for secret scanning  
- 🤖 **OpenAI integration** for automated remediation suggestions
- 📝 **GitHub PR commenting** for seamless developer workflow

## Quick Start

### Run the Vulnerable Web App (for testing)
```bash
python3 dsvw.py 
# Navigate to http://127.0.0.1:65412/
```

### Run the Security Scanner
```bash
# Install dependencies
pip install -r requirements.txt

# Scan this repo (or any repo)
python cli.py --repo . --scan all

# Results saved to pr-findings.txt and reports/ directory
```

### GitHub Action Integration
The scanner automatically runs on PRs via `.github/workflows/appsec-pr-comment.yml` and posts findings as PR comments.

## Phased Development Plan

### Phase 1: Prototype ✅ (Current)
- [x] GitHub Action to scan PRs using LLM + Semgrep
- [x] Detect OWASP Top 10 patterns in Python repos
- [x] Leave AI-generated comments on PRs with recommendations

### Phase 2: MVP (Next)
- [ ] Support full repo scanning on demand
- [ ] Integrate dependency vulnerability checks (OSV, GitHub Advisory)
- [ ] Auto-generate PRs for safe dependency upgrades
- [ ] Expand language support (Java, Go, etc.)

### Phase 3: Production
- [ ] Add GitLab and Bitbucket support
- [ ] Customize rule severity thresholds and report formats per client
- [ ] Offer remediation-as-code via secure PRs
- [ ] Build AppSec dashboard showing repo risk scores and remediation metrics

## Requirements

Python (**3.x**) and the following tools:
- Semgrep (installed via pip)
- Gitleaks (binary installation required)
- OpenAI API key (for remediation suggestions)

```bash
pip install -r requirements.txt
```

## Team Collaboration

This project is designed for AppSec guild collaboration. See the `scanner/` directory for modular components that can be extended for different security tools and integrations.
