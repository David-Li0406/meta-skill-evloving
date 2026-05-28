---
name: create-account
description: Creates Robot Framework test cases for SnapLogic account creation. Use when the user wants to create accounts (Oracle, PostgreSQL, Snowflake, Kafka, S3, etc.), needs to know what environment variables to configure, or wants to see account test case examples.
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

---

## Agentic Workflow

**Follow these steps in order:**

### Step 1: Understand the User's Request
Parse what the user wants:
- Which account type? (oracle, postgres, snowflake, etc.)
- Create test case?
- Check environment variables?
- Show template or examples?
- Multiple accounts needed?

### Step 2: Follow the Guide
Use the detailed instructions below to:
- Identify the correct env file for the account type
- Read the env file to understand available variables
- Check baseline tests for reference if needed
- Create or explain the test case

### Step 3: Respond to User
Provide the requested information or create the test case based on this guide.

---

## Quick Template Reference

**Create account test case:**
```robotframework
[Template]    Create Account From Template
${ACCOUNT_LOCATION_PATH}    ${ACCOUNT_PAYLOAD_FILE_NAME}    ${ACCOUNT_NAME}    overwrite_if_exists=${TRUE}
```

**Common account variables:**
| Account | Payload Variable | Name Variable |
|---------|------------------|---------------|
| Oracle | `${ORACLE_ACCOUNT_PAYLOAD_FILE_NAME}` | `${ORACLE_ACCOUNT_NAME}` |
| PostgreSQL | `${POSTGRES_ACCOUNT_PAYLOAD_FILE_NAME}` | `${POSTGRES_ACCOUNT_NAME}` |
| Snowflake | `${SNOWFLAKE_ACCOUNT_PAYLOAD_FILE_NAME}` | `${SNOWFLAKE_ACCOUNT_NAME}` |
| Kafka | `${KAFKA_ACCOUNT_PAYLOAD_FILE_NAME}` | `${KAFKA_ACCOUNT_NAME}` |
| S3 | `${S3_ACCOUNT_PAYLOAD_FILE_NAME}` | `${S3_ACCOUNT_NAME}` |

---

## Quick Reference

**Supported account types:**
`oracle`, `postgres`, `mysql`, `sqlserver`, `snowflake`, `snowflake-keypair`, `db2`, `teradata`, `kafka`, `jms`, `s3`, `email`, `salesforce`

---

## Environment Variable Setup

### Case 1: Using Docker Services (Local Testing)
If you're creating an account for an endpoint brought up using Docker services:
- Use the default credentials from the respective file in `env_files/`
- No changes needed - the values are pre-configured for Docker containers

### Case 2: Using External/Your Own Instance
If you're using your own external instance:
1. Read the env file to understand the required variables.
2. Copy the variables to root `.env` file and update the values with your actual credentials.

---

## Test Case Examples by Account Type

### Database Accounts

#### Oracle Account
```robotframework
Create Oracle Account
    [Documentation]    Creates an Oracle database account in SnapLogic.
    [Tags]    oracle    account_setup
    [Template]    Create Account From Template
    ${ACCOUNT_LOCATION_PATH}    ${ORACLE_ACCOUNT_PAYLOAD_FILE_NAME}    ${ORACLE_ACCOUNT_NAME}    overwrite_if_exists=${TRUE}
```

#### PostgreSQL Account
```robotframework
Create PostgreSQL Account
    [Documentation]    Creates a PostgreSQL database account in SnapLogic.
    [Tags]    postgres    account_setup
    [Template]    Create Account From Template
    ${ACCOUNT_LOCATION_PATH}    ${POSTGRES_ACCOUNT_PAYLOAD_FILE_NAME}    ${POSTGRES_ACCOUNT_NAME}    overwrite_if_exists=${TRUE}
```

#### Snowflake Account (Password Auth)
```robotframework
Create Snowflake Account
    [Documentation]    Creates a Snowflake account using password authentication.
    [Tags]    snowflake    account_setup
    [Template]    Create Account From Template
    ${ACCOUNT_LOCATION_PATH}    ${SNOWFLAKE_ACCOUNT_PAYLOAD_FILE_NAME}    ${SNOWFLAKE_ACCOUNT_NAME}    overwrite_if_exists=${TRUE}
```

---

## Checklist Before Committing
- [ ] Payload file exists in `accounts_payload/`
- [ ] Environment file exists in `env_files/`
- [ ] All Jinja variables in payload have corresponding env variables
- [ ] JAR files added if required
- [ ] Test has appropriate tags
- [ ] Documentation describes the account type
- [ ] No sensitive credentials are hardcoded