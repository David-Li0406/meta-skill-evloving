#!/usr/bin/env python3
"""VCS provider abstraction for workflow scripts.

This module provides a unified interface for interacting with different VCS providers
(GitHub, Azure DevOps) through CLI tools (gh, az).

Usage:
    from vcs import get_vcs_adapter

    vcs = get_vcs_adapter()
    username = vcs.get_current_user()
    vcs.create_pull_request(source, target, title, body)
"""

import sys

from .azure_adapter import AzureDevOpsAdapter
from .base_adapter import BaseVCSAdapter
from .config import load_vcs_config
from .github_adapter import GitHubAdapter
from .provider import VCSProvider, detect_provider, extract_azure_repo_from_remote

__all__ = [
    "BaseVCSAdapter",
    "GitHubAdapter",
    "AzureDevOpsAdapter",
    "VCSProvider",
    "get_vcs_adapter",
]


def get_vcs_adapter() -> BaseVCSAdapter:
    """Get appropriate VCS adapter based on configuration and context.

    Detection order:
    1. Load .vcs_config.yaml if exists → use specified provider
    2. Detect from git remote URL
    3. Default to GitHub (backward compatibility)

    Returns:
        Configured VCS adapter instance

    Raises:
        ValueError: If provider configuration is invalid
    """
    # Try loading explicit configuration
    config = load_vcs_config()
    if config:
        provider = config.get("vcs_provider")
        if provider == "github":
            return GitHubAdapter()
        elif provider == "azure_devops":
            azure_config = config.get("azure_devops", {})
            org = azure_config.get("organization")
            project = azure_config.get("project")
            if not org or not project:
                raise ValueError("Azure DevOps requires 'organization' and 'project' in config")

            # Get repository from config or extract from git remote
            repository = azure_config.get("repository")
            if not repository:
                repository = extract_azure_repo_from_remote()
                if not repository:
                    # Warn when extraction fails - adapter will default to project name
                    print(
                        f"⚠️  Warning: Could not extract repository name from git remote.\n"
                        f"   Repository will default to project name ('{project}').\n"
                        f"   If your Azure DevOps repository name differs from project name,\n"
                        f"   add 'repository' to .vcs_config.yaml:\n"
                        f"     azure_devops:\n"
                        f'       repository: "YourRepoName"',
                        file=sys.stderr,
                    )

            return AzureDevOpsAdapter(organization=org, project=project, repository=repository)
        else:
            raise ValueError(f"Unknown VCS provider in config: {provider}")

    # Try detecting from git remote
    detected = detect_provider()
    if detected == VCSProvider.AZURE_DEVOPS:
        # TODO: Extract org/project from git remote URL
        raise ValueError("Azure DevOps detected but requires .vcs_config.yaml with org/project")

    # Default to GitHub (backward compatibility)
    return GitHubAdapter()
