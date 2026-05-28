"""
Clearbit API Client

Clearbit provides company and person enrichment data.
https://clearbit.com/docs

Features:
- Company enrichment (firmographics, tech stack, funding)
- Person enrichment
- Company name/domain resolution

Usage:
    from tools.clearbit import ClearbitClient

    client = ClearbitClient()

    # Check if available
    if not client.is_available:
        print(client.get_availability_error())

    # Enrich company
    company = client.enrich_company("example.com")

    # Enrich person
    person = client.enrich_person("john@example.com")
"""

from typing import Optional, Any
from tools.base import BaseAPIClient, get_credential, has_credential, extract_domain
from tools.errors import format_missing_credential_error, format_error_message


class ClearbitClient(BaseAPIClient):
    """Clearbit API client for enrichment data."""

    BASE_URL = "https://company.clearbit.com/v2"
    PERSON_URL = "https://person.clearbit.com/v2"
    SERVICE_NAME = "clearbit"

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
        api_key = get_credential("clearbit", "api_key")
        return {
            "Authorization": f"Bearer {api_key}"
        }
    
    def enrich_company(self, domain: str) -> dict[str, Any]:
        """
        Enrich company data by domain.

        Args:
            domain: Company website domain

        Returns:
            {
                "id": "...",
                "name": "...",
                "legalName": "...",
                "domain": "...",
                "domainAliases": [...],
                "site": {...},
                "category": {...},
                "tags": [...],
                "description": "...",
                "foundedYear": int,
                "location": "...",
                "geo": {...},
                "logo": "...",
                "facebook": {...},
                "linkedin": {...},
                "twitter": {...},
                "crunchbase": {...},
                "emailProvider": bool,
                "type": "...",
                "ticker": "...",
                "identifiers": {...},
                "phone": "...",
                "metrics": {
                    "employees": int,
                    "employeesRange": "...",
                    "raised": int,
                    "annualRevenue": int,
                    "estimatedAnnualRevenue": "...",
                    ...
                },
                "tech": [...],
                "techCategories": [...],
                "parent": {...},
                "ultimateParent": {...}
            }

            If credentials are missing, returns error dict with recovery steps.
        """
        # Check if credentials are available
        error = self._check_availability()
        if error:
            return error

        domain = extract_domain(domain)
        return self.get(f"/companies/find?domain={domain}")
    
    def enrich_person(
        self,
        email: str,
        include_company: bool = True
    ) -> dict[str, Any]:
        """
        Enrich person data by email.

        Args:
            email: Person's email address
            include_company: Include company data in response

        Returns:
            {
                "id": "...",
                "name": {...},
                "email": "...",
                "location": "...",
                "geo": {...},
                "bio": "...",
                "site": "...",
                "avatar": "...",
                "employment": {...},
                "facebook": {...},
                "github": {...},
                "twitter": {...},
                "linkedin": {...},
                "company": {...} (if include_company)
            }

            If credentials are missing, returns error dict with recovery steps.
        """
        # Check if credentials are available
        error = self._check_availability()
        if error:
            return error

        # Use combined endpoint for person + company
        if include_company:
            url = f"https://person-stream.clearbit.com/v2/combined/find?email={email}"
        else:
            url = f"{self.PERSON_URL}/people/find?email={email}"

        return self.get(url.replace(self.BASE_URL, ""))
    
    def find_company(
        self,
        name: Optional[str] = None,
        domain: Optional[str] = None
    ) -> dict[str, Any]:
        """
        Find company by name or domain.

        Args:
            name: Company name
            domain: Company domain

        Returns:
            Company data if found, or error dict if credentials missing.
        """
        # Check if credentials are available
        error = self._check_availability()
        if error:
            return error

        if domain:
            return self.enrich_company(domain)
        elif name:
            # Use name-to-domain lookup
            return self.get(f"/companies/find?name={name}")
        else:
            return {"error": True, "message": "Provide either name or domain"}
    
    def get_company_tech_stack(self, domain: str) -> list[str] | dict[str, Any]:
        """
        Get technologies used by a company.

        Args:
            domain: Company domain

        Returns:
            List of technology names, or error dict if credentials missing.
        """
        company = self.enrich_company(domain)
        if company.get("error"):
            return company
        return company.get("tech", [])
    
    def get_company_metrics(self, domain: str) -> dict[str, Any]:
        """
        Get company metrics (employees, revenue, funding).

        Args:
            domain: Company domain

        Returns:
            Metrics dictionary, or error dict if credentials missing.
        """
        company = self.enrich_company(domain)
        if company.get("error"):
            return company
        return company.get("metrics", {})


# ============================================================================
# CLI Interface
# ============================================================================

def main():
    """CLI entry point for Clearbit tools."""
    import argparse
    import json
    import sys

    parser = argparse.ArgumentParser(description="Clearbit enrichment data")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Company command
    company_parser = subparsers.add_parser("company", help="Enrich company")
    company_parser.add_argument("domain", help="Company domain")
    company_parser.add_argument("--tech", action="store_true", help="Show tech stack only")
    company_parser.add_argument("--metrics", action="store_true", help="Show metrics only")

    # Person command
    person_parser = subparsers.add_parser("person", help="Enrich person")
    person_parser.add_argument("email", help="Email address")
    person_parser.add_argument("--no-company", action="store_true", help="Exclude company data")

    args = parser.parse_args()
    client = ClearbitClient()

    # Check if credentials are available
    if not client.is_available:
        print(client.get_availability_message(), file=sys.stderr)
        sys.exit(1)

    try:
        if args.command == "company":
            if args.tech:
                result = client.get_company_tech_stack(args.domain)
                if isinstance(result, dict) and result.get("error"):
                    print(json.dumps(result, indent=2), file=sys.stderr)
                    sys.exit(1)
                print("\nTech Stack:")
                for tech in result:
                    print(f"  • {tech}")
            elif args.metrics:
                result = client.get_company_metrics(args.domain)
                if result.get("error"):
                    print(json.dumps(result, indent=2), file=sys.stderr)
                    sys.exit(1)
                print("\nCompany Metrics:")
                print(json.dumps(result, indent=2))
            else:
                result = client.enrich_company(args.domain)
                if result.get("error"):
                    print(json.dumps(result, indent=2), file=sys.stderr)
                    sys.exit(1)
                print(json.dumps(result, indent=2))

        elif args.command == "person":
            result = client.enrich_person(
                args.email,
                include_company=not args.no_company
            )
            if result.get("error"):
                print(json.dumps(result, indent=2), file=sys.stderr)
                sys.exit(1)
            print(json.dumps(result, indent=2))

    finally:
        if client.is_available:
            client.close()


if __name__ == "__main__":
    main()
