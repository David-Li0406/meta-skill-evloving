# Civitai Analyst Skill

Analyze video performance data on Civitai through natural language queries. This skill enables Claude to generate SQL, execute queries against the civitai_records database, and provide actionable insights.

## Features

- **Natural Language to SQL** - Ask questions in plain English or Chinese, get SQL queries
- **Performance Analysis** - Track likes, hearts, comments, and engagement metrics
- **Content Insights** - Analyze tags, themes, quality scores, and motion intensity
- **Video Comparison** - Compare multiple videos to find common success patterns
- **Weekly Reports** - Generate JSON/HTML performance summaries
- **Recommendations** - Get actionable content strategy suggestions

## Setup

### 1. Environment Variable

Set the MCP server authentication token:

```bash
export CIVITAI_RECORD_MCP_SERVER_TOKEN="your-token-here"
```

Add to your shell profile (`~/.bashrc`, `~/.zshrc`, etc.) for persistence:

```bash
echo 'export CIVITAI_RECORD_MCP_SERVER_TOKEN="your-token-here"' >> ~/.zshrc
```

### 2. MCP Server Configuration

The skill includes a `.mcp.json` file that configures the `civitai_records` MCP server:

```json
{
  "mcpServers": {
    "civitai_records": {
      "type": "http",
      "url": "https://n8n-ock80s0oowgc4cws8g0o48sk.18.191.220.185.sslip.io/mcp/8fe59958-c0d9-4777-847c-0887913c84fc",
      "headers": {
        "Authorization": "Bearer ${CIVITAI_RECORD_MCP_SERVER_TOKEN}"
      }
    }
  }
}
```

## Usage Examples

### Basic Queries

```
"Show me this week's video performance"
"What are my top 10 videos by engagement?"
"Compare rank 2 and rank 9 videos - what do they have in common?"
```

### Analytics Questions

```
"Which tags generate the most engagement?"
"How does quality score correlate with likes?"
"What content themes are trending?"
```

### Weekly Reports

```
"Generate a weekly report for last week"
"Create an HTML performance summary"
```

### Chinese Queries

```
"显示本周的视频表现"
"我的热门视频有哪些共同标签？"
"生成上周的周报"
```

## Database Tables

| Table | Description |
|-------|-------------|
| `civitai.assets` | Core asset records (videos/images) |
| `civitai.asset_stats` | Engagement metrics (likes, hearts, comments) |
| `civitai.video_analysis` | AI-generated analysis (tags, quality scores) |
| `civitai.civitai_posts` | Post metadata |
| `civitai.prompts` | Generation prompts |
| `civitai.events` | Audit log |

## File Structure

```
civitai-analyst/
├── .mcp.json              # MCP server configuration
├── README.md              # This file
├── SKILL.md               # Skill instructions for Claude
└── references/
    ├── schema.md          # Database schema documentation
    ├── query-index.md     # Query catalog with parameters
    ├── report-templates.md # JSON + HTML report templates
    └── queries/           # Pre-built SQL queries
        ├── weekly-feedback-stats.sql
        ├── top-performing-assets.sql
        ├── week-over-week-comparison.sql
        ├── tag-performance.sql
        ├── video-comparison.sql
        ├── quality-vs-engagement.sql
        └── content-theme-analysis.sql
```

## Key Parameters

- **civitai_account**: Account identifier (default: `'c29'`)
- **on_behalf_of**: User's first name for filtering assets
- **Date ranges**: Calendar weeks (Monday-Sunday), PostgreSQL timestamptz format

## Link Formatting

Results include clickable links:
- Assets: `https://civitai.com/images/{civitai_id}`
- Posts: `https://civitai.com/posts/{civitai_id}`

## Author

Richard Hao (richard@feedmob.com)
