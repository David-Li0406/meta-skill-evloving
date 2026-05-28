# GitOps + ArgoCD (m0sh1.cc)

## Table of Contents

1. Source of Truth
2. App Layout Rules
3. ArgoCD Application Rules
4. Recovery Exceptions

## 1. Source of Truth

- Git is authoritative; reconcile reality to Git, not the other way around.
- Bootstrap is for first install and disaster recovery only.

## 2. App Layout Rules

- Wrapper charts live under:
  - `apps/cluster/<name>/` (cluster apps)
  - `apps/user/<name>/` (user apps)
- Disabled apps go only under:
  - `apps/argocd/disabled/`
- No environment overlays beyond `cluster/environments/lab/`.

## 3. ArgoCD Application Rules

- All workloads managed via ArgoCD Applications in `apps/argocd/applications/`.
- App-of-apps children must include label:
  - `app.kubernetes.io/part-of: apps-root`
- Do not use direct Helm repository dependencies in Applications.
  - Use wrapper charts in this repo and `path:` sources.

## 4. Recovery Exceptions

- `argocd.argoproj.io/skip-reconcile` is recovery-only.
- Any temporary imperative changes must be documented in `docs/history.md`.
