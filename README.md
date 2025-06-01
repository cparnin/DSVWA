# 🕵️‍♂️ AppSec Scanner

**AI-Powered Security Scanner for Git Repositories**

An intelligent security scanner that combines multiple security tools with AI-powered remediation suggestions. Perfect for automated security scanning in CI/CD pipelines and PR workflows.

## 🚀 **Quick Start**

### **Prerequisites**
- Python 3.8+
- [Semgrep](https://semgrep.dev/docs/getting-started/) installed
- [Gitleaks](https://github.com/gitleaks/gitleaks) installed  
- OpenAI API key (for AI remediation suggestions)

### **Installation**

1. **Clone the repository:**
   ```bash
   git clone https://github.com/cparnin/appsec_scanner.git
   cd appsec_scanner
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment:**
   ```bash
   echo "OPENAI_API_KEY=your_api_key_here" > .env
   ```

### **Usage**

**Scan any repository:**
```bash
cd src
python cli.py --repo /path/to/target/repo --scan all
```

**Run specific scanners:**
```bash
# SAST only (Static Application Security Testing)
python cli.py --repo /path/to/repo --scan semgrep

# Secrets scanning only  
python cli.py --repo /path/to/repo --scan gitleaks

# Both scanners
python cli.py --repo /path/to/repo --scan all
```

## 🛠️ **What It Does**

### **Current Features ✅**

1. **🔍 SAST Scanning (Semgrep)**
   - Detects security vulnerabilities in code
   - Supports 30+ programming languages
   - Uses auto-configured rulesets
   - Repo-agnostic scanning

2. **🔑 Secrets Detection (Gitleaks)**  
   - Finds hardcoded secrets, API keys, passwords
   - Comprehensive custom rules for 20+ secret types
   - Configurable allowlists and patterns
   - Works across all file types

3. **🤖 AI-Powered Remediation**
   - Provides specific, actionable fix suggestions
   - Batch processing for cost efficiency
   - Context-aware security advice
   - Powered by OpenAI GPT models

4. **📊 Professional Reports**
   - Clean HTML reports with severity indicators
   - GitHub PR comment integration
   - Text summaries for quick review
   - Emoji-enhanced output for clarity

5. **🚀 GitHub Actions Integration**
   - Zero-configuration PR scanning
   - Automatic security review comments
   - Sticky PR comments with results
   - Works with any repository

### **Planned Features 🔮**

- **SCA (Software Composition Analysis)** - Trivy integration for dependency scanning
- **Enhanced multi-language support** - Specialized rules for Java, Go, C#
- **Custom rule integration** - Organization-specific security patterns
- **Dashboard and metrics** - Historical tracking and trends

## 📁 **Project Structure**

```
appsec_scanner/
├── src/                     # Main source code
│   ├── cli.py              # Command-line interface
│   ├── scanners/           # Security scanner modules
│   │   ├── __init__.py     # Package initialization
│   │   ├── semgrep.py      # SAST scanning (Semgrep)
│   │   ├── gitleaks.py     # Secrets detection (Gitleaks)
│   │   └── sca.py          # SCA scanning (planned)
│   ├── ai/                 # AI remediation
│   │   ├── __init__.py     # Package initialization
│   │   └── remediation.py  # OpenAI integration
│   └── reporting/          # Report generation
│       ├── __init__.py     # Package initialization
│       ├── html.py         # HTML report generator
│       └── templates/      # Jinja2 templates
│           └── report.html # HTML report template
├── configs/                # Configuration files
│   └── .gitleaks.toml     # Secrets detection rules
├── .github/workflows/      # CI/CD automation
│   └── appsec-pr-comment.yml # GitHub Action for PR scanning
├── outputs/                # Generated reports (gitignored)
└── requirements.txt        # Python dependencies
```

## 🎯 **GitHub Integration**

### **For Any Repository:**

1. **Copy the GitHub Action:**
   ```bash
   cp .github/workflows/appsec-pr-comment.yml /path/to/target/repo/.github/workflows/
   ```

2. **Add your OpenAI API key** to the target repo's GitHub Secrets as `OPENAI_API_KEY`

3. **Create a PR** - The scanner automatically runs and posts results as PR comments

4. **Review findings** - Each finding includes AI-generated fix suggestions

## 🔧 **Configuration**

### **Secrets Detection**
The scanner uses a comprehensive configuration in `configs/.gitleaks.toml` that detects:
- AWS keys, GitHub tokens, API keys
- Database passwords, connection strings  
- Cloud service credentials (GCP, Azure, Salesforce)
- JWT secrets, OAuth tokens, and more

### **AI Batch Processing**
Adjust batch size for cost control:
```bash
python cli.py --repo . --scan all --ai-batch-size 5
```

## 📈 **Sample Output**

```
🕵️‍♂️ AppSec Scanner starting...
🔍 Running Semgrep scan...
🔍 Running Gitleaks scan...
🤖 Generating AI remediation suggestions...
📝 Writing findings to pr-findings.txt...
📝 Generating HTML report...
🎉 Scan complete! Findings saved to pr-findings.txt and HTML report.
```

## 🏗️ **Extending the Scanner**

This tool is designed for easy extension:

1. **Add new scanners** - Follow the interface in `src/scanners/`
2. **Modify AI prompts** - Update `src/ai/remediation.py`
3. **Customize reports** - Edit templates in `src/reporting/templates/`
4. **Add new rules** - Update `configs/.gitleaks.toml`

## 🔒 **Security Notes**

- This scanner follows security best practices
- All findings include remediation guidance
- No sensitive data is stored or transmitted
- AI suggestions are advisory only

## 📝 **License**

MIT License - See LICENSE file for details

---

**Built for secure software development workflows** 🛡️