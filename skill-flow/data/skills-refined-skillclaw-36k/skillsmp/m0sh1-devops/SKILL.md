---
name: m0sh1-devops
description: >
  Use for DevOps work in m0sh1.cc homelab repos (infra and helm-charts), covering
  GitOps/ArgoCD rules, Helm wrapper charts, Terraform lab workflow, Ansible Vault
  boundaries, and supply-chain checks. Includes repo-specific guard/scaffold tools.
---

# m0sh1 DevOps

Repo-specific DevOps guidance and tools for the m0sh1.cc homelab.

## Integration with Custom Agent

This skill directory supports the **@m0sh1-devops** custom agent, which:

- Enforces all rules defined in this skill automatically
- Uses guard scripts (gitops_guard.py, helm_scaffold.py, etc.) as part of workflows
- Integrates Memory Bank for infrastructure decision logging
- Provides 12 specialized toolsets for GitOps workflows
- Accesses kubectl, Ansible, Terraform, and ArgoCD/Helm documentation

**Agent files:**

- Definition: `.github/agents/m0sh1-devops.agent.md`
- Toolsets: `.github/agents/m0sh1-devops.toolsets.jsonc`

**To use:** Type `@m0sh1-devops` in Copilot chat when working with infrastructure.

## Quick Start

```bash
# Validate GitOps hygiene in infra repo
python tools/m0sh1-devops/scripts/gitops_guard.py --repo /Users/smeya/git/m0sh1.cc/infra

# Scaffold a wrapper chart + ArgoCD Application
python tools/m0sh1-devops/scripts/helm_scaffold.py \
  --repo /Users/smeya/git/m0sh1.cc/infra \
  --scope user \
  --name example-app \
  --layout detect \
  --argocd

# Scaffold a standalone chart in helm-charts repo
python tools/m0sh1-devops/scripts/helm_scaffold.py \
  --repo /Users/smeya/git/m0sh1.cc/helm-charts \
  --name example-chart

# Validate Terraform lab conventions
python tools/m0sh1-devops/scripts/terraform_lab_guard.py --repo /Users/smeya/git/m0sh1.cc/infra

# Supply-chain checks (tags vs digests, workflow pinning)
python tools/m0sh1-devops/scripts/supply_chain_guard.py --repo /Users/smeya/git/m0sh1.cc/infra
```

## What This Skill Enforces

- **GitOps only**: No imperative kubectl/helm changes outside bootstrap recovery.
- **Wrapper charts**: Apps go under `apps/cluster` or `apps/user` (wrapper charts).
- **Secrets**: Ansible Vault for host/infra secrets; SealedSecrets for k8s.
- **Terraform**: Only `terraform/envs/lab` is valid; providers/backends live there.
- **Supply chain**: Prefer digests; document tag usage in `docs/history.md`.

## Use These Focused Skills When Needed

- Ansible workflows: `/Users/smeya/.codex/skills/ansible-homelab/SKILL.md`
- Ansible secrets: `/Users/smeya/.codex/skills/ansible-secrets/SKILL.md`

## References (Open When Needed)

- `references/gitops-argocd.md`
- `references/helm-wrappers.md`
- `references/terraform-lab.md`
- `references/supply-chain.md`
