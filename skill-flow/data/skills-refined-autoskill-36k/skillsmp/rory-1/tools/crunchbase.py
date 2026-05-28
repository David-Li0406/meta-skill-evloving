"""
Crunchbase Data Tool

Get company funding, investors, and M&A data from Crunchbase.
Uses web scraping since Crunchbase API is enterprise-only.

Features:
- Company funding history
- Investor information
- Acquisitions
- Key people

Usage:
    from tools.crunchbase import CrunchbaseClient
    
    client = CrunchbaseClient()
    company = client.lookup("notion")
"""

from typing import Optional, Any
from tools.firecrawl import FirecrawlClient
from tools.base import extract_domain


class CrunchbaseClient:
    """Crunchbase data via web scraping."""
    
    def __init__(self):
        self.firecrawl = FirecrawlClient()
    
    def lookup(self, company_slug: str) -> dict[str, Any]:
        """
        Look up company on Crunchbase.
        
        Args:
            company_slug: Company slug (e.g., "notion" for notion.so)
        
        Returns:
            Company data including funding
        """
        # Clean slug
        slug = company_slug.lower().replace(" ", "-").replace(".", "-")
        url = f"https://www.crunchbase.com/organization/{slug}"
        
        result = self.firecrawl.scrape(url, formats=["markdown"], wait_for=2000)
        
        if not result.get("success"):
            return {"error": f"Failed to lookup {company_slug}", "url": url}
        
        content = result.get("data", {}).get("markdown", "")
        metadata = result.get("data", {}).get("metadata", {})
        
        # Parse key data points
        parsed = self._parse_crunchbase_content(content)
        
        return {
            "company": company_slug,
            "url": url,
            "title": metadata.get("title", ""),
            "description": metadata.get("description", ""),
            "parsed": parsed,
            "raw_content": content[:8000],
            "raw_content_length": len(content)
        }
    
    def get_funding_rounds(self, company_slug: str) -> dict[str, Any]:
        """
        Get detailed funding rounds for a company.
        
        Args:
            company_slug: Company slug
        
        Returns:
            Funding rounds data
        """
        slug = company_slug.lower().replace(" ", "-").replace(".", "-")
        url = f"https://www.crunchbase.com/organization/{slug}/company_financials"
        
        result = self.firecrawl.scrape(url, formats=["markdown"], wait_for=2000)
        
        if not result.get("success"):
            return {"error": f"Failed to get funding for {company_slug}"}
        
        content = result.get("data", {}).get("markdown", "")
        
        return {
            "company": company_slug,
            "url": url,
            "content": content[:10000],
            "raw_content_length": len(content)
        }
    
    def get_people(self, company_slug: str) -> dict[str, Any]:
        """
        Get key people at a company.
        
        Args:
            company_slug: Company slug
        
        Returns:
            People data
        """
        slug = company_slug.lower().replace(" ", "-").replace(".", "-")
        url = f"https://www.crunchbase.com/organization/{slug}/people"
        
        result = self.firecrawl.scrape(url, formats=["markdown"], wait_for=2000)
        
        if not result.get("success"):
            return {"error": f"Failed to get people for {company_slug}"}
        
        content = result.get("data", {}).get("markdown", "")
        
        return {
            "company": company_slug,
            "url": url,
            "content": content[:10000],
            "raw_content_length": len(content)
        }
    
    def search(self, query: str) -> dict[str, Any]:
        """
        Search Crunchbase for companies.
        
        Args:
            query: Search query
        
        Returns:
            Search results
        """
        url = f"https://www.crunchbase.com/textsearch?q={query.replace(' ', '%20')}"
        
        result = self.firecrawl.scrape(url, formats=["markdown"], wait_for=2000)
        
        if not result.get("success"):
            return {"error": f"Failed to search for {query}"}
        
        content = result.get("data", {}).get("markdown", "")
        
        return {
            "query": query,
            "url": url,
            "content": content[:10000],
            "raw_content_length": len(content)
        }
    
    def _parse_crunchbase_content(self, content: str) -> dict[str, Any]:
        """Parse key data from Crunchbase page content."""
        import re
        
        parsed = {}
        
        # Try to extract funding amount
        funding_patterns = [
            r'Total Funding[:\s]*\$?([\d,.]+[BMK]?)',
            r'raised[:\s]*\$?([\d,.]+[BMK]?)',
            r'\$?([\d,.]+[BMK]?)\s*(?:total funding|raised)',
        ]
        
        for pattern in funding_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                parsed["total_funding"] = match.group(1)
                break
        
        # Try to extract last funding round
        round_patterns = [
            r'(Series [A-Z]|Seed|Pre-Seed|IPO)\s*[-–]\s*\$?([\d,.]+[BMK]?)',
            r'Last Funding[:\s]*(Series [A-Z]|Seed)',
        ]
        
        for pattern in round_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                parsed["last_round"] = match.group(1)
                if len(match.groups()) > 1:
                    parsed["last_round_amount"] = match.group(2)
                break
        
        # Try to extract employee count
        emp_patterns = [
            r'(\d+[-–]\d+)\s*employees',
            r'employees[:\s]*(\d+[-–]\d+)',
            r'(\d+)\s*employees',
        ]
        
        for pattern in emp_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                parsed["employees"] = match.group(1)
                break
        
        # Try to extract founded year
        founded_match = re.search(r'(?:founded|established)[:\s]*(\d{4})', content, re.IGNORECASE)
        if founded_match:
            parsed["founded"] = founded_match.group(1)
        
        # Try to extract headquarters
        hq_match = re.search(r'(?:headquarters|hq|based in)[:\s]*([A-Za-z\s,]+)', content, re.IGNORECASE)
        if hq_match:
            parsed["headquarters"] = hq_match.group(1).strip()[:50]
        
        return parsed
    
    def close(self):
        self.firecrawl.close()
    
    def __enter__(self):
        return self
    
    def __exit__(self, *args):
        self.close()


# ============================================================================
# CLI Interface
# ============================================================================

def main():
    """CLI entry point for Crunchbase tools."""
    import argparse
    import json
    
    parser = argparse.ArgumentParser(description="Crunchbase company data")
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    # Lookup command
    lookup_parser = subparsers.add_parser("lookup", help="Look up a company")
    lookup_parser.add_argument("company", help="Company slug (e.g., 'notion')")
    lookup_parser.add_argument("--funding", action="store_true", help="Get detailed funding")
    lookup_parser.add_argument("--people", action="store_true", help="Get key people")
    
    # Search command
    search_parser = subparsers.add_parser("search", help="Search companies")
    search_parser.add_argument("query", help="Search query")
    
    args = parser.parse_args()
    client = CrunchbaseClient()
    
    try:
        if args.command == "lookup":
            result = client.lookup(args.company)
            
            print(f"\n📊 Crunchbase: {args.company}\n")
            print("-" * 40)
            
            parsed = result.get("parsed", {})
            if parsed.get("total_funding"):
                print(f"💰 Total Funding: ${parsed['total_funding']}")
            if parsed.get("last_round"):
                print(f"📈 Last Round: {parsed['last_round']}")
            if parsed.get("employees"):
                print(f"👥 Employees: {parsed['employees']}")
            if parsed.get("founded"):
                print(f"📅 Founded: {parsed['founded']}")
            if parsed.get("headquarters"):
                print(f"📍 HQ: {parsed['headquarters']}")
            
            print(f"\n🔗 {result.get('url')}")
            
            if args.funding:
                print("\n--- Funding Details ---")
                funding = client.get_funding_rounds(args.company)
                print(funding.get("content", "")[:2000])
            
            if args.people:
                print("\n--- Key People ---")
                people = client.get_people(args.company)
                print(people.get("content", "")[:2000])
        
        elif args.command == "search":
            result = client.search(args.query)
            print(json.dumps(result, indent=2))
    
    finally:
        client.close()


if __name__ == "__main__":
    main()
