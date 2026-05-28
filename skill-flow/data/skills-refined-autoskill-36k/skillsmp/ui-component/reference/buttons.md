# Button Components

모든 버튼 변형 및 사용 예시

## Base Button Classes

```
inline-flex items-center justify-center gap-2
whitespace-nowrap text-sm font-medium
transition-colors
focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring
disabled:pointer-events-none disabled:opacity-50
```

## Primary Button

**용도**: 주요 액션 (생성, 저장, 제출)

```erb
<%= link_to "새 게시글", new_post_path, class: "inline-flex items-center justify-center gap-2 whitespace-nowrap text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50 bg-primary text-primary-foreground hover:bg-primary/90 h-9 rounded-md px-3" %>
```

**Form Submit**:
```erb
<%= form.submit "저장", class: "bg-primary text-primary-foreground hover:bg-primary/90 h-9 rounded-md px-3 inline-flex items-center justify-center text-sm font-medium" %>
```

## Secondary Button

**용도**: 보조 액션 (취소, 뒤로가기)

```erb
<%= link_to "취소", :back, class: "inline-flex items-center justify-center gap-2 whitespace-nowrap text-sm font-medium transition-colors hover:bg-secondary hover:text-secondary-foreground h-9 rounded-md px-3 border border-border" %>
```

## Ghost Button (Icon + Text)

**용도**: 좋아요, 댓글, 공유

```erb
<button class="inline-flex items-center justify-center gap-2 whitespace-nowrap text-sm font-medium transition-colors hover:bg-accent hover:text-accent-foreground h-9 rounded-md px-3">
  <%= render partial: "shared/icons/heart", locals: { css_class: "h-4 w-4" } %>
  <span><%= @post.likes_count %></span>
</button>
```

**북마크 버튼**:
```erb
<button class="inline-flex items-center justify-center gap-2 whitespace-nowrap text-sm font-medium transition-colors hover:bg-accent hover:text-accent-foreground h-9 rounded-md px-3 ml-auto">
  <%= render partial: "shared/icons/bookmark", locals: { css_class: "h-4 w-4" } %>
</button>
```

## Floating Action Button (FAB)

**용도**: 주요 생성 액션 (새 게시글, 새 메시지)

```erb
<%= link_to new_post_path, class: "fixed bottom-24 right-4 h-14 w-14 rounded-full shadow-lg z-40 inline-flex items-center justify-center whitespace-nowrap text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50 bg-primary text-primary-foreground hover:bg-primary/90" do %>
  <%= render partial: "shared/icons/plus", locals: { css_class: "h-6 w-6" } %>
<% end %>
```

**위치 조정**:
- `bottom-24`: 하단 네비게이션 위
- `right-4`: 오른쪽 여백
- `z-40`: 다른 요소 위에 표시

## Icon-Only Button

**용도**: 공간 절약, 뒤로가기

```erb
<%= link_to :back, class: "inline-flex items-center justify-center h-9 w-9 rounded-md hover:bg-accent hover:text-accent-foreground transition-colors", "aria-label": "뒤로가기" do %>
  <%= render partial: "shared/icons/arrow_left", locals: { css_class: "h-5 w-5" } %>
<% end %>
```

**중요**: `aria-label` 필수!

## Tab Button

**용도**: 탭 전환 (구인/구직)

```erb
<button data-tab="jobs" class="tab-trigger inline-flex items-center justify-center whitespace-nowrap rounded-md px-3 py-1 text-sm font-medium ring-offset-background transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 data-[state=active]:bg-background data-[state=active]:text-foreground data-[state=active]:shadow">
  <%= render partial: "shared/icons/briefcase", locals: { css_class: "h-4 w-4 mr-2" } %>
  구인 (<%= @jobs_count %>)
</button>
```

**Active 상태 클래스**:
```
active bg-background text-foreground shadow
```

## Button Sizes

**Small** (`h-8 px-2 text-xs`):
```erb
<button class="... h-8 px-2 text-xs">작은 버튼</button>
```

**Default** (`h-9 px-3 text-sm`):
```erb
<button class="... h-9 px-3 text-sm">기본 버튼</button>
```

**Large** (`h-10 px-4 text-base`):
```erb
<button class="... h-10 px-4 text-base">큰 버튼</button>
```

## Button States

**Disabled**:
```erb
<button disabled class="... disabled:pointer-events-none disabled:opacity-50">
  비활성 버튼
</button>
```

**Loading**:
```erb
<button disabled class="...">
  <svg class="animate-spin h-4 w-4 mr-2" viewBox="0 0 24 24">
    <!-- Spinner SVG -->
  </svg>
  처리 중...
</button>
```

## Button Groups

**Horizontal Group**:
```erb
<div class="flex items-center gap-2">
  <button class="...">버튼 1</button>
  <button class="...">버튼 2</button>
  <button class="...">버튼 3</button>
</div>
```

**Action Bar** (게시글 하단):
```erb
<div class="flex items-center gap-4 pt-3 border-t border-border">
  <!-- 좋아요 버튼 -->
  <!-- 댓글 버튼 -->
  <!-- 공유 버튼 -->
  <!-- 북마크 버튼 (ml-auto로 오른쪽 정렬) -->
</div>
```

## Accessibility

- **텍스트 버튼**: 이미 설명적
- **아이콘 버튼**: `aria-label` 필수
- **Submit 버튼**: 자동으로 form과 연결
- **Focus states**: `focus-visible:ring-1` 포함

## Examples in Code

**posts/index.html.erb** (lines 49-62):
```erb
<div class="flex items-center gap-4 pt-3 border-t border-border">
  <button class="...">
    <%= render partial: "shared/icons/heart" %>
    <span><%= post.likes_count %></span>
  </button>
  <!-- More buttons -->
</div>
```

**FAB** (line 70-72):
```erb
<%= link_to new_post_path, class: "fixed bottom-24 right-4 h-14 w-14 rounded-full shadow-lg..." do %>
  <%= render partial: "shared/icons/plus" %>
<% end %>
```
