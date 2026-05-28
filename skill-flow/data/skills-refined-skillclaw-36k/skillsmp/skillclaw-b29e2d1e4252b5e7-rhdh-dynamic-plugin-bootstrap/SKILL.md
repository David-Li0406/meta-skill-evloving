---
name: rhdh-dynamic-plugin-bootstrap
description: Use this skill when creating a new dynamic plugin (frontend or backend) for Red Hat Developer Hub (RHDH), ensuring the correct setup and deployment for the intended plugin type.
---

# Skill body

## Purpose

Bootstrap a new dynamic plugin for Red Hat Developer Hub (RHDH). This skill supports both frontend and backend dynamic plugins, which can be installed or uninstalled without rebuilding the application.

## When to Use

Use this skill when creating a new dynamic plugin intended for RHDH dynamic plugin deployment. This includes:
- **Frontend Plugins**: New pages, entity cards, sidebar menu items, custom themes, and any UI components.
- **Backend Plugins**: New backend API plugins, backend modules, scaffolder actions, catalog processors, and server-side functionality.

**Do NOT use this skill for:**
- Frontend plugins when creating backend functionality.
- Backend plugins when creating UI components or visual customizations.

## Prerequisites

Before starting, ensure the following are available:
- Node.js 22+ and Yarn
- Container runtime (`podman` or `docker`)
- Access to a container registry (e.g., quay.io) for publishing

## Workflow Overview

1. **Determine RHDH Version** - Identify target RHDH version for compatibility.
2. **Create Backstage App** - Scaffold Backstage app with matching version.
3. **Create Plugin** - Generate new plugin (frontend or backend) using Backstage CLI.
4. **Implement Plugin Components/Logic** - Build React components for frontend or write the plugin code for backend.
5. **Configure Scalprum (Frontend Only)** - Set up module federation for dynamic loading.
6. **Export as Dynamic Plugin** - Build and export using RHDH CLI.
7. **Package as OCI Image** - Create container image for deployment.
8. **Configure Plugin Wiring (Frontend Only)** - Define routes, mount points, and menu items for frontend plugins.

## Step 1: Determine RHDH Version

Check the target RHDH version and find the compatible Backstage version. Consult `references/versions.md` for version compatibility.