#!/usr/bin/env python3
"""Azure DevOps VCS adapter using az CLI.

This adapter implements VCS operations for Azure DevOps using the az command-line tool.

Requirements:
- Azure CLI installed (https://learn.microsoft.com/cli/azure/)
- Azure DevOps extension: az extension add --name azure-devops
- Authenticated via: az login
- Configured: az devops configure --defaults organization=... project=...

Constants:
- AZURE_CLI: az command name
  Rationale: Centralize CLI command name for easier testing/mocking
"""

import json
import subprocess

from .base_adapter import BaseVCSAdapter

# Constants
AZURE_CLI = "az"


class AzureDevOpsAdapter(BaseVCSAdapter):
    """Azure DevOps VCS adapter using az CLI.

    Implements VCS operations for Azure DevOps repositories.

    Args:
        organization: Azure DevOps organization URL (e.g., https://dev.azure.com/myorg)
        project: Azure DevOps project name
        repository: Repository name (optional, defaults to project name)
    """

    def __init__(self, organization: str, project: str, repository: str = None):
        """Initialize Azure DevOps adapter.

        Args:
            organization: Azure DevOps organization URL
            project: Azure DevOps project name
            repository: Repository name (optional, defaults to project name if not provided)

        Raises:
            ValueError: If organization or project is empty
        """
        if not organization or not organization.strip():
            raise ValueError("organization is required for Azure DevOps")
        if not project or not project.strip():
            raise ValueError("project is required for Azure DevOps")

        self.organization = organization.strip()
        self.project = project.strip()
        # Default to project name if repository not provided (backward compatibility)
        # Note: Treats None, empty string, and whitespace-only values as "not provided"
        # to maintain consistency with organization and project validation (issue #110)
        stripped_repo = repository.strip() if repository else ""
        self.repository = stripped_repo if stripped_repo else self.project

    def check_authentication(self) -> bool:
        """Check if user is authenticated with Azure.

        Returns:
            True if authenticated, False otherwise
        """
        try:
            subprocess.run([AZURE_CLI, "account", "show"], capture_output=True, text=True, check=True, timeout=10)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            return False

    def get_current_user(self) -> str:
        """Get the current authenticated Azure DevOps user.

        Returns:
            User email address

        Raises:
            RuntimeError: If not authenticated or command fails
        """
        try:
            result = subprocess.check_output(
                [AZURE_CLI, "devops", "user", "show", "--user", "me", "--query", "user.emailAddress", "--output", "tsv", "--organization", self.organization],
                text=True,
                stderr=subprocess.PIPE,
                timeout=15,
            )
            return result.strip()

        except FileNotFoundError:
            raise RuntimeError(f"'{AZURE_CLI}' CLI not found. Install from https://learn.microsoft.com/cli/azure/")
        except subprocess.CalledProcessError as e:
            error_msg = e.stderr.strip() if e.stderr else str(e)
            raise RuntimeError(
                f"Failed to get Azure DevOps user. "
                f"Make sure you're authenticated: az login\n"
                f"And have the Azure DevOps extension: az extension add --name azure-devops\n"
                f"Error: {error_msg}"
            )
        except subprocess.TimeoutExpired:
            raise RuntimeError("Timeout while getting Azure DevOps user")

    def create_pull_request(self, source_branch: str, target_branch: str, title: str, body: str) -> str:
        """Create an Azure DevOps pull request.

        Args:
            source_branch: Source branch name
            target_branch: Target branch name
            title: PR title
            body: PR description

        Returns:
            Pull request URL

        Raises:
            RuntimeError: If PR creation fails
        """
        try:
            result = subprocess.check_output(
                [
                    AZURE_CLI,
                    "repos",
                    "pr",
                    "create",
                    "--source-branch",
                    source_branch,
                    "--target-branch",
                    target_branch,
                    "--title",
                    title,
                    "--description",
                    body,
                    "--organization",
                    self.organization,
                    "--project",
                    self.project,
                    "--query",
                    "url",
                    "--output",
                    "tsv",
                ],
                text=True,
                stderr=subprocess.PIPE,
                timeout=30,
            )
            pr_url = result.strip()
            return pr_url

        except FileNotFoundError:
            raise RuntimeError(f"'{AZURE_CLI}' CLI not found. Install from https://learn.microsoft.com/cli/azure/")
        except subprocess.CalledProcessError as e:
            error_msg = e.stderr.strip() if e.stderr else str(e)
            raise RuntimeError(f"Failed to create Azure DevOps pull request.\nError: {error_msg}")
        except subprocess.TimeoutExpired:
            raise RuntimeError("Timeout while creating Azure DevOps pull request")

    def fetch_pr_comments(self, pr_number: int) -> list:
        """Fetch review comments from an Azure DevOps pull request.

        Args:
            pr_number: Pull request ID

        Returns:
            List of comment dictionaries

        Raises:
            RuntimeError: If fetching comments fails
        """
        try:
            result = subprocess.check_output(
                [AZURE_CLI, "repos", "pr", "show", "--id", str(pr_number), "--organization", self.organization, "--query", "threads", "--output", "json"],
                text=True,
                stderr=subprocess.PIPE,
                timeout=30,
            )
            threads = json.loads(result)

            comments = []

            # Process comment threads
            for thread in threads:
                for comment in thread.get("comments", []):
                    if comment.get("content"):
                        comments.append(
                            {
                                "author": comment["author"]["displayName"] if comment.get("author") else "Unknown",
                                "body": comment["content"],
                                "file": thread.get("threadContext", {}).get("filePath"),
                                "line": thread.get("threadContext", {}).get("rightFileStart", {}).get("line"),
                                "created_at": comment["publishedDate"],
                            }
                        )

            return comments

        except FileNotFoundError:
            raise RuntimeError(f"'{AZURE_CLI}' CLI not found. Install from https://learn.microsoft.com/cli/azure/")
        except subprocess.CalledProcessError as e:
            error_msg = e.stderr.strip() if e.stderr else str(e)
            raise RuntimeError(f"Failed to fetch Azure DevOps PR comments.\nError: {error_msg}")
        except subprocess.TimeoutExpired:
            raise RuntimeError("Timeout while fetching Azure DevOps PR comments")
        except (json.JSONDecodeError, KeyError) as e:
            raise RuntimeError(f"Failed to parse PR comment data: {e}")

    def update_pr(self, pr_number: int, title: str = None, body: str = None) -> None:
        """Update Azure DevOps pull request title or description.

        Args:
            pr_number: Pull request ID
            title: New PR title (optional)
            body: New PR description (optional)

        Raises:
            RuntimeError: If update fails
        """
        if not title and not body:
            return  # Nothing to update

        try:
            cmd = [AZURE_CLI, "repos", "pr", "update", "--id", str(pr_number), "--organization", self.organization]

            if title:
                cmd.extend(["--title", title])
            if body:
                cmd.extend(["--description", body])

            subprocess.check_output(cmd, text=True, stderr=subprocess.PIPE, timeout=30)

        except FileNotFoundError:
            raise RuntimeError(f"'{AZURE_CLI}' CLI not found. Install from https://learn.microsoft.com/cli/azure/")
        except subprocess.CalledProcessError as e:
            error_msg = e.stderr.strip() if e.stderr else str(e)
            raise RuntimeError(f"Failed to update Azure DevOps PR.\nError: {error_msg}")
        except subprocess.TimeoutExpired:
            raise RuntimeError("Timeout while updating Azure DevOps PR")

    def get_pr_status(self, pr_number: int) -> dict:
        """Get Azure DevOps pull request status.

        Args:
            pr_number: Pull request ID

        Returns:
            Dictionary with status information

        Raises:
            RuntimeError: If fetching status fails
        """
        try:
            result = subprocess.check_output(
                [
                    AZURE_CLI,
                    "repos",
                    "pr",
                    "show",
                    "--id",
                    str(pr_number),
                    "--organization",
                    self.organization,
                    "--query",
                    "{status:status, mergeStatus:mergeStatus, reviewers:reviewers}",
                    "--output",
                    "json",
                ],
                text=True,
                stderr=subprocess.PIPE,
                timeout=30,
            )
            data = json.loads(result)

            # Count approved reviewers
            approved_count = sum(
                1
                for r in data.get("reviewers", [])
                if r.get("vote") == 10  # 10 = Approved in Azure DevOps
            )

            return {
                "state": data.get("status", "unknown").lower(),
                "mergeable": data.get("mergeStatus") == "succeeded",
                "approved": approved_count > 0,
                "reviews_required": max(0, 1 - approved_count),
            }

        except FileNotFoundError:
            raise RuntimeError(f"'{AZURE_CLI}' CLI not found. Install from https://learn.microsoft.com/cli/azure/")
        except subprocess.CalledProcessError as e:
            error_msg = e.stderr.strip() if e.stderr else str(e)
            raise RuntimeError(f"Failed to fetch Azure DevOps PR status.\nError: {error_msg}")
        except subprocess.TimeoutExpired:
            raise RuntimeError("Timeout while fetching Azure DevOps PR status")
        except (json.JSONDecodeError, KeyError) as e:
            raise RuntimeError(f"Failed to parse PR status data: {e}")

    def get_provider_name(self) -> str:
        """Get provider name.

        Returns:
            "Azure DevOps"
        """
        return "Azure DevOps"
