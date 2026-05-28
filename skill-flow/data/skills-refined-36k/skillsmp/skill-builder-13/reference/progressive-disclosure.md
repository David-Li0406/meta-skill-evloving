# Progressive Disclosure

> **Definition**: A design pattern that sequences information and actions across multiple screens to reduce cognitive load and improve user experience.

**Navigation**: [← Back to Best Practices](../SKILL.md) | [Next: Dynamic Manifests →](./dynamic-manifests.md)

---

## Table of Contents

- [What Is It?](#what-is-it) ← Start here
- [Why Use It?](#why-use-it)
- [Simple Examples](#simple-examples)
- [Implementation Patterns](#implementation-patterns) ← For practitioners
- [Architectural Principles](#architectural-principles) ← For architects
- [UI Patterns](#ui-patterns)
- [Related Concepts](#related-concepts)

---

## What Is It?

Progressive disclosure is revealing information **gradually** rather than all at once.

### The Core Idea

```
❌ Bad: Show everything immediately
User sees: [100 buttons] [50 options] [20 menus]
Result: Overwhelmed, confused

✅ Good: Show essentials, reveal more as needed
User sees: [5 core actions]
User clicks "More": [15 additional options appear]
User clicks "Advanced": [Advanced features panel opens]
Result: Focused, confident
```

### Real-World Analogy

**Restaurant Menu**
```
1. Main categories (Appetizers, Entrees, Desserts) ← Level 1
   └─ Click "Entrees"
      2. Entree types (Pasta, Seafood, Steak) ← Level 2
         └─ Click "Pasta"
            3. Specific dishes with details ← Level 3
```

This prevents menu overwhelm while still providing complete information.

---

## Why Use It?

### Benefits

| Benefit | Description | Impact |
|---------|-------------|--------|
| **Reduced Cognitive Load** | Users process less information at once | Less confusion, faster decisions |
| **Improved Discoverability** | Users find relevant features easier | Better feature adoption |
| **Faster Performance** | Load only what's needed now | Quicker startup, less memory |
| **Adaptive Complexity** | Beginners see simple, experts see advanced | Serves all skill levels |

### When to Use

✅ **Use progressive disclosure when:**
- Users don't need all features/info immediately
- Feature set is large or complex
- Users have varying skill levels
- Performance/load time matters

❌ **Don't use when:**
- All information is equally critical
- Users need to compare all options at once
- Feature set is small (< 7 items)
- Extra clicks harm the experience

---

## Simple Examples

### Example 1: Settings Panel

**Traditional Approach:**
```
Settings
├── Profile Name: _______
├── Email: _______
├── Password: _______
├── Theme: [ Dark | Light ]
├── Language: [ English ▼ ]
├── Timezone: [ UTC-5 ▼ ]
├── Date Format: [ MM/DD/YYYY ▼ ]
├── Currency: [ USD ▼ ]
├── API Keys: _______
├── Webhook URL: _______
├── Debug Mode: [ ]
├── Log Level: [ Info ▼ ]
└── ... (20 more settings)
```
Result: Users scrolls, scans, feels lost.

**Progressive Disclosure:**
```
Settings
├── Profile Name: _______
├── Email: _______
├── Theme: [ Dark | Light ]
│
├── [▼ Advanced Settings]
│   └── (collapsed by default)
│
└── [▼ Developer Settings]
    └── (collapsed by default)
```
Click "Advanced Settings":
```
Advanced Settings
├── Language: [ English ▼ ]
├── Timezone: [ UTC-5 ▼ ]
├── Date Format: [ MM/DD/YYYY ▼ ]
└── Currency: [ USD ▼ ]
```

### Example 2: MCP Skills

**Traditional: All Skills Loaded**
```python
# Load everything at startup
available_skills = [
    "basic-search",
    "file-operations",
    "web-scraping",
    "data-analysis",
    "machine-learning",
    "blockchain-analysis",
    "video-processing",
    # ... 50 more skills
]
```
Result: Slow startup, high memory, overwhelming list.

**Progressive Disclosure:**
```python
# Level 1: Always available
tier_1_skills = ["basic-search", "file-operations"]

# Level 2: Loaded when project type detected
if is_data_project():
    tier_2_skills = ["data-analysis", "visualization"]

# Level 3: Loaded on explicit request
if user_requests("machine-learning"):
    tier_3_skills = ["ml-training", "model-deployment"]
```

### Example 3: Command Line Tool

**Traditional:**
```bash
$ mytool --help

Usage: mytool [OPTIONS] COMMAND [ARGS]...

Options:
  --config PATH          Configuration file path
  --verbose              Verbose output
  --debug                Debug mode
  --log-file PATH        Log file path
  --log-level LEVEL      Logging level
  --timeout SECONDS      Operation timeout
  --retry-count N        Number of retries
  --parallel N           Parallel workers
  --cache-dir PATH       Cache directory
  --no-cache             Disable caching
  --format FORMAT        Output format
  ... (30 more options)

Commands:
  init      Initialize project
  build     Build project
  deploy    Deploy project
  test      Run tests
  ... (20 more commands)
```

**Progressive Disclosure:**
```bash
$ mytool --help

Usage: mytool [OPTIONS] COMMAND

Common Commands:
  init      Initialize project
  build     Build project
  deploy    Deploy project

Run 'mytool COMMAND --help' for command-specific options
Run 'mytool --help-all' for complete documentation

$ mytool build --help

Usage: mytool build [OPTIONS]

Essential Options:
  --output PATH    Output directory (default: ./dist)
  --watch          Watch for changes

Advanced Options (mytool build --help-advanced):
  --parallel N     Parallel workers
  --cache-dir PATH Cache directory
  ... (more advanced options)
```

---

## Implementation Patterns

### Pattern 1: Tiered Information Architecture

Organize content into logical tiers:

```
Tier 1: Essentials (80% of users need this)
├── Core functionality
├── Most common tasks
└── Critical information

Tier 2: Intermediate (30% of users need this)
├── Advanced features
├── Customization options
└── Detailed documentation

Tier 3: Expert (5% of users need this)
├── Edge cases
├── Debug/diagnostic tools
└── API reference
```

**Implementation:**
```markdown
# My API Documentation

## Quick Start (Tier 1)
Basic usage examples that work for most cases.

<details>
<summary>Advanced Usage (Tier 2)</summary>

## Authentication Options
Detailed authentication flows...

## Rate Limiting
How to handle rate limits...

</details>

[Expert Guide](./expert-guide.md) (Tier 3) →
```

### Pattern 2: Context-Aware Disclosure

Show features based on user context:

```python
class FeatureDisclosure:
    def get_available_features(self, user_context):
        features = ["core_feature_1", "core_feature_2"]  # Always available

        # Intermediate features
        if user_context.skill_level >= "intermediate":
            features.extend(["advanced_search", "bulk_operations"])

        # Expert features
        if user_context.has_permission("admin"):
            features.extend(["system_config", "user_management"])

        # Contextual features
        if user_context.project_type == "data_science":
            features.extend(["ml_tools", "visualization"])

        return features
```

### Pattern 3: Progressive Enhancement

Start minimal, add capabilities:

```javascript
// Level 1: Basic functionality works everywhere
function saveData(data) {
    localStorage.setItem('data', JSON.stringify(data));
}

// Level 2: Enhanced with sync (if available)
if (navigator.onLine && hasCloudSync()) {
    function saveData(data) {
        localStorage.setItem('data', JSON.stringify(data));
        cloudSync.upload(data);  // Progressive enhancement
    }
}

// Level 3: Real-time collaboration (if enabled)
if (hasFeature('realtime_collaboration')) {
    function saveData(data) {
        localStorage.setItem('data', JSON.stringify(data));
        cloudSync.upload(data);
        websocket.broadcast(data);  // Further enhancement
    }
}
```

### Pattern 4: Lazy Loading

Defer initialization until needed:

```python
class SkillManager:
    def __init__(self):
        self._skills = {}
        self._skill_registry = {
            'basic': ['search', 'files'],
            'advanced': ['ml', 'data_analysis'],
            'expert': ['custom_models']
        }

    def get_skill(self, skill_name):
        # Progressive disclosure: Load on first access
        if skill_name not in self._skills:
            self._skills[skill_name] = self._load_skill(skill_name)
        return self._skills[skill_name]

    def _load_skill(self, skill_name):
        # Deferred loading happens here
        module = import_module(f'skills.{skill_name}')
        return module.SkillClass()
```

---

## Architectural Principles

### Principle 1: Information Hierarchy

Design with clear levels:

```
Level 0: Critical (always visible, < 5 items)
  └─ Things users MUST see/do immediately

Level 1: Primary (visible by default, < 10 items)
  └─ Core functionality, 80% use case

Level 2: Secondary (behind 1 click, < 20 items)
  └─ Advanced features, configuration

Level 3: Tertiary (behind 2+ clicks, unlimited)
  └─ Expert features, detailed docs, edge cases
```

### Principle 2: Cognitive Load Management

**Miller's Law**: Humans can hold 7±2 items in working memory.

**Application:**
- Level 1 UI: Show ≤ 7 primary actions
- Menus: Group into ≤ 7 categories
- Forms: Break into ≤ 7 fields per step

**Bad Example:**
```
[Button1] [Button2] [Button3] [Button4] [Button5]
[Button6] [Button7] [Button8] [Button9] [Button10]
[Button11] [Button12] [Button13] [Button14] [Button15]
```

**Good Example:**
```
[Common Actions ▼]
  ├─ Action 1
  ├─ Action 2
  └─ Action 3

[Advanced ▼]
  ├─ Action 4
  └─ Action 5

[Expert ▼]
  └─ More...
```

### Principle 3: Discoverability vs. Visibility

Balance showing enough vs. hiding too much:

```
High Discoverability
↑
│   Ideal Zone:
│   Core features visible,
│   Advanced features discoverable
│
│       ┌─────────────┐
│       │  ✓ Sweet    │
│       │    Spot     │
│       └─────────────┘
│
└──────────────────────────→ High Visibility
  Hidden features           Feature overload
```

**Techniques:**
- Visual cues: "▼ More options" "⚙ Advanced"
- Tooltips: Hint at hidden features
- Progressive help: "New features available!"
- Analytics: Track if users find features

### Principle 4: Reversible Disclosure

Users should control disclosure:

```
✅ Good: User-controlled
[▼ Show Advanced Options] ← User clicks to expand
[▲ Hide Advanced Options] ← User clicks to collapse

❌ Bad: Forced progression
Step 1 → Step 2 → Step 3 (can't go back)
```

**Implementation:**
- Persistent state: Remember user's disclosure preferences
- Keyboard shortcuts: Power users want quick access
- Breadcrumbs: Show where user is in hierarchy

---

## UI Patterns

### Pattern: Accordion/Collapsible Sections

```html
<details>
  <summary>Basic Configuration</summary>
  <p>Essential settings here...</p>
</details>

<details>
  <summary>Advanced Configuration</summary>
  <p>Advanced settings here...</p>
</details>
```

### Pattern: Tabs

```
┌─────────┬──────────┬──────────┐
│ Basic   │ Advanced │ Expert   │
├─────────┴──────────┴──────────┤
│                                │
│  [Content for selected tab]   │
│                                │
└────────────────────────────────┘
```

### Pattern: Modal/Dialog

```
Main Screen (Simple)
[Click "Advanced Settings" button]
    ↓
┌─────────────────────────┐
│ Advanced Settings       │
│                         │
│ [Complex options here]  │
│                         │
│ [Cancel]  [Apply]       │
└─────────────────────────┘
```

### Pattern: Progressive Form

```
Step 1: Basic Info          Step 2: Details         Step 3: Preferences
┌─────────────────┐        ┌─────────────────┐     ┌─────────────────┐
│ Name: _______   │   →    │ Address: ____   │  →  │ Theme: [ ]      │
│ Email: ______   │        │ Phone: ______   │     │ Notifications:  │
│                 │        │                 │     │   [ ] Email     │
│ [Next]          │        │ [Back] [Next]   │     │   [ ] SMS       │
└─────────────────┘        └─────────────────┘     │ [Back] [Finish] │
                                                    └─────────────────┘
```

### Pattern: Contextual Help

```
Setting Name  [?]  ← Hover shows basic help
   ↓
Hover: "Controls the display theme"
Click [?]: Opens detailed documentation
```

---

## Related Concepts

### Progressive Disclosure → [Dynamic Manifests](./dynamic-manifests.md)

Progressive disclosure = **design philosophy**
Dynamic manifests = **technical implementation**

Example:
- Progressive disclosure says: "Show basic tools first"
- Dynamic manifests implement: Runtime query of available tools based on context

See: [Dynamic Manifests: Configuration](./dynamic-manifests.md#configuration)

### Progressive Disclosure → [Deferred Loading](./deferred-loading.md)

Progressive disclosure = **what to show**
Deferred loading = **when to load**

Example:
- Progressive disclosure: "Advanced feature hidden until clicked"
- Deferred loading: "Advanced feature code loaded on first access"

See: [Deferred Loading: Strategies](./deferred-loading.md#strategies)

### Progressive Disclosure in MCP

MCP Skills use progressive disclosure:
```
User starts → Basic skills available
  ↓
User works with Python files → Python skills appear
  ↓
User requests ML feature → ML skills loaded
```

Implemented via:
- Metadata scanning (what's available)
- Lazy loading (when to load)
- Context awareness (what to show)

See: [Skill Builder](../SKILL.md) for practical examples

---

## Measurement & Testing

### Key Metrics

Track these to validate progressive disclosure:

| Metric | Good | Bad |
|--------|------|-----|
| Time to first action | < 5s | > 30s |
| Feature discovery rate | > 70% | < 30% |
| User confusion (support tickets) | Decreasing | Increasing |
| Task completion rate | > 85% | < 60% |

### A/B Testing

```
Group A: Everything visible (control)
Group B: Progressive disclosure (test)

Measure:
- Time to complete common task
- Number of clicks
- Error rate
- User satisfaction
```

---

## Anti-Patterns

### ❌ Hiding Critical Information

```
❌ Bad: Hide error messages in collapsed section
✅ Good: Show errors prominently, hide resolution steps
```

### ❌ Too Many Levels

```
❌ Bad: Menu → Submenu → Submenu → Submenu → Action
✅ Good: Menu → Submenu → Action (max 3 levels)
```

### ❌ Inconsistent Disclosure

```
❌ Bad: Some settings in tabs, others in accordions, others in modals
✅ Good: Consistent pattern throughout app
```

### ❌ No Visual Cues

```
❌ Bad: Hidden features with no hint they exist
✅ Good: "⚙ Advanced settings" or "▼ Show more"
```

---

## Further Reading

- [Jakob Nielsen: Progressive Disclosure](https://www.nngroup.com/articles/progressive-disclosure/)
- [Information Architecture Basics](https://www.usability.gov/what-and-why/information-architecture.html)
- [Cognitive Load Theory](https://en.wikipedia.org/wiki/Cognitive_load)

---

**Navigation**: [← Back to Best Practices](../SKILL.md) | [Next: Dynamic Manifests →](./dynamic-manifests.md)

**Last Updated**: 2025-10-20
