---
name: helm-chart-best-practices
description: Use this skill when authoring and maintaining Helm charts to ensure adherence to standardized conventions, effective templating, and optimal Kubernetes deployment patterns.
---

# Helm Chart Style Guide

This skill provides standardized conventions for authoring and maintaining Helm charts, focusing on:

- Global registry override using `.Values.global.image.registry`
- Clear, minimal templating
- Consistent `image:` blocks for all containers

## When to Use

Activate this skill when:

- Creating new Helm charts
- Reviewing or modifying existing Helm charts
- Configuring image registries for air-gapped environments
- Setting up multi-chart deployments with Helmfile

## Image Configuration Best Practices

All charts **must** support the top-level configuration for global image settings.

```yaml
global:
  image:
    registry: registry.mycompany.com
```

This enables centralized control of image sources across all dependencies and microservices.

### Consistent Image Blocks

All charts should follow a consistent `image:` block for every containerized application.

Fields should be templated for `registry`, `repository`, `tag`, `pullPolicy`, and `pullSecrets` for all containers.

Every chart **must** define all image values with reasonable defaults in `values.yaml`:

```yaml
prometheus:
  image:
    registry: docker.io
    repository: prom/prometheus
    tag: v2.52.0
    pullPolicy: IfNotPresent
```

### Templating Pattern for Registry Override

Use a registry value at the top of the template. This pattern ensures the ability to use internal registries (e.g., `registry.mycompany.com`) for air-gapped environments or mirrored image sources:

```gotmpl
{{- $registry := .Values.prometheus.image.registry | default .Values.global.image.registry | default "docker.io" -}}
image:
  registry: {{ $registry }}
  repository: {{ .Values.prometheus.image.repository }}
  tag: {{ .Values.prometheus.image.tag }}
  pullPolicy: {{ .Values.prometheus.image.pullPolicy }}
```

## Templating Conventions

Template **only when necessary**. Keep templates readable and manageable by avoiding over-templating.

**Template:**

- Labels
- Annotations
- Resource requests and limits for CPU and memory for each container
- Service port numbers and names

**Avoid Templating:**

- Most values already present in `values.yaml` unless dynamically constructed

## Linting

Ensure to lint your Helm charts regularly to catch potential issues early in the development process.