---
name: shiki-code-blocks
description: Use this skill when you need to syntax highlight code blocks with Shiki, supporting server-side rendering and automatic theme switching.
---

# Shiki Code Blocks

To set up Shiki Code Blocks, follow these steps:

1. **Fetch the Recipe**: If the MCP server is configured, use the following resource URI:
   ```
   recipe://fullstackrecipes.com/shiki-code-blocks
   ```

2. **Direct Fetch**: If the MCP server is not configured, fetch the recipe directly using:
   ```bash
   curl -H "Accept: text/plain" https://fullstackrecipes.com/api/recipes/shiki-code-blocks
   ```

3. **Syntax Highlighting**: Use Shiki to syntax highlight your code blocks. This setup supports server-side rendering in RSC and automatic light/dark theme switching.