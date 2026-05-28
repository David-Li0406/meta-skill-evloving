---
name: authentication-and-ui
description: Use this skill when you need to implement authentication with JWS and create a user-friendly UI in a Next.js application.
---

# Authentication with JWS
- Create a Signer when the app loads, which will be different each time the app starts.
- When a user signs in, they will receive a JWT containing the username and a timeout (default 1 hour, configurable).
- Maintain a DynamoDB database with an entry for each user to reflect their logged in/out status.
- The JWT will be included in a "header".

# UI Design
## Role
- You are an expert Staff engineer working with Next.js.
- Write clean, understandable code with good documentation.
- Ensure good visibility in the console for easy issue resolution.
- Apply great UX skills by placing functionality logically in the UI for easy access.

## Style
- The app should match the style of [Cross River](https://www.crossriver.com/).
- Keep the UI friendly, calm, and pleasant within the specified style.
- Prefer using Tailwind CSS for styling.

## Page Setup
- Users should not have to scroll to see content unless the output of a prompt is large.
- Provide a clear menu that matches the style of the reference site.
- Ensure that user data is not lost during login interactions; users should return to their previous page with all data intact.
- All fields relevant to the current action should be easily accessible.
- Settings should be located in a dedicated settings menu.
- Navigating between pages should not result in data loss.

## Menu
- The menu will support logout, settings, prompts, and admin functionalities for updating/adding agents.

## Login
- After a normal login, users will be directed to the main prompt page.
- If login is required during an interaction, prompt the user to log in and then return them to the requested page with all data preserved.

## Toolstack
- Next.js
- React
- React-DOM
- Tailwind CSS
- TypeScript
- ESLint and related configurations
- Type definitions for Node, React, and React-DOM