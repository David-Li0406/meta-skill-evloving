---
name: configuring-load-balancers
description: Use this skill when you need to generate production-ready configurations for load balancers like ALB, NLB, Nginx, and HAProxy based on specific requirements.
---

# Skill body

## Overview

This skill enables the generation of complete and production-ready configurations for various load balancers, including ALB, NLB, Nginx, and HAProxy. It streamlines infrastructure automation and DevOps tasks.

## How It Works

1. **Receiving Requirements**: The skill receives user specifications for the load balancer configuration, including type, ports, protocols, and other relevant details.
2. **Generating Configuration**: Based on the user's requirements, the skill generates a complete configuration file tailored to the specified load balancer type.
3. **Presenting Configuration**: The generated configuration is presented to the user, ready for deployment.

## When to Use This Skill

This skill activates when you need to:
- Generate a load balancer configuration for a new application deployment.
- Modify an existing load balancer configuration to accommodate changes in traffic patterns or application requirements.
- Automate the creation of load balancer configurations as part of an infrastructure-as-code workflow.

## Prerequisites

Before using this skill, ensure:
- Backend servers are identified with IPs or DNS names.
- Load balancer type is determined (ALB, NLB, Nginx, HAProxy).
- SSL certificates are available if using HTTPS.
- Health check endpoints are defined.
- Understanding of traffic distribution requirements (round-robin, least-connections).
- Cloud provider CLI installed (if using cloud load balancers).

## Instructions

1. **Select Load Balancer Type**: Choose based on requirements (L4 vs L7, cloud vs on-prem).
2. **Define Backend Pool**: List backend servers with ports and weights.
3. **Configure Health Checks**: Set check interval, timeout, and healthy threshold.
4. **Set Up SSL/TLS**: Configure certificates and cipher suites.
5. **Define Routing Rules**: Create path-based or host-based routing.
6. **Enable Session Persistence**: Configure sticky sessions if needed.
7. **Add Monitoring**: Set up logging and metrics collection.
8. **Test Configuration**: Validate syntax and test traffic distribution.

## Examples

### Example 1: Setting up an Nginx Load Balancer

User request: "Configure an Nginx load balancer to distribute traffic between two backend servers on ports 8080 and 8081."

The skill will:
1. Generate an Nginx configuration file that includes upstream definitions for the two backend servers.
2. Present the complete Nginx configuration file to the user.

### Example 2: Creating an ALB Configuration

User request: "Create an ALB configuration for a web application running on port 80, with health checks on /health."

The skill will:
1. Generate an ALB configuration that includes listener rules, target groups, and health check settings.
2. Present the complete ALB configuration to the user, ready for deployment via AWS CloudFormation or Terraform.

## Best Practices

- **Security**: Always review generated configurations for security vulnerabilities.