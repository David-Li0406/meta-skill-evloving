# Motion Design - Sharp Edges

## Reduced Motion Ignored

### **Id**
reduced-motion-ignored
### **Summary**
Not implementing prefers-reduced-motion media query
### **Severity**
critical
### **Situation**
  Animations play regardless of user preferences. No @media query for
  prefers-reduced-motion anywhere in the codebase. Users with vestibular
  disorders experience motion sickness.
  
### **Why**
  WCAG 2.3.3 requires respecting motion preferences. 35% of adults over 40
  have vestibular disorders. Motion can trigger nausea, vertigo, and migraines.
  This isn't a nice-to-have - it's accessibility compliance.
  
### **Solution**
  # Global reduced motion support (add to base CSS)
  @media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
      animation-duration: 0.01ms !important;
      animation-iteration-count: 1 !important;
      transition-duration: 0.01ms !important;
      scroll-behavior: auto !important;
    }
  }
  
  # Better - semantic reduced motion
  @media (prefers-reduced-motion: reduce) {
    .parallax { transform: none !important; }
    .animate-bounce { animation: none; }
    .animate-slide { opacity: 1; transform: none; }
  }
  
  # React hook for JavaScript animations
  const prefersReducedMotion =
    window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  
### **Symptoms**
  - User complaints about motion sickness
  - Accessibility audit failures
  - Users avoiding your site
  - Vestibular disorder reports
### **Detection Pattern**
animation:|transition:(?!.*prefers-reduced-motion)

## Layout Property Animation

### **Id**
layout-property-animation
### **Summary**
Animating width, height, top, left instead of transform
### **Severity**
critical
### **Situation**
  Animations use width, height, margin, top, left, or other layout-triggering
  properties. Animation drops frames, feels janky, especially on mobile or
  slower machines.
  
### **Why**
  Layout-triggering properties force browser to recalculate layout for entire
  page on every frame. Transform and opacity are GPU-accelerated - they don't
  trigger layout. This is the difference between 60fps and 15fps.
  
### **Solution**
  # BAD - triggers layout
  .slide-in {
    transition: left 300ms;
    left: -100%;
  }
  .slide-in.active { left: 0; }
  
  # GOOD - GPU accelerated
  .slide-in {
    transition: transform 300ms;
    transform: translateX(-100%);
  }
  .slide-in.active { transform: translateX(0); }
  
  # Property mapping:
  left/right/top/bottom → translateX/translateY
  width/height → scale
  margin → translate
  
  # Force GPU layer
  .animated { will-change: transform, opacity; }
  
### **Symptoms**
  - Choppy animations
  - Frame drops on mobile
  - Battery drain during animation
  - UI feels sluggish
### **Detection Pattern**
transition:\s*[^;]*(width|height|left|right|top|bottom|margin|padding).*\d+m?s

## Animation Blocking Interaction

### **Id**
animation-blocking-interaction
### **Summary**
UI unresponsive during animation completion
### **Severity**
high
### **Situation**
  User clicks during animation but nothing happens until animation finishes.
  Modal is closing and user clicks backdrop - click is ignored. Dropdown is
  opening and user clicks away - stuck waiting.
  
### **Why**
  Animation state locks out interaction. Users expect immediate response.
  Forcing users to wait for animation completion feels broken, not polished.
  
### **Solution**
  # Cancel animation on new interaction
  element.addEventListener('click', () => {
    // Cancel any running animation
    element.getAnimations().forEach(anim => anim.cancel());
    // Process click immediately
    handleClick();
  });
  
  # CSS - allow pointer events during exit
  .modal.closing {
    pointer-events: none;  /* Don't block what's underneath */
  }
  
  # Framer Motion - interrupt animations
  <motion.div
    animate={{ opacity: isOpen ? 1 : 0 }}
    transition={{ duration: 0.3 }}
    onAnimationComplete={() => {
      if (!isOpen) cleanup();
    }}
  />
  
### **Symptoms**
  - Clicks don't register during animation
  - Users clicking multiple times
  - "Is this broken?" feeling
  - Rage clicks on slow animations
### **Detection Pattern**
pointer-events:\s*none.*transition

## Linear Easing Movement

### **Id**
linear-easing-movement
### **Summary**
Using linear easing for spatial animations
### **Severity**
high
### **Situation**
  Position, scale, or rotation animations use linear timing. Movement feels
  robotic, mechanical, unnatural. Users can't put their finger on why it
  feels wrong.
  
### **Why**
  Real objects accelerate and decelerate. Linear motion doesn't exist in
  nature. The human eye is trained to expect easing. Linear motion triggers
  subconscious "something's off" feeling.
  
### **Solution**
  # BAD
  transition: transform 300ms linear;
  
  # GOOD - standard easing
  transition: transform 300ms ease-out;      /* entrances */
  transition: transform 300ms ease-in;       /* exits */
  transition: transform 300ms ease-in-out;   /* position changes */
  
  # Better - precise curves
  --ease-out: cubic-bezier(0, 0, 0.2, 1);
  --ease-in: cubic-bezier(0.4, 0, 1, 1);
  --ease-standard: cubic-bezier(0.4, 0, 0.2, 1);
  
  # Linear is ONLY for:
  # - Continuous spinners
  # - Color transitions
  # - Opacity fades (sometimes)
  # - Progress bars
  
### **Symptoms**
  - Animations feel "off"
  - Robotic feeling UI
  - User can't explain discomfort
  - Unpolished appearance
### **Detection Pattern**
transition:\s*[^;]*(transform|translate|scale|rotate)[^;]*linear

## Duration Extremes

### **Id**
duration-extremes
### **Summary**
Animations too fast (< 100ms) or too slow (> 500ms)
### **Severity**
high
### **Situation**
  Micro-interactions are imperceptible (< 100ms) or functional UI feels
  sluggish (> 500ms for modals, dropdowns, etc).
  
### **Why**
  Under 100ms is subliminal - users don't perceive the change, defeating
  the purpose. Over 500ms feels like waiting. Repeated use amplifies
  annoyance exponentially. What feels fine once feels painful 100 times.
  
### **Solution**
  # Timing scale:
  50-100ms:   Instant feedback (button press, toggle)
  150-200ms:  Quick transitions (hover, small movements)
  200-300ms:  Standard transitions (modal, dropdown)
  300-400ms:  Large transitions (page, drawer)
  400-500ms:  Complex reveals (only for emphasis)
  
  # Never:
  < 100ms for important state changes (invisible)
  > 500ms for anything functional (frustrating)
  > 300ms for hover states (feels unresponsive)
  
  # Test: Use the feature 50 times in a row
  # If animation becomes irritating, it's too slow
  
### **Symptoms**
  - Users don't notice animation (too fast)
  - Users waiting for UI (too slow)
  - Frustration on repeated use
  - "Laggy" user feedback
### **Detection Pattern**
transition-duration:\s*[1-9][0-9]{3,}ms|animation-duration:\s*[1-9]s

## Z Index Animation Clash

### **Id**
z-index-animation-clash
### **Summary**
Z-index conflicts during animation causing visual glitches
### **Severity**
high
### **Situation**
  Animated elements disappear behind other content. Modal animates but
  content shows through. Dropdown clips behind adjacent elements.
  Stacking contexts create unexpected layering.
  
### **Why**
  Transforms create new stacking contexts. Z-index works within stacking
  context, not globally. Animated elements may not be in expected layer.
  
### **Solution**
  # Understand stacking contexts
  # These create new stacking context:
  - position: fixed/sticky
  - transform: anything
  - opacity < 1
  - filter: anything
  - will-change
  - isolation: isolate
  
  # Solution: Explicit stacking
  :root {
    --z-dropdown: 100;
    --z-sticky: 200;
    --z-modal-backdrop: 400;
    --z-modal: 500;
    --z-popover: 600;
    --z-tooltip: 700;
  }
  
  # Isolation for animated containers
  .animated-container {
    isolation: isolate;
    z-index: var(--z-modal);
  }
  
### **Symptoms**
  - Elements disappear during animation
  - Unexpected overlap
  - Z-index doesn't work
  - Modal content shows through backdrop
### **Detection Pattern**


## Parallax Performance Death

### **Id**
parallax-performance-death
### **Summary**
Heavy parallax effects causing scroll jank
### **Severity**
high
### **Situation**
  Scroll-based parallax animations cause stuttering, dropped frames, and
  high CPU usage. Mobile devices struggle. Users report laggy scrolling.
  
### **Why**
  Parallax often uses scroll events + transforms on multiple elements.
  JavaScript scroll handlers fire hundreds of times per second. Each
  recalculation triggers layout or paint. Mobile GPUs can't keep up.
  
### **Solution**
  # Bad - scroll event listener
  window.addEventListener('scroll', () => {
    element.style.transform = `translateY(${scrollY * 0.5}px)`;
  });
  
  # Better - CSS only parallax
  .parallax-container {
    perspective: 1px;
    overflow-x: hidden;
    overflow-y: auto;
  }
  .parallax-layer {
    transform: translateZ(-1px) scale(2);
  }
  
  # Best - Intersection Observer for simple reveals
  # Avoid parallax entirely for most use cases
  
  # CRITICAL: Disable for reduced motion
  @media (prefers-reduced-motion: reduce) {
    .parallax-layer { transform: none; }
  }
  
### **Symptoms**
  - Stuttering scroll
  - High CPU during scroll
  - Mobile performance issues
  - Battery drain
### **Detection Pattern**
addEventListener.*scroll.*transform

## Animation Memory Leak

### **Id**
animation-memory-leak
### **Summary**
Animations continue running when component unmounts
### **Severity**
high
### **Situation**
  React/Vue component unmounts but animation continues. requestAnimationFrame
  keeps firing. GSAP timelines keep running. Lottie animations play to
  destroyed DOM. Memory usage climbs over time.
  
### **Why**
  JavaScript animations don't automatically stop when DOM elements are
  removed. Animation frames keep firing, callbacks keep executing.
  Memory leaks accumulate, eventually crashing tab.
  
### **Solution**
  # React - cleanup animations
  useEffect(() => {
    const animation = element.animate(...);
    return () => animation.cancel();  // Cleanup!
  }, []);
  
  # GSAP cleanup
  useEffect(() => {
    const tl = gsap.timeline();
    tl.to(elementRef.current, { x: 100 });
    return () => tl.kill();  // Kill timeline on unmount
  }, []);
  
  # Framer Motion - automatic cleanup via AnimatePresence
  <AnimatePresence>
    {isVisible && <motion.div exit={{ opacity: 0 }} />}
  </AnimatePresence>
  
  # requestAnimationFrame cleanup
  useEffect(() => {
    let rafId;
    const animate = () => {
      // animation logic
      rafId = requestAnimationFrame(animate);
    };
    rafId = requestAnimationFrame(animate);
    return () => cancelAnimationFrame(rafId);
  }, []);
  
### **Symptoms**
  - Memory usage growing
  - Console warnings about unmounted updates
  - Tab becoming slow over time
  - Can't perform state update on unmounted component
### **Detection Pattern**
requestAnimationFrame(?![\\s\\S]*cancelAnimationFrame)

## Spring Animation Overshoot

### **Id**
spring-animation-overshoot
### **Summary**
Spring animations that overshoot and overlap content
### **Severity**
medium
### **Situation**
  Spring/bounce animations overshoot bounds, overlapping adjacent content
  or extending beyond viewport. Modal bounces past its final position.
  Elements briefly cover other interactive areas.
  
### **Why**
  Spring physics includes overshoot by design. Without constraints, elements
  can temporarily occupy unintended space, causing visual glitches and
  accessibility issues (covered content becomes inaccessible).
  
### **Solution**
  # Framer Motion - clamp spring
  <motion.div
    animate={{ y: 0 }}
    transition={{
      type: "spring",
      stiffness: 300,
      damping: 30,
      restDelta: 0.001
    }}
  />
  
  # High damping = less overshoot
  # damping ratio 1.0 = critical damping (no overshoot)
  
  # CSS containment
  .modal-container {
    overflow: hidden;  /* Contain overshoot */
  }
  
  # React Spring - clamp option
  useSpring({
    y: 0,
    config: { clamp: true }  /* No overshoot */
  })
  
### **Symptoms**
  - Elements briefly overlap others
  - Flash of content outside bounds
  - Scrollbars appearing briefly
  - Visual jank at animation end
### **Detection Pattern**


## No Will Change Cleanup

### **Id**
no-will-change-cleanup
### **Summary**
will-change applied permanently instead of dynamically
### **Severity**
medium
### **Situation**
  will-change: transform applied in base CSS, never removed. Browser keeps
  GPU layers allocated permanently. Memory usage high. Compositing costs
  increase across entire page.
  
### **Why**
  will-change tells browser to prepare for animation. It allocates GPU
  memory and creates compositor layers. Keeping it always-on wastes
  resources and can actually hurt performance.
  
### **Solution**
  # BAD - permanent will-change
  .card {
    will-change: transform;  /* Always on = memory waste */
  }
  
  # GOOD - dynamic will-change
  .card:hover {
    will-change: transform;  /* Only when needed */
  }
  .card:not(:hover) {
    will-change: auto;  /* Release resources */
  }
  
  # Best - JavaScript controlled
  element.addEventListener('mouseenter', () => {
    element.style.willChange = 'transform';
  });
  element.addEventListener('animationend', () => {
    element.style.willChange = 'auto';
  });
  
  # Only use will-change for:
  # - Complex animations that are about to happen
  # - Elements that animate frequently
  # Remove after animation completes
  
### **Symptoms**
  - High GPU memory usage
  - Slow performance with many elements
  - DevTools shows many compositor layers
  - Mobile battery drain
### **Detection Pattern**
will-change:\s*(transform|opacity|all)(?![^}]*:hover)

## Transform Origin Forgotten

### **Id**
transform-origin-forgotten
### **Summary**
Scale/rotate animations with wrong transform-origin
### **Severity**
medium
### **Situation**
  Element scales from wrong point (center instead of corner). Rotation
  pivots unexpectedly. Animation looks wrong but hard to diagnose.
  
### **Why**
  Default transform-origin is center. Scaling from center ≠ scaling from
  button position. Rotation from center ≠ hinge rotation. Origin must
  match the visual metaphor.
  
### **Solution**
  # Default behavior
  transform-origin: center center;  /* Default */
  
  # Scale from top-left (dropdown from button)
  .dropdown {
    transform-origin: top left;
    transform: scale(0);
  }
  .dropdown.open { transform: scale(1); }
  
  # Common origins:
  - Dropdown: top left or top center
  - Context menu: top left
  - Modal: center center
  - Toast: bottom right (if appearing there)
  - Tooltip: varies by position
  
  # Match origin to trigger element position
  const rect = trigger.getBoundingClientRect();
  dropdown.style.transformOrigin =
    `${rect.left}px ${rect.top}px`;
  
### **Symptoms**
  - Animation looks "off"
  - Element appears from wrong direction
  - Scaling feels disconnected
  - Rotation pivot unexpected
### **Detection Pattern**
scale\([^)]+\)(?![\\s\\S]{0,100}transform-origin)

## Infinite Animation Battery Drain

### **Id**
infinite-animation-battery-drain
### **Summary**
Infinite animations running on non-visible elements
### **Severity**
medium
### **Situation**
  Loading spinner keeps animating in hidden tab. Pulsing elements animate
  while scrolled out of view. Continuous animations run in minimized windows.
  
### **Why**
  Animations consume CPU/GPU even when not visible. Battery drain on mobile.
  Performance impact on other tabs/apps. Waste of resources.
  
### **Solution**
  # Intersection Observer - pause when not visible
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.style.animationPlayState = 'running';
      } else {
        entry.target.style.animationPlayState = 'paused';
      }
    });
  });
  observer.observe(animatedElement);
  
  # Page Visibility API - pause in background tabs
  document.addEventListener('visibilitychange', () => {
    if (document.hidden) {
      animations.forEach(a => a.pause());
    } else {
      animations.forEach(a => a.play());
    }
  });
  
  # CSS - prefer animation-play-state
  .hidden { animation-play-state: paused; }
  
### **Symptoms**
  - Battery drain when page is "idle"
  - CPU usage in background tab
  - Slow overall browser performance
  - Hot device during "nothing happening"
### **Detection Pattern**
animation.*infinite(?![\\s\\S]*animation-play-state)