# Color System

## Table of Contents
1. [Up/Down Theme](#updown-theme)
2. [Liquidation Colors (Long/Short)](#liquidation-colors-longshort)
3. [Tailwind Custom Colors](#tailwind-custom-colors)
4. [Dark Mode](#dark-mode)
5. [Gradient Patterns](#gradient-patterns)

---

## Up/Down Theme

기도 버튼 및 게이지에 사용되는 Up/Down 색상.

### Button Backgrounds

```tsx
// Up (상승) - 빨강 계열
className="bg-gradient-to-br from-red-400 to-red-600"
// hover state
className="hover:from-red-500 hover:to-red-700"

// Down (하락) - 파랑 계열
className="bg-gradient-to-br from-blue-400 to-blue-600"
// hover state
className="hover:from-blue-500 hover:to-blue-700"
```

### Text Colors

```tsx
// Up
className="text-red-500"

// Down
className="text-blue-500"
```

### Gauge Bar

```tsx
// Up 영역
className="bg-gradient-to-r from-red-400 to-red-500"

// Down 영역
className="bg-gradient-to-r from-blue-400 to-blue-500"
```

### Glow Effects

```tsx
// Up glow
className="bg-red-300 opacity-30"

// Down glow
className="bg-blue-300 opacity-30"
```

---

## Liquidation Colors (Long/Short)

청산 피드에 사용되는 Long/Short 색상. **Up/Down과 다름에 주의!**

### Tag Backgrounds

```tsx
// Long 청산 - 빨강
className="bg-red-500"
// with opacity
className="bg-red-500/20"

// Short 청산 - 초록
className="bg-green-500"
// with opacity
className="bg-green-500/20"
```

### Text Colors

```tsx
// Long
className="text-red-400"

// Short
className="text-green-400"
```

### 조건부 적용 예시

```tsx
const isLong = liquidation.side === 'LONG';

<div
  className={clsx(
    'px-3 py-1.5 rounded-full font-bold text-white',
    isLong ? 'bg-red-500' : 'bg-green-500'
  )}
>
  {isLong ? 'LONG' : 'SHORT'}
</div>
```

---

## Tailwind Custom Colors

`tailwind.config.js`에 정의된 커스텀 색상.

```js
// tailwind.config.js
colors: {
  prayer: {
    up: '#22c55e',    // green-500
    down: '#ef4444',  // red-500
  },
  liquidation: {
    long: '#ef4444',  // red-500
    short: '#22c55e', // green-500
  },
}
```

### 사용법

```tsx
// Tailwind 클래스로 사용
className="text-prayer-up"
className="bg-liquidation-long"
```

---

## Dark Mode

`darkMode: 'class'` 설정으로 활성화됨.

### 기본 패턴

```tsx
// 배경
className="bg-white dark:bg-gray-900"
className="bg-gray-100 dark:bg-gray-800"
className="bg-gray-200 dark:bg-gray-700"

// 텍스트
className="text-gray-900 dark:text-gray-100"
className="text-gray-600 dark:text-gray-400"
className="text-gray-500 dark:text-gray-500"

// 테두리
className="border-gray-200 dark:border-gray-700"
```

### 게이지 바 배경

```tsx
className="bg-gray-200 dark:bg-gray-700"
```

---

## Gradient Patterns

### 버튼 그라데이션

```tsx
// 기본 구조: bg-gradient-to-{direction}
// direction: t, tr, r, br, b, bl, l, tl

// 버튼에 주로 사용
className="bg-gradient-to-br from-{color}-400 to-{color}-600"
```

### 게이지 그라데이션

```tsx
// 수평 그라데이션
className="bg-gradient-to-r from-{color}-400 to-{color}-500"
```

### Disabled 상태

```tsx
// 비활성화 시 회색 처리
className={clsx(
  {
    'bg-gradient-to-br from-red-400 to-red-600': isUp && !disabled,
    'bg-gradient-to-br from-blue-400 to-blue-600': !isUp && !disabled,
    'bg-gray-400 cursor-not-allowed opacity-50': disabled,
  }
)}
```
