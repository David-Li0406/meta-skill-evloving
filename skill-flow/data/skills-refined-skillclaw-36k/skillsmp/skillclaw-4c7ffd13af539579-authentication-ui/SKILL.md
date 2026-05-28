---
name: authentication-ui
description: Use this skill when you need to implement user authentication with JWT and a user-friendly UI in a Next.js application.
---

# Skill body

## Overview
This skill outlines the steps to implement user authentication using JSON Web Tokens (JWT) and a local signer, while ensuring a seamless user experience in a Next.js application.

## Steps

### 1. Set Up JWT Authentication
- **Create a Signer**: Initialize a Signer when the application loads. This Signer should be unique for each session.
- **User Sign-In**: When a user signs in, generate a JWT that includes the username and a timeout (default is 1 hour, configurable).
- **Database Integration**: Use DynamoDB to maintain user session states (logged in/out).

### 2. Implement the User Interface
- **Role Definition**: As a Staff Engineer, ensure the code is clean, well-documented, and user-friendly.
- **UI Style**: Match the application style to [Cross River](https://www.crossriver.com/), ensuring a calm and pleasant user experience using Tailwind CSS.
- **Page Setup**:
  - Ensure no scrolling is required to view essential elements.
  - Implement a clear menu structure that includes options for logout, settings, and prompts.
  - Maintain user data during login interactions, redirecting users back to their previous state post-login.

### 3. Menu and Navigation
- **Menu Features**:
  - Include options for logout, settings, and admin functionalities (e.g., updating/adding agents).
- **Login Flow**:
  - After a successful login, redirect users to the main prompt page.
  - If login is required during an interaction, prompt the user to log in without losing any entered data.

### 4. Toolstack
- Utilize the following technologies:
  - Next.js
  - React
  - Tailwind CSS
  - TypeScript
  - ESLint for code quality

## Example Code
Refer to the example implementation in `auth.ts` for a practical demonstration of the authentication process.

```typescript
// Example of creating a JWT
const jwt = require('jsonwebtoken');

function createJWT(username) {
    const payload = { username };
    const token = jwt.sign(payload, 'your_secret_key', { expiresIn: '1h' });
    return token;
}
```