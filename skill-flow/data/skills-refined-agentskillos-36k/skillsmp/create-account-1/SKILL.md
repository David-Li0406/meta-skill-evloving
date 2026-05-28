---
name: create-account
description: Creates Robot Framework test cases for SnapLogic account creation. Use when the user wants to create accounts (Oracle, PostgreSQL, Snowflake, Kafka, S3, etc.), needs to know what environment variables to configure, or wants to see account test case examples.
user-invocable: true
---

# SnapLogic Account Creation Skill

## Agentic Workflow (Claude: Follow these steps in order)

### Step 1: Load the Complete Guide
```
ACTION: Use the Read tool to load:
{{cookiecutter.primary_pipeline_name}}/.claude/skills/create-account/SKILL.md
```
**Do not proceed until you have read the complete guide.**

### Step 2: Understand the User's Request
Parse what the user wants:
- Which account type? (oracle, postgres, snowflake, etc.)
- Create test case?
- Check environment variables?
- Show template or examples?
- Multiple accounts needed?

### Step 3: Follow the Guide
Use the detailed instructions from the file you loaded in Step 1 to:
- Identify the correct env file for the account type
- Read the env file to understand available variables
- Check baseline tests for reference if needed
- Create or explain the test case

### Step 4: Respond to User
Provide the requested information or create the test case based on the complete guide.

---

## Quick Reference

**Supported account types:**
`oracle`, `postgres`, `mysql`, `sqlserver`, `snowflake`, `snowflake-keypair`, `db2`, `teradata`, `kafka`, `jms`, `s3`, `email`, `salesforce`

**Related slash command:** `/create-account-testcase`
