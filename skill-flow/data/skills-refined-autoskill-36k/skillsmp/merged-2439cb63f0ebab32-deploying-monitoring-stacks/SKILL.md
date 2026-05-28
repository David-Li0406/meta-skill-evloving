---
name: deploying-monitoring-stacks
description: Use this skill when you need to set up or configure monitoring infrastructure for applications or systems, including Prometheus, Grafana, and Datadog.
---

## Overview

This skill automates the deployment of comprehensive monitoring solutions, simplifying the setup of Prometheus, Grafana, and Datadog while ensuring best practices and production-ready configurations.

## How It Works

1. **Configuration Gathering**: Gather specific requirements for the monitoring stack, including the desired platform and tools.
2. **Stack Generation**: Generate the necessary configuration files and deployment scripts for the selected monitoring stack based on the requirements.
3. **Deployment Instructions**: Provide clear, step-by-step instructions for deploying the generated configuration to the target environment.

## When to Use This Skill

This skill activates when you need to:
- Deploy a new monitoring stack (Prometheus, Grafana, Datadog).
- Configure an existing monitoring stack.
- Generate production-ready monitoring configurations.

## Prerequisites

Before using this skill, ensure:
- Target infrastructure is identified (Kubernetes, Docker, bare metal).
- Metric endpoints are accessible from the monitoring platform.
- Storage backend is configured for time-series data.
- Alert notification channels are defined (email, Slack, PagerDuty).
- Resource requirements are calculated based on scale.

## Instructions

1. **Select Platform**: Choose Prometheus/Grafana, Datadog, or a hybrid approach.
2. **Deploy Collectors**: Install exporters and agents on monitored systems.
3. **Configure Scraping**: Define metric collection endpoints and intervals.
4. **Set Up Storage**: Configure retention policies and data compaction.
5. **Create Dashboards**: Build visualization panels for key metrics.
6. **Define Alerts**: Create alerting rules with appropriate thresholds.
7. **Test Monitoring**: Verify metrics flow and alert triggering.

## Best Practices

- **Security**: Follow security best practices when deploying monitoring stacks, including using secure credentials and limiting access to sensitive data.
- **Scalability**: Design your monitoring stack to be scalable to handle increasing data volumes and traffic.
- **Documentation**: Thoroughly document your monitoring setup, including configuration details and deployment procedures.

## Examples

### Example 1: Setting up Prometheus and Grafana on Kubernetes

User request: "I need to set up Prometheus and Grafana on my Kubernetes cluster to monitor my application."

The skill will:
1. Generate Kubernetes manifests for deploying Prometheus and Grafana.
2. Provide instructions for configuring Prometheus to scrape application metrics and Grafana to visualize them.

### Example 2: Deploying Datadog Agent

User request: "Deploy Datadog agent to monitor our servers."

The skill will:
1. Generate configuration files for the Datadog agent based on the target environment.
2. Provide instructions for installing and configuring the Datadog agent on the specified servers.

## Error Handling

- **Metrics Not Appearing**: Verify scrape targets are accessible and returning metrics.
- **High Cardinality**: Reduce label combinations or increase Prometheus resources.
- **Alert Not Firing**: Check Alertmanager configuration and notification channels.
- **Dashboard Load Failure**: Verify Grafana datasource configuration and permissions.

## Integration

This skill works seamlessly with other Claude Code skills for infrastructure provisioning and application deployment. It can be integrated into automated CI/CD pipelines for continuous monitoring.

## Resources

- Prometheus documentation: https://prometheus.io/docs/
- Grafana documentation: https://grafana.com/docs/