"""
Apollo.io API Client

Apollo provides contact and company data for sales and marketing.
https://apolloio.github.io/apollo-api-docs/

Features:
- Search for people by title, company, industry
- Enrich contacts with email, phone, LinkedIn
- Company data and employee counts
- Lead scoring and intent data

Usage:
    from tools.apollo import ApolloClient

    client = ApolloClient()

    # Check if available
    if not client.is_available:
        print(client.get_availability_error())

    # Search for people
    contacts = client.people_search(
        titles=["VP Marketing", "CMO"],
        company_size=["50-200"],
        limit=25
    )

    # Enrich a contact
    contact = client.enrich_person(email="john@example.com")

    # Get company data
    company = client.company_search(domain="example.com")
"""

from typing import Optional, Any
from tools.base import BaseAPIClient, get_credential, has_credential, extract_domain
from tools.errors import format_missing_credential_error, format_error_message


class ApolloClient(BaseAPIClient):
    """Apollo.io API client for contact and company data."""

    BASE_URL = "https://api.apollo.io/v1"
    SERVICE_NAME = "apollo"

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
        api_key = get_credential("apollo", "api_key")
        return {
            "Content-Type": "application/json",
            "Cache-Control": "no-cache",
            "X-Api-Key": api_key
        }
    
    # ========================================================================
    # People Search & Enrichment
    # ========================================================================
    
    def people_search(
        self,
        titles: Optional[list[str]] = None,
        company: Optional[str] = None,
        company_domains: Optional[list[str]] = None,
        company_size: Optional[list[str]] = None,
        industries: Optional[list[str]] = None,
        locations: Optional[list[str]] = None,
        seniority: Optional[list[str]] = None,
        keywords: Optional[str] = None,
        page: int = 1,
        limit: int = 25
    ) -> dict[str, Any]:
        """
        Search for people matching criteria.

        Args:
            titles: Job titles to search (e.g., ["VP Marketing", "CMO"])
            company: Company name
            company_domains: Company domains (e.g., ["example.com"])
            company_size: Company sizes (e.g., ["1-10", "11-50", "51-200", "201-500", "501-1000", "1001-5000", "5001+"])
            industries: Industry names
            locations: Location names (e.g., ["United States", "San Francisco"])
            seniority: Seniority levels (e.g., ["c_suite", "vp", "director", "manager"])
            keywords: Keyword search across profiles
            page: Page number (1-indexed)
            limit: Results per page (max 100)

        Returns:
            {
                "people": [...],
                "pagination": {...}
            }
            Or error dict with recovery steps if credentials missing.
        """
        # Check if credentials are available
        error = self._check_availability()
        if error:
            return error

        payload: dict[str, Any] = {
            "page": page,
            "per_page": min(limit, 100)
        }

        if titles:
            payload["person_titles"] = titles
        if company:
            payload["q_organization_name"] = company
        if company_domains:
            payload["organization_domains"] = company_domains
        if company_size:
            payload["organization_num_employees_ranges"] = company_size
        if industries:
            payload["organization_industry_tag_ids"] = industries
        if locations:
            payload["person_locations"] = locations
        if seniority:
            payload["person_seniorities"] = seniority
        if keywords:
            payload["q_keywords"] = keywords

        return self.post("/mixed_people/search", json=payload)
    
    def enrich_person(
        self,
        email: Optional[str] = None,
        linkedin_url: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        company_domain: Optional[str] = None
    ) -> dict[str, Any]:
        """
        Enrich a person's profile with contact data.

        Provide either email OR LinkedIn URL OR (name + company).

        Args:
            email: Person's email address
            linkedin_url: LinkedIn profile URL
            first_name: First name (requires last_name and company_domain)
            last_name: Last name (requires first_name and company_domain)
            company_domain: Company domain (used with name)

        Returns:
            {
                "person": {...}
            }
            Or error dict with recovery steps if credentials missing.
        """
        # Check if credentials are available
        error = self._check_availability()
        if error:
            return error

        payload: dict[str, Any] = {}

        if email:
            payload["email"] = email
        elif linkedin_url:
            payload["linkedin_url"] = linkedin_url
        elif first_name and last_name and company_domain:
            payload["first_name"] = first_name
            payload["last_name"] = last_name
            payload["domain"] = company_domain
        else:
            return {
                "error": True,
                "message": "Provide email, linkedin_url, or (first_name + last_name + company_domain)"
            }

        return self.post("/people/match", json=payload)
    
    def bulk_enrich_people(
        self,
        emails: Optional[list[str]] = None,
        linkedin_urls: Optional[list[str]] = None
    ) -> dict[str, Any]:
        """
        Bulk enrich multiple people.

        Args:
            emails: List of email addresses
            linkedin_urls: List of LinkedIn URLs

        Returns:
            {
                "matches": [...],
                "status": "..."
            }
            Or error dict with recovery steps if credentials missing.
        """
        # Check if credentials are available
        error = self._check_availability()
        if error:
            return error

        payload: dict[str, Any] = {}

        if emails:
            payload["emails"] = emails
        if linkedin_urls:
            payload["linkedin_urls"] = linkedin_urls

        return self.post("/people/bulk_match", json=payload)
    
    # ========================================================================
    # Company Search & Enrichment
    # ========================================================================
    
    def company_search(
        self,
        domain: Optional[str] = None,
        name: Optional[str] = None,
        company_size: Optional[list[str]] = None,
        industries: Optional[list[str]] = None,
        locations: Optional[list[str]] = None,
        keywords: Optional[str] = None,
        page: int = 1,
        limit: int = 25
    ) -> dict[str, Any]:
        """
        Search for companies matching criteria.

        Args:
            domain: Company domain (e.g., "example.com")
            name: Company name
            company_size: Employee count ranges
            industries: Industry filters
            locations: HQ locations
            keywords: Keyword search
            page: Page number
            limit: Results per page

        Returns:
            {
                "organizations": [...],
                "pagination": {...}
            }
            Or error dict with recovery steps if credentials missing.
        """
        # Check if credentials are available
        error = self._check_availability()
        if error:
            return error

        payload: dict[str, Any] = {
            "page": page,
            "per_page": min(limit, 100)
        }
        
        if domain:
            payload["organization_domains"] = [extract_domain(domain)]
        if name:
            payload["q_organization_name"] = name
        if company_size:
            payload["organization_num_employees_ranges"] = company_size
        if industries:
            payload["organization_industry_tag_ids"] = industries
        if locations:
            payload["organization_locations"] = locations
        if keywords:
            payload["q_keywords"] = keywords
        
        return self.post("/mixed_companies/search", json=payload)
    
    def enrich_company(self, domain: str) -> dict[str, Any]:
        """
        Enrich company data by domain.

        Args:
            domain: Company domain

        Returns:
            {
                "organization": {
                    "id": "...",
                    "name": "...",
                    "website_url": "...",
                    "industry": "...",
                    "estimated_num_employees": int,
                    "founded_year": int,
                    "linkedin_url": "...",
                    "phone": "...",
                    "technologies": [...]
                }
            }
            Or error dict with recovery steps if credentials missing.
        """
        # Check if credentials are available
        error = self._check_availability()
        if error:
            return error

        payload = {
            "domain": extract_domain(domain)
        }
        
        return self.post("/organizations/enrich", json=payload)
    
    # ========================================================================
    # Helper Methods
    # ========================================================================
    
    def find_contacts_at_company(
        self,
        company: str,
        titles: list[str],
        limit: int = 10
    ) -> list[dict[str, Any]]:
        """
        Find contacts with specific titles at a company.
        
        Args:
            company: Company name or domain
            titles: List of job titles to find
            limit: Max contacts to return
        
        Returns:
            List of contact dictionaries
        """
        # Determine if company is a domain or name
        if "." in company and " " not in company:
            result = self.people_search(
                titles=titles,
                company_domains=[company],
                limit=limit
            )
        else:
            result = self.people_search(
                titles=titles,
                company=company,
                limit=limit
            )
        
        return result.get("people", [])
    
    def get_company_employees(
        self,
        domain: str,
        seniority: Optional[list[str]] = None,
        limit: int = 50
    ) -> list[dict[str, Any]]:
        """
        Get employees at a company.
        
        Args:
            domain: Company domain
            seniority: Filter by seniority (c_suite, vp, director, manager)
            limit: Max employees to return
        
        Returns:
            List of employee dictionaries
        """
        result = self.people_search(
            company_domains=[extract_domain(domain)],
            seniority=seniority,
            limit=limit
        )
        
        return result.get("people", [])


# ============================================================================
# CLI Interface
# ============================================================================

def main():
    """CLI entry point for Apollo tools."""
    import argparse
    import json
    import sys

    parser = argparse.ArgumentParser(description="Apollo.io contact and company data")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # People search command
    people_parser = subparsers.add_parser("people", help="Search for people")
    people_parser.add_argument("--titles", nargs="+", help="Job titles to search")
    people_parser.add_argument("--company", help="Company name")
    people_parser.add_argument("--domain", help="Company domain")
    people_parser.add_argument("--size", nargs="+", help="Company size ranges")
    people_parser.add_argument("--seniority", nargs="+", choices=["c_suite", "vp", "director", "manager", "senior", "entry"])
    people_parser.add_argument("--limit", type=int, default=25)
    people_parser.add_argument("--output", choices=["json", "table"], default="table")

    # Enrich person command
    enrich_parser = subparsers.add_parser("enrich", help="Enrich a person")
    enrich_parser.add_argument("--email", help="Email address")
    enrich_parser.add_argument("--linkedin", help="LinkedIn URL")
    enrich_parser.add_argument("--name", help="Full name (requires --domain)")
    enrich_parser.add_argument("--domain", help="Company domain (for name lookup)")

    # Company search command
    company_parser = subparsers.add_parser("company", help="Search/enrich company")
    company_parser.add_argument("domain", help="Company domain")
    company_parser.add_argument("--employees", action="store_true", help="Also fetch employees")

    args = parser.parse_args()
    client = ApolloClient()

    # Check if credentials are available
    if not client.is_available:
        print(client.get_availability_message(), file=sys.stderr)
        sys.exit(1)

    try:
        if args.command == "people":
            result = client.people_search(
                titles=args.titles,
                company=args.company,
                company_domains=[args.domain] if args.domain else None,
                company_size=args.size,
                seniority=args.seniority,
                limit=args.limit
            )
            
            people = result.get("people", [])
            
            if args.output == "json":
                print(json.dumps(people, indent=2))
            else:
                print(f"\nFound {len(people)} contacts:\n")
                print(f"{'Name':<30} {'Title':<35} {'Company':<25} {'Email':<35}")
                print("-" * 125)
                for p in people:
                    name = f"{p.get('first_name', '')} {p.get('last_name', '')}"
                    title = p.get('title', '')[:33]
                    company = p.get('organization', {}).get('name', '')[:23]
                    email = p.get('email', 'N/A')
                    print(f"{name:<30} {title:<35} {company:<25} {email:<35}")
        
        elif args.command == "enrich":
            if args.email:
                result = client.enrich_person(email=args.email)
            elif args.linkedin:
                result = client.enrich_person(linkedin_url=args.linkedin)
            elif args.name and args.domain:
                parts = args.name.split(" ", 1)
                first = parts[0]
                last = parts[1] if len(parts) > 1 else ""
                result = client.enrich_person(
                    first_name=first,
                    last_name=last,
                    company_domain=args.domain
                )
            else:
                print("Error: Provide --email, --linkedin, or (--name and --domain)")
                return
            
            print(json.dumps(result, indent=2))
        
        elif args.command == "company":
            result = client.enrich_company(args.domain)
            print(json.dumps(result, indent=2))
            
            if args.employees:
                print("\n--- Key Employees ---\n")
                employees = client.get_company_employees(
                    args.domain,
                    seniority=["c_suite", "vp", "director"],
                    limit=20
                )
                for e in employees:
                    name = f"{e.get('first_name', '')} {e.get('last_name', '')}"
                    print(f"  {name}: {e.get('title', '')}")
    
    finally:
        client.close()


if __name__ == "__main__":
    main()
