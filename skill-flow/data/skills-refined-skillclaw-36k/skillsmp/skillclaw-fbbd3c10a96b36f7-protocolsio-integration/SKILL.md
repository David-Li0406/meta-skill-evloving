---
name: protocolsio-integration
description: Use this skill when working with protocols.io to manage scientific protocols, including searching, creating, updating, and publishing protocols, as well as managing discussions, files, and collaborative workflows.
---

# Protocols.io Integration

## Overview

Protocols.io is a comprehensive platform for developing, sharing, and managing scientific protocols. This skill provides complete integration with the protocols.io API v3, enabling programmatic access to protocols, workspaces, discussions, file management, and collaboration features.

## When to Use This Skill

Use this skill when working with protocols.io in any of the following scenarios:

- **Protocol Discovery**: Searching for existing protocols by keywords, DOI, or category.
- **Protocol Management**: Creating, updating, or publishing scientific protocols.
- **Step Management**: Adding, editing, or organizing protocol steps and procedures.
- **Collaborative Development**: Working with team members on shared protocols.
- **Workspace Organization**: Managing lab or institutional protocol repositories.
- **Discussion & Feedback**: Adding or responding to protocol comments.
- **File Management**: Uploading data files, images, or documents to protocols.
- **Experiment Tracking**: Documenting protocol executions and results.
- **Data Export**: Backing up or migrating protocol collections.
- **Integration Projects**: Building tools that interact with protocols.io.

## Core Capabilities

This skill provides comprehensive guidance across major capability areas:

### 1. Authentication & Access

Manage API authentication using access tokens and OAuth flows. This includes both client access tokens (for personal content) and OAuth tokens (for multi-user applications).

**Key operations:**
- Generate authorization links for OAuth flow.
- Exchange authorization codes for access tokens.
- Refresh expired tokens.
- Manage rate limits and permissions.

**Reference:** Read `references/authentication.md` for detailed authentication procedures, OAuth implementation, and security best practices.

### 2. Protocol Operations

Complete protocol lifecycle management from creation to publication.

**Key operations:**
- Create new protocols.
- Update existing protocols.
- Publish protocols for public access.
- Manage protocol steps and materials.

### 3. File Management

Upload and manage files associated with protocols, including data files, images, and documents.

### 4. Collaboration

Facilitate discussions and feedback on protocols, enabling collaborative development and improvement.

### 5. Experiment Tracking

Document and track the execution of protocols, including results and modifications.