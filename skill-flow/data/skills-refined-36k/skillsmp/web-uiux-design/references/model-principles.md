# Model & Conceptual Design Principles

Guidelines for designing mental models, information architecture, and object-oriented UI.

## Table of Contents
1. [Simplicity & Efficiency](#simplicity--efficiency)
2. [Mental Models](#mental-models)
3. [Object-Oriented UI](#object-oriented-ui)
4. [User Control & Freedom](#user-control--freedom)
5. [Design Laws](#design-laws)
6. [Design Philosophy](#design-philosophy)

---

## Simplicity & Efficiency

### 1. Keep it Simple
Carefully select functions and information, minimizing elements. This is a fundamental principle across all design disciplines.

### 2. Make it Easy
Streamline usage, reducing steps and effort to achieve goals.

### 14. Precomputation
Use pre-discovered optimal values as presets. Examples: rice cooker measuring lines, microwave preset timers, automatic transmission shift timing.

### 18. Conservation of Complexity
Process complexity cannot be eliminated, only moved. Design to move complexity from user side to system side to improve usability.

### 20. Optimize for Major Tasks
Prioritize information and functions for tasks most users perform. 80% of users use only 20% of features (Pareto principle). Treating all requirements equally makes the system harder for everyone.

### 29. Automate Single-Option Actions
If only one action is possible, execute it automatically. Requiring users to perform the only available action provides zero information value.

### 56. Distinguish Possibility from Probability
Don't overcomplicate common usage by overplanning for rare cases. Programmers focus on edge cases; designers should focus on main cases. Treating main and edge cases equally makes interfaces complex and hinders normal use.

### 83. Keep Simple Things Simple
As products mature and gain features, basic functions can become buried in advanced features. Simple tasks must remain simple even as the product grows.

---

## Mental Models

### 3. Mental Model
Match user-imagined usage models with system structure and behavior. Use learnable idioms (conventions) to provide users with usage models. Use metaphors to convey concepts and functionality.

### 4. Signifier
Make interactive elements visible and their meaning instantly understandable. Use familiar expressions and self-evident shapes to suggest usage. Make clickable things look clickable; non-clickable things look non-clickable.

### 5. Mapping
Help users understand correspondence between controls and their effects. Use position, shape, color, and symbols as cues.

### 11. Use User Language
Use labels that match users' everyday vocabulary, not technical system terminology or industry jargon.

### 12. Don't Rely on User Memory
Never assume users remember previous messages or property values. Reference information must be available where needed.

### 71. Idiomatic Over Intuitive
What people call "intuitive" UI is usually "idiomatic" (conventional). Double-clicking to open files and pinch-to-zoom require learning. Focus on using established idioms and, when introducing new interactions, make them naturally learnable.

---

## Object-Oriented UI

### 23. Object-Based Design
Extract objects from requirements and reflect them in UI. Procedure-based function presentation lacks cohesion, is inefficient, and confusing. Extract the fundamental objects (targets of interest) from requirements and let users work with them directly.

### 24. Views Represent Objects
Interfaces are composed of views that represent objects (user concepts of interest). A single object can have multiple views with different representations.

### 25. Objects Embody Their State
All screen objects (icons, selectable items, controls, panes, windows) must visually and continuously reflect their current state. Users modify them through interactive operations, approaching their work goals.

### 26. Noun → Verb Operation Order
Users first select the target (noun), then choose the action (verb). This is fundamental GUI operation order. Action-first creates "waiting for target" states that reduce operational freedom.

### 33. Navigation Items Should Be Nouns
Action-based (verb) navigation labels make it unclear what's there. Action-organized screens create duplicate list views. Organize screens by information type with noun navigation labels.

### 34. Icons Represent Nouns or Adjectives
Icons should depict the object (noun) they symbolize or the resulting state (adjective). Actions (verbs) are difficult to illustrate; except for common ones, avoid forcing them into icons.

### 35. Bind Data
When the same object appears in multiple views simultaneously, synchronize their states. Bidirectional real-time updates give users the feeling of directly working with objects without thinking about data I/O.

---

## User Control & Freedom

### 7. User Control
Let users control the system, not vice versa. Minimize forced operations for system convenience. Don't arbitrarily restrict user actions. Let users always proceed based on their own choices.

### 9. Modeless Design
Minimize modes. In UI, a mode is when an operation's meaning changes based on context, limiting available operations or forcing fixed sequences. Modeless UI allows free-order work.

### 36. Zero, One, Infinity
Avoid arbitrary quantity specifications. Element counts should be 0, 1, or unlimited. Don't limit list items, folder depths, or input characters. Ensure UI handles any quantity without breaking.

### 38. User Input Belongs to User
Save all user-entered values and settings. Users must be able to delete items they added and modify content they entered.

### 76. Enable Spatial Memory
Let users place objects at arbitrary 2D locations (desktops, springboards, windows, palettes) for spatial memory. System should save and restore positions. Never change them without user action.

### 77. Prospective Memory
Let users leave cues for their future selves: bookmarks, flags, open windows, virtual sticky notes, markers, draft saves.

### 87. Make it User's Tool
Build systems as user property, not provider property. Not tools to make users do things, but tools for users to do things. E-commerce: design for buying, not selling.

### 88. Enable Personal Methods and Improvement
Create modeless tools (free operation order) rather than just manual-less ones (easy-to-remember procedures). Creativity comes from devising tool usage. Design for mutual development of person and tool.

### 89. Enable Learning, Don't Educate
Systems should be usable by domain-experienced users without instruction. Make interfaces self-explanatory rather than adding usage instructions.

### 97. Let Users Work at Their Own Pace
No time limits on operations. Don't change operation validity based on timing. Don't require fast reflexes. Users want control, not challenge (except games).

---

## Design Laws

### 16. Fitts's Law
Time to point at a target depends on distance and target depth. Closer + larger = easier to point; farther + smaller = harder. Design clickable areas accordingly.

### 17. Hick's Law
Selection time increases with number of choices. Even if the choice is predetermined, more options mean more time to find it.

### 19. Task Coherence
Users likely repeat yesterday's actions today. Remembering the last action effectively predicts user behavior.

---

## Design Philosophy

### 58. Show Guts
Fulfilling all requirements prevents form from emerging. Design requires courage to make trade-offs. Prioritizing completeness, logic, and precision to avoid misunderstanding or complaints adds information and options that obscure basic intent.

### 98. User Illusion
Computers' capacity and speed allow hiding internal mechanisms while presenting virtual worlds. Enable users to focus on work through illusions: infinitely nestable folders, instantly delivered emails.

### 99. Design Proposes New Meaning
Many innovative designs emerge from internal deliberation as meaning proposals, while drawing on external context (user needs, behavior data). Design not only solves problems but guides new ways of understanding things.

### 100. Positive Impact on Humanity
Tool design isn't just for temporary goal achievement. It serves humanity through tolerance of human shortcomings and enhancement of strengths, enriching life. We inherit accumulated cultural design.
