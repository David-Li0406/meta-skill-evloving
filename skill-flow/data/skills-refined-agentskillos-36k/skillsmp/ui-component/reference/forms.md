# Form Components

폼 입력 및 검증 패턴

## Base Form

```erb
<%= form_with model: @object, class: "space-y-6" do |form| %>
  <!-- Form fields -->

  <div class="flex gap-3">
    <%= form.submit "저장", class: "bg-primary text-primary-foreground hover:bg-primary/90 h-9 rounded-md px-3 inline-flex items-center justify-center text-sm font-medium" %>
    <%= link_to "취소", :back, class: "inline-flex items-center justify-center h-9 rounded-md px-3 text-sm border border-border hover:bg-secondary" %>
  </div>
<% end %>
```

## Text Input

**Standard Input**:
```erb
<div class="space-y-2">
  <%= form.label :title, "제목", class: "text-sm font-medium" %>
  <%= form.text_field :title, class: "flex h-9 w-full rounded-md border border-input bg-transparent px-3 py-1 text-sm shadow-sm transition-colors placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:cursor-not-allowed disabled:opacity-50", placeholder: "제목을 입력하세요" %>
  <% if @object.errors[:title].any? %>
    <p class="text-sm text-destructive"><%= @object.errors[:title].first %></p>
  <% end %>
</div>
```

**Input Classes**:
```
flex h-9 w-full rounded-md border border-input bg-transparent px-3 py-1
text-sm shadow-sm transition-colors
placeholder:text-muted-foreground
focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring
disabled:cursor-not-allowed disabled:opacity-50
```

## Textarea

```erb
<div class="space-y-2">
  <%= form.label :content, "내용", class: "text-sm font-medium" %>
  <%= form.text_area :content, rows: 5, class: "flex min-h-[80px] w-full rounded-md border border-input bg-transparent px-3 py-2 text-sm shadow-sm placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:cursor-not-allowed disabled:opacity-50", placeholder: "내용을 입력하세요" %>
  <% if @object.errors[:content].any? %>
    <p class="text-sm text-destructive"><%= @object.errors[:content].first %></p>
  <% end %>
</div>
```

## Select / Dropdown

```erb
<div class="space-y-2">
  <%= form.label :category, "카테고리", class: "text-sm font-medium" %>
  <%= form.select :category,
      options_for_select([["개발", "development"], ["디자인", "design"], ["기획", "planning"]], @object.category),
      {},
      class: "flex h-9 w-full rounded-md border border-input bg-transparent px-3 py-1 text-sm shadow-sm focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring" %>
  <% if @object.errors[:category].any? %>
    <p class="text-sm text-destructive"><%= @object.errors[:category].first %></p>
  <% end %>
</div>
```

## Checkbox

```erb
<div class="flex items-center space-x-2">
  <%= form.check_box :terms_accepted, class: "h-4 w-4 rounded border-border text-primary focus:ring-2 focus:ring-ring" %>
  <%= form.label :terms_accepted, "이용약관에 동의합니다", class: "text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70" %>
</div>
```

## Radio Buttons

```erb
<div class="space-y-2">
  <label class="text-sm font-medium">프로젝트 타입</label>
  <div class="space-y-2">
    <div class="flex items-center space-x-2">
      <%= form.radio_button :project_type, "short_term", class: "h-4 w-4 border-border text-primary focus:ring-2 focus:ring-ring" %>
      <%= form.label :project_type_short_term, "단기", class: "text-sm" %>
    </div>
    <div class="flex items-center space-x-2">
      <%= form.radio_button :project_type, "long_term", class: "h-4 w-4 border-border text-primary focus:ring-2 focus:ring-ring" %>
      <%= form.label :project_type_long_term, "장기", class: "text-sm" %>
    </div>
  </div>
</div>
```

## File Upload

```erb
<div class="space-y-2">
  <%= form.label :avatar, "프로필 사진", class: "text-sm font-medium" %>
  <div class="flex items-center gap-3">
    <%= form.file_field :avatar, class: "flex h-9 w-full rounded-md border border-input bg-transparent px-3 py-1 text-sm file:border-0 file:bg-transparent file:text-sm file:font-medium" %>
  </div>
  <% if @object.errors[:avatar].any? %>
    <p class="text-sm text-destructive"><%= @object.errors[:avatar].first %></p>
  <% end %>
</div>
```

## Error Handling

**Field with Error**:
```erb
<div class="space-y-2">
  <%= form.label :email, "이메일", class: "text-sm font-medium" %>
  <%= form.email_field :email, class: "flex h-9 w-full rounded-md border #{@object.errors[:email].any? ? 'border-destructive' : 'border-input'} bg-transparent px-3 py-1 text-sm shadow-sm focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring" %>
  <% if @object.errors[:email].any? %>
    <p class="text-sm text-destructive"><%= @object.errors[:email].first %></p>
  <% end %>
</div>
```

**Form-level Errors**:
```erb
<% if @object.errors.any? %>
  <div class="rounded-md bg-destructive/10 p-4 mb-6">
    <div class="flex">
      <div class="flex-shrink-0">
        <svg class="h-5 w-5 text-destructive" viewBox="0 0 20 20" fill="currentColor">
          <!-- Error icon -->
        </svg>
      </div>
      <div class="ml-3">
        <h3 class="text-sm font-medium text-destructive">
          <%= pluralize(@object.errors.count, "개의 오류") %>가 발생했습니다:
        </h3>
        <div class="mt-2 text-sm text-destructive">
          <ul class="list-disc pl-5 space-y-1">
            <% @object.errors.full_messages.each do |message| %>
              <li><%= message %></li>
            <% end %>
          </ul>
        </div>
      </div>
    </div>
  </div>
<% end %>
```

## Form Layouts

**Single Column** (현재 프로젝트 스타일):
```erb
<%= form_with model: @object, class: "space-y-6" do |form| %>
  <div class="space-y-2"><!-- Field 1 --></div>
  <div class="space-y-2"><!-- Field 2 --></div>
  <div class="space-y-2"><!-- Field 3 --></div>
<% end %>
```

**Two Column**:
```erb
<%= form_with model: @object, class: "space-y-6" do |form| %>
  <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
    <div class="space-y-2"><!-- Field 1 --></div>
    <div class="space-y-2"><!-- Field 2 --></div>
  </div>
<% end %>
```

## Helper Text

```erb
<div class="space-y-2">
  <%= form.label :password, "비밀번호", class: "text-sm font-medium" %>
  <%= form.password_field :password, class: "..." %>
  <p class="text-xs text-muted-foreground">8자 이상, 영문/숫자 조합</p>
</div>
```

## Required Fields

```erb
<%= form.label :email, class: "text-sm font-medium" do %>
  이메일 <span class="text-destructive">*</span>
<% end %>
```

## Form Buttons

**Primary + Secondary**:
```erb
<div class="flex gap-3">
  <%= form.submit "저장", class: "bg-primary text-primary-foreground hover:bg-primary/90 h-9 rounded-md px-4 inline-flex items-center justify-center text-sm font-medium" %>
  <%= link_to "취소", :back, class: "inline-flex items-center justify-center h-9 rounded-md px-4 text-sm border border-border hover:bg-secondary transition-colors" %>
</div>
```

**Full Width Button**:
```erb
<%= form.submit "저장", class: "w-full bg-primary text-primary-foreground hover:bg-primary/90 h-9 rounded-md inline-flex items-center justify-center text-sm font-medium" %>
```

## Loading State

```erb
<%= form.submit "저장",
    data: { disable_with: "저장 중..." },
    class: "bg-primary text-primary-foreground hover:bg-primary/90 h-9 rounded-md px-4 inline-flex items-center justify-center text-sm font-medium disabled:opacity-50" %>
```

## Best Practices

1. **Label + Input 묶기**: 항상 `space-y-2` div로 묶기
2. **Error 표시**: 각 필드마다 에러 메시지 영역
3. **Placeholder**: 명확한 예시 제공
4. **Required 표시**: 필수 필드는 `*` 표시
5. **Accessible**: label과 input은 항상 연결
6. **Focus States**: `focus-visible:ring-1` 포함
7. **Spacing**: 폼 전체는 `space-y-6`
