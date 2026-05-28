#!/usr/bin/env python3
"""GitHub VCS adapter using gh CLI.

This adapter implements VCS operations for GitHub using the gh command-line tool.

Requirements:
- gh CLI installed (https://cli.github.com/)
- Authenticated via: gh auth login

Constants:
- GITHUB_CLI: gh command name
  Rationale: Centralize CLI command name for easier testing/mocking
"""

import json
import subprocess

from .base_adapter import BaseVCSAdapter

# Constants
GITHUB_CLI = "gh"


class GitHubAdapter(BaseVCSAdapter):
    """GitHub VCS adapter using gh CLI.

    Implements VCS operations for GitHub repositories.
    """

    def check_authentication(self) -> bool:
        """Check if user is authenticated with GitHub.

        Returns:
            True if authenticated, False otherwise
        """
        try:
            subprocess.run([GITHUB_CLI, "auth", "status"], capture_output=True, text=True, check=True, timeout=10)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            return False

    def get_current_user(self) -> str:
        """Get the current authenticated GitHub user.

        Returns:
            GitHub username

        Raises:
            RuntimeError: If not authenticated or command fails
        """
        try:
            result = subprocess.check_output([GITHUB_CLI, "api", "user", "--jq", ".login"], text=True, stderr=subprocess.PIPE, timeout=10)
            return result.strip()

        except FileNotFoundError:
            raise RuntimeError(f"'{GITHUB_CLI}' CLI not found. Install from https://cli.github.com/")
        except subprocess.CalledProcessError as e:
            error_msg = e.stderr.strip() if e.stderr else str(e)
            raise RuntimeError(f"Failed to get GitHub username. Make sure you're authenticated: gh auth login\nError: {error_msg}")
        except subprocess.TimeoutExpired:
            raise RuntimeError("Timeout while getting GitHub username")

    def create_pull_request(self, source_branch: str, target_branch: str, title: str, body: str) -> str:
        """Create a GitHub pull request.

        Args:
            source_branch: Source branch name
            target_branch: Target branch name (base)
            title: PR title
            body: PR description

        Returns:
            Pull request URL

        Raises:
            RuntimeError: If PR creation fails
        """
        try:
            result = subprocess.check_output(
                [GITHUB_CLI, "pr", "create", "--base", target_branch, "--head", source_branch, "--title", title, "--body", body],
                text=True,
                stderr=subprocess.PIPE,
                timeout=30,
            )
            # gh pr create outputs the PR URL
            pr_url = result.strip()
            return pr_url

        except FileNotFoundError:
            raise RuntimeError(f"'{GITHUB_CLI}' CLI not found. Install from https://cli.github.com/")
        except subprocess.CalledProcessError as e:
            error_msg = e.stderr.strip() if e.stderr else str(e)
            raise RuntimeError(f"Failed to create GitHub pull request.\nError: {error_msg}")
        except subprocess.TimeoutExpired:
            raise RuntimeError("Timeout while creating GitHub pull request")

    def fetch_pr_comments(self, pr_number: int) -> list:
        """Fetch review comments from a GitHub pull request.

        Args:
            pr_number: Pull request number

        Returns:
            List of comment dictionaries

        Raises:
            RuntimeError: If fetching comments fails
        """
        try:
            result = subprocess.check_output(
                [GITHUB_CLI, "pr", "view", str(pr_number), "--json", "reviews,comments", "--jq", "."], text=True, stderr=subprocess.PIPE, timeout=30
            )
            data = json.loads(result)

            comments = []

            # Process review comments (file-level comments)
            for review in data.get("reviews", []):
                if review.get("body"):
                    comments.append(
                        {
                            "author": review["author"]["login"] if review.get("author") else "Ghost",
                            "body": review["body"],
                            "file": None,
                            "line": None,
                            "created_at": review["submittedAt"],
                        }
                    )

            # Process general comments
            for comment in data.get("comments", []):
                comments.append(
                    {
                        "author": comment["author"]["login"] if comment.get("author") else "Ghost",
                        "body": comment["body"],
                        "file": None,
                        "line": None,
                        "created_at": comment["createdAt"],
                    }
                )

            return comments

        except FileNotFoundError:
            raise RuntimeError(f"'{GITHUB_CLI}' CLI not found. Install from https://cli.github.com/")
        except subprocess.CalledProcessError as e:
            error_msg = e.stderr.strip() if e.stderr else str(e)
            raise RuntimeError(f"Failed to fetch PR comments.\nError: {error_msg}")
        except subprocess.TimeoutExpired:
            raise RuntimeError("Timeout while fetching PR comments")
        except (json.JSONDecodeError, KeyError) as e:
            raise RuntimeError(f"Failed to parse PR comment data: {e}")

    def update_pr(self, pr_number: int, title: str = None, body: str = None) -> None:
        """Update GitHub pull request title or description.

        Args:
            pr_number: Pull request number
            title: New PR title (optional)
            body: New PR description (optional)

        Raises:
            RuntimeError: If update fails
        """
        if not title and not body:
            return  # Nothing to update

        try:
            cmd = [GITHUB_CLI, "pr", "edit", str(pr_number)]

            if title:
                cmd.extend(["--title", title])
            if body:
                cmd.extend(["--body", body])

            subprocess.check_output(cmd, text=True, stderr=subprocess.PIPE, timeout=30)

        except FileNotFoundError:
            raise RuntimeError(f"'{GITHUB_CLI}' CLI not found. Install from https://cli.github.com/")
        except subprocess.CalledProcessError as e:
            error_msg = e.stderr.strip() if e.stderr else str(e)
            raise RuntimeError(f"Failed to update PR.\nError: {error_msg}")
        except subprocess.TimeoutExpired:
            raise RuntimeError("Timeout while updating PR")

    def get_pr_status(self, pr_number: int) -> dict:
        """Get GitHub pull request status.

        Args:
            pr_number: Pull request number

        Returns:
            Dictionary with status information

        Raises:
            RuntimeError: If fetching status fails
        """
        try:
            result = subprocess.check_output(
                [GITHUB_CLI, "pr", "view", str(pr_number), "--json", "state,mergeable,reviewDecision", "--jq", "."], text=True, stderr=subprocess.PIPE, timeout=30
            )
            data = json.loads(result)

            return {
                "state": data.get("state", "UNKNOWN").lower(),
                "mergeable": data.get("mergeable") == "MERGEABLE",
                "approved": data.get("reviewDecision") == "APPROVED",
                "reviews_required": 1 if data.get("reviewDecision") != "APPROVED" else 0,
            }

        except FileNotFoundError:
            raise RuntimeError(f"'{GITHUB_CLI}' CLI not found. Install from https://cli.github.com/")
        except subprocess.CalledProcessError as e:
            error_msg = e.stderr.strip() if e.stderr else str(e)
            raise RuntimeError(f"Failed to fetch PR status.\nError: {error_msg}")
        except subprocess.TimeoutExpired:
            raise RuntimeError("Timeout while fetching PR status")
        except (json.JSONDecodeError, KeyError) as e:
            raise RuntimeError(f"Failed to parse PR status data: {e}")

    def get_provider_name(self) -> str:
        """Get provider name.

        Returns:
            "GitHub"
        """
        return "GitHub"
