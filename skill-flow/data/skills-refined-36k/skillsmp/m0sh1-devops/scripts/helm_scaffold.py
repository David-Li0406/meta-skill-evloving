#!/usr/bin/env python3
"""Helm scaffold for m0sh1.cc infra and helm-charts repos."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path
from typing import Optional


def detect_repo_type(repo: Path) -> str:
    if (repo / "apps").exists() and (repo / "cluster").exists():
        return "infra"
    if (repo / "charts").exists():
        return "helm-charts"
    return "unknown"


def detect_layout(repo: Path) -> str:
    # Prefer repo default layout under apps/<scope>/<name>/Chart.yaml.
    if list(repo.glob("apps/cluster/*/Chart.yaml")) or list(repo.glob("apps/user/*/Chart.yaml")):
        return "root"
    # Fallback to "helm" layout under apps/<scope>/<name> if present.
    helm_glob_cluster = str(Path("apps") / "cluster" / "*" / "helm" / "Chart.yaml")
    helm_glob_user = str(Path("apps") / "user" / "*" / "helm" / "Chart.yaml")
    if list(repo.glob(helm_glob_cluster)) or list(repo.glob(helm_glob_user)):
        return "helm"
    return "root"


def git_origin(repo: Path) -> Optional[str]:
    try:
        result = subprocess.run(
            ["git", "-C", str(repo), "remote", "get-url", "origin"],
            check=True,
            capture_output=True,
            text=True,
        )
        return result.stdout.strip() or None
    except Exception:
        return None


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def write_file(path: Path, content: str, force: bool) -> None:
    if path.exists() and not force:
        raise FileExistsError(f"File exists: {path}")
    path.write_text(content)


def scaffold_wrapper_chart(
    repo: Path,
    name: str,
    scope: str,
    layout: str,
    argocd: bool,
    disabled: bool,
    dest_namespace: Optional[str],
    repo_url: Optional[str],
    revision: str,
    force: bool,
) -> None:
    base_dir = repo / "apps" / scope / name
    chart_dir = base_dir / "helm" if layout == "helm" else base_dir

    ensure_dir(chart_dir / "templates")

    chart_yaml = f"""apiVersion: v2
name: {name}
version: 0.1.0
description: {name} wrapper chart
type: application
appVersion: \"0.1.0\"
"""

    values_yaml = """image:
  repository: example/image
  tag: "0.1.0"
  pullPolicy: IfNotPresent

service:
  port: 8080

envFromSecret: ""

env: {}

ingress:
  enabled: false
  className: traefik
  annotations: {}
  hosts:
    - host: example.m0sh1.cc
      paths:
        - path: /
          pathType: Prefix
  tls: []

resources:
  requests:
    cpu: 50m
    memory: 64Mi
  limits:
    cpu: 200m
    memory: 256Mi
"""

    deployment_yaml = f"""apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{'{{'}} .Release.Name {{'}}'}}
spec:
  replicas: 1
  selector:
    matchLabels:
      app: {name}
  template:
    metadata:
      labels:
        app: {name}
    spec:
      containers:
        - name: {name}
          image: \"{{'{{'}} .Values.image.repository {{'}}'}}:{{'{{'}} .Values.image.tag {{'}}'}}\"
          imagePullPolicy: {{'{{'}} .Values.image.pullPolicy {{'}}'}}
          ports:
            - containerPort: {{'{{'}} .Values.service.port {{'}}'}}
          env:
            {{'{{'}}- range $name, $value := .Values.env {{'}}'}}
            - name: {{'{{'}} $name {{'}}'}}
              value: {{'{{'}} $value | quote {{'}}'}}
            {{'{{'}}- end {{'}}'}}
          {{'{{'}}- if .Values.envFromSecret {{'}}'}}
          envFrom:
            - secretRef:
                name: {{'{{'}} .Values.envFromSecret {{'}}'}}
          {{'{{'}}- end {{'}}'}}
"""

    service_yaml = f"""apiVersion: v1
kind: Service
metadata:
  name: {{'{{'}} .Release.Name {{'}}'}}
  namespace: {{'{{'}} .Release.Namespace {{'}}'}}
  labels:
    app: {name}
{{'{{'}}- with .Values.service.annotations {{'}}'}}
  annotations:
    {{'{{'}}- toYaml . | nindent 4 {{'}}'}}
{{'{{'}}- end {{'}}'}}
spec:
  type: {{'{{'}} .Values.service.type | default \"ClusterIP\" {{'}}'}}
  ports:
    - name: http
      port: {{'{{'}} .Values.service.port {{'}}'}}
      targetPort: {{'{{'}} .Values.service.port {{'}}'}}
      protocol: TCP
  selector:
    app: {name}
"""

    ingress_yaml = """{{- if .Values.ingress.enabled }}
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: {{ .Release.Name }}
  namespace: {{ .Release.Namespace }}
{{- with .Values.ingress.annotations }}
  annotations:
    {{- toYaml . | nindent 4 }}
{{- end }}
spec:
  ingressClassName: {{ .Values.ingress.className | default "traefik" | quote }}
  rules:
  {{- range .Values.ingress.hosts }}
    - host: {{ .host | quote }}
      http:
        paths:
        {{- range .paths }}
          - path: {{ .path | quote }}
            pathType: {{ .pathType | default "Prefix" | quote }}
            backend:
              service:
                name: {{ $.Release.Name }}
                port:
                  number: {{ $.Values.service.port }}
        {{- end }}
  {{- end }}
{{- with .Values.ingress.tls }}
  tls:
  {{- range . }}
    - secretName: {{ .secretName }}
      hosts:
      {{- range .hosts }}
        - {{ . }}
      {{- end }}
  {{- end }}
{{- end }}
{{- end }}
"""

    write_file(chart_dir / "Chart.yaml", chart_yaml, force)
    write_file(chart_dir / "values.yaml", values_yaml, force)
    write_file(chart_dir / "templates" / "deployment.yaml", deployment_yaml, force)
    write_file(chart_dir / "templates" / "service.yaml", service_yaml, force)
    write_file(chart_dir / "templates" / "ingress.yaml", ingress_yaml, force)

    if argocd:
        app_base = repo / "argocd" / ("disabled" if disabled else "apps") / scope
        ensure_dir(app_base)
        app_path = app_base / f"{name}.yaml"

        repo_url = repo_url or git_origin(repo) or "REPO_URL"
        dest_ns = dest_namespace or ("apps" if scope == "user" else name)
        source_path = f"apps/{scope}/{name}"
        if layout == "helm":
            source_path = f"{source_path}/helm"

        app_yaml = f"""apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: {name}
  namespace: argocd
  labels:
    app.kubernetes.io/part-of: apps-root
spec:
  project: default

  source:
    repoURL: {repo_url}
    targetRevision: {revision}
    path: {source_path}
    helm:
      releaseName: {name}
      valueFiles:
        - values.yaml

  destination:
    server: https://kubernetes.default.svc
    namespace: {dest_ns}

  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
      - CreateNamespace=true
"""

        write_file(app_path, app_yaml, force)


def scaffold_chart(repo: Path, name: str, force: bool) -> None:
    chart_dir = repo / "charts" / name
    ensure_dir(chart_dir / "templates")

    chart_yaml = f"""apiVersion: v2
name: {name}
version: 0.1.0
description: {name} chart
type: application
appVersion: \"0.1.0\"
"""

    values_yaml = """image:
  repository: example/image
  tag: "0.1.0"
  pullPolicy: IfNotPresent

service:
  port: 8080

envFromSecret: ""

env: {}

resources:
  requests:
    cpu: 50m
    memory: 64Mi
  limits:
    cpu: 200m
    memory: 256Mi
"""

    deployment_yaml = f"""apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{'{{'}} .Release.Name {{'}}'}}
spec:
  replicas: 1
  selector:
    matchLabels:
      app: {name}
  template:
    metadata:
      labels:
        app: {name}
    spec:
      containers:
        - name: {name}
          image: \"{{'{{'}} .Values.image.repository {{'}}'}}:{{'{{'}} .Values.image.tag {{'}}'}}\"
          imagePullPolicy: {{'{{'}} .Values.image.pullPolicy {{'}}'}}
          ports:
            - containerPort: {{'{{'}} .Values.service.port {{'}}'}}
"""

    service_yaml = f"""apiVersion: v1
kind: Service
metadata:
  name: {{'{{'}} .Release.Name {{'}}'}}
  namespace: {{'{{'}} .Release.Namespace {{'}}'}}
  labels:
    app: {name}
spec:
  type: {{'{{'}} .Values.service.type | default \"ClusterIP\" {{'}}'}}
  ports:
    - name: http
      port: {{'{{'}} .Values.service.port {{'}}'}}
      targetPort: {{'{{'}} .Values.service.port {{'}}'}}
      protocol: TCP
  selector:
    app: {name}
"""

    write_file(chart_dir / "Chart.yaml", chart_yaml, force)
    write_file(chart_dir / "values.yaml", values_yaml, force)
    write_file(chart_dir / "templates" / "deployment.yaml", deployment_yaml, force)
    write_file(chart_dir / "templates" / "service.yaml", service_yaml, force)


def main() -> int:
    parser = argparse.ArgumentParser(description="Helm scaffold for m0sh1.cc repos")
    parser.add_argument("--repo", required=True, help="Path to infra or helm-charts repo")
    parser.add_argument("--name", required=True, help="Chart/app name")
    parser.add_argument("--repo-type", choices=["infra", "helm-charts", "auto"], default="auto")
    parser.add_argument("--scope", choices=["cluster", "user"], help="Required for infra repo")
    parser.add_argument("--layout", choices=["detect", "helm", "root"], default="detect")
    parser.add_argument("--argocd", action="store_true", help="Create ArgoCD Application stub")
    parser.add_argument("--disabled", action="store_true", help="Place Application under disabled")
    parser.add_argument("--dest-namespace", help="Destination namespace for ArgoCD Application")
    parser.add_argument("--repo-url", help="Override repoURL in ArgoCD Application")
    parser.add_argument("--revision", default="main", help="Git revision for ArgoCD Application")
    parser.add_argument("--force", action="store_true", help="Overwrite existing files")
    args = parser.parse_args()

    repo = Path(args.repo).resolve()
    if not repo.exists():
        print(f"Repo path does not exist: {repo}", file=sys.stderr)
        return 2

    repo_type = args.repo_type
    if repo_type == "auto":
        repo_type = detect_repo_type(repo)

    if repo_type == "infra":
        if not args.scope:
            print("--scope is required for infra repo", file=sys.stderr)
            return 2
        layout = args.layout
        if layout == "detect":
            layout = detect_layout(repo)
        scaffold_wrapper_chart(
            repo=repo,
            name=args.name,
            scope=args.scope,
            layout=layout,
            argocd=args.argocd,
            disabled=args.disabled,
            dest_namespace=args.dest_namespace,
            repo_url=args.repo_url,
            revision=args.revision,
            force=args.force,
        )
        print(f"Scaffolded wrapper chart in {repo}")
        return 0

    if repo_type == "helm-charts":
        scaffold_chart(repo=repo, name=args.name, force=args.force)
        print(f"Scaffolded chart in {repo}")
        return 0

    print("Could not detect repo type; use --repo-type", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
