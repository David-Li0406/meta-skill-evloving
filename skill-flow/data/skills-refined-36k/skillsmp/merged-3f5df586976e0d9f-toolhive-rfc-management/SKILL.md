---
name: toolhive-rfc-management
description: Use this skill when you want to write or review RFCs for the ToolHive ecosystem, ensuring they meet quality standards and follow established conventions.
---

# ToolHive RFC Management Skill

This skill assists in both writing and reviewing RFCs for the ToolHive ecosystem, ensuring they adhere to quality standards, architectural alignment, and security requirements.

## Overview

ToolHive RFCs follow a specific format and naming convention, and they must be evaluated against multiple dimensions: completeness, technical accuracy, architectural alignment, security considerations, and feasibility.

## Writing an RFC

### Workflow

#### Step 1: Gather Requirements

Before writing an RFC, ask the user about:

1. **Problem Statement**: What problem are they trying to solve?
2. **Target Repository**: Which repo does this affect? (e.g., `toolhive`, `toolhive-studio`, `toolhive-registry`, etc.)
3. **Scope**: What are the goals and explicit non-goals?

#### Step 2: Research the Ecosystem

- **Fetch Architectural Documentation**: Use `mcp__github__get_file_contents` to read from the `stacklok/toolhive` repo's `docs/arch/` directory.
- **Review Existing RFCs**: Check the `rfcs/` directory for patterns and related proposals.
- **Search Relevant Codebases**: Use `mcp__github__search_code` or `mcp__github__get_file_contents` to explore relevant repositories.

#### Step 3: Draft the RFC

Create the RFC following the template structure from `rfcs/0000-template.md`.

##### Required Metadata

```markdown
# RFC-XXXX: Title

- **Status**: Draft
- **Author(s)**: Name (@github-handle)
- **Created**: YYYY-MM-DD
- **Last Updated**: YYYY-MM-DD
- **Target Repository**: [from step 1]
- **Related Issues**: [links if applicable]
```

##### Core Sections

1. **Summary**
2. **Problem Statement**
3. **Goals**
4. **Non-Goals**
5. **Proposed Solution**
6. **Security Considerations** (REQUIRED)
7. **Alternatives Considered**
8. **Compatibility**
9. **Implementation Plan**
10. **Testing Strategy**
11. **Documentation**
12. **Open Questions**
13. **References**

#### Step 4: Use Proper Conventions

- **Code Examples**: Use appropriate languages for different components (Go, TypeScript, YAML).
- **Kubernetes CRDs**: Include CRD examples if applicable.

#### Step 5: File Naming

The RFC file should be named `THV-XXXX-{descriptive-name}.md` where XXXX is the PR number.

#### Step 6: Review Checklist

Before finalizing, verify:

- Problem is clearly stated
- Goals and non-goals are explicit
- Security section is complete
- Alternatives are discussed
- Diagrams illustrate complex flows
- Code examples are concrete
- Implementation phases are defined
- Testing strategy covers all levels

## Reviewing an RFC

### Review Workflow

#### Step 1: Read the RFC

Read the RFC document completely. If provided a PR number or file path, fetch and read it.

#### Step 2: Fetch Architectural Context

Gather context from the ToolHive architecture documentation using `mcp__github__get_file_contents`.

#### Step 3: Check Related Existing RFCs

Search for related RFCs that might conflict with or provide context for the proposal.

#### Step 4: Verify Against Target Repository

Search the target repository to verify proposed changes align with existing code patterns and no conflicts exist.

### Review Checklist

#### A. Structure and Completeness

- Metadata present
- Clear summary
- Well-articulated problem statement
- Specific goals and non-goals
- Detailed proposed solution
- Security considerations addressed
- Alternatives considered
- Compatibility discussed
- Implementation plan outlined
- Testing strategy included
- Open questions listed

#### B. Security Review (CRITICAL)

The Security Considerations section must address:

- Threat Model
- Authentication and Authorization
- Data Security
- Input Validation
- Secrets Management
- Audit and Logging
- Mitigations

#### C. Technical Accuracy

- Correct terminology
- Architecture alignment
- Code examples are syntactically correct
- API design consistency
- Configuration format matches existing patterns

#### D. Diagrams and Examples

- Clear Mermaid diagrams
- Concrete code examples
- Realistic configuration examples

#### E. Feasibility and Impact

- Implementation complexity
- Dependencies identified
- Breaking changes addressed
- Performance impact considered
- Cross-repo impact identified

## ToolHive Ecosystem Context

### Target Repositories

| Repository | Type | Key Considerations |
|------------|------|-------------------|
| `toolhive` | Go | Core platform, CLI, operator, proxy, virtual MCP |
| `toolhive-studio` | TypeScript | Desktop UI, Electron app |
| `toolhive-registry-server` | Go | Registry API, MCP Registry spec compliance |
| `toolhive-registry` | Go/JSON | Registry data, server definitions |
| `toolhive-cloud-ui` | TypeScript/Next.js | Cloud UI, OIDC integration |
| `dockyard` | Go | Container packaging, security scanning |

### Key Architecture Principles to Verify

1. Platform, not runner
2. Security by default
3. Middleware composability
4. RunConfig portability
5. Cloud-native

## Reference Files

- Template: `rfcs/0000-template.md`
- Contributing guide: `CONTRIBUTING.md`
- Existing RFCs: `rfcs/THV-*.md`