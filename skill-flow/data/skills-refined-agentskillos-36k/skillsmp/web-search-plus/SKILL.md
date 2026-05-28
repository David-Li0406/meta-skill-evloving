---
name: web-search-plus
description: Unified search skill with Smart Auto-Routing. Automatically selects between Serper (Google), Tavily (Research), and Exa (Neural) based on query analysis. Just search - the skill picks the best provider.
---

# Web Search Plus

Multi-provider web search with **Smart Auto-Routing**: Serper (Google), Tavily (Research), Exa (Neural).

**NEW in v2.0.0**: Smart Auto-Routing analyzes your query and automatically selects the best provider!

---

## 🚀 Smart Auto-Routing (NEW)

No need to choose a provider - just search! The skill analyzes your query and routes it to the optimal provider:

```bash
# These queries are automatically routed to the best provider:
python3 scripts/search.py -q "iPhone 16 price"              # → Serper (shopping keyword)
python3 scripts/search.py -q "how does quantum computing work"  # → Tavily (research keyword)  
python3 scripts/search.py -q "companies similar to Stripe"  # → Exa (similarity keyword)
python3 scripts/search.py -q "weather in Vienna"            # → Serper (local/weather)
python3 scripts/search.py -q "explain transformer architecture"  # → Tavily (explain keyword)
python3 scripts/search.py -q "AI startups like OpenAI"      # → Exa (companies like)
```

### How It Works

| Query Contains | Routes To | Why |
|---------------|-----------|-----|
| "price", "buy", "shop", "cost", "deal" | **Serper** | Shopping/product queries |
| "near me", "local", "restaurant", "hotel" | **Serper** | Local business queries |
| "weather", "news", "latest" | **Serper** | Real-time information |
| "how does", "how to", "explain", "what is" | **Tavily** | Research/educational |
| "research", "study", "analyze", "compare" | **Tavily** | Deep dive queries |
| "tutorial", "guide", "learn", "understand" | **Tavily** | Learning content |
| "similar to", "companies like", "alternatives" | **Exa** | Similarity search |
| "startup", "YC company", "Series A" | **Exa** | Company discovery |
| "github", "research paper", "arxiv" | **Exa** | Technical discovery |

### Debug Auto-Routing

See exactly why a provider was selected:

```bash
python3 scripts/search.py --explain-routing -q "best laptop to buy 2024"
```

Output:
```json
{
  "query": "best laptop to buy 2024",
  "selected_provider": "serper",
  "reason": "matched_keywords (score=2)",
  "matched_keywords": ["buy", "best"],
  "available_providers": ["serper", "tavily", "exa"]
}
```

---

## 🔍 When to Use This Skill vs Built-in Brave Search

### Use **Built-in Brave Search** (default `web_search` tool) when:
- ✅ General web searches (news, info, questions)
- ✅ Privacy is important
- ✅ Quick lookups without specific requirements
- ✅ No provider-specific features needed
- ✅ Default fallback for most searches

### Use **web-search-plus** when:

#### → **Serper** (Google results):
- 🛍️ **Product specs, prices, shopping** - "Compare iPhone 16 vs Samsung S24"
- 📍 **Local businesses, places** - "Best pizza in Vienna"
- 🎯 **User says "Google it"** - Explicitly wants Google results
- 📰 **Shopping/images needed** - `--type shopping/images`
- 🏆 **Knowledge Graph data** - Structured info (prices, ratings, etc.)

#### → **Tavily** (AI-optimized research):
- 📚 **Research questions** - "How does quantum computing work?"
- 🔬 **Deep dives** - Complex multi-part questions
- 📄 **Need full page content** - Not just snippets (`--raw-content`)
- 🎓 **Academic/technical research** - Synthesized answers
- 🔒 **Domain filtering** - `--include-domains` for trusted sources only

#### → **Exa** (Neural semantic search):
- 🔗 **Find similar pages** - "Sites like OpenAI.com" (`--similar-url`)
- 🏢 **Company/startup discovery** - "AI companies like Anthropic" (`--category company`)
- 📝 **Research papers** - `--category "research paper"`
- 💻 **GitHub projects** - `--category github`
- 📅 **Date-specific content** - `--start-date` / `--end-date`

---

## Quick Decision Tree

```
                    ┌─────────────────────────────┐
                    │  Just use auto-routing!     │
                    │  python3 search.py -q "..." │
                    └─────────────┬───────────────┘
                                  │
                     (Or choose manually:)
                                  │
        ┌─────────────────────────┼─────────────────────────┐
        │                         │                         │
        ▼                         ▼                         ▼
┌───────────────┐       ┌─────────────────┐       ┌─────────────────┐
│ Quick Lookup  │       │    Research     │       │   Discovery     │
│ Products/News │       │   Deep Dive     │       │ Similar/Semantic│
└───────┬───────┘       └────────┬────────┘       └────────┬────────┘
        │                        │                         │
        ▼                        ▼                         ▼
   ┌─────────┐              ┌─────────┐              ┌─────────┐
   │ SERPER  │              │ TAVILY  │              │   EXA   │
   └─────────┘              └─────────┘              └─────────┘
```

### Decision Rules

| If the query involves... | Use | Why |
|--------------------------|-----|-----|
| Product specs, prices, shopping | **Serper** | Google Shopping + Knowledge Graph |
| "Google it" / quick facts | **Serper** | Fastest, most accurate for facts |
| Local businesses, places | **Serper** | Google Maps/Places integration |
| Current news headlines | **Serper** | Real-time Google News |
| Research questions | **Tavily** | Synthesized answers + full content |
| "Explain X" / "How does Y work" | **Tavily** | Deep research with context |
| Need actual page content | **Tavily** | `--raw-content` option |
| Authoritative sources only | **Tavily** | `--include-domains` filtering |
| "Companies like X" | **Exa** | Neural/semantic understanding |
| Find similar pages | **Exa** | `--similar-url` feature |
| Startup/company discovery | **Exa** | `--category company` |
| Research papers | **Exa** | `--category "research paper"` |
| GitHub projects | **Exa** | `--category github` |
| Content from specific dates | **Exa** | Date range filtering |

---

## Provider Comparison

### Feature Matrix

| Feature | Serper | Tavily | Exa |
|---------|:------:|:------:|:---:|
| Speed | ⚡⚡⚡ | ⚡⚡ | ⚡⚡ |
| Factual Accuracy | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| Semantic Understanding | ⭐ | ⭐⭐ | ⭐⭐⭐ |
| Research Quality | ⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| AI Answers | ✓ (snippets) | ✓✓✓ | ✓ |
| Full Page Content | ✗ | ✓ | ✓ |
| Images | ✓ | ✓ | ✗ |
| Shopping | ✓ | ✗ | ✗ |
| Local/Places | ✓ | ✗ | ✗ |
| News | ✓ | ✓ | ✓ |
| Domain Filtering | ✗ | ✓ | ✓ |
| Date Filtering | ✓ (time-range) | ✗ | ✓ (precise) |
| Similar Pages | ✗ | ✗ | ✓ |
| Category Filtering | ✓ (search type) | ✓ (topic) | ✓ (detailed) |
| Knowledge Graph | ✓ | ✗ | ✗ |

### Performance Comparison

| Metric | Serper | Tavily | Exa |
|--------|--------|--------|-----|
| Avg Response Time | 200-400ms | 500-1500ms | 400-800ms |
| Free Tier | 2,500 queries | 1,000/mo | 1,000/mo |
| Cost (paid) | ~$0.001/query | ~$0.004/query | ~$0.001/query |
| Rate Limit | 100/min | 60/min | 100/min |

---

## Usage Patterns

### Pattern 0: Auto-Routed (Recommended)

Let the skill choose the best provider:

```bash
python3 scripts/search.py -q "iPhone 16 Pro Max price"
python3 scripts/search.py -q "how does mRNA vaccination work"
python3 scripts/search.py -q "companies like Linear"
```

### Pattern 1: Quick Lookup (Serper)

For facts, products, definitions, weather, conversions:

```bash
python3 scripts/search.py -p serper -q "iPhone 16 Pro Max specs"
python3 scripts/search.py -p serper -q "weather Vienna"
python3 scripts/search.py -p serper -q "USD to EUR"
```

### Pattern 2: Shopping Research (Serper)

```bash
# Get prices
python3 scripts/search.py -p serper -q "Sony WH-1000XM5" --type shopping

# Get images
python3 scripts/search.py -p serper -q "Sony WH-1000XM5" --images
```

### Pattern 3: News Monitoring (Serper + Tavily)

```bash
# Breaking news (Serper - fast)
python3 scripts/search.py -p serper -q "AI regulation EU" --type news --time-range day

# In-depth analysis (Tavily)
python3 scripts/search.py -p tavily -q "AI regulation EU implications" --depth advanced --topic news
```

### Pattern 4: Research Deep Dive (Tavily)

```bash
# Basic research
python3 scripts/search.py -p tavily -q "how do transformers work in NLP"

# Advanced with full content
python3 scripts/search.py -p tavily -q "transformer attention mechanism" \
  --depth advanced --raw-content

# From authoritative sources
python3 scripts/search.py -p tavily -q "climate change solutions" \
  --include-domains nature.com science.org arxiv.org
```

### Pattern 5: Company/Startup Discovery (Exa)

```bash
# Find companies in a space
python3 scripts/search.py -p exa -q "AI code review startups" --category company

# Find companies similar to a known one
python3 scripts/search.py -p exa --similar-url "https://linear.app" --category company

# Recent funding
python3 scripts/search.py -p exa -q "AI startup Series A" --category company --start-date 2024-01-01
```

### Pattern 6: Academic Research (Exa)

```bash
# Find papers on a topic
python3 scripts/search.py -p exa -q "multimodal large language models" --category "research paper"

# Recent papers only
python3 scripts/search.py -p exa -q "LLM reasoning" --category "research paper" --start-date 2024-01-01

# Papers similar to a reference
python3 scripts/search.py -p exa --similar-url "https://arxiv.org/abs/2303.08774"
```

### Pattern 7: Similar Page Discovery (Exa)

```bash
# Find similar companies
python3 scripts/search.py -p exa --similar-url "https://notion.so"

# Find similar blogs/content
python3 scripts/search.py -p exa --similar-url "https://waitbutwhy.com" --category "personal site"

# Find similar tools
python3 scripts/search.py -p exa --similar-url "https://vercel.com" --max-results 10
```

### Pattern 8: Multi-Provider Workflow

For comprehensive research, combine providers:

```bash
# 1. Quick context (Serper)
python3 scripts/search.py -p serper -q "GPT-4 capabilities"

# 2. Deep research (Tavily)  
python3 scripts/search.py -p tavily -q "GPT-4 technical architecture" --depth advanced

# 3. Find related work (Exa)
python3 scripts/search.py -p exa -q "large language model research" --category "research paper" --start-date 2023-01-01

# 4. Find competitors (Exa)
python3 scripts/search.py -p exa --similar-url "https://openai.com" --category company
```

---

## ⚙️ Configuration

### config.json Options

```json
{
  "defaults": {
    "provider": "serper",       // Default when auto-routing is disabled
    "max_results": 5            // Default number of results
  },
  
  "auto_routing": {
    "enabled": true,            // Enable/disable smart routing
    "fallback_provider": "serper",  // Used when no keywords match
    "provider_priority": ["serper", "tavily", "exa"],  // Tie-breaker order
    "disabled_providers": [],   // Providers to skip (e.g., ["exa"])
    "keyword_mappings": {
      "serper": ["price", "buy", "shop", ...],
      "tavily": ["how does", "explain", "research", ...],
      "exa": ["similar to", "companies like", ...]
    }
  },
  
  "serper": {
    "country": "us",
    "language": "en"
  },
  
  "tavily": {
    "depth": "basic",
    "topic": "general"
  },
  
  "exa": {
    "type": "neural"
  }
}
```

### Customization Examples

**Disable a provider:**
```json
{
  "auto_routing": {
    "disabled_providers": ["exa"]
  }
}
```

**Add custom keywords:**
```json
{
  "auto_routing": {
    "keyword_mappings": {
      "serper": ["price", "buy", "shop", "amazon", "ebay"],
      "tavily": ["how does", "explain", "tutorial", "course"],
      "exa": ["similar to", "competitors", "YC batch"]
    }
  }
}
```

**Change fallback provider:**
```json
{
  "auto_routing": {
    "fallback_provider": "tavily"
  }
}
```

**Disable auto-routing entirely:**
```json
{
  "auto_routing": {
    "enabled": false
  },
  "defaults": {
    "provider": "serper"
  }
}
```

---

## Cost Optimization

### Budget Strategy

| Budget | Strategy |
|--------|----------|
| **Free only** | Serper (2500) + Tavily (1000) + Exa (1000) = 4500 queries/mo |
| **$5/mo** | Add Tavily Basic for research-heavy use |
| **$50/mo** | Add Serper Starter for high-volume lookups |

### Cost-Saving Tips

1. **Use auto-routing** - it defaults to Serper (cheapest) when no keywords match
2. **Use Tavily `basic`** before trying `advanced` (50% cheaper)
3. **Set `max_results` appropriately** - don't fetch 10 when 3 suffice
4. **Use Exa only for semantic queries** - don't waste on keyword searches
5. **Cache repeated queries** in your application

### Cost per Query Type

| Query Type | Recommended | Cost |
|------------|-------------|------|
| Quick fact | Serper | ~$0.001 |
| Product lookup | Serper | ~$0.001 |
| Basic research | Tavily basic | ~$0.004 |
| Deep research | Tavily advanced | ~$0.008 |
| Semantic search | Exa neural | ~$0.001 |
| Similar pages | Exa | ~$0.001 |

---

## Output Format

Unified JSON structure from all providers:

```json
{
  "provider": "serper|tavily|exa",
  "query": "search query",
  "results": [
    {
      "title": "Page Title",
      "url": "https://example.com",
      "snippet": "Content excerpt...",
      "score": 0.95,
      "date": "2024-01-15",
      "raw_content": "Full content (Tavily only)"
    }
  ],
  "images": ["url1", "url2"],
  "answer": "Synthesized answer",
  "knowledge_graph": { },
  "routing": {
    "auto_routed": true,
    "selected_provider": "serper",
    "reason": "matched_keywords (score=2)",
    "matched_keywords": ["price", "buy"]
  }
}
```

---

## Environment Setup

```bash
# Set API keys (at least one required)
export SERPER_API_KEY="..."   # https://serper.dev
export TAVILY_API_KEY="..."   # https://tavily.com  
export EXA_API_KEY="..."      # https://exa.ai
```

---

## Defaults

| Provider | Setting | Default |
|----------|---------|---------|
| Serper | country | `us` |
| Serper | language | `en` |
| Serper | max_results | 5 |
| Tavily | depth | `basic` |
| Tavily | topic | `general` |
| Tavily | max_results | 5 |
| Exa | type | `neural` |
| Exa | max_results | 5 |

---

## FAQ

### General

**Q: Do I need API keys for all three providers?**
> No. You only need keys for providers you want to use. Auto-routing automatically skips providers without keys.

**Q: What happens if auto-routing can't find a match?**
> It uses the fallback provider (default: Serper, the fastest).

**Q: Can I force a specific provider?**
> Yes, use `-p serper`, `-p tavily`, or `-p exa` to bypass auto-routing.

**Q: How do I know which provider was used?**
> Check the `routing` field in the JSON output.

### Auto-Routing

**Q: Why did my query go to the wrong provider?**
> Use `--explain-routing` to debug. You can also add custom keywords to config.json.

**Q: Can I add my own keywords?**
> Yes! Edit `config.json` → `auto_routing.keyword_mappings`.

**Q: How does scoring work?**
> Multi-word phrases get higher weights. "companies like" scores 2, "like" scores 1.

### Troubleshooting

**Q: I get "Missing API key" error**
> Set the environment variable for the provider you want to use.

**Q: Results are empty**
> Try a different provider or broaden your query.

**Q: Auto-routing always picks Serper**
> Your query may not contain keywords for other providers, or they don't have API keys set.
