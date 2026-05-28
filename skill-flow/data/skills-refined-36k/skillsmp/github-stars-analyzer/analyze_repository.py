"""
Repository analysis module.
Core engine for analyzing GitHub repository metrics and trends.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import statistics


class RepositoryAnalyzer:
    """Analyze GitHub repository metrics and trends."""

    def __init__(self, github_api_handler):
        """
        Initialize repository analyzer.

        Args:
            github_api_handler: Instance of GitHubAPIHandler
        """
        self.github_api = github_api_handler
        self.metrics = {}

    def safe_divide(self, numerator: float, denominator: float, default: float = 0.0) -> float:
        """Safely divide two numbers, returning default if denominator is zero."""
        if denominator == 0:
            return default
        return numerator / denominator

    def analyze_single_repository(self, owner: str, repo: str, days: int = 30) -> Dict[str, Any]:
        """
        Analyze a single repository.

        Args:
            owner: Repository owner
            repo: Repository name
            days: Time period for analysis in days

        Returns:
            Dictionary with comprehensive analysis
        """
        try:
            # Fetch basic repository info
            repo_info = self.github_api.get_repository_info(owner, repo)

            # Calculate metrics
            stars = repo_info.get("stargazers_count", 0)
            forks = repo_info.get("forks_count", 0)
            watchers = repo_info.get("watchers_count", 0)
            open_issues = repo_info.get("open_issues_count", 0)
            size = repo_info.get("size", 0)
            created_at = repo_info.get("created_at", "")
            updated_at = repo_info.get("updated_at", "")

            # Calculate derived metrics
            stars_per_fork = self.safe_divide(stars, forks)
            stars_per_watcher = self.safe_divide(stars, watchers)
            issues_per_star = self.safe_divide(open_issues, stars)

            # Get additional metrics
            contributors = self.github_api.get_contributors_count(owner, repo)
            languages = self.github_api.get_repository_languages(owner, repo)
            activity = self.github_api.get_repository_activity(owner, repo, days)

            # Calculate repository age
            if created_at:
                created_date = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
                age_days = (datetime.now() - created_date).days
                stars_per_day = self.safe_divide(stars, age_days)
            else:
                age_days = 0
                stars_per_day = 0

            # Build comprehensive analysis
            analysis = {
                "basic_info": {
                    "owner": owner,
                    "repo": repo,
                    "full_name": repo_info.get("full_name", f"{owner}/{repo}"),
                    "description": repo_info.get("description", ""),
                    "url": repo_info.get("html_url", f"https://github.com/{owner}/{repo}"),
                    "created_at": created_at,
                    "updated_at": updated_at,
                    "age_days": age_days,
                    "size_kb": size
                },
                "metrics": {
                    "stars": stars,
                    "forks": forks,
                    "watchers": watchers,
                    "open_issues": open_issues,
                    "contributors": contributors,
                    "stars_per_day": stars_per_day,
                    "stars_per_fork": stars_per_fork,
                    "stars_per_watcher": stars_per_watcher,
                    "issues_per_star": issues_per_star
                },
                "activity": activity,
                "languages": languages,
                "popularity_score": self.calculate_popularity_score(
                    stars, forks, contributors, activity.get("commits_per_day", 0)
                ),
                "health_score": self.calculate_health_score(
                    stars, forks, open_issues, activity.get("commits_per_day", 0)
                )
            }

            return analysis

        except Exception as e:
            raise Exception(f"Failed to analyze repository {owner}/{repo}: {e}")

    def calculate_popularity_score(self, stars: int, forks: int, contributors: int, commits_per_day: float) -> float:
        """
        Calculate a popularity score for the repository.

        Args:
            stars: Number of stars
            forks: Number of forks
            contributors: Number of contributors
            commits_per_day: Average commits per day

        Returns:
            Popularity score (0-100)
        """
        # Normalize metrics (log scale for stars and forks)
        star_score = min(100, (stars ** 0.5) * 2) if stars > 0 else 0
        fork_score = min(100, (forks ** 0.5) * 5) if forks > 0 else 0
        contributor_score = min(100, contributors * 10) if contributors > 0 else 0
        activity_score = min(100, commits_per_day * 100) if commits_per_day > 0 else 0

        # Weighted average
        weights = {
            "stars": 0.4,
            "forks": 0.3,
            "contributors": 0.2,
            "activity": 0.1
        }

        score = (
            star_score * weights["stars"] +
            fork_score * weights["forks"] +
            contributor_score * weights["contributors"] +
            activity_score * weights["activity"]
        )

        return round(score, 2)

    def calculate_health_score(self, stars: int, forks: int, open_issues: int, commits_per_day: float) -> float:
        """
        Calculate a health score for the repository.

        Args:
            stars: Number of stars
            forks: Number of forks
            open_issues: Number of open issues
            commits_per_day: Average commits per day

        Returns:
            Health score (0-100)
        """
        # Activity component
        activity_score = min(100, commits_per_day * 200) if commits_per_day > 0 else 0

        # Issue resolution component (lower issues per star is better)
        issues_per_star = self.safe_divide(open_issues, stars)
        issue_score = max(0, 100 - (issues_per_star * 1000))

        # Fork activity component (forks per star)
        forks_per_star = self.safe_divide(forks, stars)
        fork_score = min(100, forks_per_star * 500)

        # Weighted average
        weights = {
            "activity": 0.4,
            "issues": 0.3,
            "forks": 0.3
        }

        score = (
            activity_score * weights["activity"] +
            issue_score * weights["issues"] +
            fork_score * weights["forks"]
        )

        return round(score, 2)

    def compare_repositories(self, repositories: List[Dict[str, str]], days: int = 30) -> Dict[str, Any]:
        """
        Compare multiple repositories.

        Args:
            repositories: List of dictionaries with owner and repo keys
            days: Time period for analysis in days

        Returns:
            Dictionary with comparative analysis
        """
        analyses = []
        for repo_info in repositories:
            owner = repo_info.get("owner")
            repo = repo_info.get("repo")
            if owner and repo:
                try:
                    analysis = self.analyze_single_repository(owner, repo, days)
                    analyses.append(analysis)
                except Exception as e:
                    print(f"Warning: Failed to analyze {owner}/{repo}: {e}")

        if not analyses:
            raise ValueError("No repositories could be analyzed")

        # Calculate comparative metrics
        star_counts = [a["metrics"]["stars"] for a in analyses]
        fork_counts = [a["metrics"]["forks"] for a in analyses]
        popularity_scores = [a["popularity_score"] for a in analyses]
        health_scores = [a["health_score"] for a in analyses]

        comparison = {
            "repositories": analyses,
            "summary": {
                "total_repositories": len(analyses),
                "total_stars": sum(star_counts),
                "total_forks": sum(fork_counts),
                "average_stars": statistics.mean(star_counts) if star_counts else 0,
                "average_forks": statistics.mean(fork_counts) if fork_counts else 0,
                "average_popularity": statistics.mean(popularity_scores) if popularity_scores else 0,
                "average_health": statistics.mean(health_scores) if health_scores else 0,
                "max_stars": max(star_counts) if star_counts else 0,
                "min_stars": min(star_counts) if star_counts else 0,
                "max_popularity": max(popularity_scores) if popularity_scores else 0,
                "min_popularity": min(popularity_scores) if popularity_scores else 0
            },
            "rankings": {
                "by_stars": sorted(
                    analyses,
                    key=lambda x: x["metrics"]["stars"],
                    reverse=True
                ),
                "by_popularity": sorted(
                    analyses,
                    key=lambda x: x["popularity_score"],
                    reverse=True
                ),
                "by_health": sorted(
                    analyses,
                    key=lambda x: x["health_score"],
                    reverse=True
                )
            }
        }

        return comparison

    def calculate_growth_metrics(self, owner: str, repo: str, days: int = 30) -> Dict[str, Any]:
        """
        Calculate growth metrics for a repository.

        Args:
            owner: Repository owner
            repo: Repository name
            days: Time period for analysis in days

        Returns:
            Dictionary with growth metrics
        """
        analysis = self.analyze_single_repository(owner, repo, days)

        stars = analysis["metrics"]["stars"]
        stars_per_day = analysis["metrics"]["stars_per_day"]
        age_days = analysis["basic_info"]["age_days"]

        # Calculate growth rates
        if age_days > 0:
            daily_growth_rate = self.safe_divide(stars_per_day, stars) * 100
            weekly_growth_rate = daily_growth_rate * 7
            monthly_growth_rate = daily_growth_rate * 30
        else:
            daily_growth_rate = weekly_growth_rate = monthly_growth_rate = 0

        # Project future growth
        if daily_growth_rate > 0:
            projected_30_days = stars * (1 + daily_growth_rate/100) ** 30
            projected_90_days = stars * (1 + daily_growth_rate/100) ** 90
            projected_180_days = stars * (1 + daily_growth_rate/100) ** 180
        else:
            projected_30_days = projected_90_days = projected_180_days = stars

        growth_metrics = {
            "current_stars": stars,
            "stars_per_day": stars_per_day,
            "daily_growth_rate_percent": round(daily_growth_rate, 4),
            "weekly_growth_rate_percent": round(weekly_growth_rate, 4),
            "monthly_growth_rate_percent": round(monthly_growth_rate, 4),
            "projections": {
                "30_days": round(projected_30_days),
                "90_days": round(projected_90_days),
                "180_days": round(projected_180_days)
            },
            "growth_category": self.categorize_growth(daily_growth_rate)
        }

        return growth_metrics

    def categorize_growth(self, daily_growth_rate: float) -> str:
        """
        Categorize growth rate.

        Args:
            daily_growth_rate: Daily growth rate in percent

        Returns:
            Growth category string
        """
        if daily_growth_rate >= 1.0:
            return "Explosive"
        elif daily_growth_rate >= 0.5:
            return "Rapid"
        elif daily_growth_rate >= 0.2:
            return "Steady"
        elif daily_growth_rate >= 0.05:
            return "Slow"
        elif daily_growth_rate > 0:
            return "Minimal"
        elif daily_growth_rate == 0:
            return "Stagnant"
        else:
            return "Declining"