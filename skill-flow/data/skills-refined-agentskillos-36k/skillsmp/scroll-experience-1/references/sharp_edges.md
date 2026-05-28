# Scroll Experience - Sharp Edges

## Scroll Jank

### **Id**
scroll-jank
### **Summary**
Animations stutter during scroll
### **Severity**
high
### **Situation**
Scroll animations aren't smooth 60fps
### **Why**
  Animating wrong properties.
  Too many elements animating.
  Heavy JavaScript on scroll.
  No GPU acceleration.
  
### **Solution**
  ## Fixing Scroll Jank
  
  ### Only Animate These
  ```css
  /* GPU-accelerated, smooth */
  transform: translateX(), translateY(), scale(), rotate()
  opacity: 0 to 1
  
  /* Triggers layout, causes jank */
  width, height, top, left, margin, padding
  ```
  
  ### Force GPU Acceleration
  ```css
  .animated-element {
    will-change: transform;
    transform: translateZ(0); /* Force GPU layer */
  }
  ```
  
  ### Throttle Scroll Events
  ```javascript
  // Don't do this
  window.addEventListener('scroll', heavyFunction);
  
  // Do this instead
  let ticking = false;
  window.addEventListener('scroll', () => {
    if (!ticking) {
      requestAnimationFrame(() => {
        heavyFunction();
        ticking = false;
      });
      ticking = true;
    }
  });
  
  // Or use GSAP (handles this automatically)
  ```
  
  ### Debug Performance
  - Chrome DevTools → Performance tab
  - Record scroll, look for red frames
  - Check "Rendering" → Paint flashing
  - Profile on mobile device
  
### **Symptoms**
  - Choppy animations
  - Laggy scroll
  - CPU spikes during scroll
  - Mobile especially bad
### **Detection Pattern**
scroll.*jank|stutter|laggy|choppy|not smooth

## Parallax On Mobile

### **Id**
parallax-on-mobile
### **Summary**
Parallax breaks on mobile devices
### **Severity**
high
### **Situation**
Parallax effects glitch on iOS/Android
### **Why**
  Mobile browsers handle scroll differently.
  iOS momentum scrolling conflicts.
  Transform during scroll is tricky.
  Performance varies wildly.
  
### **Solution**
  ## Mobile-Safe Parallax
  
  ### Detection
  ```javascript
  const isMobile = /iPhone|iPad|iPod|Android/i.test(navigator.userAgent);
  // Or better: check viewport width
  const isMobile = window.innerWidth < 768;
  ```
  
  ### Reduce or Disable
  ```javascript
  if (isMobile) {
    // Simpler animations
    gsap.to('.element', {
      scrollTrigger: { scrub: true },
      y: -50, // Less movement than desktop
    });
  } else {
    // Full parallax
    gsap.to('.element', {
      scrollTrigger: { scrub: true },
      y: -200,
    });
  }
  ```
  
  ### iOS-Specific Fix
  ```css
  /* Helps with iOS scroll issues */
  .scroll-container {
    -webkit-overflow-scrolling: touch;
  }
  
  .parallax-layer {
    transform: translate3d(0, 0, 0);
    backface-visibility: hidden;
  }
  ```
  
  ### Alternative: CSS Only
  ```css
  /* Works better on mobile */
  @supports (animation-timeline: scroll()) {
    .parallax {
      animation: parallax linear;
      animation-timeline: scroll();
    }
  }
  ```
  
### **Symptoms**
  - Glitchy on iPhone
  - Stuttering on scroll
  - Elements jumping
  - Works on desktop, broken on mobile
### **Detection Pattern**
mobile|iOS|iPhone|Android|touch|parallax.*broken

## Accessibility Scroll

### **Id**
accessibility-scroll
### **Summary**
Scroll experience is inaccessible
### **Severity**
medium
### **Situation**
Screen readers and keyboard users can't use the site
### **Why**
  Animations hide content.
  Scroll hijacking breaks navigation.
  No reduced motion support.
  Focus management ignored.
  
### **Solution**
  ## Accessible Scroll Experiences
  
  ### Respect Reduced Motion
  ```css
  @media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
      animation-duration: 0.01ms !important;
      transition-duration: 0.01ms !important;
      scroll-behavior: auto !important;
    }
  }
  ```
  
  ```javascript
  const prefersReducedMotion = window.matchMedia(
    '(prefers-reduced-motion: reduce)'
  ).matches;
  
  if (!prefersReducedMotion) {
    initScrollAnimations();
  }
  ```
  
  ### Content Always Accessible
  - Don't hide content behind animations
  - Ensure text is readable without JS
  - Provide skip links
  - Test with screen reader
  
  ### Keyboard Navigation
  ```javascript
  // Ensure scroll sections are keyboard navigable
  document.querySelectorAll('.scroll-section').forEach(section => {
    section.setAttribute('tabindex', '0');
  });
  ```
  
### **Symptoms**
  - Failed accessibility audit
  - Can't navigate with keyboard
  - Screen reader doesn't work
  - Vestibular disorder complaints
### **Detection Pattern**
accessible|a11y|screen reader|keyboard|reduced motion

## Content Below Fold

### **Id**
content-below-fold
### **Summary**
Critical content hidden below animations
### **Severity**
medium
### **Situation**
Users have to scroll through animations to find content
### **Why**
  Prioritized experience over content.
  Long scroll to reach info.
  SEO suffering.
  Mobile users bounce.
  
### **Solution**
  ## Content-First Scroll Design
  
  ### Above-the-Fold Content
  - Key message visible immediately
  - CTA visible without scroll
  - Value proposition clear
  - Skip animation option
  
  ### Progressive Enhancement
  ```
  Level 1: Content readable without JS
  Level 2: Basic styling and layout
  Level 3: Scroll animations enhance
  ```
  
  ### SEO Considerations
  - Text in DOM, not just in canvas
  - Proper heading hierarchy
  - Content not hidden by default
  - Fast initial load
  
  ### Quick Exit Points
  - Clear navigation always visible
  - Skip to content links
  - Don't trap users in experience
  
### **Symptoms**
  - High bounce rate
  - Low time on page (paradoxically)
  - SEO ranking issues
  - User complaints about finding info
### **Detection Pattern**
can't find|where is|too much scroll|bounce