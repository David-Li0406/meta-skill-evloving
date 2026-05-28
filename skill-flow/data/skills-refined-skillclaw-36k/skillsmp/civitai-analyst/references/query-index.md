# Query Index

Quick reference for available SQL query templates.

## Query Catalog

| Query | Use Case | File |
|-------|----------|------|
| Weekly Feedback Stats | Weekly summary by uploader with engagement totals | `queries/weekly-feedback-stats.sql` |
| Top Performing Assets | Best videos ranked by engagement | `queries/top-performing-assets.sql` |
| Week-over-Week | Compare current vs previous week | `queries/week-over-week-comparison.sql` |
| Tag Performance | Analyze which tags drive engagement | `queries/tag-performance.sql` |
| Video Comparison | Compare specific videos by rank or ID | `queries/video-comparison.sql` |
| Quality vs Engagement | Correlate quality_score with reactions | `queries/quality-vs-engagement.sql` |
| Content Themes | Analyze themes from descriptions/prompts | `queries/content-theme-analysis.sql` |

## Parameter Reference

### Date Parameters

Use PostgreSQL timestamptz format: `'2025-01-06T00:00:00Z'`

**Calendar Week Calculation (Monday-Sunday):**
- "This week" = Current Monday 00:00:00Z to next Monday 00:00:00Z
- "Last week" = Previous Monday 00:00:00Z to current Monday 00:00:00Z

**Example for week of Jan 6-12, 2025:**
```sql
start_date = '2025-01-06T00:00:00Z'
end_date = '2025-01-13T00:00:00Z'
```

### Common Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `$1`, `$2` | timestamptz | Date range (start, end) | Required |
| `$3` | text | civitai_account | `'c29'` |
| on_behalf_of | text | User first name | From session |

## Query Details

### 1. Weekly Feedback Stats
**File:** `queries/weekly-feedback-stats.sql`

**Use when:** User asks for weekly summary, overall stats, engagement breakdown by uploader.

**Parameters:**
- `$1`: start_date (inclusive)
- `$2`: end_date (exclusive)
- `$3`: civitai_account

**Returns:** Uploader, total assets/posts, all engagement metrics, engagement rates.

---

### 2. Top Performing Assets
**File:** `queries/top-performing-assets.sql`

**Use when:** User asks for best videos, top performers, highest engagement content.

**Parameters:**
- `$1`: start_date (inclusive)
- `$2`: end_date (exclusive)
- `$3`: civitai_account

**Returns:** Top 20 assets with Civitai URLs, all engagement metrics, ranked by total engagement.

---

### 3. Week-over-Week Comparison
**File:** `queries/week-over-week-comparison.sql`

**Use when:** User asks to compare weeks, growth analysis, trend over time.

**Parameters:**
- `$1`: last_week_start
- `$2`: last_week_end
- `$3`: prev_week_start
- `$4`: prev_week_end
- `$5`: civitai_account

**Returns:** Both weeks' metrics, changes, growth percentages, trend indicator.

---

### 4. Tag Performance
**File:** `queries/tag-performance.sql`

**Use when:** User asks which tags perform best, content category analysis, what themes work.

**Parameters:**
- `$1`: start_date (inclusive)
- `$2`: end_date (exclusive)
- `$3`: on_behalf_of (user name)

**Returns:** Tags ranked by engagement, video count, avg quality score per tag.

---

### 5. Video Comparison
**File:** `queries/video-comparison.sql`

**Use when:** User asks to compare specific videos, "what do rank 2 and 9 have in common", differences between videos.

**Parameters:**
- `$1`: start_date (inclusive)
- `$2`: end_date (exclusive)
- `$3`: on_behalf_of (user name)
- `$4`, `$5`: ranks to compare (e.g., 2, 9)

**Returns:** Full details of both videos for comparison.

---

### 6. Quality vs Engagement
**File:** `queries/quality-vs-engagement.sql`

**Use when:** User asks about quality score impact, whether high quality means more engagement.

**Parameters:**
- `$1`: start_date (inclusive)
- `$2`: end_date (exclusive)
- `$3`: on_behalf_of (user name)

**Returns:** Quality score buckets with avg engagement, identifies optimal quality ranges.

---

### 7. Content Theme Analysis
**File:** `queries/content-theme-analysis.sql`

**Use when:** User asks what content themes work, topic analysis, description patterns.

**Parameters:**
- `$1`: start_date (inclusive)
- `$2`: end_date (exclusive)
- `$3`: on_behalf_of (user name)

**Returns:** Videos with descriptions, inferred prompts, tags, and engagement for theme analysis.

## Customization Guide

**Adding filters:**
```sql
-- Filter by specific user
AND ast.on_behalf_of = 'Richard'

-- Filter by asset type
AND a.asset_type = 'video'

-- Filter by minimum engagement
HAVING SUM(engagement) >= 10
```

**Changing result count:**
```sql
LIMIT 50  -- More results
LIMIT 5   -- Fewer results
```

**Adding video_analysis data:**
```sql
JOIN civitai.video_analysis va ON va.asset_id = a.id
-- Then select: va.tags, va.quality_score, va.description
```
