---
name: conducting-browser-compatibility-tests
description: Use this skill when you need to ensure a web application functions correctly across different browsers and devices by identifying browser-specific bugs and compatibility issues.
---

# Skill body

## Overview

This skill automates cross-browser compatibility testing for web applications using BrowserStack, Selenium Grid, or Playwright. It tests across Chrome, Firefox, Safari, and Edge, ensuring consistent functionality and identifying browser-specific issues.

## How It Works

1. **Configuring Browser Matrix**: Define the target browsers (Chrome, Firefox, Safari, Edge), versions, operating systems, and device configurations for testing.
2. **Generating Cross-Browser Tests**: Create and configure tests to run across the defined browser matrix, handling browser-specific quirks and setting up parallel execution for efficiency.
3. **Executing Tests**: Run the tests in parallel using BrowserStack, Selenium Grid, or Playwright, capturing screenshots and logs for analysis.
4. **Generating Compatibility Report**: Compile a detailed report highlighting any compatibility issues, including screenshots and error logs, for easy identification and resolution.

## When to Use This Skill

This skill activates when you need to:
- Ensure a web application functions correctly across different browsers and devices.
- Identify browser-specific bugs or compatibility issues.
- Automate cross-browser testing as part of a CI/CD pipeline.

## Examples

### Example 1: Testing a new feature

User request: "Test browser compatibility for the new shopping cart feature."

The skill will:
1. Configure the browser matrix with the latest versions of Chrome, Firefox, Safari, and Edge.
2. Execute tests specifically targeting the shopping cart functionality across the configured browsers.
3. Generate a report highlighting any compatibility issues encountered with the shopping cart feature, including screenshots.

### Example 2: Regression testing after an update

User request: "/bt"

The skill will:
1. Use the default browser matrix (or a previously defined configuration) to run tests across all specified browsers.
2. Generate a report detailing any compatibility issues found during the regression testing process.