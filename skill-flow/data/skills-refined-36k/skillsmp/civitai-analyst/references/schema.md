# Civitai Database Schema

All tables are in the **`civitai`** schema. Always use full qualification: `civitai.table_name`.

## Tables Overview

| Table | Purpose |
|-------|---------|
| `civitai.assets` | Core asset records (videos/images) with civitai_id for links |
| `civitai.asset_stats` | Engagement metrics (likes, hearts, comments, etc.) |
| `civitai.video_analysis` | AI-generated video analysis (tags, description, quality) |
| `civitai.civitai_posts` | Post metadata with separate civitai_id for post links |
| `civitai.prompts` | Generation prompts |
| `civitai.events` | Audit/change log |

## Key Relationships

```
asset_stats.asset_id    → assets.id
asset_stats.post_id     → civitai_posts.id
video_analysis.asset_id → assets.id
assets.input_prompt_id  → prompts.id
assets.output_prompt_id → prompts.id
```

## Table: civitai.assets

Core asset records for videos and images.

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| id | bigint | NO | Primary key |
| civitai_id | text | YES | **Civitai image ID for links** |
| civitai_url | text | YES | Full Civitai URL |
| asset_type | enum | NO | 'video' or 'image' |
| asset_source | enum | NO | Source of asset |
| uri | text | NO | Storage URI |
| sha256sum | text | NO | File hash |
| post_id | bigint | YES | FK to civitai_posts |
| input_prompt_id | bigint | YES | FK to prompts (input) |
| output_prompt_id | bigint | YES | FK to prompts (output) |
| input_asset_ids | bigint[] | NO | Array of source asset IDs |
| metadata | jsonb | YES | Additional metadata |
| on_behalf_of | text | YES | **User first name** |
| created_by | text | NO | System user |
| created_at | timestamptz | NO | Record creation time |
| updated_at | timestamptz | NO | Last update time |

## Table: civitai.asset_stats

Engagement metrics for assets.

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| id | bigint | NO | Primary key |
| asset_id | bigint | NO | **FK to assets.id** |
| post_id | bigint | YES | FK to civitai_posts.id |
| like_count | bigint | NO | Number of likes (default 0) |
| heart_count | bigint | NO | Number of hearts (default 0) |
| laugh_count | bigint | NO | Number of laughs (default 0) |
| cry_count | bigint | NO | Number of cries (default 0) |
| dislike_count | bigint | NO | Number of dislikes (default 0) |
| comment_count | bigint | NO | Number of comments (default 0) |
| civitai_created_at | timestamptz | YES | **When posted on Civitai** |
| civitai_account | text | YES | Civitai account identifier |
| on_behalf_of | text | YES | **User first name** |
| created_at | timestamptz | NO | Record creation time |
| updated_at | timestamptz | NO | Last update time |

**Engagement Calculations:**
- Positive engagement: `like_count + heart_count + laugh_count`
- Total engagement: `like_count + heart_count + laugh_count + cry_count + dislike_count + comment_count`

## Table: civitai.video_analysis

AI-generated video analysis from ffprobe and LLM (Gemini).

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| id | bigint | NO | Primary key |
| asset_id | bigint | NO | **FK to assets.id** |
| duration_seconds | numeric(10,3) | YES | Video duration |
| frame_rate | numeric(6,3) | YES | FPS |
| frame_count | integer | YES | Total frames |
| bitrate_kbps | integer | YES | Bitrate in kbps |
| video_codec | text | YES | e.g., h264, vp9 |
| audio_codec | text | YES | e.g., aac, mp3 |
| has_audio | boolean | YES | Has audio track |
| nsfw_score | numeric(4,3) | YES | NSFW score (0-1) |
| quality_score | numeric(4,3) | YES | **Quality score (0-1)** |
| motion_intensity | numeric(4,3) | YES | **Motion intensity (0-1)** |
| blur_score | numeric(4,3) | YES | Blur detection (0-1) |
| noise_score | numeric(4,3) | YES | Noise/grain (0-1) |
| description | text | YES | **LLM-generated description** |
| inferred_prompt | text | YES | **LLM-inferred generation prompt** |
| tags | text[] | YES | **LLM-generated tags array** |
| technical_details | jsonb | YES | Raw ffprobe output |
| visual_analysis | jsonb | YES | Colors, scenes, brightness |
| audio_analysis | jsonb | YES | Speech, volume, silence |
| quality_analysis | jsonb | YES | Blur regions, artifacts |
| ai_analysis | jsonb | YES | Objects, faces, styles |
| llm_metadata | jsonb | YES | LLM model info, confidence |
| analyzer_version | text | YES | Analyzer version |
| created_at | timestamptz | NO | Record creation time |
| updated_at | timestamptz | NO | Last update time |

**Querying Tags (array):**
```sql
WHERE 'anime' = ANY(va.tags)
```

**Querying JSONB:**
```sql
WHERE va.ai_analysis->>'is_clearly_ai_generated' = 'true'
WHERE va.visual_analysis->'dominant_colors' ? '#ff0000'
```

## Table: civitai.civitai_posts

Post metadata.

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| id | bigint | NO | Primary key |
| civitai_id | text | NO | **Civitai post ID for links** |
| civitai_url | text | NO | Full Civitai URL |
| title | text | YES | Post title |
| description | text | YES | Post description |
| civitai_account | text | NO | Account (default 'c29') |
| status | enum | NO | Post status |
| metadata | jsonb | YES | Additional metadata |
| on_behalf_of | text | YES | User first name |
| created_at | timestamptz | NO | Record creation time |
| updated_at | timestamptz | NO | Last update time |

## Table: civitai.prompts

Generation prompts.

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| id | bigint | NO | Primary key |
| content | text | NO | Prompt content |
| llm_model_provider | text | YES | Model provider |
| llm_model | text | YES | Model name |
| purpose | text | YES | Prompt purpose |
| metadata | jsonb | YES | Additional metadata |
| on_behalf_of | text | YES | User first name |
| created_at | timestamptz | NO | Record creation time |

## Table: civitai.events

Audit log for changes.

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| id | bigint | NO | Primary key |
| occurred_at | timestamptz | NO | Event time |
| actor | text | NO | Who made the change |
| table_name | text | NO | Affected table |
| op | text | NO | Operation type |
| row_id | bigint | NO | Affected row ID |
| old_data | jsonb | YES | Previous values |
| new_data | jsonb | YES | New values |

## Common JOIN Patterns

**Assets with Stats:**
```sql
SELECT a.civitai_id, ast.*
FROM civitai.assets a
JOIN civitai.asset_stats ast ON ast.asset_id = a.id
WHERE a.asset_type = 'video'
```

**Assets with Video Analysis:**
```sql
SELECT a.civitai_id, va.description, va.tags, va.quality_score
FROM civitai.assets a
JOIN civitai.video_analysis va ON va.asset_id = a.id
WHERE a.asset_type = 'video'
```

**Full Video Data (Assets + Stats + Analysis):**
```sql
SELECT 
  a.civitai_id,
  ast.like_count, ast.heart_count, ast.comment_count,
  va.tags, va.quality_score, va.motion_intensity
FROM civitai.assets a
JOIN civitai.asset_stats ast ON ast.asset_id = a.id
JOIN civitai.video_analysis va ON va.asset_id = a.id
WHERE a.asset_type = 'video'
```
