# IaC & DevSecOps Review Standards (Dec 2025)
## 1. Governance & Platform Engineering
In 2025, IaC is the "Product" of the Platform Team. Review for reusability, safety, and cognitive load reduction.
### The Self-Service Check
- [ ] **Module Standardization:** Are developers using "Golden Modules" from an Internal Service Catalog (e.g., Backstage) rather than writing raw VPCs/S3s?
- [ ] **Policy-as-Code (OPA):** Are OPA/Rego tests running in CI to block non-compliant infra? (e.g., "No public S3 buckets," "Encryption-at-rest mandatory").
- [ ] **Ephemeral Lifecycle:** Do PR-triggered "Preview Environments" include automatic TTL (Time-To-Live) cleanup to avoid cost sprawl?
## 2. Security & Zero Trust Infrastructure
"Log in, don't break in." The focus is on **Identity** over **Secrets**.
### Non-Human Identity (NHI) & Secrets
- [ ] **Workload Identity (OIDC):** Are CI/CD runners (GitHub Actions/GitLab) using OIDC to assume cloud roles? (🔴 **Critical:** Ban long-lived `AWS_ACCESS_KEY_ID`).
- [ ] **Dynamic Secrets:** Are database credentials generated JIT (Just-In-Time) via Vault or Infisical, or are they static strings?
- [ ] **State Security:** If using OpenTofu, is **Native State Encryption** enabled? If Terraform, is the state backend (S3/GCS) encrypted with a customer-managed KMS key?
### Network & Perimeter
- [ ] **Zero-Trust Networking:** Are internal services using **mTLS** or identity-aware proxies (Cloudflare Tunnel/Tailscale) instead of open Security Groups?
- [ ] **Egress Lockdown:** Is egress traffic restricted to a known allowlist to prevent data exfiltration?
## 3. Tooling & Ecosystem (Terraform vs. OpenTofu)
By late 2025, the choice between Terraform (BSL) and OpenTofu (MPL) is a strategic compliance decision.
| Feature | Review Requirement |
| :--- | :--- |
| **Governance** | Verify the provider registry is trusted and locked. |
| **Compatibility** | Ensure HCL features used (like `removed` blocks) are supported by the chosen binary. |
| **Migration** | For Terraform -> OpenTofu migrations, verify state file version compatibility. |
## 4. FinOps: Cost-as-Code
Infrastructure efficiency is now a performance metric.
- [ ] **Cost Impact Analysis:** Does the PR include an **Infracost** or similar breakdown? Flag any change that increases spend by >15% without justification.
- [ ] **Right-Sizing:** Are instance types matched to the workload? (e.g., No `m5.large` for a simple cron job; use `t4g.nano` or Serverless).
- [ ] **Graviton/ARM Priority:** Are workloads using Graviton4 (AWS) or Ampere (GCP/Azure) to maximize price-performance and reduce carbon?
## 5. Deployment & Reliability
- [ ] **Database Branching:** Are database changes tested against a data branch (Neon/PlanetScale) before hitting staging?
- [ ] **Drift Detection:** Is there an automated process (e.g., DriftCTL or Flux/ArgoCD) to detect manual "Console changes" and alert the team?
- [ ] **Artifact Integrity:** Are container images and IaC plans signed (Cosign/Sigstore) to verify they haven't been tampered with in the pipeline?
