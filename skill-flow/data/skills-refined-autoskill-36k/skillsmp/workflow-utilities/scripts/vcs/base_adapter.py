#!/usr/bin/env python3
"""Base VCS adapter abstract class.

This module defines the interface that all VCS adapters must implement.

Design:
- Abstract base class enforces consistent interface across providers
- Concrete adapters implement provider-specific CLI commands
"""

from abc import ABC, abstractmethod


class BaseVCSAdapter(ABC):
    """Abstract base class for VCS provider adapters.

    All VCS adapters must implement these methods to provide a consistent
    interface for workflow scripts.
    """

    @abstractmethod
    def check_authentication(self) -> bool:
        """Check if user is authenticated with the VCS provider.

        Returns:
            True if authenticated, False otherwise

        Example:
            GitHub: gh auth status
            Azure DevOps: az account show
        """
        pass

    @abstractmethod
    def get_current_user(self) -> str:
        """Get the current authenticated user's identifier.

        Returns:
            Username, email, or other user identifier

        Raises:
            RuntimeError: If not authenticated or command fails

        Example:
            GitHub: gh api user --jq '.login'
            Azure DevOps: az devops user show --user me --query user.emailAddress
        """
        pass

    @abstractmethod
    def create_pull_request(self, source_branch: str, target_branch: str, title: str, body: str) -> str:
        """Create a pull request.

        Args:
            source_branch: Source branch name
            target_branch: Target branch name
            title: PR title
            body: PR description

        Returns:
            Pull request URL

        Raises:
            RuntimeError: If PR creation fails

        Example:
            GitHub: gh pr create --base target --head source --title "..." --body "..."
            Azure DevOps: az repos pr create --source-branch source --target-branch target
        """
        pass

    @abstractmethod
    def fetch_pr_comments(self, pr_number: int) -> list:
        """Fetch review comments from a pull request.

        Args:
            pr_number: Pull request number

        Returns:
            List of comment dictionaries with keys:
                - author: Comment author
                - body: Comment text
                - file: File path (if file comment)
                - line: Line number (if file comment)
                - created_at: Comment timestamp

        Raises:
            RuntimeError: If fetching comments fails

        Example:
            GitHub: gh pr view <pr> --json reviews,comments
            Azure DevOps: az repos pr show --id <pr> --query threads
        """
        pass

    @abstractmethod
    def update_pr(self, pr_number: int, title: str = None, body: str = None) -> None:
        """Update pull request title or description.

        Args:
            pr_number: Pull request number
            title: New PR title (optional)
            body: New PR description (optional)

        Raises:
            RuntimeError: If update fails

        Example:
            GitHub: gh pr edit <pr> --title "..." --body "..."
            Azure DevOps: az repos pr update --id <pr> --title "..." --description "..."
        """
        pass

    @abstractmethod
    def get_pr_status(self, pr_number: int) -> dict:
        """Get pull request status (approval, merge state).

        Args:
            pr_number: Pull request number

        Returns:
            Dictionary with keys:
                - state: PR state (open/closed/merged)
                - mergeable: Boolean indicating if PR can be merged
                - approved: Boolean indicating if PR is approved
                - reviews_required: Number of approvals required

        Raises:
            RuntimeError: If fetching status fails

        Example:
            GitHub: gh pr view <pr> --json state,mergeable,reviewDecision
            Azure DevOps: az repos pr show --id <pr> --query status,mergeStatus
        """
        pass

    def get_provider_name(self) -> str:
        """Get human-readable provider name.

        Returns:
            Provider name (e.g., "GitHub", "Azure DevOps")

        Note:
            This is a concrete method with a default implementation.
            Subclasses can override if needed.
        """
        return self.__class__.__name__.replace("Adapter", "")
