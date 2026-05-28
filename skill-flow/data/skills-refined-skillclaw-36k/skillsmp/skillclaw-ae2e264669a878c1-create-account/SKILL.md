---
name: create-account
description: Use this skill when you need to create Robot Framework test cases for SnapLogic account creation, configure environment variables, or view account test case examples.
---

# SnapLogic Account Creation Skill

## Usage Examples

| What You Want | Example Prompt |
|---------------|----------------|
| Explain steps | `Explain the steps to create an account in SnapLogic` |
| Create account test case | `Create a robot test case for Oracle account` |
| Create multiple accounts | `I need to create Snowflake and S3 accounts for my pipeline` |
| Check env variables | `What environment variables do I need for Kafka?` |
| View env file contents | `Show me what's in the Snowflake keypair env file` |
| Get template | `Show me a template for creating accounts` |
| See example | `What does an Oracle account test case look like?` |
| Troubleshoot | `I'm getting an error creating my Snowflake account` |
| JAR file info | `What JAR files do I need for DB2?` |
| List account types | `What account types are supported?` |
| Configure credentials | `Help me configure MySQL account credentials` |

## Agentic Workflow

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

## Quick Template Reference

**Create account test case:**
```robotframework
[Template]    Create Account From Template
${ACCOUNT_LOCATION_PATH}    ${ORACLE_ACCOUNT_PAYLOAD_FILE_NAME}    ${ORACLE_ACCOUNT_NAME}    overwrite_if_exists=${TRUE}
```

**Common account variables:**
| Account | Payload Variable | Name Variable |
|---------|------------------|---------------|
| Oracle | `${ORACLE_ACCOUNT_PAYLOAD_FILE_NAME}` | `${ORACLE_ACCOUNT_NAME}` |
| PostgreSQL | `${POSTGRES_ACCOUNT_PAYLOAD_FILE_NAME}` | `${POSTGRES_ACCOUNT_NAME}` |
| Snowflake | `${SNOWFLAKE_ACCOUNT_PAYLOAD_FILE_NAME}` | `${SNOWFLAKE_ACCOUNT_NAME}` |
| Kafka | `${KAFKA_ACCOUNT_PAYLOAD_FILE_NAME}` | `${KAFKA_ACCOUNT_NAME}` |
| S3 | `${S3_ACCOUNT_PAYLOAD_FILE_NAME}` | `${S3_ACCOUNT_NAME}` |

**Related slash command:** `/create-account-testcase`