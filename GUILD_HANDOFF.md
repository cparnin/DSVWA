# Guild Handoff - Quick Reference

## What We Built
AI-powered security scanner that scans PRs and posts AI-generated fix suggestions as comments.

## Current Status (Phase 1 COMPLETE)
- ✅ **Working**: PR scanning with Semgrep + OpenAI + GitHub Actions
- ✅ **Tested**: Successfully found 3 vulnerabilities in DSVWA and posted AI fixes
- ✅ **Ready**: Documentation, contribution guidelines, team setup

## Common Questions & Answers

### "How do I test this?"
```bash
git clone https://github.com/cparnin/DSVWA
cd DSVWA && python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python cli.py --repo . --scan semgrep
# Check pr-findings.txt and reports/ folder
```

### "How do I add a new security tool?"
1. Create `scanner/newtool.py` following the interface in `scanner/semgrep.py`
2. Add to `cli.py` scan options
3. Update GitHub workflow to install the tool
4. Test against DSVWA (should find vulnerabilities)

### "What's the architecture?"
- `cli.py` - Main interface
- `scanner/` - Modular security tools (semgrep, gitleaks, sca, ai, report)
- `.github/workflows/` - Automated PR scanning
- `dsvw.py` - Intentionally vulnerable test app

### "What are the Phase 2 priorities?"
1. **GitHub Action Marketplace** - Package as reusable action
2. **Amazon Bedrock** - Consider using ImagineX account instead of OpenAI
3. **Dependency Scanning** - SCA for npm/pip packages
4. **Multi-language** - Expand beyond Python

### "How does the AI work?"
- Semgrep finds vulnerabilities
- `scanner/ai.py` sends findings to OpenAI GPT-4
- AI generates specific fix suggestions
- Posted as PR comments via GitHub Actions

### "Is this secure to run?"
- Yes, designed with security in mind
- No shell=True, parameterized commands
- Secrets via environment variables only
- DSVWA is intentionally vulnerable for testing

## Key Files
- `README.md` - Main documentation
- `.cursorrules` - AI assistant training for project
- `cli.py` - Command line interface
- `scanner/ai.py` - OpenAI integration
- `.github/workflows/appsec-pr-comment.yml` - GitHub Action

## Emergency Contacts
- **Original Author**: @cparnin
- **Repo**: https://github.com/cparnin/DSVWA
- **Slack**: #security-guild, #devsecops-guild

## Quick Wins for New Contributors
- Add support for new programming languages
- Improve HTML report styling
- Add new Semgrep rules
- Enhance GitHub Action workflow
- Create documentation/tutorials 