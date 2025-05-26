# AppSec Scanner + DSVWA Test Environment

**AI-Powered Security Scanner with GitHub Actions Integration**

Built for the Imagine X Security Guild - Ready for team collaboration and development.

## 🚀 What This Does

- **🔍 Automated PR Security Scanning** - Finds security vulnerabilities in code before they reach production
- **🤖 AI-Powered Fix Suggestions** - OpenAI generates step-by-step remediation instructions
- **📝 Developer-Friendly Comments** - Posts findings directly in PR comments (no separate tools needed)
- **🎯 OWASP Top 10 Detection** - Catches common web vulnerabilities (injection, XSS, secrets, etc.)
- **📊 Detailed Reports** - HTML and JSON outputs for security teams

## 🛡️ Security Tools Explained

### What is Semgrep?
**Semgrep** is a static analysis tool that scans source code for security vulnerabilities and bugs. Think of it as a smart "find and replace" that understands code patterns and can spot dangerous coding practices like:
- SQL injection vulnerabilities
- Cross-site scripting (XSS) flaws  
- Hardcoded secrets and passwords
- Insecure API usage

### What is SAST?
**Static Application Security Testing (SAST)** means analyzing source code without running it. It's like having a security expert review every line of code looking for potential vulnerabilities.

### What is SCA?
**Software Composition Analysis (SCA)** scans your dependencies (npm packages, pip packages, etc.) for known security vulnerabilities. Most apps use hundreds of third-party libraries - SCA makes sure they're safe.

## ⚡ Quick Start

### For Guild Members (SWEs & Security Engineers)

1. **Clone and setup:**
```bash
git clone https://github.com/cparnin/DSVWA
cd DSVWA
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

2. **Set up OpenAI API:**
```bash
echo "OPENAI_API_KEY=your_key_here" > .env
```

3. **Test the scanner:**
```bash
python cli.py --repo . --scan semgrep
# Check pr-findings.txt and reports/ for results
```

### GitHub Action (Auto-runs on PRs)

Already configured! Just:
1. Add `OPENAI_API_KEY` to repo secrets
2. Create a PR 
3. Watch the magic happen ✨

## 🏗️ Architecture (Simple Overview)

```
scanner/
├── semgrep.py      # Finds security bugs in source code
├── gitleaks.py     # Finds secrets/passwords in code  
├── sca.py          # Checks dependencies for vulnerabilities (Phase 2)
├── ai.py           # Generates fix suggestions using OpenAI
└── report.py       # Creates readable reports

cli.py              # Main command-line interface
.github/workflows/  # Automated PR scanning
dsvw.py            # Intentionally vulnerable test app
```

## 🎯 Development Phases

### ✅ Phase 1 (COMPLETE)
- [x] **PR Security Scanning** - Automatically scan pull requests for security issues
- [x] **OWASP Top 10 Detection** - Find the most common web vulnerabilities
- [x] **AI Fix Suggestions** - Get specific remediation steps for each finding
- [x] **GitHub Integration** - Works seamlessly with existing development workflow

### 🔄 Phase 2 (Guild TODO - Great for SWEs!)
- [ ] **GitHub Action Marketplace** - Package as reusable action for other teams to use
- [ ] **Amazon Bedrock Integration** - Consider using ImagineX's existing Bedrock account (cost savings + better security)
- [ ] **Dependency Scanning** - Check if your npm/pip packages have known vulnerabilities
- [ ] **Multi-language Support** - Expand beyond Python to Java, Go, JavaScript
- [ ] **Full Repo Scanning** - Scan entire repositories on-demand

### 🚀 Phase 3 (Future)
- [ ] **GitLab/Bitbucket Support** - Work with other Git platforms
- [ ] **Custom Rules** - Add company-specific security checks
- [ ] **Security Dashboard** - Visual overview of security posture
- [ ] **Auto-fix PRs** - Automatically create PRs to fix simple security issues

## 👥 Team Development

### For Software Engineers
- **No security expertise required!** - The tool explains what each vulnerability means
- **Familiar workflow** - Just create PRs like normal, get security feedback automatically
- **Learn as you go** - AI explanations help you understand security concepts

### For Security Engineers  
- **Extend existing tools** - Add new security scanners easily
- **Customize rules** - Adjust what gets flagged based on your environment
- **Scale security reviews** - Automate what used to be manual code reviews

### Cursor AI IDE Integration
This project works great with Cursor IDE:
```bash
# Open in Cursor IDE for enhanced development
cursor .
```

**Future Consideration**: We may set up ImagineX Cursor Team sharing for enhanced collaboration.

**AI Assistant**: The `.cursorrules` file trains Cursor's AI to understand this security project, giving better code suggestions and maintaining consistent patterns.

### Guild Collaboration Guidelines
- **Modular design** - Easy to add new security tools (great first contributions!)
- **Test environment** - DSVW app included for testing (intentionally vulnerable)
- **Branch naming**: `feature/scanner-name` or `phase2/enhancement`
- **All PRs** get automatically scanned by our own tool 😎

## 🔧 Adding New Security Tools (Perfect for SWEs!)

1. **Create scanner module**: `scanner/newtool.py`
2. **Follow the simple interface**:
```python
def run_newtool(repo_path: str) -> List[Dict[str, Any]]:
    """
    Standard scanner interface - returns list of security findings
    
    Each finding should have:
    - path: which file has the issue
    - line: which line number  
    - description: what's wrong
    - severity: how bad it is (low/medium/high)
    """
    return [
        {
            'path': 'app.py',
            'line': 42,
            'description': 'SQL injection vulnerability detected',
            'severity': 'high',
            'rule_id': 'sql-injection-001'
        }
    ]
```
3. **Update CLI**: Add to `cli.py` scan options
4. **Update GitHub workflow**: Install tool in `.github/workflows/`
5. **Test**: Run against DSVW app (should find vulnerabilities)

## 📋 Guild Handoff Checklist

### ✅ Ready Now
- **Phase 1 Complete** - PR scanning working perfectly
- **Production Ready** - GitHub Actions configured and tested
- **Team Ready** - Cursor project configured with development guidelines
- **Documentation** - Clear setup and contribution guidelines
- **Test Environment** - DSVW vulnerable app for testing
- **Beginner Friendly** - No prior AppSec knowledge required

### 🎯 Phase 2 Priorities for Guild (Great Learning Opportunities!)
1. **GitHub Action Marketplace** - Package for reuse across ImagineX and external teams
2. **Amazon Bedrock Integration** - Consider leveraging ImagineX's Bedrock account for cost savings
3. **Dependency Scanning** - Understand supply chain security
4. **Multi-language Rules** - Expand to languages your team uses
5. **Enhanced Reporting** - Build dashboards and metrics

## 🤝 Contributing (All Skill Levels Welcome!)

1. **Branch**: `feature/your-feature` or `phase2/enhancement`
2. **Test**: Run scanner on this repo (finds 3 vulnerabilities by design)
3. **PR**: Security scanner will automatically review your code
4. **Review**: Guild members approve and merge

### Good First Issues for SWEs:
- Add support for a new programming language
- Improve report formatting/styling
- Add new security rule configurations
- Enhance GitHub Action workflow

### Good First Issues for Security Engineers:
- Add new security tool integrations
- Customize vulnerability severity levels
- Add security-specific reporting features
- Tune false positive rates

## 🛠️ Technical Notes

### Current Stack (All Standard Tools)
- **Python 3.x** - Main programming language
- **Semgrep** - Security code scanner (like ESLint but for security)
- **OpenAI GPT-4** - AI for generating fix suggestions
- **GitHub Actions** - Automated CI/CD pipeline
- **Jinja2** - Template engine for reports

### Future Enhancements (Guild TODO)
- **GitHub Action Marketplace** - Standalone action: `uses: imaginex/appsec-scanner@v1`
- **Amazon Bedrock** - Consider using ImagineX's existing AWS Bedrock account (Claude-3, Titan models)
- **Gitleaks** - Tool for finding secrets in Git history
- **OSV/GitHub Advisory** - Databases of known vulnerabilities
- **Multi-cloud** - GitLab, Bitbucket support

## 🎓 Learning Resources

New to application security? These resources help:
- **OWASP Top 10** - Most common web vulnerabilities
- **Semgrep Rules** - Examples of security patterns to detect
- **SAST vs DAST** - Different types of security testing
- **DevSecOps** - Integrating security into development workflows

---

**Ready for guild collaboration!** 🛡️ 

**Questions?** Ping the AppSec channel or check the `.cursorrules` file for development guidelines.

**New to security?** That's perfect! This project is designed to help you learn while contributing.
