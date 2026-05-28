# Interaction Design Principles

Guidelines for direct manipulation, feedback, controls, forms, and user input.

## Table of Contents
1. [Direct Manipulation](#direct-manipulation)
2. [Feedback & Response](#feedback--response)
3. [Error Handling](#error-handling)
4. [Form Design](#form-design)
5. [Controls & Input](#controls--input)
6. [Shortcuts & Efficiency](#shortcuts--efficiency)

---

## Direct Manipulation

### 8. Direct Manipulation
Give the sensation of directly touching and manipulating on-screen objects. Update display in real-time following physical actions (feedback). Enable returning to previous state through reverse actions (reversibility).

### 30. Keep Pen Near Paper
Place tools near their targets. If objects are visible but require opening separate windows to operate, it's like walking to the hallway for a pen. Enable modeless in-place operations with immediate results.

### 79. Direct Manipulation Gestures
Screen responses to gestures should directly follow input movements. Purely symbolic gestures (specific movements triggering commands) are hard to learn because movement-meaning mapping is arbitrary.

### 92. Move as Intended, Not as Moved
Interfaces should respond to operations smoothly, but for true control feeling, include appropriate "play" and "correction" from experience rather than raw input device values.

---

## Feedback & Response

### 65. Respond Within 0.1 Seconds
Respond to user operations as quickly as possible. The limit for feeling instantaneous is 0.1 seconds. Flow of thought is maintained up to 1 second. Focused waiting time is 10 seconds. Longer processes need progress indicators and time estimates.

### 66. Feedback Near the Action
Show system state changes near where users are focusing. For object actions, show change in the object itself. For standalone buttons, show feedback near the button.

### 63. Animate Screen Changes
When changing large screen areas, use transition animations so users can perceive state change continuity. Show intermediate states between before and after in 0.1-0.5 seconds.

### 64. Bidirectional Transitions
When animating from state A to B, apply reverse animation for B to A. This directional correspondence helps users correctly imagine the information space structure.

### 57. Execute Silently
Don't confirm every user intention or report successful completion. Communicate operation status and results through screen changes, not modal dialogs. Only confirm irreversible actions with data loss risk.

### 90. Don't Lock UI
In GUI: 1. User action → 2. Program processing → 3. Result display, repeated. UI lock means step 2 takes long, step 3 is delayed, and UI won't accept next actions. UI locks over a few seconds break the sense of free application control.

---

## Error Handling

### 13. Constraint
Intentionally limit user actions to reduce errors and promote effective usage. Example: Scissors handle shape constrains grip direction so blades always orient correctly (force-efficient, visible cut line).

### 15. Prevent Errors
Make operation mistakes difficult. Good error messages matter, but preventing errors is more important. Clearly distinguish similar things. Disable contextually meaningless operations.

### 39. Don't Request Integrity-Breaking Operations
Never ask users to perform operations that could break data integrity. Don't let users manually turn on brake lights. Don't ask for both birthdate and age input.

### 54. Fail-Safe Over Fool-Proof
Making things impossible to mistake matters less than making mistakes harmless. If all operations are reversible, errors essentially don't exist—everything becomes part of goal-directed trial and error.

### 55. Constructive Error Display
Help user understanding and action with clear error messages. Explain what happened accurately and show what to do next. Programmer error codes are useless to general users. Avoid excessive language.

### 50. Don't Demand Precision
Minimize input format constraints from system requirements. Absorb format variations (full/half-width, hiragana/katakana, hyphen presence) on system side with automatic formatting/completion. Don't require mechanical precision from users.

---

## Form Design

### 32. Present Prerequisites First
Requiring prerequisites at the end of long procedures may waste user effort. Examples: externally referenced input information, required agreement to terms.

### 40. Give Forms Story Flow
Group input items meaningfully for users. Order items from familiar/simple to complex.

### 41. Create Operation Flow
Use Gestalt grouping and story-based item placement to guide user vision and operation. Action buttons suggest flow endpoints (button gravity), so users should see paths to them.

### 42. Good Defaults
Good default values in selection inputs and settings reduce operations. Good defaults: lower risk, more common, more neutral, reflect current state, reflect user history.

### 43. Use Constraint Controls
For inputs with limited valid values (fixed options, numbers, dates), use radio buttons, dropdowns, steppers, sliders, pickers to allow only valid input.

### 44. Phrase Options Positively
Make option wording positive. With toggle controls like radio buttons and checkboxes, negative labels mean selection "affirms negation," which is confusing.

### 45. Let Users Choose Results, Not Input Values
Users generally prefer selecting from choices over typing. Show resulting states as options rather than having them set parameter values.

### 46. Structure Input Fields
Divide input fields or use constraint controls matching expected value format. This suggests input content, improves efficiency, and reduces errors. But consider information characteristics and usage context—sometimes simple text boxes are more efficient.

### 47. Use Specific Verbs for Default Buttons
In modal dialogs and form screens, label default buttons with specific action verbs ("Save", "Delete") rather than "OK" or "Yes."

### 51. Provide Input Suggestions
Typing is high-effort; users prefer selecting from options. Present "what they were trying to input" or "valuable input values" as suggestions partway through input.

### 62. Defer Answers
Don't require all decisions upfront; allow deferring non-essential answers. Allow use without accounts, allow record creation without filling all attributes. Only require clearly necessary fields.

---

## Controls & Input

### 48. Radio Buttons for Single Selection, Checkboxes for On/Off
Radio buttons: single selection from options. Require default value. Checkboxes: independent on/off items. Also for multiple selection from options. A or B = radio button; true or false = checkbox.

### 49. Avoid Flip-Flop Problem
When one button toggles on/off, it's unclear if the label shows current state or post-press state. Separate state display from button label to avoid this problem.

### 78. Touch Targets 7mm or Larger
On touchscreens, make buttons and controls 7-10mm square minimum for finger pressing. Also space elements apart to prevent mis-taps since touch targets obscure the pressed element.

### 93. Expand Hotspots
Make tap/click areas larger than visible button boundaries. This balances visual design with pressability. But don't separate the element from its hotspot.

---

## Shortcuts & Efficiency

### 22. Provide Shortcuts
Offer ways for experienced users to perform frequent actions faster than step-by-step procedures: keyboard shortcuts, bookmarks, gestures, history.

### 21. Persuasion
Use persuasive mechanisms to encourage user action: usage guides, recommendations, psychological rewards, social comparison, VR/simulation-based vicarious experiences to motivate and prompt decisions.

### 53. Show Previews in Property Choices
When selecting object styles or tools, show result-state previews as options. Seeing results before applying properties improves trial-and-error efficiency.

### 67. Progressive Disclosure
Hide advanced features initially for beginners, revealing them when needed or when users are ready. This enables gradual learning.
