---
name: skeleton-ui
description: How to use skeleton-ui in frontend development
---

## Purpose
Create and style components using Skeleton UI framework with proper preset classes.

## Prerequisites
- Consult https://www.skeleton.dev/llms.txt for component documentation
- Use `webfetch` tool to retrieve latest component specs

## Guidelines
- Use preset classes (e.g., `bg-primary-500`) instead of `variant-*`
- Ensure dark mode compatibility
- Follow Skeleton's spacing and typography system

## Example Usage
When user requests: "Create a card component with avatar"
→ Look up Card and Avatar components from Skeleton docs
→ Generate TypeScript component with proper props
→ Apply theme-aware styling
→ Include accessibility attributes