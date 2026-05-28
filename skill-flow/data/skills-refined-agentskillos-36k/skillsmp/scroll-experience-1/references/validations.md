# Scroll Experience - Validations

## No Reduced Motion Support

### **Id**
no-reduced-motion
### **Severity**
high
### **Type**
pattern
### **Check**
Should respect prefers-reduced-motion
### **Pattern**
prefers-reduced-motion
### **Indicators**
  - No @media (prefers-reduced-motion)
  - Animations run regardless of preference
  - No matchMedia check for reduced motion
### **Message**
Not respecting reduced motion preference - accessibility issue.
### **Fix Action**
Add prefers-reduced-motion media query to disable/reduce animations

## Unthrottled Scroll Events

### **Id**
scroll-event-no-throttle
### **Severity**
medium
### **Type**
pattern
### **Check**
Scroll events should be throttled
### **Pattern**
addEventListener.*scroll
### **Indicators**
  - Raw scroll event listeners
  - Heavy computation on scroll
  - No requestAnimationFrame
### **Message**
Scroll events may not be throttled - potential jank.
### **Fix Action**
Use requestAnimationFrame or GSAP ScrollTrigger for smooth performance

## Animating Layout-Triggering Properties

### **Id**
animating-layout-properties
### **Severity**
medium
### **Type**
pattern
### **Check**
Should only animate transform and opacity
### **Pattern**
animation.*(?:width|height|top|left|margin|padding)
### **Indicators**
  - Animating width/height
  - Animating position properties
  - Animating margin/padding
### **Message**
Animating layout properties causes jank.
### **Fix Action**
Use transform (translate, scale) and opacity instead

## Missing will-change Optimization

### **Id**
no-will-change
### **Severity**
low
### **Type**
conceptual
### **Check**
Heavy animations should use will-change
### **Indicators**
  - Complex animations without will-change
  - Many animated elements
  - No GPU hints
### **Message**
Consider adding will-change for heavy animations.
### **Fix Action**
Add will-change: transform to frequently animated elements

## Scroll Hijacking Detected

### **Id**
scroll-hijacking
### **Severity**
medium
### **Type**
pattern
### **Check**
Should not prevent default scroll
### **Pattern**
preventDefault.*scroll|scrollTo.*behavior
### **Indicators**
  - Preventing default scroll
  - Custom scroll speed
  - Scroll snapping everything
### **Message**
May be hijacking scroll behavior.
### **Fix Action**
Let users scroll naturally, use scrub animations instead