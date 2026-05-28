---
name: labarchive-integration
description: Use this skill when you need to automate interactions with the LabArchives electronic lab notebook API for managing research documentation and data workflows.
---

# LabArchives Integration

## Overview

LabArchives is an electronic lab notebook platform for research documentation and data management. This skill allows you to access notebooks, manage entries and attachments, generate reports, and integrate with third-party tools programmatically via the REST API.

## When to Use This Skill

Use this skill when:
- Working with the LabArchives REST API for notebook automation
- Backing up notebooks programmatically
- Creating or managing notebook entries and attachments
- Generating site reports and analytics
- Integrating LabArchives with third-party tools (Protocols.io, Jupyter, REDCap)
- Automating data uploads to electronic lab notebooks
- Managing user access and permissions programmatically

## Core Capabilities

### 1. Authentication and Configuration

Set up API access credentials and regional endpoints for LabArchives API integration.

**Prerequisites:**
- An Enterprise LabArchives license with API access enabled
- API access key ID and password from the LabArchives administrator
- User authentication credentials (email and external applications password)

**Configuration setup:**

Use the following command to create a configuration file:

```bash
python3 scripts/setup_config.py
```

This creates a `config.yaml` file with the following structure:

```yaml
api_url: https://api.labarchives.com/api  # or regional endpoint
access_key_id: YOUR_ACCESS_KEY_ID
access_password: YOUR_ACCESS_PASSWORD
```

**Regional API endpoints:**
- US/International: `https://api.labarchives.com/api`
- Australia: `https://auapi.labarchives.com/api`
- UK: `https://ukapi.labarchives.com/api`

### 2. User Information Retrieval

Obtain user ID (UID) and access information required for subsequent API operations.

**Workflow:**

1. Call the `users/user_access_info` API method with login credentials.
2. Parse the XML/JSON response to extract the user ID (UID).
3. Use the UID to retrieve detailed user information via `users/user_info_via_id`.

**Example using Python wrapper:**

```python
from labarchivespy.client import Client

# Initialize client
client = Client(api_url, access_key_id, access_password)

# Get user access information
user_info = client.get_user_access_info()
```