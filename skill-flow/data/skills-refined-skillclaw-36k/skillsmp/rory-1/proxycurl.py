"""
Proxycurl API Client

Proxycurl provides LinkedIn data without scraping restrictions.
https://nubela.co/proxycurl/

Features:
- Full LinkedIn profile data
- Company pages
- Job listings
- Employee search
- Recent posts/activity

Usage:
    from tools.proxycurl import ProxycurlClient
    
    client = ProxycurlClient()
    
    # Get person profile
    profile = client.get_person_profile("https://linkedin.com/in/username")
    
    # Get company profile
    company = client.get_company_profile("https://linkedin.com/company/example")
    
    # Get recent posts
    posts = client.get_person_posts("https://linkedin.com/in/username")
"""

from typing import Optional, Any
from tools.base import BaseAPIClient, get_credential, has_credential
from tools.errors import format_missing_credential_error, format_error_message


class ProxycurlClient(BaseAPIClient):
    """Proxycurl API client for LinkedIn data."""

    BASE_URL = "https://nubela.co/proxycurl/api"
    SERVICE_NAME = "proxycurl"

    def __init__(self):
        self._is_available = has_credential(self.SERVICE_NAME, "api_key")
        if self._is_available:
            super().__init__()

    @property
    def is_available(self) -> bool:
        """Check if the client has valid credentials configured."""
        return self._is_available

    def get_availability_error(self) -> dict[str, Any]:
        """Get structured error information when credentials are missing."""
        return format_missing_credential_error(self.SERVICE_NAME)

    def get_availability_message(self) -> str:
        """Get human-readable error message when credentials are missing."""
        return format_error_message(self.get_availability_error())

    def _check_availability(self) -> Optional[dict[str, Any]]:
        """Check if client is available, return error dict if not."""
        if not self._is_available:
            error = self.get_availability_error()
            error["data"] = None
            return error
        return None

    def _get_headers(self) -> dict[str, str]:
        api_key = get_credential("proxycurl", "api_key")
        return {
            "Authorization": f"Bearer {api_key}"
        }
    
    # ========================================================================
    # Person Profiles
    # ========================================================================
    
    def get_person_profile(
        self,
        linkedin_url: str,
        skills: bool = True,
        experiences: bool = True,
        education: bool = True,
        certifications: bool = True,
        publications: bool = False,
        honors: bool = False,
        personal_emails: bool = False,
        personal_numbers: bool = False
    ) -> dict[str, Any]:
        """
        Get full LinkedIn profile data for a person.

        Args:
            linkedin_url: LinkedIn profile URL
            skills: Include skills
            experiences: Include work experience
            education: Include education
            certifications: Include certifications
            publications: Include publications
            honors: Include honors/awards
            personal_emails: Include personal emails (extra credit cost)
            personal_numbers: Include personal phone (extra credit cost)

        Returns:
            {
                "public_identifier": "...",
                "first_name": "...",
                "last_name": "...",
                "full_name": "...",
                "headline": "...",
                "summary": "...",
                "city": "...",
                "state": "...",
                "country": "...",
                "experiences": [...],
                "education": [...],
                "skills": [...],
                "connections": int,
                "follower_count": int,
                ...
            }
            Or error dict with recovery steps if credentials missing.
        """
        # Check if credentials are available
        error = self._check_availability()
        if error:
            return error

        params = {
            "url": linkedin_url,
            "skills": "include" if skills else "exclude",
            "inferred_salary": "exclude",
            "personal_email": "include" if personal_emails else "exclude",
            "personal_contact_number": "include" if personal_numbers else "exclude",
            "extra": "include" if (publications or honors) else "exclude"
        }
        
        return self.get("/v2/linkedin", params=params)
    
    def get_person_posts(
        self,
        linkedin_url: str,
        limit: int = 10
    ) -> dict[str, Any]:
        """
        Get recent posts from a LinkedIn profile.

        Args:
            linkedin_url: LinkedIn profile URL
            limit: Max posts to return

        Returns:
            {
                "posts": [
                    {
                        "text": "...",
                        "posted_at": "...",
                        "num_likes": int,
                        "num_comments": int,
                        "url": "..."
                    }
                ]
            }
            Or error dict with recovery steps if credentials missing.
        """
        # Check if credentials are available
        error = self._check_availability()
        if error:
            return error

        params = {
            "linkedin_person_profile_url": linkedin_url,
            "page_size": min(limit, 50)
        }
        
        return self.get("/v2/linkedin/person/post", params=params)
    
    def lookup_person_by_email(self, email: str) -> dict[str, Any]:
        """
        Find LinkedIn profile by email address.

        Args:
            email: Email address

        Returns:
            {
                "url": "linkedin_profile_url" or null,
                ...
            }
            Or error dict with recovery steps if credentials missing.
        """
        # Check if credentials are available
        error = self._check_availability()
        if error:
            return error

        params = {"email": email}
        return self.get("/linkedin/profile/resolve/email", params=params)
    
    def lookup_person_by_name(
        self,
        first_name: str,
        last_name: str,
        company_domain: Optional[str] = None,
        company_name: Optional[str] = None,
        title: Optional[str] = None,
        location: Optional[str] = None
    ) -> dict[str, Any]:
        """
        Find LinkedIn profile by name and company.

        Args:
            first_name: First name
            last_name: Last name
            company_domain: Company website domain
            company_name: Company name
            title: Job title
            location: Location string

        Returns:
            Profile data if found, or error dict with recovery steps if credentials missing.
        """
        # Check if credentials are available
        error = self._check_availability()
        if error:
            return error

        params = {
            "first_name": first_name,
            "last_name": last_name,
            "enrich_profile": "enrich"
        }
        
        if company_domain:
            params["company_domain"] = company_domain
        if company_name:
            params["company_name"] = company_name
        if title:
            params["title"] = title
        if location:
            params["location"] = location
        
        return self.get("/linkedin/profile/resolve", params=params)
    
    # ========================================================================
    # Company Profiles
    # ========================================================================
    
    def get_company_profile(
        self,
        linkedin_url: str,
        resolve_numeric_id: bool = False
    ) -> dict[str, Any]:
        """
        Get LinkedIn company page data.

        Args:
            linkedin_url: LinkedIn company URL
            resolve_numeric_id: Include numeric company ID

        Returns:
            {
                "name": "...",
                "description": "...",
                "website": "...",
                "industry": "...",
                "company_size": [...],
                "hq": {...},
                "specialities": [...],
                "follower_count": int,
                ...
            }
            Or error dict with recovery steps if credentials missing.
        """
        # Check if credentials are available
        error = self._check_availability()
        if error:
            return error

        params = {
            "url": linkedin_url,
            "resolve_numeric_id": str(resolve_numeric_id).lower()
        }
        
        return self.get("/linkedin/company", params=params)
    
    def lookup_company_by_domain(self, domain: str) -> dict[str, Any]:
        """
        Find LinkedIn company page by domain.

        Args:
            domain: Company website domain

        Returns:
            {
                "url": "linkedin_company_url" or null,
                ...
            }
            Or error dict with recovery steps if credentials missing.
        """
        # Check if credentials are available
        error = self._check_availability()
        if error:
            return error

        params = {"domain": domain}
        return self.get("/linkedin/company/resolve", params=params)
    
    def get_company_employees(
        self,
        linkedin_url: str,
        page_size: int = 10,
        country: Optional[str] = None,
        keyword_filter: Optional[str] = None
    ) -> dict[str, Any]:
        """
        Get employees at a company.

        Args:
            linkedin_url: LinkedIn company URL
            page_size: Results per page
            country: Filter by country
            keyword_filter: Filter by keyword in profile

        Returns:
            {
                "employees": [
                    {"profile_url": "...", "profile": {...}}
                ]
            }
            Or error dict with recovery steps if credentials missing.
        """
        # Check if credentials are available
        error = self._check_availability()
        if error:
            return error

        params = {
            "url": linkedin_url,
            "page_size": min(page_size, 100),
            "enrich_profiles": "enrich"
        }
        
        if country:
            params["country"] = country
        if keyword_filter:
            params["keyword_filter"] = keyword_filter
        
        return self.get("/linkedin/company/employees", params=params)
    
    # ========================================================================
    # Job Listings
    # ========================================================================
    
    def get_company_jobs(
        self,
        linkedin_url: str,
        limit: int = 20
    ) -> dict[str, Any]:
        """
        Get job listings from a company.

        Args:
            linkedin_url: LinkedIn company URL
            limit: Max jobs to return

        Returns:
            {
                "jobs": [
                    {
                        "title": "...",
                        "location": "...",
                        "url": "...",
                        "posted_at": "..."
                    }
                ]
            }
            Or error dict with recovery steps if credentials missing.
        """
        # Check if credentials are available
        error = self._check_availability()
        if error:
            return error

        params = {
            "url": linkedin_url,
            "page_size": min(limit, 100)
        }
        
        return self.get("/linkedin/company/job", params=params)
    
    # ========================================================================
    # Helper Methods
    # ========================================================================
    
    def get_profile_summary(self, linkedin_url: str) -> dict[str, Any]:
        """
        Get a summarized view of a LinkedIn profile.

        Returns key info for outreach personalization,
        or error dict with recovery steps if credentials missing.
        """
        # Check if credentials are available
        error = self._check_availability()
        if error:
            return error

        profile = self.get_person_profile(
            linkedin_url,
            skills=True,
            experiences=True,
            education=True,
            certifications=False,
            publications=False
        )
        
        # Extract current role
        current_role = None
        if profile.get("experiences"):
            for exp in profile["experiences"]:
                if exp.get("ends_at") is None:
                    current_role = {
                        "title": exp.get("title"),
                        "company": exp.get("company"),
                        "starts_at": exp.get("starts_at")
                    }
                    break
        
        # Extract education
        education = None
        if profile.get("education"):
            edu = profile["education"][0]
            education = {
                "school": edu.get("school"),
                "degree": edu.get("degree_name"),
                "field": edu.get("field_of_study")
            }
        
        return {
            "name": profile.get("full_name"),
            "headline": profile.get("headline"),
            "location": f"{profile.get('city', '')}, {profile.get('country', '')}".strip(", "),
            "summary": profile.get("summary"),
            "current_role": current_role,
            "education": education,
            "skills": profile.get("skills", [])[:10],
            "connections": profile.get("connections"),
            "followers": profile.get("follower_count"),
            "linkedin_url": linkedin_url
        }


# ============================================================================
# CLI Interface
# ============================================================================

def main():
    """CLI entry point for Proxycurl tools."""
    import argparse
    import json
    import sys

    parser = argparse.ArgumentParser(description="Proxycurl LinkedIn data")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Person profile command
    person_parser = subparsers.add_parser("person", help="Get person profile")
    person_parser.add_argument("url", help="LinkedIn profile URL")
    person_parser.add_argument("--summary", action="store_true", help="Return summary only")
    person_parser.add_argument("--posts", action="store_true", help="Include recent posts")

    # Company profile command
    company_parser = subparsers.add_parser("company", help="Get company profile")
    company_parser.add_argument("url", help="LinkedIn company URL or domain")
    company_parser.add_argument("--employees", action="store_true", help="Include employees")
    company_parser.add_argument("--jobs", action="store_true", help="Include job listings")

    # Lookup commands
    lookup_parser = subparsers.add_parser("lookup", help="Find LinkedIn profile")
    lookup_parser.add_argument("--email", help="Lookup by email")
    lookup_parser.add_argument("--name", help="First and last name")
    lookup_parser.add_argument("--company", help="Company name or domain")

    args = parser.parse_args()
    client = ProxycurlClient()

    # Check if credentials are available
    if not client.is_available:
        print(client.get_availability_message(), file=sys.stderr)
        sys.exit(1)

    try:
        if args.command == "person":
            if args.summary:
                result = client.get_profile_summary(args.url)
            else:
                result = client.get_person_profile(args.url)
            
            print(json.dumps(result, indent=2, default=str))
            
            if args.posts:
                print("\n--- Recent Posts ---\n")
                posts = client.get_person_posts(args.url)
                for post in posts.get("posts", [])[:5]:
                    print(f"[{post.get('posted_at')}] {post.get('text', '')[:200]}...")
                    print(f"  👍 {post.get('num_likes', 0)} | 💬 {post.get('num_comments', 0)}\n")
        
        elif args.command == "company":
            # Check if URL or domain
            if args.url.startswith("http"):
                linkedin_url = args.url
            else:
                lookup = client.lookup_company_by_domain(args.url)
                linkedin_url = lookup.get("url")
                if not linkedin_url:
                    print(f"Could not find LinkedIn page for domain: {args.url}")
                    return
            
            result = client.get_company_profile(linkedin_url)
            print(json.dumps(result, indent=2, default=str))
            
            if args.employees:
                print("\n--- Employees ---\n")
                employees = client.get_company_employees(linkedin_url, page_size=10)
                for emp in employees.get("employees", []):
                    profile = emp.get("profile", {})
                    print(f"  {profile.get('full_name')}: {profile.get('headline')}")
            
            if args.jobs:
                print("\n--- Job Listings ---\n")
                jobs = client.get_company_jobs(linkedin_url)
                for job in jobs.get("jobs", [])[:10]:
                    print(f"  {job.get('title')} - {job.get('location')}")
        
        elif args.command == "lookup":
            if args.email:
                result = client.lookup_person_by_email(args.email)
            elif args.name:
                parts = args.name.split(" ", 1)
                first = parts[0]
                last = parts[1] if len(parts) > 1 else ""
                result = client.lookup_person_by_name(
                    first_name=first,
                    last_name=last,
                    company_name=args.company
                )
            else:
                print("Error: Provide --email or --name")
                return
            
            print(json.dumps(result, indent=2, default=str))
    
    finally:
        client.close()


if __name__ == "__main__":
    main()
