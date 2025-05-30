# Guild Handoff – Quick Reference

## What is This?
- PR security scanner: Semgrep + OpenAI + GitHub Actions
- Posts AI fix suggestions as PR comments

## How to Test
```bash
git clone https://github.com/cparnin/DSVWA
cd DSVWA && python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python cli.py --repo . --scan semgrep
```

## Add a New Tool
- Copy `scanner/semgrep.py` as template
- Add to `cli.py` scan options
- Update GitHub workflow if needed
- Test on DSVWA

## Key Files
- `cli.py`, `scanner/`, `.github/workflows/`, `dsvw.py`, `.cursorrules`

## Contact
- @cparnin, #security-guild, #devsecops-guild 