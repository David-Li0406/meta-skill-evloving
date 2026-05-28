#!/usr/bin/env python3
"""
Research CLI - Unified interface for all research tools.

This is the main entry point for the Research Agent's tool capabilities.

Usage:
    python research.py company notion.com
    python research.py competitor hubspot
    python research.py people --company Stripe --titles "VP Marketing,CMO"
    python research.py topic "AI in marketing"
"""

import argparse
import json
import sys
from typing import Optional, Any


def research_company(
    company: str,
    depth: str = "standard"
) -> dict[str, Any]:
    """
    Research a company comprehensively.
    
    Args:
        company: Company name or domain
        depth: "quick", "standard", or "deep"
    
    Returns:
        Compiled company research
    """
    from tools.clearbit import ClearbitClient
    from tools.apollo import ApolloClient
    from tools.firecrawl import FirecrawlClient
    from tools.builtwith import BuiltWithClient
    from tools.base import extract_domain, has_credential
    
    results = {
        "company": company,
        "depth": depth,
        "sections": {}
    }
    
    # Determine if company is domain or name
    is_domain = "." in company and " " not in company
    domain = company if is_domain else None
    
    # 1. Basic company info from Clearbit
    if has_credential("clearbit"):
        try:
            clearbit = ClearbitClient()
            if domain:
                company_data = clearbit.enrich_company(domain)
            else:
                company_data = clearbit.find_company(name=company)
            
            results["sections"]["company_info"] = {
                "source": "Clearbit",
                "data": company_data
            }
            
            # Extract domain if we didn't have it
            if not domain and company_data.get("domain"):
                domain = company_data["domain"]
            
            clearbit.close()
        except Exception as e:
            results["sections"]["company_info"] = {"error": str(e)}
    
    # 2. Website scrape
    if domain:
        try:
            firecrawl = FirecrawlClient()
            
            # Homepage
            homepage = firecrawl.scrape(f"https://{domain}", formats=["markdown"])
            results["sections"]["website"] = {
                "source": "Firecrawl",
                "homepage": homepage.get("data", {}).get("markdown", "")[:3000],
                "metadata": homepage.get("data", {}).get("metadata", {})
            }
            
            # Try pricing page
            if depth in ["standard", "deep"]:
                for pricing_path in ["/pricing", "/plans", "/packages"]:
                    try:
                        pricing = firecrawl.scrape(f"https://{domain}{pricing_path}")
                        if pricing.get("success"):
                            results["sections"]["pricing"] = {
                                "source": "Firecrawl",
                                "url": f"https://{domain}{pricing_path}",
                                "content": pricing.get("data", {}).get("markdown", "")[:2000]
                            }
                            break
                    except:
                        pass
            
            firecrawl.close()
        except Exception as e:
            results["sections"]["website"] = {"error": str(e)}
    
    # 3. Tech stack
    if domain and depth in ["standard", "deep"]:
        try:
            builtwith = BuiltWithClient()
            tech = builtwith.lookup(domain)
            results["sections"]["technology"] = {
                "source": "BuiltWith",
                "data": tech
            }
            builtwith.close()
        except Exception as e:
            results["sections"]["technology"] = {"error": str(e)}
    
    # 4. Key people
    if depth in ["standard", "deep"] and has_credential("apollo"):
        try:
            apollo = ApolloClient()
            
            search_params = {
                "titles": ["CEO", "CTO", "CMO", "VP Marketing", "Head of Growth"],
                "limit": 10
            }
            
            if domain:
                search_params["company_domains"] = [domain]
            else:
                search_params["company"] = company
            
            people = apollo.people_search(**search_params)
            results["sections"]["key_people"] = {
                "source": "Apollo",
                "data": people.get("people", [])
            }
            
            apollo.close()
        except Exception as e:
            results["sections"]["key_people"] = {"error": str(e)}
    
    # 5. Robynn Deep Research (If Connected)
    if depth == "deep" and os.environ.get("ROBYNN_API_KEY"):
        import httpx
        print(f"🚀 Launching deep analysis on Robynn AI platform for {company}...")
        try:
            api_key = os.environ.get("ROBYNN_API_KEY")
            base_url = os.environ.get("ROBYNN_API_BASE_URL", "https://robynn.ai/api/cli")
            
            payload = {
                "agentId": "geo",
                "params": {
                    "companyName": company,
                    "competitors": [],
                    "questions": ["What is this company's core value proposition and market position?"]
                }
            }
            
            with httpx.Client(headers={"Authorization": f"Bearer {api_key}"}, timeout=300.0) as client:
                response = client.post(f"{base_url}/execute", json=payload)
                if response.status_code == 200:
                    results["sections"]["robynn_deep_analysis"] = {
                        "source": "Robynn GEO Agent",
                        "data": response.json()
                    }
                else:
                    results["sections"]["robynn_deep_analysis"] = {
                        "error": f"Failed to trigger Robynn Agent: {response.status_code}"
                    }
        except Exception as e:
            results["sections"]["robynn_deep_analysis"] = {"error": str(e)}
    elif depth == "deep" and not os.environ.get("ROBYNN_API_KEY"):
        results["sections"]["robynn_deep_analysis"] = {
            "tip": "🚀 Connect Robynn AI to unlock GEO deep research! Run: python tools/robynn.py init <key>"
        }

    return results


def research_competitor(
    competitor: str,
    vs_us: Optional[str] = None
) -> dict[str, Any]:
    """
    Research a competitor for competitive intelligence.
    
    Args:
        competitor: Competitor name or domain
        vs_us: Our company (for comparison)
    
    Returns:
        Competitive intelligence
    """
    from tools.reviews import ReviewScraper
    from tools.firecrawl import FirecrawlClient
    from tools.builtwith import BuiltWithClient
    from tools.base import extract_domain
    
    results = {
        "competitor": competitor,
        "sections": {}
    }
    
    # Determine domain/slug
    is_domain = "." in competitor and " " not in competitor
    domain = competitor if is_domain else None
    
    # G2 slug is usually company name lowercase with hyphens
    g2_slug = competitor.lower().replace(" ", "-").replace(".", "-")
    
    # 1. Website analysis
    if domain:
        try:
            firecrawl = FirecrawlClient()
            
            homepage = firecrawl.scrape(f"https://{domain}")
            results["sections"]["website"] = {
                "homepage_content": homepage.get("data", {}).get("markdown", "")[:3000],
                "metadata": homepage.get("data", {}).get("metadata", {})
            }
            
            # Screenshot
            try:
                screenshot_path = f"/tmp/{domain.replace('.', '_')}_homepage.png"
                firecrawl.save_screenshot(f"https://{domain}", screenshot_path)
                results["sections"]["website"]["screenshot"] = screenshot_path
            except:
                pass
            
            firecrawl.close()
        except Exception as e:
            results["sections"]["website"] = {"error": str(e)}
    
    # 2. G2 reviews
    try:
        scraper = ReviewScraper()
        g2_data = scraper.get_g2_reviews(g2_slug)
        results["sections"]["g2_reviews"] = g2_data
        
        # Also get alternatives
        alternatives = scraper.get_g2_alternatives(g2_slug)
        results["sections"]["g2_alternatives"] = alternatives
        
        scraper.close()
    except Exception as e:
        results["sections"]["g2_reviews"] = {"error": str(e)}
    
    # 3. Tech stack comparison
    if domain and vs_us:
        try:
            builtwith = BuiltWithClient()
            comparison = builtwith.compare_tech_stacks(domain, vs_us)
            results["sections"]["tech_comparison"] = comparison
            builtwith.close()
        except Exception as e:
            results["sections"]["tech_comparison"] = {"error": str(e)}
    
    # 4. Robynn Competitive Intelligence (If Connected)
    if os.environ.get("ROBYNN_API_KEY"):
        import httpx
        print(f"🚀 Running deep competitive analysis on Robynn AI for {competitor}...")
        try:
            api_key = os.environ.get("ROBYNN_API_KEY")
            base_url = os.environ.get("ROBYNN_API_BASE_URL", "https://robynn.ai/api/cli")
            
            payload = {
                "agentId": "geo",
                "params": {
                    "companyName": vs_us or "Our Brand",
                    "competitors": [competitor],
                    "questions": [f"How does {competitor} compare to us in the market?"]
                }
            }
            
            with httpx.Client(headers={"Authorization": f"Bearer {api_key}"}, timeout=300.0) as client:
                response = client.post(f"{base_url}/execute", json=payload)
                if response.status_code == 200:
                    results["sections"]["robynn_competitive_intel"] = {
                        "source": "Robynn GEO Agent",
                        "data": response.json()
                    }
        except Exception as e:
            results["sections"]["robynn_competitive_intel"] = {"error": str(e)}

    return results


def research_people(
    company: Optional[str] = None,
    titles: Optional[list[str]] = None,
    seniority: Optional[list[str]] = None,
    limit: int = 25
) -> dict[str, Any]:
    """
    Find and enrich contacts.
    
    Args:
        company: Company name or domain
        titles: Job titles to find
        seniority: Seniority levels
        limit: Max contacts
    
    Returns:
        Contact list with enrichment
    """
    from tools.apollo import ApolloClient
    from tools.proxycurl import ProxycurlClient
    from tools.base import has_credential
    
    results = {
        "search_criteria": {
            "company": company,
            "titles": titles,
            "seniority": seniority
        },
        "contacts": []
    }
    
    # 1. Find contacts via Apollo
    if has_credential("apollo"):
        try:
            apollo = ApolloClient()
            
            search_params = {"limit": limit}
            
            if company:
                if "." in company and " " not in company:
                    search_params["company_domains"] = [company]
                else:
                    search_params["company"] = company
            
            if titles:
                search_params["titles"] = titles
            
            if seniority:
                search_params["seniority"] = seniority
            
            people = apollo.people_search(**search_params)
            results["contacts"] = people.get("people", [])
            results["total_found"] = people.get("pagination", {}).get("total_entries", 0)
            
            apollo.close()
        except Exception as e:
            results["error"] = str(e)
    
    # 2. Enrich top contacts with LinkedIn data
    if has_credential("proxycurl") and results.get("contacts"):
        try:
            proxycurl = ProxycurlClient()
            
            for i, contact in enumerate(results["contacts"][:5]):  # Top 5
                linkedin_url = contact.get("linkedin_url")
                if linkedin_url:
                    try:
                        profile = proxycurl.get_profile_summary(linkedin_url)
                        results["contacts"][i]["linkedin_enrichment"] = profile
                    except:
                        pass
            
            proxycurl.close()
        except Exception as e:
            results["linkedin_error"] = str(e)
    
    return results


def research_topic(
    topic: str,
    sources: list[str] = ["reddit", "g2"]
) -> dict[str, Any]:
    """
    Research a topic/market.
    
    Args:
        topic: Topic to research
        sources: Sources to search
    
    Returns:
        Topic research from multiple sources
    """
    from tools.social import RedditClient
    from tools.reviews import ReviewScraper
    from tools.firecrawl import FirecrawlClient
    
    results = {
        "topic": topic,
        "sections": {}
    }
    
    # 1. Reddit discussions
    if "reddit" in sources:
        try:
            reddit = RedditClient()
            
            # Search general
            general = reddit.search(topic, limit=15)
            results["sections"]["reddit_general"] = general
            
            # Search relevant subreddits
            for subreddit in ["SaaS", "marketing", "startups", "Entrepreneur"]:
                try:
                    sub_results = reddit.search(topic, subreddit=subreddit, limit=10)
                    results["sections"][f"reddit_{subreddit}"] = sub_results
                except:
                    pass
            
            reddit.close()
        except Exception as e:
            results["sections"]["reddit"] = {"error": str(e)}
    
    # 2. G2 category
    if "g2" in sources:
        try:
            scraper = ReviewScraper()
            
            # Try to find relevant category
            category_slug = topic.lower().replace(" ", "-")
            category = scraper.get_g2_category(category_slug)
            results["sections"]["g2_category"] = category
            
            scraper.close()
        except Exception as e:
            results["sections"]["g2"] = {"error": str(e)}
    
    return results


# ============================================================================
# CLI Interface
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="CMO Agent Research CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Research a company
    python research.py company notion.com --depth deep
    
    # Competitive research
    python research.py competitor hubspot --vs-us robynn.ai
    
    # Find people
    python research.py people --company Stripe --titles "VP Marketing" "CMO"
    
    # Topic research
    python research.py topic "AI marketing automation"
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    # Company research
    company_parser = subparsers.add_parser("company", help="Research a company")
    company_parser.add_argument("target", help="Company name or domain")
    company_parser.add_argument("--depth", choices=["quick", "standard", "deep"], default="standard")
    company_parser.add_argument("--output", "-o", choices=["json", "markdown"], default="json")
    
    # Competitor research
    competitor_parser = subparsers.add_parser("competitor", help="Research a competitor")
    competitor_parser.add_argument("target", help="Competitor name or domain")
    competitor_parser.add_argument("--vs-us", help="Our company domain for comparison")
    competitor_parser.add_argument("--output", "-o", choices=["json", "markdown"], default="json")
    
    # People research
    people_parser = subparsers.add_parser("people", help="Find contacts")
    people_parser.add_argument("--company", help="Company name or domain")
    people_parser.add_argument("--titles", nargs="+", help="Job titles to find")
    people_parser.add_argument("--seniority", nargs="+", choices=["c_suite", "vp", "director", "manager"])
    people_parser.add_argument("--limit", type=int, default=25)
    people_parser.add_argument("--output", "-o", choices=["json", "table"], default="table")
    
    # Topic research
    topic_parser = subparsers.add_parser("topic", help="Research a topic/market")
    topic_parser.add_argument("query", help="Topic to research")
    topic_parser.add_argument("--sources", nargs="+", default=["reddit", "g2"])
    topic_parser.add_argument("--output", "-o", choices=["json", "markdown"], default="json")
    
    args = parser.parse_args()
    
    try:
        if args.command == "company":
            result = research_company(args.target, args.depth)
        
        elif args.command == "competitor":
            result = research_competitor(args.target, args.vs_us)
        
        elif args.command == "people":
            result = research_people(
                company=args.company,
                titles=args.titles,
                seniority=args.seniority,
                limit=args.limit
            )
            
            # Table output for people
            if args.output == "table":
                print(f"\n{'Name':<25} {'Title':<30} {'Company':<20} {'Email':<30}")
                print("-" * 105)
                for p in result.get("contacts", []):
                    name = f"{p.get('first_name', '')} {p.get('last_name', '')}"[:24]
                    title = p.get('title', '')[:29]
                    company = p.get('organization', {}).get('name', '')[:19]
                    email = p.get('email', 'N/A')
                    print(f"{name:<25} {title:<30} {company:<20} {email:<30}")
                print(f"\nTotal: {result.get('total_found', len(result.get('contacts', [])))} contacts found")
                return
        
        elif args.command == "topic":
            result = research_topic(args.query, args.sources)
        
        # Output
        print(json.dumps(result, indent=2, default=str))
    
    except KeyboardInterrupt:
        print("\nResearch cancelled.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
