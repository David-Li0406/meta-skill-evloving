---
name: managing-database-replication
description: Use this skill when you need to manage database replication, configure failover, or ensure high availability for databases like PostgreSQL or MySQL.
---

# Skill body

## Overview

This skill empowers Claude to automate and streamline database replication processes, ensuring high availability and data consistency across multiple database instances. It simplifies the configuration and management of complex replication topologies.

## How It Works

1. **Initialization**: The skill activates the database-replication-manager plugin upon detecting relevant keywords.
2. **Configuration**: The skill prompts the user for database connection details, replication type (physical/logical), and desired configuration parameters (e.g., failover settings, replication lag thresholds).
3. **Implementation**: The plugin generates and executes the necessary commands to configure database replication based on the user's specifications.

## When to Use This Skill

This skill activates when you need to:
- Set up a new database replication environment.
- Configure automatic failover for a database cluster.
- Monitor replication lag and trigger alerts based on defined thresholds.
- Implement read scaling by distributing read queries across multiple replicas.

## Examples

### Example 1: Setting up Master-Slave Replication

User request: "Set up master-slave replication for my PostgreSQL database with automatic failover."

The skill will:
1. Activate the database-replication-manager plugin.
2. Guide the user through the configuration process, prompting for connection details and failover settings.
3. Generate and execute the necessary PostgreSQL commands to establish master-slave replication and configure automatic failover.

### Example 2: Monitoring Replication Lag

User request: "Monitor replication lag on my MySQL replica and alert me if it exceeds 5 seconds."

The skill will:
1. Activate the database-replication-manager plugin.
2. Configure replication lag monitoring for the specified MySQL replica.