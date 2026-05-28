# Dynamic Resolution Scaler (R3F)

Use this reference when you need a drop-in dynamic DPR scaler similar to `src/components/DynamicResScaler.tsx`.

## Drop-in Implementation

```tsx
import { useFrame, useThree } from '@react-three/fiber';
import { useEffect, useRef } from 'react';

const TARGET_FPS = 60;
const CHECK_INTERVAL = 500; // ms
const FPS_TOLERANCE = 5;
const MIN_DPR = 0.5;
const MAX_DPR = typeof window !== 'undefined' ? Math.min(window.devicePixelRatio, 2) : 1;
const STEP = 0.1;

export function DynamicResScaler() {
  const setDpr = useThree((state) => state.setDpr);
  const frameCount = useRef(0);
  const lastTime = useRef(performance.now());
  const dprRef = useRef(MAX_DPR);

  useEffect(() => {
    setDpr(dprRef.current);
  }, [setDpr]);

  useFrame(() => {
    frameCount.current += 1;
    const time = performance.now();
    const elapsed = time - lastTime.current;

    if (elapsed >= CHECK_INTERVAL) {
      const fps = Math.round((frameCount.current * 1000) / elapsed);
      frameCount.current = 0;
      lastTime.current = time;

      let nextDpr = dprRef.current;
      if (fps < TARGET_FPS - FPS_TOLERANCE) {
        nextDpr = Math.max(MIN_DPR, dprRef.current - STEP);
      } else if (fps > TARGET_FPS + FPS_TOLERANCE) {
        nextDpr = Math.min(MAX_DPR, dprRef.current + STEP);
      }

      if (nextDpr !== dprRef.current) {
        dprRef.current = nextDpr;
        setDpr(nextDpr);
        if (process.env.NODE_ENV === 'development') {
          console.log(`[DynamicResScaler] FPS: ${fps}, DPR: ${nextDpr.toFixed(2)}`);
        }
      }
    }
  });

  return null;
}
```

## Usage Notes

- Mount inside the `Canvas` tree (near the root) so it always runs.
- Keep counters in refs to avoid re-render churn.
- Cap `MAX_DPR` so high-DPI screens do not overwhelm fill rate.
- Use small `STEP` values to minimize visible resolution jumps.
