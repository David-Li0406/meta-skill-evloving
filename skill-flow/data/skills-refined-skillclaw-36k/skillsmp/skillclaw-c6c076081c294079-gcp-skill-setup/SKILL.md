---
name: gcp-skill-setup
description: Use this skill when you need automated assistance for setting up various Google Cloud Platform (GCP) services, including logging sinks, SQL instances, and task queues.
---

# GCP Skill Setup

## Overview

This skill provides automated assistance for setting up various Google Cloud Platform (GCP) services, including cloud logging sinks, cloud SQL instances, and cloud tasks queues.

## When to Use

This skill activates automatically when you:
- Mention "cloud logging sink setup", "cloud sql instance setup", or "cloud tasks queue setup" in your request.
- Ask about setup patterns or best practices for these GCP services.
- Need help with Google Cloud Platform skills covering compute, storage, BigQuery, Vertex AI, and GCP-specific services.

## Instructions

1. Provides step-by-step guidance for the requested GCP service setup.
2. Follows industry best practices and patterns.
3. Generates production-ready code and configurations.
4. Validates outputs against common standards.

## Examples

**Example: Basic Usage**
- Request: "Help me with cloud logging sink setup"
- Result: Provides step-by-step guidance and generates appropriate configurations.

**Example: SQL Instance Setup**
- Request: "How do I set up a cloud SQL instance?"
- Result: Offers detailed instructions and necessary configurations.

**Example: Task Queue Setup**
- Request: "Can you assist with cloud tasks queue setup?"
- Result: Supplies guidance and code for setting up a cloud tasks queue.

## Prerequisites

- Relevant development environment configured.
- Access to necessary tools and services.
- Basic understanding of GCP concepts.

## Output

- Generated configurations and code.
- Best practice recommendations.
- Validation results.

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Configuration invalid | Missing required fields | Check documentation for required parameters. |
| Tool not found | Dependency not installed | Install required tools per prerequisites. |
| Permission denied | Insufficient access | Verify credentials and permissions. |

## Resources

- Official documentation for related tools.
- Best practices guides.
- Community examples and tutorials.

## Related Skills

Part of the **GCP Skills** skill category.
Tags: gcp, bigquery, vertex-ai, cloud-run, firebase