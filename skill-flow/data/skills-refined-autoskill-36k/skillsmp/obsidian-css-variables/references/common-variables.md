# 자주 사용하는 Obsidian CSS 변수

이 문서는 테마 및 플러그인 개발 시 자주 사용하는 핵심 CSS 변수들을 정리한 것입니다.

## 색상 (Colors)

### 배경색 (Background)

| 변수 | 용도 |
|------|------|
| `--background-primary` | 주요 배경색 (노트 영역) |
| `--background-primary-alt` | 대체 배경색 |
| `--background-secondary` | 보조 배경색 (사이드바) |
| `--background-secondary-alt` | 보조 배경색 대체 |
| `--background-modifier-hover` | 호버 상태 배경 |
| `--background-modifier-active-hover` | 활성 호버 상태 |
| `--background-modifier-border` | 테두리 색상 |
| `--background-modifier-border-hover` | 테두리 호버 색상 |
| `--background-modifier-border-focus` | 테두리 포커스 색상 |
| `--background-modifier-error` | 에러 상태 배경 |
| `--background-modifier-success` | 성공 상태 배경 |

### 텍스트 색상 (Text)

| 변수 | 용도 |
|------|------|
| `--text-normal` | 일반 텍스트 |
| `--text-muted` | 흐린 텍스트 |
| `--text-faint` | 매우 흐린 텍스트 |
| `--text-on-accent` | 강조색 위의 텍스트 |
| `--text-on-accent-inverted` | 반전된 강조색 위의 텍스트 |
| `--text-error` | 에러 텍스트 |
| `--text-success` | 성공 텍스트 |
| `--text-warning` | 경고 텍스트 |
| `--text-accent` | 강조 텍스트 |
| `--text-accent-hover` | 강조 텍스트 호버 |

### 상호작용 색상 (Interactive)

| 변수 | 용도 |
|------|------|
| `--interactive-normal` | 일반 상호작용 요소 |
| `--interactive-hover` | 호버 상태 |
| `--interactive-accent` | 강조된 상호작용 요소 |
| `--interactive-accent-hover` | 강조 요소 호버 |
| `--interactive-accent-hsl` | 강조색 HSL 값 |

### 강조색 (Accent)

| 변수 | 용도 |
|------|------|
| `--color-accent` | 기본 강조색 |
| `--color-accent-1` | 강조색 변형 1 (밝음) |
| `--color-accent-2` | 강조색 변형 2 |

## 타이포그래피 (Typography)

### 폰트 패밀리

| 변수 | 용도 |
|------|------|
| `--font-text` | 본문 텍스트 폰트 |
| `--font-monospace` | 고정폭 폰트 (코드) |
| `--font-interface` | UI 인터페이스 폰트 |
| `--font-text-theme` | 테마 텍스트 폰트 |
| `--font-monospace-theme` | 테마 고정폭 폰트 |
| `--font-interface-theme` | 테마 인터페이스 폰트 |

### 폰트 크기

| 변수 | 용도 |
|------|------|
| `--font-text-size` | 본문 텍스트 크기 |
| `--font-ui-smaller` | UI 더 작은 크기 |
| `--font-ui-small` | UI 작은 크기 |
| `--font-ui-medium` | UI 중간 크기 |
| `--font-ui-large` | UI 큰 크기 |
| `--font-ui-larger` | UI 더 큰 크기 |

### 라인 높이

| 변수 | 용도 |
|------|------|
| `--line-height-normal` | 일반 줄 높이 |
| `--line-height-tight` | 좁은 줄 높이 |

## 간격 (Spacing)

### 크기 단위

| 변수 | 값 | 용도 |
|------|-----|------|
| `--size-2-1` | 2px | 매우 작은 간격 |
| `--size-2-2` | 4px | 작은 간격 |
| `--size-2-3` | 6px | 작은-중간 간격 |
| `--size-4-1` | 4px | 기본 작은 간격 |
| `--size-4-2` | 8px | 기본 간격 |
| `--size-4-3` | 12px | 중간 간격 |
| `--size-4-4` | 16px | 큰 간격 |
| `--size-4-5` | 20px | 더 큰 간격 |
| `--size-4-6` | 24px | 매우 큰 간격 |
| `--size-4-8` | 32px | 섹션 간격 |
| `--size-4-12` | 48px | 대형 간격 |

## 테두리 (Borders)

### 반경 (Radius)

| 변수 | 용도 |
|------|------|
| `--radius-s` | 작은 반경 (4px) |
| `--radius-m` | 중간 반경 (8px) |
| `--radius-l` | 큰 반경 (12px) |
| `--radius-xl` | 매우 큰 반경 (16px) |

### 테두리 너비

| 변수 | 용도 |
|------|------|
| `--border-width` | 기본 테두리 너비 |

## 컴포넌트 변수

### 입력 필드 (Input)

| 변수 | 용도 |
|------|------|
| `--input-height` | 입력 필드 높이 |
| `--input-radius` | 입력 필드 반경 |

### 버튼 (Button)

| 변수 | 용도 |
|------|------|
| `--button-height` | 버튼 높이 |
| `--button-radius` | 버튼 반경 |

### 모달 (Modal)

| 변수 | 용도 |
|------|------|
| `--modal-border-width` | 모달 테두리 너비 |
| `--modal-border-color` | 모달 테두리 색상 |
| `--modal-radius` | 모달 반경 |
| `--modal-max-width` | 모달 최대 너비 |
| `--modal-max-height` | 모달 최대 높이 |
| `--modal-max-width-narrow` | 좁은 모달 최대 너비 |
| `--modal-background` | 모달 배경색 |

### 스크롤바 (Scrollbar)

| 변수 | 용도 |
|------|------|
| `--scrollbar-size` | 스크롤바 크기 |
| `--scrollbar-active-thumb-bg` | 활성 스크롤바 썸 배경 |
| `--scrollbar-bg` | 스크롤바 배경 |
| `--scrollbar-thumb-bg` | 스크롤바 썸 배경 |

## 에디터 변수 (Editor)

### 제목 (Headings)

| 변수 | 용도 |
|------|------|
| `--h1-size` | H1 크기 |
| `--h2-size` | H2 크기 |
| `--h3-size` | H3 크기 |
| `--h4-size` | H4 크기 |
| `--h5-size` | H5 크기 |
| `--h6-size` | H6 크기 |
| `--heading-spacing` | 제목 간격 |

### 링크 (Links)

| 변수 | 용도 |
|------|------|
| `--link-color` | 링크 색상 |
| `--link-color-hover` | 링크 호버 색상 |
| `--link-external-color` | 외부 링크 색상 |
| `--link-external-color-hover` | 외부 링크 호버 색상 |
| `--link-unresolved-color` | 미해결 링크 색상 |
| `--link-unresolved-opacity` | 미해결 링크 불투명도 |

### 코드 (Code)

| 변수 | 용도 |
|------|------|
| `--code-size` | 인라인 코드 크기 |
| `--code-background` | 인라인 코드 배경 |
| `--code-normal` | 코드 일반 텍스트 |
| `--code-comment` | 코드 주석 색상 |
| `--code-function` | 함수 이름 색상 |
| `--code-keyword` | 키워드 색상 |
| `--code-string` | 문자열 색상 |
| `--code-value` | 값 색상 |

### 인용문 (Blockquote)

| 변수 | 용도 |
|------|------|
| `--blockquote-border-thickness` | 인용문 테두리 두께 |
| `--blockquote-border-color` | 인용문 테두리 색상 |
| `--blockquote-font-style` | 인용문 폰트 스타일 |
| `--blockquote-color` | 인용문 텍스트 색상 |
| `--blockquote-background-color` | 인용문 배경색 |

## 아이콘 (Icons)

| 변수 | 용도 |
|------|------|
| `--icon-size` | 아이콘 크기 |
| `--icon-stroke` | 아이콘 선 두께 |
| `--icon-color` | 아이콘 색상 |
| `--icon-color-hover` | 아이콘 호버 색상 |
| `--icon-color-active` | 아이콘 활성 색상 |
| `--icon-color-focused` | 아이콘 포커스 색상 |
| `--icon-opacity` | 아이콘 불투명도 |
| `--icon-opacity-hover` | 아이콘 호버 불투명도 |
| `--icon-opacity-active` | 아이콘 활성 불투명도 |

## 사용 예시

```css
/* 플러그인 컨테이너 기본 스타일 */
.my-plugin-container {
  background-color: var(--background-primary);
  color: var(--text-normal);
  border: var(--border-width) solid var(--background-modifier-border);
  border-radius: var(--radius-m);
  padding: var(--size-4-4);
}

/* 호버 상태 */
.my-plugin-item:hover {
  background-color: var(--background-modifier-hover);
}

/* 활성 상태 */
.my-plugin-item.is-active {
  background-color: var(--interactive-accent);
  color: var(--text-on-accent);
}

/* 입력 필드 */
.my-plugin-input {
  height: var(--input-height);
  border-radius: var(--input-radius);
  font-size: var(--font-ui-small);
  padding: 0 var(--size-4-2);
}

/* 버튼 */
.my-plugin-button {
  height: var(--button-height);
  border-radius: var(--button-radius);
  background-color: var(--interactive-accent);
  color: var(--text-on-accent);
}

.my-plugin-button:hover {
  background-color: var(--interactive-accent-hover);
}
```

## 참고

더 자세한 정보는 [Obsidian 개발자 문서](https://docs.obsidian.md/Reference/CSS+variables/CSS+variables)를 참조하세요.
