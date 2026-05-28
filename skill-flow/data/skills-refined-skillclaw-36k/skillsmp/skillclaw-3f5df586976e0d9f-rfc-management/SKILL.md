---
name: rfc-management
description: Use this skill when you need to write or review RFCs for the ToolHive ecosystem, ensuring they meet quality standards and follow established conventions.
---

# Skill body

## Overview

This skill encompasses both writing and reviewing RFCs for the ToolHive ecosystem. It ensures that RFCs are well-structured, complete, and aligned with architectural standards.

## Writing an RFC

### Step 1: Gather Requirements

Before writing an RFC, ask the user about:

1. **Problem Statement**: What problem are they trying to solve?
2. **Target Repository**: Which repo does this affect?
   - `toolhive` - Core runtime, CLI, operator, proxy-runner, virtual MCP
   - `toolhive-studio` - Desktop UI application
   - `toolhive-registry` - MCP server registry data
   - `toolhive-registry-server` - Registry API server
   - `toolhive-cloud-ui` - Cloud/Enterprise web UI
   - `dockyard` - Container packaging for MCP servers
   - `multiple` - Cross-cutting changes
3. **Scope**: What are the goals and explicit non-goals?

### Step 2: Research the Ecosystem

#### 2.1 Fetch Architectural Documentation

Use `mcp__github__get_file_contents` to read from the `stacklok/toolhive` repo's `docs/arch/` directory:

| Document | Content |
|----------|---------|
| `00-overview.md` | Platform overview, key components |
| `01-deployment-modes.md` | Local vs Kubernetes modes |
| `02-core-concepts.md` | Nouns and verbs in the ecosystem |
| `03-transport-architecture.md` | Transport mechanisms |
| `04-secrets-management.md` | Secrets handling |
| `05-runconfig-and-permissions.md` | Configuration and permissions |
| `06-registry-system.md` | Registry architecture |
| `07-groups.md` | Server grouping concepts |
| `08-workloads-lifecycle.md` | Lifecycle management |
| `09-operator-architecture.md` | K8s operator and CRDs |
| `10-virtual-mcp-architecture.md` | Virtual MCP aggregation |

#### 2.2 Review Existing RFCs

Read the `rfcs/` directory for related RFCs that might:
- Conflict with the proposal
- Be superseded by the proposal
- Provide context or dependencies

### Step 3: Draft the RFC

Follow the naming convention `THV-{NUMBER}-{descriptive-name}.md`, ensuring the NUMBER matches the PR number and is zero-padded to 4 digits.

## Reviewing an RFC

### Step 1: Read the RFC

Read the RFC document completely. If provided a PR number or file path, fetch and read it.

### Step 2: Fetch Architectural Context

Gather context from the ToolHive architecture documentation as outlined above.

### Step 3: Check Related Existing RFCs

Search for related RFCs that might conflict with or provide context for the proposal.

### Step 4: Verify Against Target Repository

Ensure proposed changes align with existing code patterns, check for conflicts with recent changes, and verify API compatibility.

## Review Checklist

### A. Structure and Completeness

- [ ] **Metadata present**: Status, Author, Created, Last Update
- [ ] **Problem Statement**: Clearly defined
- [ ] **Goals and Non-Goals**: Explicitly stated
- [ ] **Architectural Alignment**: Reviewed against relevant documents