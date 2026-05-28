---
name: setting-up-log-aggregation
description: Use this skill when setting up log aggregation solutions using ELK (Elasticsearch, Logstash, Kibana), Loki, or Splunk, generating production-ready configurations and setup code based on specific requirements and infrastructure.
---

# Log Aggregation Setup

This skill provides automated assistance for setting up centralized log aggregation systems, including ingestion pipelines, parsing, retention policies, dashboards, and security controls.

## Overview

This skill simplifies the deployment and configuration of log aggregation systems. It automates the process of setting up ELK, Loki, or Splunk, providing production-ready configurations tailored to your environment.

## Prerequisites

Before using this skill, ensure:
- Target infrastructure is identified (Kubernetes, Docker, VMs)
- Storage requirements are calculated based on log volume
- Network connectivity between log sources and aggregation platform
- Authentication mechanism is defined (LDAP, OAuth, basic auth)
- Resource allocation planned (CPU, memory, disk)

## How It Works

1. **Requirement Gathering**: Identify the user's specific requirements, including the desired log aggregation platform (ELK, Loki, or Splunk), infrastructure details, and security considerations.
2. **Select Platform**: Choose ELK, Loki, or Splunk.
3. **Configuration Generation**: Generate necessary configuration files for the chosen platform, including configurations for data ingestion, processing, storage, and visualization.
4. **Setup Code Generation**: Provide the setup code needed to deploy and configure the log aggregation solution on the target infrastructure, which might include scripts, Docker Compose files, or other deployment artifacts.
5. **Test Pipeline**: Verify logs flow from sources to visualization.

## Instructions

1. **Configure Ingestion**: Set up log shippers (Filebeat, Promtail, Fluentd).
2. **Define Storage**: Configure retention policies and index lifecycle.
3. **Set Up Processing**: Create parsing rules and field extractions.
4. **Deploy Visualization**: Configure Kibana/Grafana dashboards.
5. **Implement Security**: Enable authentication, encryption, and RBAC.

## Examples

### Example 1: Deploying an ELK Stack

User request: "Set up an ELK stack for my Kubernetes cluster to aggregate application logs."

The skill will:
1. Generate Elasticsearch, Logstash, and Kibana configuration files optimized for Kubernetes.
2. Provide a Docker Compose file or Kubernetes manifests for deploying the ELK stack.

### Example 2: Configuring Loki for a Docker Swarm

User request: "Configure Loki to aggregate logs from my Docker Swarm environment."

The skill will:
1. Generate a Loki configuration file optimized for Docker Swarm.
2. Provide instructions for deploying Loki as a service within the Swarm.

## Best Practices

- **Security**: Ensure that all generated configurations adhere to security best practices, including proper authentication and authorization mechanisms.
- **Scalability**: Design the log aggregation system to be scalable, allowing it to handle increasing log volumes over time.
- **Monitoring**: Implement monitoring for the log aggregation system itself to ensure its health and performance.

## Error Handling

- **Out of Memory**: "Elasticsearch heap space exhausted" - Solution: Increase heap size in elasticsearch.yml or add more nodes.
- **Connection Refused**: "Cannot connect to Elasticsearch" - Solution: Verify network connectivity and firewall rules.
- **Index Creation Failed**: "Failed to create index" - Solution: Check disk space and index template configuration.
- **Log Parsing Errors**: "Failed to parse log line" - Solution: Review grok patterns or JSON parsing configuration.

## Resources

- ELK Stack guide: https://www.elastic.co/guide/
- Loki documentation: https://grafana.com/docs/loki/
- Example configurations in `{baseDir}/log-aggregation-examples/`