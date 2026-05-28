# Presentation & Layout Principles

Guidelines for visual design, navigation, layout, and accessibility.

## Table of Contents
1. [Visual Consistency](#visual-consistency)
2. [Visual Perception](#visual-perception)
3. [Information Display](#information-display)
4. [Navigation & Wayfinding](#navigation--wayfinding)
5. [Mobile & Touch](#mobile--touch)
6. [Internationalization](#internationalization)
7. [Accessibility](#accessibility)

---

## Visual Consistency

### 6. Consistency
Apply consistent rules to colors, shapes, placement, and behavior. Same properties = same expression; different properties = different expression. Consistency embodies design logic and provides basic cues for users to predict and learn system usage.

### 27. Unify Graphic Tone & Manner
Align visual elements: hue/saturation/brightness, gradients, borders, shadows, corner radius, fill vs. stroke, line weight, color vs. silhouette, concrete vs. abstract levels.

### 37. All Operable Elements Must Have Meaning
Every currently operable element and selectable item must be meaningful for user tasks. Meaningless elements obstruct tasks—disable or hide them.

### 73. Don't Change Menu Item Positions
In menus with action or navigation items, maintain positional relationships regardless of context. Users remember menu items spatially; changing positions prevents learning.

### 74. Highlight by Changing Only One Element
To highlight items among peers, change or add only one visual attribute. Too much change makes the highlight look like a different element type.

### 75. Account for Optical Illusions
While unifying element sizes, shapes, positions, and colors is important for consistency, screen composition can create optical illusions with unintended appearances. Know illusion patterns and adjust by eye when needed.

### 84. Don't Overuse Colors and Fonts
Colors and typefaces can emphasize elements and show information groups, but too many varieties create visual clutter.

### 85. Lay Out Systematically
Position screen elements along grids. Apply consistent, repetitive margins and alignment. This creates visual stability and logically shows information structure through containment relationships and shape continuity.

---

## Visual Perception

### 10. Visual Gestalt
Human perception defines objects from holistic frameworks, not individual elements (Gestalt psychology). Use patterns (proximity, similarity, closure—Prägnanz laws) to effectively show element groupings.

### 31. Show Visually, Explain with Text
Make object presence and state visually perceptible; supplement with text. Use icons to express item nature, labels for clarity. Express information graphically, add numerical details.

### 28. Convey Information, Not Data
Users want meaning, not numbers. They want to know disk space remaining percentage, not bytes used. They want to know roughly how many songs fit, not exact storage capacity when buying a music player.

---

## Information Display

### 52. Show Continuation on Scrollable Screens
When users should scroll long pages, avoid content breaks exactly at screen bottom—it won't look scrollable. Adjust content breaks to suggest continuation.

### 86. Don't Rely on Customization
Using customization to address varying user requirements makes systems more complex, reducing learnability and maintainability. First determine optimal UI specifications, then offer customization cautiously and sparingly.

### 91. Don't Introduce Games
Users want to achieve goals, not play games (unless it's a game app). Don't include gaming elements: chance, surprise, gambling, complexity, speed/timing demands, dexterity requirements, intuition requirements.

---

## Navigation & Wayfinding

### 59. Wayfinding
Provide signposts in information spaces to prevent users from getting lost: where am I, where can I go, what's nearby, how do I return. Use consistent navigation schemes to help users grasp system overview.

### 60. Escape Hatch
Provide exits to return to starting points anytime. In home-screen-based navigation or specific modes, let lost or interrupted users easily return to base screens.

### 61. Immediate Gratification
Let users achieve success within seconds of starting the product. Show basic work screens or object lists as early as possible. Let users start work immediately and feel legitimate progress.

### 80. Drill-Down: Top→Bottom, Left→Right
When dividing screens into hierarchical panes for navigation: selections on top show content below; selections on left show content on right. Reverse for RTL languages (Arabic, etc.).

### 81. Left is Back, Right is Forward
When showing screen transition direction horizontally: left = back (past), right = forward (future). Reverse for RTL languages.

### 82. Mobile: Hierarchical Over Comprehensive
Desktop apps should comprehensively show workspace overview. Mobile should limit visible information and show hierarchically.

---

## Mobile & Touch

### 78. Touch Targets 7mm or Larger
On touchscreens, make buttons and controls 7-10mm square minimum. Space elements to prevent mis-taps since fingers obscure touched elements.

### 79. Direct Manipulation Gestures
Gesture screen responses should directly follow input movements. Symbolic gestures (specific movements = commands) are hard to learn due to arbitrary movement-meaning mapping.

### 93. Expand Hotspots
Make tap/click areas larger than visible button boundaries to balance visual design with pressability. Don't separate elements from their hotspots.

---

## Internationalization

### 68. Don't Base Icon Motifs on Specific Cultures
Icons typically use symbolic expressions, but signs used only in specific cultures or language-dependent idioms shouldn't be used in international services.

### 69. Account for Label Length Differences Across Languages
Word length varies by language. German averages 1.4x English—useful for layout testing. Conversely, Chinese characters and Korean create short labels—ensure buttons remain pressable.

### 70. Don't Casually Use ○✕△ Symbols
In Japan, ○ and ✕ mean "good" and "bad," but these symbol nuances vary by culture. International interfaces may not convey meaning. ✕ sometimes has positive connotations like checkmarks.

### 72. Follow Platform Rules for Positive/Negative Button Order
Dialog button order should follow platform conventions over app logic, prioritizing user habits. Without clear rules, follow general sense: left = back, right = forward, so right = positive button.

---

## Accessibility

### 94. Support Screen Readers
Enable use with screen readers and voice browsers. Add alt text to non-text information like images. Follow standard platform/environment specifications for accessibility.

### 95. Support Text Scaling
Enable use with enlarged text display. Support platform/browser text scaling functions through standard implementation.

### 96. Don't Depend on Color
Don't make interfaces color-dependent. Ensure information conveys without color through: brightness contrast, border/underline decoration, shape/position mapping, text supplements. Test in grayscale to verify.

### 97. Let Users Work at Their Own Pace
No time limits on operations. Don't vary operation validity by timing. Don't require fast reflexes. Users want control, not challenge (except games).
