# Helm Wrapper Charts (m0sh1.cc)

## Table of Contents

1. Wrapper Chart Contract
2. Layout Options
3. Values and Templates
4. ArgoCD Source Path

## 1. Wrapper Chart Contract

- Wrapper charts are the contract boundary; upstream charts may change, wrappers must not.
- No direct Helm repo dependencies in ArgoCD Applications.
- Values live inside the wrapper folder.

## 2. Layout Options

Preferred layout (per repo guidelines):

- `apps/cluster/<name>/`
- `apps/user/<name>/`

Some existing charts may be at `apps/<scope>/<name>/` root. Use the repo's
current pattern or pass `--layout` in scaffolding.

## 3. Values and Templates

- Use `values.yaml` for image, service, ingress, resources, env.
- Avoid plaintext secrets; reference SealedSecrets via `envFrom` or mounted files.

## 4. ArgoCD Source Path

- Application `spec.source.path` should point at the wrapper chart directory.
- Use `path:` not `chart:` to avoid direct Helm repo dependency.
