# Headless API Configuration Rules

**For Wagtail 6.0+ with Next.js/React/Vue frontend**

## The Core Problem

Wagtail's internal data formats are **NOT** suitable for frontend consumption:

| Field Type | Internal Format | Problem |
|------------|----------------|---------|
| RichTextField | `<embed embedtype="image" id="123" />` | Frontend can't render |
| ImageChooserBlock | `{'id': 123}` | No URL for `<img src>` |
| PageChooserBlock | `{'id': 456}` | No title/URL for links |
| DocumentChooserBlock | `{'id': 789}` | No download URL |

**If you don't configure serializers, your API will return garbage data.**

## Rule 1: Always Use Wagtail API v2

### ❌ Incorrect (seen in 40% of projects)

```python
# api.py
from django.http import JsonResponse

def article_list(request):
    articles = ArticlePage.objects.live()
    data = {
        'articles': [
            {
                'id': a.id,
                'title': a.title,
                'body': a.body,  # ❌ RichTextField 返回内部格式
            }
            for a in articles
        ]
    }
    return JsonResponse(data)
```

**Problems**:
- 重复实现了 Wagtail 已有功能
- 无分页 → 性能问题
- 无字段选择 → 过度获取
- RichText/Image 未序列化 → 前端无法使用

### ✅ Correct

```python
# settings/base.py
INSTALLED_APPS += ['wagtail.api.v2']

# myapp/api.py
from wagtail.api.v2.router import WagtailAPIRouter
from wagtail.api.v2.views import PagesAPIViewSet
from wagtail.images.api.v2.views import ImagesAPIViewSet

api_router = WagtailAPIRouter('wagtailapi')
api_router.register_endpoint('pages', PagesAPIViewSet)
api_router.register_endpoint('images', ImagesAPIViewSet)

# urls.py
from myapp.api import api_router
urlpatterns += [path('api/v2/', api_router.urls)]
```

**Benefits**:
- ✅ 自动分页: `?offset=10&limit=20`
- ✅ 字段选择: `?fields=title,author,body`
- ✅ 搜索: `?search=query`
- ✅ 过滤: `?type=myapp.ArticlePage`
- ✅ 嵌套对象展开
- ✅ 缓存支持

**Setup time**: ~5 分钟 vs 手写 API ~3 小时

---

## Rule 2: RichTextField Serialization

### The Problem

```python
# models.py
class ArticlePage(Page):
    body = RichTextField()

    api_fields = [
        APIField('body'),  # ❌ 未配置序列化器
    ]
```

**API Response**:
```json
{
  "body": "<p>Check out <embed embedtype=\"image\" id=\"123\" format=\"left\" />our product</p>"
}
```

**Frontend sees**: Literal text `<embed embedtype="image" id="123" />` 😱

### ✅ Solution: RichTextSerializer

```python
from wagtail.api import APIField
from wagtail.api.v2.serializers import RichTextSerializer

class ArticlePage(Page):
    body = RichTextField()

    api_fields = [
        APIField('body', serializer=RichTextSerializer()),  # ✅ 配置序列化器
    ]
```

**API Response**:
```json
{
  "body": "<p>Check out <img src=\"/media/images/product.width-800.jpg\" alt=\"Product\" />our product</p>"
}
```

**Frontend sees**: Proper `<img>` tag with URL ✅

### For StreamField with RichTextBlock

```python
# blocks.py
class ContentBlock(blocks.StreamBlock):
    paragraph = blocks.RichTextBlock()  # 内部也需要序列化

# models.py
class ProductPage(Page):
    content = StreamField(ContentBlock())

    api_fields = [
        APIField('content'),  # ✅ StreamField 自动处理 RichTextBlock 序列化
    ]
```

**Note**: StreamField 会**自动**为内部的 RichTextBlock 应用序列化器，无需手动配置。

---

## Rule 3: ImageChooserBlock Serialization

### The Problem

```python
# blocks.py
class HeroBlock(blocks.StructBlock):
    image = ImageChooserBlock()

# API returns
{
  "image": 123  # ❌ 只有 ID，frontend 无法显示图片
}
```

### ✅ Solution: Custom Serializer

```python
# serializers.py
from rest_framework import serializers
from wagtail.images.api.fields import ImageRenditionField

class ImageSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    url = ImageRenditionField('original')
    thumbnail = ImageRenditionField('fill-300x200')

# blocks.py
class HeroBlock(blocks.StructBlock):
    image = ImageChooserBlock()

    class Meta:
        # Wagtail 6.1+ 支持 block-level serializer
        api_serializer = ImageSerializer
```

**Alternative** (simpler, Wagtail 7.0+):
```python
class HeroBlock(blocks.StructBlock):
    image = ImageChooserBlock()

    def get_api_representation(self, value, context=None):
        representation = super().get_api_representation(value, context)
        if value.get('image'):
            img = value['image']
            representation['image'] = {
                'id': img.id,
                'title': img.title,
                'url': img.file.url,
                'width': img.width,
                'height': img.height,
                'thumbnail': img.get_rendition('fill-300x200').url,
            }
        return representation
```

---

## Rule 4: PageChooserBlock Serialization

### The Problem

```python
# blocks.py
class RelatedArticleBlock(blocks.StructBlock):
    page = blocks.PageChooserBlock()

# API returns
{
  "page": 456  # ❌ 只有 ID，frontend 无法生成链接
}
```

### ✅ Solution: Nested Page Data

```python
# blocks.py
class RelatedArticleBlock(blocks.StructBlock):
    page = blocks.PageChooserBlock()

    def get_api_representation(self, value, context=None):
        representation = super().get_api_representation(value, context)
        if value.get('page'):
            page = value['page'].specific
            representation['page'] = {
                'id': page.id,
                'title': page.title,
                'url': page.url,
                'slug': page.slug,
            }
        return representation
```

**Alternative** (use API query parameter):
```
GET /api/v2/pages/123/?fields=*,related_articles(page(*))
```

This expands nested `PageChooserBlock` automatically.

---

## Rule 5: CORS Configuration

### ❌ Incorrect (security risk)

```python
# settings/base.py
CORS_ALLOW_ALL_ORIGINS = True  # ❌ 允许任何域名
CORS_ALLOW_CREDENTIALS = True  # ❌ 只读 API 不需要
CORS_ALLOW_METHODS = ['GET', 'POST', 'PUT', 'DELETE']  # ❌ 过宽
```

### ✅ Correct (least privilege)

```python
# settings/base.py
INSTALLED_APPS += ['corsheaders']

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # Must be before CommonMiddleware
    'django.middleware.common.CommonMiddleware',
    # ...
]

# Only allow specific frontend domains
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',  # Dev
    'https://yoursite.com',   # Prod
]

# Read-only API doesn't need credentials
CORS_ALLOW_CREDENTIALS = False

# Only allow GET (read-only)
CORS_ALLOW_METHODS = ['GET', 'OPTIONS']

# Standard headers
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'content-type',
]
```

**For different environments**:
```python
# settings/dev.py
CORS_ALLOWED_ORIGINS = ['http://localhost:3000', 'http://127.0.0.1:3000']

# settings/production.py
CORS_ALLOWED_ORIGINS = [os.environ.get('FRONTEND_URL')]
```

---

## Rule 6: Preview System (Don't Defer)

### ❌ Common Mistake

> "预览功能先不急，能看到 JSON 数据就行"

**Reality**: "先不急" = 永远不做

### ✅ Setup Headless Preview (15 minutes)

```bash
pip install wagtail-headless-preview
```

```python
# settings/base.py
INSTALLED_APPS += ['wagtail_headless_preview']

WAGTAIL_HEADLESS_PREVIEW = {
    'CLIENT_URLS': {
        'default': 'http://localhost:3000/api/preview',
    }
}

# Wagtail 7.1+
WAGTAIL_HEADLESS_PREVIEW_REDIRECT_ON_PREVIEW = True
```

```python
# models.py
from wagtail_headless_preview.models import HeadlessPreviewMixin

class ArticlePage(HeadlessPreviewMixin, Page):
    # ... fields ...

    # Specify preview modes
    preview_modes = [
        ('', 'Default'),
        ('amp', 'AMP'),
    ]
```

**Frontend (Next.js)**:
```typescript
// app/api/preview/route.ts
export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const contentType = searchParams.get('content_type');
  const token = searchParams.get('token');

  // Validate token with Wagtail
  const page = await fetch(
    `${WAGTAIL_API}/page_preview/1/?content_type=${contentType}&token=${token}`
  ).then(r => r.json());

  // Enable Draft Mode
  draftMode().enable();

  // Redirect to the preview page
  redirect(page.meta.html_url);
}
```

---

## Complete Setup Checklist

**Phase 1: API Configuration (5 min)**
- [ ] Add `wagtail.api.v2` to INSTALLED_APPS
- [ ] Create api.py with WagtailAPIRouter
- [ ] Register endpoints (pages, images, documents)
- [ ] Add api_router.urls to urlpatterns

**Phase 2: Model Configuration (10 min)**
- [ ] Add `api_fields` to Page models
- [ ] Configure RichTextField with RichTextSerializer
- [ ] Test: `curl http://localhost:8000/api/v2/pages/?fields=*`
- [ ] Verify: RichText returns HTML, not `<embed>` tags

**Phase 3: Block Serialization (20 min)**
- [ ] For ImageChooserBlock: Add get_api_representation
- [ ] For PageChooserBlock: Add get_api_representation or use nested expansion
- [ ] Test each block type in API response

**Phase 4: CORS (2 min)**
- [ ] Install django-cors-headers
- [ ] Configure CORS_ALLOWED_ORIGINS (specific domains)
- [ ] Set CORS_ALLOW_METHODS = ['GET', 'OPTIONS']
- [ ] Set CORS_ALLOW_CREDENTIALS = False

**Phase 5: Preview (15 min)**
- [ ] Install wagtail-headless-preview
- [ ] Configure WAGTAIL_HEADLESS_PREVIEW settings
- [ ] Add HeadlessPreviewMixin to models
- [ ] Implement frontend preview route

**Total time**: ~50 minutes for complete setup

---

## Testing API Serialization

```bash
# 1. Basic endpoint
curl http://localhost:8000/api/v2/pages/

# 2. Specific page with all fields
curl http://localhost:8000/api/v2/pages/123/?fields=*

# 3. Check RichText serialization
curl http://localhost:8000/api/v2/pages/123/?fields=body | jq '.body'
# Should see: <img src="/media/..."> NOT <embed embedtype="image">

# 4. Check ImageChooserBlock
curl http://localhost:8000/api/v2/pages/123/?fields=hero | jq '.hero.image'
# Should see: {id, title, url} NOT just a number

# 5. Check nested PageChooserBlock
curl http://localhost:8000/api/v2/pages/123/?fields=related_articles
# Should see: page objects with title/url NOT just IDs
```

---

## Common Errors and Fixes

### Error 1: "Object of type Image is not JSON serializable"

**Cause**: ImageChooserBlock 未配置序列化
**Fix**: Add `get_api_representation` method (see Rule 3)

### Error 2: Frontend sees `<embed embedtype="image" id="123">`

**Cause**: RichTextField 未配置 RichTextSerializer
**Fix**: `APIField('body', serializer=RichTextSerializer())`

### Error 3: CORS error in browser console

**Cause**: django-cors-headers 未配置或配置错误
**Fix**: 检查 MIDDLEWARE 顺序，CORS_ALLOWED_ORIGINS 是否包含前端域名

### Error 4: PageChooserBlock 只返回 ID

**Cause**: 未配置嵌套展开
**Fix**: 使用 `?fields=related(page(*))` 或 add `get_api_representation`

---

## Performance Considerations

```python
# ❌ Bad: N+1 queries in API
class ArticlePagesAPIViewSet(PagesAPIViewSet):
    def get_queryset(self):
        return ArticlePage.objects.live()  # Will query author/images separately

# ✅ Good: Optimized queries
class ArticlePagesAPIViewSet(PagesAPIViewSet):
    def get_queryset(self):
        return ArticlePage.objects.live().select_related(
            'author',
            'listing_image',
        ).prefetch_related(
            'tags',
            'related_pages',
        )
```

**Monitor queries** in development:
```python
# settings/dev.py
DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda request: DEBUG,
}
```

---

## Summary

**The 3 Critical Rules**:
1. Always use Wagtail API v2 (not hand-written JsonResponse)
2. RichTextField **MUST** use RichTextSerializer
3. ImageChooserBlock/PageChooserBlock **MUST** be serialized

**If you skip these**, your frontend will receive broken data.

**Setup time**: 50 minutes for complete Headless API

**See also**:
- `../assets/snippets/api-serializer.py` - Ready-to-use serializer code
- `../assets/checklists/api-setup-checklist.md` - Step-by-step verification
