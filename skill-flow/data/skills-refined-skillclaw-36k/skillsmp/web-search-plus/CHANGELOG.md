# Changelog - Web Search Plus

## [2.0.0] - 2026-01-23

### 🎉 Major Features

#### Smart Auto-Routing
- **Automatic provider selection** based on query analysis
- No need to manually choose provider - just search!
- Intelligent keyword matching for routing decisions
- Pattern detection for query types (shopping, research, discovery)
- Scoring system for provider selection

#### User Configuration
- **config.json**: Full control over auto-routing behavior
- **Configurable keyword mappings**: Add your own routing keywords
- **Provider priority**: Set tie-breaker order
- **Disable providers**: Turn off providers you don't have API keys for
- **Enable/disable auto-routing**: Opt-in or opt-out as needed

#### Debugging Tools
- **--explain-routing** flag: See exactly why a provider was selected
- Detailed routing metadata in JSON responses
- Shows matched keywords and routing scores

### 📚 Documentation

#### Updated Files
- **README.md**: Complete auto-routing guide with examples
- **SKILL.md**: Detailed routing logic and configuration reference
- **FAQ section**: Common questions about auto-routing
- **Configuration examples**: Pre-built configs for common use cases

#### New Content
- Query routing decision table
- Provider selection logic flowchart
- Customization guide with JSON examples
- Debug mode walkthrough
- Performance and accuracy notes

### 🔧 Technical Changes

#### search.py
- Added `auto_route_provider()` function for query analysis
- Added `explain_routing()` function for debugging
- Default provider changed from required to "auto"
- Enhanced keyword matching with phrase detection
- Provider fallback logic with priority ordering
- Routing metadata in API responses

#### config.json
- New `auto_routing` section with:
  - `enabled`: Toggle auto-routing on/off
  - `fallback_provider`: Default when no match found
  - `provider_priority`: Tie-breaker order
  - `disabled_providers`: Disable specific providers
  - `keyword_mappings`: Customizable routing keywords

### 🎯 Routing Logic

**Serper** (Google):
- Shopping: "price", "buy", "shop", "cost", "deal"
- Local: "near me", "restaurant", "hotel", "weather"
- News: "news", "latest", "breaking"
- Product: "specs", "specification", "review"

**Tavily** (Research):
- Questions: "how does", "how to", "what is", "why does"
- Learning: "explain", "tutorial", "guide", "learn"
- Research: "research", "study", "analyze", "compare"
- Deep dive: "comprehensive", "in-depth", "detailed"

**Exa** (Neural):
- Similarity: "similar to", "like", "alternatives to"
- Discovery: "companies like", "competitors", "related sites"
- Technical: "github", "research paper", "arxiv", "pdf"
- Startup: "startup", "Series A", "YC company"

### 🚀 Usage Examples

```bash
# Auto-routing (default)
python3 scripts/search.py -q "iPhone 16 price"              # → Serper
python3 scripts/search.py -q "how does quantum computing work"  # → Tavily
python3 scripts/search.py -q "companies like Stripe"        # → Exa

# Explicit provider (override auto-routing)
python3 scripts/search.py -p serper -q "your query"

# Debug routing decisions
python3 scripts/search.py --explain-routing -q "your query"
```

### ⚙️ Configuration Examples

**Disable auto-routing:**
```json
{"auto_routing": {"enabled": false}}
```

**Prefer Tavily for research:**
```json
{
  "auto_routing": {
    "fallback_provider": "tavily",
    "provider_priority": ["tavily", "serper", "exa"]
  }
}
```

**Disable Exa (only use Serper & Tavily):**
```json
{"auto_routing": {"disabled_providers": ["exa"]}}
```

**Add custom keywords:**
```json
{
  "auto_routing": {
    "keyword_mappings": {
      "serper": ["bitcoin price", "eth price", "crypto prices"],
      "tavily": ["blockchain tutorial", "smart contracts guide"],
      "exa": ["DeFi companies", "Web3 startups"]
    }
  }
}
```

### 📦 Package Updates

- **Version**: 1.0.8 → 2.0.0
- **Description**: Updated to highlight auto-routing
- **Keywords**: Added "auto-routing", "smart-routing"

### 🔗 Repository

- **GitHub**: https://github.com/robbyczgw-cla/web-search-plus
- **Commits**: 
  - `766ce3b`: Main auto-routing implementation
  - `c29614d`: Package.json update

### 🎓 Documentation Links

- Full documentation: README.md
- Skill reference: SKILL.md
- Configuration: config.json
- Examples: Both docs contain numerous examples

### 🧪 Testing

Verified with test queries:
- ✅ Shopping: "iPhone 16 price" → Serper
- ✅ Research: "how does quantum computing work" → Tavily
- ✅ Discovery: "companies like Stripe" → Exa
- ✅ Ambiguous: "best laptop for programming" → Serper (fallback)
- ✅ Debug mode: --explain-routing working correctly

### 🎯 Next Steps

1. ✅ Code changes committed and pushed to GitHub
2. ✅ Documentation updated (README, SKILL.md)
3. ✅ Configuration examples added
4. ✅ Testing completed
5. ⏳ Publish to ClawdHub (manual step - visit clawdhub.com)

### 💡 Future Enhancements

Potential improvements for future versions:
- ML-based routing using query embeddings
- Usage analytics to improve routing accuracy
- User feedback loop for routing corrections
- A/B testing for routing algorithms
- Provider performance monitoring
- Automatic fallback on provider failures
- Query rewriting for better routing
- Custom routing functions via plugins
