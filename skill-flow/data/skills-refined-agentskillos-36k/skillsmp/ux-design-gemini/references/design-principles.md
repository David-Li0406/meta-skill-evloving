# UX Design Principles and Methodology

Foundational design principles and methodologies for creating user-centered experiences using Gemini.

---

## UX Design Methodologies

### User-Centered Design (UCD)

User-Centered Design places users at the heart of the design process through iterative research and validation.

**Core Principles:**
1. **Early focus on users** - Understand user needs before designing
2. **Empirical measurement** - Test designs with real users
3. **Iterative design** - Refine based on feedback
4. **Integrated design** - Consider entire user experience

**UCD Process:**
```
Research → Design → Prototype → Test → Iterate
```

### Design Thinking (5 Stages)

A human-centered approach to innovation combining empathy, creativity, and rationality.

**5-Stage Framework:**

1. **Empathize** - Understand user needs through research
   - User interviews
   - Contextual inquiry
   - Empathy mapping

2. **Define** - Synthesize findings into clear problem statements
   - User personas
   - Problem framing
   - Point-of-view statements

3. **Ideate** - Generate creative solutions
   - Brainstorming
   - Mind mapping
   - "How Might We" questions

4. **Prototype** - Create tangible representations
   - Low-fidelity wireframes
   - Paper prototypes
   - Interactive mockups

5. **Test** - Validate with users and iterate
   - Usability testing
   - A/B testing
   - Feedback analysis

### Double Diamond Process

British Design Council's framework dividing design into four phases:

```
Discover → Define → Develop → Deliver
  (Diverge)  (Converge) (Diverge)  (Converge)
```

**Diamond 1: Problem Space**
- Discover: Research the problem
- Define: Identify the core challenge

**Diamond 2: Solution Space**
- Develop: Explore possible solutions
- Deliver: Finalize and implement

---

## Usability Principles

### Nielsen's 10 Heuristics

Jakob Nielsen's foundational usability principles for interface design.

#### 1. Visibility of System Status

**Principle:** Keep users informed about what's happening through timely feedback.

**Examples:**
- Loading spinners during data fetch
- Progress bars for multi-step processes
- Success/error messages after actions
- Active state indicators in navigation

**Gemini Prompt:**
```
设计一个文件上传流程的状态反馈系统，包含等待、进行中、成功、失败四种状态的UI表现
```

#### 2. Match Between System and Real World

**Principle:** Use familiar language and concepts instead of system-oriented terms.

**Examples:**
- "Trash" icon for delete (vs "Remove from database")
- "Shopping cart" metaphor for e-commerce
- Calendar interfaces resembling physical calendars

#### 3. User Control and Freedom

**Principle:** Provide undo/redo and easy exit options.

**Examples:**
- Undo button for accidental deletions
- Cancel button in forms
- Back navigation in wizards
- Edit after submission

#### 4. Consistency and Standards

**Principle:** Follow platform conventions and maintain internal consistency.

**Examples:**
- iOS: Bottom tab bar navigation
- Android: Material Design floating action button
- Web: Blue underlined links
- Consistent button placement across pages

#### 5. Error Prevention

**Principle:** Prevent errors before they occur through good design.

**Examples:**
- Disable submit button until form is valid
- Confirmation dialogs for destructive actions
- Input constraints (date pickers vs manual entry)
- Auto-save drafts

#### 6. Recognition Rather Than Recall

**Principle:** Minimize memory load by making options visible.

**Examples:**
- Dropdown menus vs typing commands
- Auto-complete in search
- Recently used items
- Visual breadcrumbs

#### 7. Flexibility and Efficiency of Use

**Principle:** Provide shortcuts for expert users while remaining accessible to novices.

**Examples:**
- Keyboard shortcuts (Ctrl+C, Ctrl+V)
- Bulk actions for power users
- Customizable dashboards
- Quick filters

#### 8. Aesthetic and Minimalist Design

**Principle:** Remove unnecessary elements that compete for attention.

**Examples:**
- White space for breathing room
- Progressive disclosure (show details on demand)
- Clear visual hierarchy
- Focused call-to-actions

#### 9. Help Users Recognize, Diagnose, and Recover from Errors

**Principle:** Error messages should be clear, constructive, and helpful.

**Examples:**
- "Email already registered. Try logging in?" (vs "Error 409")
- Highlight invalid form fields
- Suggest corrections ("Did you mean: example@gmail.com?")
- Provide recovery options

#### 10. Help and Documentation

**Principle:** Provide searchable, task-focused help when needed.

**Examples:**
- Contextual tooltips
- Interactive onboarding
- Searchable FAQ
- In-app tutorials

---

### Key UX Laws

#### Jakob's Law

**Principle:** Users spend most time on other sites, so they prefer yours to work the same way.

**Application:** Follow established patterns (e.g., logo in top-left, hamburger menu for mobile)

#### Fitts's Law

**Principle:** Time to acquire a target is a function of distance and size.

**Application:**
- Make important buttons larger
- Place related actions close together
- Keep primary CTAs within thumb reach (mobile)

#### Hick's Law

**Principle:** Decision time increases with number of choices.

**Application:**
- Limit menu items (7±2 rule)
- Progressive disclosure for complex options
- Group related choices

---

## Mobile Design Guidelines

### iOS Human Interface Guidelines

**Key Principles:**

1. **Clarity** - Text is legible, icons precise, functionality obvious
2. **Deference** - UI helps users understand content without competing
3. **Depth** - Layering and motion provide hierarchy and vitality

**Design Specs:**
- Safe area: Respect notch and home indicator
- Tap targets: Minimum 44×44 pt
- Typography: SF Pro (system font)
- Navigation: Tab bar (max 5 items), navigation bar

**iOS-Specific Patterns:**
- Swipe gestures (back, delete)
- Pull-to-refresh
- Action sheets and alerts
- SF Symbols for icons

### Material Design (Android)

**Core Concepts:**

1. **Material is the metaphor** - Inspired by physical materials
2. **Bold, graphic, intentional** - Print-based design principles
3. **Motion provides meaning** - Responsive and natural animations

**Design Specs:**
- Touch targets: Minimum 48×48 dp
- Elevation: 0-24dp for layering
- Typography: Roboto font
- 8dp grid system

**Material Components:**
- Floating Action Button (FAB)
- Bottom sheets
- Cards and elevation
- Snackbars for feedback

### Responsive Design Principles

**Breakpoints:**
- Mobile: 320-480px
- Tablet: 768-1024px
- Desktop: 1280px+

**Strategies:**
- **Fluid grids** - Percentage-based layouts
- **Flexible images** - max-width: 100%
- **Media queries** - Conditional CSS
- **Mobile-first** - Design for smallest screen first

---

## Accessibility Design (WCAG)

### WCAG 2.1 Level AA Standards

Web Content Accessibility Guidelines ensure designs are usable by people with disabilities.

#### 1. Perceivable

**1.1 Text Alternatives**
- Alt text for images
- Captions for videos
- Transcripts for audio

**1.4 Distinguishable**
- Color contrast ratio ≥ 4.5:1 (normal text)
- Color contrast ratio ≥ 3:1 (large text, 18pt+)
- Text resizable up to 200%
- Don't rely on color alone to convey information

#### 2. Operable

**2.1 Keyboard Accessible**
- All functionality available via keyboard
- No keyboard traps
- Visible focus indicators

**2.4 Navigable**
- Skip to main content link
- Clear page titles
- Logical tab order
- Multiple ways to find pages

#### 3. Understandable

**3.1 Readable**
- Identify language (lang attribute)
- Define unusual words

**3.2 Predictable**
- Consistent navigation
- No unexpected context changes
- Consistent identification

#### 4. Robust

**4.1 Compatible**
- Valid HTML markup
- ARIA labels for custom widgets
- Screen reader compatibility

### Practical Accessibility Tips

**Form Design:**
- Label every input field
- Group related fields with `<fieldset>`
- Clear error messages
- Inline validation feedback

**Color Usage:**
- Use text labels with color coding
- Provide multiple visual cues (icons + color)
- Test with color blindness simulators

**Interactive Elements:**
- Focus visible (outline or highlight)
- Large enough touch targets (44×44 pt)
- Descriptive link text ("Learn more about accessibility" vs "Click here")

---

## Visual Hierarchy Principles

### Reading Patterns

#### F-Pattern (Text-Heavy Pages)

Users scan in an F-shaped pattern:
1. Horizontal movement across top
2. Horizontal movement partway down
3. Vertical scanning on left

**Design Strategy:**
- Place important info at top
- Front-load headings and lists
- Use left-aligned text

#### Z-Pattern (Sparse Content)

Eyes move in Z-shape:
1. Top-left to top-right
2. Diagonal to bottom-left
3. Bottom-left to bottom-right

**Design Strategy:**
- Logo top-left
- CTA top-right
- Supporting info middle
- Secondary CTA bottom-right

### Visual Weight Distribution

**Creating Hierarchy:**

1. **Size** - Larger elements attract attention first
2. **Color** - Bright colors stand out
3. **Contrast** - High contrast draws the eye
4. **Position** - Top and center are noticed first
5. **Whitespace** - Isolation creates emphasis
6. **Typography** - Bold, uppercase, or unique fonts

### Whitespace Usage

**Benefits:**
- Improves readability (line spacing, margins)
- Groups related elements
- Creates focus on key elements
- Conveys elegance and simplicity

**Application:**
- Micro whitespace: Between lines, letters, UI elements
- Macro whitespace: Between major layout sections

---

## Color Theory for UX

### Color Psychology

| Color | Associations | Common Uses |
|-------|-------------|-------------|
| **Blue** | Trust, calm, professional | Finance, healthcare, corporate |
| **Green** | Growth, health, money | Environment, wellness, banking |
| **Red** | Urgency, passion, danger | Sales, alerts, food |
| **Yellow** | Optimism, warning, energy | Warnings, highlights, children |
| **Purple** | Luxury, creativity, wisdom | Beauty, premium products |
| **Black** | Sophistication, power | Luxury brands, minimalism |
| **White** | Purity, simplicity, cleanliness | Healthcare, minimalism |

### Color Schemes

#### Monochromatic
- Single hue with varying shades/tints
- Creates harmonious, clean look
- Use for minimalist designs

#### Complementary
- Opposite colors on color wheel (e.g., blue/orange)
- High contrast and vibrant
- Use for CTAs that need to stand out

#### Analogous
- Adjacent colors on wheel (e.g., blue/teal/green)
- Harmonious and calming
- Use for cohesive brand palettes

#### Triadic
- Three evenly spaced colors (e.g., red/yellow/blue)
- Vibrant and balanced
- Use for playful, energetic designs

### Accessible Color Selection

**Contrast Requirements (WCAG):**
- **AA (Minimum):** 4.5:1 for normal text, 3:1 for large text
- **AAA (Enhanced):** 7:1 for normal text, 4.5:1 for large text

**Tools for Testing:**
- WebAIM Contrast Checker
- Color Oracle (color blindness simulator)
- Stark plugin (Figma/Sketch)

**Common Mistakes:**
- Light gray text on white background
- Yellow text on white background
- Relying only on red/green for status

---

## Applying Principles with Gemini

### Example Prompts

**Heuristic Evaluation:**
```
使用Nielsen's 10 Heuristics评估这个登录页面设计：
1. 系统状态可见性
2. 系统与现实世界的匹配
3. 用户控制和自由
[附上设计稿截图]
```

**Accessibility Audit:**
```
审查这个表单设计的无障碍性：
- WCAG 2.1 Level AA合规性
- 色彩对比度检查
- 键盘导航支持
- 屏幕阅读器兼容性
[附上设计稿]
```

**Visual Hierarchy Review:**
```
分析这个首页的视觉层次：
- 用户视线流向（F型或Z型）
- 视觉权重分配是否合理
- 关键CTA是否突出
- 留白使用是否恰当
```

---

## Further Reading

- **Books:**
  - "Don't Make Me Think" by Steve Krug
  - "The Design of Everyday Things" by Don Norman
  - "Designing Interfaces" by Jenifer Tidwell

- **Online Resources:**
  - Nielsen Norman Group (nngroup.com)
  - Material Design Guidelines
  - Apple HIG
  - WCAG 2.1 Specification

- **Related Skills:**
  - [design-workflow.md](./design-workflow.md) - Complete design process
  - [multimodal-tips.md](./multimodal-tips.md) - Gemini image analysis
  - [examples/design-review.md](../examples/design-review.md) - Design critique examples
