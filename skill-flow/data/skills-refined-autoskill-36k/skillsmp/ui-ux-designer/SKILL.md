---
name: ui_ux_designer
description: "AI Design Lead: Access to style, palette, and typography databases."
version: 1.0.0
---

# UI/UX Designer Skill

Activate this skill when you need to make aesthetic decisions, generate CSS, or define the project's style.

## 🛠️ Tools
### Style Search
Use this command to find real (not invented) configurations:
`uv run .agent/skills/ui_ux_designer/scripts/search_design.py --query "<keywords>" --type <colors|typography|styles|products|ux|landing|charts>`

## 📋 Operational Protocol
1. **Search**: Always search the database before proposing a color.
2. **Apply**: If you're hydrating a project (`custom_project`), use the found values to compile `docs_custom/brand_identity_guide.md`.
3. **Fallback**: If the database returns no results, use the "Minimal Monochrome" style.

## 🚫 Prohibitions
- Do not invent Hex codes (e.g., `#123456`) if not present in the database or in `brand_identity_guide.md` (unless they are calculated shades).
- Do not hardcode styles in React components without first defining them in global tokens.
