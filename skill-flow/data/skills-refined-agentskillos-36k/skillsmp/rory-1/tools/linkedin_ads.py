#!/usr/bin/env python3
"""
LinkedIn Ads API Tool
=====================
Wrapper for LinkedIn Marketing API operations with safety rails.

Setup:
    1. Install: pip install httpx pyyaml python-dotenv
    2. Configure .env with LinkedIn credentials
    3. Run: python linkedin_ads.py --help

Safety Features:
    - All new campaigns created in DRAFT status
    - Budget limits enforced from ads_config.yaml
    - Confirmation required for destructive actions
"""

import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional, Dict, List, Any
from urllib.parse import urlencode

# Add parent directory for imports
sys.path.insert(0, str(Path(__file__).parent))

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

try:
    import yaml
except ImportError:
    yaml = None

try:
    import httpx
    HTTPX_AVAILABLE = True
except ImportError:
    HTTPX_AVAILABLE = False
    httpx = None

# Import error handling utilities
try:
    from tools.errors import format_missing_credential_error, format_error_message
except ImportError:
    # Fallback if errors module not available
    def format_missing_credential_error(service: str) -> dict:
        return {
            "error": True,
            "service": service,
            "message": f"{service} credentials not configured",
            "recovery_steps": [f"Configure {service} API credentials in .env file"]
        }
    def format_error_message(error_dict: dict) -> str:
        return error_dict.get("message", "Unknown error")


class AdsConfig:
    """Load and manage ads configuration."""
    
    def __init__(self, config_path: Optional[str] = None):
        self.config = self._load_config(config_path)
    
    def _load_config(self, config_path: Optional[str] = None) -> dict:
        """Load configuration from YAML file."""
        if config_path is None:
            config_path = Path(__file__).parent / "ads_config.yaml"
        
        if yaml and Path(config_path).exists():
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        
        # Default config
        return {
            "safety": {
                "force_draft_mode": True,
                "require_confirmation": True
            },
            "budgets": {
                "linkedin_ads": {
                    "max_daily_budget": 0,
                    "max_total_budget": 0,
                    "max_cpc_bid": 10.00
                }
            },
            "defaults": {
                "linkedin_ads": {
                    "status": "DRAFT",
                    "objective": "WEBSITE_VISITS"
                }
            },
            "api": {
                "linkedin_ads": {
                    "api_version": "202401"
                }
            }
        }
    
    def get_max_daily_budget(self) -> float:
        return self.config.get("budgets", {}).get("linkedin_ads", {}).get("max_daily_budget", 0)
    
    def get_max_cpc_bid(self) -> float:
        return self.config.get("budgets", {}).get("linkedin_ads", {}).get("max_cpc_bid", 10.00)
    
    def get_api_version(self) -> str:
        return self.config.get("api", {}).get("linkedin_ads", {}).get("api_version", "202401")
    
    def force_draft_mode(self) -> bool:
        return self.config.get("safety", {}).get("force_draft_mode", True)
    
    def require_confirmation(self) -> bool:
        return self.config.get("safety", {}).get("require_confirmation", True)


class LinkedInAdsAPI:
    """
    LinkedIn Marketing API wrapper with safety features.
    """

    BASE_URL = "https://api.linkedin.com/rest"
    SERVICE_NAME = "linkedin_ads"

    def __init__(self, config: Optional[AdsConfig] = None):
        self.config = config or AdsConfig()
        self.access_token = os.getenv("LINKEDIN_ACCESS_TOKEN")
        self.ad_account_id = os.getenv("LINKEDIN_AD_ACCOUNT_ID")
        self.api_version = self.config.get_api_version()
        self._is_available = False
        self._availability_reason = None

        self._validate_credentials()

    def _validate_credentials(self):
        """Check if credentials are configured."""
        if not HTTPX_AVAILABLE:
            self._availability_reason = "httpx library not installed. Install with: pip install httpx"
            return

        if not self.access_token:
            self._availability_reason = "LINKEDIN_ACCESS_TOKEN not set in environment"
            return

        self._is_available = True

    @property
    def is_available(self) -> bool:
        """Check if the client has valid credentials configured."""
        return self._is_available

    def get_availability_error(self) -> Dict[str, Any]:
        """Get structured error information when credentials are missing."""
        error = format_missing_credential_error(self.SERVICE_NAME)
        if self._availability_reason:
            error["details"] = self._availability_reason
        return error

    def get_availability_message(self) -> str:
        """Get human-readable error message when credentials are missing."""
        msg = format_error_message(self.get_availability_error())
        if self._availability_reason:
            msg += f"\nDetails: {self._availability_reason}"
        return msg

    def _check_availability(self) -> Optional[Dict[str, Any]]:
        """Check if client is available, return error dict if not."""
        if not self._is_available:
            error = self.get_availability_error()
            error["data"] = None
            return error
        return None

    def has_credentials(self) -> bool:
        """Check if credentials are configured (alias for is_available)."""
        return self._is_available
    
    def _get_headers(self) -> Dict[str, str]:
        """Get headers for API requests."""
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
            "X-Restli-Protocol-Version": "2.0.0",
            "LinkedIn-Version": self.api_version
        }
    
    def _make_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict] = None,
        data: Optional[Dict] = None
    ) -> Dict:
        """Make API request to LinkedIn."""
        # Check if credentials are available
        error = self._check_availability()
        if error:
            return error
        
        url = f"{self.BASE_URL}{endpoint}"
        
        try:
            with httpx.Client(timeout=60.0) as client:
                if method == "GET":
                    response = client.get(url, headers=self._get_headers(), params=params)
                elif method == "POST":
                    response = client.post(url, headers=self._get_headers(), json=data)
                elif method == "PATCH":
                    response = client.patch(url, headers=self._get_headers(), json=data)
                elif method == "DELETE":
                    response = client.delete(url, headers=self._get_headers())
                else:
                    return {"error": f"Unsupported method: {method}"}
                
                if response.status_code == 204:
                    return {"success": True}
                
                if response.status_code >= 400:
                    return {
                        "error": f"API Error {response.status_code}",
                        "details": response.text
                    }
                
                return response.json()
                
        except httpx.RequestError as e:
            return {"error": f"Request failed: {str(e)}"}
        except json.JSONDecodeError:
            return {"error": "Invalid JSON response", "raw": response.text[:500]}
    
    # =========================================================================
    # READ OPERATIONS
    # =========================================================================
    
    def list_ad_accounts(self) -> List[Dict]:
        """List accessible LinkedIn ad accounts."""
        endpoint = "/adAccounts"
        params = {
            "q": "search",
            "search": "(status:(values:List(ACTIVE,DRAFT)))"
        }
        
        result = self._make_request("GET", endpoint, params=params)
        
        if "error" in result:
            return result
        
        accounts = []
        for element in result.get("elements", []):
            accounts.append({
                "id": element.get("id"),
                "name": element.get("name"),
                "status": element.get("status"),
                "type": element.get("type"),
                "currency": element.get("currency"),
                "reference": element.get("reference")
            })
        
        return accounts
    
    def list_campaigns(self, account_id: Optional[str] = None) -> List[Dict]:
        """List campaigns for an ad account."""
        account_id = account_id or self.ad_account_id
        
        if not account_id:
            return {"error": "No account ID specified"}
        
        endpoint = "/adCampaigns"
        params = {
            "q": "search",
            "search": f"(account:(values:List(urn:li:sponsoredAccount:{account_id})))"
        }
        
        result = self._make_request("GET", endpoint, params=params)
        
        if "error" in result:
            return result
        
        campaigns = []
        for element in result.get("elements", []):
            campaigns.append({
                "id": element.get("id"),
                "name": element.get("name"),
                "status": element.get("status"),
                "type": element.get("type"),
                "objectiveType": element.get("objectiveType"),
                "dailyBudget": element.get("dailyBudget"),
                "totalBudget": element.get("totalBudget"),
                "costType": element.get("costType"),
                "runSchedule": element.get("runSchedule")
            })
        
        return campaigns
    
    def get_campaign(self, campaign_id: str) -> Dict:
        """Get details for a specific campaign."""
        endpoint = f"/adCampaigns/{campaign_id}"
        return self._make_request("GET", endpoint)
    
    def get_campaign_analytics(
        self,
        campaign_id: str,
        days: int = 30,
        metrics: Optional[List[str]] = None
    ) -> Dict:
        """Get analytics for a campaign."""
        
        # Calculate date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        default_metrics = [
            "impressions",
            "clicks",
            "costInLocalCurrency",
            "externalWebsiteConversions",
            "shares",
            "comments",
            "reactions",
            "follows"
        ]
        metrics = metrics or default_metrics
        
        endpoint = "/adAnalytics"
        params = {
            "q": "analytics",
            "pivot": "CAMPAIGN",
            "dateRange": f"(start:(year:{start_date.year},month:{start_date.month},day:{start_date.day}),end:(year:{end_date.year},month:{end_date.month},day:{end_date.day}))",
            "campaigns": f"List(urn:li:sponsoredCampaign:{campaign_id})",
            "fields": ",".join(metrics)
        }
        
        result = self._make_request("GET", endpoint, params=params)
        
        if "error" in result:
            return result
        
        # Process and summarize results
        elements = result.get("elements", [])
        if not elements:
            return {"message": "No analytics data for the specified period"}
        
        # Aggregate metrics
        totals = {metric: 0 for metric in metrics}
        for element in elements:
            for metric in metrics:
                val = element.get(metric, 0)
                if isinstance(val, (int, float)):
                    totals[metric] += val
                elif isinstance(val, dict) and "amount" in val:
                    totals[metric] += float(val["amount"])
        
        # Calculate derived metrics
        if totals["impressions"] > 0:
            totals["ctr"] = (totals["clicks"] / totals["impressions"]) * 100
        else:
            totals["ctr"] = 0
        
        if totals["clicks"] > 0:
            totals["cpc"] = totals.get("costInLocalCurrency", 0) / totals["clicks"]
        else:
            totals["cpc"] = 0
        
        return {
            "campaign_id": campaign_id,
            "date_range": {
                "start": start_date.strftime("%Y-%m-%d"),
                "end": end_date.strftime("%Y-%m-%d")
            },
            "metrics": totals,
            "raw_elements": len(elements)
        }
    
    def get_targeting_facets(self) -> List[Dict]:
        """Get available targeting facets."""
        endpoint = "/adTargetingFacets"
        result = self._make_request("GET", endpoint)
        
        if "error" in result:
            return result
        
        facets = []
        for element in result.get("elements", []):
            facets.append({
                "urn": element.get("urn"),
                "name": element.get("name"),
                "facetType": element.get("facetType")
            })
        
        return facets
    
    def search_targeting_entities(
        self,
        facet_urn: str,
        query: str,
        limit: int = 25
    ) -> List[Dict]:
        """Search for targeting entity values."""
        endpoint = "/adTargetingEntities"
        params = {
            "q": "search",
            "facet": facet_urn,
            "query": query,
            "count": limit
        }
        
        result = self._make_request("GET", endpoint, params=params)
        
        if "error" in result:
            return result
        
        entities = []
        for element in result.get("elements", []):
            entities.append({
                "urn": element.get("urn"),
                "name": element.get("name"),
                "facetUrn": element.get("facetUrn")
            })
        
        return entities
    
    def get_audience_count(self, targeting_criteria: Dict) -> Dict:
        """Get estimated audience size for targeting criteria."""
        endpoint = "/adTargetingEstimates"
        
        data = {
            "targetingCriteria": targeting_criteria,
            "campaignType": "SPONSORED_UPDATES"
        }
        
        result = self._make_request("POST", endpoint, data=data)
        
        if "error" in result:
            return result
        
        return {
            "total_count": result.get("totalCount", 0),
            "active_count": result.get("activeCount", 0),
            "minimum_required": 300
        }
    
    # =========================================================================
    # WRITE OPERATIONS (with safety rails)
    # =========================================================================
    
    def create_campaign(
        self,
        account_id: str,
        name: str,
        objective: str = "WEBSITE_VISITS",
        daily_budget: float = 0,
        total_budget: float = 0,
        targeting_criteria: Optional[Dict] = None,
        confirm: bool = False
    ) -> Dict:
        """
        Create a new campaign in DRAFT status.
        
        ⚠️ SAFETY: Campaign is always created in DRAFT status.
        """
        
        # Safety check: force draft mode
        status = "DRAFT"  # Always DRAFT
        
        # Budget validation
        max_budget = self.config.get_max_daily_budget()
        if max_budget > 0 and daily_budget > max_budget:
            return {
                "error": f"Budget ${daily_budget} exceeds maximum allowed ${max_budget}",
                "max_budget": max_budget
            }
        
        # Confirmation for non-zero budget
        if daily_budget > 0 and self.config.require_confirmation() and not confirm:
            return {
                "requires_confirmation": True,
                "message": f"Creating campaign '{name}' with ${daily_budget}/day budget. Add --confirm to proceed.",
                "details": {
                    "name": name,
                    "objective": objective,
                    "daily_budget": daily_budget,
                    "status": status
                }
            }
        
        # Build campaign data
        campaign_data = {
            "account": f"urn:li:sponsoredAccount:{account_id}",
            "name": name,
            "status": status,  # Always DRAFT
            "type": "SPONSORED_UPDATES",
            "objectiveType": objective,
            "costType": "CPC",
            "locale": {
                "country": "US",
                "language": "en"
            }
        }
        
        # Add budget if specified
        if daily_budget > 0:
            campaign_data["dailyBudget"] = {
                "currencyCode": "USD",
                "amount": str(daily_budget)
            }
        
        if total_budget > 0:
            campaign_data["totalBudget"] = {
                "currencyCode": "USD",
                "amount": str(total_budget)
            }
        
        # Add targeting if provided
        if targeting_criteria:
            campaign_data["targetingCriteria"] = targeting_criteria
        
        endpoint = "/adCampaigns"
        result = self._make_request("POST", endpoint, data=campaign_data)
        
        if "error" in result:
            return result
        
        campaign_id = result.get("id")
        
        return {
            "success": True,
            "campaign_id": campaign_id,
            "name": name,
            "status": "DRAFT",
            "daily_budget": daily_budget,
            "message": f"✅ Campaign '{name}' created in DRAFT status. Log into LinkedIn Campaign Manager to review and activate."
        }
    
    def update_campaign_status(
        self,
        campaign_id: str,
        status: str,
        confirm: bool = False
    ) -> Dict:
        """
        Update campaign status.
        
        ⚠️ SAFETY: Activating campaigns requires confirmation.
        """
        
        # Safety check for activating
        if status.upper() == "ACTIVE":
            if self.config.require_confirmation() and not confirm:
                return {
                    "requires_confirmation": True,
                    "message": f"⚠️ Activating campaign {campaign_id} will start ad spend. Add --confirm to proceed.",
                    "warning": "This action will make the campaign LIVE and may incur costs."
                }
        
        endpoint = f"/adCampaigns/{campaign_id}"
        data = {
            "patch": {
                "$set": {
                    "status": status.upper()
                }
            }
        }
        
        result = self._make_request("PATCH", endpoint, data=data)
        
        if "error" in result:
            return result
        
        return {
            "success": True,
            "campaign_id": campaign_id,
            "new_status": status.upper(),
            "message": f"Campaign {campaign_id} status updated to {status.upper()}"
        }
    
    def update_campaign_budget(
        self,
        campaign_id: str,
        daily_budget: Optional[float] = None,
        total_budget: Optional[float] = None,
        confirm: bool = False
    ) -> Dict:
        """
        Update campaign budget.
        
        ⚠️ SAFETY: Budget increases require confirmation.
        """
        
        # Get current campaign
        current = self.get_campaign(campaign_id)
        if "error" in current:
            return current
        
        current_daily = 0
        if current.get("dailyBudget"):
            current_daily = float(current["dailyBudget"].get("amount", 0))
        
        # Check max budget
        max_budget = self.config.get_max_daily_budget()
        if daily_budget and max_budget > 0 and daily_budget > max_budget:
            return {
                "error": f"Budget ${daily_budget} exceeds maximum allowed ${max_budget}",
                "max_budget": max_budget
            }
        
        # Require confirmation for budget increases
        if daily_budget and daily_budget > current_daily:
            if self.config.require_confirmation() and not confirm:
                return {
                    "requires_confirmation": True,
                    "message": f"⚠️ Increasing budget from ${current_daily:.2f} to ${daily_budget:.2f}. Add --confirm to proceed.",
                    "current_budget": current_daily,
                    "new_budget": daily_budget
                }
        
        # Build update
        update_data = {"patch": {"$set": {}}}
        
        if daily_budget is not None:
            update_data["patch"]["$set"]["dailyBudget"] = {
                "currencyCode": "USD",
                "amount": str(daily_budget)
            }
        
        if total_budget is not None:
            update_data["patch"]["$set"]["totalBudget"] = {
                "currencyCode": "USD",
                "amount": str(total_budget)
            }
        
        endpoint = f"/adCampaigns/{campaign_id}"
        result = self._make_request("PATCH", endpoint, data=update_data)
        
        if "error" in result:
            return result
        
        return {
            "success": True,
            "campaign_id": campaign_id,
            "new_daily_budget": daily_budget,
            "new_total_budget": total_budget,
            "message": f"Campaign {campaign_id} budget updated"
        }
    
    def create_campaign_group(
        self,
        account_id: str,
        name: str,
        total_budget: float = 0,
        confirm: bool = False
    ) -> Dict:
        """Create a campaign group for organizing campaigns."""
        
        # Budget validation
        max_budget = self.config.get_max_daily_budget() * 30  # Monthly equivalent
        if max_budget > 0 and total_budget > max_budget:
            return {
                "error": f"Budget ${total_budget} exceeds maximum allowed ${max_budget}",
                "max_budget": max_budget
            }
        
        group_data = {
            "account": f"urn:li:sponsoredAccount:{account_id}",
            "name": name,
            "status": "DRAFT"
        }
        
        if total_budget > 0:
            group_data["totalBudget"] = {
                "currencyCode": "USD",
                "amount": str(total_budget)
            }
        
        endpoint = "/adCampaignGroups"
        result = self._make_request("POST", endpoint, data=group_data)
        
        if "error" in result:
            return result
        
        return {
            "success": True,
            "group_id": result.get("id"),
            "name": name,
            "status": "DRAFT",
            "message": f"✅ Campaign group '{name}' created in DRAFT status."
        }


def parse_targeting_string(targeting_str: str) -> Dict:
    """
    Parse a simple targeting string into API format.
    
    Format: "facet:value1,value2;facet2:value1"
    Example: "titles:VP Marketing,CMO;industries:Software"
    """
    if not targeting_str:
        return {}
    
    # This is a simplified parser - real implementation would need URN lookups
    criteria = {"include": {"and": []}}
    
    for facet_spec in targeting_str.split(";"):
        if ":" not in facet_spec:
            continue
        facet, values = facet_spec.split(":", 1)
        value_list = [v.strip() for v in values.split(",")]
        
        # Map common facet names to URNs
        facet_map = {
            "titles": "urn:li:adTargetingFacet:titles",
            "industries": "urn:li:adTargetingFacet:industries",
            "companySizes": "urn:li:adTargetingFacet:companySizes",
            "functions": "urn:li:adTargetingFacet:functions",
            "seniorities": "urn:li:adTargetingFacet:seniorities",
            "locations": "urn:li:adTargetingFacet:locations"
        }
        
        facet_urn = facet_map.get(facet, f"urn:li:adTargetingFacet:{facet}")
        
        # Note: Real implementation would lookup URNs for values
        criteria["include"]["and"].append({
            "or": {
                facet_urn: [f"placeholder:{v}" for v in value_list]
            }
        })
    
    return criteria


def format_results(results: Any, format_type: str = "table") -> str:
    """Format results for display."""
    if isinstance(results, dict):
        if "error" in results:
            return f"❌ Error: {results['error']}\n{results.get('details', '')}"
        if "requires_confirmation" in results:
            return f"⚠️  {results['message']}"
        return json.dumps(results, indent=2)
    
    if not results:
        return "No results found."
    
    if format_type == "json":
        return json.dumps(results, indent=2)
    
    # Table format
    if isinstance(results, list) and len(results) > 0:
        headers = list(results[0].keys())
        lines = [" | ".join(headers)]
        lines.append("-" * len(lines[0]))
        
        for row in results:
            values = []
            for key in headers:
                val = row.get(key, "")
                if isinstance(val, dict):
                    val = json.dumps(val)[:30]
                else:
                    val = str(val)[:30]
                values.append(val)
            lines.append(" | ".join(values))
        
        return "\n".join(lines)
    
    return str(results)


def main():
    parser = argparse.ArgumentParser(
        description="LinkedIn Ads API Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # List ad accounts
  python linkedin_ads.py accounts

  # List campaigns
  python linkedin_ads.py campaigns --account-id 123456789

  # Get analytics
  python linkedin_ads.py analytics --campaign-id 123456 --days 30

  # Create campaign (DRAFT)
  python linkedin_ads.py create --account-id 123456789 --name "My Campaign" --budget 100

  # Update status
  python linkedin_ads.py update --campaign-id 123456 --status PAUSED

  # Explore targeting
  python linkedin_ads.py targeting --facets
  python linkedin_ads.py targeting --search "Marketing" --facet titles
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Accounts command
    accounts_parser = subparsers.add_parser("accounts", help="List ad accounts")
    
    # Campaigns command
    campaigns_parser = subparsers.add_parser("campaigns", help="List campaigns")
    campaigns_parser.add_argument("--account-id", help="Ad account ID")
    
    # Analytics command
    analytics_parser = subparsers.add_parser("analytics", help="Get campaign analytics")
    analytics_parser.add_argument("--campaign-id", required=True, help="Campaign ID")
    analytics_parser.add_argument("--days", type=int, default=30, help="Number of days")
    
    # Create command
    create_parser = subparsers.add_parser("create", help="Create campaign (DRAFT)")
    create_parser.add_argument("--account-id", required=True, help="Ad account ID")
    create_parser.add_argument("--name", required=True, help="Campaign name")
    create_parser.add_argument("--objective", default="WEBSITE_VISITS",
                               choices=["BRAND_AWARENESS", "WEBSITE_VISITS", "ENGAGEMENT", 
                                       "VIDEO_VIEWS", "LEAD_GENERATION", "WEBSITE_CONVERSIONS"],
                               help="Campaign objective")
    create_parser.add_argument("--budget", type=float, default=0, help="Daily budget in USD")
    create_parser.add_argument("--total-budget", type=float, default=0, help="Total budget in USD")
    create_parser.add_argument("--targeting", help="Targeting criteria (format: facet:value1,value2)")
    create_parser.add_argument("--confirm", action="store_true", help="Confirm creation")
    
    # Update command
    update_parser = subparsers.add_parser("update", help="Update campaign")
    update_parser.add_argument("--campaign-id", required=True, help="Campaign ID")
    update_parser.add_argument("--status", choices=["ACTIVE", "PAUSED", "ARCHIVED"], help="New status")
    update_parser.add_argument("--budget", type=float, help="New daily budget")
    update_parser.add_argument("--confirm", action="store_true", help="Confirm changes")
    
    # Targeting command
    targeting_parser = subparsers.add_parser("targeting", help="Explore targeting options")
    targeting_parser.add_argument("--facets", action="store_true", help="List targeting facets")
    targeting_parser.add_argument("--search", help="Search for targeting values")
    targeting_parser.add_argument("--facet", help="Facet to search within")
    
    # Audience command
    audience_parser = subparsers.add_parser("audience", help="Get audience size estimate")
    audience_parser.add_argument("--targeting", required=True, help="Targeting criteria")
    
    # Global options
    parser.add_argument("--format", choices=["table", "json"], default="table", help="Output format")
    
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    # Initialize API
    api = LinkedInAdsAPI()

    # Check if credentials are available
    if not api.is_available:
        print(api.get_availability_message(), file=sys.stderr)
        sys.exit(1)

    # Execute command
    if args.command == "accounts":
        results = api.list_ad_accounts()
    
    elif args.command == "campaigns":
        results = api.list_campaigns(args.account_id)
    
    elif args.command == "analytics":
        results = api.get_campaign_analytics(args.campaign_id, days=args.days)
    
    elif args.command == "create":
        targeting = parse_targeting_string(args.targeting) if args.targeting else None
        results = api.create_campaign(
            account_id=args.account_id,
            name=args.name,
            objective=args.objective,
            daily_budget=args.budget,
            total_budget=args.total_budget,
            targeting_criteria=targeting,
            confirm=args.confirm
        )
    
    elif args.command == "update":
        if args.status:
            results = api.update_campaign_status(
                campaign_id=args.campaign_id,
                status=args.status,
                confirm=args.confirm
            )
        elif args.budget:
            results = api.update_campaign_budget(
                campaign_id=args.campaign_id,
                daily_budget=args.budget,
                confirm=args.confirm
            )
        else:
            print("Specify --status or --budget to update")
            return
    
    elif args.command == "targeting":
        if args.facets:
            results = api.get_targeting_facets()
        elif args.search and args.facet:
            facet_urn = f"urn:li:adTargetingFacet:{args.facet}"
            results = api.search_targeting_entities(facet_urn, args.search)
        else:
            print("Use --facets or --search with --facet")
            return
    
    elif args.command == "audience":
        targeting = parse_targeting_string(args.targeting)
        results = api.get_audience_count(targeting)
    
    else:
        parser.print_help()
        return
    
    # Output results
    print(format_results(results, args.format))


if __name__ == "__main__":
    main()
