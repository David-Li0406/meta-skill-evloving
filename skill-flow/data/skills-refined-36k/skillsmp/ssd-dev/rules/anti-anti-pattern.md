# Rule: Anti-Anti-Pattern

**避免 Synnovator 项目中的常见反模式**

## Core Principle

本项目基于 **Wagtail CMS + Django**，有特定的架构约束和最佳实践。违反这些规则会导致:
- 技术债积累
- 维护困难
- 用户体验下降
- 安全风险

## 反模式速查表

| ❌ 反模式 | ✅ 正确做法 | 原因 |
|-----------|-------------|------|
| Jinja2 模板语法 | Django Template 语法 | 项目配置使用 Django Templates |
| 硬编码业务逻辑在 Template | Admin 面板可配置 | 编辑需要修改内容 |
| 直接插入数据库 | Wagtail 数据添加模式 | 保持数据一致性 |
| Django View + URLconf | Wagtail Index Page | 统一路由管理 |
| 手写 API 端点 | Wagtail API v2 | 功能更完整 |
| 中文作为 msgid | 英文 msgid + 中文翻译 | 翻译系统要求 |

---

## Anti-Pattern 1: Jinja2 vs Django Template

### ❌ 错误: 使用 Jinja2 语法

```django
{# ❌ 多行注释用 {# #} - Jinja2 可以，Django 不行 #}
{#
    This is a multi-line comment
    It will SHOW on the page in Django!
#}

{# ❌ 条件中使用括号 - Jinja2 可以，Django 不行 #}
{% if (status == 'active' or status == 'pending') and user.is_authenticated %}

{# ❌ extends 前有内容 - Jinja2 可以，Django 不行 #}
{# Template documentation #}
{% extends "base.html" %}
```

### ✅ 正确: Django Template 语法

```django
{# ✅ 多行注释用 {% comment %} #}
{% comment %}
    This is a multi-line comment
    It will NOT render on the page
{% endcomment %}

{# ✅ 条件用嵌套 if 或 view 计算 #}
{% if user.is_authenticated %}
    {% if status == 'active' or status == 'pending' %}
        ...
    {% endif %}
{% endif %}

{# ✅ extends 必须是第一行 #}
{% extends "base.html" %}
{% load i18n static %}
{% comment %}Template documentation{% endcomment %}
```

### 检测方法

```bash
# 查找可能的 Jinja2 语法
grep -r "{#" templates/ --include="*.html" | grep -v "{% comment %}"
```

---

## Anti-Pattern 2: 硬编码业务逻辑在 Template

### ❌ 错误: Template 中硬编码

```django
{# ❌ 硬编码文案 #}
<h1>Welcome to Synnovator Hackathon Platform</h1>
<p>Join the world's best AI hackathons</p>

{# ❌ 硬编码业务规则 #}
{% if team.members.count >= 5 %}
    <p>Team is full</p>
{% endif %}

{# ❌ 硬编码链接 #}
<a href="https://github.com/synnovator">GitHub</a>
```

### ✅ 正确: Admin 面板可配置

```django
{# ✅ 从 Page 模型获取内容 #}
<h1>{{ page.title }}</h1>
<p>{{ page.subtitle }}</p>

{# ✅ 业务规则在 Model 中 #}
{% if team.is_full %}
    <p>{% trans "Team is full" %}</p>
{% endif %}

{# ✅ 链接从 Settings 或 Snippet 获取 #}
<a href="{{ settings.navigation.NavigationSettings.github_url }}">GitHub</a>
```

### 对应的 Model 实现

```python
# models.py
class Team(models.Model):
    MAX_MEMBERS = 5  # 可以改为 settings 或 admin 可配置

    @property
    def is_full(self):
        return self.members.count() >= self.MAX_MEMBERS


# navigation/models.py
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting

@register_setting
class NavigationSettings(BaseSiteSetting):
    github_url = models.URLField(blank=True)

    panels = [
        FieldPanel('github_url'),
    ]
```

### 检测方法

```bash
# 查找硬编码文案
grep -r "Welcome to" templates/ --include="*.html"
grep -r "http" templates/ --include="*.html" | grep -v "{% static" | grep -v "{% url"
```

---

## Anti-Pattern 3: 直接插入数据库

### ❌ 错误: 直接 create()

```python
# ❌ 直接创建 Wagtail Page
from synnovator.hackathons.models import HackathonPage

HackathonPage.objects.create(
    title="New Hackathon",
    slug="new-hackathon",
    depth=3,
    path="000100010001",  # 硬编码 path!
)

# ❌ Management command 直接插入
class Command(BaseCommand):
    def handle(self, *args, **options):
        for i in range(10):
            HackathonPage.objects.create(...)
```

### ✅ 正确: Wagtail 数据添加模式

```python
# ✅ 使用 add_child() 添加页面
from wagtail.models import Page

parent = Page.objects.get(slug="hackathons")
new_page = HackathonPage(
    title="New Hackathon",
    slug="new-hackathon",
)
parent.add_child(instance=new_page)

# ✅ 使用 Wagtail 的 revision 系统
new_page.save_revision().publish()

# ✅ 使用 Fixtures
# fixtures/demo.json
[
    {
        "model": "hackathons.hackathonpage",
        "pk": 1,
        "fields": {
            "title": "Demo Hackathon",
            "slug": "demo-hackathon"
        }
    }
]

# 加载
uv run python manage.py loaddata demo
```

### Wagtail Page 树结构

```
Root (path: 0001)
├── Home (path: 00010001)
├── Hackathons Index (path: 00010002)
│   ├── Hackathon 1 (path: 000100020001)
│   └── Hackathon 2 (path: 000100020002)
└── News Index (path: 00010003)
```

**关键**: `path` 和 `depth` 由 Wagtail 的 Treebeard 自动管理，**绝不能手动设置**。

### 检测方法

```bash
# 查找直接创建 Page 的代码
grep -r "Page.objects.create" synnovator/ --include="*.py"
grep -r "\.objects\.create" synnovator/ --include="*.py" | grep -i "page"
```

---

## Anti-Pattern 4: Django View 替代 Index Page

### ❌ 错误: 使用 Django View 做列表页

```python
# urls.py
urlpatterns = [
    path('hackathons/', views.hackathon_list, name='hackathon_list'),
]

# views.py
def hackathon_list(request):
    hackathons = HackathonPage.objects.live().public()
    return render(request, 'hackathon_list.html', {'hackathons': hackathons})
```

### ✅ 正确: 使用 Wagtail Index Page

```python
# models.py
class HackathonIndexPage(Page):
    intro = RichTextField(blank=True)
    featured_hackathon = models.ForeignKey(
        'HackathonPage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        FieldPanel('featured_hackathon'),
    ]

    subpage_types = ['hackathons.HackathonPage']
    max_count = 1

    def get_context(self, request):
        context = super().get_context(request)
        context['hackathons'] = (
            HackathonPage.objects.live().public()
            .descendant_of(self)
            .order_by('-first_published_at')
        )
        return context
```

### 为什么 Index Page 更好?

| 方面 | Django View | Index Page |
|------|-------------|------------|
| Admin 可见 | ❌ | ✅ |
| 编辑可管理 | ❌ | ✅ |
| SEO 控制 | 手动 | ✅ 内置 |
| URL 管理 | URLconf | ✅ Wagtail 路由 |
| 预览 | 需实现 | ✅ 内置 |

### 什么时候用 Django View?

- API 端点 (非内容)
- 表单处理 (POST)
- AJAX 请求
- Webhooks
- 认证相关

---

## Anti-Pattern 5: 中文作为翻译源

### ❌ 错误: 代码中用中文

```python
# ❌ 中文 msgid
from django.utils.translation import gettext as _

message = _("欢迎")  # WRONG!
title = _("用户列表")  # WRONG!

# ❌ 模型中用中文
class Event(models.Model):
    title = models.CharField("标题", max_length=200)  # WRONG!

    class Meta:
        verbose_name = "活动"  # WRONG!
```

```django
{# ❌ 模板中用中文 msgid #}
{% trans "欢迎" %}
```

### ✅ 正确: 英文 msgid + 中文翻译

```python
# ✅ 英文 msgid
from django.utils.translation import gettext as _
from django.utils.translation import gettext_lazy as _

message = _("Welcome")
title = _("User List")

# ✅ 模型用 gettext_lazy
class Event(models.Model):
    title = models.CharField(_("Title"), max_length=200)

    class Meta:
        verbose_name = _("Event")
        verbose_name_plural = _("Events")
```

```django
{# ✅ 模板用英文 msgid #}
{% load i18n %}
{% trans "Welcome" %}
```

```po
# locale/zh_Hans/LC_MESSAGES/django.po
msgid "Welcome"
msgstr "欢迎"

msgid "User List"
msgstr "用户列表"
```

### 翻译工作流

```bash
# 1. 提取字符串
make translate-ui

# 2. 编辑 PO 文件
# locale/zh_Hans/LC_MESSAGES/django.po

# 3. 编译
make compile-translations

# 4. 重启服务器
make start
```

### 检测方法

```bash
# 查找代码中的中文
grep -r "_(" synnovator/ --include="*.py" | grep "[\u4e00-\u9fff]"

# 查找模板中未翻译的中文
grep -r "[\u4e00-\u9fff]" templates/ --include="*.html" | grep -v "{% trans" | grep -v "{% blocktrans"
```

---

## Anti-Pattern 6: 手写 API 替代 Wagtail API v2

### ❌ 错误: 手写 REST API

```python
# ❌ 手写 API
from django.http import JsonResponse

def hackathon_api(request):
    hackathons = HackathonPage.objects.live()
    data = []
    for h in hackathons:  # N+1 问题
        data.append({
            'title': h.title,
            'description': h.description,
            # 忘记分页、过滤、字段选择...
        })
    return JsonResponse({'items': data})
```

### ✅ 正确: 使用 Wagtail API v2

```python
# api.py
from wagtail.api.v2.views import PagesAPIViewSet
from wagtail.api.v2.router import WagtailAPIRouter

api_router = WagtailAPIRouter('wagtailapi')


class HackathonAPIViewSet(PagesAPIViewSet):
    model = HackathonPage

    body_fields = PagesAPIViewSet.body_fields + [
        'description',
        'status',
        'start_date',
    ]

    listing_default_fields = PagesAPIViewSet.listing_default_fields + [
        'description',
        'status',
    ]


api_router.register_endpoint('hackathons', HackathonAPIViewSet)

# urls.py
urlpatterns = [
    path('api/v2/', api_router.urls),
]
```

### API v2 自动提供

- ✅ 分页: `?limit=10&offset=20`
- ✅ 字段选择: `?fields=title,description`
- ✅ 过滤: `?status=active`
- ✅ 搜索: `?search=AI`
- ✅ 排序: `?order=-start_date`
- ✅ 缓存机制

---

## 检测脚本

将以下脚本保存为 `scripts/check_anti_patterns.sh`:

```bash
#!/bin/bash
echo "=== Checking for anti-patterns ==="

echo -e "\n1. Jinja2 syntax in templates:"
grep -rn "{#" templates/ --include="*.html" | grep -v "{% comment %}" | head -5

echo -e "\n2. Hardcoded URLs in templates:"
grep -rn "http://" templates/ --include="*.html" | grep -v "{% static" | head -5
grep -rn "https://" templates/ --include="*.html" | grep -v "{% static" | head -5

echo -e "\n3. Direct Page.objects.create:"
grep -rn "\.objects\.create" synnovator/ --include="*.py" | grep -i "page" | head -5

echo -e "\n4. Chinese in msgid:"
grep -rn "_(" synnovator/ --include="*.py" 2>/dev/null | grep -E "[\u4e00-\u9fff]" | head -5

echo -e "\n5. Untranslated Chinese in templates:"
grep -rn "[\u4e00-\u9fff]" templates/ --include="*.html" 2>/dev/null | grep -v "{% trans" | grep -v "{% blocktrans" | head -5

echo -e "\n=== Done ==="
```

## Checklist

代码提交前检查:

- [ ] 没有使用 Jinja2 特有语法
- [ ] Template 中无硬编码业务文案
- [ ] Page 创建使用 `add_child()` 而非 `create()`
- [ ] 列表页使用 Index Page 而非 Django View
- [ ] 所有 msgid 使用英文
- [ ] API 使用 Wagtail API v2

参考: 更多反模式见 `wagtail-builder` skill 的 `references/anti-patterns.md`
