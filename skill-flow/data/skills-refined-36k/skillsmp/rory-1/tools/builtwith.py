"""
BuiltWith API Client

Detect technologies used by websites.
https://builtwith.com/

Features:
- Technology detection
- Tech stack analysis
- Competitor tech comparison

Usage:
    from tools.builtwith import BuiltWithClient
    
    client = BuiltWithClient()
    
    # Get tech stack
    tech = client.lookup("example.com")
"""

from typing import Optional, Any
from tools.base import BaseAPIClient, get_credential, has_credential, extract_domain
from tools.firecrawl import FirecrawlClient


class BuiltWithClient(BaseAPIClient):
    """
    BuiltWith API client for technology detection.
    
    Falls back to scraping BuiltWith's free lookup if no API key.
    """
    
    BASE_URL = "https://api.builtwith.com"
    
    def __init__(self):
        super().__init__()
        self._use_scraping = not has_credential("builtwith", "api_key")
        
        if self._use_scraping:
            self.firecrawl = FirecrawlClient()
        else:
            self.firecrawl = None
    
    def _get_headers(self) -> dict[str, str]:
        if self._use_scraping:
            return {}
        
        return {
            "Content-Type": "application/json"
        }
    
    def lookup(self, domain: str) -> dict[str, Any]:
        """
        Look up technologies used by a domain.
        
        Args:
            domain: Website domain
        
        Returns:
            {
                "domain": "...",
                "technologies": [
                    {
                        "name": "...",
                        "category": "...",
                        "description": "..."
                    }
                ],
                "categories": {
                    "Analytics": [...],
                    "CMS": [...],
                    ...
                }
            }
        """
        domain = extract_domain(domain)
        
        if self._use_scraping:
            return self._lookup_via_scraping(domain)
        
        # Use official API
        api_key = get_credential("builtwith", "api_key")
        result = self.get(
            f"/v21/api.json",
            params={"KEY": api_key, "LOOKUP": domain}
        )
        
        return self._parse_api_response(domain, result)
    
    def _lookup_via_scraping(self, domain: str) -> dict[str, Any]:
        """Look up tech stack via BuiltWith free lookup."""
        url = f"https://builtwith.com/{domain}"
        
        result = self.firecrawl.scrape(url, formats=["markdown"])
        
        if not result.get("success"):
            return {"error": f"Failed to lookup {domain}", "technologies": []}
        
        content = result.get("data", {}).get("markdown", "")
        
        # Parse technologies from content
        technologies = self._parse_scraped_content(content)
        
        return {
            "domain": domain,
            "url": url,
            "technologies": technologies,
            "categories": self._categorize_technologies(technologies),
            "raw_content_length": len(content)
        }
    
    def _parse_api_response(self, domain: str, result: dict) -> dict[str, Any]:
        """Parse official API response."""
        technologies = []
        
        for result_item in result.get("Results", []):
            for path in result_item.get("Result", {}).get("Paths", []):
                for tech in path.get("Technologies", []):
                    technologies.append({
                        "name": tech.get("Name"),
                        "category": tech.get("Categories", ["Other"])[0] if tech.get("Categories") else "Other",
                        "description": tech.get("Description"),
                        "first_detected": tech.get("FirstDetected"),
                        "last_detected": tech.get("LastDetected")
                    })
        
        return {
            "domain": domain,
            "technologies": technologies,
            "categories": self._categorize_technologies(technologies)
        }
    
    def _parse_scraped_content(self, content: str) -> list[dict[str, str]]:
        """Parse technologies from scraped BuiltWith page."""
        import re
        
        technologies = []
        
        # Look for technology mentions
        # BuiltWith pages have sections like "Analytics and Tracking", "Widgets", etc.
        
        # Common technology patterns
        tech_patterns = [
            r'([A-Z][a-zA-Z0-9\s\.\-]+)\s*[-–]\s*([A-Za-z\s]+)',  # "Google Analytics - Analytics"
            r'###?\s*([A-Z][a-zA-Z0-9\s\.\-]+)',  # Headers often contain tech names
        ]
        
        for pattern in tech_patterns:
            matches = re.findall(pattern, content)
            for match in matches:
                if isinstance(match, tuple):
                    name, category = match
                else:
                    name, category = match, "Unknown"
                
                name = name.strip()
                if len(name) > 2 and len(name) < 50:
                    technologies.append({
                        "name": name,
                        "category": category.strip() if isinstance(category, str) else "Unknown"
                    })
        
        # Deduplicate
        seen = set()
        unique_tech = []
        for tech in technologies:
            if tech["name"].lower() not in seen:
                seen.add(tech["name"].lower())
                unique_tech.append(tech)
        
        return unique_tech[:50]  # Limit results
    
    def _categorize_technologies(
        self,
        technologies: list[dict]
    ) -> dict[str, list[str]]:
        """Group technologies by category."""
        categories: dict[str, list[str]] = {}
        
        for tech in technologies:
            category = tech.get("category", "Other")
            if category not in categories:
                categories[category] = []
            categories[category].append(tech.get("name", ""))
        
        return categories
    
    def compare_tech_stacks(
        self,
        domain1: str,
        domain2: str
    ) -> dict[str, Any]:
        """
        Compare tech stacks of two domains.
        
        Args:
            domain1: First domain
            domain2: Second domain
        
        Returns:
            {
                "domain1": {...},
                "domain2": {...},
                "shared": [...],
                "only_domain1": [...],
                "only_domain2": [...]
            }
        """
        stack1 = self.lookup(domain1)
        stack2 = self.lookup(domain2)
        
        tech1_names = {t.get("name", "").lower() for t in stack1.get("technologies", [])}
        tech2_names = {t.get("name", "").lower() for t in stack2.get("technologies", [])}
        
        shared = tech1_names & tech2_names
        only1 = tech1_names - tech2_names
        only2 = tech2_names - tech1_names
        
        return {
            "domain1": {
                "domain": domain1,
                "tech_count": len(tech1_names),
                "technologies": stack1.get("technologies", [])
            },
            "domain2": {
                "domain": domain2,
                "tech_count": len(tech2_names),
                "technologies": stack2.get("technologies", [])
            },
            "shared": list(shared),
            "only_domain1": list(only1),
            "only_domain2": list(only2)
        }
    
    def close(self):
        if self.firecrawl:
            self.firecrawl.close()


# ============================================================================
# Wappalyzer Alternative (Free)
# ============================================================================

class TechDetector:
    """
    Simple tech detection using page analysis.
    
    Detects common technologies by analyzing HTML/JS.
    No API key required.
    """
    
    # Common technology signatures
    SIGNATURES = {
        # Analytics
        "Google Analytics": ["google-analytics.com", "gtag", "ga.js", "analytics.js"],
        "Mixpanel": ["mixpanel.com", "mixpanel.init"],
        "Segment": ["segment.com", "analytics.js", "segment.io"],
        "Amplitude": ["amplitude.com", "amplitude.init"],
        "Hotjar": ["hotjar.com", "hj.js"],
        "Heap": ["heap.io", "heap.load"],
        
        # Marketing
        "HubSpot": ["hubspot.com", "hs-scripts", "hbspt"],
        "Marketo": ["marketo.com", "munchkin"],
        "Intercom": ["intercom.io", "intercomSettings"],
        "Drift": ["drift.com", "driftt"],
        "Salesforce": ["salesforce.com", "pardot"],
        
        # CMS/Frameworks
        "WordPress": ["wp-content", "wp-includes", "wordpress"],
        "Webflow": ["webflow.com", "wf-"],
        "Squarespace": ["squarespace.com", "sqsp"],
        "Shopify": ["shopify.com", "cdn.shopify"],
        "React": ["react", "__REACT", "reactDOM"],
        "Vue.js": ["vue.js", "__VUE"],
        "Next.js": ["_next", "next.js"],
        
        # Infrastructure
        "Cloudflare": ["cloudflare", "cf-ray"],
        "AWS": ["amazonaws.com", "cloudfront"],
        "Vercel": ["vercel.com", "vercel.app"],
        "Netlify": ["netlify.com", "netlify.app"],
        
        # Chat/Support
        "Zendesk": ["zendesk.com", "zdassets"],
        "Freshdesk": ["freshdesk.com", "freshchat"],
        "Crisp": ["crisp.chat", "crisp.im"],
        
        # Payment
        "Stripe": ["stripe.com", "stripe.js"],
        "PayPal": ["paypal.com", "paypalobjects"],
    }
    
    def __init__(self):
        self.firecrawl = FirecrawlClient()
    
    def detect(self, domain: str) -> dict[str, Any]:
        """
        Detect technologies on a website.
        
        Args:
            domain: Website domain
        
        Returns:
            Detected technologies
        """
        domain = extract_domain(domain)
        url = f"https://{domain}"
        
        result = self.firecrawl.scrape(url, formats=["html"])
        
        if not result.get("success"):
            return {"error": f"Failed to analyze {domain}", "technologies": []}
        
        html = result.get("data", {}).get("html", "")
        
        detected = []
        for tech_name, signatures in self.SIGNATURES.items():
            for sig in signatures:
                if sig.lower() in html.lower():
                    detected.append({
                        "name": tech_name,
                        "confidence": "high" if sig in html else "medium"
                    })
                    break
        
        return {
            "domain": domain,
            "technologies": detected,
            "tech_count": len(detected)
        }
    
    def close(self):
        self.firecrawl.close()


# ============================================================================
# CLI Interface
# ============================================================================

def main():
    """CLI entry point for tech detection tools."""
    import argparse
    import json
    
    parser = argparse.ArgumentParser(description="Technology detection tools")
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    # Lookup command
    lookup_parser = subparsers.add_parser("lookup", help="Look up tech stack")
    lookup_parser.add_argument("domain", help="Domain to analyze")
    lookup_parser.add_argument("--quick", action="store_true", help="Use quick detection (no API)")
    
    # Compare command
    compare_parser = subparsers.add_parser("compare", help="Compare tech stacks")
    compare_parser.add_argument("domain1", help="First domain")
    compare_parser.add_argument("domain2", help="Second domain")
    
    args = parser.parse_args()
    
    if args.command == "lookup":
        if args.quick:
            client = TechDetector()
        else:
            client = BuiltWithClient()
        
        try:
            result = client.lookup(args.domain) if hasattr(client, 'lookup') else client.detect(args.domain)
            
            print(f"\n🔍 Tech Stack for {args.domain}\n")
            print("-" * 40)
            
            for tech in result.get("technologies", []):
                print(f"  • {tech.get('name')}")
            
            print(f"\n📊 Total: {len(result.get('technologies', []))} technologies detected")
            
            if result.get("categories"):
                print("\n📁 By Category:")
                for cat, techs in result["categories"].items():
                    print(f"  {cat}: {', '.join(techs)}")
        
        finally:
            client.close()
    
    elif args.command == "compare":
        client = BuiltWithClient()
        
        try:
            result = client.compare_tech_stacks(args.domain1, args.domain2)
            
            print(f"\n🔄 Tech Stack Comparison\n")
            print(f"{args.domain1}: {result['domain1']['tech_count']} technologies")
            print(f"{args.domain2}: {result['domain2']['tech_count']} technologies")
            print(f"\n✅ Shared ({len(result['shared'])}): {', '.join(list(result['shared'])[:10])}")
            print(f"\n🔹 Only {args.domain1} ({len(result['only_domain1'])}): {', '.join(list(result['only_domain1'])[:10])}")
            print(f"\n🔸 Only {args.domain2} ({len(result['only_domain2'])}): {', '.join(list(result['only_domain2'])[:10])}")
        
        finally:
            client.close()


if __name__ == "__main__":
    main()
