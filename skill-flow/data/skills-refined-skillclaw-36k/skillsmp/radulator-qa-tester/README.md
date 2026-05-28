# Radulator QA Tester - Complete Testing System

**Status:** ✅ Fully Configured and Ready to Use
**Version:** 2.0 - Updated for 18 Calculators
**Date:** November 2025

---

## 🎯 Overview

The Radulator QA Tester is a comprehensive automated testing skill for Claude Code that transforms Claude into your personal QA engineer. It provides end-to-end testing for all 18 medical calculators in the Radulator application across radiology, hepatology/liver, and urology specialties.

### What This System Does

✅ **Automated Browser Testing** - Uses Playwright MCP to interact with your app like a real user
✅ **Mathematical Verification** - Python scripts validate calculations against medical formulas
✅ **Diagnostic Collection** - Captures console errors, network requests, and screenshots
✅ **Test Generation** - Automatically creates Playwright regression tests
✅ **Git Workflow Integration** - Manages dev1 → test1 → main promotion workflow
✅ **PR Management** - Posts test results as GitHub PR comments

---

## 📦 What's Included

```
.claude/skills/radulator-qa-tester/
├── SKILL.md                              # Main skill instructions for Claude
├── README.md                             # This file
├── references/
│   ├── test_cases.md                    # Test data for all 18 calculators
│   ├── mcp_setup.md                     # Playwright & GitHub MCP setup guide
│   └── workflow.md                      # Git workflow documentation
├── scripts/
│   ├── compute_expected.py              # Formula verification (11 calculators)
│   ├── verify_calculators.py            # Legacy verification script
│   └── generate_playwright_test.py      # Test generator
└── assets/
    └── playwright_test_template.js      # Playwright test templates
```

---

## 🚀 Quick Start

### Prerequisites

Before using this skill, you need:

1. **Node.js** (v18+) - For running Playwright
2. **Python 3** (v3.8+) - For verification scripts
3. **Docker** - For GitHub MCP server
4. **GitHub Personal Access Token** - For PR management

### Step 1: Install MCP Servers

The skill requires two MCP servers. Add them to your Claude config:

**Location:** `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["-y", "@playwright/mcp@latest"]
    },
    "github": {
      "command": "docker",
      "args": [
        "run", "-i", "--rm",
        "-e", "GITHUB_PERSONAL_ACCESS_TOKEN",
        "ghcr.io/github/github-mcp-server"
      ],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "your-github-token-here"
      }
    }
  }
}
```

**Create GitHub Token:** https://github.com/settings/tokens
**Required Scopes:** `repo`, `read:org`, `workflow`

### Step 2: Restart Claude

After updating the config:
1. Quit Claude Desktop completely
2. Reopen Claude Desktop
3. Verify MCP servers are loaded (check status indicator)

### Step 3: Test the Setup

Ask Claude:
```
Navigate to localhost:5173 and tell me what you see
```

If that works, you're ready to use the skill!

---

## 💡 How to Use

### Basic Calculator Testing

Simply ask Claude to test a calculator:

```
Test the Adrenal CT Washout calculator
```

Claude will:
1. Start your dev server (`npm run dev`)
2. Open browser via Playwright
3. Fill in test values
4. Calculate results
5. Verify against expected values
6. Show you screenshots and a detailed report

### Testing Pull Requests

When you have a PR ready:

```
Test PR #42
```

Claude will:
1. Fetch PR from GitHub
2. Identify which calculators changed
3. Run tests on affected calculators
4. Post results as PR comment
5. Recommend merge/fix based on results

### Generating Test Suites

Build up your regression tests:

```
Generate Playwright tests for all calculators
```

This creates reusable test files you can run in CI/CD.

---

## 📊 Supported Calculators

### Radiology (6 calculators)
- **Adrenal CT Washout** - Absolute/relative washout percentages
- **Adrenal MRI CSI** - Chemical shift index and ratio
- **Prostate Volume** - Volume and PSA density
- **Renal Cyst Bosniak** - Bosniak classification
- **Spleen Size ULN** - Upper limit of normal by age/sex
- **Hip Dysplasia** - Alpha/beta angles and migration index

### Hepatology/Liver (9 calculators)
- **ALBI Score** - Albumin-bilirubin grade
- **AVS Cortisol** - Adrenal vein sampling for Cushing
- **AVS Aldosterone** - Adrenal vein sampling for hyperaldosteronism
- **BCLC Staging** - Barcelona Clinic Liver Cancer staging
- **Child-Pugh** - Cirrhosis severity score
- **Milan Criteria** - HCC transplant eligibility
- **MELD-Na** - Liver transplant prioritization
- **MR Elastography** - Liver fibrosis staging
- **Y-90 Segmentectomy** - Radioembolization dosimetry

### Urology (3 calculators)
- **IPSS** - International Prostate Symptom Score
- **RENAL Nephrometry** - Renal tumor complexity scoring
- **SHIM** - Sexual Health Inventory for Men (IIEF-5)

---

## 🧪 Example Test Cases

### Example 1: Adrenal CT Washout

**Input:**
- Unenhanced HU: 10
- Portal Venous HU: 100
- Delayed HU: 40

**Expected:**
- Absolute Washout: 66.7%
- Relative Washout: 60.0%
- Interpretation: Suggests benign adenoma

### Example 2: Child-Pugh Score

**Input:**
- Bilirubin: 1.5 mg/dL
- Albumin: 3.8 g/dL
- INR: 1.2
- Ascites: None
- Encephalopathy: None

**Expected:**
- Total Score: 5 points
- Class: A (Well-compensated)
- 1-Year Mortality: 5-10%

### Example 3: MELD-Na Score

**Input:**
- Creatinine: 3.5 mg/dL
- Bilirubin: 5.0 mg/dL
- INR: 2.0
- Sodium: 130 mEq/L
- Dialysis: No

**Expected:**
- MELD Score: ~24
- MELD-Na Score: ~28
- Risk: High (19.6% 3-month mortality)
- Interpretation: High priority for transplantation

---

## 🔧 Manual Script Usage

### Python Verification Script

Test calculator formulas directly:

```bash
# Adrenal CT Washout
python3 scripts/compute_expected.py adrenal-ct 10 100 40

# Prostate Volume
python3 scripts/compute_expected.py prostate 4 3 3.5 2

# ALBI Score (SI units)
python3 scripts/compute_expected.py albi SI 40 15

# Child-Pugh
python3 scripts/compute_expected.py child-pugh 1.5 3.8 1.2 none none

# MELD-Na
python3 scripts/compute_expected.py meld-na 3.5 5.0 2.0 130 no
```

Each command returns JSON with expected values that you can compare against browser output.

---

## 📁 Test Data Reference

All test cases are documented in `references/test_cases.md` with:

- **Inputs:** Specific values to test
- **Expected Outputs:** What the calculator should produce
- **Formulas:** Mathematical calculations explained
- **Interpretations:** Clinical significance

This file covers all 18 calculators with multiple test cases each.

---

## 🌐 Git Workflow Integration

### Three-Branch Strategy

```
dev1 (feature development)
  ↓
test1 (QA/staging) ← QA Skill tests here
  ↓
main (production) ← QA Skill re-tests before merge
```

### Automated Workflow

1. **Developer pushes to dev1**
2. **PR created: dev1 → test1**
3. **QA Skill runs tests** on test1 branch
4. **If tests pass:** PR merged to test1
5. **PR created: test1 → main**
6. **QA Skill re-tests** to ensure no regressions
7. **If tests pass:** PR merged to main

---

## 🎨 Customization

### Adding New Test Cases

Edit `references/test_cases.md` to add new test scenarios:

```markdown
### New Test Case Name
**Inputs:**
- Parameter 1: value
- Parameter 2: value

**Expected Outputs:**
- Result 1: expected value
- Result 2: expected value
```

### Adding Calculator Support to Python Script

Edit `scripts/compute_expected.py` and add your calculator function:

```python
def my_new_calculator(param1, param2):
    """
    My New Calculator
    Formula: result = param1 + param2
    """
    result = float(param1) + float(param2)
    return {
        "result": round(result, 2)
    }

# Add to CALCULATORS registry
CALCULATORS = {
    "my-calc": my_new_calculator,
    # ... other calculators
}
```

---

## 🐛 Troubleshooting

### "Playwright MCP not found"

**Solution:**
1. Ensure Node.js is installed: `node --version`
2. Check config file syntax (valid JSON)
3. Restart Claude Desktop

### "GitHub MCP not working"

**Solution:**
1. Verify Docker is running: `docker ps`
2. Check GitHub token is valid
3. Ensure token has required scopes

### "Tests are failing"

**Solution:**
1. Check if dev server is running
2. Verify calculator formulas match test_cases.md
3. Review screenshots Claude captures
4. Check console for JavaScript errors

### "Can't find calculator"

**Solution:**
- Calculator names must match exactly
- Use sidebar text as shown in the app
- Check `src/App.jsx` for exact names

---

## 📚 Additional Resources

### Documentation Files

- **`SKILL.md`** - Complete skill instructions for Claude
- **`references/mcp_setup.md`** - Detailed MCP server setup
- **`references/workflow.md`** - Git workflow explained
- **`assets/playwright_test_template.js`** - Test templates with examples

### External Links

- **Playwright MCP:** https://github.com/microsoft/playwright-mcp
- **GitHub MCP:** https://github.com/github/github-mcp-server
- **Radulator App:** https://radulator.com
- **CLAUDE.md:** Project instructions in repository root

---

## 🔐 Security Notes

1. **Never commit GitHub tokens** to version control
2. **Store tokens** in environment variables or secure vaults
3. **Rotate tokens** regularly (every 90 days recommended)
4. **Use minimal scopes** - only what's needed for PR management

---

## 🎯 Success Metrics

A well-functioning QA system should:

✅ **Catch bugs before merge** - No calculator errors reach main
✅ **Save development time** - Automated testing vs. manual clicking
✅ **Build confidence** - Know exactly what works before deployment
✅ **Enable rapid iteration** - Test changes instantly
✅ **Create regression suites** - Prevent future breakage

---

## 💬 Support

### Getting Help

For questions about:
- **The QA Skill:** Ask Claude - it knows everything about its own skill!
- **Calculator Formulas:** Check calculator source code comments
- **Git Workflow:** See `references/workflow.md`
- **MCP Setup:** See `references/mcp_setup.md`

### Common Commands

```
"Explain the Radulator QA workflow"
"Show me how to test a specific calculator"
"What test data is available for ALBI score?"
"Generate a test report for all calculators"
"Create Playwright tests for the hepatology calculators"
```

---

## 🎉 You're All Set!

Your Radulator QA testing system is fully configured and ready to use. Start by testing a simple calculator, then gradually integrate it into your full development workflow.

**Next Steps:**
1. Test your first calculator
2. Review the test report
3. Generate your first Playwright test
4. Use it in your next PR

Happy testing! 🧪
