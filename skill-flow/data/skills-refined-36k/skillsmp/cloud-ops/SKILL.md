---
name: cloud-ops
description: Infrastructure as Code (IaC), Containerization (Docker/K8s), and Cloud Best Practices (AWS/GCS).
---

# Cloud & DevOps Commander

## Containerization (Docker)
* **Multi-Stage Builds:** Always use multi-stage builds to minimize image size (e.g., `builder` stage vs `runner` stage).
* **Security:** Run containers as a non-root user.
* **Optimization:** Order `Dockerfile` instructions to maximize layer caching (copy `package.json` before source code).

## Kubernetes (K8s)
* **Liveness/Readiness:** Every deployment must define liveness and readiness probes.
* **Resources:** MUST define `requests` and `limits` for CPU and Memory.
* **Config:** strictly separate configuration (ConfigMaps/Secrets) from image artifacts.

## Cloud Provider Patterns (AWS & GCS)
* **IAM Least Privilege:** When generating IAM policies, grant only the specific permissions needed (no `*`).
* **Infrastructure as Code:** Prefer Terraform or Pulumi syntax over manual console clicks.
* **Storage:** For S3/GCS, enforce encryption at rest and lifecycle policies for cost management.

## Message Brokers (RabbitMQ / Kafka)
* **Idempotency:** Consumers must handle duplicate messages gracefully.
* **Dead Letter Queues (DLQ):** Always configure DLQs for failed messages.
* **Backpressure:** Ensure consumers can handle load spikes without crashing.