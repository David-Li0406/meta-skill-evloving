---
name: detecting-infrastructure-drift
description: Use this skill when you need to identify discrepancies between the current infrastructure configuration and the desired state, ensuring consistency and preventing configuration errors.
---

# Skill body

## Overview

This skill empowers Claude to identify and report on deviations between the current state of your infrastructure and its defined desired state. By leveraging the `drift-detect` command, it provides insights into configuration inconsistencies, helping maintain infrastructure integrity and prevent unexpected issues.

## How It Works

1. **Invocation**: The user requests drift detection.
2. **Drift Analysis**: Claude executes the `drift-detect` command.
3. **Report Generation**: The command analyzes the infrastructure and identifies any deviations from the defined configuration.
4. **Result Presentation**: Claude presents a report detailing the detected drift, including affected resources and configuration differences.

## When to Use This Skill

This skill activates when you need to:
- Identify infrastructure drift in your environment.
- Ensure that your infrastructure configuration matches the desired state.
- Generate a report detailing discrepancies between the current and desired infrastructure configurations.

## Examples

### Example 1: Checking for Infrastructure Drift

User request: "Check for infrastructure drift in my production environment."

The skill will:
1. Execute the `drift-detect` command.
2. Present a report detailing any detected drift, including resource changes and configuration differences.

### Example 2: Identifying Configuration Changes

User request: "Are there any configuration changes that haven't been applied to my infrastructure?"

The skill will:
1. Execute the `drift-detect` command.
2. Provide a summary of configuration changes that are present in the desired state but not reflected in the current infrastructure.

## Best Practices

- **Regular Monitoring**: Regularly check for drift to maintain infrastructure consistency.
- **Documentation**: Keep documentation updated to reflect the desired state of the infrastructure.