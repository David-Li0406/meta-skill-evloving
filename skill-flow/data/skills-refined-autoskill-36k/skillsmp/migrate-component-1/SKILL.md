---
name: migrate-component
description: 기존 디자인 컴포넌트를 officener-ui로 마이그레이션합니다. Figma 디자인과 기존 구현을 참조하여 CVA 기반 컴포넌트를 생성합니다. 컴포넌트 옮겨줘, 마이그레이션, officener-ui로 이전 요청 시 사용합니다.
---

# 컴포넌트 마이그레이션

> **⚠️ 이 스킬을 사용할 때 반드시 "migrate-component 스킬을 사용합니다"라고 먼저 알려주세요.**

기존 `officener-manager-frontend` 또는 `officener-frontend`의 컴포넌트를 `officener-ui`로 마이그레이션할 때 사용합니다.

## 작업 흐름

### 1단계: Figma 디자인 조회

```
mcp__figma__get_figma_data로 디자인 스펙 확인
- fileKey: lHZdfoOBOLyYDtY3lFHpi6
- nodeId: Figma URL에서 node-id 파라미터 추출
```

**추출할 정보:**
- Variants (variant, size, color 등)
- States (default, hover, active, disabled)
- 색상 값 (gray-500, blue-600 등)
- 크기 값 (h-9 w-9 등)

### 2단계: 기존 구현 확인

```bash
# 1. 컴포넌트 파일 찾기
Glob: **/[component-name]*.tsx

# 2. 주요 확인 위치
- officener-manager-frontend/src/components/ui/
- officener-manager-frontend/src/components/design-component/
- officener-frontend/src/components/ui/
```

**비교 포인트:**
| 항목 | manager-frontend | frontend |
|------|-----------------|----------|
| Navigation | react-router-dom | next/link |
| 스타일 | 직접 작성 | 직접 작성 |
| 상태 관리 | useSearchParams | URL params |

### 3단계: officener-ui 컴포넌트 생성

#### 파일 구조

```
officener-ui/
├── src/components/ui/[component].tsx
├── stories/[component].stories.tsx
└── src/index.tsx (export 추가)
```

#### 컴포넌트 패턴

**Primitive + High-level Component 패턴:**

```tsx
'use client';

import { Slot } from '@radix-ui/react-slot';
import { type VariantProps, cva } from 'class-variance-authority';
import * as React from 'react';
import { cn } from '@/lib/utils';

// 1. CVA Variants (Figma 스펙 기반)
const componentVariants = cva(
  'base-styles-from-figma',
  {
    variants: {
      variant: {
        default: 'variant-styles',
        // ...Figma variants
      },
      size: {
        sm: 'size-styles',
        // ...Figma sizes
      },
    },
    defaultVariants: {
      variant: 'default',
      size: 'sm',
    },
  },
);

// 2. Types
export interface ComponentProps
  extends React.ComponentProps<'div'>,
    VariantProps<typeof componentVariants> {
  asChild?: boolean;
}

// 3. Primitive Components (forwardRef 필수)
const Component = React.forwardRef<HTMLDivElement, ComponentProps>(
  ({ className, variant, size, asChild = false, ...props }, ref) => {
    const Comp = asChild ? Slot : 'div';
    return (
      <Comp
        ref={ref}
        className={cn(componentVariants({ variant, size }), className)}
        {...props}
      />
    );
  },
);
Component.displayName = 'Component';

// 4. High-level Component (선택적)
export interface ComponentWrapperProps {
  // framework-agnostic props
  value: string;
  onChange: (value: string) => void;
  // ...
}

const ComponentWrapper = ({ value, onChange, ...props }: ComponentWrapperProps) => {
  return (
    <Component>
      {/* Primitive 조합 */}
    </Component>
  );
};

// 5. Export
export { Component, ComponentWrapper, componentVariants };
```

### 4단계: Storybook 스토리 생성

```tsx
import type { Meta, StoryObj } from '@storybook/react';
import * as React from 'react';
import { Component, ComponentWrapper } from '../src/components/ui/component';

const meta = {
  title: 'Components/Component',
  component: ComponentWrapper, // High-level 컴포넌트를 메인으로
  tags: ['autodocs'],
  parameters: {
    layout: 'centered',
  },
  argTypes: {
    variant: {
      control: 'select',
      options: ['default', 'circle'], // Figma variants
    },
  },
} satisfies Meta<typeof ComponentWrapper>;

export default meta;
type Story = StoryObj<typeof meta>;

// Interactive Story (상태 관리 포함)
export const Default: Story = {
  render: () => {
    const [value, setValue] = React.useState('initial');
    return (
      <ComponentWrapper
        value={value}
        onChange={setValue}
      />
    );
  },
};

// All Variants
export const AllVariants: Story = {
  render: () => (
    <div className="flex flex-col gap-4">
      <ComponentWrapper variant="default" />
      <ComponentWrapper variant="circle" />
    </div>
  ),
};

// Primitives Example
export const Primitives: Story = {
  render: () => (
    <Component>
      Primitive 컴포넌트 직접 사용
    </Component>
  ),
};
```

### 5단계: Export 추가

```tsx
// src/index.tsx에 추가

export {
  Component,
  ComponentWrapper,
  componentVariants,
} from '@/components/ui/component';
export type {
  ComponentProps,
  ComponentWrapperProps,
} from '@/components/ui/component';
```

### 6단계: 빌드 및 검증

```bash
cd officener-ui && pnpm build
```

## Framework-Agnostic 원칙

| 기존 패턴 | officener-ui 패턴 |
|----------|------------------|
| `useSearchParams()` | `currentPage` + `onPageChange` props |
| `useNavigate()` | `onClick` handler |
| `<Link href={}>` | `asChild` + Slot 패턴 |
| `page` prop (URL용) | `onClick={() => onPageChange(page)}` |

## 스타일 결정 기준

1. **Figma 스펙이 최우선**
2. **기존 구현 참고** (manager-frontend 우선)
3. **충돌 시 사용자에게 질문**

## 체크리스트

- [ ] Figma 디자인 스펙 조회
- [ ] 기존 구현 확인 (manager-frontend, frontend)
- [ ] CVA variants 정의 (Figma 기반)
- [ ] Primitive 컴포넌트 생성 (forwardRef, displayName)
- [ ] High-level 컴포넌트 생성 (선택적)
- [ ] Framework-agnostic props (onClick, onChange 등)
- [ ] Storybook 스토리 생성
- [ ] index.tsx export 추가
- [ ] pnpm build 성공 확인
