---
name: server-management
description: Use this skill when you need to manage server operations effectively, focusing on process management, monitoring strategies, and scaling decisions.
---

# Server Management

> Server management principles for production operations.
> **Learn to THINK, not memorize commands.**

## 1. Process Management Principles

### Tool Selection

| Scenario          | Tool                     |
| ----------------- | ------------------------ |
| **Node.js app**   | PM2 (clustering, reload) |
| **Any app**       | systemd (Linux native)   |
| **Containers**    | Docker/Podman            |
| **Orchestration** | Kubernetes, Docker Swarm |

### Process Management Goals

| Goal                     | What It Means           |
| ------------------------ | ----------------------- |
| **Restart on crash**     | Auto-recovery           |
| **Zero-downtime reload** | No service interruption |
| **Clustering**           | Use all CPU cores       |
| **Persistence**          | Survive server reboot   |

## 2. Monitoring Principles

### What to Monitor

| Category         | Key Metrics               |
| ---------------- | ------------------------- |
| **Availability** | Uptime, health checks     |
| **Performance**  | Response time, throughput |
| **Errors**       | Error rate, types         |
| **Resources**    | CPU, memory, disk         |

### Alert Severity Strategy

| Level        | Response         |
| ------------ | ---------------- |
| **Critical** | Immediate action |
| **Warning**  | Investigate soon |
| **Info**     | Review daily     |

### Monitoring Tool Selection

| Need               | Options              |
| ------------------ | -------------------- |
| Simple/Free        | PM2 metrics, htop    |
| Full observability | Grafana, Datadog     |
| Error tracking     | Sentry               |
| Uptime             | UptimeRobot, Pingdom |

## 3. Log Management Principles

### Log Strategy

| Log Type             | Purpose          |
| -------------------- | ---------------- |
| **Application logs** | Debug, audit     |
| **Access logs**      | Traffic analysis |
| **Error logs**       | Issue detection  |

### Log Principles

1. **Rotate logs** to prevent disk fill
2. **Structured logging** (JSON) for parsing
3. **Appropriate levels** (error/warn/info/debug)
4. **No sensitive data** in logs

## 4. Scaling Decisions

### When to Scale

| Symptom        | Solution                     |
| ---------------| -----------------------------|
| High CPU       | Add instances (horizontal)   |
| High memory    | Increase RAM or fix leak     |
| Slow response  | Profile first, then scale    |
| Traffic spikes | Auto-scaling                 |

### Scaling Strategy

| Type         | When to Use                     |
|--------------|----------------------------------|
| **Vertical** | Quick fix, single instance       |
| **Horizontal** | Sustainable, distributed       |
| **Auto**     | Variable traffic                 |

## 5. Health Check Principles

### What Constitutes Healthy

| Check | Meaning |
|-------|---------|
| Uptime | Service is running without interruption |
| Response Time | Service responds within acceptable limits |
| Resource Usage | CPU and memory usage are within thresholds |