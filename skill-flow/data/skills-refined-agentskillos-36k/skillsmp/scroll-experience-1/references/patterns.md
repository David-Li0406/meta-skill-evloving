# Scroll Experience

## Patterns


---
  #### **Name**
Scroll Animation Stack
  #### **Description**
Tools and techniques for scroll animations
  #### **When To Use**
When planning scroll-driven experiences
  #### **Implementation**
    ## Scroll Animation Stack
    
    ### Library Options
    | Library | Best For | Learning Curve |
    |---------|----------|----------------|
    | GSAP ScrollTrigger | Complex animations | Medium |
    | Framer Motion | React projects | Low |
    | Locomotive Scroll | Smooth scroll + parallax | Medium |
    | Lenis | Smooth scroll only | Low |
    | CSS scroll-timeline | Simple, native | Low |
    
    ### GSAP ScrollTrigger Setup
    ```javascript
    import { gsap } from 'gsap';
    import { ScrollTrigger } from 'gsap/ScrollTrigger';
    
    gsap.registerPlugin(ScrollTrigger);
    
    // Basic scroll animation
    gsap.to('.element', {
      scrollTrigger: {
        trigger: '.element',
        start: 'top center',
        end: 'bottom center',
        scrub: true, // Links animation to scroll position
      },
      y: -100,
      opacity: 1,
    });
    ```
    
    ### Framer Motion Scroll
    ```jsx
    import { motion, useScroll, useTransform } from 'framer-motion';
    
    function ParallaxSection() {
      const { scrollYProgress } = useScroll();
      const y = useTransform(scrollYProgress, [0, 1], [0, -200]);
    
      return (
        <motion.div style={{ y }}>
          Content moves with scroll
        </motion.div>
      );
    }
    ```
    
    ### CSS Native (2024+)
    ```css
    @keyframes reveal {
      from { opacity: 0; transform: translateY(50px); }
      to { opacity: 1; transform: translateY(0); }
    }
    
    .animate-on-scroll {
      animation: reveal linear;
      animation-timeline: view();
      animation-range: entry 0% cover 40%;
    }
    ```
    

---
  #### **Name**
Parallax Storytelling
  #### **Description**
Tell stories through scroll depth
  #### **When To Use**
When creating narrative experiences
  #### **Implementation**
    ## Parallax Storytelling
    
    ### Layer Speeds
    | Layer | Speed | Effect |
    |-------|-------|--------|
    | Background | 0.2x | Far away, slow |
    | Midground | 0.5x | Middle depth |
    | Foreground | 1.0x | Normal scroll |
    | Content | 1.0x | Readable |
    | Floating elements | 1.2x | Pop forward |
    
    ### Creating Depth
    ```javascript
    // GSAP parallax layers
    gsap.to('.background', {
      scrollTrigger: {
        scrub: true
      },
      y: '-20%', // Moves slower
    });
    
    gsap.to('.foreground', {
      scrollTrigger: {
        scrub: true
      },
      y: '-50%', // Moves faster
    });
    ```
    
    ### Story Beats
    ```
    Section 1: Hook (full viewport, striking visual)
        ↓ scroll
    Section 2: Context (text + supporting visuals)
        ↓ scroll
    Section 3: Journey (parallax storytelling)
        ↓ scroll
    Section 4: Climax (dramatic reveal)
        ↓ scroll
    Section 5: Resolution (CTA or conclusion)
    ```
    
    ### Text Reveals
    - Fade in on scroll
    - Typewriter effect on trigger
    - Word-by-word highlight
    - Sticky text with changing visuals
    

---
  #### **Name**
Sticky Sections
  #### **Description**
Pin elements while scrolling through content
  #### **When To Use**
When content should stay visible during scroll
  #### **Implementation**
    ## Sticky Sections
    
    ### CSS Sticky
    ```css
    .sticky-container {
      height: 300vh; /* Space for scrolling */
    }
    
    .sticky-element {
      position: sticky;
      top: 0;
      height: 100vh;
    }
    ```
    
    ### GSAP Pin
    ```javascript
    gsap.to('.content', {
      scrollTrigger: {
        trigger: '.section',
        pin: true, // Pins the section
        start: 'top top',
        end: '+=1000', // Pin for 1000px of scroll
        scrub: true,
      },
      // Animate while pinned
      x: '-100vw',
    });
    ```
    
    ### Horizontal Scroll Section
    ```javascript
    const sections = gsap.utils.toArray('.panel');
    
    gsap.to(sections, {
      xPercent: -100 * (sections.length - 1),
      ease: 'none',
      scrollTrigger: {
        trigger: '.horizontal-container',
        pin: true,
        scrub: 1,
        end: () => '+=' + document.querySelector('.horizontal-container').offsetWidth,
      },
    });
    ```
    
    ### Use Cases
    - Product feature walkthrough
    - Before/after comparisons
    - Step-by-step processes
    - Image galleries
    

---
  #### **Name**
Performance Optimization
  #### **Description**
Keep scroll experiences smooth
  #### **When To Use**
Always - scroll jank kills experiences
  #### **Implementation**
    ## Performance Optimization
    
    ### The 60fps Rule
    - Animations must hit 60fps
    - Only animate transform and opacity
    - Use will-change sparingly
    - Test on real mobile devices
    
    ### GPU-Friendly Properties
    | Safe to Animate | Avoid Animating |
    |-----------------|-----------------|
    | transform | width/height |
    | opacity | top/left/right/bottom |
    | filter | margin/padding |
    | clip-path | font-size |
    
    ### Lazy Loading
    ```javascript
    // Only animate when in viewport
    ScrollTrigger.create({
      trigger: '.heavy-section',
      onEnter: () => initHeavyAnimation(),
      onLeave: () => destroyHeavyAnimation(),
    });
    ```
    
    ### Mobile Considerations
    - Reduce parallax intensity
    - Fewer animated layers
    - Consider disabling on low-end
    - Test on throttled CPU
    
    ### Debug Tools
    ```javascript
    // GSAP markers for debugging
    scrollTrigger: {
      markers: true, // Shows trigger points
    }
    ```
    

## Anti-Patterns


---
  #### **Name**
Scroll Hijacking
  #### **Description**
Taking over natural scroll behavior
  #### **Why Bad**
    Users hate losing scroll control.
    Accessibility nightmare.
    Breaks back button expectations.
    Frustrating on mobile.
    
  #### **What To Do Instead**
    Enhance scroll, don't replace it.
    Keep natural scroll speed.
    Use scrub animations.
    Allow users to scroll normally.
    

---
  #### **Name**
Animation Overload
  #### **Description**
Everything animates on scroll
  #### **Why Bad**
    Distracting, not delightful.
    Performance tanks.
    Content becomes secondary.
    User fatigue.
    
  #### **What To Do Instead**
    Less is more.
    Animate key moments.
    Static content is okay.
    Guide attention, don't overwhelm.
    

---
  #### **Name**
Desktop-Only Experience
  #### **Description**
Scroll effects that break on mobile
  #### **Why Bad**
    Mobile is majority of traffic.
    Touch scroll is different.
    Performance issues on phones.
    Unusable experience.
    
  #### **What To Do Instead**
    Mobile-first scroll design.
    Simpler effects on mobile.
    Test on real devices.
    Graceful degradation.
    