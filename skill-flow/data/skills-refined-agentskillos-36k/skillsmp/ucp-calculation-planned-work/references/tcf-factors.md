# Technical Complexity Factors (TCF) Reference

## Overview

Technical Complexity Factor (TCF) measures the technical characteristics of the system being developed. It ranges from 0.6 to 1.4 (typically 0.8-1.2 for most projects).

**Formula:**
```
TFactor = Σ(Rating × Weight) for all factors
TCF = 0.6 + (0.01 × TFactor)
TCF (capped) = min(TCF, 1.4)
```

---

## Standard Technical Factors (T1-T13)

### T1: Distributed System (Weight: 2.0)

**Definition:** System operates across multiple processes, servers, or geographical locations.

| Rating | Criteria | Example |
|--------|----------|---------|
| 0 | Monolithic, single process | Standalone desktop app |
| 1-2 | Client-server architecture | Web app with database |
| 3-4 | Multi-service distributed system | Microservices, message queues, caching |
| 5 | Complex distributed architecture | Global CDN, multi-region failover, orchestration |

### T2: Response Time/Performance (Weight: 1.0)

**Definition:** Requirements for system response time and performance.

| Rating | Criteria | Example |
|--------|----------|---------|
| 0 | No specific requirements | Batch processing, offline reports |
| 1-2 | General responsiveness expected | <5s page loads acceptable |
| 3-4 | Specific performance targets | <2s API responses, <500ms queries |
| 5 | Real-time/sub-second requirements | <100ms responses, streaming data |

### T3: End-user Efficiency (Weight: 1.0)

**Definition:** How efficient the UI/UX needs to be for user productivity.

| Rating | Criteria | Example |
|--------|----------|---------|
| 0 | Admin-only, occasional use | Deployment scripts, config tools |
| 1-2 | Standard web UI | Basic CRUD forms |
| 3-4 | Optimized UX with keyboard shortcuts | Power-user features, bulk operations |
| 5 | Highly optimized workflow | Context-aware suggestions, AI assistance |

### T4: Complex Internal Processing (Weight: 1.0)

**Definition:** Complexity of business logic and internal algorithms.

| Rating | Criteria | Example |
|--------|----------|---------|
| 0 | Simple CRUD operations | Direct database reads/writes |
| 1-2 | Basic validation and transformation | Form validation, data mapping |
| 3-4 | Complex business rules | Multi-step workflows, orchestration |
| 5 | Advanced algorithms | AI/ML models, consensus algorithms, graph processing |

### T5: Code Reusability (Weight: 1.0)

**Definition:** Extent to which code must be reusable across contexts.

| Rating | Criteria | Example |
|--------|----------|---------|
| 0 | Single-use, disposable code | Proof-of-concept, throwaway scripts |
| 1-2 | Some shared utilities | Shared helper functions |
| 3-4 | Modular architecture with reusable components | Component library, service layer |
| 5 | Framework or SDK for other teams | Plugin architecture, public SDK |

### T6: Easy to Install (Weight: 0.5)

**Definition:** Complexity of installation and deployment.

| Rating | Criteria | Example |
|--------|----------|---------|
| 0 | No installation (SaaS) | Cloud-hosted, web-only |
| 1-2 | Simple installer | npm install, Docker pull |
| 3-4 | Multi-step installation | Database setup, service configuration |
| 5 | Complex deployment | Multi-server orchestration, infrastructure provisioning |

### T7: Easy to Use (Weight: 0.5)

**Definition:** How intuitive and learnable the system is.

| Rating | Criteria | Example |
|--------|----------|---------|
| 0 | No UI (API only) | Headless service |
| 1-2 | Self-explanatory UI | Standard web forms |
| 3-4 | Some training required | Admin dashboards, specialized tools |
| 5 | Significant training needed | Complex workflows, domain-specific UI |

### T8: Portability (Weight: 2.0)

**Definition:** Ability to run on different platforms/environments.

| Rating | Criteria | Example |
|--------|----------|---------|
| 0 | Single platform only | Windows-only .NET Framework app |
| 1-2 | Cross-platform with dependencies | Node.js app requiring specific OS versions |
| 3-4 | Container-ready | Docker support, cloud-agnostic |
| 5 | Fully portable | Docker + Kubernetes, multi-cloud, edge deployment |

### T9: Easy to Change (Weight: 1.0)

**Definition:** Maintainability and ability to make changes.

| Rating | Criteria | Example |
|--------|----------|---------|
| 0 | Throwaway prototype | Proof-of-concept |
| 1-2 | Basic structure, some documentation | Monolithic app with limited docs |
| 3-4 | Modular with good documentation | Service-oriented, clear architecture |
| 5 | Highly maintainable | Plugin architecture, comprehensive docs, automated tests |

### T10: Concurrent Users (Weight: 1.0)

**Definition:** Number of simultaneous users supported.

| Rating | Criteria | Example |
|--------|----------|---------|
| 0 | Single user | Desktop app, personal tool |
| 1-2 | <10 concurrent users | Small team tool |
| 3-4 | 10-100 concurrent users | Department-level app |
| 5 | >100 concurrent users | Enterprise multi-tenant system |

### T11: Security Features (Weight: 1.0)

**Definition:** Security requirements and implementation complexity.

| Rating | Criteria | Example |
|--------|----------|---------|
| 0 | No security (internal/trusted) | Development tools, local scripts |
| 1-2 | Basic authentication | Login with password |
| 3-4 | Standard security practices | JWT, HTTPS, input validation, RBAC |
| 5 | Advanced security | Encryption at rest, audit logging, compliance (SOC 2, HIPAA) |

### T12: Direct Access for Third Parties (Weight: 1.0)

**Definition:** External system integrations and APIs.

| Rating | Criteria | Example |
|--------|----------|---------|
| 0 | No external access | Standalone system |
| 1-2 | Basic API for internal use | Internal REST API |
| 3-4 | Public API with documentation | REST API, webhooks, SDK |
| 5 | Complex integrations | Multiple protocols (REST, GraphQL, gRPC), rate limiting, versioning |

### T13: Special User Training (Weight: 1.0)

**Definition:** Training required for users to operate the system.

| Rating | Criteria | Example |
|--------|----------|---------|
| 0 | No training needed | Familiar web UI patterns |
| 1-2 | Brief orientation | Quick start guide sufficient |
| 3-4 | Formal training sessions | 1-2 day training course |
| 5 | Extensive training | Weeks of training, certification required |

---

## AI/ML-Specific Factors (T14-T20)

### T14: ML Model Complexity (Weight: 2.0)

**Definition:** Complexity of machine learning models used.

| Rating | Criteria | Example |
|--------|----------|---------|
| 0 | No ML | Traditional software |
| 1-2 | Simple models (pre-trained APIs) | OpenAI API calls, sentiment analysis |
| 3-4 | Custom fine-tuning or ensemble models | Fine-tuned models, multi-model consensus |
| 5 | Custom architecture development | Training from scratch, novel architectures |

### T15: Data Volume/Velocity (Weight: 2.0)

**Definition:** Scale and speed of data processing.

| Rating | Criteria | Example |
|--------|----------|---------|
| 0 | Small datasets (<1GB) | User-uploaded files |
| 1-2 | Medium datasets (1-100GB) | Document processing, embeddings |
| 3-4 | Large datasets (100GB-1TB) | Batch vector processing, web crawling |
| 5 | Very large/streaming (>1TB) | Real-time streaming, petabyte-scale |

### T16: Data Quality Challenges (Weight: 1.5)

**Definition:** Difficulty of data cleaning and validation.

| Rating | Criteria | Example |
|--------|----------|---------|
| 0 | Clean, structured data | JSON API responses |
| 1-2 | Standard validation needed | Form inputs, CSV files |
| 3-4 | Significant cleaning required | Web scraping, PDF parsing, Unicode handling |
| 5 | Extreme data quality issues | Legacy systems, OCR, multi-language corpora |

### T17: Model Explainability Needs (Weight: 1.0)

**Definition:** Requirements for explaining AI decisions.

| Rating | Criteria | Example |
|--------|----------|---------|
| 0 | No AI decisions | Traditional software |
| 1-2 | Black box acceptable | Content recommendations |
| 3-4 | Some explainability | Citation tracking, confidence scores |
| 5 | Full auditability required | Healthcare, legal, financial AI |

### T18: Real-time Inference Requirements (Weight: 1.5)

**Definition:** Speed requirements for AI model inference.

| Rating | Criteria | Example |
|--------|----------|---------|
| 0 | No AI | N/A |
| 1-2 | Batch processing acceptable | Overnight report generation |
| 3-4 | Near real-time (<5s) | Chat responses, search |
| 5 | Real-time (<1s) | Streaming responses, fraud detection |

### T19: MLOps Maturity Requirements (Weight: 1.0)

**Definition:** ML operations complexity (versioning, monitoring, etc.).

| Rating | Criteria | Example |
|--------|----------|---------|
| 0 | No ML | N/A |
| 1-2 | Manual model management | API key rotation |
| 3-4 | Basic MLOps | Model versioning, performance monitoring |
| 5 | Advanced MLOps | A/B testing, auto-retraining, model observability |

### T20: AI Bias & Fairness Requirements (Weight: 1.5)

**Definition:** Requirements to prevent and monitor AI bias.

| Rating | Criteria | Example |
|--------|----------|---------|
| 0 | No AI | N/A |
| 1-2 | Awareness, no formal requirements | Content filtering |
| 3-4 | Monitoring and mitigation | Input sanitization, prompt injection detection |
| 5 | Strict compliance | Regulated industries, fairness audits |

---

## Example Calculations

### Example 1: Enterprise Web Application (No AI)

```
T1: Distributed System = 3 × 2.0 = 6.0
T2: Response Time = 3 × 1.0 = 3.0
T3: End-user Efficiency = 4 × 1.0 = 4.0
T4: Complex Processing = 3 × 1.0 = 3.0
T5: Code Reusability = 4 × 1.0 = 4.0
T6: Easy to Install = 4 × 0.5 = 2.0
T7: Easy to Use = 3 × 0.5 = 1.5
T8: Portability = 4 × 2.0 = 8.0
T9: Easy to Change = 4 × 1.0 = 4.0
T10: Concurrent Users = 4 × 1.0 = 4.0
T11: Security Features = 4 × 1.0 = 4.0
T12: Third-Party Access = 3 × 1.0 = 3.0
T13: User Training = 3 × 1.0 = 3.0

TFactor = 49.5
TCF = 0.6 + (0.01 × 49.5) = 1.095 → 1.10
```

### Example 2: AI Agent Platform (Agent Studio Pro)

```
Standard Factors (T1-T13) = 59.0
T14: ML Model Complexity = 4 × 2.0 = 8.0
T15: Data Volume = 4 × 2.0 = 8.0
T16: Data Quality = 5 × 1.5 = 7.5
T17: Explainability = 3 × 1.0 = 3.0
T18: Real-time Inference = 4 × 1.5 = 6.0
T19: MLOps Maturity = 3 × 1.0 = 3.0
T20: Bias & Fairness = 3 × 1.5 = 4.5

TFactor = 59.0 + 40.0 = 99.0
TCF = 0.6 + (0.01 × 99.0) = 1.59 → 1.40 (capped)
```

---

## Interpretation Guidelines

| TCF Range | Interpretation |
|-----------|---------------|
| 0.60-0.80 | Below average technical complexity |
| 0.80-1.00 | Average complexity |
| 1.00-1.20 | Above average complexity |
| 1.20-1.40 | High technical complexity |

**Note:** Most enterprise projects fall in the 0.95-1.15 range. TCF values >1.30 indicate exceptional technical challenges.
