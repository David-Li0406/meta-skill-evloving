# Badge Components

배지 및 라벨 컴포넌트 패턴

## Base Badge

```erb
<span class="inline-flex items-center rounded-md px-2.5 py-0.5 text-xs font-semibold">
  텍스트
</span>
```

## Category Badge (Secondary)

**용도**: 카테고리, 태그

```erb
<span class="inline-flex items-center rounded-md bg-secondary px-2.5 py-0.5 text-xs font-semibold text-secondary-foreground">
  <%= category %>
</span>
```

**With Icon**:
```erb
<span class="inline-flex items-center rounded-md bg-secondary px-2.5 py-0.5 text-xs font-semibold text-secondary-foreground">
  구인 · <%= job.category_i18n %>
</span>
```

## Outline Badge

**용도**: 상태, 타입

```erb
<span class="inline-flex items-center rounded-md border border-border px-2.5 py-0.5 text-xs font-semibold">
  <%= status %>
</span>
```

## Role Badge

**용도**: 사용자 역할/직책 (프로필 옆)

```erb
<span class="inline-flex items-center rounded-md bg-secondary px-2 py-1 text-xs font-medium text-secondary-foreground">
  <%= user.role_title %>
</span>
```

## Badge Sizes

**Extra Small** (px-2 py-0.5):
```erb
<span class="inline-flex items-center rounded-md bg-secondary px-2 py-0.5 text-xs">
  XS Badge
</span>
```

**Small** (px-2.5 py-0.5):
```erb
<span class="inline-flex items-center rounded-md bg-secondary px-2.5 py-0.5 text-xs font-semibold">
  Small Badge
</span>
```

**Default** (px-3 py-1):
```erb
<span class="inline-flex items-center rounded-md bg-secondary px-3 py-1 text-sm font-medium">
  Default Badge
</span>
```

## Badge Groups

**Horizontal List**:
```erb
<div class="flex items-center gap-2">
  <%= render partial: "shared/icons/briefcase", locals: { css_class: "h-4 w-4 text-primary" } %>
  <span class="inline-flex items-center rounded-md bg-secondary px-2.5 py-0.5 text-xs font-semibold">
    구인 · <%= category %>
  </span>
  <span class="inline-flex items-center rounded-md border border-border px-2.5 py-0.5 text-xs font-semibold">
    <%= project_type %>
  </span>
  <span class="inline-flex items-center rounded-md border border-border px-2.5 py-0.5 text-xs font-semibold">
    <%= status %>
  </span>
</div>
```

**Wrapped List**:
```erb
<div class="flex flex-wrap items-center gap-2">
  <% tags.each do |tag| %>
    <span class="inline-flex items-center rounded-md bg-secondary px-2.5 py-0.5 text-xs font-semibold">
      <%= tag %>
    </span>
  <% end %>
</div>
```

## Badge with Icon

**Left Icon**:
```erb
<span class="inline-flex items-center gap-1 rounded-md bg-secondary px-2.5 py-0.5 text-xs font-semibold">
  <%= render partial: "shared/icons/briefcase", locals: { css_class: "h-3 w-3" } %>
  <%= text %>
</span>
```

**Right Icon** (Removable):
```erb
<span class="inline-flex items-center gap-1 rounded-md bg-secondary px-2.5 py-0.5 text-xs font-semibold">
  <%= text %>
  <button class="hover:text-foreground" aria-label="제거">
    <svg class="h-3 w-3" viewBox="0 0 24 24"><!-- X icon --></svg>
  </button>
</span>
```

## Status Colors

**Success** (green):
```erb
<span class="inline-flex items-center rounded-md bg-green-100 px-2.5 py-0.5 text-xs font-semibold text-green-800">
  완료
</span>
```

**Warning** (yellow):
```erb
<span class="inline-flex items-center rounded-md bg-yellow-100 px-2.5 py-0.5 text-xs font-semibold text-yellow-800">
  진행중
</span>
```

**Error** (red):
```erb
<span class="inline-flex items-center rounded-md bg-red-100 px-2.5 py-0.5 text-xs font-semibold text-red-800">
  마감
</span>
```

**Note**: 프로젝트는 주로 neutral badges 사용 중

## Badge Positioning

**In Header**:
```erb
<div class="flex items-center gap-2">
  <h3 class="font-semibold"><%= user.name %></h3>
  <span class="inline-flex items-center rounded-md bg-secondary px-2 py-1 text-xs font-medium">
    <%= user.role_title %>
  </span>
</div>
```

**In Card**:
```erb
<div class="flex items-center gap-2 mb-3">
  <!-- Icon + multiple badges -->
</div>
```

## Examples in Project

**posts/index.html.erb** (line 28-30):
```erb
<span class="inline-flex items-center rounded-md bg-secondary px-2 py-1 text-xs font-medium text-secondary-foreground">
  <%= post.user.role_title %>
</span>
```

**job_posts/index.html.erb** (lines 49-59):
```erb
<div class="flex items-center gap-2 mb-3">
  <%= render partial: "shared/icons/briefcase" %>
  <span class="...bg-secondary...">구인 · <%= category %></span>
  <span class="...border..."><%= project_type %></span>
  <span class="...border..."><%= status %></span>
</div>
```
