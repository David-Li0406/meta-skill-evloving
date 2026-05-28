#!/usr/bin/env python3
"""VCS provider detection and enumeration.

This module provides VCS provider detection from git remotes and configuration.

Constants:
- VCS URL patterns for GitHub and Azure DevOps
  Rationale: Enable automatic provider detection from git remote URLs
"""

import re
import subprocess
from enum import Enum


class VCSProvider(Enum):
    """Supported VCS providers."""

    GITHUB = "github"
    AZURE_DEVOPS = "azure_devops"


# URL patterns for provider detection
GITHUB_PATTERNS = [
    r"github\.com[:/]",  # https://github.com/user/repo or git@github.com:user/repo
]

AZURE_DEVOPS_PATTERNS = [
    r"dev\.azure\.com[/:]",  # https://dev.azure.com/org/project or git@ssh.dev.azure.com:v3
    r"@vs-ssh\.visualstudio\.com",  # git@vs-ssh.visualstudio.com:v3/org/project/repo
    r"\.visualstudio\.com/",  # https://org.visualstudio.com/project
]


def detect_from_remote() -> VCSProvider | None:
    """Detect VCS provider from git remote URL.

    Returns:
        VCSProvider if detected, None otherwise

    Example URLs:
        GitHub:
        - https://github.com/user/repo.git
        - git@github.com:user/repo.git

        Azure DevOps:
        - https://dev.azure.com/org/project/_git/repo
        - git@ssh.dev.azure.com:v3/org/project/repo
    """
    try:
        result = subprocess.run(["git", "remote", "get-url", "origin"], capture_output=True, text=True, check=True, timeout=5)
        remote_url = result.stdout.strip()

        # Check GitHub patterns
        for pattern in GITHUB_PATTERNS:
            if re.search(pattern, remote_url):
                return VCSProvider.GITHUB

        # Check Azure DevOps patterns
        for pattern in AZURE_DEVOPS_PATTERNS:
            if re.search(pattern, remote_url):
                return VCSProvider.AZURE_DEVOPS

        return None

    except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError):
        return None


def extract_azure_repo_from_remote() -> str | None:
    """Extract repository name from Azure DevOps git remote URL.

    Returns:
        Repository name if detected, None otherwise

    Example URLs and extracted repo names:
        - https://dev.azure.com/org/project/_git/repo → repo
        - git@ssh.dev.azure.com:v3/org/project/repo → repo
        - https://org.visualstudio.com/project/_git/repo → repo
    """
    try:
        result = subprocess.run(["git", "remote", "get-url", "origin"], capture_output=True, text=True, check=True, timeout=5)
        remote_url = result.stdout.strip()

        # Pattern 1: https://dev.azure.com/org/project/_git/repo
        match = re.search(r"/_git/([^/\s]+?)(?:\.git)?$", remote_url)
        if match:
            return match.group(1)

        # Pattern 2: git@ssh.dev.azure.com:v3/org/project/repo
        match = re.search(r":v3/[^/]+/[^/]+/([^/\s]+?)(?:\.git)?$", remote_url)
        if match:
            return match.group(1)

        return None

    except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError):
        return None


def detect_provider() -> VCSProvider:
    """Detect VCS provider with fallback to GitHub.

    Detection order:
    1. Try detect from git remote
    2. Default to GitHub

    Returns:
        VCSProvider (defaults to GitHub for backward compatibility)
    """
    detected = detect_from_remote()
    if detected:
        return detected

    # Default to GitHub for backward compatibility
    return VCSProvider.GITHUB
