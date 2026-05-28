---
name: mobile-game-development
description: Use this skill when you need to understand the principles of mobile game development, including touch input, performance optimization, and app store requirements.
---

# Mobile Game Development

> Platform constraints and optimization principles.

## 1. Platform Considerations

### Key Constraints

| Constraint        | Strategy                  |
| ----------------- | ------------------------- |
| **Touch input**   | Large hit areas, gestures |
| **Battery**       | Limit CPU/GPU usage       |
| **Thermal**       | Throttle when hot         |
| **Screen size**   | Responsive UI             |
| **Interruptions** | Pause on background       |

## 2. Touch Input Principles

### Touch vs Controller

| Touch              | Desktop/Console |
| ------------------ | --------------- |
| Imprecise          | Precise         |
| Occludes screen    | No occlusion    |
| Limited buttons    | Many buttons    |
| Gestures available | Buttons/sticks  |

### Best Practices

- Minimum touch target: 44x44 points
- Visual feedback on touch
- Avoid precise timing requirements
- Support both portrait and landscape orientations

## 3. Performance Targets

### Thermal Management

| Action         | Trigger       |
| -------------- | ------------- |
| Reduce quality | Device warm   |
| Limit FPS      | Device hot    |
| Pause effects  | Critical temp |

### Battery Optimization

- 30 FPS is often sufficient
- Sleep when paused
- Minimize GPS/network usage
- Dark mode saves OLED battery

## 4. App Store Requirements

### iOS (App Store)

| Requirement      | Note                       |
| ---------------- | -------------------------- |
| Privacy labels   | Required                   |
| Account deletion | If account creation exists |
| Screenshots      | For all device sizes       |

### Android (Google Play)

| Requirement | Note               |
| ----------- | ------------------ |
| Target API  | Current year's SDK |
| 64-bit      | Required           |
| App bundles | Recommended        |

## 5. Monetization Models

| Model            | Best For                      |
| ---------------- | ----------------------------- |
| **Premium**      | Quality games, loyal audience |
| **Free + IAP**   | Casual, progression-based     |
| **Ads**          | Hyper-casual, high volume     |
| **Subscription** | Content updates, multiplayer  |

## 6. Anti-Patterns

| ❌ Don't                   | ✅ Do                     |
| -------------------------- | ------------------------- |
| Desktop controls on mobile | Design for touch          |
| Ignore battery drain       | Monitor thermals          |
| Force landscape            | Support player preference  |
| Always-on network          | Cache and sync            |

> **Remember:** Mobile is the most constrained platform. Respect battery and user attention.