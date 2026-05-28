---
name: tech-research-enforcer
description: Use this skill when you need to verify current information about programming languages, frameworks, libraries, DevOps tools, or any technical topic to avoid outdated assumptions.
---

# Tech Research Enforcer

## Core Principle

**Never assume. Always verify.** Technology changes rapidly—APIs evolve, libraries update, best practices shift, and documentation changes. Even when Claude has knowledge about a topic, that knowledge may be outdated or incomplete for the user's specific context.

## Mandatory Research Workflow

### When to Use This Workflow

ALWAYS use this workflow for questions involving:

- Programming languages (Python, JavaScript, Go, Rust, Java, C#, etc.)
- Frameworks and libraries (React, Vue, Django, FastAPI, Spring Boot, .NET, etc.)
- DevOps tools (Docker, Kubernetes, Terraform, Ansible, Helm, etc.)
- Cloud platforms (AWS, Azure, GCP, DigitalOcean, etc.)
- Databases (PostgreSQL, MySQL, MongoDB, Redis, etc.)
- Build tools and package managers (npm, pip, cargo, Maven, Gradle, etc.)
- CI/CD platforms (GitHub Actions, GitLab CI, Jenkins, CircleCI, etc.)
- Monitoring and observability (Prometheus, Grafana, ELK, Datadog, etc.)
- Infrastructure as Code (Terraform, Pulumi, CloudFormation, etc.)
- Container orchestration (Kubernetes, Docker Swarm, ECS, etc.)

### Step 1: Identify What Needs Verification

Before answering any technical question, explicitly identify:

1. **Specific technologies mentioned**: Names, versions if mentioned
2. **Implicit assumptions**: What am I assuming about current state, APIs, or behavior?
3. **Critical details**: Configuration syntax, API endpoints, CLI commands, file formats
4. **Version sensitivity**: Does this answer depend on specific versions?

### Step 2: Search for Current Information

Use `web_search` to find authoritative sources:

**Primary sources to prioritize:**
- Official documentation sites (docs.python.org, kubernetes.io/docs, react.dev, etc.)
- Official GitHub repositories (for libraries and tools)
- Official blogs or announcements from technology providers