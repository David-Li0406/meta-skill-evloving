#!/usr/bin/env python3
"""
Unified Ads CLI
===============
Cross-platform ads management interface.

Provides a unified view across Google Ads, LinkedIn Ads, and Meta Ads.

Usage:
    python ads_unified.py summary           # Summary across all platforms
    python ads_unified.py compare --days 30 # Compare platform performance
    python ads_unified.py status            # Check credentials status
"""

import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional, Dict, List, Any

# Add parent directory for imports
sys.path.insert(0, str(Path(__file__).parent))

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Import platform-specific tools
try:
    from google_ads import GoogleAdsAPI
    GOOGLE_ADS_AVAILABLE = True
except ImportError:
    GOOGLE_ADS_AVAILABLE = False
    GoogleAdsAPI = None

try:
    from linkedin_ads import LinkedInAdsAPI
    LINKEDIN_ADS_AVAILABLE = True
except ImportError:
    LINKEDIN_ADS_AVAILABLE = False
    LinkedInAdsAPI = None


class UnifiedAdsManager:
    """
    Cross-platform ads management.
    
    Aggregates data from Google Ads, LinkedIn Ads, and Meta Ads
    for unified reporting and comparison.
    """
    
    def __init__(self):
        self.google = None
        self.linkedin = None
        self.meta = None
        
        self._init_clients()
    
    def _init_clients(self):
        """Initialize available platform clients."""
        print("Initializing ads platform connections...\n")
        
        # Google Ads
        if GOOGLE_ADS_AVAILABLE:
            try:
                self.google = GoogleAdsAPI()
            except Exception as e:
                print(f"⚠️  Google Ads: {e}")
        else:
            print("⚠️  Google Ads: Module not available")
        
        # LinkedIn Ads
        if LINKEDIN_ADS_AVAILABLE:
            try:
                self.linkedin = LinkedInAdsAPI()
            except Exception as e:
                print(f"⚠️  LinkedIn Ads: {e}")
        else:
            print("⚠️  LinkedIn Ads: Module not available")
        
        # Meta Ads - placeholder for future
        # if META_ADS_AVAILABLE:
        #     self.meta = MetaAdsAPI()
        
        print()
    
    def check_status(self) -> Dict:
        """Check credential status for all platforms."""
        status = {
            "google_ads": {
                "available": GOOGLE_ADS_AVAILABLE,
                "configured": self.google.has_credentials() if self.google else False,
                "required_env_vars": [
                    "GOOGLE_ADS_DEVELOPER_TOKEN",
                    "GOOGLE_ADS_CLIENT_ID",
                    "GOOGLE_ADS_CLIENT_SECRET",
                    "GOOGLE_ADS_REFRESH_TOKEN"
                ]
            },
            "linkedin_ads": {
                "available": LINKEDIN_ADS_AVAILABLE,
                "configured": self.linkedin.has_credentials() if self.linkedin else False,
                "required_env_vars": [
                    "LINKEDIN_ACCESS_TOKEN",
                    "LINKEDIN_AD_ACCOUNT_ID"
                ]
            },
            "meta_ads": {
                "available": False,
                "configured": False,
                "required_env_vars": [
                    "META_APP_ID",
                    "META_APP_SECRET",
                    "META_ACCESS_TOKEN"
                ],
                "note": "Coming soon"
            }
        }
        
        # Check which env vars are set
        for platform, info in status.items():
            info["env_vars_set"] = []
            info["env_vars_missing"] = []
            for var in info["required_env_vars"]:
                if os.getenv(var):
                    info["env_vars_set"].append(var)
                else:
                    info["env_vars_missing"].append(var)
        
        return status
    
    def get_summary(self) -> Dict:
        """Get summary across all platforms."""
        summary = {
            "generated_at": datetime.now().isoformat(),
            "platforms": {}
        }
        
        # Google Ads
        if self.google and self.google.has_credentials():
            try:
                accounts = self.google.list_accounts()
                if isinstance(accounts, list):
                    summary["platforms"]["google_ads"] = {
                        "status": "connected",
                        "accounts": len(accounts),
                        "account_ids": [a.get("customer_id") for a in accounts[:5]]
                    }
                else:
                    summary["platforms"]["google_ads"] = {
                        "status": "error",
                        "error": accounts.get("error", "Unknown error")
                    }
            except Exception as e:
                summary["platforms"]["google_ads"] = {
                    "status": "error",
                    "error": str(e)
                }
        else:
            summary["platforms"]["google_ads"] = {"status": "not_configured"}
        
        # LinkedIn Ads
        if self.linkedin and self.linkedin.has_credentials():
            try:
                accounts = self.linkedin.list_ad_accounts()
                if isinstance(accounts, list):
                    summary["platforms"]["linkedin_ads"] = {
                        "status": "connected",
                        "accounts": len(accounts),
                        "account_ids": [a.get("id") for a in accounts[:5]]
                    }
                else:
                    summary["platforms"]["linkedin_ads"] = {
                        "status": "error",
                        "error": accounts.get("error", "Unknown error")
                    }
            except Exception as e:
                summary["platforms"]["linkedin_ads"] = {
                    "status": "error",
                    "error": str(e)
                }
        else:
            summary["platforms"]["linkedin_ads"] = {"status": "not_configured"}
        
        # Meta Ads
        summary["platforms"]["meta_ads"] = {"status": "coming_soon"}
        
        return summary
    
    def compare_performance(
        self,
        days: int = 30,
        google_customer_id: Optional[str] = None,
        linkedin_account_id: Optional[str] = None
    ) -> Dict:
        """Compare performance across platforms."""
        
        comparison = {
            "period": f"Last {days} days",
            "generated_at": datetime.now().isoformat(),
            "platforms": {}
        }
        
        # Google Ads
        if self.google and self.google.has_credentials() and google_customer_id:
            try:
                perf = self.google.get_campaign_performance(
                    google_customer_id, 
                    days=days
                )
                
                if isinstance(perf, list):
                    # Aggregate metrics
                    totals = {
                        "impressions": 0,
                        "clicks": 0,
                        "cost": 0,
                        "conversions": 0
                    }
                    
                    for campaign in perf:
                        metrics = campaign.get("metrics", {})
                        totals["impressions"] += metrics.get("impressions", 0)
                        totals["clicks"] += metrics.get("clicks", 0)
                        totals["cost"] += metrics.get("cost", 0)
                        totals["conversions"] += metrics.get("conversions", 0)
                    
                    totals["ctr"] = (totals["clicks"] / totals["impressions"] * 100) if totals["impressions"] > 0 else 0
                    totals["cpc"] = totals["cost"] / totals["clicks"] if totals["clicks"] > 0 else 0
                    totals["cpa"] = totals["cost"] / totals["conversions"] if totals["conversions"] > 0 else 0
                    totals["campaigns_count"] = len(perf)
                    
                    comparison["platforms"]["google_ads"] = totals
                else:
                    comparison["platforms"]["google_ads"] = {"error": perf.get("error")}
                    
            except Exception as e:
                comparison["platforms"]["google_ads"] = {"error": str(e)}
        else:
            comparison["platforms"]["google_ads"] = {"status": "not_configured_or_no_account_id"}
        
        # LinkedIn Ads
        # Note: Would need to aggregate across campaigns
        linkedin_account_id = linkedin_account_id or os.getenv("LINKEDIN_AD_ACCOUNT_ID")
        if self.linkedin and self.linkedin.has_credentials() and linkedin_account_id:
            try:
                campaigns = self.linkedin.list_campaigns(linkedin_account_id)
                
                if isinstance(campaigns, list) and campaigns:
                    # Get analytics for first campaign as sample
                    # Real implementation would aggregate all
                    totals = {
                        "campaigns_count": len(campaigns),
                        "note": "Per-campaign aggregation requires campaign IDs"
                    }
                    comparison["platforms"]["linkedin_ads"] = totals
                else:
                    comparison["platforms"]["linkedin_ads"] = {"campaigns": 0}
                    
            except Exception as e:
                comparison["platforms"]["linkedin_ads"] = {"error": str(e)}
        else:
            comparison["platforms"]["linkedin_ads"] = {"status": "not_configured_or_no_account_id"}
        
        # Meta Ads
        comparison["platforms"]["meta_ads"] = {"status": "coming_soon"}
        
        return comparison
    
    def list_all_campaigns(
        self,
        google_customer_id: Optional[str] = None,
        linkedin_account_id: Optional[str] = None
    ) -> Dict:
        """List all campaigns across platforms."""
        
        all_campaigns = {
            "generated_at": datetime.now().isoformat(),
            "platforms": {}
        }
        
        # Google Ads
        if self.google and self.google.has_credentials() and google_customer_id:
            try:
                campaigns = self.google.list_campaigns(google_customer_id)
                if isinstance(campaigns, list):
                    all_campaigns["platforms"]["google_ads"] = {
                        "count": len(campaigns),
                        "campaigns": [
                            {
                                "id": c.get("campaign", {}).get("id"),
                                "name": c.get("campaign", {}).get("name"),
                                "status": c.get("campaign", {}).get("status"),
                                "type": c.get("campaign", {}).get("advertising_channel_type")
                            }
                            for c in campaigns
                        ]
                    }
                else:
                    all_campaigns["platforms"]["google_ads"] = campaigns
            except Exception as e:
                all_campaigns["platforms"]["google_ads"] = {"error": str(e)}
        else:
            all_campaigns["platforms"]["google_ads"] = {"status": "not_configured"}
        
        # LinkedIn Ads
        linkedin_account_id = linkedin_account_id or os.getenv("LINKEDIN_AD_ACCOUNT_ID")
        if self.linkedin and self.linkedin.has_credentials() and linkedin_account_id:
            try:
                campaigns = self.linkedin.list_campaigns(linkedin_account_id)
                if isinstance(campaigns, list):
                    all_campaigns["platforms"]["linkedin_ads"] = {
                        "count": len(campaigns),
                        "campaigns": campaigns
                    }
                else:
                    all_campaigns["platforms"]["linkedin_ads"] = campaigns
            except Exception as e:
                all_campaigns["platforms"]["linkedin_ads"] = {"error": str(e)}
        else:
            all_campaigns["platforms"]["linkedin_ads"] = {"status": "not_configured"}
        
        # Meta Ads
        all_campaigns["platforms"]["meta_ads"] = {"status": "coming_soon"}
        
        return all_campaigns


def format_status(status: Dict) -> str:
    """Format credential status for display."""
    lines = ["=" * 60, "Ads Platform Credential Status", "=" * 60, ""]
    
    for platform, info in status.items():
        icon = "✅" if info["configured"] else "❌"
        lines.append(f"{icon} {platform.upper().replace('_', ' ')}")
        lines.append(f"   Available: {info['available']}")
        lines.append(f"   Configured: {info['configured']}")
        
        if info.get("note"):
            lines.append(f"   Note: {info['note']}")
        
        if info.get("env_vars_missing"):
            lines.append(f"   Missing: {', '.join(info['env_vars_missing'])}")
        
        lines.append("")
    
    return "\n".join(lines)


def format_summary(summary: Dict) -> str:
    """Format summary for display."""
    lines = ["=" * 60, "Ads Platform Summary", "=" * 60, ""]
    lines.append(f"Generated: {summary['generated_at']}")
    lines.append("")
    
    for platform, info in summary["platforms"].items():
        status = info.get("status", "unknown")
        icon = "✅" if status == "connected" else "⚠️"
        lines.append(f"{icon} {platform.upper().replace('_', ' ')}: {status}")
        
        if status == "connected":
            lines.append(f"   Accounts: {info.get('accounts', 'N/A')}")
            if info.get("account_ids"):
                lines.append(f"   IDs: {', '.join(map(str, info['account_ids']))}")
        elif info.get("error"):
            lines.append(f"   Error: {info['error']}")
        
        lines.append("")
    
    return "\n".join(lines)


def format_comparison(comparison: Dict) -> str:
    """Format comparison for display."""
    lines = ["=" * 60, f"Cross-Platform Performance Comparison", "=" * 60, ""]
    lines.append(f"Period: {comparison['period']}")
    lines.append(f"Generated: {comparison['generated_at']}")
    lines.append("")
    
    # Header
    lines.append(f"{'Metric':<20} | {'Google Ads':>15} | {'LinkedIn Ads':>15} | {'Meta Ads':>15}")
    lines.append("-" * 75)
    
    # Get metrics from each platform
    google = comparison["platforms"].get("google_ads", {})
    linkedin = comparison["platforms"].get("linkedin_ads", {})
    meta = comparison["platforms"].get("meta_ads", {})
    
    metrics = ["impressions", "clicks", "cost", "ctr", "cpc", "conversions", "cpa"]
    
    for metric in metrics:
        g_val = google.get(metric, "-")
        l_val = linkedin.get(metric, "-")
        m_val = meta.get(metric, "-")
        
        # Format values
        if isinstance(g_val, float):
            g_val = f"${g_val:.2f}" if metric in ["cost", "cpc", "cpa"] else f"{g_val:.2f}"
        if isinstance(l_val, float):
            l_val = f"${l_val:.2f}" if metric in ["cost", "cpc", "cpa"] else f"{l_val:.2f}"
        
        lines.append(f"{metric:<20} | {str(g_val):>15} | {str(l_val):>15} | {str(m_val):>15}")
    
    lines.append("")
    
    # Notes
    if google.get("error"):
        lines.append(f"⚠️  Google Ads: {google['error']}")
    if linkedin.get("note"):
        lines.append(f"ℹ️  LinkedIn Ads: {linkedin['note']}")
    if meta.get("status") == "coming_soon":
        lines.append("ℹ️  Meta Ads: Coming soon")
    
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Unified Ads CLI - Cross-platform ads management",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Check credential status
  python ads_unified.py status

  # Get summary across platforms  
  python ads_unified.py summary

  # Compare platform performance
  python ads_unified.py compare --days 30 --google-customer-id 1234567890

  # List all campaigns
  python ads_unified.py campaigns --google-customer-id 1234567890
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Status command
    status_parser = subparsers.add_parser("status", help="Check credential status")
    
    # Summary command
    summary_parser = subparsers.add_parser("summary", help="Get platform summary")
    
    # Compare command
    compare_parser = subparsers.add_parser("compare", help="Compare platform performance")
    compare_parser.add_argument("--days", type=int, default=30, help="Number of days")
    compare_parser.add_argument("--google-customer-id", help="Google Ads customer ID")
    compare_parser.add_argument("--linkedin-account-id", help="LinkedIn ad account ID")
    
    # Campaigns command
    campaigns_parser = subparsers.add_parser("campaigns", help="List all campaigns")
    campaigns_parser.add_argument("--google-customer-id", help="Google Ads customer ID")
    campaigns_parser.add_argument("--linkedin-account-id", help="LinkedIn ad account ID")
    
    # Global options
    parser.add_argument("--format", choices=["text", "json"], default="text", help="Output format")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Initialize manager
    manager = UnifiedAdsManager()
    
    # Execute command
    if args.command == "status":
        result = manager.check_status()
        if args.format == "json":
            print(json.dumps(result, indent=2))
        else:
            print(format_status(result))
    
    elif args.command == "summary":
        result = manager.get_summary()
        if args.format == "json":
            print(json.dumps(result, indent=2))
        else:
            print(format_summary(result))
    
    elif args.command == "compare":
        result = manager.compare_performance(
            days=args.days,
            google_customer_id=args.google_customer_id,
            linkedin_account_id=args.linkedin_account_id
        )
        if args.format == "json":
            print(json.dumps(result, indent=2))
        else:
            print(format_comparison(result))
    
    elif args.command == "campaigns":
        result = manager.list_all_campaigns(
            google_customer_id=args.google_customer_id,
            linkedin_account_id=args.linkedin_account_id
        )
        print(json.dumps(result, indent=2))
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
