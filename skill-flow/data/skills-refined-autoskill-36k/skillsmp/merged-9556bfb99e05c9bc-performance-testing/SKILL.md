---
name: performance-testing
description: Use this skill when you need to design, execute, and analyze performance tests to assess system performance under various conditions.
---

## Overview

This skill automates performance testing workflows, allowing Claude to create and run tests such as load, stress, spike, and endurance tests. It facilitates bottleneck identification and provides actionable recommendations for optimization.

## How It Works

1. **Test Design**: Analyze the user's request to determine the appropriate test type and configure parameters such as target users, duration, and ramp-up time.
2. **Test Execution**: Execute the designed test using the performance-test-suite plugin, collecting metrics like response times, throughput, and error rates.
3. **Metrics Analysis**: Analyze the collected metrics to identify performance bottlenecks and potential issues.
4. **Report Generation**: Generate a comprehensive report summarizing the test results, highlighting key performance indicators, and providing recommendations for improvement.

## When to Use This Skill

This skill activates when you need to:
- Create a load test for an API.
- Design a stress test to determine the breaking point of a system.
- Simulate a spike test to evaluate system behavior during sudden traffic surges.
- Develop an endurance test to detect memory leaks or stability issues.

## Examples

### Example 1: Load Testing an API

User request: "Create a load test for the /users API, ramping up to 200 concurrent users over 10 minutes."

The skill will:
1. Design a load test configuration with a ramp-up stage to 200 users over 10 minutes.
2. Execute the load test using the performance-test-suite plugin.
3. Generate a report showing response times, throughput, and error rates for the /users API.

### Example 2: Stress Testing a Checkout Process

User request: "Design a stress test to find the breaking point of the checkout process."

The skill will:
1. Design a stress test configuration with gradually increasing load on the checkout process.
2. Execute the stress test, monitoring response times and error rates.
3. Identify the point at which the checkout process fails and generate a report detailing the system's breaking point.

## Best Practices

- **Realistic Scenarios**: Design tests that accurately reflect real-world usage patterns.
- **Comprehensive Metrics**: Monitor a wide range of performance metrics to gain a holistic view of system performance.
- **Iterative Testing**: Run multiple tests with different configurations to fine-tune performance and identify optimal settings.

## Integration

This skill integrates with other monitoring and alerting plugins to provide real-time feedback on system performance during testing. It can also be used in conjunction with deployment plugins to automatically validate performance after code changes.