---
name: ui-component
description: Generate consistent Tailwind UI components following project design system. Use when user wants to create buttons, cards, forms, modals, badges, or says "create component", "add UI element", "make button/card/form", "design component".
---

# UI Component Generator

Generate reusable UI components matching this project's Tailwind design system.

## Quick Start

```
Task Progress (copy and check off):
- [ ] 1. Identify component type needed
- [ ] 2. Select appropriate pattern from reference
- [ ] 3. Generate ERB partial
- [ ] 4. Add Stimulus controller (if interactive)
- [ ] 5. Add to shared/components directory
- [ ] 6. Test responsiveness
```

## Project Design System

**Color Palette** (CSS Variables):
- `bg-background` - 기본 배경
- `bg-card` - 카드 배경
- `bg-primary` - 주요 색상
- `text-foreground` - 기본 텍스트
- `text-muted-foreground` - 보조 텍스트
- `border-border` - 테두리

**Typography**:
- Headers: `text-2xl font-bold`
- Subheaders: `text-lg font-semibold`
- Body: `text-sm` or `text-base`
- Muted: `text-xs text-muted-foreground`

**Spacing**:
- Container padding: `px-4 py-6`
- Card padding: `p-6`
- Gap between elements: `gap-3`, `gap-4`
- Space-y for vertical: `space-y-4`

**Component Patterns**:
- Buttons: [reference/buttons.md](reference/buttons.md)
- Cards: [reference/cards.md](reference/cards.md)
- Forms: [reference/forms.md](reference/forms.md)
- Badges: [reference/badges.md](reference/badges.md)
- Modals: [reference/modals.md](reference/modals.md)

**Examples**:
- Complete components: [examples/](examples/)

## Component Types

### 1. Buttons

**Primary Button**:
```erb
<%= link_to "액션", path, class: "inline-flex items-center justify-center gap-2 whitespace-nowrap text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50 bg-primary text-primary-foreground hover:bg-primary/90 h-9 rounded-md px-3" %>
```

**Icon Button**:
```erb
<button class="inline-flex items-center justify-center gap-2 whitespace-nowrap text-sm font-medium transition-colors hover:bg-accent hover:text-accent-foreground h-9 rounded-md px-3">
  <%= render partial: "shared/icons/heart", locals: { css_class: "h-4 w-4" } %>
  <span><%= count %></span>
</button>
```

**Floating Action Button (FAB)**:
```erb
<%= link_to path, class: "fixed bottom-24 right-4 h-14 w-14 rounded-full shadow-lg z-40 inline-flex items-center justify-center bg-primary text-primary-foreground hover:bg-primary/90" do %>
  <%= render partial: "shared/icons/plus", locals: { css_class: "h-6 w-6" } %>
<% end %>
```

See [reference/buttons.md](reference/buttons.md) for all button variants.

### 2. Cards

**Content Card**:
```erb
<article class="bg-card rounded-xl p-6 border border-border hover:border-muted-foreground/20 transition-colors">
  <!-- Card content -->
</article>
```

**Profile Card**:
```erb
<div class="flex items-start gap-3">
  <div class="h-10 w-10 rounded-full bg-secondary flex items-center justify-center overflow-hidden">
    <%= image_tag user.avatar_url, class: "h-full w-full object-cover" %>
  </div>
  <div class="flex-1">
    <h3 class="font-semibold"><%= user.name %></h3>
    <p class="text-xs text-muted-foreground"><%= user.role_title %></p>
  </div>
</div>
```

See [reference/cards.md](reference/cards.md) for all card patterns.

### 3. Badges

**Category Badge**:
```erb
<span class="inline-flex items-center rounded-md bg-secondary px-2.5 py-0.5 text-xs font-semibold text-secondary-foreground">
  <%= category %>
</span>
```

**Status Badge**:
```erb
<span class="inline-flex items-center rounded-md border border-border px-2.5 py-0.5 text-xs font-semibold">
  <%= status %>
</span>
```

See [reference/badges.md](reference/badges.md) for badge variants.

### 4. Forms

**Input Field**:
```erb
<div class="space-y-2">
  <%= form.label :title, class: "text-sm font-medium" %>
  <%= form.text_field :title, class: "flex h-9 w-full rounded-md border border-input bg-transparent px-3 py-1 text-sm shadow-sm transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring" %>
  <% if object.errors[:title].any? %>
    <p class="text-sm text-destructive"><%= object.errors[:title].first %></p>
  <% end %>
</div>
```

See [reference/forms.md](reference/forms.md) for complete form patterns.

### 5. Layouts

**Header (Sticky)**:
```erb
<header class="sticky top-0 bg-background/95 backdrop-blur-sm border-b border-border z-40">
  <div class="max-w-screen-xl mx-auto px-4 py-4">
    <h1 class="text-2xl font-bold"><%= title %></h1>
    <p class="text-sm text-muted-foreground"><%= subtitle %></p>
  </div>
</header>
```

**Main Container**:
```erb
<main class="max-w-screen-xl mx-auto px-4 py-6">
  <div class="space-y-4">
    <!-- Content -->
  </div>
</main>
```

## Icons

프로젝트는 SVG 아이콘을 `app/views/shared/icons/` 에 partial로 관리합니다.

**사용 방법**:
```erb
<%= render partial: "shared/icons/heart", locals: { css_class: "h-4 w-4" } %>
```

**Available Icons**:
- home, user, briefcase, bookmark
- heart, share, plus, mail
- message_square, calendar, globe
- file_text, arrow_left, map_pin

## Component Organization

**파일 위치**:
```
app/views/shared/
├── components/          # 재사용 가능한 컴포넌트
│   ├── _button.html.erb
│   ├── _card.html.erb
│   └── _badge.html.erb
├── icons/              # SVG 아이콘
│   ├── _heart.html.erb
│   └── ...
└── _bottom_nav.html.erb # 네비게이션 바
```

**Naming Convention**:
- Partial files: `_component_name.html.erb`
- Locals 사용: `<%= render "shared/components/button", text: "클릭", path: root_path %>`

## Responsive Design

**Mobile-First 접근**:
```erb
<!-- Mobile: full width, Desktop: max-width -->
<div class="w-full max-w-screen-xl mx-auto">

<!-- Hide on mobile, show on desktop -->
<div class="hidden md:block">

<!-- Different sizes -->
<div class="text-sm md:text-base lg:text-lg">
```

**Container Constraints**:
- Max width: `max-w-screen-xl` (1280px)
- Padding: `px-4` (mobile), `px-6` (desktop)
- Bottom navigation padding: `pb-20` (모바일 하단 네비 공간)

## Accessibility

**필수 요소**:
- Buttons: `aria-label` for icon-only buttons
- Links: Descriptive text or `aria-label`
- Forms: Associated `<label>` for inputs
- Focus states: `focus-visible:outline-none focus-visible:ring-1`

**예시**:
```erb
<button aria-label="좋아요" class="...">
  <%= render partial: "shared/icons/heart" %>
</button>
```

## After Generation

```bash
# View in browser
rails server
# Visit http://localhost:3000

# Check responsiveness
# Resize browser or use DevTools mobile view
```

## Common Patterns

**Empty State**:
```erb
<div class="text-center py-20 text-muted-foreground">
  <%= render partial: "shared/icons/icon_name", locals: { css_class: "h-16 w-16 mx-auto mb-4 opacity-50" } %>
  <p class="text-lg font-medium mb-2">메인 메시지</p>
  <p class="text-sm">서브 메시지</p>
</div>
```

**Loading Skeleton**:
```erb
<div class="animate-pulse">
  <div class="h-4 bg-muted rounded w-3/4 mb-2"></div>
  <div class="h-4 bg-muted rounded w-1/2"></div>
</div>
```

**Line Clamp** (텍스트 자르기):
```erb
<p class="line-clamp-2">긴 텍스트...</p>
<p class="line-clamp-3">더 긴 텍스트...</p>
```

## Checklist

- [ ] Component uses project color variables
- [ ] Responsive on mobile and desktop
- [ ] Proper spacing (px-4, py-6, gap-3, etc.)
- [ ] Icons from shared/icons/ if needed
- [ ] Accessibility attributes added
- [ ] Hover/focus states defined
- [ ] Consistent with existing components
- [ ] Saved as partial if reusable
- [ ] Tested in browser
