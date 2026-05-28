"""
Review Sites Scraper

Scrape product reviews and data from G2 and Capterra.
Uses Firecrawl for reliable scraping of JavaScript-rendered pages.

Features:
- G2 product reviews and ratings
- G2 category comparisons
- Capterra reviews
- Review sentiment analysis

Usage:
    from tools.reviews import ReviewScraper
    
    scraper = ReviewScraper()
    
    # Get G2 reviews
    reviews = scraper.get_g2_reviews("hubspot-marketing")
    
    # Get Capterra reviews
    reviews = scraper.get_capterra_reviews("hubspot")
    
    # Compare products
    comparison = scraper.compare_on_g2("hubspot-marketing", "salesforce-marketing-cloud")
"""

import re
from typing import Optional, Any
from tools.firecrawl import FirecrawlClient


class ReviewScraper:
    """Scraper for G2, Capterra, and other review sites."""
    
    def __init__(self):
        self.firecrawl = FirecrawlClient()
    
    def close(self):
        self.firecrawl.close()
    
    def __enter__(self):
        return self
    
    def __exit__(self, *args):
        self.close()
    
    # ========================================================================
    # G2 Scraping
    # ========================================================================
    
    def get_g2_product_url(self, product_slug: str) -> str:
        """Convert product slug to G2 URL."""
        return f"https://www.g2.com/products/{product_slug}/reviews"
    
    def get_g2_reviews(
        self,
        product_slug: str,
        max_pages: int = 1
    ) -> dict[str, Any]:
        """
        Get G2 reviews for a product.
        
        Args:
            product_slug: G2 product slug (e.g., "hubspot-marketing")
            max_pages: Number of review pages to scrape
        
        Returns:
            {
                "product": "...",
                "url": "...",
                "rating": float,
                "review_count": int,
                "reviews": [
                    {
                        "title": "...",
                        "rating": int,
                        "pros": "...",
                        "cons": "...",
                        "reviewer": "...",
                        "date": "..."
                    }
                ],
                "summary": {
                    "avg_rating": float,
                    "common_pros": [...],
                    "common_cons": [...]
                }
            }
        """
        url = self.get_g2_product_url(product_slug)
        
        # Scrape the reviews page
        result = self.firecrawl.scrape(url, formats=["markdown", "html"])
        
        if not result.get("success"):
            return {"error": f"Failed to scrape {url}", "raw": result}
        
        content = result.get("data", {}).get("markdown", "")
        metadata = result.get("data", {}).get("metadata", {})
        
        # Parse reviews from content
        reviews = self._parse_g2_reviews(content)
        
        # Extract rating from metadata or content
        rating = self._extract_g2_rating(content)
        
        return {
            "product": product_slug,
            "url": url,
            "title": metadata.get("title", ""),
            "description": metadata.get("description", ""),
            "rating": rating,
            "reviews": reviews,
            "raw_content_length": len(content)
        }
    
    def get_g2_product_info(self, product_slug: str) -> dict[str, Any]:
        """
        Get G2 product overview (not reviews).
        
        Args:
            product_slug: G2 product slug
        
        Returns:
            Product info including features, pricing, etc.
        """
        url = f"https://www.g2.com/products/{product_slug}"
        
        result = self.firecrawl.scrape(url, formats=["markdown"])
        
        if not result.get("success"):
            return {"error": f"Failed to scrape {url}"}
        
        content = result.get("data", {}).get("markdown", "")
        metadata = result.get("data", {}).get("metadata", {})
        
        return {
            "product": product_slug,
            "url": url,
            "title": metadata.get("title", ""),
            "description": metadata.get("description", ""),
            "content": content[:5000],  # First 5000 chars
            "raw_content_length": len(content)
        }
    
    def get_g2_category(self, category_slug: str) -> dict[str, Any]:
        """
        Get G2 category page with product listings.
        
        Args:
            category_slug: G2 category slug (e.g., "marketing-automation")
        
        Returns:
            Category info with top products
        """
        url = f"https://www.g2.com/categories/{category_slug}"
        
        result = self.firecrawl.scrape(url, formats=["markdown"])
        
        if not result.get("success"):
            return {"error": f"Failed to scrape {url}"}
        
        content = result.get("data", {}).get("markdown", "")
        
        return {
            "category": category_slug,
            "url": url,
            "content": content[:10000],
            "raw_content_length": len(content)
        }
    
    def compare_on_g2(
        self,
        product1_slug: str,
        product2_slug: str
    ) -> dict[str, Any]:
        """
        Get G2 comparison between two products.
        
        Args:
            product1_slug: First product slug
            product2_slug: Second product slug
        
        Returns:
            Comparison data
        """
        url = f"https://www.g2.com/compare/{product1_slug}-vs-{product2_slug}"
        
        result = self.firecrawl.scrape(url, formats=["markdown"])
        
        if not result.get("success"):
            return {"error": f"Failed to scrape {url}"}
        
        content = result.get("data", {}).get("markdown", "")
        
        return {
            "product1": product1_slug,
            "product2": product2_slug,
            "url": url,
            "content": content[:10000],
            "raw_content_length": len(content)
        }
    
    def get_g2_alternatives(self, product_slug: str) -> dict[str, Any]:
        """
        Get alternatives to a product on G2.
        
        Args:
            product_slug: G2 product slug
        
        Returns:
            Alternatives page content
        """
        url = f"https://www.g2.com/products/{product_slug}/competitors/alternatives"
        
        result = self.firecrawl.scrape(url, formats=["markdown"])
        
        if not result.get("success"):
            return {"error": f"Failed to scrape {url}"}
        
        content = result.get("data", {}).get("markdown", "")
        
        return {
            "product": product_slug,
            "url": url,
            "content": content[:10000],
            "raw_content_length": len(content)
        }
    
    def _parse_g2_reviews(self, content: str) -> list[dict[str, Any]]:
        """Parse review data from G2 markdown content."""
        reviews = []
        
        # G2 reviews have specific patterns - extract what we can
        # This is a best-effort extraction as the format may vary
        
        # Look for review blocks
        review_pattern = r'###?\s*["\']?(.+?)["\']?\s*\n(.*?)(?=###|\Z)'
        matches = re.findall(review_pattern, content, re.DOTALL)
        
        for title, body in matches[:20]:  # Limit to 20 reviews
            review = {
                "title": title.strip()[:200],
                "content": body.strip()[:1000]
            }
            
            # Try to extract pros/cons
            pros_match = re.search(r'(?:what do you like|pros?)[:\s]*(.+?)(?:what do you dislike|cons?|$)', body, re.IGNORECASE | re.DOTALL)
            cons_match = re.search(r'(?:what do you dislike|cons?)[:\s]*(.+?)(?:what|$)', body, re.IGNORECASE | re.DOTALL)
            
            if pros_match:
                review["pros"] = pros_match.group(1).strip()[:500]
            if cons_match:
                review["cons"] = cons_match.group(1).strip()[:500]
            
            if len(review.get("content", "")) > 50:
                reviews.append(review)
        
        return reviews
    
    def _extract_g2_rating(self, content: str) -> Optional[float]:
        """Extract overall rating from G2 content."""
        # Look for rating patterns
        patterns = [
            r'(\d+\.?\d*)\s*(?:out of 5|/5|stars)',
            r'rating[:\s]*(\d+\.?\d*)',
            r'(\d+\.?\d*)\s*★'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                try:
                    rating = float(match.group(1))
                    if 0 <= rating <= 5:
                        return rating
                except ValueError:
                    continue
        
        return None
    
    # ========================================================================
    # Capterra Scraping
    # ========================================================================
    
    def get_capterra_reviews(self, product_slug: str) -> dict[str, Any]:
        """
        Get Capterra reviews for a product.
        
        Args:
            product_slug: Capterra product slug
        
        Returns:
            Review data
        """
        url = f"https://www.capterra.com/p/{product_slug}/reviews/"
        
        result = self.firecrawl.scrape(url, formats=["markdown"])
        
        if not result.get("success"):
            # Try alternative URL format
            url = f"https://www.capterra.com/software/{product_slug}/reviews/"
            result = self.firecrawl.scrape(url, formats=["markdown"])
        
        if not result.get("success"):
            return {"error": f"Failed to scrape Capterra for {product_slug}"}
        
        content = result.get("data", {}).get("markdown", "")
        metadata = result.get("data", {}).get("metadata", {})
        
        return {
            "product": product_slug,
            "url": url,
            "title": metadata.get("title", ""),
            "description": metadata.get("description", ""),
            "content": content[:10000],
            "rating": self._extract_capterra_rating(content),
            "raw_content_length": len(content)
        }
    
    def search_capterra(self, query: str) -> dict[str, Any]:
        """
        Search Capterra for products.
        
        Args:
            query: Search query
        
        Returns:
            Search results
        """
        url = f"https://www.capterra.com/search/?search={query.replace(' ', '+')}"
        
        result = self.firecrawl.scrape(url, formats=["markdown"])
        
        if not result.get("success"):
            return {"error": f"Failed to search Capterra for {query}"}
        
        content = result.get("data", {}).get("markdown", "")
        
        return {
            "query": query,
            "url": url,
            "content": content[:10000],
            "raw_content_length": len(content)
        }
    
    def _extract_capterra_rating(self, content: str) -> Optional[float]:
        """Extract rating from Capterra content."""
        # Similar to G2 extraction
        patterns = [
            r'(\d+\.?\d*)\s*(?:out of 5|/5)',
            r'overall[:\s]*(\d+\.?\d*)',
            r'(\d+\.?\d*)\s*/\s*5'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                try:
                    rating = float(match.group(1))
                    if 0 <= rating <= 5:
                        return rating
                except ValueError:
                    continue
        
        return None
    
    # ========================================================================
    # TrustRadius Scraping
    # ========================================================================
    
    def get_trustradius_reviews(self, product_slug: str) -> dict[str, Any]:
        """
        Get TrustRadius reviews for a product.
        
        Args:
            product_slug: TrustRadius product slug
        
        Returns:
            Review data
        """
        url = f"https://www.trustradius.com/products/{product_slug}/reviews"
        
        result = self.firecrawl.scrape(url, formats=["markdown"])
        
        if not result.get("success"):
            return {"error": f"Failed to scrape TrustRadius for {product_slug}"}
        
        content = result.get("data", {}).get("markdown", "")
        metadata = result.get("data", {}).get("metadata", {})
        
        return {
            "product": product_slug,
            "url": url,
            "title": metadata.get("title", ""),
            "description": metadata.get("description", ""),
            "content": content[:10000],
            "raw_content_length": len(content)
        }


# ============================================================================
# CLI Interface
# ============================================================================

def main():
    """CLI entry point for review scraping tools."""
    import argparse
    import json
    
    parser = argparse.ArgumentParser(description="Scrape product reviews from G2, Capterra")
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    # G2 commands
    g2_parser = subparsers.add_parser("g2", help="G2 reviews and data")
    g2_parser.add_argument("product", help="G2 product slug")
    g2_parser.add_argument("--info", action="store_true", help="Get product info (not reviews)")
    g2_parser.add_argument("--alternatives", action="store_true", help="Get alternatives")
    g2_parser.add_argument("--compare", help="Compare with another product slug")
    
    # Capterra commands
    capterra_parser = subparsers.add_parser("capterra", help="Capterra reviews")
    capterra_parser.add_argument("product", help="Capterra product slug")
    capterra_parser.add_argument("--search", action="store_true", help="Search instead of direct lookup")
    
    # Category command
    category_parser = subparsers.add_parser("category", help="G2 category")
    category_parser.add_argument("slug", help="G2 category slug")
    
    args = parser.parse_args()
    scraper = ReviewScraper()
    
    try:
        if args.command == "g2":
            if args.compare:
                result = scraper.compare_on_g2(args.product, args.compare)
            elif args.alternatives:
                result = scraper.get_g2_alternatives(args.product)
            elif args.info:
                result = scraper.get_g2_product_info(args.product)
            else:
                result = scraper.get_g2_reviews(args.product)
            
            print(json.dumps(result, indent=2))
        
        elif args.command == "capterra":
            if args.search:
                result = scraper.search_capterra(args.product)
            else:
                result = scraper.get_capterra_reviews(args.product)
            
            print(json.dumps(result, indent=2))
        
        elif args.command == "category":
            result = scraper.get_g2_category(args.slug)
            print(json.dumps(result, indent=2))
    
    finally:
        scraper.close()


if __name__ == "__main__":
    main()
