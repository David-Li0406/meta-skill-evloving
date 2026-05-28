---
name: frontend-design-guide
description: |
  청산 기도 메타 프로젝트의 프론트엔드 디자인 가이드. 새 컴포넌트 생성, UI 스타일링, 애니메이션 구현 시 사용.

  **트리거 조건:**
  - 새 React 컴포넌트 생성 요청
  - UI 스타일링 또는 Tailwind CSS 관련 작업
  - Framer Motion 애니메이션 구현
  - Jotai 상태 관리 패턴 적용
  - Up/Down 또는 Long/Short 색상 적용
  - 다크모드, 반응형, i18n 관련 작업
---

# Frontend Design Guide

청산 기도 메타 프론트엔드의 디자인 일관성을 위한 가이드.

## Tech Stack

- **Tailwind CSS** + **clsx** (조건부 클래스)
- **Framer Motion** (애니메이션)
- **Jotai** (상태 관리)
- **react-i18next** (다국어)

## Quick Reference

### 색상 (Up/Down)

| 용도 | Up (상승) | Down (하락) |
|------|----------|-------------|
| 버튼 | `from-red-400 to-red-600` | `from-blue-400 to-blue-600` |
| 텍스트 | `text-red-500` | `text-blue-500` |
| 게이지 | `from-red-400 to-red-500` | `from-blue-400 to-blue-500` |

### 청산 색상 (Long/Short)

| 용도 | Long | Short |
|------|------|-------|
| 태그 배경 | `bg-red-500` | `bg-green-500` |
| 텍스트 | `text-red-400` | `text-green-400` |

상세 색상 가이드: [references/color-system.md](references/color-system.md)

### 컴포넌트 기본 구조

```tsx
import { motion } from 'framer-motion';
import { clsx } from 'clsx';
import { useAtomValue } from 'jotai';
import { useTranslation } from 'react-i18next';

interface ComponentNameProps {
  value: number;
  disabled?: boolean;
  onChange: (value: number) => void;
}

export function ComponentName({ value, disabled = false, onChange }: ComponentNameProps) {
  const { t } = useTranslation();

  return (
    <motion.div
      className={clsx('base-styles', { 'conditional-style': disabled })}
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
    >
      {/* content */}
    </motion.div>
  );
}
```

## File Structure

```
frontend/src/
├── components/
│   ├── prayer/       # 기도 버튼 (PrayerButton, NumberParticle)
│   ├── gauge/        # 게이지 바 (GaugeBar, RpmIndicator)
│   ├── liquidation/  # 청산 피드 (LiquidationFeed, FloatingLiquidation)
│   ├── ticker/       # BTC 시세 (TickerDisplay)
│   ├── effects/      # 화면 효과 (ScreenFlash, ScreenShake)
│   ├── sound/        # 사운드 컨트롤 (SoundToggle, BgmToggle)
│   ├── layout/       # 레이아웃 (Header, ThemeToggle)
│   ├── mobile/       # 모바일 전용 (MobileLayout, MobilePrayerButtons)
│   └── ui/           # 공통 UI (Toast)
├── stores/           # Jotai atoms
└── hooks/            # Custom hooks
```

## Patterns

### clsx 조건부 스타일

```tsx
className={clsx(
  'base-class rounded-2xl',
  {
    'bg-red-500': isUp,
    'bg-blue-500': !isUp,
    'opacity-50 cursor-not-allowed': disabled,
  }
)}
```

### Jotai 상태 관리

```tsx
// 읽기 전용
const count = useAtomValue(prayerCountAtom);

// 쓰기 전용
const setCount = useSetAtom(prayerCountAtom);

// 읽기 + 쓰기
const [count, setCount] = useAtom(prayerCountAtom);
```

### 반응형 breakpoint

- 모바일: `< 768px` (기본)
- 데스크톱: `md:` (`>= 768px`)
- 대형: `lg:` (`>= 1024px`)

```tsx
className="h-32 md:h-40 lg:h-48"
className="text-lg md:text-xl lg:text-2xl"
```

### 다크모드

`dark:` prefix 사용, `darkMode: 'class'` 설정됨.

```tsx
className="bg-gray-200 dark:bg-gray-700"
```

## Reference Files

| 파일 | 내용 |
|------|------|
| [color-system.md](references/color-system.md) | 색상 팔레트, 커스텀 색상, 그라데이션 |
| [animation-patterns.md](references/animation-patterns.md) | Framer Motion 패턴, 버튼 인터랙션, 청산 애니메이션 |
| [component-examples.md](references/component-examples.md) | 실제 컴포넌트 구현 예제 |

## Checklist

새 컴포넌트 구현 시:

- [ ] clsx로 조건부 스타일 관리
- [ ] Up/Down, Long/Short 색상 가이드 준수
- [ ] `dark:` prefix로 다크모드 지원
- [ ] `md:` / `lg:` breakpoint로 반응형 처리
- [ ] Framer Motion으로 애니메이션 구현
- [ ] Props 인터페이스 명시적 정의
- [ ] 필요시 `useTranslation` 으로 i18n 지원
