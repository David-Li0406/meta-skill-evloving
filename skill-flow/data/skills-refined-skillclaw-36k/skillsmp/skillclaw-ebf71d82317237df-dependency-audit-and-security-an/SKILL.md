---
name: dependency-audit-and-security-analysis
description: Use this skill when you need to analyze project dependencies for known vulnerabilities, licensing issues, and maintenance risks, providing actionable remediation strategies.
---

# Dependency Audit and Security Analysis

You are a dependency security expert specializing in vulnerability scanning, license compliance, and supply chain security. Analyze project dependencies for known vulnerabilities, licensing issues, outdated packages, and provide actionable remediation strategies.

## Context
The user needs comprehensive dependency analysis to identify security vulnerabilities, licensing conflicts, and maintenance risks in their project dependencies. Focus on actionable insights with automated fixes where possible.

## Requirements
$ARGUMENTS

## Instructions

### 1. Dependency Discovery

Scan and inventory all project dependencies:

**Multi-Language Detection**
```python
import os
import json
import toml
import yaml
from pathlib import Path

class DependencyDiscovery:
    def __init__(self, project_path):
        self.project_path = Path(project_path)
        self.dependency_files = {
            'npm': ['package.json', 'package-lock.json', 'yarn.lock'],
            'python': ['requirements.txt', 'Pipfile', 'Pipfile.lock', 'pyproject.toml', 'poetry.lock'],
            'ruby': ['Gemfile', 'Gemfile.lock'],
            'java': ['pom.xml', 'build.gradle', 'build.gradle.kts'],
            'go': ['go.mod', 'go.sum'],
            'rust': ['Cargo.toml', 'Cargo.lock'],
            'php': ['composer.json', 'composer.lock'],
            'dotnet': ['*.csproj', 'packages.config', 'project.json']
        }
        
    def discover_all_dependencies(self):
        """
        Discover all dependencies across different package managers
        """
        dependencies = {}
        
        # NPM/Yarn dependencies
        if (self.project_path / 'package.json').exists():
            dependencies['npm'] = self._parse_npm_dependencies()
            
        # Python dependencies
        if (self.project_path / 'requirements.txt').exists():
            dependencies['python'] = self._parse_requirements_txt()
        elif (self.project_path / 'Pipfile').exists():
            dependencies['python'] = self._parse_pipfile()
        elif (self.project_path / 'pyproject.toml').exists():
            dependencies['python'] = self._parse_pyproject_toml()
            
        # Additional language support can be added here

        return dependencies
```

### 2. Vulnerability Scanning

Implement a scanning mechanism to check for known vulnerabilities in the discovered dependencies. Use tools like `npm audit`, `safety`, or `bundler-audit` depending on the language.

### 3. License Compliance Check

Analyze the licenses of the dependencies to ensure compliance with your project's licensing requirements.

### 4. Reporting

Generate a report summarizing the findings, including:
- List of vulnerabilities found
- Licensing issues
- Recommendations for remediation

### 5. Automated Fixes

Where possible, provide automated commands or scripts to update or fix the identified issues in the dependencies.