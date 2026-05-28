---
name: planning-disaster-recovery
description: Use this skill when you need to plan and implement disaster recovery (DR) procedures, generate configurations, or automate setup code based on specific infrastructure requirements.
---

# Skill body

## Overview

This skill empowers Claude to generate disaster recovery plans tailored to specific infrastructure and business needs. It automates the creation of configurations and setup code, significantly reducing the manual effort required for DR implementation.

## How It Works

1. **Requirement Gathering**: Identify the user's specific disaster recovery requirements, including platform, recovery time objective (RTO), and recovery point objective (RPO).
2. **Configuration Generation**: Generate production-ready configurations for the disaster recovery plan based on the gathered requirements.
3. **Code Generation**: Produce the necessary setup code to implement the disaster recovery plan.

## When to Use This Skill

This skill activates when you need to:
- Create a disaster recovery plan for a specific environment.
- Generate configurations for disaster recovery infrastructure.
- Automate the setup of disaster recovery procedures.

## Examples

### Example 1: Creating a DR Plan for AWS

User request: "Create a disaster recovery plan for my AWS environment with an RTO of 1 hour and an RPO of 15 minutes."

The skill will:
1. Gather the AWS environment details, RTO, and RPO requirements.
2. Generate a disaster recovery plan configuration using AWS services like S3 replication, EC2 snapshots, and Route 53 failover.

### Example 2: Setting Up a Business Continuity Strategy

User request: "Help me set up a business continuity strategy using a multi-region deployment."

The skill will:
1. Analyze the existing infrastructure and application architecture.
2. Generate configurations for deploying the application across multiple regions, including database replication and load balancing.

## Best Practices

- **Security**: Always prioritize security when designing disaster recovery plans. Ensure that all data is encrypted and access controls are in place.