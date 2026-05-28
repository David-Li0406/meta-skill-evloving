---
name: agent-browser
description: Use this skill for headless browser automation to navigate websites, interact with elements, take screenshots, and extract data using the agent-browser CLI.
---

# Skill body

## Overview
The `agent-browser` CLI tool allows for headless browser automation, enabling users to perform web scraping, testing, form filling, and other interactions with web pages through a command-line interface.

## Core Workflow
1. **Navigate to a URL**: 
   ```bash
   agent-browser open <url>
   ```
2. **Take a Snapshot**: 
   ```bash
   agent-browser snapshot -i --json
   ```
   This command captures the interactive elements on the page and provides unique references (like `@e1`, `@e2`) for each element.
3. **Interact with Elements**: 
   Use the references from the snapshot to perform actions:
   ```bash
   agent-browser click @e1
   agent-browser fill @e2 "text"
   ```
4. **Re-snapshot if needed**: 
   After interactions or significant changes to the DOM, take another snapshot to verify the state:
   ```bash
   agent-browser snapshot -i --json
   ```

## Key Commands

### Navigation
- Open a URL: 
  ```bash
  agent-browser open <url>
  ```
- Go back: 
  ```bash
  agent-browser back
  ```
- Go forward: 
  ```bash
  agent-browser forward
  ```
- Reload the page: 
  ```bash
  agent-browser reload
  ```
- Close the browser: 
  ```bash
  agent-browser close
  ```

### Interactions
- Click an element: 
  ```bash
  agent-browser click @e1
  ```
- Fill an input: 
  ```bash
  agent-browser fill @e2 "text"
  ```
- Press a key: 
  ```bash
  agent-browser press Enter
  ```
- Check a checkbox: 
  ```bash
  agent-browser check @e3
  ```
- Uncheck a checkbox: 
  ```bash
  agent-browser uncheck @e3
  ```

### Screenshots
- Take a screenshot: 
  ```bash
  agent-browser screenshot page.png
  ```
- Take a full-page screenshot: 
  ```bash
  agent-browser screenshot --full page.png
  ```

### Wait for Elements
- Wait for an element to be visible: 
  ```bash
  agent-browser wait @e1
  ```
- Wait for a specific amount of time: 
  ```bash
  agent-browser wait 1000  # Wait for 1000 milliseconds
  ```

## Setup
To install the `agent-browser`, run:
```bash
npm install -g agent-browser
```