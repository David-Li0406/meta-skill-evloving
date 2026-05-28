---
name: sdk-install-auth
description: Use this skill when setting up and configuring authentication for SDKs of various services like Ideogram or Deepgram.
---

# SDK Install & Auth

## Overview
Set up the SDK for a specified service and configure authentication credentials.

## Prerequisites
- Node.js 18+ or Python 3.10+
- Package manager (npm, pnpm, or pip)
- Service account with API access
- API key from the service dashboard

## Instructions

### Step 1: Install SDK
```bash
# Node.js
npm install <service-sdk>

# Python
pip install <service-sdk>
```

### Step 2: Configure Authentication
```bash
# Set environment variable
export <SERVICE>_API_KEY="your-api-key"

# Or create .env file
echo '<SERVICE>_API_KEY=your-api-key' >> .env
```

### Step 3: Verify Connection
```typescript
import { <ServiceClient> } from '<service-sdk>';

const client = new <ServiceClient>({
  apiKey: process.env.<SERVICE>_API_KEY,
});

// Test connection code here
```

## Output
- Installed SDK package in node_modules or site-packages
- Environment variable or .env file with API key
- Successful connection verification output

## Error Handling
| Error | Cause | Solution |
|-------|-------|----------|
| Invalid API Key | Incorrect or expired key | Verify key in the service dashboard |
| 401 Unauthorized | API key not set | Check environment variable is exported |
| Network Error | Firewall blocking | Ensure outbound HTTPS allowed |
| Module Not Found | Installation failed | Run `npm install` or `pip install` again |

## Examples

### TypeScript Setup
```typescript
import { <ServiceClient> } from '<service-sdk>';

const client = new <ServiceClient>({
  apiKey: process.env.<SERVICE>_API_KEY,
});

// Verify connection
async function verifyConnection() {
  const { result, error } = await client.manage.getProjects();
  if (error) throw error;
  console.log('Projects:', result.projects);
}
```

### Python Setup
```python
from <service-sdk> import <ServiceClient>
import os

client = <ServiceClient>(os.environ.get('<SERVICE>_API_KEY'))

# Verify connection
response = client.manage.get_projects()
```

## Resources
- [Service Documentation](https://docs.<service>.com)
- [Service Dashboard](https://console.<service>.com)
- [Service Status](https://status.<service>.com)

## Next Steps
After successful authentication, proceed to the respective service's tutorial for your first API call.