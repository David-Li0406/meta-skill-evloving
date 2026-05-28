# Motion Design - Validations

## Missing prefers-reduced-motion Support

### **Id**
missing-reduced-motion
### **Severity**
error
### **Type**
regex
### **Pattern**
@keyframes\s+\w+|animation:\s*\w+|animation-name:\s*\w+
### **Negative Pattern**
prefers-reduced-motion
### **Message**
Animation defined without prefers-reduced-motion support in the file.
### **Fix Action**
Add @media (prefers-reduced-motion: reduce) { ... } query to disable or reduce animations
### **Applies To**
  - *.css
  - *.scss
  - *.less
### **Test Cases**
  #### **Should Match**
    - @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
    - animation: slideIn 300ms ease-out
    - animation-name: bounce
  #### **Should Not Match**
    - @media (prefers-reduced-motion: reduce) { animation: none; }

## Layout-Triggering Animation

### **Id**
layout-property-transition
### **Severity**
error
### **Type**
regex
### **Pattern**
transition:\s*[^;]*(width|height|left|right|top|bottom|margin|padding)[^;]*\d+m?s
### **Message**
Animating layout properties causes jank. Use transform instead.
### **Fix Action**
Replace width/height with scale, left/top/right/bottom with translate
### **Applies To**
  - *.css
  - *.scss
  - *.tsx
  - *.jsx
### **Test Cases**
  #### **Should Match**
    - transition: width 300ms ease
    - transition: height 200ms, opacity 200ms
    - transition: left 150ms linear
    - transition: margin-top 300ms
  #### **Should Not Match**
    - transition: transform 300ms ease
    - transition: opacity 200ms
    - width: 100px

## Linear Easing on Transform

### **Id**
linear-easing-transform
### **Severity**
warning
### **Type**
regex
### **Pattern**
transition:\s*[^;]*(transform|translate|scale|rotate)[^;]*linear
### **Message**
Linear easing on movement looks robotic. Use ease-out for entrances, ease-in for exits.
### **Fix Action**
Replace linear with ease-out (entrances) or ease-in (exits) or custom cubic-bezier
### **Applies To**
  - *.css
  - *.scss
### **Test Cases**
  #### **Should Match**
    - transition: transform 300ms linear
    - transition: translateX 200ms linear
    - transition: scale 150ms linear
  #### **Should Not Match**
    - transition: opacity 200ms linear
    - transition: transform 300ms ease-out
    - transition: transform 300ms cubic-bezier(0.4, 0, 0.2, 1)

## Animation Duration Too Long

### **Id**
excessive-animation-duration
### **Severity**
warning
### **Type**
regex
### **Pattern**
(animation-duration|transition-duration|transition:\s*\w+):\s*([1-9][0-9]{3,}ms|[1-9](\.\d+)?s(?!\s*infinite))
### **Message**
Animation over 1 second feels sluggish for functional UI. Keep under 500ms.
### **Fix Action**
Reduce duration to 200-500ms for functional UI transitions
### **Applies To**
  - *.css
  - *.scss
### **Test Cases**
  #### **Should Match**
    - animation-duration: 1500ms
    - transition-duration: 2s
    - transition: opacity 1200ms
  #### **Should Not Match**
    - animation-duration: 300ms
    - transition-duration: 0.3s
    - animation: spin 2s linear infinite

## Permanent will-change Property

### **Id**
permanent-will-change
### **Severity**
warning
### **Type**
regex
### **Pattern**
^\s*will-change:\s*(transform|opacity|all|auto)
### **Negative Pattern**
:hover|:focus|:active
### **Message**
will-change applied permanently wastes GPU memory. Apply only during animation.
### **Fix Action**
Move will-change to :hover state or apply dynamically via JavaScript
### **Applies To**
  - *.css
  - *.scss
### **Test Cases**
  #### **Should Match**
    - .card { will-change: transform; }
    - will-change: opacity
  #### **Should Not Match**
    - .card:hover { will-change: transform; }
    - .card:focus { will-change: transform; }

## Missing Animation Cleanup in React

### **Id**
missing-animation-cleanup-react
### **Severity**
error
### **Type**
regex
### **Pattern**
requestAnimationFrame\s*\(
### **Negative Pattern**
cancelAnimationFrame
### **Message**
requestAnimationFrame without cancelAnimationFrame causes memory leaks.
### **Fix Action**
Store RAF ID and call cancelAnimationFrame in useEffect cleanup
### **Applies To**
  - *.tsx
  - *.jsx
  - *.ts
  - *.js
### **Test Cases**
  #### **Should Match**
    - requestAnimationFrame(animate)
    - requestAnimationFrame(() => {})
  #### **Should Not Match**
    - const id = requestAnimationFrame(animate); cancelAnimationFrame(id)

## Infinite Animation Without Visibility Control

### **Id**
infinite-animation-no-pause
### **Severity**
warning
### **Type**
regex
### **Pattern**
animation:\s*[^;]+infinite
### **Negative Pattern**
animation-play-state|IntersectionObserver|visibilitychange
### **Message**
Infinite animation runs even when not visible, wasting battery.
### **Fix Action**
Add animation-play-state control or pause with Intersection Observer
### **Applies To**
  - *.css
  - *.scss
### **Test Cases**
  #### **Should Match**
    - animation: spin 1s linear infinite
    - animation: pulse 2s ease-in-out infinite
  #### **Should Not Match**
    - .spinner { animation-play-state: paused; }

## Transition Without Easing Function

### **Id**
no-easing-function
### **Severity**
info
### **Type**
regex
### **Pattern**
transition:\s*(\w+(-\w+)?)\s+\d+m?s\s*;
### **Message**
Transition missing easing function. Defaults to ease which may not be intended.
### **Fix Action**
Explicitly specify easing: ease-out for entrances, ease-in for exits
### **Applies To**
  - *.css
  - *.scss
### **Test Cases**
  #### **Should Match**
    - transition: opacity 200ms;
    - transition: transform 300ms;
  #### **Should Not Match**
    - transition: opacity 200ms ease-out;
    - transition: transform 300ms cubic-bezier(0.4, 0, 0.2, 1);

## GSAP Timeline Without Kill

### **Id**
gsap-no-kill
### **Severity**
warning
### **Type**
regex
### **Pattern**
gsap\.(timeline|to|from|fromTo)\s*\(
### **Negative Pattern**
\.kill\(|\.clear\(|gsap\.killTweensOf
### **Message**
GSAP animations should be killed on component unmount to prevent memory leaks.
### **Fix Action**
Call timeline.kill() or gsap.killTweensOf(element) in cleanup
### **Applies To**
  - *.tsx
  - *.jsx
  - *.ts
  - *.js
### **Test Cases**
  #### **Should Match**
    - gsap.to(element, { x: 100 })
    - const tl = gsap.timeline()
  #### **Should Not Match**
    - tl.kill()
    - gsap.killTweensOf(element)

## Framer Motion Without Exit Animation

### **Id**
framer-motion-no-exit
### **Severity**
info
### **Type**
regex
### **Pattern**
<motion\.\w+[^>]*animate=[^>]*>
### **Negative Pattern**
exit=|AnimatePresence
### **Message**
Motion component may disappear abruptly without exit animation.
### **Fix Action**
Add exit prop and wrap in AnimatePresence for smooth exit
### **Applies To**
  - *.tsx
  - *.jsx
### **Test Cases**
  #### **Should Match**
    - <motion.div animate={{ opacity: 1 }}>
    - <motion.span animate={controls}>
  #### **Should Not Match**
    - <motion.div animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
    - <AnimatePresence><motion.div /></AnimatePresence>

## Scale Animation Missing transform-origin

### **Id**
scale-missing-transform-origin
### **Severity**
info
### **Type**
regex
### **Pattern**
(scale\s*\(|transform:\s*[^;]*scale)
### **Negative Pattern**
transform-origin
### **Message**
Scale animation defaults to center. Verify this is the intended origin point.
### **Fix Action**
Add transform-origin if scaling should occur from a specific point (e.g., top-left for dropdowns)
### **Applies To**
  - *.css
  - *.scss
### **Test Cases**
  #### **Should Match**
    - transform: scale(1.1)
    - scale(0)
  #### **Should Not Match**
    - transform: scale(1.1); transform-origin: top left;

## Transition All Properties

### **Id**
transition-all-performance
### **Severity**
warning
### **Type**
regex
### **Pattern**
transition:\s*all\s+\d+m?s
### **Message**
transition: all animates every property change, causing performance issues.
### **Fix Action**
Specify exact properties: transition: transform 200ms, opacity 200ms
### **Applies To**
  - *.css
  - *.scss
### **Test Cases**
  #### **Should Match**
    - transition: all 300ms ease
    - transition: all 0.3s
  #### **Should Not Match**
    - transition: transform 300ms, opacity 300ms
    - transition: color 200ms ease

## Animation Only on Hover (Mobile Issue)

### **Id**
hover-only-animation-trigger
### **Severity**
info
### **Type**
regex
### **Pattern**
:hover\s*\{[^}]*animation:
### **Message**
Animation triggered only on hover won't work on touch devices.
### **Fix Action**
Consider adding touch/click trigger or providing non-hover alternative
### **Applies To**
  - *.css
  - *.scss
### **Test Cases**
  #### **Should Match**
    - .card:hover { animation: pulse 1s; }
  #### **Should Not Match**
    - .card { animation: pulse 1s; }
    - .card:active { animation: pulse 1s; }

## Negative Animation Delay Overuse

### **Id**
negative-animation-delay
### **Severity**
info
### **Type**
regex
### **Pattern**
animation-delay:\s*-\d+m?s
### **Message**
Negative animation delay can cause jarring starts. Ensure this is intentional.
### **Fix Action**
Verify negative delay creates the desired 'mid-animation start' effect
### **Applies To**
  - *.css
  - *.scss
### **Test Cases**
  #### **Should Match**
    - animation-delay: -200ms
    - animation-delay: -0.5s
  #### **Should Not Match**
    - animation-delay: 200ms
    - animation-delay: 0s