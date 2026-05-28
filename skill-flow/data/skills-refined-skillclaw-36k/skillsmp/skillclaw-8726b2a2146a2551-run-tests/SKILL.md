---
name: run-tests
description: Use this skill when you want to run Robot Framework tests in the SnapLogic project, need to know the appropriate make command, or want to understand test tags and execution options.
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

## Quick Command Reference

| Test Type | Command |
|-----------|---------|
| Oracle | `make robot-run-all-tests TAGS="oracle" PROJECT_SPACE_SETUP=True` |
| PostgreSQL | `make robot-run-all-tests TAGS="postgres" PROJECT_SPACE_SETUP=True` |
| Snowflake | `make robot-run-all-tests TAGS="snowflake" PROJECT_SPACE_SETUP=True` |
| Kafka | `make robot-run-all-tests TAGS="kafka" PROJECT_SPACE_SETUP=True` |
| MySQL | `make robot-run-all-tests TAGS="mysql" PROJECT_SPACE_SETUP=True` |
| SQL Server | `make robot-run-all-tests TAGS="sqlserver" PROJECT_SPACE_SETUP=True` |
| S3/MinIO | `make robot-run-all-tests TAGS="s3" PROJECT_SPACE_SETUP=True` |
| Multiple | `make robot-run-all-tests TAGS="oracle OR postgres" PROJECT_SPACE_SETUP=True` |

**Note:** Use `PROJECT_SPACE_SETUP=True` for the first run, omit for subsequent runs.

## Agentic Workflow

### Step 1: Understand the User's Request
Parse what the user wants:
- Run tests for a specific system? (Oracle, Snowflake, Kafka, etc.)
- First time setup or subsequent run?
- With or without Groundplex management?

### Step 2: Provide Quick Answer First
For simple questions, give the command immediately.

### Step 3: Offer More Details If Needed
Only provide additional context if asked.