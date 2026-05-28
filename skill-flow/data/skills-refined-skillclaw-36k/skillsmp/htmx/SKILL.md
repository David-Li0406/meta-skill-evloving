---
name: htmx
description: HTMX patterns for server-driven interactivity, WebSocket real-time updates, and progressive enhancement
activation_keywords:
  - htmx
  - hx-get
  - hx-post
  - hx-swap
  - hx-trigger
  - websocket
  - html fragments
  - server-driven
  - hypermedia
invoke_as: htmx
---

# HTMX Development Patterns

Server-driven interactivity using HTML over the wire.

---

## Core Concepts

HTMX extends HTML with attributes that enable AJAX, WebSockets, and server-sent events directly in markup. The server returns HTML fragments, not JSON.

**Philosophy:** HTML is the API. Server renders, client displays.

---

## Essential Attributes

| Attribute | Purpose | Example |
|-----------|---------|---------|
| `hx-get` | GET request | `hx-get="/api/v1/html/items"` |
| `hx-post` | POST request | `hx-post="/api/v1/html/items"` |
| `hx-put` | PUT request | `hx-put="/api/v1/html/items/1"` |
| `hx-delete` | DELETE request | `hx-delete="/api/v1/html/items/1"` |
| `hx-trigger` | Event that triggers request | `hx-trigger="click"` |
| `hx-target` | Element to update | `hx-target="#list"` |
| `hx-swap` | How to swap content | `hx-swap="innerHTML"` |
| `hx-indicator` | Loading indicator | `hx-indicator="#spinner"` |
| `hx-confirm` | Browser confirmation | `hx-confirm="Delete?"` |
| `hx-vals` | Additional values | `hx-vals='{"key": "value"}'` |

---

## Swap Strategies

| Strategy | Behavior |
|----------|----------|
| `innerHTML` | Replace children (default) |
| `outerHTML` | Replace entire element |
| `beforebegin` | Insert before element |
| `afterbegin` | Insert as first child |
| `beforeend` | Insert as last child |
| `afterend` | Insert after element |
| `delete` | Delete element |
| `none` | No swap (for side effects) |

---

## Trigger Patterns

### Common Triggers

| Trigger | When It Fires |
|---------|---------------|
| `load` | On element load |
| `click` | On click |
| `change` | On input change |
| `submit` | On form submit |
| `keyup` | On key release |
| `revealed` | When element becomes visible |
| `intersect` | When element enters viewport |

### Modifiers

```html
<!-- Single fire -->
hx-trigger="load once"
hx-trigger="intersect once"

<!-- Debounce input -->
hx-trigger="keyup changed delay:300ms"

<!-- Multiple triggers -->
hx-trigger="load, itemCreated from:body"

<!-- Polling -->
hx-trigger="every 5s"
```

---

## Project Patterns (In Use)

### Page Load Pattern

Used on every page to load initial content:

```html
<div
  id="content-container"
  hx-get="/api/v1/html/content"
  hx-trigger="load"
  hx-swap="innerHTML"
>
  <!-- Loading skeleton shown while fetching -->
  <div class="animate-pulse">Loading...</div>
</div>
```

### Lazy Load Pattern (Tabs)

Used for tab content that loads when tab becomes visible:

```html
<div
  id="browse-list-container"
  hx-get="/api/v1/html/browse"
  hx-trigger="intersect once"
  hx-swap="innerHTML"
>
  <div class="animate-pulse">Loading...</div>
</div>
```

### Search with Debounce

Used in gear library for real-time search:

```html
<input
  type="search"
  name="q"
  placeholder="Search gear..."
  hx-get="/api/v1/html/library/my-gear"
  hx-trigger="keyup changed delay:300ms"
  hx-target="#gear-list-container"
  hx-include="[name='gear_type'],[name='sort']"
  class="w-full px-3 py-2 bg-bg-surface border border-border rounded-md"
/>
```

### Filter Buttons

Used for gear type filtering:

```html
<div class="flex gap-2 flex-wrap">
  {% for type in ['All', 'Amp', 'Pedal', 'IR', 'Full-Rig', 'Outboard'] %}
  <button
    name="gear_type"
    value="{{ type if type != 'All' else '' }}"
    hx-get="/api/v1/html/library/my-gear"
    hx-target="#gear-list"
    hx-include="[name='q'],[name='sort']"
    class="px-3 py-1 rounded-full text-sm {{ active_class if current_type == type else inactive_class }}"
  >
    {{ type }}
  </button>
  {% endfor %}
</div>
```

### Dropdown with HTMX

Used for sort options:

```html
<select
  name="sort"
  hx-get="/api/v1/html/library/my-gear"
  hx-target="#gear-list"
  hx-include="[name='q'],[name='gear_type']"
  class="bg-bg-surface border border-border rounded-md px-3 py-2"
>
  <option value="name">Name (A-Z)</option>
  <option value="-name">Name (Z-A)</option>
  <option value="-created_at">Newest</option>
</select>
```

### Model Save/Unsave (Toggle Button)

Used for saving/removing models from user's gear with toast notification:

```html
<!-- Single toggle endpoint handles both states -->
<button
  data-testid="model-save-btn"
  hx-post="/api/v1/html/gear/model/{{ model.id }}/toggle"
  hx-target="closest [data-testid='model-row']"
  hx-swap="outerHTML"
  class="px-3 py-1 rounded {{ 'bg-green-500' if model.is_saved else 'bg-gray-500' }}"
>
  {{ 'Saved' if model.is_saved else 'Save' }}
</button>
```

The toggle endpoint returns an HX-Trigger header for toast notifications.

### Delete with Confirmation

Used for DI track deletion:

```html
<button
  data-testid="track-delete-btn"
  hx-delete="/api/v1/html/library/tracks/{{ track.id }}"
  hx-target="closest [data-testid='track-item']"
  hx-swap="outerHTML"
  hx-confirm="Delete this track? This cannot be undone."
  class="text-red-500 hover:text-red-400"
>
  Delete
</button>
```

### Pagination (Infinite Scroll)

Used for loading more items:

```html
{% if has_more %}
<div
  hx-get="/api/v1/html/library/items?page={{ page + 1 }}"
  hx-trigger="revealed"
  hx-swap="outerHTML"
  class="py-4 text-center"
>
  <span class="text-muted-foreground">Loading more...</span>
</div>
{% endif %}
```

### Pagination (Page Numbers)

Used when specific pages are needed:

```html
<div class="flex items-center gap-2">
  {% if page > 1 %}
  <button
    hx-get="/api/v1/html/items?page={{ page - 1 }}"
    hx-target="#items-container"
    class="px-3 py-1 bg-bg-surface rounded"
  >
    Previous
  </button>
  {% endif %}

  <span>Page {{ page }} of {{ total_pages }}</span>

  {% if page < total_pages %}
  <button
    hx-get="/api/v1/html/items?page={{ page + 1 }}"
    hx-target="#items-container"
    class="px-3 py-1 bg-bg-surface rounded"
  >
    Next
  </button>
  {% endif %}
</div>
```

---

## FastAPI HTML Fragment Endpoints

### Basic Fragment Endpoint

```python
from fastapi import APIRouter, Request, Depends
from app.api.deps import CurrentUser
from app.core.templates import templates

router = APIRouter(prefix="/api/v1/html", tags=["html"])

@router.get("/library/items")
async def get_items_fragment(
    request: Request,
    user: CurrentUser,
    page: int = 1,
    q: str | None = None,
    sort: str = "name",
):
    """Return HTML fragment for HTMX."""
    items = await item_service.get_items(
        user_id=user.id,
        page=page,
        search=q,
        sort=sort,
    )
    return templates.TemplateResponse(
        request=request,
        name="fragments/library/items.html",
        context={
            "items": items.items,
            "page": page,
            "has_more": items.has_more,
        },
    )
```

### POST Endpoint (Toggle)

```python
@router.post("/gear/model/{model_id}/toggle")
async def toggle_gear_model(
    request: Request,
    model_id: UUID,
    user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    """Toggle save/unsave state for a model with toast notification."""
    # ... toggle logic ...
    response = templates.TemplateResponse(
        request=request,
        name="fragments/gear/model_row.html",
        context={"model": model_data},
    )
    # Add toast notification trigger
    response.headers["HX-Trigger"] = json.dumps({
        "showToast": {"message": toast_message, "type": "success"}
    })
    return response
```

### DELETE Endpoint

```python
@router.delete("/library/tracks/{track_id}")
async def delete_track(
    request: Request,
    track_id: UUID,
    user: CurrentUser,
    track_service: DITrackService = Depends(),
):
    """Delete track and return empty response for swap."""
    await track_service.delete(track_id, user.id)
    # Return empty response - HTMX will swap with nothing (delete)
    return Response(content="", media_type="text/html")
```

---

## Alpine.js + HTMX Integration

HTMX handles server communication, Alpine handles client-side UI state:

### Tabs with Lazy Loading

```html
<div
  x-data="{
    activeTab: 'my-gear',
    init() {
      // Restore tab from URL hash
      if (window.location.hash === '#browse') {
        this.activeTab = 'browse';
      }
    }
  }"
>
  <!-- Tab buttons -->
  <nav class="border-b border-border">
    <button
      @click="activeTab = 'browse'; window.location.hash = 'browse'"
      :class="activeTab === 'browse' ? 'border-accent' : 'border-transparent'"
      class="border-b-2 px-4 py-2"
    >
      Browse
    </button>
    <button
      @click="activeTab = 'my-gear'; window.location.hash = 'my-gear'"
      :class="activeTab === 'my-gear' ? 'border-accent' : 'border-transparent'"
      class="border-b-2 px-4 py-2"
    >
      My Gear
    </button>
  </nav>

  <!-- Tab content with HTMX loading -->
  <div x-show="activeTab === 'browse'" x-transition>
    <div
      hx-get="/api/v1/html/gear/results"
      hx-trigger="intersect once"
      hx-swap="innerHTML"
    >
      Loading...
    </div>
  </div>

  <div x-show="activeTab === 'my-gear'" x-transition>
    <div
      hx-get="/api/v1/html/my-gear/results"
      hx-trigger="load"
      hx-swap="innerHTML"
    >
      Loading...
    </div>
  </div>
</div>
```

### Dynamic Values from Alpine State

```html
<div x-data="{ filter: 'all' }">
  <select x-model="filter" @change="htmx.trigger('#items', 'filterChanged')">
    <option value="all">All</option>
    <option value="active">Active</option>
  </select>

  <div
    id="items"
    hx-get="/api/v1/html/items"
    hx-trigger="load, filterChanged"
    hx-vals="js:{filter: filter}"
  >
  </div>
</div>
```

---

## Error Handling

### Auth Redirect on 401

Add to protected pages:

```html
<script>
  document.body.addEventListener('htmx:responseError', (event) => {
    const xhr = event.detail?.xhr;
    if (xhr && xhr.status === 401) {
      const currentPath = window.location.pathname;
      window.location.href = `/login?next=${encodeURIComponent(currentPath)}`;
    }
  });
</script>
```

### Server-Side Error Responses

Return error HTML with appropriate status code:

```python
from fastapi import Response

@router.get("/items/{id}")
async def get_item(id: int):
    item = await get_item_by_id(id)
    if not item:
        return Response(
            content='<div class="text-red-500">Item not found</div>',
            status_code=404,
            media_type="text/html"
        )
    return templates.TemplateResponse(...)
```

---

## Response Headers

Control HTMX behavior from server:

| Header | Purpose |
|--------|---------|
| `HX-Redirect` | Client-side redirect |
| `HX-Refresh` | Full page refresh |
| `HX-Retarget` | Change target element |
| `HX-Reswap` | Change swap strategy |
| `HX-Trigger` | Trigger client events |

```python
from fastapi import Response

@router.post("/items")
async def create_item(response: Response):
    # ... create item
    response.headers["HX-Trigger"] = "itemCreated"
    return templates.TemplateResponse(...)
```

---

## Out-of-Band Swaps

Update multiple elements from a single response:

```html
<!-- Server response updates both the list AND the count badge -->
<div id="item-list">
  <!-- New list content -->
</div>

<span id="item-count" hx-swap-oob="true">5</span>
```

---

## WebSocket Extension

For real-time notifications:

```html
<body hx-ext="ws" ws-connect="/api/v1/ws/notifications">
  <div id="notifications"></div>
</body>
```

Server pushes HTML fragments:

```python
@app.websocket("/api/v1/ws/notifications")
async def websocket_notifications(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_text('''
        <div id="notification" class="toast success">
            Job complete! <a href="/shootout/123">View</a>
        </div>
    ''')
```

---

## Testability

All HTMX elements MUST have `data-testid` attributes:

```html
<div
  data-testid="item-list"
  data-loading="false"
  hx-get="/api/v1/html/items"
  hx-trigger="load"
>
  <div
    data-testid="item-card"
    data-item-id="{{ item.id }}"
  >
    <button
      data-testid="item-card-delete-btn"
      hx-delete="/api/v1/html/items/{{ item.id }}"
    >
      Delete
    </button>
  </div>
</div>
```

---

## Common Mistakes

### Wrong: Returning JSON

```python
# DON'T - HTMX expects HTML
return {"items": items}
```

### Right: Return HTML

```python
# DO - Return rendered template
return templates.TemplateResponse("fragments/items.html", {...})
```

### Wrong: Manual DOM Manipulation

```javascript
// DON'T - Let HTMX handle swaps
fetch('/api/items').then(r => r.json()).then(data => {
  document.getElementById('list').innerHTML = renderItems(data);
});
```

### Right: Declarative HTMX

```html
<!-- DO - Declarative in HTML -->
<div id="list" hx-get="/api/v1/html/items" hx-trigger="load"></div>
```

### Wrong: Missing Request Context

```python
# DON'T - templates.TemplateResponse needs request
return templates.TemplateResponse("fragment.html", {"items": items})
```

### Right: Include Request

```python
# DO - Always pass request
return templates.TemplateResponse(
    request=request,
    name="fragment.html",
    context={"items": items},
)
```

---

## Performance Tips

1. **Use `intersect once`** for content below fold
2. **Debounce inputs** with `delay:300ms`
3. **Include `once`** modifier to prevent duplicate loads
4. **Use `hx-boost`** for progressive enhancement of regular links
5. **Preload on hover** with `hx-trigger="mouseenter"`

---

## Related

- [HTMX Documentation](https://htmx.org/docs/)
- [Alpine.js Documentation](https://alpinejs.dev/)
- `.claude/skills/frontend-dev/SKILL.md` - Full frontend patterns
- `.claude/skills/backend-dev/SKILL.md` - FastAPI patterns
