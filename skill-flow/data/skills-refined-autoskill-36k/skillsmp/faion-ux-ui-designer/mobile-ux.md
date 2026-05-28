---
id: mobile-ux
name: "Mobile UX Design"
domain: UX
skill: faion-ux-ui-designer
category: "ux-design"
---

# Mobile UX Design

## Metadata
- **Category:** UX / Design Methods
- **Difficulty:** Intermediate
- **Tags:** #methodology #ux #design #mobile #responsive
- **Agent:** faion-usability-agent

---

## Problem

Desktop designs scaled down look bad on mobile. Touch targets are too small. Users abandon mobile experiences. Mobile is an afterthought. Performance suffers on slower connections. Context of mobile use is ignored.

Without mobile UX focus:
- Poor mobile experience
- High abandonment
- Frustrated users
- Missed opportunities

---

## Framework

### Mobile-First Thinking

Start with mobile, enhance for larger screens. This forces focus on essential content and functionality.

```
Mobile-First Approach:
1. Design for smallest screen first
2. Identify core content and features
3. Add enhancements for larger screens
4. Test across devices
```

### Mobile Context

| Factor | Consideration |
|--------|---------------|
| **Attention** | Partial attention, interruptions |
| **Time** | Short sessions, quick tasks |
| **Location** | Variable environments |
| **Connection** | Slow or unreliable network |
| **Input** | Touch, sometimes voice |
| **Screen** | Small, varying sizes |

### Key Mobile Principles

| Principle | Implementation |
|-----------|----------------|
| **Focus** | One primary action per screen |
| **Simplify** | Reduce choices and steps |
| **Speed** | Fast loading, instant feedback |
| **Reachability** | Important actions in thumb zone |
| **Context** | Leverage device capabilities |

---

## Process

### Step 1: Define Mobile User Goals

Understand why users come to mobile:

```
Questions:
- What tasks do users need on mobile?
- What can be done on mobile vs. desktop?
- What context are users in?
- What are the micro-moments?
```

### Step 2: Prioritize Features

Not everything belongs on mobile:

| Priority | Features |
|----------|----------|
| **Must have** | Core functionality, most common tasks |
| **Should have** | Important but can be simplified |
| **Nice to have** | Enhanced on larger screens |
| **Desktop only** | Complex tasks, rarely needed |

### Step 3: Design for Touch

**Touch target minimums:**
- iOS: 44 x 44 pt
- Android: 48 x 48 dp
- Space between targets: 8+ px

**Thumb zone:**
```
Phone held in one hand:
┌─────────────────┐
│   HARD TO       │
│   REACH         │
├─────────────────┤
│   OK TO         │
│   REACH         │
├─────────────────┤
│   EASY          │ ← Primary actions here
│   ZONE          │
└─────────────────┘
```

### Step 4: Simplify Navigation

**Mobile navigation patterns:**

| Pattern | When to use |
|---------|-------------|
| **Bottom tab bar** | 3-5 main sections |
| **Hamburger menu** | Many sections, less frequent |
| **Tab bar** | 2-5 content types |
| **Full-screen menu** | Focused selection |
| **Gesture navigation** | Supplement, not replace |

### Step 5: Optimize Forms

**Mobile form best practices:**
- Minimize required fields
- Use appropriate input types
- Show progress for multi-step
- Auto-fill when possible
- Large touch targets
- Clear error messages
- Show/hide password option

### Step 6: Design for Performance

**Performance matters:**
- Users expect pages in <3 seconds
- 53% abandon if >3 seconds
- Every second costs conversions

**Techniques:**
- Optimize images
- Lazy load content
- Minimize requests
- Use skeleton screens
- Cache aggressively

---

## Templates

### Mobile Design Checklist Template

```markdown
# Mobile UX Checklist: [Screen/Feature]

**Date:** [Date]
**Designer:** [Name]
**Device targets:** [iOS/Android/Both]

## Touch Targets

- [ ] Primary buttons: 44pt minimum
- [ ] Clickable text links: adequate spacing
- [ ] Form inputs: easy to tap
- [ ] No targets too close together

## Thumb Reachability

- [ ] Primary actions in easy zone
- [ ] Critical CTAs reachable one-handed
- [ ] Toolbar actions accessible

## Navigation

- [ ] Clear back/close actions
- [ ] Current location obvious
- [ ] Key actions visible (not buried)
- [ ] Gestures have visible alternatives

## Content

- [ ] Key content above fold
- [ ] Text readable without zooming (16px minimum)
- [ ] Images sized for mobile
- [ ] Horizontal scrolling avoided

## Forms

- [ ] Appropriate keyboard types (email, number, etc.)
- [ ] Labels visible when typing
- [ ] Error messages near fields
- [ ] Minimal required fields

## Performance

- [ ] Page loads in <3 seconds on 3G
- [ ] Images optimized
- [ ] Loading states present
- [ ] Offline behavior defined

## Gestures

- [ ] Standard gestures only
- [ ] Alternatives for all gestures
- [ ] Accidental gestures prevented

## Orientation

- [ ] Works in portrait (primary)
- [ ] Works in landscape (if needed)
- [ ] No content lost on rotation
```

### Mobile Pattern Documentation

```markdown
# Mobile Pattern: [Pattern Name]

## Overview
[What this pattern is for]

## When to Use
- [Situation 1]
- [Situation 2]

## When NOT to Use
- [Counter-situation]

## Specifications

### iOS
- Size: [Dimensions]
- Font: [Typography]
- Colors: [Color specs]
- Animation: [Motion specs]

### Android
- Size: [Dimensions]
- Font: [Typography]
- Colors: [Color specs]
- Animation: [Motion specs]

## Behavior

**Default State:**
[Description]

**Active/Pressed State:**
[Description]

**Disabled State:**
[Description]

## Accessibility

- VoiceOver/TalkBack: [How it's announced]
- Focus order: [Tab sequence]
- Touch target: [Size]

## Examples

[Screenshots or links]

## Code Reference

[Link to component]
```

---

## Examples

### Example 1: Mobile Checkout Optimization

**Problem:** 68% mobile cart abandonment

**Before:**
- 5-step checkout
- Desktop-sized forms
- No autofill
- Hidden cost summary

**After:**
- 2-step checkout
- Numeric keyboard for phone/card
- Apple Pay / Google Pay
- Sticky order summary

**Result:** Abandonment reduced to 45%

### Example 2: Mobile Search

**Problem:** Users can't find products on mobile

**Changes:**
- Search bar always visible (not in menu)
- Recent searches shown
- Auto-suggest with images
- Filter overlay (not inline)
- Sort as floating button

**Result:** Search usage up 40%

---

## Platform Considerations

### iOS vs. Android

| Element | iOS | Android |
|---------|-----|---------|
| **Navigation** | Bottom tab, back gesture | Bottom nav, back button |
| **Touch targets** | 44pt | 48dp |
| **Modals** | Sheets from bottom | Full-screen or dialog |
| **Search** | Search bar in nav | Search icon in toolbar |
| **Actions** | Right side of screen | Floating action button |

### Progressive Enhancement

```
Mobile Baseline:
- Core functionality
- Touch-optimized
- Fast loading

Tablet Enhancement:
- Side panels
- More content visible
- Hover states (stylus)

Desktop Enhancement:
- Full navigation
- Multi-column layouts
- Keyboard shortcuts
```

---

## Common Mistakes

1. **Shrinking desktop** - Scaling down instead of redesigning
2. **Tiny targets** - Links and buttons too small
3. **Hidden navigation** - Over-relying on hamburger
4. **Ignoring thumb zone** - Primary actions out of reach
5. **Slow performance** - Not optimizing for mobile networks
6. **Missing input types** - Not using appropriate keyboards

---

## Mobile Gestures

### Standard Gestures

| Gesture | Action |
|---------|--------|
| **Tap** | Select, activate |
| **Long press** | Context menu, selection |
| **Swipe horizontal** | Navigate, reveal actions |
| **Swipe vertical** | Scroll |
| **Pinch** | Zoom |
| **Pull down** | Refresh |

### Gesture Guidelines

```
Rules:
1. Always provide visible alternative
2. Use standard gestures (don't invent)
3. Provide feedback
4. Prevent accidental activation
5. Make discoverable
```

---

## Accessibility on Mobile

### Key Considerations

| Area | Requirements |
|------|--------------|
| **Touch targets** | 44x44pt minimum |
| **Screen reader** | VoiceOver/TalkBack support |
| **Text size** | Respect system settings |
| **Color** | Sufficient contrast |
| **Motion** | Respect reduced motion |

### Testing Tools

| Platform | Tool |
|----------|------|
| iOS | Accessibility Inspector, VoiceOver |
| Android | Accessibility Scanner, TalkBack |
| Both | Manual testing with screen reader |

---

## Performance Targets

### Key Metrics

| Metric | Target | Why |
|--------|--------|-----|
| **LCP** | <2.5s | Largest content visible |
| **FID** | <100ms | First input delay |
| **CLS** | <0.1 | Layout stability |
| **TTI** | <5s | Time to interactive |

### Optimization Techniques

```
Images:
- Use WebP format
- Responsive sizes (srcset)
- Lazy loading
- Proper dimensions

JavaScript:
- Code splitting
- Defer non-critical
- Minimize bundles

Network:
- Service worker caching
- CDN usage
- Compression
```

---

## Testing on Mobile

### Methods

| Method | What it catches |
|--------|-----------------|
| **Device lab** | Real device behavior |
| **Emulators** | Layout issues |
| **Remote testing** | User behavior |
| **Field testing** | Real context |

### Essential Devices

```
Recommended device coverage:
- iPhone (recent + older)
- Android (various sizes)
- Budget Android
- Tablet (iPad, Android)
```

---

## Checklist

Design phase:
- [ ] Mobile goals defined
- [ ] Core features prioritized
- [ ] Mobile-first wireframes
- [ ] Touch targets sized properly
- [ ] Thumb zone considered
- [ ] Navigation pattern chosen

Development phase:
- [ ] Responsive breakpoints
- [ ] Touch targets implemented
- [ ] Performance optimized
- [ ] Input types set
- [ ] Gestures implemented

Testing phase:
- [ ] Tested on real devices
- [ ] Performance measured
- [ ] Accessibility checked
- [ ] Different network speeds
- [ ] Different orientations

---

## References

- Mobile First by Luke Wroblewski
- Touch Design for Mobile Interfaces by Steven Hoober
- Material Design: Mobile Guidelines
- iOS Human Interface Guidelines