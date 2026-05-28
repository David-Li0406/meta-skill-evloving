# Animation Design Principles

Curated guidance from leading animation designers and resources.

## Core Philosophy

### From Emil Kowalski (emilkowal.ski)

**Developing Taste**

- Taste is pattern recognition from exposure to quality work
- Study best-in-class animations (Linear, Stripe, Apple)
- Ask "why does this feel right?" not just "how was this made?"
- Build your animation library mentally by analyzing great work

**7 Practical Tips**

1. **Start subtle** - Reduce animation intensity by 30-50% from your first instinct
2. **Respect the user** - Don't animate purely for delight; serve purpose
3. **Use springs** - More natural than easing curves
4. **Stagger with restraint** - Small delays (50-100ms) between elements
5. **Animate spatial properties** - Position, scale, opacity (GPU-accelerated)
6. **Test on slower devices** - What works on M-series may struggle elsewhere
7. **Observe the transition** - Watch the middle frames, not just start/end

**When NOT to Animate**

- User has seen it before (first-time only for onboarding)
- During user-controlled actions (scrolling, dragging)
- High-frequency events (typing, selecting)
- Performance-critical paths (data loading, computation)

**The Magic of Clip Path**

- Creates impossibly smooth morphs between shapes
- Use for revealing/hiding content with shape transitions
- Combine with transforms for compound effects
- Particularly effective for:
  - Expanding buttons into panels
  - Shape-shifting modals
  - Progressive disclosure

### From Devouring Details (devouringdetails.com)

**Inferring Intent**

- Predict what the user wants to do next
- Pre-animate likely actions (hover states, drawer prep)
- Reduce perceived latency through optimistic animations
- Example: Button scales slightly before click completes

**Interaction Metaphors**

- Digital physics should feel familiar but improved
- Rubber-banding at boundaries (iOS scroll)
- Momentum and friction for throws
- Snap points that "pull" elements into place

**Ergonomic Interactions**

- Larger hit targets during motion
- Forgive imprecise gestures
- Maintain interaction during animations
- Don't lock UI while transitioning

**Simulating Physics**

- Springs > easing curves (they respond to interruption)
- Mass affects perception (heavy objects move slower)
- Friction creates believability
- Example: Modal slides in with spring, not linear

**Motion Choreography**

- Lead with the most important element
- Support elements follow (stagger)
- Exit in reverse order of entrance
- Maintain spatial relationships during transitions

**Contained Gestures**

- Start and end in the same UI region
- Avoid cross-screen gestures for common actions
- Keep related actions spatially grouped
- Example: Swipe within card, not across viewport

### From Apple (WWDC - Designing Fluid Interfaces)

**Springs Are Superior**

- Respond naturally to interruptions
- No fixed duration - adapt to context
- Parameters: stiffness (speed), damping (bounciness), mass (weight)
- Always feel responsive regardless when user acts

**Interruptible Animations**

- User input should always take priority
- New animations inherit velocity from interrupted ones
- Creates continuous, fluid feel
- Never lock interactions waiting for animations

**Spatial Consistency**

- Elements should move along believable paths
- Maintain orientation during transforms
- Preserve spatial relationships
- Use arc motion for natural movement

**Design for Fingers**

- Touch targets: minimum 44x44pt
- Increase during motion (forgiveness)
- Provide instant feedback (<100ms)
- Physical metaphors (buttons depress, switches slide)

### From Benjamin De Cock (Stripe)

**Motion & Playfulness**

- Animation is communication, not decoration
- Guide attention through choreography
- Create hierarchy through timing
- Delight is a byproduct of clarity

**Stripe's Animation Principles**

1. **Purposeful** - Every animation serves a function
2. **Fast** - Never slow down the user
3. **Subtle** - Background, not foreground
4. **Consistent** - Repeated patterns build trust
5. **Accessible** - Respect prefers-reduced-motion

**Improving Payment Experience**

- Use animation to reduce anxiety during wait states
- Show progress, not just spinners
- Confirm success with celebration (but quick)
- Handle errors gracefully with helpful motion

### From Motion.dev Performance Guide

**Performance Tier List**

**S-Tier (60fps+):**

- `transform` (translate, scale, rotate)
- `opacity`
- Hardware-accelerated properties

**A-Tier (Good but watch):**

- `filter` (blur, brightness)
- `backdrop-filter`
- Requires compositing layer

**B-Tier (Use sparingly):**

- `box-shadow`
- `border-radius` (when animating)
- `background` gradients

**C-Tier (Avoid):**

- `width`, `height` (use scale instead)
- `top`, `left` (use translate instead)
- `margin`, `padding`

**F-Tier (Never):**

- Layout-triggering properties during scroll
- Synchronous re-layouts
- Animating large images without GPU

### From Maxime Heckel (Physics of Springs)

**Spring Parameters Explained**

**Stiffness** (tension):

- Low (< 100): Loose, floaty feel
- Medium (100-200): Balanced, natural
- High (> 200): Snappy, tight response
- Use higher for micro-interactions

**Damping** (friction):

- Low (< 10): Oscillates, bouncy
- Medium (10-20): Slight overshoot
- High (> 20): No bounce, smooth stop
- iOS default: ~1.0 (bouncy), Web default: ~10 (balanced)

**Mass** (weight):

- Heavier = slower to start/stop
- Lighter = quick, snappy
- Use to convey information hierarchy
- Large modals feel "heavier" than tooltips

**Velocity**:

- Initial push affects animation
- Inherit from interrupted animations
- Creates continuity in gesture sequences

## Timing Guidelines

### Durations by Context

**Micro-interactions** (150-200ms):

- Button hover states
- Checkbox toggles
- Tooltip appearance
- Icon changes

**Component transitions** (200-300ms):

- Dropdown menus
- Tab switching
- Accordion expand/collapse
- Toast notifications

**Panel/Modal transitions** (300-400ms):

- Drawer open/close
- Modal appear/dismiss
- Sheet slide-ups
- Navigation transitions

**Page transitions** (400-500ms):

- Route changes
- Major view shifts
- Maximum for user-blocking animations

### Easing Reference

**Ease-out** (default choice):

- Starts fast, ends slow
- Feels responsive (immediate feedback)
- Use for: entrances, reveals, expansions

**Ease-in**:

- Starts slow, ends fast
- Feels like acceleration
- Use for: exits, dismissals

**Ease-in-out**:

- Slow at both ends
- Feels polished but less responsive
- Use for: continuous loops, position swaps

**Linear**:

- Constant speed
- Feels mechanical
- Use for: loading spinners, progress bars

**Custom cubic-bezier**:

- Stripe: `cubic-bezier(0.4, 0.0, 0.2, 1)`
- iOS: `cubic-bezier(0.25, 0.1, 0.25, 1)`
- Linear: `cubic-bezier(0.36, 0, 0.66, -0.56)` (elastic)

## When to Use Springs vs Duration

### Use Springs For:

- Interactive elements (buttons, switches)
- Gesture-driven animations (drag, swipe)
- Layout shifts (reordering, resize)
- Anything that can be interrupted
- Natural-feeling motion

### Use Duration For:

- Loading indicators (predictable)
- Intentional choreography (sequence)
- Looping animations (spinners)
- When you need exact timing
- Cross-component coordination

### Hybrid Approach:

```jsx
// Spring for feel, duration for cap
<motion.div
  animate={{ x: 100 }}
  transition={{
    type: 'spring',
    stiffness: 300,
    damping: 30,
    restDelta: 0.001,
    restSpeed: 0.001,
  }}
/>
```

## Animation Patterns by Use Case

### Loading States

**Skeleton screens** (preferred):

- Show layout immediately
- Pulse/shimmer animation
- Reduces perceived load time

**Spinners** (fallback):

- Indeterminate: spinning circle
- Determinate: progress bar
- Add micro-delays to avoid flashing

### Form Interactions

**Validation feedback**:

- Shake on error (quick horizontal oscillation)
- Checkmark on success (scale + fade in)
- Highlight invalid field (subtle glow)

**Field focus**:

- Border color transition
- Label float animation
- Input scale (barely noticeable)

### Notifications

**Toast/Alert**:

- Enter from edge (spring, ~300ms)
- Auto-dismiss or manual close
- Exit same direction as entrance
- Stack with stagger (~50ms offset)

**Badge updates**:

- Scale bounce on count change
- Color pulse for critical
- Shake for urgent attention

### Navigation

**Page transitions**:

- Fade + slight vertical offset
- Respect user motion preference
- Fast (200-300ms max)
- Consider direction (forward/back)

**Tab switching**:

- Underline slide between tabs
- Content crossfade
- No vertical movement (reduces confusion)

### Modals & Overlays

**Modal entrance**:

- Backdrop fade in (150ms)
- Content scale + fade (200ms, slight delay)
- Spring for natural feel

**Drawer**:

- Slide from edge
- Backdrop simultaneously
- Spring that settles into place

### Data Visualization

**Chart animations**:

- Stagger data points (~20ms each)
- Ease-out for bars/columns
- Draw paths for line charts
- Spring for interactive elements

## Accessibility Principles

### Respect User Preferences

```jsx
// Motion handles this automatically
const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

// Springs become instant when reduced motion is preferred
```

### Additional Considerations

- Provide skip buttons for long animations
- Never auto-play looping animations indefinitely
- Avoid seizure-inducing flashing (< 3 flashes/second)
- Ensure animations don't obscure critical content
- Allow pausing of non-essential motion

### Focus Management

- Maintain focus during transitions
- Announce state changes to screen readers
- Don't trap focus in animating elements
- Ensure keyboard navigation works during motion

## The "Feel Right" Checklist

Before shipping an animation, ask:

1. **Does it have a purpose?** (Not just delight)
2. **Is it fast enough?** (< 300ms for most interactions)
3. **Can it be interrupted?** (Springs help here)
4. **Does it guide attention?** (Choreography matters)
5. **Is it too much?** (Reduce by 30% and try again)
6. **Does it respect reduced motion?** (Automatic with Motion)
7. **Is it consistent?** (Same component = same animation)
8. **Does it work on slower devices?** (Test on mid-range hardware)

## Anti-Patterns to Avoid

❌ **Animating every single thing**

- Creates visual chaos
- Exhausts users
- Reduces impact of important animations

❌ **Long durations** (> 500ms)

- Feels sluggish
- Users will try to interrupt
- Creates frustration

❌ **Easing in for entrances**

- Delays visual feedback
- Feels unresponsive
- Use ease-out instead

❌ **Animating during scroll**

- Competes with user control
- Performance issues
- Motion sickness risk

❌ **Over-bouncing springs**

- Looks amateur
- Distracting
- Use damping > 15 for UI

❌ **Inconsistent timing**

- Same element, different speeds
- Breaks mental model
- Feels buggy

❌ **Ignoring physics**

- Teleporting elements
- Instant direction changes
- Breaking spatial consistency

❌ **Animation for animation's sake**

- No functional purpose
- Slows down user
- Pure decoration

## Resources for Deeper Study

- **animations.dev/learn** - Structured lessons on theory and implementation
- **animations.dev/vault** - Curated articles, videos, and examples
- See `resources.md` for complete catalog
