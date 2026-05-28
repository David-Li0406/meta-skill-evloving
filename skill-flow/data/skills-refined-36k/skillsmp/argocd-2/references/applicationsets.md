# ArgoCD ApplicationSets

ApplicationSets generate multiple Applications from templates using generators.

## Basic Structure

```yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: myappset
  namespace: argocd
spec:
  generators:
    - <generator>
  template:
    metadata:
      name: '{{name}}'
    spec:
      project: default
      source:
        repoURL: https://github.com/org/repo.git
        targetRevision: HEAD
        path: '{{path}}'
      destination:
        server: '{{server}}'
        namespace: '{{namespace}}'
```

## List Generator

Fixed list of parameter sets:

```yaml
spec:
  generators:
    - list:
        elements:
          - cluster: production
            url: https://prod.example.com
            namespace: prod
          - cluster: staging
            url: https://staging.example.com
            namespace: staging
  template:
    metadata:
      name: 'myapp-{{cluster}}'
    spec:
      destination:
        server: '{{url}}'
        namespace: '{{namespace}}'
```

## Cluster Generator

Generate from registered ArgoCD clusters:

```yaml
spec:
  generators:
    - clusters:
        selector:
          matchLabels:
            env: production
        # Or match all clusters:
        # selector: {}
  template:
    metadata:
      name: 'myapp-{{name}}'
    spec:
      destination:
        server: '{{server}}'
        namespace: myapp
```

Built-in parameters: `{{name}}`, `{{server}}`, `{{metadata.labels.<key>}}`, `{{metadata.annotations.<key>}}`

## Git Generator - Directory

Generate from directories in a Git repo:

```yaml
spec:
  generators:
    - git:
        repoURL: https://github.com/org/repo.git
        revision: HEAD
        directories:
          - path: apps/*
          - path: apps/excluded
            exclude: true
  template:
    metadata:
      name: '{{path.basename}}'
    spec:
      source:
        path: '{{path}}'
```

Parameters: `{{path}}`, `{{path.basename}}`, `{{path[n]}}`

## Git Generator - Files

Generate from JSON/YAML files:

```yaml
spec:
  generators:
    - git:
        repoURL: https://github.com/org/repo.git
        revision: HEAD
        files:
          - path: "config/**/config.json"
  template:
    metadata:
      name: '{{name}}'
    spec:
      source:
        path: '{{path}}'
      destination:
        namespace: '{{namespace}}'
```

File content fields become template parameters.

## Matrix Generator

Combine two generators (cartesian product):

```yaml
spec:
  generators:
    - matrix:
        generators:
          - clusters:
              selector:
                matchLabels:
                  env: production
          - list:
              elements:
                - app: frontend
                  path: apps/frontend
                - app: backend
                  path: apps/backend
  template:
    metadata:
      name: '{{name}}-{{app}}'
    spec:
      source:
        path: '{{path}}'
      destination:
        server: '{{server}}'
```

## Merge Generator

Combine generators with override priority:

```yaml
spec:
  generators:
    - merge:
        mergeKeys:
          - cluster
        generators:
          - clusters: {}
          - list:
              elements:
                - cluster: production
                  replicas: "5"
```

## Pull Request Generator

Generate from open PRs:

```yaml
spec:
  generators:
    - pullRequest:
        github:
          owner: org
          repo: myrepo
          tokenRef:
            secretName: github-token
            key: token
        filters:
          - branchMatch: "feature-.*"
  template:
    metadata:
      name: 'pr-{{number}}'
    spec:
      source:
        targetRevision: '{{head_sha}}'
```

## Sync Policy

```yaml
spec:
  syncPolicy:
    preserveResourcesOnDeletion: true  # Don't delete apps when AppSet deleted
  template:
    spec:
      syncPolicy:
        automated:
          prune: true
          selfHeal: true
```

## Go Templating

Enable Go templates for advanced logic:

```yaml
spec:
  goTemplate: true
  goTemplateOptions: ["missingkey=error"]
  template:
    metadata:
      name: '{{.name | lower}}'
      {{- if .labels }}
      labels:
        {{- range $k, $v := .labels }}
        {{ $k }}: {{ $v }}
        {{- end }}
      {{- end }}
```

## Progressive Syncs (Rolling Update)

```yaml
spec:
  strategy:
    type: RollingSync
    rollingSync:
      steps:
        - matchExpressions:
            - key: env
              operator: In
              values: [staging]
        - matchExpressions:
            - key: env
              operator: In
              values: [production]
          maxUpdate: 25%  # Update 25% at a time
```
