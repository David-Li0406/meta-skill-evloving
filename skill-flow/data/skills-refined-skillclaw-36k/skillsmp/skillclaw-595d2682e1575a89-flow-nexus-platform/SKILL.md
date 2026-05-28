---
name: flow-nexus-platform
description: Use this skill for comprehensive management of the Flow Nexus platform, including user authentication, sandbox creation, app deployment, payment processing, and coding challenges.
---

# Flow Nexus Platform Management

This skill provides a unified interface for managing the Flow Nexus platform, covering various functionalities such as user authentication, sandbox execution, app deployment, payment management, and coding challenges.

## Command Categories
- **Authentication**: User registration, login, profile management
- **Sandboxes**: Create and manage isolated environments for development
- **App Deployment**: Deploy applications to the Flow Nexus platform
- **Payments**: Handle credits, billing, and subscriptions
- **Challenges**: Manage coding challenges and achievements

## Quick Start

### Step 1: Authenticate

**Register New Account**
```javascript
mcp__flow-nexus__user_register({
  email: "user@example.com",
  password: "secure_password",
  full_name: "Your Name"
})
```

**Login to Existing Account**
```javascript
mcp__flow-nexus__user_login({
  email: "user@example.com",
  password: "your_password"
})
```

### Step 2: Create a Sandbox

```javascript
mcp__flow-nexus__sandbox_create({
  template: "node",
  name: "dev-environment",
  install_packages: ["express", "dotenv"],
  env_vars: { NODE_ENV: "development" }
})
```

### Step 3: Execute Code in Sandbox

```javascript
mcp__flow-nexus__sandbox_execute({
  sandbox_id: "your_sandbox_id",
  code: 'console.log("Hello Flow Nexus!")',
  language: "javascript"
})
```

### Step 4: Deploy an Application

```javascript
mcp__flow-nexus__template_deploy({
  template_name: "express-api-starter",
  deployment_name: "my-api",
  variables: { database_url: "postgres://..." }
})
```

## Additional Features

- **Payment Management**: Handle credits and subscriptions through the Flow Nexus payment system.
- **Challenges**: Participate in coding challenges and track achievements.

## Prerequisites
- Flow Nexus MCP server configured
- Valid Flow Nexus account

## Tools Required
- Commands prefixed with `mcp__flow-nexus__*`

For detailed information, refer to the Flow Nexus documentation.