# Testing with Assistive Technology

### Problem

Automated testing catches only 30-50% of issues.

### Solution: Manual + Assistive Tech Testing

**Testing Layers:**
```
Automated (30-50%) → Manual review → Screen reader → Keyboard-only → User testing
```

**Screen Reader Testing:**

| OS | Screen Reader | Browser |
|----|---------------|---------|
| Windows | NVDA (free) | Firefox, Chrome |
| Windows | JAWS | Chrome, Edge |
| macOS | VoiceOver | Safari |
| iOS | VoiceOver | Safari |
| Android | TalkBack | Chrome |

**Keyboard Testing:**
| Action | Keys |
|--------|------|
| Navigate | Tab, Shift+Tab |
| Activate | Enter, Space |
| Navigate options | Arrow keys |
| Exit/Cancel | Escape |
| Skip to main | Skip link |

**Common Issues Found:**
1. Missing form labels
2. No skip navigation
3. Inaccessible custom components
4. Missing alt text
5. Poor focus management
6. Keyboard traps
