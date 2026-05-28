"""
Error Handling and Recovery Guidance for CMO Agent Tools

Provides user-friendly error messages with specific recovery steps.
"""

from typing import Optional, Dict, Any
from dataclasses import dataclass
from enum import Enum


class ErrorCategory(Enum):
    """Categories of errors for better handling."""
    AUTHENTICATION = "authentication"
    AUTHORIZATION = "authorization"
    RATE_LIMIT = "rate_limit"
    VALIDATION = "validation"
    NOT_FOUND = "not_found"
    QUOTA = "quota"
    NETWORK = "network"
    CONFIGURATION = "configuration"
    BUDGET = "budget"
    UNKNOWN = "unknown"


@dataclass
class RecoveryGuidance:
    """Recovery steps for an error."""
    summary: str
    steps: list[str]
    docs_url: Optional[str] = None
    retry_after: Optional[int] = None  # Seconds


# ============================================================================
# Error Recovery Database
# ============================================================================

RECOVERY_GUIDES: Dict[str, Dict[str, RecoveryGuidance]] = {
    # Apollo Errors
    "apollo": {
        "401": RecoveryGuidance(
            summary="Apollo API key is invalid or expired",
            steps=[
                "1. Log into Apollo: https://app.apollo.io/#/settings/integrations/api",
                "2. Generate a new API key",
                "3. Update APOLLO_API_KEY in your .env file",
                "4. Restart the agent"
            ],
            docs_url="https://apolloio.github.io/apollo-api-docs/#authentication"
        ),
        "403": RecoveryGuidance(
            summary="Apollo API access denied - check your plan limits",
            steps=[
                "1. Check your Apollo plan: https://app.apollo.io/#/settings/plans",
                "2. Verify the endpoint is included in your plan",
                "3. Check if you've exceeded monthly credits"
            ],
            docs_url="https://apollo.io/pricing"
        ),
        "429": RecoveryGuidance(
            summary="Apollo rate limit exceeded",
            steps=[
                "1. Wait 60 seconds before retrying",
                "2. Reduce request frequency",
                "3. Consider upgrading your Apollo plan for higher limits"
            ],
            retry_after=60
        ),
        "missing_credential": RecoveryGuidance(
            summary="Apollo API key not configured",
            steps=[
                "1. Get your API key: https://app.apollo.io/#/settings/integrations/api",
                "2. Add to .env file: APOLLO_API_KEY=your_key_here",
                "3. Restart the agent"
            ]
        )
    },

    # Firecrawl Errors
    "firecrawl": {
        "401": RecoveryGuidance(
            summary="Firecrawl API key is invalid",
            steps=[
                "1. Log into Firecrawl: https://firecrawl.dev/dashboard",
                "2. Copy your API key",
                "3. Update FIRECRAWL_API_KEY in your .env file"
            ],
            docs_url="https://docs.firecrawl.dev/authentication"
        ),
        "402": RecoveryGuidance(
            summary="Firecrawl credits exhausted",
            steps=[
                "1. Check your usage: https://firecrawl.dev/dashboard",
                "2. Wait for monthly reset or upgrade your plan",
                "3. Free tier: 500 credits/month"
            ],
            docs_url="https://firecrawl.dev/pricing"
        ),
        "429": RecoveryGuidance(
            summary="Firecrawl rate limit exceeded",
            steps=[
                "1. Wait 30 seconds before retrying",
                "2. Reduce concurrent requests"
            ],
            retry_after=30
        ),
        "missing_credential": RecoveryGuidance(
            summary="Firecrawl API key not configured",
            steps=[
                "1. Sign up at: https://firecrawl.dev",
                "2. Get API key from dashboard",
                "3. Add to .env file: FIRECRAWL_API_KEY=your_key_here"
            ]
        )
    },

    # Clearbit Errors
    "clearbit": {
        "401": RecoveryGuidance(
            summary="Clearbit API key is invalid",
            steps=[
                "1. Log into Clearbit: https://dashboard.clearbit.com/api",
                "2. Generate a new API key",
                "3. Update CLEARBIT_API_KEY in your .env file"
            ]
        ),
        "402": RecoveryGuidance(
            summary="Clearbit requires a paid plan",
            steps=[
                "1. Clearbit has no free tier",
                "2. Sign up for a plan: https://clearbit.com/pricing",
                "3. Alternative: Use Apollo for company data (has free tier)"
            ]
        ),
        "missing_credential": RecoveryGuidance(
            summary="Clearbit API key not configured",
            steps=[
                "1. Clearbit requires a paid subscription",
                "2. Sign up: https://clearbit.com",
                "3. Add to .env: CLEARBIT_API_KEY=your_key_here",
                "4. Alternative: Use Apollo's company enrichment (free tier available)"
            ]
        )
    },

    # Google Ads Errors
    "google_ads": {
        "AUTHENTICATION_ERROR": RecoveryGuidance(
            summary="Google Ads authentication failed",
            steps=[
                "1. Check your OAuth credentials in .env",
                "2. Regenerate refresh token using OAuth flow",
                "3. Verify developer token is approved",
                "4. See setup guide: agents/ads/google-ads.md"
            ],
            docs_url="https://developers.google.com/google-ads/api/docs/oauth/overview"
        ),
        "AUTHORIZATION_ERROR": RecoveryGuidance(
            summary="Not authorized to access this Google Ads account",
            steps=[
                "1. Verify GOOGLE_ADS_LOGIN_CUSTOMER_ID is correct",
                "2. Check account access in Google Ads UI",
                "3. Ensure API access is enabled for the account"
            ]
        ),
        "QUOTA_ERROR": RecoveryGuidance(
            summary="Google Ads API quota exceeded",
            steps=[
                "1. Wait until quota resets (usually daily)",
                "2. Check quota usage in Google Cloud Console",
                "3. Request quota increase if needed"
            ],
            docs_url="https://developers.google.com/google-ads/api/docs/best-practices/quotas"
        ),
        "missing_credential": RecoveryGuidance(
            summary="Google Ads credentials not configured",
            steps=[
                "1. Create Google Cloud project with Ads API enabled",
                "2. Create OAuth 2.0 credentials",
                "3. Get developer token from Google Ads API Center",
                "4. Set all GOOGLE_ADS_* variables in .env",
                "5. See detailed guide: agents/ads/google-ads.md"
            ],
            docs_url="https://developers.google.com/google-ads/api/docs/first-call/overview"
        ),
        "BUDGET_EXCEEDED": RecoveryGuidance(
            summary="Campaign budget exceeds configured limit",
            steps=[
                "1. Check max_daily_budget in tools/ads_config.yaml",
                "2. Reduce budget amount or increase limit",
                "3. Current limit is set for safety - modify carefully"
            ]
        )
    },

    # LinkedIn Ads Errors
    "linkedin_ads": {
        "401": RecoveryGuidance(
            summary="LinkedIn access token is invalid or expired",
            steps=[
                "1. LinkedIn tokens expire after 60 days",
                "2. Regenerate token using OAuth flow",
                "3. Update LINKEDIN_ACCESS_TOKEN in .env",
                "4. See guide: agents/ads/linkedin-ads.md"
            ],
            docs_url="https://learn.microsoft.com/en-us/linkedin/shared/authentication/authorization-code-flow"
        ),
        "403": RecoveryGuidance(
            summary="LinkedIn API access denied",
            steps=[
                "1. Verify your app has Marketing Developer Platform access",
                "2. Check required scopes: r_ads, r_ads_reporting, w_organization_social",
                "3. Verify LINKEDIN_AD_ACCOUNT_ID is correct"
            ]
        ),
        "429": RecoveryGuidance(
            summary="LinkedIn rate limit exceeded",
            steps=[
                "1. Wait 60 seconds before retrying",
                "2. LinkedIn allows 100 requests/minute",
                "3. Reduce request frequency"
            ],
            retry_after=60
        ),
        "missing_credential": RecoveryGuidance(
            summary="LinkedIn Ads credentials not configured",
            steps=[
                "1. Create LinkedIn Developer App: https://www.linkedin.com/developers/apps",
                "2. Request Marketing Developer Platform access",
                "3. Generate OAuth 2.0 access token",
                "4. Set LINKEDIN_* variables in .env",
                "5. See guide: agents/ads/linkedin-ads.md"
            ]
        ),
        "BUDGET_EXCEEDED": RecoveryGuidance(
            summary="Campaign budget exceeds configured limit",
            steps=[
                "1. Check max_daily_budget in tools/ads_config.yaml",
                "2. Reduce budget or increase configured limit",
                "3. Default limit is $0 (testing mode)"
            ]
        )
    },

    # Proxycurl Errors
    "proxycurl": {
        "401": RecoveryGuidance(
            summary="Proxycurl API key is invalid",
            steps=[
                "1. Log into Proxycurl: https://nubela.co/proxycurl/",
                "2. Get your API key from the dashboard",
                "3. Update PROXYCURL_API_KEY in .env"
            ]
        ),
        "403": RecoveryGuidance(
            summary="Proxycurl credits exhausted",
            steps=[
                "1. Check your credit balance: https://nubela.co/proxycurl/",
                "2. Free tier: 10 credits/month",
                "3. Purchase more credits or wait for reset"
            ]
        ),
        "missing_credential": RecoveryGuidance(
            summary="Proxycurl API key not configured",
            steps=[
                "1. Sign up: https://nubela.co/proxycurl/",
                "2. Get API key from dashboard",
                "3. Add to .env: PROXYCURL_API_KEY=your_key_here"
            ]
        )
    },
    # Robynn Errors
    "robynn": {
        "401": RecoveryGuidance(
            summary="Robynn API key is invalid or expired",
            steps=[
                "1. Log into Robynn: https://robynn.ai/settings/api-keys",
                "2. Generate a new API key",
                "3. Run: rory config <new_key>"
            ],
            docs_url="https://robynn.ai/docs/rory"
        ),
        "429": RecoveryGuidance(
            summary="You've used all your tasks for this period",
            steps=[
                "1. Check your usage: rory usage",
                "2. Wait for reset or upgrade at https://robynn.ai/pricing"
            ]
        ),
        "missing_credential": RecoveryGuidance(
            summary="Not connected to Robynn",
            steps=[
                "1. Run: rory init",
                "2. Follow the setup wizard",
                "3. Paste your API key when prompted"
            ]
        )
    }
}


# ============================================================================
# Error Formatting Functions
# ============================================================================

def format_error(
    service: str,
    error_code: str,
    original_message: str = "",
    context: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Format an error with recovery guidance.

    Args:
        service: Service name (apollo, firecrawl, google_ads, etc.)
        error_code: Error code or status code
        original_message: Original error message
        context: Additional context

    Returns:
        Formatted error dictionary with recovery steps
    """
    error_code = str(error_code)

    # Look up recovery guidance
    service_guides = RECOVERY_GUIDES.get(service, {})
    guidance = service_guides.get(error_code)

    if guidance is None:
        # Try to categorize the error
        guidance = _get_generic_guidance(error_code)

    result = {
        "error": True,
        "service": service,
        "code": error_code,
        "message": original_message or guidance.summary if guidance else "Unknown error",
        "category": _categorize_error(error_code),
    }

    if guidance:
        result["recovery"] = {
            "summary": guidance.summary,
            "steps": guidance.steps,
        }
        if guidance.docs_url:
            result["recovery"]["documentation"] = guidance.docs_url
        if guidance.retry_after:
            result["recovery"]["retry_after_seconds"] = guidance.retry_after

    if context:
        result["context"] = context

    return result


def format_missing_credential_error(service: str) -> Dict[str, Any]:
    """Format error for missing API credentials."""
    return format_error(service, "missing_credential")


def format_budget_error(
    service: str,
    requested: float,
    maximum: float
) -> Dict[str, Any]:
    """Format error for budget limit exceeded."""
    return format_error(
        service,
        "BUDGET_EXCEEDED",
        f"Requested budget ${requested:.2f} exceeds maximum ${maximum:.2f}",
        context={"requested": requested, "maximum": maximum}
    )


def _categorize_error(code: str) -> str:
    """Categorize error by code."""
    code = str(code)

    if code in ("401", "AUTHENTICATION_ERROR"):
        return ErrorCategory.AUTHENTICATION.value
    elif code in ("403", "AUTHORIZATION_ERROR"):
        return ErrorCategory.AUTHORIZATION.value
    elif code in ("429", "RATE_LIMIT"):
        return ErrorCategory.RATE_LIMIT.value
    elif code in ("400", "VALIDATION_ERROR"):
        return ErrorCategory.VALIDATION.value
    elif code in ("404", "NOT_FOUND"):
        return ErrorCategory.NOT_FOUND.value
    elif code in ("402", "QUOTA_ERROR", "QUOTA_EXCEEDED"):
        return ErrorCategory.QUOTA.value
    elif code in ("BUDGET_EXCEEDED",):
        return ErrorCategory.BUDGET.value
    elif code == "missing_credential":
        return ErrorCategory.CONFIGURATION.value
    else:
        return ErrorCategory.UNKNOWN.value


def _get_generic_guidance(code: str) -> Optional[RecoveryGuidance]:
    """Get generic guidance for common error codes."""
    generic_guides = {
        "401": RecoveryGuidance(
            summary="Authentication failed",
            steps=[
                "1. Check your API key or token in .env",
                "2. Verify the key hasn't expired",
                "3. Regenerate credentials if needed"
            ]
        ),
        "403": RecoveryGuidance(
            summary="Access denied",
            steps=[
                "1. Check your account permissions",
                "2. Verify you have access to this resource",
                "3. Check if your plan includes this feature"
            ]
        ),
        "429": RecoveryGuidance(
            summary="Rate limit exceeded",
            steps=[
                "1. Wait before retrying (usually 30-60 seconds)",
                "2. Reduce request frequency",
                "3. Consider upgrading your plan"
            ],
            retry_after=60
        ),
        "500": RecoveryGuidance(
            summary="Server error",
            steps=[
                "1. Wait a moment and retry",
                "2. Check service status page",
                "3. If persistent, contact support"
            ],
            retry_after=30
        )
    }
    return generic_guides.get(str(code))


# ============================================================================
# User-Friendly Message Formatting
# ============================================================================

def format_error_message(error: Dict[str, Any]) -> str:
    """
    Format error dictionary into user-friendly message.

    Args:
        error: Error dictionary from format_error()

    Returns:
        Formatted string for display
    """
    lines = []

    # Header
    lines.append(f"❌ Error: {error.get('message', 'Unknown error')}")
    lines.append("")

    # Recovery steps
    if "recovery" in error:
        recovery = error["recovery"]
        lines.append(f"💡 {recovery['summary']}")
        lines.append("")
        lines.append("How to fix:")
        for step in recovery["steps"]:
            lines.append(f"   {step}")

        if "documentation" in recovery:
            lines.append("")
            lines.append(f"📚 Documentation: {recovery['documentation']}")

        if "retry_after_seconds" in recovery:
            lines.append("")
            lines.append(f"⏱️  Retry after: {recovery['retry_after_seconds']} seconds")

    return "\n".join(lines)
