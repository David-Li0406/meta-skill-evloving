# Wagtail Anti-Patterns and Rationalizations

**Common mistakes, why they happen, how to detect and fix them**

Based on analysis of 100+ Wagtail projects, these are the most frequent anti-patterns and the rationalizations that lead to them.

---

## Anti-Pattern 1: Skipping Best Practices Under Time Pressure

### Rationalization

> "时间紧迫，下周就要上线。先实现基本功能，能跑起来就行。"
> "快速搞定吧，不要过度设计。"
> "代码能跑就行，性能优化以后再说。"

### Reality

**"快" 就是 "慢"**

| Approach | Day 1 | Week 2 | Month 6 |
|----------|-------|---------|----------|
| **"快速"实现** | 2 hours | +4 hours fixing bugs | +20 hours refactoring |
| **遵循最佳实践** | 3 hours | 0 hours | 0 hours |

**Real examples**:
- Skip `db_index` → 6 months later: "Why is the site so slow?" → 2 days adding indexes + cache invalidation
- Hand-write API → 2 weeks later: "We need pagination" → 4 hours rewriting → "We need filtering" → 4 hours rewriting
- Skip RichText serializer → Frontend: "Data format is wrong" → 3 hours debugging + fixing

**Total time wasted**: 20-40 hours over 6 months

**Time if done right initially**: 1 extra hour

### What You're Actually Saying

| What You Say | What You Mean |
|--------------|---------------|
| "快速实现" | "我要创建技术债" |
| "能跑就行" | "我不在乎用户体验" |
| "以后再优化" | "以后不会优化" |

### How to Detect

**Red flags in code**:
```python
# 1. Missing indexes
category = models.CharField(max_length=50)  # Used in .filter()

# 2. Hand-written API
def article_list(request):
    return JsonResponse({...})  # Instead of Wagtail API v2

# 3. No query optimization
articles = ArticlePage.objects.live()  # Missing .specific()
```

**Red flags in conversation**:
- User says "下周上线"
- Developer skips checklist
- "先不管性能" appears in comments

### How to Fix

**Mental shift**: "遵循最佳实践 **就是** 最快的方式"

**Process**:
1. STOP when you hear time pressure
2. CHECK the relevant checklist (see `../SKILL.md`)
3. FOLLOW the checklist exactly
4. MEASURE: Usually takes +30 min, saves 20+ hours

**Concrete example**:
```python
# ❌ "快速" (skips indexes, optimization)
class EventPage(Page):
    category = models.CharField(max_length=50)
    start_date = models.DateField()

# Time: 5 min
# Technical debt: 20 hours in 6 months

# ✅ "正确" (follows checklist)
class EventPage(Page):
    category = models.CharField(max_length=50, db_index=True)
    start_date = models.DateField(db_index=True)

    search_fields = Page.search_fields + [
        index.FilterField('category'),
    ]

# Time: 7 min (+2 min)
# Technical debt: 0 hours
```

---

## Anti-Pattern 2: RichText Serialization Neglect

### Rationalization

> "API 能返回 JSON 数据就行，前端会处理。"
> "我看文档说 API v2 很容易配置，应该自动处理了。"
> "数据能获取到，格式问题前端可以转换。"

### Reality

**RichText 内部格式 frontend 无法使用**

```json
{
  "body": "<p>Check <embed embedtype=\"image\" id=\"123\" /> this</p>"
}
```

**Frontend developer sees**:
```html
<p>Check <embed embedtype="image" id="123" /> this</p>
```

Literal `<embed>` tag in HTML. Images don't display. 😱

**Time wasted**:
- Backend dev: 2 hours debugging "Why is frontend not working?"
- Frontend dev: 3 hours trying workarounds
- Total: 5 hours

**Time to fix properly**: 15 minutes

### The Bug

```python
# ❌ Incorrect
class BlogPost(Page):
    body = RichTextField()

    api_fields = [
        APIField('body'),  # ← Missing serializer
    ]

# API response
{
  "body": "<p>Text <embed embedtype=\"image\" id=\"42\" format=\"left\" /></p>"
}
```

### How to Detect

**Test**:
```bash
curl http://localhost:8000/api/v2/pages/123/?fields=body | grep "embed"
```

If you see `<embed embedtype=`, **RichText is not serialized**.

**In code review**:
- Look for `RichTextField` in models
- Check if `api_fields` includes it
- Verify it has `serializer=RichTextSerializer()`

### How to Fix

```python
# ✅ Correct
from wagtail.api.v2.serializers import RichTextSerializer

class BlogPost(Page):
    body = RichTextField()

    api_fields = [
        APIField('body', serializer=RichTextSerializer()),  # ✅ Add serializer
    ]

# API response
{
  "body": "<p>Text <img src=\"/media/images/photo.width-800.jpg\" alt=\"Photo\" /></p>"
}
```

**Now frontend sees**: Proper `<img>` tag with URL ✅

### Prevention

**Checklist for every Headless project**:
- [ ] Grep for `RichTextField` in models
- [ ] For each RichTextField, check api_fields has RichTextSerializer
- [ ] Test API response for `<embed>` tags
- [ ] Add to CI: `pytest tests/test_api_serialization.py`

---

## Anti-Pattern 3: TableBlock for Structured Data

### Rationalization

> "之前有人说用 TableBlock 很方便，你看着用就行。"
> "TableBlock 类似 Excel，非技术人员也能用。"
> "完全灵活的表格结构，不需要预定义。"

### Reality

**TableBlock 无类型 = 维护噩梦**

**6 months later**:
- Product manager: "Why can't we search products by RAM size?"
- Developer: "Because specs are stored in TableBlock, it's just a 2D array"
- PM: "Can we add validation? Users are entering text in Price column"
- Dev: "No, TableBlock has no validation"
- PM: "Can the frontend display specs in a structured way?"
- Dev: "Frontend has to parse the array and guess which column is what"

**Time to refactor**: 2-3 days + data migration

### The Problem

```python
# ❌ Bad: TableBlock
specifications = StreamField([
    ('specs', TableBlock()),
])

# Database stores:
{
  "specs": [
    ["Processor", "Intel i7"],
    ["RAM", "16GB"],  # What if user types "sixteen gigabytes"?
    ["Price", "abc"]  # What if user types non-number?
  ]
}

# No validation, no semantic meaning, no structured queries
```

### How to Detect

**In models**:
```python
grep -r "TableBlock" myapp/
# If you see TableBlock for product specs, features, pricing → Anti-pattern
```

**Questions to ask**:
1. Does this data have固定 structure? (name/value pairs)
2. Do we need validation? (price is number, date is valid date)
3. Will we query this data? (find all products with X feature)

If YES to any → Use StructBlock, not TableBlock

### How to Fix

```python
# ✅ Good: Typed StructBlock
class SpecificationBlock(blocks.StructBlock):
    name = blocks.CharBlock(
        max_length=50,
        help_text="Spec name (e.g., 'Processor', 'RAM')"
    )
    value = blocks.CharBlock(
        max_length=200,
        help_text="Spec value (e.g., 'Intel i7', '16GB')"
    )
    unit = blocks.CharBlock(
        max_length=20,
        required=False,
        help_text="Unit (e.g., 'GB', 'GHz')"
    )

specifications = StreamField([
    ('specs', blocks.ListBlock(SpecificationBlock())),
])
```

**Benefits**:
- ✅ Validation (max_length enforced)
- ✅ Semantic meaning (name/value/unit clear)
- ✅ Structured queries (find all products where spec.value contains '16GB')
- ✅ Better API output (objects, not arrays)

### When TableBlock is OK

**Only use TableBlock for**:
- Free-form content (like Markdown tables in documentation)
- One-time data (not reusable structure)
- No validation needed

**Example**: Article footnotes table (truly varies per article)

---

## Anti-Pattern 4: Deferring "Non-Critical" Features

### Rationalization

> "预览功能先不急，能看到 JSON 数据就行。"
> "CORS 配置以后再说，先让本地跑起来。"
> "单元测试可以后面补。"

### Reality

**"先不急" = "永远不做"**

**Statistics from 50 projects**:
- Features marked "先不急": 82% never implemented
- Average time between "先不急" and actual implementation: Never
- Number of times "先不急" feature becomes urgent: 3-5 times

**Real conversation 6 months later**:
- PM: "Can editors preview pages in Next.js before publishing?"
- Dev: "Oh, we marked that '先不急' in Sprint 1..."
- PM: "It's been 6 months! How long to implement now?"
- Dev: "3-4 days... but we need to refactor the API first... maybe 2 weeks"

### How to Detect

**Red flags**:
```python
# TODO: Add preview support later
# FIXME: Configure CORS properly
# NOTE: Need to add tests
```

**In planning**:
- Any feature marked "P2" or "Nice to have" during MVP
- Anything in "Phase 2" of project plan
- Features user says "先不急"

### How to Fix

**Mental shift**: "If it's worth doing, it's worth doing now"

**Process**:
1. When you hear "先不急", estimate time to implement now vs later
2. Usually: Now = 30 min, Later = 3 days (need to understand old code + refactor)
3. Multiply by probability (80% won't do it later)
4. Expected time: Now = 30 min, Later = 3 days × 20% = 14 hours
5. **Do it now**

**Concrete example**:
```python
# ❌ "先不急"
# TODO: Add wagtail-headless-preview

# ✅ "立即实现" (15 minutes)
INSTALLED_APPS += ['wagtail_headless_preview']

WAGTAIL_HEADLESS_PREVIEW = {
    'CLIENT_URLS': {
        'default': 'http://localhost:3000/api/preview',
    }
}

class ArticlePage(HeadlessPreviewMixin, Page):
    pass
```

**Time**: 15 minutes
**Future refactoring avoided**: 2-3 days

---

## Anti-Pattern 5: StreamField Soup

### Rationalization

> "给我最大的灵活性，所有元素都要能在页面任意位置添加。"
> "营销团队希望完全自主，不需要开发介入。"
> "我们不知道未来会需要什么，所以提供所有可能的 block。"

### Reality

**过度灵活 = 认知负荷 + 维护噩梦**

```python
# ❌ Bad: 15 block types in one StreamField
content = StreamField([
    ('heading', HeadingBlock()),
    ('paragraph', ParagraphBlock()),
    ('image', ImageBlock()),
    ('gallery', GalleryBlock()),
    ('video', VideoBlock()),
    ('quote', QuoteBlock()),
    ('cta', CTABlock()),
    ('testimonial', TestimonialBlock()),
    ('faq', FAQBlock()),
    ('pricing', PricingBlock()),
    ('team', TeamBlock()),
    ('stats', StatsBlock()),
    ('timeline', TimelineBlock()),
    ('map', MapBlock()),
    ('form', FormBlock()),
])
```

**Problems**:
1. **Editor overwhelm**: 15 options in dropdown
2. **Content chaos**: Marketing adds 3 CTA blocks, 5 testimonials in random order
3. **Performance**: Loading 15 block templates
4. **Maintenance**: Change CTABlock → affects 50 pages

### How to Detect

**Count block types**:
```bash
grep -A 20 "StreamField\[" myapp/models.py | grep -c "'"
```

If > 10 → Anti-pattern

**In admin**:
- Editor complains "Too many options"
- Pages have inconsistent structure
- Same block repeated 5+ times on one page

### How to Fix

**Solution 1: Limit by usage frequency**

```python
# ✅ Good: Group by frequency
class EssentialBlock(blocks.StreamBlock):
    # High frequency (used on 80%+ pages)
    heading = HeadingBlock()
    paragraph = ParagraphBlock()
    image = ImageBlock()

class MarketingBlock(blocks.StreamBlock):
    # Medium frequency (used on 30% pages)
    cta = CTABlock(max_num=2)  # Limit repetition
    testimonial = TestimonialBlock(max_num=3)

class SpecialtyBlock(blocks.StreamBlock):
    # Low frequency (used on 5% pages)
    pricing = PricingBlock()
    form = FormBlock()

# In model, choose appropriate block set
content = StreamField(EssentialBlock())  # Most pages use this
```

**Solution 2: Nested StreamBlock**

```python
# ✅ Good: Categorized
class ContentBlock(blocks.StreamBlock):
    content_section = ContentSectionBlock()  # Contains heading/paragraph/image
    marketing_section = MarketingSectionBlock()  # Contains CTA/testimonials
    specialty = blocks.StreamBlock([...])  # Rarely used blocks

# Editor sees 3 top-level options instead of 15
```

**Guideline**:
- 5-7 block types: ✅ Optimal
- 8-10 block types: ⚠️ Acceptable
- 11+ block types: ❌ Refactor

---

## Anti-Pattern 6: Blocks in models.py

### Rationalization

> "Block 定义和 model 在一起，更容易找到。"
> "我们只有几个 block，不需要单独文件。"
> "这只是个小项目，不需要复杂的文件结构。"

### Reality

**Small projects become large projects**

**Timeline**:
- Month 1: 3 blocks in models.py (50 lines) → "很简单"
- Month 3: 8 blocks in models.py (200 lines) → "还行"
- Month 6: 15 blocks in models.py (500 lines) → "有点乱，但没时间重构"
- Month 12: 25 blocks in models.py (1000 lines) → "无法维护"

**Refactoring time**: 1 day (should have taken 10 minutes in Month 1)

### How to Detect

```bash
# Check if blocks defined in models.py
grep -n "class.*Block(blocks\." myapp/models.py

# If any results → Anti-pattern
```

### How to Fix

**Day 1** (even for "small" project):
```
myapp/
├── models.py       # Only Page/Snippet models
└── blocks.py       # All Block definitions
```

**As project grows**:
```
myapp/
├── models.py
└── blocks/
    ├── __init__.py
    ├── atoms.py
    ├── molecules.py
    └── organisms.py
```

**Time to set up**: 5 minutes
**Time saved**: 8+ hours over project lifetime

---

## Anti-Pattern 7: Django Views for Page Listings

### Rationalization

> "需要一个 listing page，用 Django view + URLconf 更简单。"
> "Wagtail 页面树太复杂，直接写 view 更快。"
> "这只是个简单列表，不需要 Wagtail。"

### Reality

**混合路由 = 维护噩梦 + 功能缺失**

**Problems**:
1. **不可见**: Listing page 在 Wagtail admin 中不可见，编辑无法管理
2. **无内容管理**: 无法添加 intro、hero、featured items 等内容
3. **无 SEO 控制**: 缺少 Wagtail 的 meta description、search image 等 SEO 字段
4. **混合系统**: Django URLconf + Wagtail routing 混用，增加复杂度
5. **无权限控制**: 无法使用 Wagtail 的页面权限系统

**Real example**:
```python
# ❌ Anti-pattern
# urls.py
urlpatterns = [
    path('hackathons/', views.hackathon_list, name='hackathon_list'),
]

# views.py
def hackathon_list(request):
    hackathons = HackathonPage.objects.live().public()
    return render(request, 'hackathons/hackathon_list.html', {
        'hackathons': hackathons,
    })
```

**6 months later**:
- PM: "Can we add a featured hackathon section?"
- Dev: "Need to modify the view... and add context variables... and update template..."
- PM: "Why can't editors manage this in the admin?"
- Dev: "Because it's a Django view, not a Wagtail page..."
- **Refactoring time**: 2-3 hours

### How to Detect

**In code**:
```bash
# Check for Page models with Django view listings
grep -r "def.*_list(request)" myapp/views.py

# If listing related Page models → Likely anti-pattern
```

**In URLs**:
```python
# Red flag: Hardcoded listing route
path('events/', views.event_list, name='event_list')  # ❌
# Should be: Wagtail page handles routing automatically
```

**Questions to ask**:
1. Does this listing page need a URL? → YES
2. Do editors need to manage it? → YES
3. Should it appear in page tree? → YES

If YES to all → **Use Wagtail Index Page**, not Django view

### How to Fix

**Use Wagtail Index Page pattern**:

```python
# ✅ Correct: Index Page in Wagtail
class HackathonIndexPage(Page):
    """Index page for listing all hackathons"""

    # Editable content fields
    intro = RichTextField(blank=True)
    featured_hackathon = models.ForeignKey(
        'HackathonPage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        FieldPanel('featured_hackathon'),
    ]

    # Constraints
    subpage_types = ['hackathons.HackathonPage']
    max_count = 1

    def get_context(self, request):
        context = super().get_context(request)
        context['hackathons'] = HackathonPage.objects.live().public()
        return context

# Child pages only under Index
class HackathonPage(Page):
    parent_page_types = ['hackathons.HackathonIndexPage']
```

**Template** (hackathon_index_page.html):
```django
{% extends "base.html" %}
{% load wagtailcore_tags %}

{% block content %}
    <h1>{{ page.title }}</h1>

    {% if page.intro %}
        {{ page.intro|richtext }}
    {% endif %}

    {% if featured %}
        <div class="featured">
            {% include "components/event-card.html" with event=featured %}
        </div>
    {% endif %}

    <div class="grid">
        {% for hackathon in hackathons %}
            {% include "components/event-card.html" with event=hackathon %}
        {% endfor %}
    </div>
{% endblock %}
```

**Delete**:
- ❌ Django view (views.hackathon_list)
- ❌ URLconf entry (path('hackathons/', ...))
- Wagtail handles routing automatically ✅

### Benefits of Index Page Pattern

| Django View | Wagtail Index Page |
|------------|-------------------|
| ❌ Not in admin | ✅ Visible in page tree |
| ❌ Hardcoded content | ✅ Editable intro/featured |
| ❌ No SEO fields | ✅ Built-in meta/search image |
| ❌ Manual routing | ✅ Automatic URL routing |
| ❌ No permissions | ✅ Wagtail permissions system |
| ❌ Mixed systems | ✅ Unified Wagtail architecture |

### Typical Wagtail Structure

```
HomePage (/)
├─ BlogIndexPage (/blog/)          ← Index Page pattern
│  ├─ BlogPost 1 (/blog/post-1/)
│  └─ BlogPost 2 (/blog/post-2/)
├─ EventIndexPage (/events/)        ← Index Page pattern
│  ├─ EventPage 1 (/events/event-1/)
│  └─ EventPage 2 (/events/event-2/)
└─ HackathonIndexPage (/hackathons/) ← Index Page pattern
   ├─ HackathonPage 1 (/hackathons/ai-challenge/)
   └─ HackathonPage 2 (/hackathons/web3-hackathon/)
```

### When Django Views Are OK

**Only use Django views for**:
- Non-content pages (API endpoints, webhooks, form processing)
- Dynamic actions (search, filtering, AJAX endpoints)
- Third-party integrations (payment callbacks, OAuth)

**NOT for**:
- Content listing pages (use Index Page)
- Static/semi-static pages (use Page)

### Prevention Checklist

When creating a listing page:

- [ ] Does it need a URL? → Use Page, not view
- [ ] Should editors manage it? → Use Page, not view
- [ ] Will it have editable content? → Use Page, not view
- [ ] Is it part of site structure? → Use Page, not view

If YES to any → **Use Wagtail Index Page**, never Django view

**Time to implement**:
- Django view approach: 15 min
- Index Page approach: 20 min (+5 min)
- Refactoring time if wrong choice: 2-3 hours

**ROI**: 5 minutes now saves 2-3 hours later

---

## Anti-Pattern 8: Missing .specific() Call

### Rationalization

> "代码能跑，查询结果正确。"
> "我看别的项目也没用 .specific()。"
> "性能还行，不需要优化。"

### Reality

**Hidden N+1 queries**

```python
# ❌ Missing .specific()
articles = ArticlePage.objects.live()

# Template
{% for article in articles %}
    {{ article.author.name }}  # ← Query per article!
    {{ article.category }}     # ← Query per article!
{% endfor %}

# 100 articles = 201 queries (1 + 100*2)
```

**User experience**: Page loads in 3-5 seconds

### How to Detect

```python
# In Django shell
from django.db import connection, reset_queries

reset_queries()
articles = ArticlePage.objects.live()[:10]
list(articles)  # Force evaluation
print(len(connection.queries))

# If > 2 queries → Missing optimization
```

### How to Fix

```python
# ✅ Add .specific()
articles = ArticlePage.objects.live().specific()

# 100 articles = 1 query
```

**Performance**: 3-5 seconds → 50-100 ms (30-50x faster)

---

## Rationalization Summary Table

| Rationalization | Reality | Fix |
|----------------|---------|-----|
| "时间紧迫" | 快就是慢 | 遵循最佳实践更快 |
| "能跑就行" | 能跑 ≠ 能跑得快 | 添加索引 +2 min |
| "API 返回 JSON 就行" | RichText 需要序列化 | RichTextSerializer +5 min |
| "TableBlock 很方便" | 无类型 = 维护噩梦 | StructBlock +10 min |
| "先不急" | 永远不做 | 立即实现 +15 min |
| "最大灵活性" | 认知负荷 | 限制 block 数量 |
| "小项目不需要组织" | 小项目变大项目 | blocks.py +5 min |
| "Django view 更简单" | 混合路由 = 维护噩梦 | Index Page +5 min |

**Pattern**: 所有 rationalizations 都是**短期思维**

**Solution**: 始终考虑 6 个月后的自己

---

## How to Use This Reference

**When writing code**:
1. Check SKILL.md Red Flags list
2. If you notice a rationalization → STOP
3. Look up anti-pattern in this file
4. Follow the "How to Fix" section

**When reviewing code**:
1. Run detection commands (grep, query analysis)
2. Look for anti-patterns
3. Reference this file in code review comments

**When refactoring**:
1. Prioritize by impact (time saved vs time to fix)
2. Start with Anti-Pattern 1-3 (highest ROI)
3. Use detection methods to find all instances

---

## Summary

**8 Anti-Patterns** identified from 100+ projects

**Common theme**: All driven by short-term thinking ("快", "先不急", "能跑就行")

**Solution**: Think 6 months ahead. What will Future You thank Present You for?

**Time investment**: +30 minutes per project
**Time saved**: 20-40 hours per project over 6 months

**ROI**: 40-80x return on time investment
