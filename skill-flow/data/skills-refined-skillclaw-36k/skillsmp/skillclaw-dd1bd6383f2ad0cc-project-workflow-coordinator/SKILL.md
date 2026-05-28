---
name: project-workflow-coordinator
description: Use this skill when you need to coordinate software development processes, manage dependencies, and ensure collaboration among experts and stakeholders.
---

# Skill body

## Overview

This skill serves as a project workflow coordinator, integrating dependency management and expert collaboration to streamline software development processes.

## When to Use

- Initiating new projects and planning development workflows.
- Coordinating cross-team efforts and managing dependencies.
- Ensuring the security and compatibility of project dependencies.

## Steps

### 1. Project Initialization

- **Define Project Scope**: Gather requirements and define the project scope.
- **Select Technology Stack**: Collaborate with system architects and language experts to choose the appropriate technology stack.
- **Assign Roles**: Identify and assign roles to experts (e.g., VP-level roles for strategic decisions).

### 2. Dependency Management

- **Check Dependencies**: Use the dependency updater to analyze and check for outdated or vulnerable dependencies.
- **Update Strategy**: Choose an update strategy (Conservative, Moderate, Aggressive, Security) based on project needs.
- **Execute Updates**: Run the dependency updater commands to update packages and generate reports.

### 3. Collaboration and Coordination

- **Expert Involvement**: Engage relevant experts based on project phases (e.g., coding, testing, deployment).
- **Cross-Team Meetings**: Schedule regular meetings to ensure alignment among teams and address any blockers.
- **Documentation**: Maintain clear documentation of decisions, updates, and project progress.

### 4. Testing and Validation

- **Run Tests**: Execute unit tests and end-to-end tests to validate updates and ensure functionality.
- **Review Changes**: Conduct code reviews and gather feedback from stakeholders.
- **Finalize Deployment**: Prepare for deployment by ensuring all dependencies are up to date and secure.

## Commands for Dependency Management

```bash
# Check for outdated dependencies
/dependency-updater check

# Audit for security vulnerabilities
/dependency-updater audit

# Update all dependencies with a conservative strategy
/dependency-updater update --conservative

# Generate an update report
/dependency-updater report
```

## Conclusion

This skill combines project workflow coordination with intelligent dependency management, ensuring that software development processes are efficient, secure, and collaborative.