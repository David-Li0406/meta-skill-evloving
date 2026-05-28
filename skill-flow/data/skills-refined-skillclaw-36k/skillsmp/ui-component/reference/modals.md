# Modal & Dialog Components

모달 및 다이얼로그 컴포넌트 패턴

## Simple Modal (Turbo Frame)

```erb
<!-- Trigger Button -->
<%= button_to "모달 열기", modal_path, method: :get,
    data: { turbo_frame: "modal" },
    class: "..." %>

<!-- Modal Container (in layout) -->
<turbo-frame id="modal" class="fixed inset-0 z-50 hidden" data-modal-target="frame">
  <!-- Modal content loaded here -->
</turbo-frame>
```

## Modal Overlay

```erb
<div class="fixed inset-0 z-50 bg-background/80 backdrop-blur-sm" data-modal-overlay>
  <!-- Modal Dialog -->
  <div class="fixed left-1/2 top-1/2 z-50 w-full max-w-lg -translate-x-1/2 -translate-y-1/2">
    <div class="bg-card rounded-xl border border-border shadow-lg p-6">
      <!-- Modal content -->
    </div>
  </div>
</div>
```

## Full Modal Template

```erb
<div class="fixed inset-0 z-50 bg-background/80 backdrop-blur-sm" data-controller="modal">
  <!-- Dialog Container -->
  <div class="fixed left-1/2 top-1/2 z-50 w-full max-w-lg -translate-x-1/2 -translate-y-1/2 p-4">
    <div class="bg-card rounded-xl border border-border shadow-lg">
      <!-- Header -->
      <div class="flex items-center justify-between p-6 border-b border-border">
        <h2 class="text-lg font-semibold">모달 제목</h2>
        <button data-action="click->modal#close" class="h-4 w-4 rounded-sm opacity-70 hover:opacity-100 transition-opacity" aria-label="닫기">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <line x1="18" y1="6" x2="6" y2="18"></line>
            <line x1="6" y1="6" x2="18" y2="18"></line>
          </svg>
        </button>
      </div>

      <!-- Content -->
      <div class="p-6">
        <p class="text-sm text-muted-foreground">
          모달 내용이 여기에 들어갑니다.
        </p>
      </div>

      <!-- Footer -->
      <div class="flex gap-3 justify-end p-6 border-t border-border">
        <button data-action="click->modal#close" class="inline-flex items-center justify-center h-9 rounded-md px-4 text-sm border border-border hover:bg-secondary">
          취소
        </button>
        <button class="inline-flex items-center justify-center h-9 rounded-md px-4 text-sm bg-primary text-primary-foreground hover:bg-primary/90">
          확인
        </button>
      </div>
    </div>
  </div>
</div>
```

## Modal Stimulus Controller

```javascript
// app/javascript/controllers/modal_controller.js
import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
  connect() {
    // Add body overflow hidden
    document.body.style.overflow = "hidden"
  }

  disconnect() {
    // Restore body overflow
    document.body.style.overflow = ""
  }

  close(event) {
    event.preventDefault()
    this.element.remove()
  }

  // Close on backdrop click
  closeOnBackdrop(event) {
    if (event.target === this.element) {
      this.close(event)
    }
  }

  // Close on ESC key
  closeOnEscape(event) {
    if (event.key === "Escape") {
      this.close(event)
    }
  }
}
```

**Enhanced Modal**:
```erb
<div class="fixed inset-0 z-50 bg-background/80 backdrop-blur-sm"
     data-controller="modal"
     data-action="click->modal#closeOnBackdrop keydown@window->modal#closeOnEscape">
  <!-- Modal content -->
</div>
```

## Confirm Dialog

```erb
<div class="fixed inset-0 z-50 bg-background/80 backdrop-blur-sm flex items-center justify-center p-4">
  <div class="bg-card rounded-xl border border-border shadow-lg max-w-md w-full p-6">
    <!-- Icon -->
    <div class="mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-destructive/10 mb-4">
      <svg class="h-6 w-6 text-destructive" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
      </svg>
    </div>

    <!-- Title & Description -->
    <h3 class="text-lg font-semibold text-center mb-2">정말 삭제하시겠습니까?</h3>
    <p class="text-sm text-muted-foreground text-center mb-6">
      이 작업은 취소할 수 없습니다.
    </p>

    <!-- Actions -->
    <div class="flex gap-3">
      <button class="flex-1 inline-flex items-center justify-center h-9 rounded-md px-4 text-sm border border-border hover:bg-secondary">
        취소
      </button>
      <%= button_to "삭제", resource_path, method: :delete,
          class: "flex-1 inline-flex items-center justify-center h-9 rounded-md px-4 text-sm bg-destructive text-destructive-foreground hover:bg-destructive/90" %>
    </div>
  </div>
</div>
```

## Bottom Sheet (Mobile)

```erb
<div class="fixed inset-0 z-50 bg-background/80 backdrop-blur-sm">
  <div class="fixed inset-x-0 bottom-0 z-50 rounded-t-3xl border-t border-border bg-card p-6 shadow-lg">
    <!-- Handle -->
    <div class="mx-auto mb-4 h-1 w-12 rounded-full bg-muted"></div>

    <!-- Content -->
    <h3 class="text-lg font-semibold mb-4">옵션 선택</h3>

    <div class="space-y-2">
      <button class="w-full text-left px-4 py-3 rounded-md hover:bg-accent transition-colors">
        옵션 1
      </button>
      <button class="w-full text-left px-4 py-3 rounded-md hover:bg-accent transition-colors">
        옵션 2
      </button>
      <button class="w-full text-left px-4 py-3 rounded-md hover:bg-accent transition-colors text-destructive">
        삭제
      </button>
    </div>
  </div>
</div>
```

## Slide-over (Side Panel)

```erb
<div class="fixed inset-0 z-50 bg-background/80 backdrop-blur-sm">
  <!-- Panel -->
  <div class="fixed inset-y-0 right-0 z-50 w-full sm:max-w-md border-l border-border bg-card shadow-lg">
    <!-- Header -->
    <div class="flex items-center justify-between p-6 border-b border-border">
      <h2 class="text-lg font-semibold">사이드 패널</h2>
      <button class="h-4 w-4 opacity-70 hover:opacity-100" aria-label="닫기">
        <!-- X icon -->
      </button>
    </div>

    <!-- Content -->
    <div class="overflow-y-auto p-6" style="height: calc(100vh - 80px);">
      <!-- Content here -->
    </div>
  </div>
</div>
```

## Loading Modal

```erb
<div class="fixed inset-0 z-50 bg-background/80 backdrop-blur-sm flex items-center justify-center">
  <div class="bg-card rounded-xl border border-border shadow-lg p-8 flex flex-col items-center gap-4">
    <!-- Spinner -->
    <svg class="animate-spin h-8 w-8 text-primary" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
      <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
    </svg>
    <p class="text-sm text-muted-foreground">처리 중...</p>
  </div>
</div>
```

## Toast Notification (Alternative)

```erb
<div class="fixed top-4 right-4 z-50 bg-card border border-border rounded-xl shadow-lg p-4 max-w-sm" role="alert">
  <div class="flex items-start gap-3">
    <!-- Icon -->
    <div class="flex-shrink-0">
      <svg class="h-5 w-5 text-primary" fill="currentColor" viewBox="0 0 20 20">
        <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
      </svg>
    </div>
    <!-- Content -->
    <div class="flex-1">
      <p class="text-sm font-medium">성공</p>
      <p class="text-sm text-muted-foreground">작업이 완료되었습니다.</p>
    </div>
    <!-- Close -->
    <button class="flex-shrink-0 text-muted-foreground hover:text-foreground">
      <svg class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
        <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"></path>
      </svg>
    </button>
  </div>
</div>
```

## Best Practices

1. **Turbo 활용**: Turbo Frame으로 모달 콘텐츠 로드
2. **Backdrop**: 항상 `bg-background/80 backdrop-blur-sm`
3. **Escape 키**: ESC 키로 닫기 지원
4. **Body Overflow**: 모달 열릴 때 스크롤 방지
5. **Z-index**: `z-50` 사용
6. **접근성**: `aria-label`, focus trap
7. **모바일**: 작은 화면에서는 full-screen 고려
