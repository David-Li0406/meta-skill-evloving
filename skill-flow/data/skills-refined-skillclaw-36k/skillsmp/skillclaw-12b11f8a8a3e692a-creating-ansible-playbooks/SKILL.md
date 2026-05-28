---
name: creating-ansible-playbooks
description: Use this skill when you need to automate server configurations, software deployments, or infrastructure management using Ansible by generating production-ready playbooks based on your specifications.
---

# Skill body

## Overview

This skill empowers you to generate Ansible playbooks, streamlining infrastructure automation. It translates your specifications into executable Ansible code, allowing for repeatable and reliable deployments.

## How It Works

1. **Receiving User Request**: You provide a request for an Ansible playbook, including details about the desired configuration.
2. **Generating Playbook**: The skill utilizes the `ansible-playbook-creator` plugin to generate a complete Ansible playbook based on your input.
3. **Presenting the Playbook**: The generated Ansible playbook is presented for your review and execution.

## When to Use This Skill

This skill activates when you need to:
- Automate server configuration management tasks.
- Deploy applications across multiple servers consistently.
- Create repeatable and reliable infrastructure setups.

## Examples

### Example 1: Setting up a web server

User request: "Create an Ansible playbook to install and configure Apache on Ubuntu servers."

The skill will:
1. Generate an Ansible playbook that installs the Apache web server and configures it with a default virtual host.
2. Present the playbook to you, ready for execution against Ubuntu servers.

### Example 2: Deploying a Docker container

User request: "Generate an Ansible playbook to deploy a Docker container running Nginx on CentOS servers."

The skill will:
1. Generate an Ansible playbook that installs Docker, pulls the Nginx image, and runs it as a container on CentOS servers.
2. Provide the playbook to you for immediate deployment.

## Best Practices

- **Specificity**: Provide detailed requirements for the desired configuration to generate accurate playbooks.
- **Security**: Review the generated playbooks for security best practices before deploying them in production.
- **Testing**: Always test generated playbooks in a staging environment before applying them in production.