# Common Schema Patterns for Firecrawl Agent

This document provides ready-to-use schema patterns for common data extraction scenarios.

## Schema Basics

Schemas define the structure of extracted data. They use a simplified JSON format:

```json
{
  "field_name": "type",
  "array_field": ["type"],
  "nested_object": {
    "sub_field": "type"
  }
}
```

### Supported Types

| Type | Description | Example Values |
|------|-------------|----------------|
| `"string"` | Text data | `"John Doe"`, `"$99/month"` |
| `"number"` | Numeric data | `42`, `3.14`, `2024` |
| `"boolean"` | True/false | `true`, `false` |
| `["string"]` | Array of strings | `["item1", "item2"]` |
| `["number"]` | Array of numbers | `[1, 2, 3]` |

---

## Company Information Schemas

### Basic Company Profile

```json
{
  "company_name": "string",
  "description": "string",
  "founded_year": "number",
  "headquarters": "string",
  "website": "string"
}
```

### Company with Founders

```json
{
  "company_name": "string",
  "description": "string",
  "founded_year": "number",
  "founders": [
    {
      "name": "string",
      "role": "string",
      "linkedin": "string"
    }
  ],
  "headquarters": "string"
}
```

### Full Company Research

```json
{
  "company_name": "string",
  "description": "string",
  "founded_year": "number",
  "founders": ["string"],
  "headquarters": "string",
  "employee_count": "string",
  "funding": {
    "total_raised": "string",
    "last_round": "string",
    "last_round_date": "string",
    "investors": ["string"]
  },
  "products": ["string"],
  "tech_stack": ["string"],
  "competitors": ["string"]
}
```

---

## Pricing Schemas

### Simple Pricing Tiers

```json
{
  "product_name": "string",
  "pricing_tiers": [
    {
      "name": "string",
      "price": "string",
      "billing": "string"
    }
  ]
}
```

### Detailed Pricing

```json
{
  "product_name": "string",
  "pricing_model": "string",
  "currency": "string",
  "tiers": [
    {
      "name": "string",
      "price_monthly": "string",
      "price_yearly": "string",
      "features": ["string"],
      "limits": "string",
      "best_for": "string"
    }
  ],
  "free_tier": {
    "available": "boolean",
    "limitations": "string"
  },
  "enterprise": {
    "available": "boolean",
    "contact_required": "boolean"
  },
  "discounts": ["string"]
}
```

### Usage-Based Pricing

```json
{
  "product_name": "string",
  "pricing_model": "string",
  "base_price": "string",
  "usage_units": "string",
  "tiers": [
    {
      "range": "string",
      "price_per_unit": "string"
    }
  ],
  "included_usage": "string",
  "overage_price": "string"
}
```

---

## Product Information Schemas

### Product Features

```json
{
  "product_name": "string",
  "tagline": "string",
  "category": "string",
  "features": [
    {
      "name": "string",
      "description": "string"
    }
  ],
  "integrations": ["string"],
  "platforms": ["string"]
}
```

### Product Comparison

```json
{
  "products": [
    {
      "name": "string",
      "company": "string",
      "price_range": "string",
      "key_features": ["string"],
      "pros": ["string"],
      "cons": ["string"],
      "best_for": "string"
    }
  ],
  "comparison_summary": "string"
}
```

---

## Contact Information Schemas

### Basic Contact

```json
{
  "company_name": "string",
  "email": "string",
  "phone": "string",
  "address": "string"
}
```

### Full Contact Details

```json
{
  "company_name": "string",
  "contact": {
    "general_email": "string",
    "sales_email": "string",
    "support_email": "string",
    "phone": "string"
  },
  "address": {
    "street": "string",
    "city": "string",
    "state": "string",
    "country": "string",
    "postal_code": "string"
  },
  "social_media": {
    "twitter": "string",
    "linkedin": "string",
    "facebook": "string",
    "instagram": "string"
  }
}
```

---

## Team & People Schemas

### Leadership Team

```json
{
  "company_name": "string",
  "leadership": [
    {
      "name": "string",
      "title": "string",
      "linkedin": "string",
      "bio": "string"
    }
  ]
}
```

### Person Profile

```json
{
  "name": "string",
  "current_role": "string",
  "current_company": "string",
  "previous_roles": [
    {
      "title": "string",
      "company": "string",
      "years": "string"
    }
  ],
  "education": ["string"],
  "linkedin": "string",
  "twitter": "string"
}
```

---

## News & Content Schemas

### News Articles

```json
{
  "topic": "string",
  "articles": [
    {
      "title": "string",
      "source": "string",
      "date": "string",
      "summary": "string",
      "url": "string"
    }
  ]
}
```

### Blog Posts

```json
{
  "blog_name": "string",
  "posts": [
    {
      "title": "string",
      "author": "string",
      "date": "string",
      "excerpt": "string",
      "url": "string",
      "tags": ["string"]
    }
  ]
}
```

---

## Technical Schemas

### API Documentation

```json
{
  "api_name": "string",
  "base_url": "string",
  "authentication": "string",
  "endpoints": [
    {
      "method": "string",
      "path": "string",
      "description": "string",
      "parameters": ["string"]
    }
  ],
  "rate_limits": "string"
}
```

### Tech Stack

```json
{
  "company_name": "string",
  "frontend": ["string"],
  "backend": ["string"],
  "databases": ["string"],
  "infrastructure": ["string"],
  "tools": ["string"]
}
```

---

## Job & Career Schemas

### Job Listings

```json
{
  "company_name": "string",
  "jobs": [
    {
      "title": "string",
      "department": "string",
      "location": "string",
      "type": "string",
      "salary_range": "string",
      "url": "string"
    }
  ],
  "total_openings": "number"
}
```

---

## Tips for Schema Design

1. **Keep it focused**: Only include fields you actually need
2. **Use descriptive names**: `founded_year` is clearer than `year`
3. **Match expected data**: Design schemas that match how data is typically structured
4. **Use arrays appropriately**: For lists of items (founders, features, etc.)
5. **Nest when logical**: Group related fields (contact info, address, etc.)
6. **Consider data availability**: Not all fields may be findable for every query
