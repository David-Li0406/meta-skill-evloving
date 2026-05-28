---
name: artifacts-builder
description: Use this skill when you need to create elaborate, multi-component HTML artifacts using modern frontend web technologies (React, Tailwind CSS, shadcn/ui) for complex applications requiring state management and routing.
---

# Artifacts Builder

To build powerful frontend artifacts, follow these steps:

1. **Initialize the Frontend Repo**  
   Run the initialization script to create a new React project:
   ```bash
   bash scripts/init-artifact.sh <project-name>
   cd <project-name>
   ```

   This creates a fully configured project with:
   - ✅ React + TypeScript (via Vite)
   - ✅ Tailwind CSS 3.4.1 with shadcn/ui theming system
   - ✅ Path aliases (`@/`) configured
   - ✅ 40+ shadcn/ui components pre-installed
   - ✅ All Radix UI dependencies included
   - ✅ Parcel configured for bundling (via .parcelrc)
   - ✅ Node 18+ compatibility (auto-detects and pins Vite version)

2. **Develop Your Artifact**  
   Edit the generated files to build your artifact. Refer to **Common Development Tasks** for guidance.

3. **Bundle to Single HTML File**  
   To bundle the React app into a single HTML artifact, run:
   ```bash
   bash scripts/bundle-artifact.sh
   ```
   This creates `bundle.html` - a self-contained artifact with all JavaScript, CSS, and dependencies inlined. This file can be directly shared in conversations as an artifact.

   **Requirements**: Your project must have an `index.html` in the root directory.

   **What the script does**:
   - Installs bundling dependencies (parcel, @parcel/config-default, parcel-resolver-tspaths, html-inline)
   - Creates `.parcelrc` config with path alias support
   - Builds with Parcel (no source maps)
   - Inlines all assets into a single HTML using html-inline

4. **Share Artifact with User**  
   Finally, share the bundled HTML file in conversation with the user so they can view it as an artifact.

## Design & Style Guidelines
To avoid "AI slop", refrain from using excessive centered layouts, purple gradients, uniform rounded corners, and the Inter font.