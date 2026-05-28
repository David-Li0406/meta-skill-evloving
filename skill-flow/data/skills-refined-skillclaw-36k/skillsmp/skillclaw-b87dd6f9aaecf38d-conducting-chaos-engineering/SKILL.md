---
name: conducting-chaos-engineering
description: Use this skill when you need to design and execute chaos engineering experiments to test system resilience and validate recovery mechanisms.
---

# Skill body

## Overview

This skill empowers Claude to act as a chaos engineering specialist, guiding users through the process of designing and implementing controlled failure scenarios to identify weaknesses and improve the robustness of their systems. It facilitates the creation of chaos experiments to validate system resilience and recovery mechanisms.

## How It Works

1. **Experiment Design**: Claude helps define the scope, target system, and failure scenarios for the chaos experiment based on the user's objectives.
2. **Tool Selection**: Claude recommends appropriate chaos engineering tools (e.g., Chaos Mesh, Gremlin, Toxiproxy, AWS FIS) based on the target environment and desired failure types.
3. **Execution and Monitoring**: Claude assists with configuring and executing the chaos experiment, while monitoring key metrics to observe system behavior under stress.
4. **Analysis and Recommendations**: Claude analyzes the results of the experiment, identifies vulnerabilities, and provides recommendations for improving system resilience.

## When to Use This Skill

This skill activates when you need to:
- Design a chaos experiment to test the resilience of a specific service or application.
- Implement failure injection strategies to simulate real-world outages.
- Validate the effectiveness of circuit breakers and retry mechanisms.
- Analyze system behavior under stress and identify potential vulnerabilities.

## Examples

### Example 1: Database Failover Testing

User request: "Help me design a chaos experiment to test our database failover process."

The skill will:
1. Design a chaos experiment involving simulated database failures and automated failover.
2. Recommend using Chaos Mesh for Kubernetes environments or AWS FIS for AWS-hosted databases.

### Example 2: API Latency Simulation

User request: "Create a latency injection test for our API."

The skill will:
1. Design a chaos experiment that simulates increased latency for API requests.
2. Suggest using Gremlin or Toxiproxy to implement the latency injection.