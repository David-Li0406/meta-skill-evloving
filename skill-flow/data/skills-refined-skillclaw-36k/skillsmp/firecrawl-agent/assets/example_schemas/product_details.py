"""
Product Details Schema

Ready-to-use Pydantic models for extracting product and pricing information
using Firecrawl Agent.

Usage:
    from product_details import ProductDetails, ProductPricing
    schema = ProductDetails.model_json_schema()
"""

from typing import List, Optional
from pydantic import BaseModel, Field


class ProductFeature(BaseModel):
    """A single product feature."""
    name: str = Field(description="Feature name")
    description: Optional[str] = Field(default=None, description="Feature description")
    availability: Optional[str] = Field(
        default=None,
        description="Which plans include this feature (e.g., 'Pro and above')"
    )


class PricingTier(BaseModel):
    """A pricing tier/plan."""
    name: str = Field(description="Plan name (e.g., 'Free', 'Pro', 'Enterprise')")
    price_monthly: Optional[str] = Field(default=None, description="Monthly price")
    price_yearly: Optional[str] = Field(default=None, description="Yearly price")
    price_description: Optional[str] = Field(
        default=None,
        description="Price description for custom pricing (e.g., 'Contact sales')"
    )
    features: Optional[List[str]] = Field(default=None, description="Features included")
    limits: Optional[str] = Field(default=None, description="Usage limits or quotas")
    best_for: Optional[str] = Field(
        default=None,
        description="Who this plan is best for"
    )


class ProductPricing(BaseModel):
    """
    Product pricing information schema.

    Extracts complete pricing details including all tiers, billing options,
    and discounts.
    """
    product_name: str = Field(description="Name of the product")
    pricing_model: Optional[str] = Field(
        default=None,
        description="Type of pricing (freemium, subscription, usage-based, one-time)"
    )
    currency: Optional[str] = Field(default="USD", description="Pricing currency")

    tiers: List[PricingTier] = Field(description="Available pricing tiers")

    free_trial: Optional[str] = Field(
        default=None,
        description="Free trial details (duration, limitations)"
    )
    free_tier_available: Optional[bool] = Field(
        default=None,
        description="Whether a free tier is available"
    )

    discounts: Optional[List[str]] = Field(
        default=None,
        description="Available discounts (annual, student, nonprofit, etc.)"
    )
    money_back_guarantee: Optional[str] = Field(
        default=None,
        description="Refund policy or guarantee"
    )


class Integration(BaseModel):
    """Product integration details."""
    name: str = Field(description="Integration name")
    category: Optional[str] = Field(
        default=None,
        description="Category (e.g., 'CRM', 'Communication', 'Analytics')"
    )
    description: Optional[str] = Field(default=None, description="What the integration does")


class ProductDetails(BaseModel):
    """
    Comprehensive product details schema.

    Extracts detailed information about a software product including
    features, pricing, integrations, and technical specifications.
    """
    # Basic Info
    name: str = Field(description="Product name")
    company: Optional[str] = Field(default=None, description="Company that makes the product")
    tagline: Optional[str] = Field(default=None, description="Product tagline")
    description: str = Field(description="What the product does")
    category: Optional[str] = Field(
        default=None,
        description="Product category (e.g., 'Project Management', 'CRM')"
    )

    # Features
    key_features: Optional[List[str]] = Field(
        default=None,
        description="Main product features"
    )
    detailed_features: Optional[List[ProductFeature]] = Field(
        default=None,
        description="Detailed feature information"
    )

    # Pricing
    pricing: Optional[ProductPricing] = Field(
        default=None,
        description="Pricing information"
    )

    # Platform & Technical
    platforms: Optional[List[str]] = Field(
        default=None,
        description="Supported platforms (Web, iOS, Android, Desktop)"
    )
    integrations: Optional[List[Integration]] = Field(
        default=None,
        description="Available integrations"
    )
    api_available: Optional[bool] = Field(
        default=None,
        description="Whether an API is available"
    )

    # Reviews & Ratings
    rating: Optional[str] = Field(
        default=None,
        description="Average rating (e.g., '4.5/5')"
    )
    review_count: Optional[str] = Field(
        default=None,
        description="Number of reviews"
    )

    # Comparison
    competitors: Optional[List[str]] = Field(
        default=None,
        description="Main competitor products"
    )
    pros: Optional[List[str]] = Field(default=None, description="Product strengths")
    cons: Optional[List[str]] = Field(default=None, description="Product weaknesses")


class ProductComparison(BaseModel):
    """
    Schema for comparing multiple products.

    Use this when researching and comparing multiple competing products.
    """
    products: List[ProductDetails] = Field(description="Products being compared")
    comparison_summary: Optional[str] = Field(
        default=None,
        description="Overall comparison summary"
    )
    best_for: Optional[dict] = Field(
        default=None,
        description="Which product is best for different use cases"
    )


# JSON schema exports for direct use with Firecrawl
PRODUCT_DETAILS_SCHEMA = ProductDetails.model_json_schema()
PRODUCT_PRICING_SCHEMA = ProductPricing.model_json_schema()
PRODUCT_COMPARISON_SCHEMA = ProductComparison.model_json_schema()


if __name__ == "__main__":
    import json

    print("Product Details Schema:")
    print(json.dumps(PRODUCT_DETAILS_SCHEMA, indent=2))
    print("\n" + "=" * 50 + "\n")
    print("Product Pricing Schema:")
    print(json.dumps(PRODUCT_PRICING_SCHEMA, indent=2))
