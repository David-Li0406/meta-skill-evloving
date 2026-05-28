# Report Templates

Templates for generating weekly performance reports in JSON and HTML formats.

## JSON Report Template

```json
{
  "report_type": "weekly_performance",
  "generated_at": "2025-01-13T10:30:00Z",
  "report_period": {
    "start": "2025-01-06T00:00:00Z",
    "end": "2025-01-13T00:00:00Z",
    "week_label": "Week of Jan 6-12, 2025"
  },
  "account": {
    "civitai_account": "c29",
    "uploaders": ["Richard", "Alice", "Bob"]
  },
  "summary": {
    "total_assets": 45,
    "total_posts": 12,
    "total_engagement": 1234,
    "total_positive_engagement": 1050,
    "breakdown": {
      "likes": 420,
      "hearts": 380,
      "laughs": 250,
      "cries": 45,
      "dislikes": 14,
      "comments": 125
    },
    "avg_engagement_per_asset": 27.4,
    "positive_engagement_rate": 85.2
  },
  "week_over_week": {
    "engagement_change": 156,
    "engagement_growth_pct": 12.5,
    "assets_change": 5,
    "trend": "Growing"
  },
  "top_performers": [
    {
      "rank": 1,
      "civitai_id": "12345",
      "civitai_url": "https://civitai.com/images/12345",
      "uploader": "Richard",
      "engagement": {
        "total": 156,
        "likes": 45,
        "hearts": 68,
        "laughs": 23,
        "comments": 15
      },
      "video_analysis": {
        "tags": ["anime", "action", "dynamic"],
        "quality_score": 0.89,
        "motion_intensity": 0.75,
        "description": "High-energy anime battle scene..."
      }
    }
  ],
  "tag_insights": {
    "best_performing": [
      {"tag": "anime", "avg_engagement": 45.2, "video_count": 12},
      {"tag": "cinematic", "avg_engagement": 42.8, "video_count": 8}
    ],
    "underutilized": [
      {"tag": "nature", "avg_engagement": 38.5, "video_count": 2},
      {"tag": "abstract", "avg_engagement": 35.0, "video_count": 1}
    ]
  },
  "quality_analysis": {
    "optimal_range": "0.80-0.89",
    "correlation_insight": "Videos with quality_score 0.80-0.89 have 25% higher engagement"
  },
  "recommendations": [
    {
      "priority": "high",
      "category": "content",
      "insight": "Anime + high-motion videos get 2x engagement",
      "action": "Increase anime content production with motion_intensity > 0.7"
    },
    {
      "priority": "medium",
      "category": "quality",
      "insight": "High quality videos (>0.85) underperforming",
      "action": "Review tagging strategy for high-quality content"
    }
  ]
}
```

## HTML Report Template (Tailwind CSS)

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Weekly Performance Report - {{WEEK_LABEL}}</title>
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-50 min-h-screen">
  <div class="max-w-6xl mx-auto py-8 px-4">
    
    <!-- Header -->
    <header class="mb-8">
      <h1 class="text-3xl font-bold text-gray-900">Weekly Performance Report</h1>
      <p class="text-gray-600 mt-1">{{WEEK_LABEL}}</p>
      <p class="text-sm text-gray-500">Generated: {{GENERATED_AT}}</p>
    </header>

    <!-- Summary Cards -->
    <section class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
      <div class="bg-white rounded-lg shadow p-4">
        <p class="text-sm text-gray-500">Total Assets</p>
        <p class="text-2xl font-bold text-gray-900">{{TOTAL_ASSETS}}</p>
      </div>
      <div class="bg-white rounded-lg shadow p-4">
        <p class="text-sm text-gray-500">Total Engagement</p>
        <p class="text-2xl font-bold text-gray-900">{{TOTAL_ENGAGEMENT}}</p>
      </div>
      <div class="bg-white rounded-lg shadow p-4">
        <p class="text-sm text-gray-500">Avg per Asset</p>
        <p class="text-2xl font-bold text-gray-900">{{AVG_ENGAGEMENT}}</p>
      </div>
      <div class="bg-white rounded-lg shadow p-4">
        <p class="text-sm text-gray-500">Week Change</p>
        <p class="text-2xl font-bold {{TREND_COLOR}}">{{TREND_ICON}} {{GROWTH_PCT}}%</p>
      </div>
    </section>

    <!-- Engagement Breakdown -->
    <section class="bg-white rounded-lg shadow p-6 mb-8">
      <h2 class="text-xl font-semibold text-gray-900 mb-4">Engagement Breakdown</h2>
      <div class="grid grid-cols-3 md:grid-cols-6 gap-4 text-center">
        <div>
          <p class="text-2xl font-bold text-blue-600">{{LIKES}}</p>
          <p class="text-sm text-gray-500">Likes</p>
        </div>
        <div>
          <p class="text-2xl font-bold text-red-500">{{HEARTS}}</p>
          <p class="text-sm text-gray-500">Hearts</p>
        </div>
        <div>
          <p class="text-2xl font-bold text-yellow-500">{{LAUGHS}}</p>
          <p class="text-sm text-gray-500">Laughs</p>
        </div>
        <div>
          <p class="text-2xl font-bold text-purple-500">{{CRIES}}</p>
          <p class="text-sm text-gray-500">Cries</p>
        </div>
        <div>
          <p class="text-2xl font-bold text-gray-500">{{DISLIKES}}</p>
          <p class="text-sm text-gray-500">Dislikes</p>
        </div>
        <div>
          <p class="text-2xl font-bold text-green-600">{{COMMENTS}}</p>
          <p class="text-sm text-gray-500">Comments</p>
        </div>
      </div>
    </section>

    <!-- Top Performers -->
    <section class="bg-white rounded-lg shadow p-6 mb-8">
      <h2 class="text-xl font-semibold text-gray-900 mb-4">Top Performers</h2>
      <div class="overflow-x-auto">
        <table class="min-w-full">
          <thead>
            <tr class="border-b border-gray-200">
              <th class="text-left py-3 px-4 text-sm font-medium text-gray-500">Rank</th>
              <th class="text-left py-3 px-4 text-sm font-medium text-gray-500">Video</th>
              <th class="text-left py-3 px-4 text-sm font-medium text-gray-500">Uploader</th>
              <th class="text-left py-3 px-4 text-sm font-medium text-gray-500">Tags</th>
              <th class="text-right py-3 px-4 text-sm font-medium text-gray-500">Quality</th>
              <th class="text-right py-3 px-4 text-sm font-medium text-gray-500">Engagement</th>
            </tr>
          </thead>
          <tbody>
            {{#TOP_PERFORMERS}}
            <tr class="border-b border-gray-100 hover:bg-gray-50">
              <td class="py-3 px-4 text-sm font-medium text-gray-900">#{{RANK}}</td>
              <td class="py-3 px-4">
                <a href="{{CIVITAI_URL}}" target="_blank" class="text-blue-600 hover:underline text-sm">
                  {{CIVITAI_ID}}
                </a>
              </td>
              <td class="py-3 px-4 text-sm text-gray-600">{{UPLOADER}}</td>
              <td class="py-3 px-4">
                <div class="flex flex-wrap gap-1">
                  {{#TAGS}}
                  <span class="px-2 py-0.5 bg-gray-100 text-gray-600 text-xs rounded">{{TAG}}</span>
                  {{/TAGS}}
                </div>
              </td>
              <td class="py-3 px-4 text-sm text-right text-gray-600">{{QUALITY_SCORE}}</td>
              <td class="py-3 px-4 text-sm text-right font-medium text-gray-900">{{TOTAL_ENGAGEMENT}}</td>
            </tr>
            {{/TOP_PERFORMERS}}
          </tbody>
        </table>
      </div>
    </section>

    <!-- Tag Insights -->
    <section class="grid md:grid-cols-2 gap-6 mb-8">
      <div class="bg-white rounded-lg shadow p-6">
        <h2 class="text-xl font-semibold text-gray-900 mb-4">Best Performing Tags</h2>
        <ul class="space-y-3">
          {{#BEST_TAGS}}
          <li class="flex justify-between items-center">
            <span class="px-3 py-1 bg-green-100 text-green-800 text-sm rounded-full">{{TAG}}</span>
            <span class="text-sm text-gray-600">{{AVG_ENGAGEMENT}} avg / {{VIDEO_COUNT}} videos</span>
          </li>
          {{/BEST_TAGS}}
        </ul>
      </div>
      <div class="bg-white rounded-lg shadow p-6">
        <h2 class="text-xl font-semibold text-gray-900 mb-4">Underutilized Tags</h2>
        <ul class="space-y-3">
          {{#UNDERUTILIZED_TAGS}}
          <li class="flex justify-between items-center">
            <span class="px-3 py-1 bg-yellow-100 text-yellow-800 text-sm rounded-full">{{TAG}}</span>
            <span class="text-sm text-gray-600">{{AVG_ENGAGEMENT}} avg / {{VIDEO_COUNT}} videos</span>
          </li>
          {{/UNDERUTILIZED_TAGS}}
        </ul>
      </div>
    </section>

    <!-- Recommendations -->
    <section class="bg-white rounded-lg shadow p-6">
      <h2 class="text-xl font-semibold text-gray-900 mb-4">Recommendations for Next Week</h2>
      <ul class="space-y-4">
        {{#RECOMMENDATIONS}}
        <li class="flex items-start gap-3">
          <span class="flex-shrink-0 w-6 h-6 rounded-full {{PRIORITY_BG}} flex items-center justify-center">
            <span class="text-xs font-bold {{PRIORITY_TEXT}}">{{PRIORITY_NUM}}</span>
          </span>
          <div>
            <p class="font-medium text-gray-900">{{INSIGHT}}</p>
            <p class="text-sm text-gray-600 mt-1">{{ACTION}}</p>
          </div>
        </li>
        {{/RECOMMENDATIONS}}
      </ul>
    </section>

  </div>
</body>
</html>
```

## Template Variables

### Summary Section
| Variable | Description | Example |
|----------|-------------|---------|
| `{{WEEK_LABEL}}` | Human-readable week | "Week of Jan 6-12, 2025" |
| `{{GENERATED_AT}}` | Report generation time | "Jan 13, 2025 10:30 AM" |
| `{{TOTAL_ASSETS}}` | Total videos/images | "45" |
| `{{TOTAL_ENGAGEMENT}}` | Sum of all reactions | "1,234" |
| `{{AVG_ENGAGEMENT}}` | Engagement per asset | "27.4" |
| `{{GROWTH_PCT}}` | Week-over-week change | "+12.5" |
| `{{TREND_COLOR}}` | Tailwind color class | "text-green-600" |
| `{{TREND_ICON}}` | Up/down/stable indicator | "↑" or "↓" or "→" |

### Engagement Breakdown
| Variable | Description |
|----------|-------------|
| `{{LIKES}}` | Total like count |
| `{{HEARTS}}` | Total heart count |
| `{{LAUGHS}}` | Total laugh count |
| `{{CRIES}}` | Total cry count |
| `{{DISLIKES}}` | Total dislike count |
| `{{COMMENTS}}` | Total comment count |

### Top Performers (Loop)
| Variable | Description |
|----------|-------------|
| `{{RANK}}` | Position (1, 2, 3...) |
| `{{CIVITAI_ID}}` | Asset civitai_id |
| `{{CIVITAI_URL}}` | Full Civitai link |
| `{{UPLOADER}}` | on_behalf_of value |
| `{{TAGS}}` | Array of tag objects |
| `{{QUALITY_SCORE}}` | Video quality (0.00-1.00) |
| `{{TOTAL_ENGAGEMENT}}` | Sum of all reactions |

### Recommendations (Loop)
| Variable | Description |
|----------|-------------|
| `{{PRIORITY_NUM}}` | 1, 2, 3 |
| `{{PRIORITY_BG}}` | bg-red-100, bg-yellow-100, bg-blue-100 |
| `{{PRIORITY_TEXT}}` | text-red-600, text-yellow-600, text-blue-600 |
| `{{INSIGHT}}` | Key finding |
| `{{ACTION}}` | Recommended action |

## Usage Notes

1. **Generating Reports:**
   - Run queries: weekly-feedback-stats, top-performing-assets, tag-performance
   - Combine results into template structure
   - Replace variables with actual data

2. **Trend Colors:**
   - Growing (positive): `text-green-600`, icon `↑`
   - Declining (negative): `text-red-600`, icon `↓`
   - Stable: `text-gray-600`, icon `→`

3. **Priority Colors:**
   - High: `bg-red-100`, `text-red-600`
   - Medium: `bg-yellow-100`, `text-yellow-600`
   - Low: `bg-blue-100`, `text-blue-600`

4. **Localization:**
   - For Chinese reports, translate labels and use Chinese date formats
   - Keep structure and styling the same
