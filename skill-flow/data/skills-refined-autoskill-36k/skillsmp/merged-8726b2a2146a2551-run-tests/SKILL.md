---
name: run-tests
description: Use this skill when you want to run Robot Framework tests in the SnapLogic project, need to know which make command to use, or want to understand test tags and execution options.
---

# SnapLogic Test Execution Skill

## Usage Examples

| What You Want | Example Prompt |
|---------------|----------------|
| Run specific tests | `How do I run Oracle tests?` |
| Run multiple tests | `How do I run both Snowflake and Kafka tests?` |
| First time setup | `I'm running tests for the first time, what should I do?` |
| Understand tags | `What tags are available for running tests?` |
| Quick iteration | `I want to run tests quickly without Groundplex setup` |
| View results | `Where are the test results stored?` |
| Troubleshoot | `My tests are failing, how do I debug?` |
| Explain execution | `Explain how to run robot tests in this project` |

---

## Agentic Workflow

### Step 1: Understand the User's Request
Parse what the user wants:
- Run tests for a specific system? (Oracle, Snowflake, Kafka, etc.)
- First time setup or subsequent run?
- With or without Groundplex management?
- View results or troubleshoot?

### Step 2: Provide Quick Answer First
For simple questions, give the command immediately from the Quick Command Reference table below.

### Step 3: Offer More Details If Needed
Only provide additional context if the user asks for explanation or if the question is complex.

---

## Quick Command Reference

| Test Type | Command |
|-----------|---------|
| Oracle | `make robot-run-all-tests TAGS="oracle" PROJECT_SPACE_SETUP=True` |
| PostgreSQL | `make robot-run-all-tests TAGS="postgres" PROJECT_SPACE_SETUP=True` |
| Snowflake | `make robot-run-all-tests TAGS="snowflake" PROJECT_SPACE_SETUP=True` |
| Kafka | `make robot-run-all-tests TAGS="kafka" PROJECT_SPACE_SETUP=True` |
| Multiple | `make robot-run-all-tests TAGS="oracle OR postgres" PROJECT_SPACE_SETUP=True` |

**Note:** Use `PROJECT_SPACE_SETUP=True` for first run, omit for subsequent runs.

**Related slash command:** `/run-tests`

---

## Understanding the Make Targets

### 1. `robot-run-all-tests` - Full Workflow with Groundplex
**Use this when:** First time setup, CI/CD pipelines, or you need Groundplex managed automatically.
```bash
make robot-run-all-tests TAGS="your_tags" PROJECT_SPACE_SETUP=True|False
```

### 2. `robot-run-tests-no-gp` - Without Groundplex Launch
**Use this when:** Groundplex is already running, or tests don't need Groundplex.
```bash
make robot-run-tests-no-gp TAGS="your_tags" PROJECT_SPACE_SETUP=True|False
```

---

## Understanding Robot Framework Tags

Tags are labels attached to test cases that allow you to selectively run tests.

### Using Tags with Make Commands
```bash
# Run only tests with 'snowflake_demo' tag
make robot-run-all-tests TAGS="snowflake_demo"

# Run tests with multiple tags (OR logic)
make robot-run-all-tests TAGS="snowflake_demo OR postgres_demo"

# Run tests with multiple tags (AND logic)
make robot-run-all-tests TAGS="snowflake_demo AND task_creation"

# Exclude tests with specific tag
make robot-run-all-tests TAGS="NOT cleanup"
```

---

## Test Results

### Location
```
test/robot_output/
├── output-YYYYMMDD-HHMMSS.xml   # Raw results (for CI/CD)
├── log-YYYYMMDD-HHMMSS.html     # Detailed execution log
└── report-YYYYMMDD-HHMMSS.html  # Summary report (open this)
```

### Viewing Results
```bash
# Open the latest report (macOS)
open test/robot_output/report-*.html

# Find the latest report
ls -lt test/robot_output/report-*.html | head -1
```

---

## Troubleshooting

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| "Environment variable not found" | Missing `.env` file | Run `make check-env` |
| "Connection refused" to database | Service not running | Run `make <db>-start` |
| "Groundplex not available" | Groundplex not started | Use `robot-run-all-tests` |
| "Project space not found" | First run without setup | Add `PROJECT_SPACE_SETUP=True` |
| Tests hang or timeout | Service health issues | Check `make status` |

### Debug Steps

1. **Check environment:** `make check-env`
2. **Check services:** `make status`
3. **View test logs:** `open test/robot_output/log-*.html`
4. **Re-run with fresh setup:** Add `PROJECT_SPACE_SETUP=True`