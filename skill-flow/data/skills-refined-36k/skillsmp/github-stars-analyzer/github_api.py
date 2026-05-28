"""
GitHub API interaction module.
Handles data fetching from GitHub API with rate limit management.
"""

import requests
import time
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import json


class GitHubAPIHandler:
    """Handle GitHub API interactions with rate limiting."""

    def __init__(self, github_token: Optional[str] = None):
        """
        Initialize GitHub API handler.

        Args:
            github_token: Optional GitHub personal access token for higher rate limits
        """
        self.base_url = "https://api.github.com"
        self.session = requests.Session()
        self.rate_limit_remaining = 60  # Default for unauthenticated
        self.rate_limit_reset = 0

        if github_token:
            self.session.headers.update({
                "Authorization": f"token {github_token}",
                "Accept": "application/vnd.github.v3+json"
            })
            self.rate_limit_remaining = 5000  # Higher limit for authenticated

    def check_rate_limit(self) -> None:
        """Check and respect GitHub API rate limits."""
        if self.rate_limit_remaining <= 5:
            wait_time = max(self.rate_limit_reset - time.time(), 0)
            if wait_time > 0:
                print(f"Rate limit low. Waiting {wait_time:.0f} seconds...")
                time.sleep(wait_time + 1)
            self.update_rate_limit()

    def update_rate_limit(self) -> None:
        """Update rate limit information from GitHub API."""
        try:
            response = self.session.get(f"{self.base_url}/rate_limit")
            if response.status_code == 200:
                data = response.json()
                resources = data.get("resources", {})
                core = resources.get("core", {})
                self.rate_limit_remaining = core.get("remaining", 60)
                self.rate_limit_reset = core.get("reset", 0)
        except Exception as e:
            print(f"Error updating rate limit: {e}")

    def get_repository_info(self, owner: str, repo: str) -> Dict[str, Any]:
        """
        Get basic repository information.

        Args:
            owner: Repository owner (username or organization)
            repo: Repository name

        Returns:
            Dictionary with repository information
        """
        self.check_rate_limit()
        url = f"{self.base_url}/repos/{owner}/{repo}"

        try:
            response = self.session.get(url)
            self.rate_limit_remaining -= 1

            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                raise ValueError(f"Repository {owner}/{repo} not found")
            else:
                raise Exception(f"GitHub API error: {response.status_code}")

        except Exception as e:
            raise Exception(f"Failed to fetch repository info: {e}")

    def get_stargazers(self, owner: str, repo: str, per_page: int = 100) -> List[Dict[str, Any]]:
        """
        Get list of stargazers for a repository.

        Args:
            owner: Repository owner
            repo: Repository name
            per_page: Number of results per page (max 100)

        Returns:
            List of stargazer information
        """
        self.check_rate_limit()
        url = f"{self.base_url}/repos/{owner}/{repo}/stargazers"
        params = {"per_page": min(per_page, 100)}

        try:
            response = self.session.get(url, params=params)
            self.rate_limit_remaining -= 1

            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"GitHub API error: {response.status_code}")

        except Exception as e:
            raise Exception(f"Failed to fetch stargazers: {e}")

    def get_stargazers_count(self, owner: str, repo: str) -> int:
        """
        Get total stargazers count for a repository.

        Args:
            owner: Repository owner
            repo: Repository name

        Returns:
            Total number of stargazers
        """
        repo_info = self.get_repository_info(owner, repo)
        return repo_info.get("stargazers_count", 0)

    def get_forks_count(self, owner: str, repo: str) -> int:
        """
        Get total forks count for a repository.

        Args:
            owner: Repository owner
            repo: Repository name

        Returns:
            Total number of forks
        """
        repo_info = self.get_repository_info(owner, repo)
        return repo_info.get("forks_count", 0)

    def get_issues_count(self, owner: str, repo: str, state: str = "open") -> int:
        """
        Get issues count for a repository.

        Args:
            owner: Repository owner
            repo: Repository name
            state: Issue state (open, closed, all)

        Returns:
            Number of issues
        """
        self.check_rate_limit()
        url = f"{self.base_url}/repos/{owner}/{repo}/issues"
        params = {"state": state, "per_page": 1}

        try:
            response = self.session.get(url, params=params)
            self.rate_limit_remaining -= 1

            if response.status_code == 200:
                # GitHub returns pagination info in headers
                link_header = response.headers.get("Link", "")
                if "rel=\"last\"" in link_header:
                    # Parse the last page number from the Link header
                    import re
                    last_match = re.search(r'page=(\d+)>; rel="last"', link_header)
                    if last_match:
                        return int(last_match.group(1))
                # If no pagination, count the first page results
                return len(response.json())
            else:
                raise Exception(f"GitHub API error: {response.status_code}")

        except Exception as e:
            raise Exception(f"Failed to fetch issues count: {e}")

    def get_contributors_count(self, owner: str, repo: str) -> int:
        """
        Get number of contributors to a repository.

        Args:
            owner: Repository owner
            repo: Repository name

        Returns:
            Number of contributors
        """
        self.check_rate_limit()
        url = f"{self.base_url}/repos/{owner}/{repo}/contributors"
        params = {"per_page": 1}

        try:
            response = self.session.get(url, params=params)
            self.rate_limit_remaining -= 1

            if response.status_code == 200:
                link_header = response.headers.get("Link", "")
                if "rel=\"last\"" in link_header:
                    import re
                    last_match = re.search(r'page=(\d+)>; rel="last"', link_header)
                    if last_match:
                        return int(last_match.group(1))
                return len(response.json())
            else:
                raise Exception(f"GitHub API error: {response.status_code}")

        except Exception as e:
            raise Exception(f"Failed to fetch contributors count: {e}")

    def get_repository_languages(self, owner: str, repo: str) -> Dict[str, int]:
        """
        Get programming languages used in a repository.

        Args:
            owner: Repository owner
            repo: Repository name

        Returns:
            Dictionary of languages and bytes of code
        """
        self.check_rate_limit()
        url = f"{self.base_url}/repos/{owner}/{repo}/languages"

        try:
            response = self.session.get(url)
            self.rate_limit_remaining -= 1

            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"GitHub API error: {response.status_code}")

        except Exception as e:
            raise Exception(f"Failed to fetch languages: {e}")

    def get_repository_activity(self, owner: str, repo: str, days: int = 30) -> Dict[str, Any]:
        """
        Get repository activity metrics for a given time period.

        Args:
            owner: Repository owner
            repo: Repository name
            days: Number of days to look back

        Returns:
            Dictionary with activity metrics
        """
        # Note: GitHub API doesn't provide direct activity metrics
        # This is a simplified implementation
        self.check_rate_limit()

        # Get recent commits as a proxy for activity
        url = f"{self.base_url}/repos/{owner}/{repo}/commits"
        since_date = (datetime.now() - timedelta(days=days)).isoformat()
        params = {"since": since_date, "per_page": 100}

        try:
            response = self.session.get(url, params=params)
            self.rate_limit_remaining -= 1

            if response.status_code == 200:
                commits = response.json()
                return {
                    "commit_count": len(commits),
                    "days_active": days,
                    "commits_per_day": len(commits) / days if days > 0 else 0
                }
            else:
                raise Exception(f"GitHub API error: {response.status_code}")

        except Exception as e:
            raise Exception(f"Failed to fetch activity: {e}")