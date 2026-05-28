---
id: gitops
name: "GitOps"
domain: OPS
skill: faion-devops-engineer
category: "best-practices-2026"
---

# GitOps

### Problem

Manual deployments cause inconsistency and drift.

### Solution: Git as Single Source of Truth

**Core Principles:**
1. **Declarative** - Infrastructure described in YAML, not imperative scripts
2. **Versioned and Immutable** - All config in Git with complete history
3. **Pulled Automatically** - Agents pull from Git, not pushed by CI
4. **Continuously Reconciled** - Automatic drift detection and correction

**Push vs Pull Models:**
| Model | Best For |
|-------|----------|
| Pull-based (ArgoCD, Flux) | Security, autonomy, resilience, multi-cluster |
| Push-based | Tight control, sequencing, existing CI/CD pipelines |
| Hybrid (2026) | Push for velocity, pull for safety and drift correction |

**Workflow:**
```
Build (CI: Jenkins/GitHub Actions)
    |
Push manifest to Git
    |
Deploy (CD: ArgoCD/Flux)
    |
Continuous reconciliation
```

**Tools Comparison:**

| Tool | Strengths |
|------|-----------|
| ArgoCD | Web UI, multi-cluster (100+ clusters), RBAC with SSO |
| Flux | Lightweight, multi-source syncs, progressive delivery |
| Kargo (Akuity) | Multi-environment promotion (staging -> production) |
| Flagger | Automated canary deployments |
| Spinnaker | Multi-cloud CD, advanced deployment strategies |

**Advanced Patterns (2025-2026):**

**Multi-Cluster Management:**
- Manage 100+ clusters from single ArgoCD instance
- Hub-spoke architecture for fleet management
- Cluster fleet provisioning and bootstrapping

**Progressive Delivery:**
- Canary deployments with automated rollback
- Blue-green with traffic shifting
- ArgoCD + Helm + Flagger integration
- AI-powered deployment (Akuity AI - September 2025): auto-rollback on failure

**Stats 2025-2026:**
- 90%+ Kubernetes deployments managed via GitOps principles
- 93% organizations plan to continue/increase GitOps
- 80%+ adopters report higher reliability
- Two-thirds of organizations adopted by mid-2025

**Implementation Timeline:**
| Phase | Activities |
|-------|------------|
| Week 1-2 | Assess current state, design target architecture |
| Month 1 | Basic GitOps + security/compliance integration |
| Month 2-3 | Multi-cluster management + progressive delivery |
| Month 4-6 | Self-service developer platforms + advanced automation |

**Best Practices:**
- Separate CI (build/test) from CD (deploy)
- Use drift detection and auto-remediation
- Implement progressive delivery (canary, blue-green)
- Choose ArgoCD for powerful UI; Flux for modular workflows
