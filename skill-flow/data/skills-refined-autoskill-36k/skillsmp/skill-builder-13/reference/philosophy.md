# Best Practices Guide

**Progressive Disclosure Applied**: This guide uses a hierarchical structure where you start with high-level concepts and progressively drill down into technical details.

**Token-Optimized Structure**:
- This file: ~628 tokens (overview & navigation)
- [quick-reference.md](./quick-reference.md): ~920 tokens (quick reference for building skills)
- Topic files: 1.4k-2.2k tokens each (deep dives loaded as-needed)

**📑 Navigation**: See [quick-reference.md](./quick-reference.md) for complete file reference and navigation patterns.

---

## 🎯 Quick Start (Level 1)

### Building a New Skill?
→ **[Skill Creation Process](./skill-creation-process.md)** - Follow this step-by-step guide

### Learning Patterns?
Choose your learning path:

- **[Progressive Disclosure](./progressive-disclosure.md)** - Learn the core UX/architectural pattern
- **[Dynamic Manifests](./dynamic-manifests.md)** - Implement runtime capability discovery
- **[Deferred Loading](./deferred-loading.md)** - Optimize resource initialization

### Need Quick Reference?
→ **[quick-reference.md](./quick-reference.md)** - Checklists, templates, and common pitfalls

---

## 📚 Concept Map

```
Best Practices
│
├─── Progressive Disclosure ◄──┐
│    (Design Pattern)           │
│    │                           │
│    └─── Influences ────────────┤
│                                │
├─── Dynamic Manifests ◄────────┤
│    (Runtime Discovery)         │
│    │                           │
│    └─── Enables ───────────────┤
│                                │
└─── Deferred Loading ◄─────────┘
     (Lazy Initialization)
```

---

## 🚀 Why These Patterns Matter

### The Problem
Traditional systems load everything at startup:
- ❌ Slow initialization
- ❌ High memory consumption
- ❌ Wasted resources on unused features
- ❌ Poor scalability

### The Solution
Progressive Disclosure + Dynamic Manifests + Deferred Loading:
- ✅ Fast startup (load on-demand)
- ✅ Efficient resource usage
- ✅ Adaptive capabilities
- ✅ Context-aware feature availability

---

## 📖 Learning Path

### For Beginners
1. Start with **[Progressive Disclosure](./progressive-disclosure.md#what-is-it)** - Understand the philosophy
2. See **[Simple Examples](./progressive-disclosure.md#simple-examples)**
3. Review **[Quick Start](./dynamic-manifests.md#quick-start)**

### For Practitioners
1. Read **[Implementation Patterns](./progressive-disclosure.md#implementation-patterns)**
2. Configure **[Dynamic Manifests](./dynamic-manifests.md#configuration)**
3. Optimize with **[Deferred Loading](./deferred-loading.md#strategies)**

### For Architects
1. Study **[Architectural Principles](./progressive-disclosure.md#architectural-principles)**
2. Design **[Capability Systems](./dynamic-manifests.md#capability-systems)**
3. Implement **[Advanced Optimization](./deferred-loading.md#advanced-techniques)**

---

## 🔗 Topic Relationships

### Progressive Disclosure → Dynamic Manifests
Progressive disclosure provides the **design philosophy**: show users only what they need, when they need it.

Dynamic manifests provide the **technical implementation**: systems query capabilities at runtime, enabling features progressively.

**Example**: A chat interface starts with basic tools (Level 1), then reveals advanced tools (Level 2) as the user demonstrates expertise → The system's dynamic manifest adjusts which tools are available based on context.

### Dynamic Manifests → Deferred Loading
Dynamic manifests tell you **what's available**.

Deferred loading determines **when to initialize it**.

**Example**: Dynamic manifest says "Tool X is available" → Deferred loading ensures Tool X's code isn't loaded until first use → Saves memory and startup time.

---

## 🎓 Real-World Applications

### MCP (Model Context Protocol) Skills
```
User opens Claude Code
  ↓
[Progressive Disclosure]
  → Only basic skills shown initially

User works with project files
  ↓
[Dynamic Manifests]
  → System detects project type
  → New relevant skills appear

User invokes advanced skill
  ↓
[Deferred Loading]
  → Skill code loaded on first use
  → Subsequent calls use cached version
```

### Web Applications
```
User visits page
  ↓
[Progressive Disclosure]
  → Core UI loads first

User navigates to dashboard
  ↓
[Dynamic Manifests]
  → Check user permissions
  → Build feature menu dynamically

User clicks "Export Data"
  ↓
[Deferred Loading]
  → Load export library on demand
  → Initialize only when needed
```

---

## 🛠️ Implementation Checklist

Use this as a quick reference when implementing these patterns:

- [ ] Design information hierarchy (Progressive Disclosure)
- [ ] Identify capability tiers (Basic → Intermediate → Advanced)
- [ ] Implement runtime discovery endpoints (Dynamic Manifests)
- [ ] Create `.well-known/mcp/manifest.json` (MCP specific)
- [ ] Enable lazy initialization (Deferred Loading)
- [ ] Add caching strategies (Optimization)
- [ ] Implement change notifications (Dynamic updates)
- [ ] Test without system restart (Validation)

---

## 📊 Performance Metrics

Track these to measure success:

| Metric | Before | Target | Pattern |
|--------|--------|--------|---------|
| Initial Load Time | 5s | < 1s | Progressive Disclosure |
| Memory at Startup | 500MB | < 100MB | Deferred Loading |
| Feature Discovery | Static | Dynamic | Dynamic Manifests |
| Context Tokens Used | 10k | < 2k | Progressive Loading |

---

## 🔍 Deep Dive Topics

Ready to go deeper? Click any topic:

1. **[Progressive Disclosure](./progressive-disclosure.md)**
   - Design philosophy
   - UX patterns
   - Information architecture
   - Cognitive load management

2. **[Dynamic Manifests](./dynamic-manifests.md)**
   - Configuration guide
   - Endpoint implementation
   - Registry patterns
   - MCP-specific setup

3. **[Deferred Loading](./deferred-loading.md)**
   - Lazy initialization
   - Code splitting
   - Resource optimization
   - Caching strategies

---

## 🎯 Quick Wins

Want immediate improvements? Start here:

### 5-Minute Win: Enable Dynamic Discovery
```json
// claude_desktop_config.json
{
  "mcpServers": {
    "your-server": {
      "dynamicDiscovery": true,
      "discoveryInterval": 5000
    }
  }
}
```
See [Dynamic Manifests: Quick Start](./dynamic-manifests.md#quick-start)

### 15-Minute Win: Implement Lazy Loading
```python
from functools import lru_cache

@lru_cache(maxsize=128)
def load_expensive_resource():
    # Only loads on first call
    return initialize_resource()
```
See [Deferred Loading: Basic Patterns](./deferred-loading.md#basic-patterns)

### 30-Minute Win: Progressive Disclosure UI
```markdown
# Level 1: Essentials (always visible)
## Getting Started

# Level 2: Intermediate (click to expand)
<details>
<summary>Advanced Features</summary>
...
</details>

# Level 3: Expert (separate page)
See [Advanced Guide](./advanced.md)
```
See [Progressive Disclosure: UI Patterns](./progressive-disclosure.md#ui-patterns)

---

## 📚 Additional Resources

- [MCP Official Spec](https://spec.modelcontextprotocol.io/)
- [Progressive Disclosure (Nielsen Norman Group)](https://www.nngroup.com/articles/progressive-disclosure/)
- [Lazy Loading Best Practices](https://web.dev/lazy-loading/)

---

## 🆘 Troubleshooting

**Problem**: Changes not appearing without restart
**Solution**: Check [Dynamic Manifests: Configuration](./dynamic-manifests.md#configuration)

**Problem**: High memory usage at startup
**Solution**: Review [Deferred Loading: Strategies](./deferred-loading.md#strategies)

**Problem**: Users overwhelmed by options
**Solution**: Apply [Progressive Disclosure: Principles](./progressive-disclosure.md#architectural-principles)

---

**Last Updated**: 2025-10-20
**Version**: 1.0.0
