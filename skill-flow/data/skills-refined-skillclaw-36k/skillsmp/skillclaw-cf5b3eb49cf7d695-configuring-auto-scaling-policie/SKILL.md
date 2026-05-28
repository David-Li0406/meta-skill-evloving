---
name: configuring-auto-scaling-policies
description: Use this skill when you need to configure auto-scaling policies for applications and infrastructure, ensuring optimal performance and resilience through dynamic resource allocation.
---

# Skill body

## Overview

This skill empowers you to create and configure auto-scaling policies tailored to specific application and infrastructure needs. It streamlines the process of setting up dynamic resource allocation, ensuring optimal performance and resilience.

## How It Works

1. **Requirement Gathering**: Analyze the user's request to understand specific auto-scaling requirements, including target metrics (CPU, memory, etc.), scaling thresholds, and desired platform.
2. **Configuration Generation**: Generate a production-ready auto-scaling configuration based on the gathered requirements, incorporating best practices for security and scalability. This includes HPA configurations, scaling policies, and necessary infrastructure setup code.
3. **Code Presentation**: Present the generated configuration code to the user, ready for deployment.

## When to Use This Skill

This skill activates when you need to:
- Configure auto-scaling for a Kubernetes deployment.
- Set up dynamic scaling policies based on CPU or memory utilization.
- Implement high availability and fault tolerance through auto-scaling.

## Examples

### Example 1: Scaling a Web Application

User request: "I need to configure auto-scaling for my web application in Kubernetes based on CPU utilization. Scale up when CPU usage exceeds 70%."

The skill will:
1. Analyze the request and identify the need for a Kubernetes HPA configuration.
2. Generate an HPA configuration file that scales the web application based on CPU utilization, with a target threshold of 70%.

### Example 2: Scaling Infrastructure Based on Load

User request: "Configure auto-scaling for my infrastructure to handle peak loads during business hours. Scale up based on the number of incoming requests."

The skill will:
1. Analyze the request and determine the need for infrastructure-level auto-scaling policies.
2. Generate configuration code for scaling based on incoming request metrics.