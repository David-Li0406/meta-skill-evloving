# Motion Graphics

## Patterns


---
  #### **Name**
The 12 Principles Applied to Motion Graphics
  #### **Description**
Disney's animation principles adapted for motion design
  #### **When**
Creating any animation to ensure professional quality
  #### **Example**
    Most relevant principles for motion graphics:
    
    1. Timing: Speed conveys weight and emotion
       - Heavy elements move slowly
       - Light elements move quickly
       - Pause for emphasis
    
    2. Easing: Never linear motion
       - Ease out of starting position
       - Ease into final position
       - Use bezier curves, not linear
    
    3. Anticipation: Movement before action
       - Pull back before moving forward
       - Small movements telegraph big ones
    
    4. Follow-through: Movement after action
       - Elements settle into place
       - Overlapping motion feels natural
    
    5. Staging: Clear visual hierarchy
       - One thing moves at a time
       - Motion guides eye to what matters
    

---
  #### **Name**
Kinetic Typography Framework
  #### **Description**
Make text come alive without distracting from reading
  #### **When**
Animating text, titles, or typography-heavy content
  #### **Example**
    Rules for kinetic type:
    
    1. Sync to audio: Words appear with speech or music beats
    2. Hierarchy through timing: Important words land last or pause
    3. Movement direction: Left-to-right for reading flow
    4. Scale for emphasis: Bigger = more important
    5. Color for attention: Highlight keywords
    
    Common techniques:
    - Word-by-word reveal (synced to VO)
    - Sentence builds
    - Type tracking in/out
    - Scale pops on keywords
    - Position shifts between phrases
    
    Avoid: Random movements that fight reading flow
    

---
  #### **Name**
Logo Animation Standards
  #### **Description**
Bring logos to life while respecting brand identity
  #### **When**
Creating animated logos for intros, outros, or brand moments
  #### **Example**
    Logo animation approaches:
    
    1. Reveal: Elements draw or fade in
       - Best for clean, geometric logos
       - Mask reveals, path traces
    
    2. Assembly: Parts come together
       - Best for multi-element logos
       - Shows how pieces connect
    
    3. Transform: Shape morphs to logo
       - Best for memorable brand moments
       - Requires conceptual connection
    
    4. Character: Logo has personality
       - Best for friendly/playful brands
       - Subtle bounce, blink, or gesture
    
    Timing: 2-4 seconds total. Any longer feels self-indulgent.
    Sound: Optional but elevates when matched to movement.
    

---
  #### **Name**
Data Visualization Animation
  #### **Description**
Animate charts and graphs for clarity and impact
  #### **When**
Presenting data in video or presentation format
  #### **Example**
    Animation adds value when it shows:
    
    1. Change over time: Animate the progression
       - Bar charts growing to final values
       - Line charts drawing left to right
       - Pie charts revealing segments sequentially
    
    2. Comparison: Highlight differences
       - Elements scale relative to each other
       - Color transitions draw attention
       - Labels appear on cue with narration
    
    3. Hierarchy: Most important last
       - Build to the key insight
       - Pause on conclusion data
    
    Pacing: Match narration. Data lands with explanation.
    
    Anti-pattern: Animating data that doesn't change—adds nothing.
    

---
  #### **Name**
Micro-Interaction Design
  #### **Description**
Small animations that enhance UI/UX
  #### **When**
Creating web/app animations for buttons, states, or feedback
  #### **Example**
    Key micro-interactions:
    
    1. Button feedback
       - Hover: Subtle scale or color shift (100-200ms)
       - Click: Quick press animation (50-100ms)
       - Loading: Spinner or progress indicator
       - Success: Checkmark or confirmation
    
    2. State changes
       - Toggle: Smooth slide with easing
       - Expand/collapse: Height animation with content reveal
       - Page transitions: Fade or slide (200-300ms)
    
    3. Loading states
       - Skeleton screens over spinners
       - Progress bars over indefinite spinners
       - Subtle pulse animations
    
    Rule: Micro-animations should be felt, not noticed.
    Duration: 100-400ms for most interactions.
    

---
  #### **Name**
Export Optimization
  #### **Description**
Deliver motion graphics in the right format for every use case
  #### **When**
Preparing final deliverables for web, app, or video
  #### **Example**
    Format guide:
    
    Video (YouTube, social, ads):
    - H.264/H.265, 1080p or 4K
    - High bitrate for quality
    - Correct frame rate (24/30/60 fps)
    
    Web animation (Lottie):
    - Export from AE with Bodymovin
    - Optimize JSON file size
    - Test in browser before delivery
    
    Product UI (Rive):
    - State machine for interactivity
    - Export for platform (web, iOS, Android)
    
    GIF (legacy, avoid if possible):
    - Maximum 15 seconds
    - Optimize palette
    - Consider WebP/MP4 instead
    

## Anti-Patterns


---
  #### **Name**
Over-Animation
  #### **Description**
Animating everything just because you can
  #### **Why**
Competing movements create chaos; viewers don't know where to look
  #### **Instead**
Animate with purpose. One focus at a time.

---
  #### **Name**
Linear Easing
  #### **Description**
Using linear motion instead of easing curves
  #### **Why**
Linear motion feels robotic and unnatural
  #### **Instead**
Always use ease-in, ease-out, or custom bezier curves

---
  #### **Name**
Ignoring Timing
  #### **Description**
Treating all elements with the same duration
  #### **Why**
Uniform timing feels mechanical; natural motion has variation
  #### **Instead**
Heavy things move slower. Small things move faster. Vary duration.

---
  #### **Name**
Style Over Story
  #### **Description**
Prioritizing trendy effects over clear communication
  #### **Why**
Trends fade; clear communication endures
  #### **Instead**
What is the message? How does motion clarify it?

---
  #### **Name**
No Sound Sync
  #### **Description**
Creating motion without considering audio relationship
  #### **Why**
Motion and audio should dance together; misalignment feels wrong
  #### **Instead**
Animate to audio cues. Even if silent, imagine the rhythm.

---
  #### **Name**
Massive File Sizes
  #### **Description**
Delivering unoptimized files that slow down playback
  #### **Why**
Laggy animation is worse than no animation
  #### **Instead**
Optimize exports. Test on target platforms. Prioritize performance.