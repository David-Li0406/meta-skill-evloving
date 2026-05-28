---
name: mobile-haptics
description: Haptic feedback patterns for mobile games using Vibration API
category: development
depends-on: [r3f-fundamentals]
---

# Mobile Haptics Skill

> "Haptic feedback transforms flat screens into tactile experiences."

## When to Use This Skill

Use when:
- Building mobile/touch controls
- Adding game feel to actions
- Providing feedback for UI interactions
- Enhancing immersion on mobile devices
- Creating accessible gameplay experiences

## Quick Start

```tsx
// Simple vibration feedback
function triggerHaptic(duration = 10) {
  if ('vibrate' in navigator) {
    navigator.vibrate(duration);
  }
}

// Usage
<button onClick={() => triggerHaptic(10)}>Tap</button>
```

## Browser Support

| Browser | Android | iOS | Notes |
| ------- | ------- | ----- | ----- |
| Chrome | ✅ Full | ❌ No | Full Vibration API support |
| Firefox | ✅ Full | ❌ No | Full Vibration API support |
| Safari | ✅ Full | ❌ No | Desktop only |
| Edge | ✅ Full | ❌ No | Chromium-based |

**iOS Note**: iOS does NOT support the Vibration API. Use Taptic Engine feedback via native wrappers (Capacitor, React Native) for iOS.

## Haptic Patterns

### Tap Feedback (UI Interactions)

```tsx
// Light tap for button presses
function tapFeedback() {
  navigator.vibrate(10); // 10ms - very subtle
}

// Medium tap for toggle switches
function toggleFeedback() {
  navigator.vibrate(25); // 25ms - noticeable
}

// Heavy tap for confirm actions
function confirmFeedback() {
  navigator.vibrate(50); // 50ms - strong
}
```

### Impact Patterns (Game Actions)

```tsx
// Light impact - shooting, collecting items
function lightImpact() {
  navigator.vibrate(15);
}

// Medium impact - jumping, landing
function mediumImpact() {
  navigator.vibrate(30);
}

// Heavy impact - explosions, damage
function heavyImpact() {
  navigator.vibrate([50, 30, 50]); // Pattern: hit, pause, hit
}
```

### Success Pattern

```tsx
// Success - triple tap pattern
function successHaptic() {
  navigator.vibrate([10, 50, 10, 50, 10]);
}

// Level complete - ascending pattern
function levelCompleteHaptic() {
  navigator.vibrate([10, 50, 20, 50, 30]);
}
```

### Error Pattern

```tsx
// Error - double tap
function errorHaptic() {
  navigator.vibrate([50, 100, 50]);
}

// Deny - single long pulse
function denyHaptic() {
  navigator.vibrate(100);
}
```

### Notification Patterns

```tsx
// Gentle reminder
function gentleNotification() {
  navigator.vibrate([20, 100, 20]);
}

// Urgent alert
function urgentAlert() {
  navigator.vibrate([50, 50, 50, 50, 50]);
}

// Incoming call style
function ringingPattern() {
  // Repeating pattern - caller should loop
  navigator.vibrate([100, 200, 100]);
}
```

## Game-Specific Patterns

### Shooting Feedback

```tsx
// Single shot
function shootFeedback() {
  navigator.vibrate(15);
}

// Rapid fire
function rapidFireFeedback() {
  // Don't vibrate on every shot - too overwhelming
  // Vibrate every 5th shot instead
}

// Empty ammo click
function emptyClickFeedback() {
  navigator.vibrate([10, 30, 10]);
}
```

### Damage Feedback

```tsx
// Light damage
function lightDamageFeedback() {
  navigator.vibrate(25);
}

// Heavy damage
function heavyDamageFeedback() {
  navigator.vibrate([80, 20, 80]);
}

// Death/respawn
function deathFeedback() {
  navigator.vibrate([100, 50, 100, 50, 200]);
}
```

### Movement Feedback

```tsx
// Footsteps - subtle, rhythmic
let stepCount = 0;
function stepFeedback() {
  // Only vibrate every 3rd step
  if (stepCount % 3 === 0) {
    navigator.vibrate(5);
  }
  stepCount++;
}

// Jump
function jumpFeedback() {
  navigator.vibrate([10, 20, 30]); // Ascending pattern
}

// Landing
function landFeedback() {
  const intensity = Math.min(fallDistance / 10, 1);
  navigator.vibrate(20 + intensity * 40);
}
```

### Touch Controls Feedback

```tsx
// Button press start
function onPressStart() {
  navigator.vibrate(10);
}

// Button press release (cancel)
function onPressCancel() {
  navigator.vibrate([10, 20, 5]);
}

// Virtual joystick movement
function joystickMove(distance: number) {
  // Subtle feedback when reaching joystick edge
  if (distance > 0.9) {
    navigator.vibrate(3);
  }
}
```

## React Hook for Haptics

```tsx
import { useCallback, useEffect, useRef } from 'react';

interface HapticOptions {
  enabled?: boolean;
  intensity?: number; // 0-1 multiplier
  iosFallback?: () => void; // For iOS devices
}

export function useHaptics(options: HapticOptions = {}) {
  const { enabled = true, intensity = 1, iosFallback } = options;
  const isSupported = useRef('vibrate' in navigator);
  const isIOS = /iPhone|iPad|iPod/i.test(navigator.userAgent);

  const vibrate = useCallback((pattern: number | number[]): boolean => {
    if (!enabled) return false;

    if (isIOS && iosFallback) {
      iosFallback();
      return true;
    }

    if (!isSupported.current) return false;

    // Apply intensity multiplier
    const adjustedPattern = Array.isArray(pattern)
      ? pattern.map(d => Math.round(d * intensity))
      : Math.round(pattern * intensity);

    return navigator.vibrate(adjustedPattern);
  }, [enabled, intensity, iosFallback]);

  const tap = useCallback(() => vibrate(10), [vibrate]);
  const light = useCallback(() => vibrate(15), [vibrate]);
  const medium = useCallback(() => vibrate(30), [vibrate]);
  const heavy = useCallback(() => vibrate([50, 30, 50]), [vibrate]);
  const success = useCallback(() => vibrate([10, 50, 10, 50, 10]), [vibrate]);
  const error = useCallback(() => vibrate([50, 100, 50]), [vibrate]);
  const warning = useCallback(() => vibrate([20, 50, 20]), [vibrate]);

  return {
    isSupported: isSupported.current,
    isIOS,
    vibrate,
    tap,
    light,
    medium,
    heavy,
    success,
    error,
    warning,
  };
}

// Usage
function GameButton({ onClick, children }) {
  const { tap } = useHaptics();

  return (
    <button
      onClick={() => {
        tap();
        onClick();
      }}
    >
      {children}
    </button>
  );
}
```

## iOS Fallback (Taptic Engine)

```tsx
// iOS requires native bridge - placeholder pattern
// Actual implementation requires Capacitor or React Native

interface TapticEngine {
  selection(): void;
  impact(style: 'light' | 'medium' | 'heavy'): void;
  notification(type: 'success' | 'warning' | 'error'): void;
}

// Capacitor example
import { Haptics, ImpactStyle } from '@capacitor/haptics';

export function useHapticsWithIOS() {
  const isIOS = /iPhone|iPad|iPod/i.test(navigator.userAgent);

  const impact = async (style: 'light' | 'medium' | 'heavy' = 'medium') => {
    if (!isIOS) {
      navigator.vibrate(style === 'light' ? 15 : style === 'medium' ? 30 : 50);
      return;
    }

    const impactStyle = {
      light: ImpactStyle.Light,
      medium: ImpactStyle.Medium,
      heavy: ImpactStyle.Heavy,
    }[style];

    await Haptics.impact({ style: impactStyle });
  };

  const notification = async (type: 'success' | 'warning' | 'error') => {
    if (!isIOS) {
      const patterns = {
        success: [10, 50, 10, 50, 10],
        warning: [20, 50, 20],
        error: [50, 100, 50],
      };
      navigator.vibrate(patterns[type]);
      return;
    }

    const notificationType = {
      success: 'SUCCESS' as const,
      warning: 'WARNING' as const,
      error: 'ERROR' as const,
    }[type];

    await Haptics.notification({ type: notificationType });
  };

  return { impact, notification };
}
```

## Integration with TouchControls

```tsx
import { useHaptics } from './useHaptics';

function TouchControls() {
  const { tap, light, medium } = useHaptics();

  const handleJumpStart = () => medium();
  const handleShootStart = () => light();
  const handleButtonPress = () => tap();

  return (
    <div className="touch-controls">
      <Joystick onTouchMove={handleJoystickMove} onTouchEnd={handleButtonPress} />
      <ActionButton onTouchStart={handleJumpStart}>Jump</ActionButton>
      <ActionButton onTouchStart={handleShootStart}>Shoot</ActionButton>
    </div>
  );
}
```

## Best Practices

### DO ✅

- Keep haptic feedback short (5-50ms)
- Match feedback intensity to action importance
- Provide settings to disable haptics
- Use subtle patterns for repetitive actions
- Test on actual devices (emulators may not vibrate)
- Consider battery life for continuous feedback

### DON'T ❌

- Overuse haptics (causes fatigue)
- Vibrate for longer than 100ms continuously
- Assume all devices support vibration
- Use haptics as the only feedback mechanism
- Forget iOS doesn't support Vibration API

## Settings Integration

```tsx
// User should be able to disable haptics
interface GameSettings {
  hapticsEnabled: boolean;
  hapticIntensity: number; // 0-1
}

function useHapticsWithSettings(settings: GameSettings) {
  return useHaptics({
    enabled: settings.hapticsEnabled,
    intensity: settings.hapticIntensity,
  });
}
```

## Checklist

When implementing haptic feedback:

- [ ] Feature detection for `navigator.vibrate`
- [ ] iOS fallback or graceful degradation
- [ ] User settings to disable haptics
- [ ] Intensity slider in settings
- [ ] Test on physical Android device
- [ ] Patterns are short (< 100ms)
- [ ] Feedback matches action importance
- [ ] Not overusing (causes fatigue)

## Reference

- [MDN Vibration API](https://developer.mozilla.org/en-US/docs/Web/API/Vibration_API)
- [Vibration Pattern Best Practices](https://web.dev/vibration-pattern-design/)
- [Capacitor Haptics Plugin](https://capacitorjs.com/docs/apis/haptics)
- [agents/developer/skills/game-ui-animations.md](game-ui-animations.md) — UI animation patterns
