# AppSec Scanner + DSVWA

**AI-Powered Security Scanner for PRs**

## What is This?
- Scans code for security bugs (Semgrep)
- AI (OpenAI) suggests fixes, posted as PR comments
- GitHub Action automates PR scanning
- HTML/text reports for security teams
- DSVWA app included for testing

## Quick Start
```bash
git clone https://github.com/cparnin/DSVWA
cd DSVWA
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
echo "OPENAI_API_KEY=your_key_here" > .env
python cli.py --repo . --scan semgrep
# See pr-findings.txt and reports/
```

## GitHub Action
- Add `OPENAI_API_KEY` to repo secrets
- Create a PR – results posted automatically

## Architecture
- `cli.py` – Main CLI
- `scanner/` – Security tools (semgrep, gitleaks, sca, ai, report)
- `.github/workflows/` – PR automation
- `dsvw.py` – Vulnerable test app

## Extend/Contribute
- Add new scanner: `scanner/newtool.py` (see `scanner/semgrep.py` for interface)
- Add to `cli.py` scan options
- Update GitHub workflow if needed
- Test on DSVWA

## Phase 2+ (Guild TODO)
- SCA & secrets scanning (sca.py, gitleaks.py)
- Amazon Bedrock support
- Multi-language scanning
- GitHub Action Marketplace

**Questions?** See `.cursorrules` or ping chad parnin or #devsecops-guild
