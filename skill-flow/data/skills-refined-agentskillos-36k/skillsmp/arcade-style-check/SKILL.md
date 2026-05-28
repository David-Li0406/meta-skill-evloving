---
name: arcade-style-check
description: Validate if new UI components or CSS changes follow the QueryCraft "Arcade Lobby" design system. Use when adding new pages, modifying styles, or when user mentions "디자인 확인해줘", "스타일 가이드".
---

# Arcade Style Check

새로운 UI 컴포넌트나 스타일 변경이 QueryCraft의 "아케이드 대기실" 디자인 시스템을 준수하는지 검사합니다.

## Instructions

1. **디자인 키워드 검사**:
   - CSS 파일에서 다음 네온/게이밍 테마 키워드가 사용되었는지 확인합니다.
     - `glassmorphism`, `backdrop-filter`
     - `neon`, `glow`, `box-shadow: 0 0 ...`
     - `arcade`, `pixel`, `grid`
     - CSS 변수: `--arcade-cyan`, `--arcade-magenta`, `--future-bg`

2. **레이아웃 검사**:
   - `MainPage.css` 수준의 3컬럼 레이아웃 또는 카드 기반 그리드 시스템을 확인합니다.
   - 둥근 모서리 (`border-radius: 12px+`)와 반투명 배경 (`rgba(..., 0.7)`)이 적용되었는지 확인합니다.

3. **인터랙션 포인트**:
   - 호버 효과 (`:hover`) 시 스케일 변화(`transform: scale(1.02)`) 또는 글로우 강조가 있는지 확인합니다.

## Style Guide Reference

- **Color Palette**:
  - Cyan: `#00f2ff` (Neon Cyan)
  - Magenta: `#ff00ff` (Hyper Magenta)
  - Background: Deep Dark Blue/Black with subtle gradients.
- **Typography**:
  - 'Inter' 또는 'Roboto' (Web UI)
  - 'Orbitron' 또는 'Fredoka' (Arcade/Branding elements)

## Best Practices

- 코드 변경 시 `frontend/src/pages/MainPage.tsx` 및 `MainPage.css`를 참조하여 기존 컴포넌트와의 시각적 조화를 확인하세요.
- "Coming Soon" 배지나 아이콘 사용 시 일관된 디자인 (`badge-soon` 클래스)을 사용합니다.
