---
name: figma-design
version: 1.0.0
description: >-
  Interact with Figma design files via the web browser using the Figma Plugin API.
  Can create shapes, modify properties, extract information from design files.

triggers:
  - figma
  - design file
  - figma plugin

tools:
  chrome-devtools_navigate_page: true
  chrome-devtools_evaluate_script: true
  chrome-devtools_take_snapshot: true
  chrome-devtools_take_screenshot: true
  chrome-devtools_click: true
  chrome-devtools_fill: true
  chrome-devtools_wait_for: true
---

# Figma Design Skill

Interact with Figma design files via the web browser using the Figma Plugin API.

## Instructions

1. Use the `chrome-devtools_navigate_page` tool to go to [Figma's website](https://www.figma.com/). Then, prompt the user to log in to their Figma account if they are not already logged in and open a specific design file.

2. Once the user has opened the design file, use `chrome-devtools_evaluate_script` to confirm that you have access to the `figma` global object, which indicates that you are within the Figma environment. If you do not have access, inform the user that they need to open a Figma design file or see the Troubleshooting section below.

3. After confirming access, execute the user's query using `chrome-devtools_evaluate_script` to run JavaScript code that interacts with the Figma Plugin API. You can perform tasks such as creating shapes, modifying properties, or extracting information from the design file.

## Rules of Engagement

- Always explain in plain English what you are about to do. Assume that the user cannot read code.
- Do not try alternative solutions like using the REST API or manually interacting with the Figma UI.

## Troubleshooting

If `figma is not defined`:

1. Make sure that the user has appropriate permissions to edit the file and run plugins
2. If the user doesn't have permissions, suggest creating a new branch on the file
3. If the `figma` global is still not accessible, instruct the user to manually open any plugin and close it, then try again

> **Note:** There is a known bug where the `figma` global is not available until a plugin has been opened at least once in the file.

## Additional Documentation

The full reference to the Figma Plugin API can be found here: [Figma Plugin API Documentation](https://developers.figma.com/docs/plugins/api/global-objects/)
