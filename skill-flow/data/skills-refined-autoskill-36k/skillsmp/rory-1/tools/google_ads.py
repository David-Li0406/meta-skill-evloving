#!/usr/bin/env python3
"""
Google Ads API Tool
===================
Wrapper for Google Ads API operations with safety rails.

This tool integrates with the cohnen/mcp-google-ads MCP server or can be used
standalone with direct API calls.

Setup:
    1. Install: pip install google-ads pyyaml python-dotenv
    2. Configure .env with Google Ads credentials
    3. Run: python google_ads.py --help

Safety Features:
    - All new campaigns created in PAUSED status
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

# Try to import Google Ads library
try:
    from google.ads.googleads.client import GoogleAdsClient
    from google.ads.googleads.errors import GoogleAdsException
    GOOGLE_ADS_AVAILABLE = True
except ImportError:
    GOOGLE_ADS_AVAILABLE = False
    GoogleAdsClient = None
    GoogleAdsException = Exception

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
        
        # Default config if file not found
        return {
            "safety": {
                "force_draft_mode": True,
                "require_confirmation": True
            },
            "budgets": {
                "google_ads": {
                    "max_daily_budget": 0,
                    "max_total_budget": 0,
                    "max_cpc_bid": 5.00
                }
            },
            "defaults": {
                "google_ads": {
                    "status": "PAUSED",
                    "bidding_strategy": "MAXIMIZE_CLICKS"
                }
            }
        }
    
    def get_max_daily_budget(self) -> float:
        return self.config.get("budgets", {}).get("google_ads", {}).get("max_daily_budget", 0)
    
    def get_max_cpc_bid(self) -> float:
        return self.config.get("budgets", {}).get("google_ads", {}).get("max_cpc_bid", 5.00)
    
    def force_draft_mode(self) -> bool:
        return self.config.get("safety", {}).get("force_draft_mode", True)
    
    def require_confirmation(self) -> bool:
        return self.config.get("safety", {}).get("require_confirmation", True)


class GoogleAdsAPI:
    """
    Google Ads API wrapper with safety features.

    Can operate in two modes:
    1. Direct API mode (requires google-ads library)
    2. MCP mode (delegates to MCP server)
    """

    SERVICE_NAME = "google_ads"

    def __init__(self, config: Optional[AdsConfig] = None):
        self.config = config or AdsConfig()
        self.client = None
        self._is_available = False
        self._availability_reason = None
        self._init_client()

    def _init_client(self):
        """Initialize Google Ads client from environment variables."""
        if not GOOGLE_ADS_AVAILABLE:
            self._availability_reason = "google-ads library not installed. Install with: pip install google-ads"
            return

        # Check for required credentials
        required_vars = [
            "GOOGLE_ADS_DEVELOPER_TOKEN",
            "GOOGLE_ADS_CLIENT_ID",
            "GOOGLE_ADS_CLIENT_SECRET",
            "GOOGLE_ADS_REFRESH_TOKEN"
        ]

        missing = [v for v in required_vars if not os.getenv(v)]
        if missing:
            self._availability_reason = f"Missing environment variables: {', '.join(missing)}"
            return

        try:
            # Build configuration dict
            config_dict = {
                "developer_token": os.getenv("GOOGLE_ADS_DEVELOPER_TOKEN"),
                "client_id": os.getenv("GOOGLE_ADS_CLIENT_ID"),
                "client_secret": os.getenv("GOOGLE_ADS_CLIENT_SECRET"),
                "refresh_token": os.getenv("GOOGLE_ADS_REFRESH_TOKEN"),
                "use_proto_plus": True
            }

            login_customer_id = os.getenv("GOOGLE_ADS_LOGIN_CUSTOMER_ID")
            if login_customer_id:
                config_dict["login_customer_id"] = login_customer_id

            self.client = GoogleAdsClient.load_from_dict(config_dict)
            self._is_available = True

        except Exception as e:
            self._availability_reason = f"Failed to initialize client: {e}"

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
    
    # =========================================================================
    # READ OPERATIONS
    # =========================================================================
    
    def list_accounts(self) -> List[Dict]:
        """List accessible Google Ads accounts."""
        if not self.client:
            return self._no_client_error()
        
        try:
            customer_service = self.client.get_service("CustomerService")
            accessible_customers = customer_service.list_accessible_customers()
            
            accounts = []
            for resource_name in accessible_customers.resource_names:
                customer_id = resource_name.split("/")[-1]
                accounts.append({
                    "customer_id": customer_id,
                    "resource_name": resource_name
                })
            
            return accounts
            
        except GoogleAdsException as e:
            return self._handle_error(e)
    
    def list_campaigns(self, customer_id: str) -> List[Dict]:
        """List all campaigns for a customer."""
        query = """
            SELECT
                campaign.id,
                campaign.name,
                campaign.status,
                campaign.advertising_channel_type,
                campaign_budget.amount_micros
            FROM campaign
            WHERE campaign.status != 'REMOVED'
            ORDER BY campaign.name
        """
        return self.run_query(customer_id, query)
    
    def get_campaign(self, customer_id: str, campaign_id: str) -> Dict:
        """Get details for a specific campaign."""
        query = f"""
            SELECT
                campaign.id,
                campaign.name,
                campaign.status,
                campaign.advertising_channel_type,
                campaign.bidding_strategy_type,
                campaign_budget.amount_micros,
                campaign.start_date,
                campaign.end_date
            FROM campaign
            WHERE campaign.id = {campaign_id}
        """
        results = self.run_query(customer_id, query)
        return results[0] if results else None
    
    def get_campaign_performance(
        self, 
        customer_id: str, 
        days: int = 30,
        campaign_id: Optional[str] = None
    ) -> List[Dict]:
        """Get campaign performance metrics."""
        
        date_filter = f"segments.date DURING LAST_{days}_DAYS"
        campaign_filter = f"AND campaign.id = {campaign_id}" if campaign_id else ""
        
        query = f"""
            SELECT
                campaign.id,
                campaign.name,
                campaign.status,
                metrics.impressions,
                metrics.clicks,
                metrics.ctr,
                metrics.average_cpc,
                metrics.cost_micros,
                metrics.conversions,
                metrics.cost_per_conversion
            FROM campaign
            WHERE {date_filter}
                AND campaign.status != 'REMOVED'
                {campaign_filter}
            ORDER BY metrics.cost_micros DESC
        """
        return self.run_query(customer_id, query)
    
    def get_ad_performance(
        self,
        customer_id: str,
        days: int = 30,
        campaign_id: Optional[str] = None
    ) -> List[Dict]:
        """Get ad-level performance metrics."""
        
        date_filter = f"segments.date DURING LAST_{days}_DAYS"
        campaign_filter = f"AND campaign.id = {campaign_id}" if campaign_id else ""
        
        query = f"""
            SELECT
                ad_group_ad.ad.id,
                ad_group_ad.ad.type,
                ad_group.name,
                campaign.name,
                metrics.impressions,
                metrics.clicks,
                metrics.ctr,
                metrics.average_cpc,
                metrics.conversions
            FROM ad_group_ad
            WHERE {date_filter}
                AND ad_group_ad.status = 'ENABLED'
                {campaign_filter}
            ORDER BY metrics.clicks DESC
            LIMIT 50
        """
        return self.run_query(customer_id, query)
    
    def get_keyword_performance(
        self,
        customer_id: str,
        days: int = 30,
        campaign_id: Optional[str] = None
    ) -> List[Dict]:
        """Get keyword performance metrics (Search campaigns)."""
        
        date_filter = f"segments.date DURING LAST_{days}_DAYS"
        campaign_filter = f"AND campaign.id = {campaign_id}" if campaign_id else ""
        
        query = f"""
            SELECT
                ad_group_criterion.keyword.text,
                ad_group_criterion.keyword.match_type,
                campaign.name,
                ad_group.name,
                metrics.impressions,
                metrics.clicks,
                metrics.ctr,
                metrics.average_cpc,
                metrics.conversions
            FROM keyword_view
            WHERE {date_filter}
                {campaign_filter}
            ORDER BY metrics.conversions DESC
            LIMIT 100
        """
        return self.run_query(customer_id, query)
    
    def run_query(self, customer_id: str, query: str) -> List[Dict]:
        """Run a GAQL query and return results."""
        if not self.client:
            return self._no_client_error()
        
        try:
            ga_service = self.client.get_service("GoogleAdsService")
            
            # Clean customer ID (remove dashes if present)
            customer_id = customer_id.replace("-", "")
            
            response = ga_service.search(customer_id=customer_id, query=query)
            
            results = []
            for row in response:
                result = self._row_to_dict(row)
                results.append(result)
            
            return results
            
        except GoogleAdsException as e:
            return self._handle_error(e)
    
    # =========================================================================
    # WRITE OPERATIONS (with safety rails)
    # =========================================================================
    
    def create_campaign(
        self,
        customer_id: str,
        name: str,
        campaign_type: str = "SEARCH",
        budget_amount: float = 0,
        bidding_strategy: str = "MAXIMIZE_CLICKS",
        confirm: bool = False
    ) -> Dict:
        """
        Create a new campaign in PAUSED status.
        
        ⚠️ SAFETY: Campaign is always created in PAUSED status.
        """
        if not self.client:
            return self._no_client_error()
        
        # Safety check: force draft mode
        if self.config.force_draft_mode():
            status = "PAUSED"
        else:
            status = "PAUSED"  # Always paused regardless
        
        # Budget validation
        max_budget = self.config.get_max_daily_budget()
        if max_budget > 0 and budget_amount > max_budget:
            return {
                "error": f"Budget ${budget_amount} exceeds maximum allowed ${max_budget}",
                "max_budget": max_budget
            }
        
        # Confirmation for non-zero budget
        if budget_amount > 0 and self.config.require_confirmation() and not confirm:
            return {
                "requires_confirmation": True,
                "message": f"Creating campaign '{name}' with ${budget_amount}/day budget. Add --confirm to proceed.",
                "details": {
                    "name": name,
                    "type": campaign_type,
                    "budget": budget_amount,
                    "status": status
                }
            }
        
        try:
            customer_id = customer_id.replace("-", "")
            
            # Create budget
            campaign_budget_service = self.client.get_service("CampaignBudgetService")
            campaign_service = self.client.get_service("CampaignService")
            
            # Budget operation
            budget_operation = self.client.get_type("CampaignBudgetOperation")
            budget = budget_operation.create
            budget.name = f"{name} Budget - {datetime.now().strftime('%Y%m%d_%H%M%S')}"
            budget.amount_micros = int(budget_amount * 1_000_000)
            budget.delivery_method = self.client.enums.BudgetDeliveryMethodEnum.STANDARD
            
            budget_response = campaign_budget_service.mutate_campaign_budgets(
                customer_id=customer_id,
                operations=[budget_operation]
            )
            budget_resource_name = budget_response.results[0].resource_name
            
            # Campaign operation
            campaign_operation = self.client.get_type("CampaignOperation")
            campaign = campaign_operation.create
            campaign.name = name
            campaign.campaign_budget = budget_resource_name
            campaign.status = self.client.enums.CampaignStatusEnum.PAUSED  # Always PAUSED
            
            # Set campaign type
            channel_type_enum = self.client.enums.AdvertisingChannelTypeEnum
            campaign.advertising_channel_type = getattr(channel_type_enum, campaign_type, channel_type_enum.SEARCH)
            
            # Set bidding strategy
            if bidding_strategy == "MAXIMIZE_CLICKS":
                campaign.maximize_clicks.cpc_bid_ceiling_micros = int(self.config.get_max_cpc_bid() * 1_000_000)
            elif bidding_strategy == "MAXIMIZE_CONVERSIONS":
                campaign.maximize_conversions.target_cpa_micros = 0
            elif bidding_strategy == "MANUAL_CPC":
                campaign.manual_cpc.enhanced_cpc_enabled = False
            
            # Network settings for Search campaigns
            if campaign_type == "SEARCH":
                campaign.network_settings.target_google_search = True
                campaign.network_settings.target_search_network = False
                campaign.network_settings.target_content_network = False
            
            campaign_response = campaign_service.mutate_campaigns(
                customer_id=customer_id,
                operations=[campaign_operation]
            )
            
            campaign_resource_name = campaign_response.results[0].resource_name
            campaign_id = campaign_resource_name.split("/")[-1]
            
            return {
                "success": True,
                "campaign_id": campaign_id,
                "resource_name": campaign_resource_name,
                "name": name,
                "status": "PAUSED",
                "budget_daily": budget_amount,
                "message": f"✅ Campaign '{name}' created in PAUSED status. Log into Google Ads to review and activate."
            }
            
        except GoogleAdsException as e:
            return self._handle_error(e)
    
    def update_campaign_status(
        self,
        customer_id: str,
        campaign_id: str,
        status: str,
        confirm: bool = False
    ) -> Dict:
        """
        Update campaign status.
        
        ⚠️ SAFETY: Enabling campaigns requires confirmation.
        """
        if not self.client:
            return self._no_client_error()
        
        # Safety check for enabling
        if status.upper() == "ENABLED":
            if self.config.require_confirmation() and not confirm:
                return {
                    "requires_confirmation": True,
                    "message": f"⚠️ Enabling campaign {campaign_id} will start ad spend. Add --confirm to proceed.",
                    "warning": "This action will make the campaign LIVE and may incur costs."
                }
        
        try:
            customer_id = customer_id.replace("-", "")
            campaign_service = self.client.get_service("CampaignService")
            
            campaign_operation = self.client.get_type("CampaignOperation")
            campaign = campaign_operation.update
            campaign.resource_name = f"customers/{customer_id}/campaigns/{campaign_id}"
            
            status_enum = self.client.enums.CampaignStatusEnum
            campaign.status = getattr(status_enum, status.upper(), status_enum.PAUSED)
            
            # Set update mask
            self.client.copy_from(
                campaign_operation.update_mask,
                self._get_field_mask(["status"])
            )
            
            response = campaign_service.mutate_campaigns(
                customer_id=customer_id,
                operations=[campaign_operation]
            )
            
            return {
                "success": True,
                "campaign_id": campaign_id,
                "new_status": status.upper(),
                "message": f"Campaign {campaign_id} status updated to {status.upper()}"
            }
            
        except GoogleAdsException as e:
            return self._handle_error(e)
    
    def update_campaign_budget(
        self,
        customer_id: str,
        campaign_id: str,
        new_budget: float,
        confirm: bool = False
    ) -> Dict:
        """
        Update campaign daily budget.
        
        ⚠️ SAFETY: Budget increases require confirmation.
        """
        if not self.client:
            return self._no_client_error()
        
        # Get current budget
        current = self.get_campaign(customer_id, campaign_id)
        if not current:
            return {"error": f"Campaign {campaign_id} not found"}
        
        current_budget = current.get("campaign_budget", {}).get("amount_micros", 0) / 1_000_000
        
        # Check max budget
        max_budget = self.config.get_max_daily_budget()
        if max_budget > 0 and new_budget > max_budget:
            return {
                "error": f"Budget ${new_budget} exceeds maximum allowed ${max_budget}",
                "max_budget": max_budget
            }
        
        # Require confirmation for budget increases
        if new_budget > current_budget and self.config.require_confirmation() and not confirm:
            return {
                "requires_confirmation": True,
                "message": f"⚠️ Increasing budget from ${current_budget:.2f} to ${new_budget:.2f}. Add --confirm to proceed.",
                "current_budget": current_budget,
                "new_budget": new_budget
            }
        
        # Note: Full implementation would update the CampaignBudget resource
        # This is a simplified version
        return {
            "error": "Budget update requires updating CampaignBudget resource. Please use Google Ads UI.",
            "current_budget": current_budget,
            "requested_budget": new_budget
        }
    
    # =========================================================================
    # HELPER METHODS
    # =========================================================================
    
    def _row_to_dict(self, row) -> Dict:
        """Convert a GoogleAdsRow to a dictionary."""
        result = {}
        
        # Campaign fields
        if hasattr(row, 'campaign') and row.campaign:
            result['campaign'] = {
                'id': str(row.campaign.id),
                'name': row.campaign.name,
                'status': str(row.campaign.status.name) if row.campaign.status else None,
                'advertising_channel_type': str(row.campaign.advertising_channel_type.name) if row.campaign.advertising_channel_type else None
            }
        
        # Budget fields
        if hasattr(row, 'campaign_budget') and row.campaign_budget:
            result['campaign_budget'] = {
                'amount_micros': row.campaign_budget.amount_micros,
                'amount': row.campaign_budget.amount_micros / 1_000_000
            }
        
        # Metrics
        if hasattr(row, 'metrics') and row.metrics:
            result['metrics'] = {
                'impressions': row.metrics.impressions,
                'clicks': row.metrics.clicks,
                'ctr': row.metrics.ctr,
                'average_cpc': row.metrics.average_cpc / 1_000_000 if row.metrics.average_cpc else 0,
                'cost': row.metrics.cost_micros / 1_000_000 if row.metrics.cost_micros else 0,
                'conversions': row.metrics.conversions,
                'cost_per_conversion': row.metrics.cost_per_conversion / 1_000_000 if row.metrics.cost_per_conversion else 0
            }
        
        # Ad group fields
        if hasattr(row, 'ad_group') and row.ad_group:
            result['ad_group'] = {
                'id': str(row.ad_group.id),
                'name': row.ad_group.name
            }
        
        # Ad fields
        if hasattr(row, 'ad_group_ad') and row.ad_group_ad:
            result['ad'] = {
                'id': str(row.ad_group_ad.ad.id),
                'type': str(row.ad_group_ad.ad.type_.name) if row.ad_group_ad.ad.type_ else None
            }
        
        # Keyword fields
        if hasattr(row, 'ad_group_criterion') and row.ad_group_criterion:
            if hasattr(row.ad_group_criterion, 'keyword'):
                result['keyword'] = {
                    'text': row.ad_group_criterion.keyword.text,
                    'match_type': str(row.ad_group_criterion.keyword.match_type.name)
                }
        
        return result
    
    def _get_field_mask(self, fields: List[str]):
        """Create a field mask for update operations."""
        from google.protobuf import field_mask_pb2
        return field_mask_pb2.FieldMask(paths=fields)
    
    def _no_client_error(self) -> Dict:
        """Return error when client is not initialized."""
        return self.get_availability_error()
    
    def _handle_error(self, e: Exception) -> Dict:
        """Handle Google Ads API errors."""
        if isinstance(e, GoogleAdsException):
            errors = []
            for error in e.failure.errors:
                errors.append({
                    "message": error.message,
                    "code": str(error.error_code)
                })
            return {
                "error": "Google Ads API Error",
                "request_id": e.request_id,
                "errors": errors
            }
        return {"error": str(e)}


def format_results(results: Any, format_type: str = "table") -> str:
    """Format results for display."""
    if isinstance(results, dict):
        if "error" in results:
            return f"❌ Error: {results['error']}"
        if "requires_confirmation" in results:
            return f"⚠️  {results['message']}"
        return json.dumps(results, indent=2)
    
    if not results:
        return "No results found."
    
    if format_type == "json":
        return json.dumps(results, indent=2)
    
    # Table format
    if isinstance(results, list) and len(results) > 0:
        # Get all keys from first result
        headers = []
        for key in results[0].keys():
            if isinstance(results[0][key], dict):
                for subkey in results[0][key].keys():
                    headers.append(f"{key}.{subkey}")
            else:
                headers.append(key)
        
        lines = [" | ".join(headers)]
        lines.append("-" * len(lines[0]))
        
        for row in results:
            values = []
            for key in row.keys():
                if isinstance(row[key], dict):
                    for subkey in row[key].keys():
                        val = row[key][subkey]
                        if isinstance(val, float):
                            values.append(f"{val:.2f}")
                        else:
                            values.append(str(val)[:30])
                else:
                    values.append(str(row[key])[:30])
            lines.append(" | ".join(values))
        
        return "\n".join(lines)
    
    return str(results)


def main():
    parser = argparse.ArgumentParser(
        description="Google Ads API Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # List accounts
  python google_ads.py accounts

  # List campaigns
  python google_ads.py campaigns --customer-id 1234567890

  # Get performance
  python google_ads.py performance --customer-id 1234567890 --days 30

  # Run GAQL query
  python google_ads.py query --customer-id 1234567890 --gaql "SELECT campaign.name FROM campaign"

  # Create campaign (DRAFT)
  python google_ads.py create --customer-id 1234567890 --name "My Campaign" --budget 50

  # Update status
  python google_ads.py update --customer-id 1234567890 --campaign-id 123 --status PAUSED
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Accounts command
    accounts_parser = subparsers.add_parser("accounts", help="List accessible accounts")
    
    # Campaigns command
    campaigns_parser = subparsers.add_parser("campaigns", help="List campaigns")
    campaigns_parser.add_argument("--customer-id", required=True, help="Google Ads customer ID")
    
    # Performance command
    perf_parser = subparsers.add_parser("performance", help="Get campaign performance")
    perf_parser.add_argument("--customer-id", required=True, help="Google Ads customer ID")
    perf_parser.add_argument("--days", type=int, default=30, help="Number of days (default: 30)")
    perf_parser.add_argument("--campaign-id", help="Filter to specific campaign")
    
    # Query command
    query_parser = subparsers.add_parser("query", help="Run GAQL query")
    query_parser.add_argument("--customer-id", required=True, help="Google Ads customer ID")
    query_parser.add_argument("--gaql", required=True, help="GAQL query string")
    
    # Create command
    create_parser = subparsers.add_parser("create", help="Create new campaign (DRAFT)")
    create_parser.add_argument("--customer-id", required=True, help="Google Ads customer ID")
    create_parser.add_argument("--name", required=True, help="Campaign name")
    create_parser.add_argument("--type", default="SEARCH", choices=["SEARCH", "DISPLAY", "SHOPPING", "VIDEO", "PERFORMANCE_MAX"], help="Campaign type")
    create_parser.add_argument("--budget", type=float, default=0, help="Daily budget in USD")
    create_parser.add_argument("--bidding", default="MAXIMIZE_CLICKS", help="Bidding strategy")
    create_parser.add_argument("--confirm", action="store_true", help="Confirm creation")
    
    # Update command
    update_parser = subparsers.add_parser("update", help="Update campaign")
    update_parser.add_argument("--customer-id", required=True, help="Google Ads customer ID")
    update_parser.add_argument("--campaign-id", required=True, help="Campaign ID to update")
    update_parser.add_argument("--status", choices=["ENABLED", "PAUSED"], help="New status")
    update_parser.add_argument("--budget", type=float, help="New daily budget")
    update_parser.add_argument("--confirm", action="store_true", help="Confirm changes")
    
    # Global options
    parser.add_argument("--format", choices=["table", "json"], default="table", help="Output format")
    
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    # Initialize API
    api = GoogleAdsAPI()

    # Check if credentials are available
    if not api.is_available:
        print(api.get_availability_message(), file=sys.stderr)
        sys.exit(1)
    
    # Execute command
    if args.command == "accounts":
        results = api.list_accounts()
    
    elif args.command == "campaigns":
        results = api.list_campaigns(args.customer_id)
    
    elif args.command == "performance":
        results = api.get_campaign_performance(
            args.customer_id,
            days=args.days,
            campaign_id=args.campaign_id
        )
    
    elif args.command == "query":
        results = api.run_query(args.customer_id, args.gaql)
    
    elif args.command == "create":
        results = api.create_campaign(
            customer_id=args.customer_id,
            name=args.name,
            campaign_type=args.type,
            budget_amount=args.budget,
            bidding_strategy=args.bidding,
            confirm=args.confirm
        )
    
    elif args.command == "update":
        if args.status:
            results = api.update_campaign_status(
                customer_id=args.customer_id,
                campaign_id=args.campaign_id,
                status=args.status,
                confirm=args.confirm
            )
        elif args.budget:
            results = api.update_campaign_budget(
                customer_id=args.customer_id,
                campaign_id=args.campaign_id,
                new_budget=args.budget,
                confirm=args.confirm
            )
        else:
            print("Specify --status or --budget to update")
            return
    
    else:
        parser.print_help()
        return
    
    # Output results
    print(format_results(results, args.format))


if __name__ == "__main__":
    main()
