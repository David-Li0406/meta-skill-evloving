---
name: google-stitch-ui-design
description: Use this skill when you need to generate UI designs and frontend code using Google Stitch via the Model Context Protocol (MCP).
---

# Skill body

## Overview

Google Stitch allows you to generate production-ready UI designs and frontend code from text descriptions. It supports various device layouts including desktop, mobile, and tablet.

## Prerequisites

1. **Google Cloud Project** with the Stitch API enabled.
2. **Google Cloud CLI** (`gcloud`) installed and initialized.
3. **Required IAM Roles**:
   - `roles/serviceusage.serviceUsageAdmin` (to enable the service)
   - `roles/mcp.toolUser` (to call MCP tools)

## Setup Steps

### 1. Configure Google Cloud

Authenticate and set up your Google Cloud project:
```bash
gcloud auth application-default login
gcloud config set project YOUR_PROJECT_ID
gcloud beta services mcp enable stitch.googleapis.com --project=YOUR_PROJECT_ID
```

### 2. Set Environment Variables

Set your Google Cloud project ID and access token:
```bash
export GOOGLE_CLOUD_PROJECT="your-project-id"
export STITCH_ACCESS_TOKEN=$(gcloud auth print-access-token)
```

## Tools

Once configured, the Stitch MCP exposes the following tools:

| Tool                               | Purpose                               |
| ---------------------------------- | ------------------------------------- |
| `stitch_list_projects`             | List all your Stitch projects         |
| `stitch_create_project`            | Create a new UI design project        |
| `stitch_get_project`               | Get project details                   |
| `stitch_list_screens`              | List screens in a project             |
| `stitch_get_screen`                | Get screen details with HTML code     |
| `stitch_generate_screen_from_text` | Generate a screen from a text prompt  |

## Workflows

### Create a Project

```bash
mcporter call stitch.create_project title="My App Design"
```

### Generate a Screen

```bash
mcporter call stitch.generate_screen_from_text \
  projectId="PROJECT_ID" \
  prompt="A modern dashboard with sidebar navigation, user stats cards, and a data table" \
  deviceType="DESKTOP" \
  modelId="GEMINI_3_PRO"
```

**Parameters:**
- `projectId` (required): Numeric project ID (e.g., `4651986810686364080`)
- `prompt` (required): UI description
- `deviceType`: `MOBILE` (default), `DESKTOP`, `TABLET`, or `AGNOSTIC`
- `modelId`: `GEMINI_3_FLASH` (default, 30–60s) or `GEMINI_3_PRO` (1–3min, higher quality)

**Note:** Generation takes 1–3 minutes. Do not retry.

### List Screens

```bash
mcporter call stitch.list_screens projectId="PROJECT_ID"
```

### Get Screen Details

```bash
mcporter call stitch.get_screen projectId="PROJECT_ID" screenId="SCREEN_ID"
```

### Download Code

```bash
mcporter call stitch.fetch_screen_code projectId="PROJECT_ID" screenId="SCREEN_ID"
```