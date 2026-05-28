# Motion Design

## Patterns


---
  #### **Name**
Purposeful Animation Timing
  #### **Description**
Use timing that matches the nature and importance of the interaction
  #### **When**
Designing any animation timing
  #### **Example**
    Timing scale (duration by purpose):
    - Micro feedback: 50-100ms (button press, toggle)
    - Small transitions: 150-200ms (hover states, small movements)
    - Medium transitions: 200-300ms (modals, dropdowns, page sections)
    - Large transitions: 300-500ms (page transitions, complex reveals)
    - Complex sequences: 500-1000ms (onboarding, celebrations)
    
    Rules:
    - Faster for reversible actions (hover)
    - Slower for important state changes (navigation)
    - Never over 500ms for functional UI
    - Match duration to distance traveled
    

---
  #### **Name**
Natural Easing Curves
  #### **Description**
Use easing that mimics real-world physics for natural feel
  #### **When**
Choosing easing functions for animations
  #### **Example**
    Standard easing (CSS):
    - ease-out: cubic-bezier(0, 0, 0.2, 1)    → Entrances (fast start, gentle stop)
    - ease-in: cubic-bezier(0.4, 0, 1, 1)    → Exits (gentle start, fast end)
    - ease-in-out: cubic-bezier(0.4, 0, 0.2, 1) → Position changes
    - linear: for opacity, color (no spatial movement)
    
    Spring physics (React Spring / Framer Motion):
    - tension: 170, friction: 26  → Snappy (buttons)
    - tension: 120, friction: 14  → Bouncy (playful UI)
    - tension: 210, friction: 20  → Stiff (professional UI)
    
    Never use linear for spatial movement - objects don't move that way.
    

---
  #### **Name**
Staggered Choreography
  #### **Description**
Reveal multiple elements with staggered timing to create hierarchy and flow
  #### **When**
Loading lists, grids, or multiple UI elements
  #### **Example**
    Stagger pattern:
    - First item: 0ms delay
    - Second item: 50ms delay
    - Third item: 100ms delay
    - Max total duration: 500ms
    
    CSS implementation:
    .item { animation: fadeIn 200ms ease-out both; }
    .item:nth-child(1) { animation-delay: 0ms; }
    .item:nth-child(2) { animation-delay: 50ms; }
    .item:nth-child(3) { animation-delay: 100ms; }
    
    Rules:
    - Stagger 30-80ms between items
    - Cap total stagger at 500ms (even if more items)
    - Direction matters: top-to-bottom, left-to-right, or from focus point
    

---
  #### **Name**
Spatial Continuity
  #### **Description**
Animate elements along paths that maintain spatial relationships
  #### **When**
Navigating between views or expanding/collapsing elements
  #### **Example**
    Spatial rules:
    - Elements should animate FROM their origin
    - Modal scales from the button that triggered it
    - Dropdown slides from trigger, not from nowhere
    - Details page shares element with list card (shared element transition)
    
    Example - Card to Detail:
    1. Card scales up in place
    2. Content fades and repositions
    3. New content fades in
    Users always know where they came from and how to get back.
    

---
  #### **Name**
Loading State Design
  #### **Description**
Show progress and maintain context during async operations
  #### **When**
Any operation that takes > 100ms
  #### **Example**
    Loading progression:
    < 100ms:   Show nothing (feels instant)
    100-300ms: Spinner or pulse (brief wait)
    > 300ms:   Skeleton screens (long wait)
    > 3s:      Progress bar + message (very long)
    
    Skeleton implementation:
    - Match exact layout of content
    - Subtle pulse animation (1.5s ease-in-out infinite)
    - Gray placeholders (#E5E7EB)
    - Never show spinner for content - use skeletons
    
    Button loading:
    - Disable immediately
    - Show spinner in button (not replacing text)
    - Keep button same width (prevent layout shift)
    

---
  #### **Name**
Feedback Animation Patterns
  #### **Description**
Provide immediate visual feedback for user interactions
  #### **When**
Designing interactive element responses
  #### **Example**
    Interaction feedback:
    - Button press: scale(0.97) for 100ms
    - Success: checkmark animate in, green pulse
    - Error: shake animation (3 cycles, 300ms total)
    - Toggle: thumb slides 150ms ease-out
    - Checkbox: checkmark draws in 200ms
    
    Haptic principles (visual equivalent):
    - Immediate (< 50ms) acknowledgment
    - Clear state change
    - Return to resting state
    

---
  #### **Name**
Reduced Motion Support
  #### **Description**
Provide alternative experience for users who prefer reduced motion
  #### **When**
Every single animation you create
  #### **Example**
    Required CSS:
    @media (prefers-reduced-motion: reduce) {
      *, *::before, *::after {
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
        scroll-behavior: auto !important;
      }
    }
    
    Better approach - semantic motion:
    @media (prefers-reduced-motion: reduce) {
      .animate-slide { animation: none; opacity: 1; }
      .animate-fade { animation: fade 150ms ease-out; }
      /* Keep fades, remove movement */
    }
    
    Rules:
    - Fades are generally safe
    - Remove parallax completely
    - Reduce spring bounce
    - Eliminate auto-playing animations
    

---
  #### **Name**
GPU-Accelerated Properties
  #### **Description**
Use transform and opacity for smooth 60fps animations
  #### **When**
Implementing any animation for production
  #### **Example**
    GPU-accelerated (smooth):
    - transform: translate, scale, rotate
    - opacity
    - filter (with care)
    
    Triggers layout (avoid animating):
    - width, height
    - top, left, right, bottom
    - margin, padding
    - font-size
    
    Example optimization:
    Bad:  left: 0 → left: 100px (triggers layout)
    Good: transform: translateX(0) → translateX(100px) (GPU)
    
    Performance hint:
    .animated-element {
      will-change: transform, opacity;
      transform: translateZ(0); /* Force GPU layer */
    }
    

---
  #### **Name**
Scroll-Triggered Animations
  #### **Description**
Reveal content as users scroll using Intersection Observer
  #### **When**
Building landing pages or long-form content
  #### **Example**
    Intersection Observer pattern:
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            entry.target.classList.add('animate-in');
          }
        });
      },
      { threshold: 0.2, rootMargin: '0px 0px -50px 0px' }
    );
    
    CSS:
    .scroll-reveal {
      opacity: 0;
      transform: translateY(20px);
      transition: opacity 400ms ease-out, transform 400ms ease-out;
    }
    .scroll-reveal.animate-in {
      opacity: 1;
      transform: translateY(0);
    }
    
    Rules:
    - Trigger when 20% visible (threshold: 0.2)
    - Small movement (20-30px max)
    - Don't animate out on scroll up (annoying)
    - Disable for prefers-reduced-motion
    

## Anti-Patterns


---
  #### **Name**
Animation for Decoration
  #### **Description**
Adding motion because it "looks cool" without serving a purpose
  #### **Why**
Distracts users, slows interactions, wastes battery, annoys on repeat views
  #### **Instead**
    Every animation must answer:
    1. What does this communicate? (origin, change, confirmation)
    2. What would be lost without it? (context, feedback, clarity)
    
    If you can't answer clearly, don't animate.
    
    Example:
    Bad: Logo bouncing on load (decoration)
    Good: Modal scaling from trigger button (shows origin)
    

---
  #### **Name**
Sluggish Transitions
  #### **Description**
Animations over 500ms for functional UI elements
  #### **Why**
Users wait. Repeated actions become painful. Interface feels slow.
  #### **Instead**
    Timing rules:
    - Dropdowns, modals: 200-300ms max
    - Button feedback: 100-150ms
    - Page transitions: 300-400ms
    - Hover states: 150ms
    
    Test: Use the interface 100 times in a row.
    If animation feels slow on repetition, it's too slow.
    

---
  #### **Name**
Linear Easing for Movement
  #### **Description**
Using linear timing for spatial animations
  #### **Why**
Objects don't move linearly in real world. Feels robotic and unnatural.
  #### **Instead**
    Bad:  transition: transform 300ms linear;
    Good: transition: transform 300ms ease-out;
    
    Linear is ONLY for:
    - Continuous rotations (spinners)
    - Color/opacity changes
    - Progress bars (sometimes)
    
    Never for:
    - Position changes
    - Scale animations
    - Entrances/exits
    

---
  #### **Name**
Ignoring prefers-reduced-motion
  #### **Description**
Not providing reduced motion alternatives
  #### **Why**
Causes motion sickness, violates WCAG 2.3.3, excludes users with vestibular disorders
  #### **Instead**
    This is REQUIRED, not optional:
    @media (prefers-reduced-motion: reduce) {
      /* Provide alternative or remove animation */
    }
    
    About 35% of adults over 40 experience vestibular disorders.
    Parallax, bouncing, and continuous motion trigger symptoms.
    

---
  #### **Name**
Layout-Triggering Animations
  #### **Description**
Animating properties that cause layout recalculation
  #### **Why**
Causes jank, drops frames, ruins user experience on slower devices
  #### **Instead**
    Never animate:
    - width/height → use scale
    - top/left → use translate
    - margin/padding → use translate
    
    Performance hierarchy:
    1. transform, opacity (GPU, always smooth)
    2. filter (GPU, but expensive)
    3. background-color (paint only)
    4. width, height (layout, avoid)
    

---
  #### **Name**
Bounce Abuse
  #### **Description**
Using bouncy spring animations everywhere
  #### **Why**
Playful becomes annoying. Professional contexts need restraint.
  #### **Instead**
    Bounce appropriately:
    Yes: Success celebrations, playful apps, gamification
    No: Enterprise dashboards, data tables, form validation
    
    If using bounce:
    - Single subtle bounce, not multiple
    - Save for important moments
    - Context matters: banking app vs. game
    

---
  #### **Name**
Blocking Interactions During Animation
  #### **Description**
Preventing user interaction while animations complete
  #### **Why**
Makes UI feel unresponsive. Users click during animation and nothing happens.
  #### **Instead**
    Animation should never block:
    - Cancel previous animation on new interaction
    - Allow click-through on fading elements
    - Queue rapid interactions
    
    Example:
    If user clicks button during modal close animation,
    interrupt and respond to the click immediately.
    

---
  #### **Name**
Inconsistent Motion Language
  #### **Description**
Different animations for similar actions across the product
  #### **Why**
Creates cognitive load. Users can't predict how UI will behave.
  #### **Instead**
    Create motion tokens:
    --duration-instant: 100ms
    --duration-fast: 200ms
    --duration-normal: 300ms
    --easing-standard: cubic-bezier(0.4, 0, 0.2, 1)
    --easing-enter: cubic-bezier(0, 0, 0.2, 1)
    --easing-exit: cubic-bezier(0.4, 0, 1, 1)
    
    Document motion patterns. Same action = same animation everywhere.
    