"""
Reddit and Social Media Tools

Access Reddit discussions and social media data for market research.

Features:
- Reddit search and subreddit scraping
- Twitter/X search (basic)
- Social sentiment analysis

Usage:
    from tools.social import RedditClient
    
    client = RedditClient()
    
    # Search Reddit
    results = client.search("hubspot vs salesforce", subreddit="marketing")
    
    # Get subreddit posts
    posts = client.get_subreddit_posts("SaaS", limit=25)
"""

import os
from typing import Optional, Any
from tools.base import BaseAPIClient, get_credential, has_credential
from tools.firecrawl import FirecrawlClient


class RedditClient(BaseAPIClient):
    """
    Reddit API client.
    
    Can use either:
    1. Official Reddit API (requires app credentials)
    2. Firecrawl scraping (fallback, no auth needed)
    """
    
    BASE_URL = "https://oauth.reddit.com"
    
    def __init__(self):
        super().__init__()
        self._access_token: Optional[str] = None
        self._use_scraping = not has_credential("reddit", "client_id")
        
        if self._use_scraping:
            self.firecrawl = FirecrawlClient()
        else:
            self.firecrawl = None
    
    def _get_headers(self) -> dict[str, str]:
        if self._use_scraping:
            return {}
        
        if not self._access_token:
            self._authenticate()
        
        return {
            "Authorization": f"Bearer {self._access_token}",
            "User-Agent": "CMO-Agent/1.0"
        }
    
    def _authenticate(self):
        """Authenticate with Reddit API."""
        import httpx
        
        client_id = get_credential("reddit", "client_id")
        client_secret = get_credential("reddit", "client_secret")
        
        response = httpx.post(
            "https://www.reddit.com/api/v1/access_token",
            auth=(client_id, client_secret),
            data={"grant_type": "client_credentials"},
            headers={"User-Agent": "CMO-Agent/1.0"}
        )
        response.raise_for_status()
        self._access_token = response.json()["access_token"]
    
    def search(
        self,
        query: str,
        subreddit: Optional[str] = None,
        sort: str = "relevance",
        time_filter: str = "all",
        limit: int = 25
    ) -> dict[str, Any]:
        """
        Search Reddit for posts.
        
        Args:
            query: Search query
            subreddit: Limit to specific subreddit
            sort: Sort by (relevance, hot, top, new, comments)
            time_filter: Time filter (hour, day, week, month, year, all)
            limit: Max results
        
        Returns:
            {
                "posts": [
                    {
                        "title": "...",
                        "selftext": "...",
                        "url": "...",
                        "subreddit": "...",
                        "score": int,
                        "num_comments": int,
                        "created_utc": float,
                        "author": "..."
                    }
                ]
            }
        """
        if self._use_scraping:
            return self._search_via_scraping(query, subreddit, limit)
        
        # Use official API
        if subreddit:
            path = f"/r/{subreddit}/search"
        else:
            path = "/search"
        
        params = {
            "q": query,
            "sort": sort,
            "t": time_filter,
            "limit": min(limit, 100),
            "restrict_sr": bool(subreddit)
        }
        
        result = self.get(path, params=params)
        
        posts = []
        for child in result.get("data", {}).get("children", []):
            post = child.get("data", {})
            posts.append({
                "title": post.get("title"),
                "selftext": post.get("selftext", "")[:1000],
                "url": f"https://reddit.com{post.get('permalink', '')}",
                "subreddit": post.get("subreddit"),
                "score": post.get("score"),
                "num_comments": post.get("num_comments"),
                "created_utc": post.get("created_utc"),
                "author": post.get("author")
            })
        
        return {"posts": posts, "query": query}
    
    def _search_via_scraping(
        self,
        query: str,
        subreddit: Optional[str] = None,
        limit: int = 25
    ) -> dict[str, Any]:
        """Search Reddit via web scraping (fallback)."""
        if subreddit:
            url = f"https://www.reddit.com/r/{subreddit}/search/?q={query.replace(' ', '+')}&restrict_sr=1"
        else:
            url = f"https://www.reddit.com/search/?q={query.replace(' ', '+')}"
        
        result = self.firecrawl.scrape(url, formats=["markdown"])
        
        if not result.get("success"):
            return {"error": f"Failed to search Reddit", "posts": []}
        
        content = result.get("data", {}).get("markdown", "")
        
        return {
            "query": query,
            "subreddit": subreddit,
            "url": url,
            "content": content[:15000],
            "posts": [],  # Would need parsing
            "note": "Scraped results - use Reddit API for structured data"
        }
    
    def get_subreddit_posts(
        self,
        subreddit: str,
        sort: str = "hot",
        limit: int = 25
    ) -> dict[str, Any]:
        """
        Get posts from a subreddit.
        
        Args:
            subreddit: Subreddit name
            sort: Sort by (hot, new, top, rising)
            limit: Max posts
        
        Returns:
            List of posts
        """
        if self._use_scraping:
            url = f"https://www.reddit.com/r/{subreddit}/{sort}/"
            result = self.firecrawl.scrape(url, formats=["markdown"])
            
            if not result.get("success"):
                return {"error": f"Failed to scrape r/{subreddit}", "posts": []}
            
            content = result.get("data", {}).get("markdown", "")
            
            return {
                "subreddit": subreddit,
                "url": url,
                "content": content[:15000],
                "posts": []
            }
        
        # Use official API
        result = self.get(f"/r/{subreddit}/{sort}", params={"limit": min(limit, 100)})
        
        posts = []
        for child in result.get("data", {}).get("children", []):
            post = child.get("data", {})
            posts.append({
                "title": post.get("title"),
                "selftext": post.get("selftext", "")[:1000],
                "url": f"https://reddit.com{post.get('permalink', '')}",
                "score": post.get("score"),
                "num_comments": post.get("num_comments"),
                "created_utc": post.get("created_utc"),
                "author": post.get("author")
            })
        
        return {"subreddit": subreddit, "posts": posts}
    
    def get_post_comments(
        self,
        post_url: str,
        limit: int = 50
    ) -> dict[str, Any]:
        """
        Get comments from a Reddit post.
        
        Args:
            post_url: Full Reddit post URL
            limit: Max comments
        
        Returns:
            Post with comments
        """
        if self._use_scraping:
            result = self.firecrawl.scrape(post_url, formats=["markdown"])
            
            if not result.get("success"):
                return {"error": f"Failed to scrape post", "comments": []}
            
            content = result.get("data", {}).get("markdown", "")
            
            return {
                "url": post_url,
                "content": content[:20000],
                "comments": []
            }
        
        # Extract post ID from URL
        import re
        match = re.search(r'/comments/(\w+)/', post_url)
        if not match:
            return {"error": "Invalid Reddit URL"}
        
        post_id = match.group(1)
        result = self.get(f"/comments/{post_id}", params={"limit": limit})
        
        # First item is post, second is comments
        if len(result) < 2:
            return {"error": "Could not fetch comments"}
        
        post_data = result[0]["data"]["children"][0]["data"]
        comments_data = result[1]["data"]["children"]
        
        comments = []
        for child in comments_data:
            if child.get("kind") != "t1":
                continue
            comment = child.get("data", {})
            comments.append({
                "body": comment.get("body", "")[:1000],
                "score": comment.get("score"),
                "author": comment.get("author"),
                "created_utc": comment.get("created_utc")
            })
        
        return {
            "post": {
                "title": post_data.get("title"),
                "selftext": post_data.get("selftext"),
                "score": post_data.get("score"),
                "num_comments": post_data.get("num_comments")
            },
            "comments": comments
        }
    
    def close(self):
        if self.firecrawl:
            self.firecrawl.close()


class TwitterClient:
    """
    Twitter/X search client.
    
    Uses web scraping since Twitter API is expensive.
    Limited functionality - primarily for brand mention monitoring.
    """
    
    def __init__(self):
        self.firecrawl = FirecrawlClient()
    
    def search(self, query: str) -> dict[str, Any]:
        """
        Search Twitter/X for tweets.
        
        Note: Limited without API access. Returns scraped page content.
        
        Args:
            query: Search query
        
        Returns:
            Search results (scraped)
        """
        url = f"https://twitter.com/search?q={query.replace(' ', '%20')}&f=live"
        
        result = self.firecrawl.scrape(url, formats=["markdown"], wait_for=3000)
        
        if not result.get("success"):
            return {"error": "Failed to search Twitter", "tweets": []}
        
        content = result.get("data", {}).get("markdown", "")
        
        return {
            "query": query,
            "url": url,
            "content": content[:10000],
            "note": "Twitter scraping is limited. Consider using official API for production."
        }
    
    def get_profile(self, username: str) -> dict[str, Any]:
        """
        Get Twitter profile page.
        
        Args:
            username: Twitter username (without @)
        
        Returns:
            Profile data (scraped)
        """
        url = f"https://twitter.com/{username}"
        
        result = self.firecrawl.scrape(url, formats=["markdown"], wait_for=3000)
        
        if not result.get("success"):
            return {"error": f"Failed to get profile for @{username}"}
        
        content = result.get("data", {}).get("markdown", "")
        
        return {
            "username": username,
            "url": url,
            "content": content[:10000]
        }
    
    def close(self):
        self.firecrawl.close()


# ============================================================================
# CLI Interface
# ============================================================================

def main():
    """CLI entry point for social media tools."""
    import argparse
    import json
    
    parser = argparse.ArgumentParser(description="Reddit and social media tools")
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    # Reddit search
    reddit_parser = subparsers.add_parser("reddit", help="Search Reddit")
    reddit_parser.add_argument("query", help="Search query")
    reddit_parser.add_argument("--subreddit", "-r", help="Limit to subreddit")
    reddit_parser.add_argument("--sort", choices=["relevance", "hot", "top", "new"], default="relevance")
    reddit_parser.add_argument("--limit", type=int, default=25)
    
    # Subreddit posts
    subreddit_parser = subparsers.add_parser("subreddit", help="Get subreddit posts")
    subreddit_parser.add_argument("name", help="Subreddit name")
    subreddit_parser.add_argument("--sort", choices=["hot", "new", "top", "rising"], default="hot")
    subreddit_parser.add_argument("--limit", type=int, default=25)
    
    # Post comments
    comments_parser = subparsers.add_parser("comments", help="Get post comments")
    comments_parser.add_argument("url", help="Reddit post URL")
    
    # Twitter search
    twitter_parser = subparsers.add_parser("twitter", help="Search Twitter")
    twitter_parser.add_argument("query", help="Search query")
    
    args = parser.parse_args()
    
    if args.command == "reddit":
        client = RedditClient()
        try:
            result = client.search(
                args.query,
                subreddit=args.subreddit,
                sort=args.sort,
                limit=args.limit
            )
            print(json.dumps(result, indent=2))
        finally:
            client.close()
    
    elif args.command == "subreddit":
        client = RedditClient()
        try:
            result = client.get_subreddit_posts(
                args.name,
                sort=args.sort,
                limit=args.limit
            )
            print(json.dumps(result, indent=2))
        finally:
            client.close()
    
    elif args.command == "comments":
        client = RedditClient()
        try:
            result = client.get_post_comments(args.url)
            print(json.dumps(result, indent=2))
        finally:
            client.close()
    
    elif args.command == "twitter":
        client = TwitterClient()
        try:
            result = client.search(args.query)
            print(json.dumps(result, indent=2))
        finally:
            client.close()


if __name__ == "__main__":
    main()
