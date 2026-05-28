---
name: install-auth-sdk
description: Use this skill when setting up and configuring authentication for SDKs like Ideogram or Deepgram in your project.
---

# Install & Configure SDK Authentication

## Overview
Set up SDKs for services like Ideogram and Deepgram and configure authentication credentials.

## Prerequisites
- Node.js 18+ or Python 3.10+
- Package manager (npm, pnpm, or pip)
- Account with API access for the respective service
- API key from the service dashboard

## Instructions

### Step 1: Install SDK
```bash
# Node.js
npm install <sdk-package>

# Python
pip install <sdk-package>
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
// Example for TypeScript
import { createClient } from '<sdk-package>';

const client = createClient(process.env.<SERVICE>_API_KEY);
const { result, error } = await client.manage.getProjects();
console.log(error ? 'Failed' : 'Connected successfully');
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
import { createClient } from '<sdk-package>';

const client = createClient(process.env.<SERVICE>_API_KEY);

// Verify connection
async function verifyConnection() {
  const { result, error } = await client.manage.getProjects();
  if (error) throw error;
  console.log('Projects:', result.projects);
}
```

### Python Setup
```python
from <sdk-package> import <ClientClass>
import os

client = <ClientClass>(os.environ.get('<SERVICE>_API_KEY'))

# Verify connection
response = client.manage.get_projects()
print(f"Projects: {response.projects}")
```

## Resources
- [Service Documentation](https://docs.<service>.com)
- [Service Dashboard](https://console.<service>.com)
- [Service API Reference](https://api.<service>.com)

## Next Steps
After successful authentication, proceed to the respective "hello-world" example for your first API call.