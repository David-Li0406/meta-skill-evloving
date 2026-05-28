# Component Examples

실제 프로젝트에서 사용되는 컴포넌트 구현 예제.

## Table of Contents
1. [PrayerButton](#prayerbutton)
2. [GaugeBar](#gaugebar)
3. [FloatingLiquidation](#floatingliquidation)
4. [Jotai Store Pattern](#jotai-store-pattern)

---

## PrayerButton

기도 버튼 컴포넌트 (`frontend/src/components/prayer/PrayerButton.tsx`).

### 핵심 패턴

- clsx 조건부 스타일
- Framer Motion useAnimation
- Up/Down 색상 분기

```tsx
import { useCallback, useRef } from 'react';
import { motion, useAnimation } from 'framer-motion';
import { clsx } from 'clsx';
import { useTranslation } from 'react-i18next';
import type { Side } from '@/types/prayer';

interface PrayerButtonProps {
  side: Side;
  count: number;
  disabled?: boolean;
  onPray: (side: Side, event: React.MouseEvent) => void;
}

export function PrayerButton({
  side,
  count,
  disabled = false,
  onPray,
}: PrayerButtonProps) {
  const { t } = useTranslation();
  const controls = useAnimation();
  const isUp = side === 'up';

  const handleClick = useCallback(
    (event: React.MouseEvent) => {
      if (disabled) return;

      // 펄스 애니메이션
      controls.start({
        scale: [1, 0.95, 1],
        transition: { duration: 0.15 },
      });

      onPray(side, event);
    },
    [side, disabled, onPray, controls]
  );

  return (
    <motion.button
      animate={controls}
      onClick={handleClick}
      disabled={disabled}
      className={clsx(
        // 기본 스타일
        'relative w-full h-32 md:h-40 lg:h-48',
        'rounded-2xl font-bold text-white',
        'transition-all duration-200',
        'flex flex-col items-center justify-center gap-2',
        'shadow-lg active:shadow-md',
        // 조건부 스타일
        {
          'bg-gradient-to-br from-red-400 to-red-600 hover:from-red-500 hover:to-red-700':
            isUp && !disabled,
          'bg-gradient-to-br from-blue-400 to-blue-600 hover:from-blue-500 hover:to-blue-700':
            !isUp && !disabled,
          'bg-gray-400 cursor-not-allowed opacity-50': disabled,
        }
      )}
      whileHover={!disabled ? { scale: 1.02 } : undefined}
      whileTap={!disabled ? { scale: 0.98 } : undefined}
    >
      <div className="text-4xl md:text-5xl">{isUp ? '🚀' : '📉'}</div>
      <div className="text-lg md:text-xl font-semibold">{t(`prayer.${side}`)}</div>
      <div className="text-2xl md:text-3xl font-bold">{count.toLocaleString()}</div>
    </motion.button>
  );
}
```

---

## GaugeBar

게이지 바 컴포넌트 (`frontend/src/components/gauge/GaugeBar.tsx`).

### 핵심 패턴

- Jotai useAtomValue
- 애니메이션 width transition
- 다크모드 지원

```tsx
import { motion } from 'framer-motion';
import { useAtomValue } from 'jotai';
import { localCountAtom } from '@/stores/prayerStore';
import { useTranslation } from 'react-i18next';

export function GaugeBar() {
  const { t } = useTranslation();
  const count = useAtomValue(localCountAtom);

  const upPercentage = count.upRatio * 100;
  const downPercentage = count.downRatio * 100;

  return (
    <div className="w-full max-w-2xl mx-auto px-4">
      {/* 퍼센트 라벨 */}
      <div className="flex justify-between mb-2 text-sm font-medium">
        <span className="text-red-500">{upPercentage.toFixed(1)}%</span>
        <span className="text-blue-500">{downPercentage.toFixed(1)}%</span>
      </div>

      {/* 게이지 바 */}
      <div className="h-4 rounded-full overflow-hidden bg-gray-200 dark:bg-gray-700 flex">
        <motion.div
          className="h-full bg-gradient-to-r from-red-400 to-red-500"
          initial={{ width: '50%' }}
          animate={{ width: `${upPercentage}%` }}
          transition={{ duration: 0.3, ease: 'easeOut' }}
        />
        <motion.div
          className="h-full bg-gradient-to-r from-blue-400 to-blue-500 flex-1"
          initial={{ width: '50%' }}
          animate={{ width: `${downPercentage}%` }}
          transition={{ duration: 0.3, ease: 'easeOut' }}
        />
      </div>

      {/* RPM 표시 */}
      <div className="flex justify-between mt-2 text-xs text-gray-500 dark:text-gray-400">
        <span>{count.upRpm.toFixed(0)} {t('prayer.rpm')}</span>
        <span>{count.downRpm.toFixed(0)} {t('prayer.rpm')}</span>
      </div>
    </div>
  );
}
```

---

## FloatingLiquidation

떠다니는 청산 텍스트 (`frontend/src/components/liquidation/FloatingLiquidation.tsx`).

### 핵심 패턴

- 랜덤 시작/종료 위치 계산
- 키프레임 애니메이션
- onAnimationComplete 콜백

```tsx
import { motion } from 'framer-motion';
import { useMemo } from 'react';
import type { Liquidation } from '@/types/liquidation';

interface FloatingLiquidationProps {
  liquidation: Liquidation;
  fadeOutDuration: number;
  onComplete: () => void;
}

export function FloatingLiquidation({
  liquidation,
  fadeOutDuration,
  onComplete,
}: FloatingLiquidationProps) {
  const isLong = liquidation.side === 'LONG';

  // 랜덤 시작 위치
  const startPosition = useMemo(() => ({
    x: Math.random() > 0.5 ? -200 : window.innerWidth + 200,
    y: Math.random() * (window.innerHeight * 0.7) + 100,
  }), []);

  // 반대편 종료 위치
  const endPosition = useMemo(() => ({
    x: startPosition.x < 0 ? window.innerWidth + 200 : -200,
    y: startPosition.y + (Math.random() - 0.5) * 200,
  }), [startPosition]);

  return (
    <motion.div
      className="fixed pointer-events-none z-40 flex items-center gap-2"
      initial={{ x: startPosition.x, y: startPosition.y, opacity: 0, scale: 0.5 }}
      animate={{
        x: endPosition.x,
        y: endPosition.y,
        opacity: [0, 1, 1, 0],
        scale: [0.5, 1, 1, 0.8],
      }}
      transition={{
        duration: fadeOutDuration / 1000,
        ease: 'linear',
        opacity: { times: [0, 0.1, 0.8, 1] },
      }}
      onAnimationComplete={onComplete}
    >
      <div className={`px-3 py-1.5 rounded-full font-bold text-white text-sm ${isLong ? 'bg-red-500' : 'bg-green-500'}`}>
        <span className="opacity-75 mr-1">{isLong ? 'LONG' : 'SHORT'}</span>
        <span>${liquidation.usdValue.toLocaleString()}</span>
      </div>
    </motion.div>
  );
}
```

---

## Jotai Store Pattern

상태 관리 패턴 (`frontend/src/stores/prayerStore.ts`).

### 핵심 패턴

- 기본 atom
- 파생 atom (derived atom)
- Optimistic updates

```tsx
import { atom } from 'jotai';
import type { PrayerCount, PendingPrayer } from '@/types/prayer';

// 서버 동기화 상태
export const prayerCountAtom = atom<PrayerCount>({
  upCount: 0,
  downCount: 0,
  upRpm: 0,
  downRpm: 0,
  upRatio: 0.5,
  downRatio: 0.5,
  timestamp: Date.now(),
});

// 대기 중인 클릭 (optimistic)
export const pendingPrayersAtom = atom<PendingPrayer[]>([]);

// 파생 atom: 서버 + pending = 로컬 상태
export const localCountAtom = atom((get) => {
  const serverCount = get(prayerCountAtom);
  const pending = get(pendingPrayersAtom);

  const pendingUp = pending
    .filter((p) => p.side === 'up')
    .reduce((sum, p) => sum + p.count, 0);
  const pendingDown = pending
    .filter((p) => p.side === 'down')
    .reduce((sum, p) => sum + p.count, 0);

  const upCount = serverCount.upCount + pendingUp;
  const downCount = serverCount.downCount + pendingDown;
  const total = upCount + downCount;

  return {
    ...serverCount,
    upCount,
    downCount,
    upRatio: total > 0 ? upCount / total : 0.5,
    downRatio: total > 0 ? downCount / total : 0.5,
  };
});
```

### 컴포넌트에서 사용

```tsx
import { useAtomValue, useSetAtom, useAtom } from 'jotai';
import { prayerCountAtom, localCountAtom } from '@/stores/prayerStore';

// 읽기 전용 (최적화됨)
const localCount = useAtomValue(localCountAtom);

// 쓰기 전용
const setPrayerCount = useSetAtom(prayerCountAtom);

// 읽기 + 쓰기
const [count, setCount] = useAtom(prayerCountAtom);
```
