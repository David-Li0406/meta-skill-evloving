# Card Components

카드 레이아웃 및 변형 패턴

## Base Card

```erb
<article class="bg-card rounded-xl p-6 border border-border">
  <!-- Card content -->
</article>
```

**Base Classes**:
- `bg-card` - 카드 배경색
- `rounded-xl` - 둥근 모서리
- `p-6` - 내부 패딩
- `border border-border` - 테두리

## Interactive Card

**Hover 효과 포함**:
```erb
<article class="bg-card rounded-xl p-6 border border-border hover:border-muted-foreground/20 transition-colors">
  <!-- Content -->
</article>
```

**Clickable Card** (전체 클릭 가능):
```erb
<%= link_to post_path(post) do %>
  <article class="bg-card rounded-xl p-6 border border-border hover:border-primary/50 transition-all cursor-pointer">
    <!-- Content -->
  </article>
<% end %>
```

## Post Card (게시글)

**완전한 예시** (posts/index.html.erb):
```erb
<article class="bg-card rounded-xl p-6 border border-border hover:border-muted-foreground/20 transition-colors">
  <!-- Author Section -->
  <%= link_to profile_path(post.user_id), class: "flex items-start gap-3 mb-4 group" do %>
    <div class="h-10 w-10 rounded-full ring-2 ring-background group-hover:ring-primary/20 transition-all overflow-hidden bg-secondary flex items-center justify-center">
      <% if post.user.avatar_url %>
        <%= image_tag post.user.avatar_url, alt: post.user.name, class: "h-full w-full object-cover" %>
      <% else %>
        <span class="text-lg font-semibold"><%= post.user.name[0] %></span>
      <% end %>
    </div>
    <div class="flex-1">
      <div class="flex items-center gap-2">
        <h3 class="font-semibold group-hover:text-primary transition-colors"><%= post.user.name %></h3>
        <% if post.user.role_title.present? %>
          <span class="inline-flex items-center rounded-md bg-secondary px-2 py-1 text-xs font-medium text-secondary-foreground">
            <%= post.user.role_title %>
          </span>
        <% end %>
      </div>
      <p class="text-xs text-muted-foreground"><%= time_ago_in_words(post.created_at) %> 전</p>
    </div>
  <% end %>

  <!-- Content Section -->
  <%= link_to post_path(post) do %>
    <h2 class="text-lg font-semibold mb-2 hover:text-primary transition-colors cursor-pointer">
      <%= post.title %>
    </h2>
    <p class="text-foreground mb-3 leading-relaxed hover:text-primary transition-colors cursor-pointer line-clamp-3">
      <%= post.content %>
    </p>
  <% end %>

  <!-- Actions Section -->
  <div class="flex items-center gap-4 pt-3 border-t border-border">
    <!-- Action buttons (heart, comment, share, bookmark) -->
  </div>
</article>
```

## Job Posting Card

**구인/구직 카드** (job_posts/index.html.erb):
```erb
<%= link_to job_post_path(job) do %>
  <article class="bg-card rounded-xl p-6 border border-border hover:border-primary/50 transition-all cursor-pointer">
    <!-- Author Info (compact) -->
    <%= link_to profile_path(job.user_id), class: "flex items-center gap-3 mb-4 group", onclick: "event.stopPropagation()" do %>
      <div class="h-10 w-10 rounded-full bg-secondary flex items-center justify-center overflow-hidden flex-shrink-0">
        <% if job.user.avatar_url %>
          <%= image_tag job.user.avatar_url, class: "h-full w-full object-cover" %>
        <% else %>
          <span class="text-lg font-semibold"><%= job.user.name[0] %></span>
        <% end %>
      </div>
      <div class="flex-1">
        <p class="font-semibold text-sm text-foreground group-hover:text-primary transition-colors">
          <%= job.user.name %>
        </p>
        <% if job.user.role_title.present? %>
          <p class="text-xs text-muted-foreground"><%= job.user.role_title %></p>
        <% end %>
      </div>
    <% end %>

    <!-- Badges -->
    <div class="flex items-center gap-2 mb-3">
      <%= render partial: "shared/icons/briefcase", locals: { css_class: "h-4 w-4 text-primary" } %>
      <span class="inline-flex items-center rounded-md bg-secondary px-2.5 py-0.5 text-xs font-semibold">
        구인 · <%= job.category_i18n %>
      </span>
      <span class="inline-flex items-center rounded-md border border-border px-2.5 py-0.5 text-xs font-semibold">
        <%= job.project_type_i18n %>
      </span>
      <span class="inline-flex items-center rounded-md border border-border px-2.5 py-0.5 text-xs font-semibold">
        <%= job.status_i18n %>
      </span>
    </div>

    <!-- Content -->
    <h3 class="text-lg font-bold mb-2 text-foreground"><%= job.title %></h3>
    <p class="text-sm text-muted-foreground mb-4 line-clamp-2"><%= job.description %></p>

    <!-- Meta -->
    <div class="flex items-center gap-4 text-sm text-muted-foreground">
      <% if job.budget.present? %>
        <span class="font-medium text-primary"><%= job.budget %></span>
      <% end %>
      <span>조회 <%= job.views_count %></span>
      <span class="ml-auto"><%= time_ago_in_words(job.created_at) %> 전</span>
    </div>
  </article>
<% end %>
```

## Profile Card

**사용자 프로필 미니 카드**:
```erb
<div class="flex items-start gap-3">
  <div class="h-10 w-10 rounded-full bg-secondary flex items-center justify-center overflow-hidden">
    <% if user.avatar_url %>
      <%= image_tag user.avatar_url, alt: user.name, class: "h-full w-full object-cover" %>
    <% else %>
      <span class="text-lg font-semibold"><%= user.name[0] %></span>
    <% end %>
  </div>
  <div class="flex-1">
    <h3 class="font-semibold"><%= user.name %></h3>
    <% if user.role_title.present? %>
      <p class="text-xs text-muted-foreground"><%= user.role_title %></p>
    <% end %>
  </div>
</div>
```

**Hover 효과 추가**:
```erb
<%= link_to profile_path(user), class: "flex items-start gap-3 group" do %>
  <div class="h-10 w-10 rounded-full ring-2 ring-background group-hover:ring-primary/20 transition-all overflow-hidden bg-secondary flex items-center justify-center">
    <!-- Avatar -->
  </div>
  <div class="flex-1">
    <h3 class="font-semibold group-hover:text-primary transition-colors"><%= user.name %></h3>
    <p class="text-xs text-muted-foreground"><%= user.role_title %></p>
  </div>
<% end %>
```

## Avatar Sizes

**Small** (h-8 w-8):
```erb
<div class="h-8 w-8 rounded-full bg-secondary flex items-center justify-center">
  <span class="text-sm font-semibold"><%= user.name[0] %></span>
</div>
```

**Default** (h-10 w-10):
```erb
<div class="h-10 w-10 rounded-full bg-secondary flex items-center justify-center">
  <span class="text-lg font-semibold"><%= user.name[0] %></span>
</div>
```

**Large** (h-16 w-16):
```erb
<div class="h-16 w-16 rounded-full bg-secondary flex items-center justify-center">
  <span class="text-2xl font-semibold"><%= user.name[0] %></span>
</div>
```

## Empty State Card

**빈 상태 표시**:
```erb
<div class="text-center py-20 text-muted-foreground">
  <%= render partial: "shared/icons/briefcase", locals: { css_class: "h-16 w-16 mx-auto mb-4 opacity-50" } %>
  <p class="text-lg font-medium mb-2">아직 등록된 게시글이 없습니다</p>
  <p class="text-sm">첫 번째 게시글을 작성해보세요!</p>
</div>
```

## Card Sections

### Divider
```erb
<div class="border-t border-border pt-3 mt-3">
  <!-- Section below divider -->
</div>
```

### Header with Action
```erb
<div class="flex items-center justify-between mb-4">
  <h2 class="text-lg font-semibold">카드 제목</h2>
  <button class="text-sm text-primary hover:underline">더보기</button>
</div>
```

### Footer Meta
```erb
<div class="flex items-center gap-4 text-sm text-muted-foreground mt-4">
  <span>조회 <%= views_count %></span>
  <span>댓글 <%= comments_count %></span>
  <span class="ml-auto"><%= time_ago_in_words(created_at) %> 전</span>
</div>
```

## Grid Layout

**카드 그리드**:
```erb
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
  <% items.each do |item| %>
    <article class="bg-card rounded-xl p-6 border border-border">
      <!-- Card content -->
    </article>
  <% end %>
</div>
```

**리스트 레이아웃** (현재 프로젝트):
```erb
<div class="space-y-4">
  <% items.each do |item| %>
    <article class="bg-card rounded-xl p-6 border border-border">
      <!-- Card content -->
    </article>
  <% end %>
</div>
```

## Best Practices

1. **일관된 패딩**: 항상 `p-6` 사용
2. **Hover 효과**: Interactive card는 `hover:border-primary/50` 추가
3. **Avatar 플레이스홀더**: 이미지 없을 때 이니셜 표시
4. **Line Clamp**: 긴 텍스트는 `line-clamp-2` or `line-clamp-3`
5. **Meta 정보**: 항상 `text-sm text-muted-foreground`
6. **시간 표시**: `time_ago_in_words(created_at) + " 전"`
