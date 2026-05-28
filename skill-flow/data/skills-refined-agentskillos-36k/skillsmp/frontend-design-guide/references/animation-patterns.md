# Animation Patterns

## Table of Contents
1. [Framer Motion Basics](#framer-motion-basics)
2. [Button Interactions](#button-interactions)
3. [Conditional Animations (AnimatePresence)](#conditional-animations-animatepresence)
4. [useAnimation Hook](#useanimation-hook)
5. [Floating Liquidation Animation](#floating-liquidation-animation)
6. [Tailwind Custom Animations](#tailwind-custom-animations)

---

## Framer Motion Basics

### Import

```tsx
import { motion, AnimatePresence, useAnimation } from 'framer-motion';
```

### 기본 애니메이션

```tsx
<motion.div
  initial={{ opacity: 0, y: 10 }}
  animate={{ opacity: 1, y: 0 }}
  exit={{ opacity: 0 }}
  transition={{ duration: 0.3, ease: 'easeOut' }}
/>
```

### Transition Options

```tsx
transition={{
  duration: 0.3,           // 초 단위
  ease: 'easeOut',         // 이징 함수
  delay: 0.1,              // 지연 시간
}}

// 키프레임 타이밍
transition={{
  duration: 5,
  opacity: {
    times: [0, 0.1, 0.8, 1],  // 각 키프레임 타이밍 (0~1)
  },
}}
```

---

## Button Interactions

### whileHover / whileTap

```tsx
<motion.button
  whileHover={!disabled ? { scale: 1.02 } : undefined}
  whileTap={!disabled ? { scale: 0.98 } : undefined}
>
  Click me
</motion.button>
```

### 클릭 시 펄스 효과 (useAnimation)

```tsx
const controls = useAnimation();

const handleClick = () => {
  controls.start({
    scale: [1, 0.95, 1],
    transition: { duration: 0.15 },
  });
};

<motion.button animate={controls} onClick={handleClick}>
  Click
</motion.button>
```

---

## Conditional Animations (AnimatePresence)

조건부로 마운트/언마운트되는 요소에 exit 애니메이션 적용.

```tsx
<AnimatePresence>
  {isVisible && (
    <motion.div
      key="unique-key"  // 필수: key 지정
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
    >
      Content
    </motion.div>
  )}
</AnimatePresence>
```

### mode="wait" (순차 전환)

```tsx
<AnimatePresence mode="wait">
  {items.map((item) => (
    <motion.div key={item.id} exit={{ opacity: 0 }}>
      {item.content}
    </motion.div>
  ))}
</AnimatePresence>
```

---

## useAnimation Hook

프로그래매틱하게 애니메이션 제어.

```tsx
import { useAnimation } from 'framer-motion';

function Component() {
  const controls = useAnimation();

  // 트리거
  const triggerAnimation = async () => {
    await controls.start({
      scale: [1, 1.1, 1],
      transition: { duration: 0.3 },
    });
    // 애니메이션 완료 후 실행할 로직
  };

  return (
    <motion.div animate={controls}>
      Content
    </motion.div>
  );
}
```

---

## Floating Liquidation Animation

화면을 가로지르는 청산 애니메이션 (FloatingLiquidation.tsx 패턴).

### 기본 구조

```tsx
<motion.div
  className="fixed pointer-events-none z-40"
  initial={{
    x: startPosition.x,
    y: startPosition.y,
    opacity: 0,
    scale: 0.5,
  }}
  animate={{
    x: endPosition.x,
    y: endPosition.y,
    opacity: [0, 1, 1, 0],    // 키프레임: 페이드인 → 유지 → 페이드아웃
    scale: [0.5, 1, 1, 0.8],
  }}
  transition={{
    duration: 5,
    ease: 'linear',
    opacity: {
      times: [0, 0.1, 0.8, 1],  // 0%, 10%, 80%, 100% 지점
    },
  }}
  onAnimationComplete={onComplete}
/>
```

### 랜덤 시작 위치 계산

```tsx
const startPosition = useMemo(() => ({
  x: Math.random() > 0.5
    ? -200                          // 왼쪽에서 시작
    : window.innerWidth + 200,      // 오른쪽에서 시작
  y: Math.random() * (window.innerHeight * 0.7) + 100,
}), []);

const endPosition = useMemo(() => ({
  x: startPosition.x < 0
    ? window.innerWidth + 200       // 오른쪽으로 이동
    : -200,                         // 왼쪽으로 이동
  y: startPosition.y + (Math.random() - 0.5) * 200,
}), [startPosition]);
```

---

## Tailwind Custom Animations

`tailwind.config.js`에 정의된 커스텀 애니메이션.

### 설정

```js
// tailwind.config.js
animation: {
  'fade-in': 'fadeIn 0.3s ease-in-out',
  'slide-up': 'slideUp 0.3s ease-out',
  'pulse-fast': 'pulse 0.5s ease-in-out infinite',
},
keyframes: {
  fadeIn: {
    '0%': { opacity: '0' },
    '100%': { opacity: '1' },
  },
  slideUp: {
    '0%': { transform: 'translateY(10px)', opacity: '0' },
    '100%': { transform: 'translateY(0)', opacity: '1' },
  },
},
```

### 사용법

```tsx
className="animate-fade-in"
className="animate-slide-up"
className="animate-pulse-fast"
```
