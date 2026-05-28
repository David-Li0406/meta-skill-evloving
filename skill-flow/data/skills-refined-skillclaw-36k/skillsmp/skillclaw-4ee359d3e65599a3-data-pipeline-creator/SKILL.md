---
name: data-pipeline-creator
description: Use this skill when you need automated assistance for creating and managing data pipelines, including CDC, Spark, and Flink jobs.
---

# Data Pipeline Creator

## Overview

This skill provides automated assistance for creating and managing data pipelines across various technologies, including CDC, Spark, and Flink. It activates automatically based on specific trigger phrases related to these technologies.

## When to Use

This skill activates automatically when you:
- Mention "cdc pipeline creator", "spark job creator", or "flink job creator" in your request
- Ask about best practices or patterns for creating data pipelines
- Need help with data pipeline skills covering ETL, data transformation, workflow orchestration, and streaming data processing.

## Instructions

1. Provides step-by-step guidance for creating data pipelines.
2. Follows industry best practices and patterns.
3. Generates production-ready code and configurations.
4. Validates outputs against common standards.

## Examples

**Example: Basic Usage**
Request: "Help me with cdc pipeline creator"
Result: Provides step-by-step guidance and generates appropriate configurations.

**Example: Spark Job**
Request: "Set up spark job creator"
Result: Offers guidance and generates the necessary configurations for a Spark job.

## Prerequisites

- Relevant development environment configured
- Access to necessary tools and services
- Basic understanding of data pipeline concepts

## Output

- Generated configurations and code
- Best practice recommendations
- Validation results

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Configuration invalid | Missing required fields | Check documentation for required parameters |
| Tool not found | Dependency not installed | Install required tools per prerequisites |
| Permission denied | Insufficient access | Verify credentials and permissions |

## Resources

- Official documentation for related tools
- Best practices guides
- Community examples and tutorials

## Related Skills

Part of the **Data Pipelines** skill category.
Tags: etl, airflow, spark, streaming, data-engineering