# Copywriting: Voice & Tone Guidelines

When generating text for SpecsVibeCode, adhere to this brand persona to maintain consistency across all user-facing content.

## Brand Personality Keywords

* **Professional yet approachable** - We're experts, but not intimidating
* **Efficient and direct** - Respect users' time; get to the point
* **Technical but clear** - Use proper terminology without unnecessary jargon
* **Empathetic and supportive** - Understand developer pain points
* **Confident without arrogance** - We know our product works; we don't need to oversell

## Core Voice Attributes

### 1. Professional
We're a serious tool for serious work. Avoid:
- Excessive casualness or slang
- Emoji in core UI (acceptable in marketing materials only)
- Cutesy language or attempts to be "fun"
- Over-enthusiasm or hype

### 2. Clear
Technical users value precision. Always:
- Use concrete, specific language
- Prefer short sentences (15-20 words max)
- Define technical terms on first use
- Front-load important information

### 3. Helpful
We're here to make spec writing easier. Show this by:
- Anticipating user questions
- Providing context for actions
- Offering solutions, not just problems
- Using positive framing

## Grammar & Mechanics Rules

### Capitalization
* **Headings (H1, H2):** Title Case - "Generate Your First Specification"
* **Subheadings (H3+):** Sentence case - "How to export documents"
* **Buttons:** Title Case for primary actions, sentence case for secondary
* **Form labels:** Sentence case with colon - "Project name:"
* **Error messages:** Sentence case, end with period

### Punctuation
* **Periods:** Use for complete sentences, even in short UI messages
* **Exclamation points:** Avoid in interface copy; reserve for genuine excitement in marketing
* **Commas:** Use serial comma (Oxford comma)
* **Ellipsis:** Use `…` (single character) not `...` (three periods)

### Formatting
* **Bold:** For emphasis on key actions or important terms
* **Italics:** For technical terms on first use or subtle emphasis
* **Code blocks:** For anything the user might type or see in code
* **Links:** Make link text descriptive; avoid "click here"

### Active vs Passive Voice
* **Prefer active:** "We generated your specification" over "Your specification was generated"
* **Exceptions:** Error messages where the system is at fault - "The document could not be saved"

## Terminology Guide

Use consistent terms throughout the product:

| ✅ Use This | ❌ Not This | Context |
|------------|-------------|---------|
| specification | spec, document | Primary product output |
| project | workspace, folder | Organizational unit |
| generate | create, make, produce | AI creation action |
| credit | token, point, unit | Usage currency |
| plan | tier, subscription | Billing level |
| export | download, save | Document output |
| sign in | login, log in | Authentication |
| sign out | logout, log out | Authentication |
| set up | setup (noun only) | Configuration process |

### Word Choice Preferences

| ❌ Avoid | ✅ Use Instead | Reason |
|---------|---------------|--------|
| utilize | use | Simpler |
| in order to | to | Concise |
| at this point in time | now | Direct |
| leverage | use, apply | Less buzzwordy |
| paradigm | model, approach | Less jargony |
| robust | reliable, comprehensive | Overused |
| innovative | (describe the actual benefit) | Empty marketing speak |

## Message Types

### Success Messages
**Pattern:** `[Action completed]. [Next step or benefit].`

```
✅ Good: "Project created. Start generating your specification."
❌ Bad: "Yay! Your project was successfully created!"
```

### Error Messages
**Pattern:** `[What happened]. [Why it happened]. [How to fix it].`

```
✅ Good: "Unable to generate specification. You've reached your monthly credit limit. Upgrade your plan or wait until next month."
❌ Bad: "Error 403: Insufficient credits."
```

### Empty States
**Pattern:** `[What's missing]. [Why it matters]. [How to fix it].`

```
✅ Good: "No projects yet. Projects organize your specifications and make them easy to find. Create your first project to get started."
❌ Bad: "Nothing to see here! 🎉"
```

### Confirmation Dialogs
**Pattern:** `[What will happen]. [Consequence]. [Confirm action]?`

```
✅ Good: "Delete project 'Mobile App'? All specifications will be permanently removed. This cannot be undone."
❌ Bad: "Are you sure you want to delete this project?"
```

### Loading States
**Pattern:** `[Present progressive verb]...` (short, no period)

```
✅ Good: "Generating specification..."
✅ Good: "Analyzing requirements..."
❌ Bad: "Please wait while we process your request..."
```

## Context-Specific Guidelines

### Marketing Pages
* More conversational than in-app copy
* Can use questions to engage readers
* Focus on benefits, not just features
* Use customer language, not internal terminology

### Documentation
* Task-oriented headings ("How to export a specification")
* Step-by-step instructions with numbered lists
* Include prerequisites at the top
* End with related resources

### Email Communications
* Subject line: Clear, specific, under 50 characters
* Preview text: Complements subject, doesn't repeat it
* Body: Short paragraphs (2-3 sentences)
* CTA: One primary action per email

### Error/System Messages
* Never blame the user
* Be specific about what went wrong
* Always provide a path forward
* Technical details should be collapsible/expandable

## Examples by UI Component

### Button Text
```erb
<!-- Primary actions -->
<button>Generate Specification</button>
<button>Save Changes</button>
<button>Create Project</button>

<!-- Secondary actions -->
<button>Cancel</button>
<button>Go back</button>
<button>Learn more</button>

<!-- Destructive actions -->
<button>Delete Project</button>
<button>Remove Access</button>
```

### Form Labels
```erb
<!-- Direct, sentence case -->
<label>Project name:</label>
<label>Specification type:</label>
<label>Target audience:</label>

<!-- With helper text -->
<label>
  API endpoint:
  <span>The base URL for your API (e.g., https://api.example.com)</span>
</label>
```

### Placeholder Text
```erb
<!-- Provide examples, not instructions -->
<input placeholder="e.g., Mobile Banking App">
<input placeholder="e.g., iOS developers">
<input placeholder="https://api.example.com">

❌ Bad: <input placeholder="Enter your project name here">
```

### Navigation/Menu Items
```
Dashboard
Projects
Specifications
Settings
Billing
Sign Out
```

## Brand Differentiators in Copy

When writing about SpecsVibeCode, emphasize:

1. **Speed:** "Generate comprehensive specs in minutes, not days"
2. **Quality:** "AI-powered analysis ensures nothing is missed"
3. **Flexibility:** "Export to any format your team needs"
4. **Developer-friendly:** "Built by developers, for developers"

Avoid claiming:
- "Revolutionary" or "game-changing"
- "Best" or "perfect" (use "comprehensive," "reliable")
- Feature parity with competitors
- Absolute guarantees ("never miss a requirement")
