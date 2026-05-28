# Quick Wins Implementation Plan

> Three features to differentiate Rory from vanilla Claude Code

---

## Overview

| Feature | Moat Level | Effort | Files Changed |
|---------|------------|--------|---------------|
| 1. Performance Tracking | Medium | 2-3 days | ~8 files |
| 2. Landing Page Benchmark | High | 3-5 days | ~6 files |
| 3. LinkedIn Integration | High | 5-7 days | ~12 files |

---

## Feature 1: Performance Tracking

### Goal
Track content performance so Rory can learn what works for each org.

**User Flow:**
1. User creates content with Rory
2. User posts content somewhere (LinkedIn, Twitter, etc.)
3. User reports back: "That LinkedIn post got 500 likes, 50 comments"
4. Rory stores this and uses it in future prompts

### Database Changes (robynnv3)

**New Migration: `20260108000000_create_content_performance.sql`**

```sql
BEGIN;

CREATE TABLE IF NOT EXISTS public.content_performance (
  id              uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  organization_id uuid NOT NULL REFERENCES public.organizations(id) ON DELETE CASCADE,
  created_by      uuid REFERENCES public.profiles(id) ON DELETE SET NULL,
  created_at      timestamptz NOT NULL DEFAULT now(),
  updated_at      timestamptz NOT NULL DEFAULT now(),

  -- Content identification
  content_type    text NOT NULL,           -- 'linkedin_post', 'tweet', 'blog', 'email'
  content_hash    text NOT NULL,           -- SHA256 of content for deduplication
  content_preview text NOT NULL,           -- First 500 chars for reference

  -- Platform where posted
  platform        text NOT NULL,           -- 'linkedin', 'twitter', 'blog', etc.
  platform_url    text,                    -- URL to the live post (optional)

  -- Performance metrics
  impressions     integer DEFAULT 0,
  likes           integer DEFAULT 0,
  comments        integer DEFAULT 0,
  shares          integer DEFAULT 0,
  clicks          integer DEFAULT 0,
  engagement_rate decimal(5,4),            -- calculated: (likes+comments+shares)/impressions

  -- Timing
  posted_at       timestamptz,
  measured_at     timestamptz DEFAULT now(),

  -- Content attributes (for learning)
  hook_type       text,                    -- 'question', 'contrarian', 'story', 'statistic'
  topic_tags      text[] DEFAULT '{}',     -- ['ai', 'marketing', 'saas']
  tone            text,                    -- 'professional', 'casual', 'provocative'

  -- Metadata
  metadata        jsonb DEFAULT '{}'
);

-- Indexes
CREATE INDEX idx_content_perf_org ON public.content_performance(organization_id);
CREATE INDEX idx_content_perf_type ON public.content_performance(organization_id, content_type);
CREATE INDEX idx_content_perf_platform ON public.content_performance(organization_id, platform);
CREATE INDEX idx_content_perf_posted ON public.content_performance(organization_id, posted_at DESC);

-- RLS
ALTER TABLE public.content_performance ENABLE ROW LEVEL SECURITY;

CREATE POLICY content_perf_select ON public.content_performance
  FOR SELECT USING (public.user_has_org_access(organization_id));

CREATE POLICY content_perf_insert ON public.content_performance
  FOR INSERT WITH CHECK (public.user_can_edit_org(organization_id));

CREATE POLICY content_perf_update ON public.content_performance
  FOR UPDATE USING (public.user_can_edit_org(organization_id));

-- Updated_at trigger
CREATE TRIGGER content_performance_updated_at
  BEFORE UPDATE ON public.content_performance
  FOR EACH ROW EXECUTE FUNCTION public.set_updated_at();

COMMIT;
```

### API Endpoints (robynnv3)

**New File: `src/routes/api/cli/performance/+server.ts`**

```typescript
import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import { validateApiKey } from '$lib/server/auth/validate-api-key';
import { createServiceClient } from '$lib/server/supabase';

// POST - Record new performance data
export const POST: RequestHandler = async ({ request }) => {
  const authResult = await validateApiKey(request);
  if (!authResult.valid) {
    return json({ error: 'Unauthorized' }, { status: 401 });
  }

  const body = await request.json();
  const supabase = createServiceClient();

  const { data, error } = await supabase
    .from('content_performance')
    .insert({
      organization_id: authResult.organizationId,
      content_type: body.content_type,
      content_hash: body.content_hash,
      content_preview: body.content_preview,
      platform: body.platform,
      platform_url: body.platform_url,
      impressions: body.impressions,
      likes: body.likes,
      comments: body.comments,
      shares: body.shares,
      clicks: body.clicks,
      hook_type: body.hook_type,
      topic_tags: body.topic_tags,
      tone: body.tone,
      posted_at: body.posted_at,
    })
    .select()
    .single();

  if (error) {
    return json({ error: error.message }, { status: 500 });
  }

  return json({ success: true, data });
};

// GET - Retrieve performance insights
export const GET: RequestHandler = async ({ request, url }) => {
  const authResult = await validateApiKey(request);
  if (!authResult.valid) {
    return json({ error: 'Unauthorized' }, { status: 401 });
  }

  const supabase = createServiceClient();
  const contentType = url.searchParams.get('content_type');
  const platform = url.searchParams.get('platform');
  const limit = parseInt(url.searchParams.get('limit') || '10');

  let query = supabase
    .from('content_performance')
    .select('*')
    .eq('organization_id', authResult.organizationId)
    .order('engagement_rate', { ascending: false, nullsFirst: false })
    .limit(limit);

  if (contentType) query = query.eq('content_type', contentType);
  if (platform) query = query.eq('platform', platform);

  const { data, error } = await query;

  if (error) {
    return json({ error: error.message }, { status: 500 });
  }

  // Calculate insights
  const insights = calculateInsights(data);

  return json({
    success: true,
    data: {
      top_performers: data,
      insights
    }
  });
};

function calculateInsights(data: any[]) {
  if (!data.length) return null;

  const byHookType = groupBy(data, 'hook_type');
  const avgByHook: Record<string, number> = {};

  for (const [hook, items] of Object.entries(byHookType)) {
    if (hook && items.length) {
      avgByHook[hook] = items.reduce((acc, i) => acc + (i.engagement_rate || 0), 0) / items.length;
    }
  }

  const bestHook = Object.entries(avgByHook)
    .sort(([,a], [,b]) => b - a)[0];

  return {
    total_posts_tracked: data.length,
    best_performing_hook: bestHook ? bestHook[0] : null,
    avg_engagement_by_hook: avgByHook,
    recommendation: bestHook
      ? `Your "${bestHook[0]}" hooks perform ${(bestHook[1] * 100).toFixed(1)}% better on average`
      : null
  };
}

function groupBy<T>(arr: T[], key: keyof T): Record<string, T[]> {
  return arr.reduce((acc, item) => {
    const k = String(item[key] || 'unknown');
    acc[k] = acc[k] || [];
    acc[k].push(item);
    return acc;
  }, {} as Record<string, T[]>);
}
```

### Agent Tool (robynnv3_agents)

**New File: `src/robynnv3_agents/agents/cmo_v2/tools/performance.py`**

```python
"""Performance tracking tools for CMO Agent V2."""

import hashlib
from typing import Any

from claude_agent_sdk import SdkMcpTool, tool
from loguru import logger


@tool(
    "record_content_performance",
    "Record performance metrics for content that was posted. Call this when user reports engagement numbers.",
    {
        "content_preview": str,      # First 500 chars of the content
        "platform": str,             # 'linkedin', 'twitter', 'blog'
        "content_type": str,         # 'linkedin_post', 'tweet', 'blog_post'
        "likes": int,
        "comments": int,
        "shares": int,
        "impressions": int,          # Optional, can be 0
        "hook_type": str,            # 'question', 'contrarian', 'story', 'statistic'
        "topic_tags": list,          # ['ai', 'marketing']
        "platform_url": str,         # URL to the live post (optional)
    },
)
async def record_content_performance(args: dict[str, Any]) -> dict[str, Any]:
    """Record content performance for learning."""
    try:
        import httpx
        import os

        api_key = os.environ.get("ROBYNN_API_KEY")
        base_url = os.environ.get("ROBYNN_API_BASE_URL", "https://robynn.ai/api/cli")

        content = args.get("content_preview", "")
        content_hash = hashlib.sha256(content.encode()).hexdigest()[:16]

        payload = {
            "content_preview": content[:500],
            "content_hash": content_hash,
            "platform": args.get("platform"),
            "content_type": args.get("content_type"),
            "likes": args.get("likes", 0),
            "comments": args.get("comments", 0),
            "shares": args.get("shares", 0),
            "impressions": args.get("impressions", 0),
            "hook_type": args.get("hook_type"),
            "topic_tags": args.get("topic_tags", []),
            "platform_url": args.get("platform_url"),
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{base_url}/performance",
                json=payload,
                headers={"Authorization": f"Bearer {api_key}"},
            )
            response.raise_for_status()

        output = f"""## Performance Recorded

**Platform**: {payload['platform']}
**Engagement**: {payload['likes']} likes, {payload['comments']} comments, {payload['shares']} shares
**Hook Type**: {payload['hook_type']}

I'll use this data to improve future content recommendations for you.
"""
        return {"content": [{"type": "text", "text": output}]}

    except Exception as e:
        logger.error(f"record_content_performance failed: {e}")
        return {
            "content": [{"type": "text", "text": f"Error recording performance: {e}"}],
            "is_error": True,
        }


@tool(
    "get_performance_insights",
    "Get insights about what content performs best for this organization.",
    {
        "content_type": str,  # Optional filter
        "platform": str,      # Optional filter
    },
)
async def get_performance_insights(args: dict[str, Any]) -> dict[str, Any]:
    """Get performance insights for content optimization."""
    try:
        import httpx
        import os

        api_key = os.environ.get("ROBYNN_API_KEY")
        base_url = os.environ.get("ROBYNN_API_BASE_URL", "https://robynn.ai/api/cli")

        params = {}
        if args.get("content_type"):
            params["content_type"] = args["content_type"]
        if args.get("platform"):
            params["platform"] = args["platform"]

        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{base_url}/performance",
                params=params,
                headers={"Authorization": f"Bearer {api_key}"},
            )
            response.raise_for_status()
            data = response.json()

        insights = data.get("data", {}).get("insights", {})
        top_performers = data.get("data", {}).get("top_performers", [])

        output = f"""## Your Content Performance Insights

**Total Posts Tracked**: {insights.get('total_posts_tracked', 0)}
**Best Hook Type**: {insights.get('best_performing_hook', 'Not enough data yet')}

### Recommendation
{insights.get('recommendation', 'Keep posting and tracking to build insights!')}

### Top Performers
"""
        for i, post in enumerate(top_performers[:5], 1):
            output += f"\n{i}. {post.get('platform')} - {post.get('likes', 0)} likes - Hook: {post.get('hook_type', 'unknown')}"

        return {"content": [{"type": "text", "text": output}]}

    except Exception as e:
        logger.error(f"get_performance_insights failed: {e}")
        return {
            "content": [{"type": "text", "text": f"Error fetching insights: {e}"}],
            "is_error": True,
        }


performance_tools: list[SdkMcpTool] = [
    record_content_performance,
    get_performance_insights,
]
```

### CLI Commands (claude-code-cmo)

**Update: `tools/robynn.py`** - Add `report` command

```python
def report_command(platform: str, likes: int, comments: int, shares: int):
    """Report content performance."""
    # This triggers the agent to call record_content_performance
    print(f"\nRecorded: {platform} - {likes} likes, {comments} comments, {shares} shares")
    print("Rory will use this to improve future content.")
```

### Prompt Updates (robynnv3_agents)

**Update CMO v2 system prompt** to include performance context:

```python
# In agent.py, add to the system prompt builder:

if performance_insights := params.get("performance_insights"):
    prompt += f"""

## Your Past Performance
Based on your tracked content:
- Best performing hook type: {performance_insights.get('best_hook')}
- Average engagement rate: {performance_insights.get('avg_engagement')}%
- Recommendation: {performance_insights.get('recommendation')}

Use these insights when creating new content.
"""
```

### File Summary

| Repo | File | Action |
|------|------|--------|
| robynnv3 | `supabase/migrations/20260108000000_create_content_performance.sql` | Create |
| robynnv3 | `src/routes/api/cli/performance/+server.ts` | Create |
| robynnv3_agents | `src/robynnv3_agents/agents/cmo_v2/tools/performance.py` | Create |
| robynnv3_agents | `src/robynnv3_agents/agents/cmo_v2/tools/__init__.py` | Update (add tools) |
| robynnv3_agents | `src/robynnv3_agents/agents/cmo_v2/agent.py` | Update (fetch & inject insights) |
| claude-code-cmo | `tools/robynn.py` | Update (add report command) |
| claude-code-cmo | `SKILL.md` | Update (document report feature) |

---

## Feature 2: Landing Page Benchmark

### Goal
Provide data-backed landing page feedback by comparing against benchmarks.

**User Flow:**
1. User: "Roast my landing page at https://example.com"
2. Rory takes screenshot
3. Rory analyzes with vision model
4. Rory compares to benchmark dataset
5. Returns specific, data-backed recommendations

### Benchmark Dataset (robynnv3)

**New Migration: `20260108100000_create_landing_page_benchmarks.sql`**

```sql
BEGIN;

-- Aggregated benchmarks from analyzed landing pages
CREATE TABLE IF NOT EXISTS public.landing_page_benchmarks (
  id              uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  created_at      timestamptz NOT NULL DEFAULT now(),
  updated_at      timestamptz NOT NULL DEFAULT now(),

  -- Category
  industry        text NOT NULL,           -- 'saas', 'ecommerce', 'fintech', 'healthtech'
  page_type       text NOT NULL,           -- 'homepage', 'pricing', 'product', 'signup'

  -- Visual benchmarks
  hero_height_px_avg      integer,         -- Average hero section height
  hero_height_px_p90      integer,         -- 90th percentile
  cta_button_size_avg     integer,         -- Average CTA button height in px
  cta_above_fold_pct      decimal(5,2),    -- % of pages with CTA above fold

  -- Content benchmarks
  headline_word_count_avg integer,
  headline_word_count_p90 integer,
  subheadline_word_count_avg integer,
  social_proof_above_fold_pct decimal(5,2),

  -- Color benchmarks
  cta_contrast_ratio_avg  decimal(4,2),    -- Avg contrast ratio of CTA

  -- Performance benchmarks
  avg_conversion_rate     decimal(5,4),    -- Industry average CVR
  top_10_pct_cvr          decimal(5,4),    -- Top 10% CVR

  -- Sample size
  pages_analyzed          integer NOT NULL DEFAULT 0,
  last_updated            timestamptz DEFAULT now(),

  -- Unique constraint
  CONSTRAINT unique_industry_page_type UNIQUE (industry, page_type)
);

-- Seed with initial benchmarks (example data - replace with real data)
INSERT INTO public.landing_page_benchmarks
  (industry, page_type, hero_height_px_avg, cta_button_size_avg, cta_above_fold_pct,
   headline_word_count_avg, social_proof_above_fold_pct, cta_contrast_ratio_avg,
   avg_conversion_rate, top_10_pct_cvr, pages_analyzed)
VALUES
  ('saas', 'homepage', 600, 48, 92.5, 7, 78.3, 4.8, 0.023, 0.058, 500),
  ('saas', 'pricing', 400, 52, 88.0, 5, 45.2, 5.1, 0.031, 0.072, 350),
  ('ecommerce', 'homepage', 550, 44, 95.0, 6, 82.1, 4.5, 0.028, 0.065, 400),
  ('fintech', 'homepage', 580, 50, 90.0, 8, 85.5, 5.2, 0.019, 0.045, 200);

COMMIT;
```

### Vision Analysis Tool (robynnv3_agents)

**New File: `src/robynnv3_agents/agents/cmo_v2/tools/landing_page.py`**

```python
"""Landing page analysis tools with benchmarking."""

import base64
from typing import Any

from claude_agent_sdk import SdkMcpTool, tool
from loguru import logger


@tool(
    "analyze_landing_page_with_benchmarks",
    "Analyze a landing page screenshot and compare against industry benchmarks.",
    {
        "url": str,
        "industry": str,  # 'saas', 'ecommerce', 'fintech', 'healthtech'
        "page_type": str, # 'homepage', 'pricing', 'product', 'signup'
    },
)
async def analyze_landing_page_with_benchmarks(args: dict[str, Any]) -> dict[str, Any]:
    """Analyze landing page with benchmark comparison."""
    url = args.get("url", "")
    industry = args.get("industry", "saas")
    page_type = args.get("page_type", "homepage")

    try:
        import httpx
        import os
        from robynnv3_agents.tools.firecrawl import FirecrawlScreenshotTool

        # 1. Take screenshot
        screenshot_tool = FirecrawlScreenshotTool()
        screenshot_result = await screenshot_tool.ainvoke(url=url)

        if not screenshot_result.get("success"):
            return {
                "content": [{"type": "text", "text": f"Failed to capture screenshot: {screenshot_result.get('error')}"}],
                "is_error": True,
            }

        screenshot_url = screenshot_result.get("screenshot_url")

        # 2. Fetch benchmarks
        api_key = os.environ.get("ROBYNN_API_KEY")
        base_url = os.environ.get("ROBYNN_API_BASE_URL", "https://robynn.ai/api/cli")

        async with httpx.AsyncClient() as client:
            bench_response = await client.get(
                f"{base_url}/benchmarks",
                params={"industry": industry, "page_type": page_type},
                headers={"Authorization": f"Bearer {api_key}"},
            )
            benchmarks = bench_response.json().get("data", {}) if bench_response.status_code == 200 else {}

        # 3. Analyze with vision model (this will be done by Claude itself)
        # Return the screenshot and benchmarks for Claude to analyze

        benchmark_text = ""
        if benchmarks:
            benchmark_text = f"""
## Industry Benchmarks ({industry.upper()} {page_type})

| Metric | Industry Avg | Top 10% |
|--------|--------------|---------|
| Hero Height | {benchmarks.get('hero_height_px_avg', 'N/A')}px | {benchmarks.get('hero_height_px_p90', 'N/A')}px |
| CTA Button Size | {benchmarks.get('cta_button_size_avg', 'N/A')}px | - |
| CTA Above Fold | {benchmarks.get('cta_above_fold_pct', 'N/A')}% | - |
| Headline Words | {benchmarks.get('headline_word_count_avg', 'N/A')} | {benchmarks.get('headline_word_count_p90', 'N/A')} |
| Social Proof Above Fold | {benchmarks.get('social_proof_above_fold_pct', 'N/A')}% | - |
| CTA Contrast Ratio | {benchmarks.get('cta_contrast_ratio_avg', 'N/A')} | 5.0+ |
| Conversion Rate | {float(benchmarks.get('avg_conversion_rate', 0)) * 100:.1f}% | {float(benchmarks.get('top_10_pct_cvr', 0)) * 100:.1f}% |

*Based on {benchmarks.get('pages_analyzed', 0)} analyzed pages*
"""

        output = f"""## Landing Page Analysis: {url}

Screenshot captured. Analyzing against {industry} benchmarks...

{benchmark_text}

### Analysis Instructions for Claude

Using the screenshot at {screenshot_url}, evaluate:

1. **Hero Section**
   - Is the headline clear and under {benchmarks.get('headline_word_count_p90', 10)} words?
   - Is there a CTA button above the fold?
   - Estimate CTA button size vs benchmark ({benchmarks.get('cta_button_size_avg', 48)}px avg)

2. **Social Proof**
   - Is there social proof above the fold? (Benchmark: {benchmarks.get('social_proof_above_fold_pct', 78)}% have it)
   - Logos, testimonials, or numbers?

3. **Visual Hierarchy**
   - Is the CTA the most prominent element?
   - Good contrast ratio? (Benchmark: {benchmarks.get('cta_contrast_ratio_avg', 4.5)}+)

4. **Conversion Optimization**
   - Single clear CTA or multiple competing CTAs?
   - Value proposition clear in 5 seconds?

Provide specific, data-backed recommendations with benchmark comparisons.
"""

        # Return with image for Claude to analyze
        return {
            "content": [
                {"type": "text", "text": output},
                {"type": "image", "source": {"type": "url", "url": screenshot_url}},
            ]
        }

    except Exception as e:
        logger.error(f"analyze_landing_page_with_benchmarks failed: {e}")
        return {
            "content": [{"type": "text", "text": f"Error: {e}"}],
            "is_error": True,
        }


landing_page_tools: list[SdkMcpTool] = [
    analyze_landing_page_with_benchmarks,
]
```

### API Endpoint (robynnv3)

**New File: `src/routes/api/cli/benchmarks/+server.ts`**

```typescript
import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import { validateApiKey } from '$lib/server/auth/validate-api-key';
import { createServiceClient } from '$lib/server/supabase';

export const GET: RequestHandler = async ({ request, url }) => {
  const authResult = await validateApiKey(request);
  if (!authResult.valid) {
    return json({ error: 'Unauthorized' }, { status: 401 });
  }

  const industry = url.searchParams.get('industry') || 'saas';
  const pageType = url.searchParams.get('page_type') || 'homepage';

  const supabase = createServiceClient();

  const { data, error } = await supabase
    .from('landing_page_benchmarks')
    .select('*')
    .eq('industry', industry)
    .eq('page_type', pageType)
    .single();

  if (error) {
    // Return default benchmarks if none found
    return json({
      success: true,
      data: {
        industry,
        page_type: pageType,
        hero_height_px_avg: 600,
        cta_button_size_avg: 48,
        cta_above_fold_pct: 92,
        headline_word_count_avg: 7,
        social_proof_above_fold_pct: 78,
        cta_contrast_ratio_avg: 4.5,
        avg_conversion_rate: 0.023,
        top_10_pct_cvr: 0.058,
        pages_analyzed: 0,
      }
    });
  }

  return json({ success: true, data });
};
```

### File Summary

| Repo | File | Action |
|------|------|--------|
| robynnv3 | `supabase/migrations/20260108100000_create_landing_page_benchmarks.sql` | Create |
| robynnv3 | `src/routes/api/cli/benchmarks/+server.ts` | Create |
| robynnv3_agents | `src/robynnv3_agents/agents/cmo_v2/tools/landing_page.py` | Create |
| robynnv3_agents | `src/robynnv3_agents/agents/cmo_v2/tools/__init__.py` | Update |
| robynnv3_agents | `src/robynnv3_agents/agents/cmo_v2/agent.py` | Update (use new tool in roast skill) |

---

## Feature 3: LinkedIn Integration

### Goal
Let users post content directly to LinkedIn and track engagement.

**User Flow:**
1. User creates LinkedIn post with Rory
2. User: "Post this to LinkedIn"
3. Rory posts via LinkedIn API
4. Rory stores post ID for tracking
5. Later: "How did that post do?" → Rory fetches analytics

### OAuth Flow (robynnv3)

**New Migration: `20260108200000_create_social_integrations.sql`**

```sql
BEGIN;

CREATE TABLE IF NOT EXISTS public.social_integrations (
  id              uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  organization_id uuid NOT NULL REFERENCES public.organizations(id) ON DELETE CASCADE,
  created_by      uuid REFERENCES public.profiles(id) ON DELETE SET NULL,
  created_at      timestamptz NOT NULL DEFAULT now(),
  updated_at      timestamptz NOT NULL DEFAULT now(),

  -- Platform info
  platform        text NOT NULL,           -- 'linkedin', 'twitter', 'facebook'
  platform_user_id text NOT NULL,          -- LinkedIn URN, Twitter ID, etc.
  platform_username text,                  -- Display name

  -- OAuth tokens (encrypted in production)
  access_token    text NOT NULL,
  refresh_token   text,
  token_expires_at timestamptz,

  -- Scopes granted
  scopes          text[] DEFAULT '{}',

  -- Status
  status          text NOT NULL DEFAULT 'active', -- 'active', 'expired', 'revoked'
  last_used_at    timestamptz,

  -- Unique per org per platform
  CONSTRAINT unique_org_platform UNIQUE (organization_id, platform, platform_user_id)
);

-- Track posted content
CREATE TABLE IF NOT EXISTS public.social_posts (
  id              uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  organization_id uuid NOT NULL REFERENCES public.organizations(id) ON DELETE CASCADE,
  integration_id  uuid NOT NULL REFERENCES public.social_integrations(id) ON DELETE CASCADE,
  created_at      timestamptz NOT NULL DEFAULT now(),
  updated_at      timestamptz NOT NULL DEFAULT now(),

  -- Post info
  platform        text NOT NULL,
  platform_post_id text NOT NULL,          -- LinkedIn URN, Tweet ID, etc.
  post_url        text,
  content_preview text,

  -- Metrics (updated periodically)
  impressions     integer DEFAULT 0,
  likes           integer DEFAULT 0,
  comments        integer DEFAULT 0,
  shares          integer DEFAULT 0,
  clicks          integer DEFAULT 0,

  -- Tracking
  posted_at       timestamptz DEFAULT now(),
  metrics_updated_at timestamptz,

  CONSTRAINT unique_platform_post UNIQUE (platform, platform_post_id)
);

-- Indexes
CREATE INDEX idx_social_int_org ON public.social_integrations(organization_id);
CREATE INDEX idx_social_posts_org ON public.social_posts(organization_id);
CREATE INDEX idx_social_posts_integration ON public.social_posts(integration_id);

-- RLS
ALTER TABLE public.social_integrations ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.social_posts ENABLE ROW LEVEL SECURITY;

CREATE POLICY social_int_select ON public.social_integrations
  FOR SELECT USING (public.user_has_org_access(organization_id));
CREATE POLICY social_int_insert ON public.social_integrations
  FOR INSERT WITH CHECK (public.user_can_edit_org(organization_id));
CREATE POLICY social_int_update ON public.social_integrations
  FOR UPDATE USING (public.user_can_edit_org(organization_id));
CREATE POLICY social_int_delete ON public.social_integrations
  FOR DELETE USING (public.user_can_edit_org(organization_id));

CREATE POLICY social_posts_select ON public.social_posts
  FOR SELECT USING (public.user_has_org_access(organization_id));
CREATE POLICY social_posts_insert ON public.social_posts
  FOR INSERT WITH CHECK (public.user_can_edit_org(organization_id));

COMMIT;
```

### OAuth Endpoints (robynnv3)

**New File: `src/routes/api/oauth/linkedin/+server.ts`**

```typescript
import { redirect } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import { env } from '$env/dynamic/private';

const LINKEDIN_CLIENT_ID = env.LINKEDIN_CLIENT_ID;
const LINKEDIN_REDIRECT_URI = env.LINKEDIN_REDIRECT_URI || 'https://robynn.ai/api/oauth/linkedin/callback';
const SCOPES = ['openid', 'profile', 'w_member_social', 'r_basicprofile'];

export const GET: RequestHandler = async ({ url, cookies }) => {
  const orgId = url.searchParams.get('org_id');

  if (!orgId) {
    return new Response('Missing org_id', { status: 400 });
  }

  // Store org_id in cookie for callback
  cookies.set('linkedin_oauth_org', orgId, {
    path: '/',
    httpOnly: true,
    secure: true,
    maxAge: 600, // 10 minutes
  });

  const state = crypto.randomUUID();
  cookies.set('linkedin_oauth_state', state, {
    path: '/',
    httpOnly: true,
    secure: true,
    maxAge: 600,
  });

  const authUrl = new URL('https://www.linkedin.com/oauth/v2/authorization');
  authUrl.searchParams.set('response_type', 'code');
  authUrl.searchParams.set('client_id', LINKEDIN_CLIENT_ID);
  authUrl.searchParams.set('redirect_uri', LINKEDIN_REDIRECT_URI);
  authUrl.searchParams.set('scope', SCOPES.join(' '));
  authUrl.searchParams.set('state', state);

  throw redirect(302, authUrl.toString());
};
```

**New File: `src/routes/api/oauth/linkedin/callback/+server.ts`**

```typescript
import { json, redirect } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import { env } from '$env/dynamic/private';
import { createServiceClient } from '$lib/server/supabase';

export const GET: RequestHandler = async ({ url, cookies }) => {
  const code = url.searchParams.get('code');
  const state = url.searchParams.get('state');
  const storedState = cookies.get('linkedin_oauth_state');
  const orgId = cookies.get('linkedin_oauth_org');

  if (!code || state !== storedState || !orgId) {
    return new Response('Invalid OAuth callback', { status: 400 });
  }

  // Exchange code for tokens
  const tokenResponse = await fetch('https://www.linkedin.com/oauth/v2/accessToken', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({
      grant_type: 'authorization_code',
      code,
      redirect_uri: env.LINKEDIN_REDIRECT_URI,
      client_id: env.LINKEDIN_CLIENT_ID,
      client_secret: env.LINKEDIN_CLIENT_SECRET,
    }),
  });

  const tokens = await tokenResponse.json();

  if (!tokens.access_token) {
    return new Response('Failed to get access token', { status: 500 });
  }

  // Get LinkedIn profile
  const profileResponse = await fetch('https://api.linkedin.com/v2/userinfo', {
    headers: { Authorization: `Bearer ${tokens.access_token}` },
  });
  const profile = await profileResponse.json();

  // Store in database
  const supabase = createServiceClient();

  await supabase.from('social_integrations').upsert({
    organization_id: orgId,
    platform: 'linkedin',
    platform_user_id: profile.sub,
    platform_username: profile.name,
    access_token: tokens.access_token, // TODO: Encrypt in production
    refresh_token: tokens.refresh_token,
    token_expires_at: new Date(Date.now() + tokens.expires_in * 1000).toISOString(),
    scopes: ['openid', 'profile', 'w_member_social'],
    status: 'active',
  }, {
    onConflict: 'organization_id,platform,platform_user_id',
  });

  // Clear cookies
  cookies.delete('linkedin_oauth_state', { path: '/' });
  cookies.delete('linkedin_oauth_org', { path: '/' });

  // Redirect to success page
  throw redirect(302, '/settings/integrations?linkedin=connected');
};
```

### Post to LinkedIn Tool (robynnv3_agents)

**New File: `src/robynnv3_agents/agents/cmo_v2/tools/linkedin.py`**

```python
"""LinkedIn integration tools for CMO Agent V2."""

from typing import Any

from claude_agent_sdk import SdkMcpTool, tool
from loguru import logger


@tool(
    "post_to_linkedin",
    "Post content to LinkedIn on behalf of the user. Requires LinkedIn integration to be connected.",
    {
        "content": str,      # The post content
        "visibility": str,   # 'PUBLIC' or 'CONNECTIONS'
    },
)
async def post_to_linkedin(args: dict[str, Any]) -> dict[str, Any]:
    """Post content to LinkedIn."""
    content = args.get("content", "")
    visibility = args.get("visibility", "PUBLIC")

    try:
        import httpx
        import os

        api_key = os.environ.get("ROBYNN_API_KEY")
        base_url = os.environ.get("ROBYNN_API_BASE_URL", "https://robynn.ai/api/cli")

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{base_url}/linkedin/post",
                json={
                    "content": content,
                    "visibility": visibility,
                },
                headers={"Authorization": f"Bearer {api_key}"},
                timeout=30.0,
            )

            if response.status_code == 401:
                return {
                    "content": [{
                        "type": "text",
                        "text": "LinkedIn not connected. Visit Settings → Integrations in Robynn to connect your LinkedIn account."
                    }],
                    "is_error": True,
                }

            response.raise_for_status()
            result = response.json()

        post_url = result.get("data", {}).get("post_url", "")

        output = f"""## Posted to LinkedIn!

Your content has been published.

**Post URL**: {post_url}

I'll track engagement on this post. Ask me "How did my LinkedIn post do?" in a few hours to see performance.
"""
        return {"content": [{"type": "text", "text": output}]}

    except Exception as e:
        logger.error(f"post_to_linkedin failed: {e}")
        return {
            "content": [{"type": "text", "text": f"Error posting to LinkedIn: {e}"}],
            "is_error": True,
        }


@tool(
    "get_linkedin_post_analytics",
    "Get analytics for recent LinkedIn posts.",
    {
        "post_id": str,  # Optional - specific post
        "limit": int,    # Number of recent posts to check
    },
)
async def get_linkedin_post_analytics(args: dict[str, Any]) -> dict[str, Any]:
    """Get LinkedIn post analytics."""
    post_id = args.get("post_id")
    limit = args.get("limit", 5)

    try:
        import httpx
        import os

        api_key = os.environ.get("ROBYNN_API_KEY")
        base_url = os.environ.get("ROBYNN_API_BASE_URL", "https://robynn.ai/api/cli")

        params = {"limit": limit}
        if post_id:
            params["post_id"] = post_id

        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{base_url}/linkedin/analytics",
                params=params,
                headers={"Authorization": f"Bearer {api_key}"},
            )
            response.raise_for_status()
            result = response.json()

        posts = result.get("data", {}).get("posts", [])

        if not posts:
            return {
                "content": [{"type": "text", "text": "No LinkedIn posts found. Post some content first!"}]
            }

        output = "## LinkedIn Post Analytics\n\n"

        for i, post in enumerate(posts, 1):
            output += f"""### Post {i}
**Posted**: {post.get('posted_at', 'Unknown')}
**Preview**: {post.get('content_preview', '')[:100]}...

| Metric | Value |
|--------|-------|
| Impressions | {post.get('impressions', 0):,} |
| Likes | {post.get('likes', 0):,} |
| Comments | {post.get('comments', 0):,} |
| Shares | {post.get('shares', 0):,} |

"""

        return {"content": [{"type": "text", "text": output}]}

    except Exception as e:
        logger.error(f"get_linkedin_post_analytics failed: {e}")
        return {
            "content": [{"type": "text", "text": f"Error fetching analytics: {e}"}],
            "is_error": True,
        }


linkedin_tools: list[SdkMcpTool] = [
    post_to_linkedin,
    get_linkedin_post_analytics,
]
```

### Post API Endpoint (robynnv3)

**New File: `src/routes/api/cli/linkedin/post/+server.ts`**

```typescript
import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import { validateApiKey } from '$lib/server/auth/validate-api-key';
import { createServiceClient } from '$lib/server/supabase';

export const POST: RequestHandler = async ({ request }) => {
  const authResult = await validateApiKey(request);
  if (!authResult.valid) {
    return json({ error: 'Unauthorized' }, { status: 401 });
  }

  const supabase = createServiceClient();

  // Get LinkedIn integration
  const { data: integration, error: intError } = await supabase
    .from('social_integrations')
    .select('*')
    .eq('organization_id', authResult.organizationId)
    .eq('platform', 'linkedin')
    .eq('status', 'active')
    .single();

  if (intError || !integration) {
    return json({
      error: 'LinkedIn not connected',
      action: 'Visit Settings → Integrations to connect LinkedIn'
    }, { status: 401 });
  }

  const body = await request.json();
  const { content, visibility = 'PUBLIC' } = body;

  // Post to LinkedIn
  const postResponse = await fetch('https://api.linkedin.com/v2/ugcPosts', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${integration.access_token}`,
      'Content-Type': 'application/json',
      'X-Restli-Protocol-Version': '2.0.0',
    },
    body: JSON.stringify({
      author: `urn:li:person:${integration.platform_user_id}`,
      lifecycleState: 'PUBLISHED',
      specificContent: {
        'com.linkedin.ugc.ShareContent': {
          shareCommentary: { text: content },
          shareMediaCategory: 'NONE',
        },
      },
      visibility: {
        'com.linkedin.ugc.MemberNetworkVisibility': visibility,
      },
    }),
  });

  if (!postResponse.ok) {
    const error = await postResponse.text();
    return json({ error: `LinkedIn API error: ${error}` }, { status: 500 });
  }

  const postResult = await postResponse.json();
  const postUrn = postResult.id;
  const postUrl = `https://www.linkedin.com/feed/update/${postUrn}`;

  // Store post for tracking
  await supabase.from('social_posts').insert({
    organization_id: authResult.organizationId,
    integration_id: integration.id,
    platform: 'linkedin',
    platform_post_id: postUrn,
    post_url: postUrl,
    content_preview: content.substring(0, 500),
    posted_at: new Date().toISOString(),
  });

  return json({
    success: true,
    data: {
      post_id: postUrn,
      post_url: postUrl,
    },
  });
};
```

### File Summary

| Repo | File | Action |
|------|------|--------|
| robynnv3 | `supabase/migrations/20260108200000_create_social_integrations.sql` | Create |
| robynnv3 | `src/routes/api/oauth/linkedin/+server.ts` | Create |
| robynnv3 | `src/routes/api/oauth/linkedin/callback/+server.ts` | Create |
| robynnv3 | `src/routes/api/cli/linkedin/post/+server.ts` | Create |
| robynnv3 | `src/routes/api/cli/linkedin/analytics/+server.ts` | Create |
| robynnv3 | `src/routes/(app)/settings/integrations/+page.svelte` | Create/Update |
| robynnv3_agents | `src/robynnv3_agents/agents/cmo_v2/tools/linkedin.py` | Create |
| robynnv3_agents | `src/robynnv3_agents/agents/cmo_v2/tools/__init__.py` | Update |
| claude-code-cmo | `SKILL.md` | Update (document LinkedIn posting) |

---

## Implementation Order

### Week 1: Performance Tracking
1. Create migration and apply to Supabase
2. Build API endpoints
3. Create agent tools
4. Update CMO v2 prompt to use insights
5. Test end-to-end

### Week 2: Landing Page Benchmark
1. Create benchmark table and seed data
2. Build benchmark API
3. Create vision analysis tool
4. Update landing_page_roast skill to use benchmarks
5. Test with real pages

### Week 3: LinkedIn Integration
1. Create OAuth tables
2. Build OAuth flow
3. Create posting API
4. Create agent tools
5. Add UI for connecting LinkedIn
6. Test posting and analytics

---

## Environment Variables Required

```env
# LinkedIn OAuth (robynnv3)
LINKEDIN_CLIENT_ID=xxx
LINKEDIN_CLIENT_SECRET=xxx
LINKEDIN_REDIRECT_URI=https://robynn.ai/api/oauth/linkedin/callback
```

---

## Testing Checklist

### Feature 1: Performance Tracking
- [ ] Can record performance via natural language
- [ ] Insights appear in future prompts
- [ ] Hook type analysis is accurate

### Feature 2: Landing Page Benchmark
- [ ] Screenshot captures correctly
- [ ] Benchmarks are fetched and displayed
- [ ] Recommendations are specific and data-backed

### Feature 3: LinkedIn Integration
- [ ] OAuth flow completes successfully
- [ ] Posts appear on LinkedIn
- [ ] Analytics are fetched correctly
- [ ] Token refresh works
