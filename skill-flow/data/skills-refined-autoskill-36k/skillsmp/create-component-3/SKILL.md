---
name: create-component
description: CareMatch용 React 컴포넌트 생성. 고령자 친화적 접근성 규칙이 적용된 shadcn/ui 기반 컴포넌트를 생성합니다. 사용법 - "컴포넌트 생성해줘", "JobCard 컴포넌트 만들어줘"
allowed-tools: Read, Write, Glob
---

# Create Component Skill

CareMatch V3용 React 컴포넌트를 생성합니다.

## 컴포넌트 템플릿

```typescript
// components/{category}/{ComponentName}.tsx
import { type FC } from 'react'

interface {ComponentName}Props {
  // props 정의
}

/**
 * {ComponentName} 컴포넌트
 * @description [설명]
 * @accessibility
 * - 최소 폰트 16px
 * - 버튼 최소 48px
 */
export const {ComponentName}: FC<{ComponentName}Props> = (props) => {
  return (
    <div className="text-lg">
      {/* 구현 */}
    </div>
  )
}
```

## 접근성 규칙 (필수)

- 폰트: 최소 16px (`text-base` 이상)
- 버튼: 최소 48x48px (`min-h-12 min-w-12`)
- 색상 대비: 4.5:1 이상
- 아이콘: 반드시 텍스트 레이블과 함께

## 파일 위치

| 카테고리 | 경로 |
|---------|------|
| 공통 | components/common/ |
| 간병인 | components/caregiver/ |
| 보호자 | components/guardian/ |
| 채팅 | components/chat/ |
| 레이아웃 | components/layout/ |
