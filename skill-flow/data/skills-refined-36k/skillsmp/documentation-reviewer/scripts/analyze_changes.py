#!/usr/bin/env python3
"""
Analyze git changes and identify documentation needs.

Usage:
    python analyze_changes.py [commit_range]

Examples:
    python analyze_changes.py           # Compare HEAD with HEAD~1
    python analyze_changes.py HEAD~5    # Compare HEAD with HEAD~5
    python analyze_changes.py main      # Compare HEAD with main branch
"""

import subprocess
import sys
from pathlib import Path
from collections import defaultdict

# Mapping patterns to documentation targets
MAPPING_RULES = {
    # === Python/Django ===
    "backend/app/views.py": ["docs/api/endpoints.md"],
    "backend/app/models.py": ["docs/api/endpoints.md", "docs/architecture/backend.md"],
    "backend/app/serializers.py": ["docs/api/endpoints.md"],
    "backend/app/urls.py": ["docs/api/endpoints.md"],
    "backend/app/management/commands/": ["docs/development/"],
    "backend/settings": ["docs/getting-started/", "docs/architecture/backend.md"],
    "pyproject.toml": ["docs/getting-started/installation.md"],
    "requirements.txt": ["docs/getting-started/installation.md"],
    "setup.py": ["docs/getting-started/installation.md"],

    # === TypeScript/JavaScript/React ===
    "frontend/src/features/": ["docs/features/", "docs/architecture/frontend.md"],
    "frontend/src/components/": ["docs/architecture/frontend.md"],
    "frontend/src/routes/": ["docs/architecture/frontend.md"],
    "frontend/src/api/": ["docs/api/"],
    "frontend/app/features/": ["docs/features/", "docs/architecture/frontend.md"],
    "frontend/app/components/": ["docs/architecture/frontend.md"],
    "frontend/app/routes/": ["docs/architecture/frontend.md"],
    "frontend/app/api/": ["docs/api/"],
    "frontend/package.json": ["docs/getting-started/installation.md"],
    "package.json": ["docs/getting-started/installation.md"],
    "tsconfig.json": ["docs/development/"],

    # === Go ===
    "go.mod": ["docs/getting-started/installation.md"],
    "go.sum": ["docs/getting-started/installation.md"],
    "cmd/": ["docs/development/commands.md", "docs/getting-started/"],
    "pkg/": ["docs/api/", "docs/architecture/"],
    "internal/": ["docs/architecture/"],
    "/handlers/": ["docs/api/endpoints.md"],
    "/routes/": ["docs/api/endpoints.md"],
    "/api/": ["docs/api/"],

    # === Rust ===
    "Cargo.toml": ["docs/getting-started/installation.md"],
    "src/lib.rs": ["docs/api/"],
    "src/main.rs": ["docs/getting-started/"],
    "src/bin/": ["docs/development/commands.md"],

    # === Java/Kotlin ===
    "build.gradle": ["docs/getting-started/installation.md"],
    "pom.xml": ["docs/getting-started/installation.md"],
    "src/main/java/": ["docs/api/", "docs/architecture/"],
    "src/main/kotlin/": ["docs/api/", "docs/architecture/"],

    # === Ruby ===
    "Gemfile": ["docs/getting-started/installation.md"],
    "config/routes.rb": ["docs/api/endpoints.md"],
    "app/controllers/": ["docs/api/endpoints.md"],
    "app/models/": ["docs/architecture/"],

    # === Task Runners ===
    "justfile": ["docs/development/commands.md"],
    "Justfile": ["docs/development/commands.md"],
    "just/": ["docs/development/commands.md"],
    "Makefile": ["docs/development/commands.md"],
    "tasks/": ["docs/development/invoke-tasks.md"],
    "scripts/": ["docs/development/"],

    # === Infrastructure/DevOps ===
    "docker/": ["docs/architecture/docker.md"],
    "docker-compose": ["docs/architecture/docker.md"],
    "Dockerfile": ["docs/architecture/docker.md"],
    ".dockerfile": ["docs/architecture/docker.md"],
    "nginx/": ["docs/architecture/docker.md"],
    "kubernetes/": ["docs/architecture/deployment.md"],
    "k8s/": ["docs/architecture/deployment.md"],
    "helm/": ["docs/architecture/deployment.md"],
    ".github/workflows/": ["docs/development/ci-cd.md"],
    ".gitlab-ci": ["docs/development/ci-cd.md"],
    "terraform/": ["docs/architecture/infrastructure.md"],
    "ansible/": ["docs/architecture/infrastructure.md"],

    # === Configuration ===
    "mkdocs.yml": ["mkdocs.yml (nav structure)"],
    ".env.example": ["docs/getting-started/installation.md"],
    "config/": ["docs/getting-started/", "docs/architecture/"],
}

# Patterns that indicate new exports/APIs
# Format: (pattern, description, extensions_or_filenames)
# Extensions start with ".", filenames are exact matches
HIGH_PRIORITY_PATTERNS = [
    # === Python/Django ===
    ("@api_view", "New API endpoint", [".py"]),
    ("@task", "New invoke task", [".py"]),
    ("class Meta:", "Django model/serializer", [".py"]),
    ("models.Model", "New Django model", [".py"]),
    ("APIView", "New API view class", [".py"]),
    ("@router.", "New FastAPI route", [".py"]),
    ("@app.route", "New Flask route", [".py"]),
    ("INSTALLED_APPS", "App configuration change", [".py"]),

    # === TypeScript/JavaScript/React ===
    ("export default function", "New React component", [".tsx", ".ts", ".jsx", ".js"]),
    ("export function", "New exported function", [".tsx", ".ts", ".jsx", ".js"]),
    ("export const", "New exported const", [".tsx", ".ts", ".jsx", ".js"]),
    ("export {", "New module export", [".tsx", ".ts", ".jsx", ".js"]),
    ("createRoute", "New route definition", [".tsx", ".ts"]),
    ("createFileRoute", "New file route", [".tsx", ".ts"]),
    ("createLazyFileRoute", "New lazy route", [".tsx", ".ts"]),

    # === Go ===
    ("func (", "New method", [".go"]),
    ("func New", "New constructor", [".go"]),
    ("func Handle", "New handler", [".go"]),
    ("type ", "New type definition", [".go"]),
    ("http.Handle", "New HTTP route", [".go"]),
    ("r.GET(", "New GET route (gin)", [".go"]),
    ("r.POST(", "New POST route (gin)", [".go"]),
    ("e.GET(", "New GET route (echo)", [".go"]),
    ("e.POST(", "New POST route (echo)", [".go"]),
    ("require (", "New Go dependencies", ["go.mod"]),
    ("require ", "New Go dependency", ["go.mod"]),

    # === Rust ===
    ("pub fn", "New public function", [".rs"]),
    ("pub struct", "New public struct", [".rs"]),
    ("pub enum", "New public enum", [".rs"]),
    ("pub trait", "New public trait", [".rs"]),
    ("impl ", "New implementation", [".rs"]),
    ("#[derive(", "New derive macro", [".rs"]),
    ("[[bin]]", "New binary target", ["Cargo.toml"]),
    ("[dependencies]", "Dependencies section", ["Cargo.toml"]),

    # === Java/Kotlin ===
    ("public class", "New public class", [".java"]),
    ("public interface", "New public interface", [".java"]),
    ("@RestController", "New REST controller", [".java", ".kt"]),
    ("@GetMapping", "New GET endpoint", [".java", ".kt"]),
    ("@PostMapping", "New POST endpoint", [".java", ".kt"]),
    ("@RequestMapping", "New request mapping", [".java", ".kt"]),
    ("fun ", "New Kotlin function", [".kt"]),
    ("class ", "New Kotlin class", [".kt"]),

    # === Ruby/Rails ===
    ("def ", "New method", [".rb"]),
    ("class ", "New class", [".rb"]),
    ("get '", "New GET route", [".rb"]),
    ("post '", "New POST route", [".rb"]),
    ("resources :", "New resource routes", [".rb"]),
    ("gem '", "New gem dependency", ["Gemfile"]),

    # === Just/Make task runners ===
    (":", "New task", ["justfile", "Justfile"]),
    ("@", "New recipe line", ["justfile", "Justfile"]),
    (":", "New make target", ["Makefile"]),

    # === CI/CD ===
    ("- name:", "New CI step", [".yml", ".yaml"]),
    ("jobs:", "New CI jobs", [".yml", ".yaml"]),
    ("stage:", "New CI stage", [".yml", ".yaml"]),

    # === Docker ===
    ("FROM ", "New base image", ["Dockerfile"]),
    ("EXPOSE ", "New exposed port", ["Dockerfile"]),
    ("services:", "New docker services", [".yml", ".yaml"]),
]


def run_git_command(args: list[str]) -> str:
    """Run a git command and return output."""
    try:
        result = subprocess.run(
            ["git"] + args,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Git error: {e.stderr}")
        sys.exit(1)


def get_changed_files(base: str = "HEAD~1") -> list[str]:
    """Get list of changed files compared to base."""
    output = run_git_command(["diff", "--name-only", base])
    return [f for f in output.split("\n") if f]


def get_diff_content(base: str, file_path: str) -> str:
    """Get diff content for a specific file."""
    try:
        return run_git_command(["diff", base, "--", file_path])
    except:
        return ""


def map_file_to_docs(file_path: str) -> list[str]:
    """Map a changed file to relevant documentation targets."""
    targets = []
    for pattern, docs in MAPPING_RULES.items():
        if pattern in file_path:
            targets.extend(docs)
    return list(set(targets))


def detect_high_priority_changes(diff_content: str, file_path: str) -> list[str]:
    """Detect patterns that indicate must-document changes."""
    findings = []
    path = Path(file_path)
    file_ext = path.suffix
    file_name = path.name

    for line in diff_content.split("\n"):
        if not line.startswith("+"):
            continue
        for pattern, description, matchers in HIGH_PRIORITY_PATTERNS:
            # Check if file matches (extension or exact filename)
            matches = False
            for matcher in matchers:
                if matcher.startswith("."):
                    # Extension match
                    if file_ext == matcher:
                        matches = True
                        break
                else:
                    # Exact filename match
                    if file_name == matcher:
                        matches = True
                        break
            if not matches:
                continue
            if pattern in line:
                # Clean up the line for display
                clean_line = line[1:].strip()[:70]
                findings.append(f"{description}: {clean_line}")
    return findings


def analyze_changes(base: str = "HEAD~1"):
    """Analyze changes and produce documentation report."""
    print(f"Analyzing changes from {base} to HEAD...\n")

    changed_files = get_changed_files(base)
    if not changed_files:
        print("No changes detected.")
        return

    print(f"Changed files ({len(changed_files)}):")
    for f in changed_files:
        print(f"  - {f}")
    print()

    # Map changes to documentation
    doc_targets = defaultdict(list)
    for file_path in changed_files:
        targets = map_file_to_docs(file_path)
        for target in targets:
            doc_targets[target].append(file_path)

    if doc_targets:
        print("Documentation targets:")
        for target, sources in sorted(doc_targets.items()):
            print(f"\n  {target}")
            for src in sources:
                print(f"    <- {src}")
    else:
        print("No documentation mapping found for changed files.")

    # Detect high-priority changes
    print("\n" + "=" * 60)
    print("High-Priority Changes (must document):")
    print("=" * 60)

    high_priority_found = False
    for file_path in changed_files:
        diff = get_diff_content(base, file_path)
        findings = detect_high_priority_changes(diff, file_path)
        if findings:
            high_priority_found = True
            print(f"\n{file_path}:")
            for finding in findings:
                print(f"  ! {finding}")

    if not high_priority_found:
        print("\nNo high-priority patterns detected.")

    # Summary
    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    print(f"Files changed: {len(changed_files)}")
    print(f"Documentation targets: {len(doc_targets)}")
    print(f"High-priority items: {'Yes' if high_priority_found else 'None detected'}")


def main():
    base = sys.argv[1] if len(sys.argv) > 1 else "HEAD~1"
    analyze_changes(base)


if __name__ == "__main__":
    main()
