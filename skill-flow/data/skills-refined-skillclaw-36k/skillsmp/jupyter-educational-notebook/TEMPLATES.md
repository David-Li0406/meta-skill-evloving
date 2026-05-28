# Notebook Templates

Ready-to-use templates for creating educational Jupyter notebooks. Copy and adapt these patterns for your needs.

## Auto-Wrapping vs Manual HTML Styling

**NEW:** When displaying notebooks in **notebook mode** (`| IPynb Viewer (notebook) |`), you can write **pure markdown** without HTML wrappers! The viewer automatically detects cell types and applies styling.

**Choose your approach:**

1. **Auto-Wrapping (Pure Markdown)** - 90% less code, notebook mode only
2. **Manual HTML Styling** - Full control, works in all display modes
3. **Hybrid Approach** - Mix both in the same notebook

All templates below show **manual HTML styling**. For auto-wrapping, simply write pure markdown and the viewer handles styling automatically in notebook mode.

**Auto-Wrapping Example:**
```markdown
# 🎯 Tutorial Title

**Compelling tagline** with additional context

## What You'll Learn

Key concepts and outcomes
```

**Hybrid Example:**
```markdown
<!-- Most cells: pure markdown (auto-wrapped) -->
# Tutorial Title

Regular content here...

<!-- Special cell: custom HTML for emphasis -->
<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 12px; padding: 48px; margin: 0; text-align: center; color: white;">

<h2 style="font-size: 36px; font-weight: 800; margin: 0;">🎯 Key Takeaway</h2>

<p style="font-size: 20px;">Custom styling for this important message</p>

</div>
```

**See Also:**
- SKILL.md for complete auto-wrapping documentation
- create-notebook.md command for guided creation

## Table of Contents

- [Navigation Template](#navigation-template) - **NEW!** Multi-paradigm documentation navigation
- [Blog Post Template](#blog-post-template)
- [Tutorial Template](#tutorial-template)
- [Concept Explanation Template](#concept-explanation-template)
- [Reference Guide Template](#reference-guide-template)
- [Quick Demo Template](#quick-demo-template)

---

## Navigation Template

**Use for:** Complex documentation systems (20+ documents) with multiple audiences

**Estimated cells:** 30-40
**Content ratio:** 100% markdown (pure navigation, no code)

### When to Use

✅ **Perfect for:**
- Documenting complex systems (20+ documents)
- Multiple distinct audiences (4+ roles)
- Documentation hubs and learning path systems
- Teaching documentation architecture patterns

❌ **Skip for:**
- Simple documentation (< 10 documents)
- Single-audience documentation
- Linear learning paths
- Quick reference guides

### Template Location

**File:** `docs/for-ai/templates/ipynb/navigation-template.ipynb`

**Real Example:** `docs-navigation.ipynb` (65 cells navigating 26 documents)

### Key Features

1. **Multi-Paradigm Navigation:**
   - Role-based: "I'm a Developer/Architect/PM"
   - Task-based: "I need to build/test X"
   - Workflow-based: "I'm in the planning/testing phase"
   - Category-based: "Browse all implementation docs"

2. **Progressive Disclosure:**
   - Hero cell with main action cards
   - Table of Contents with time estimates
   - Emergency navigation for urgent problems
   - Part summaries with forward momentum

3. **Navigational Aids:**
   - Progress indicators (🔵🔵🔵⚪⚪⚪)
   - Reading time estimates per part
   - Essential bookmarks highlight
   - Search keywords guide
   - Icon legend
   - Troubleshooting section

4. **Living Documentation Principles:**
   - Self-verification (action cards validate headings)
   - Multi-audience design (6+ distinct roles)
   - Multi-modal navigation (4 ways to find info)
   - Executable truth (validated structure)

### Structure

```
Cell 1: Hero - Title with main action cards
Cell 2: TOC - Complete overview with time estimates
Cell 3: Emergency - Quick fix matrix (problem → solution)
Cell 4: Essential - The 3 must-read docs highlighted
Cell 5: Search - Keywords guide for finding info
Cell 6: Icon Legend - Emoji meanings explained

Part 1: Overview
- Big picture (documentation ecosystem)
- Living documentation principles
- Navigation strategies
- Summary card with next steps

Part 2: By Role (6 roles)
- New Developer
- Experienced Developer
- Architect/Tech Lead
- Project Manager
- Content Creator
- Each with Required/Recommended/Optional docs
- Summary card

Part 3: By Task (6 tasks)
- Building simple components
- Building complex components
- Testing components
- Debugging issues
- Creating educational content
- Creating presentations
- Summary card

Part 4: By Workflow (5 phases)
- Planning
- Development
- Testing
- Documentation
- Deployment
- Summary card

Part 5: By Category (6 categories)
- Core Navigation
- Implementation Guides
- Testing & Debugging
- Jupyter Notebooks
- Project Guidelines
- Reference Materials
- Summary card

Part 6: Pro Tips (11 tips)
- Use Navigation Flows
- Use Relationship Mapping
- Start with Getting Started
- EDS.md is Your Bible
- Know the Dual-Pattern
- Master Three Notebook Types
- Use Templates
- Build Personal Quick Reference
- Use Slash Commands
- Follow Decision Trees
- Leverage AI for Documentation
- Summary card

Part 7: Universal Patterns
- Beyond this project
- Concrete examples (Component Libraries, APIs)
- How to apply this template
- 5-step adaptation guide

Final: Troubleshooting & Remember
- 6 common navigation issues with solutions
- Living documentation reflection
```

### Metadata Example

```json
{
  "metadata": {
    "title": "[Your System] Documentation Navigator",
    "description": "Your documentation GPS for navigating [N] documents across [M] categories",
    "author": "Your Name",
    "date": "2025-01-20",
    "version": "1.0",
    "category": "navigation",
    "difficulty": "beginner",
    "duration": "15-20 minutes",
    "tags": ["navigation", "documentation", "multi-paradigm", "living-docs"],
    "license": "MIT"
  }
}
```

### Quick Start

**Copy the template:**
```bash
cp docs/for-ai/templates/ipynb/navigation-template.ipynb my-docs-nav.ipynb
```

**Customize for your system:**
1. Define your documentation domains and categories
2. Identify 4-6 distinct user roles
3. Map 5-8 common tasks
4. Define your workflow phases (typically 4-6)
5. Customize parts and action cards
6. Add role-specific learning paths
7. Create task-specific quick references
8. Add pro tips relevant to your system

### Action Cards Pattern

Navigation templates heavily use action cards for smart linking:

```markdown
# 🗺️ Your Documentation Navigator

Choose your navigation style:

<!-- action-cards -->

- [Navigate by Role](#)
- [Navigate by Task](#)
- [Navigate by Workflow](#)
- [Browse Categories](#)
```

Action cards automatically resolve to matching headings at runtime - no hardcoded IDs needed!

### Summary Headings (Important!)

**Avoid smart linking conflicts:**
- ❌ Don't: `### ✅ Part 1 Complete: The Big Picture`
- ✅ Do: `### ✅ You've Completed Part 1`

Summary headings should be distinct from actual part headings to avoid confusing the smart link resolver.

### See Also

- [docs/for-ai/templates/ipynb/README.md](../../../docs/for-ai/templates/ipynb/README.md) - Complete template catalog
- [docs/for-ai/document-relationship-mapping.md](../../../docs/for-ai/document-relationship-mapping.md) - Cross-reference strategy
- [docs/for-ai/navigation-flows.md](../../../docs/for-ai/navigation-flows.md) - Decision trees
- [docs-navigation.ipynb](../../../../docs-navigation.ipynb) - Real-world example (65 cells, 26 docs)

---

## Blog Post Template

**Use for:** Engaging content with demonstrations, optimized for shareability

**Estimated cells:** 30-45
**Content ratio:** 65% markdown / 35% code

### Metadata (Required)

```json
{
  "metadata": {
    "title": "Your Engaging Blog Title",
    "description": "One-line summary that hooks readers",
    "author": "Your Name",
    "date": "2025-01-17",
    "version": "1.0",
    "category": "blog",
    "difficulty": "beginner",
    "duration": "20 minutes",
    "tags": ["blog", "tutorial", "interactive", "javascript"],
    "license": "MIT"
  }
}
```

### Cell 1: Header (Markdown)

```markdown
# 📓 [Your Title Here]

Welcome to this **interactive [type of content]**! [Brief hook explaining what makes this special].

## What is [Topic]?

[2-3 sentence explanation of the topic]

The **[main thing]** allows you to:

📝 [Benefit 1]
▶️ [Benefit 2]
🎨 [Benefit 3]
📚 [Benefit 4]
🎓 [Benefit 5]

## Why [This Approach]?

Traditional [old way] is **[problem]** - [explain the pain point].

Interactive [your solution] lets you:

✅ **[Benefit 1]** - [Short description]
✅ **[Benefit 2]** - [Short description]
✅ **[Benefit 3]** - [Short description]
✅ **[Benefit 4]** - [Short description]

## How to Use This [Post/Guide/Tutorial]

**Read the markdown cells** for explanations
**Click "Run" on code cells** to execute
**See results inline** below each cell
**[Additional instruction]**
**[Additional instruction]**

Let's get started! 🚀
```

### Cell 2: Table of Contents (Markdown)

```markdown
## 📋 Table of Contents

[Part 1: Introduction](#part-1)
[Part 2: [Topic]](#part-2)
[Part 3: [Topic]](#part-3)
[Part 4: [Topic]](#part-4)
[Part 5: [Topic]](#part-5)
[Part 6: [Topic]](#part-6)
[Resources & Next Steps](#resources)
```

### Cell 3: Part 1 Introduction (Markdown)

```markdown
## 🚀 Part 1: [Section Title]

[Paragraph explaining this section]

### [Subsection Title]

[Explanation with context]

**Key points:**
- [Point 1]
- [Point 2]
- [Point 3]

[Transition to code example]
```

### Cell 4: First Code Example (Code)

```javascript
// [Clear description of what this demonstrates]
const [variable] = '[value]';
const [another] = new Date().toLocaleDateString();

console.log('[descriptive message]:', [variable]);
console.log('[another message]:', [another]);

return `[formatted result with ${variable} and ${another}]`;
```

### Cell 5: Explanation (Markdown)

```markdown
### 💡 What Just Happened?

When you clicked "Run":
✅ [What happened step 1]
✅ [What happened step 2]
✅ [What happened step 3]

**Key insight:** [Important takeaway]
```

### Cell 6: Part 2 Advanced (Markdown)

```markdown
## 🧪 Part 2: [Advanced Topic]

[Introduction to more complex material]

### [Subsection]

[Explanation with details]

Let's see this in action:
```

### Cell 7: Advanced Code (Code)

```javascript
// Import helpers when needed
const { [helper1], [helper2] } = await import('/scripts/[helpers].js');

// Create content
const content = `
  [your content structure here]
`;

// Use the helper
const result = await [helper1]('[blockname]', content);

console.log('✓ [Success message]');
console.log('[Details]:', result.[property]);

return result.[output];
```

### Cell 8: Best Practices (Markdown)

```markdown
## ✅ Part [N]: Best Practices & Next Steps

[Summary paragraph]

### Quick Reference

| [Column 1] | [Column 2] | [Column 3] |
|------------|------------|------------|
| [Item 1] | [Description] | [Value] |
| [Item 2] | [Description] | [Value] |
| [Item 3] | [Description] | [Value] |

### Best Practices Checklist

✅ **[Practice 1]** - [Description]
✅ **[Practice 2]** - [Description]
✅ **[Practice 3]** - [Description]
✅ **[Practice 4]** - [Description]

### What You Learned

[Recap in bullet points]

### Next Steps

1. **[Action 1]** - [Description]
2. **[Action 2]** - [Description]
3. **[Action 3]** - [Description]
```

### Cell 9: Call-to-Action (Markdown)

```markdown
## 📞 Get in Touch

**[Your Company Name]** [brief description of services]

### Contact

📧 **Email**: [email@example.com](mailto:email@example.com)
🌐 **Website**: [https://example.com](https://example.com)
👤 **LinkedIn**: [Your Profile](#)

---

[Closing statement about your passion/mission]
```

---

## Tutorial Template

**Use for:** Step-by-step learning with exercises

**Estimated cells:** 20-30
**Content ratio:** 70% markdown / 30% code

### Metadata (Required)

```json
{
  "metadata": {
    "title": "Tutorial: Master [Your Topic]",
    "description": "Step-by-step guide to learning [topic] with hands-on exercises",
    "author": "Your Name",
    "date": "2025-01-17",
    "version": "1.0",
    "category": "tutorial",
    "difficulty": "intermediate",
    "duration": "45 minutes",
    "tags": ["tutorial", "learning", "hands-on", "javascript"],
    "license": "MIT"
  }
}
```

### Cell 1: Tutorial Header (Markdown)

```markdown
# 🎓 Tutorial: [Learning Objective]

Welcome to this hands-on tutorial! By the end, you'll [understand/be able to do X, Y, Z].

## What You'll Learn

- [Learning objective 1]
- [Learning objective 2]
- [Learning objective 3]
- [Learning objective 4]

## Prerequisites

- [Prerequisite 1]
- [Prerequisite 2]
- [Prerequisite 3]

## Estimated Time

⏱️ [XX-XX] minutes

## Table of Contents

[Part 1: Foundation](#part-1)
[Part 2: Building](#part-2)
[Part 3: Testing](#part-3)
[Part 4: Advanced](#part-4)
[Summary](#summary)
```

### Cell 2: Part 1 Foundation (Markdown)

```markdown
## 📚 Part 1: [Foundation Topic]

Before we start building, let's understand [the basics].

### What is [Concept]?

[Definition and explanation]

**Example:** [Simple concrete example]

### [Key Concept]

[Explanation with details]

**Key components:**
- [Component 1] - [Description]
- [Component 2] - [Description]
- [Component 3] - [Description]

Let's see an example...
```

### Cell 3: Foundation Example (Code)

```javascript
// 🎯 Example 1: [Concept Name]
// Instructions: Run this cell to see [what it demonstrates]

[code demonstrating the concept]

console.log('✓ [Success message]');
console.log('[Details]:', [variable]);

// ✏️ Try This: [Suggestion for experimentation]

return [result];
```

### Cell 4: Exercise (Markdown)

```markdown
### 🎯 Exercise 1: [Exercise Name]

**Goal:** [What the learner should accomplish]

**Instructions:**
1. [Step 1]
2. [Step 2]
3. [Step 3]

**Expected result:** [What should happen]

Run the cell below to see the solution:
```

### Cell 5: Exercise Solution (Code)

```javascript
// Exercise 1 Solution

[solution code with comments]

// Explanation: [Why this works]

return '✓ [Completion message]';
```

### Cell 6: Part 2 Building (Markdown)

```markdown
## 🔨 Part 2: [Building Something]

Now that you understand [the basics], let's [build/create/implement] [something].

### Step 1: [First Step]

[Explanation of what to do and why]

**Our goal:** [What we're trying to achieve]

### Step 2: [Second Step]

[Instructions and context]
```

### Cell 7: Incremental Build (Code)

```javascript
// Step 2 Implementation: [What this builds]

[code showing incremental progress]

console.log('[Progress message]');

return '✓ [Step completed]';
```

### Cell 8: Part 3 Testing (Markdown)

```markdown
## 🧪 Part 3: Testing Your [Thing]

Let's test [what we built] with different scenarios.

### Test 1: [Simple Case]

First, test with [simple scenario]:
```

### Cell 9: Test Case (Code)

```javascript
// Test 1: [Test name]

[test code]

console.log('✓ Test 1 passed');

return [result];
```

### Cell 10: Summary (Markdown)

```markdown
## 🎉 Congratulations!

You've learned how to:
✅ [Skill 1]
✅ [Skill 2]
✅ [Skill 3]

### Next Steps

1. **[Next action 1]** - [Description]
2. **[Next action 2]** - [Description]
3. **[Next action 3]** - [Description]

### Resources

- [Resource 1 with link]
- [Resource 2 with link]
- [Resource 3 with link]

Keep practicing! 🚀
```

---

## Concept Explanation Template

**Use for:** Deep dive into a single topic

**Estimated cells:** 15-25
**Content ratio:** 55% markdown / 45% code

### Metadata (Required)

```json
{
  "metadata": {
    "title": "Understanding [Concept Name]",
    "description": "A comprehensive deep dive into [concept] and how it works",
    "author": "Your Name",
    "date": "2025-01-17",
    "version": "1.0",
    "category": "concept",
    "difficulty": "advanced",
    "duration": "30 minutes",
    "tags": ["concept", "deep-dive", "technical", "javascript"],
    "license": "MIT"
  }
}
```

### Cell 1: Concept Header (Markdown)

```markdown
# 🔍 Understanding [Concept Name]

A comprehensive guide to [what this is about].

## The Problem

[Describe the problem or challenge this concept addresses]

[Explain pain points of traditional approaches]

## The Solution

[Concept name] solves this by:
✅ [Benefit 1]
✅ [Benefit 2]
✅ [Benefit 3]

Let's explore how this works...

## Table of Contents

[How It Works](#how-it-works)
[Technical Details](#technical-details)
[Live Examples](#examples)
[Comparisons](#comparisons)
[Best Practices](#best-practices)
```

### Cell 2: How It Works (Markdown)

```markdown
## 🔧 How [Concept] Works

[Explain the mechanism step by step]

### Step 1: [First Step]

[Explanation]

### Step 2: [Second Step]

[Explanation]

### Step 3: [Third Step]

[Explanation]

Let's see each step in action...
```

### Cell 3: Before Example (Code)

```javascript
// BEFORE: [Traditional approach]

[code showing the old way]

console.log('Traditional approach:');
console.log([details]);

return '❌ [Problem with this approach]';
```

### Cell 4: After Example (Code)

```javascript
// AFTER: [New approach with concept]

[code showing the new way]

console.log('New approach:');
console.log([details]);

return '✅ [Benefits of new approach]';
```

### Cell 5: Comparison (Markdown)

```markdown
## ⚖️ [Old Way] vs [New Way]

| Aspect | [Old Way] | [New Way] |
|--------|-----------|-----------|
| **[Criteria 1]** | [Old value] | [New value] |
| **[Criteria 2]** | [Old value] | [New value] |
| **[Criteria 3]** | [Old value] | [New value] |

### When to Use Each

**[Old Way]:**
- [Scenario 1]
- [Scenario 2]

**[New Way]:**
- [Scenario 1]
- [Scenario 2]
```

### Cell 6: Technical Details (Markdown)

```markdown
## 🔬 Technical Details

### [Technical aspect 1]

[In-depth explanation]

**Key points:**
- [Point 1]
- [Point 2]

### [Technical aspect 2]

[In-depth explanation]
```

### Cell 7: Advanced Example (Code)

```javascript
// Advanced usage: [What this demonstrates]

[complex code example]

console.log('[Detailed output]');

return [result];
```

### Cell 8: Best Practices (Markdown)

```markdown
## ✅ Best Practices

### Do's

✅ **[Practice 1]** - [Why]
✅ **[Practice 2]** - [Why]
✅ **[Practice 3]** - [Why]

### Don'ts

❌ **[Anti-pattern 1]** - [Why not]
❌ **[Anti-pattern 2]** - [Why not]
❌ **[Anti-pattern 3]** - [Why not]

### Summary

[Concept] is powerful when:
- [Condition 1]
- [Condition 2]
- [Condition 3]

[Final thoughts]
```

---

## Reference Guide Template

**Use for:** Quick lookup documentation

**Estimated cells:** 25-40
**Content ratio:** 40% markdown / 60% code

### Metadata (Required)

```json
{
  "metadata": {
    "title": "[API/Library] Reference Guide",
    "description": "Complete reference documentation with examples and usage patterns",
    "author": "Your Name",
    "date": "2025-01-17",
    "version": "1.0",
    "category": "reference",
    "difficulty": "intermediate",
    "duration": "15 minutes",
    "tags": ["reference", "documentation", "api", "javascript"],
    "license": "MIT"
  }
}
```

### Cell 1: Reference Header (Markdown)

```markdown
# 📖 [API/Function/Library] Reference

Complete guide to [what this covers] with examples.

## Quick Reference

| [Item] | [Description] | [Signature/Details] |
|--------|---------------|---------------------|
| [Item 1] | [What it does] | [Details] |
| [Item 2] | [What it does] | [Details] |
| [Item 3] | [What it does] | [Details] |

## Usage Patterns

### Basic Import
```javascript
[import statement]
```

### Basic Usage
```javascript
[simple usage example]
```

---

## Table of Contents

[Function/Feature 1](#function-1)
[Function/Feature 2](#function-2)
[Function/Feature 3](#function-3)
[Error Handling](#errors)
[Performance](#performance)
```

### Cell 2: Function Documentation (Markdown)

```markdown
## 🔬 [Function Name]

**Signature:**
```javascript
[function signature with types]
```

**Parameters:**
- `[param1]` - [Description]
- `[param2]` - [Description]

**Returns:** [Return value description]

**Purpose:** [What this function does]

### Basic Usage
```

### Cell 3: Basic Example (Code)

```javascript
// Basic usage example

[simple code demonstrating basic usage]

return [result];
```

### Cell 4: Advanced Usage (Markdown)

```markdown
### With [Additional Feature]
```

### Cell 5: Advanced Example (Code)

```javascript
// Advanced usage with [feature]

[more complex code]

return [result];
```

### Cell 6: Error Handling (Markdown)

```markdown
### Error Handling
```

### Cell 7: Error Example (Code)

```javascript
// Error handling example

try {
  [code that might error]
  return '✓ Success';
} catch (error) {
  console.error('Error:', error.message);
  return '✗ Error: ' + error.message;
}
```

### Cell 8: Summary (Markdown)

```markdown
## 📚 Summary

### Common Patterns

**Pattern 1:**
```javascript
[common pattern code]
```

**Pattern 2:**
```javascript
[common pattern code]
```

### Quick Tips

💡 [Tip 1]
💡 [Tip 2]
💡 [Tip 3]

### Related Resources

- [Resource 1](#)
- [Resource 2](#)
- [Resource 3](#)
```

---

## Quick Demo Template

**Use for:** Showcasing capabilities quickly

**Estimated cells:** 15-20
**Content ratio:** 30% markdown / 70% code

### Metadata (Required)

```json
{
  "metadata": {
    "title": "[Thing] Interactive Demo",
    "description": "Quick interactive demonstration showcasing [thing] capabilities",
    "author": "Your Name",
    "date": "2025-01-17",
    "version": "1.0",
    "category": "demo",
    "difficulty": "beginner",
    "duration": "10 minutes",
    "tags": ["demo", "showcase", "interactive", "javascript"],
    "license": "MIT"
  }
}
```

### Cell 1: Demo Header (Markdown)

```markdown
# 🎨 [Thing] Interactive Demo

See what [thing] can do! Click "Run" on each cell to see live demonstrations.

## What You'll See

- [Demo 1]
- [Demo 2]
- [Demo 3]
- [Demo 4]

No explanation needed - just click and explore! 🚀
```

### Cell 2: Quick Demo 1 (Code)

```javascript
// Demo 1: [Name]

[short demo code]

return '✓ [Demo completed message]!';
```

### Cell 3: Quick Demo 2 (Code)

```javascript
// Demo 2: [Name]

[short demo code]

return '✓ [Demo completed message]!';
```

### Cell 4: Experimentation Prompt (Markdown)

```markdown
## 🎯 Try It Yourself

Want to experiment? Modify the content in the cells above and run them again!

**Ideas to try:**
- [Suggestion 1]
- [Suggestion 2]
- [Suggestion 3]
- [Suggestion 4]
```

### Cell 5: Customizable Demo (Code)

```javascript
// Customizable Demo
// Change the values below and run again!

const [variable1] = '[value]';
const [variable2] = '[value]';

[code using these variables]

return '✓ [Result]';
```

### Cell 6: Closing (Markdown)

```markdown
## 🎉 That's It!

You've seen:
✅ [What they saw 1]
✅ [What they saw 2]
✅ [What they saw 3]

### Want More?

- [Link to tutorial]
- [Link to documentation]
- [Link to examples]

Have fun! 🚀
```

---

## Usage Tips

### Choosing a Template

1. **Navigation** - Complex documentation systems (20+ docs, multiple audiences)
2. **Blog Post** - When you want to publish engaging content
3. **Tutorial** - When teaching step-by-step
4. **Concept Explanation** - When diving deep into one topic
5. **Reference Guide** - When documenting APIs or features
6. **Quick Demo** - When showcasing quickly

### Customizing Templates

- Replace `[placeholders]` with your content
- Adjust cell counts based on your needs
- Maintain the content ratio guidelines
- Keep the progressive disclosure pattern
- Add your own emojis and styling

### Styling Approach Decision

**For notebook mode (`| IPynb Viewer (notebook) |`):**
- ✅ **Recommended:** Use pure markdown (auto-wrapped) for 90% less code
- ✅ **Mix with custom HTML** for cells needing special styling
- ✅ Speed: Write content fast, customize selectively

**For other modes (paged, autorun, basic):**
- ✅ Use manual HTML styling (shown in templates above)
- ✅ Full design control across all display modes
- ✅ Professional polish and consistency

**Hybrid Approach Benefits:**
- Most cells: Pure markdown (fast authoring)
- Special cells: Custom HTML (unique styling)
- Best of both worlds: speed + flexibility

### Creating from Templates

1. Copy the template structure
2. **Choose styling approach** based on display mode
3. Fill in all placeholders
4. Add your specific content
5. Test all code cells
6. Verify markdown rendering
7. Adjust flow as needed

**Remember:**
- Templates show manual HTML styling for maximum compatibility
- In notebook mode, consider pure markdown for faster authoring
- Mix both approaches in the same notebook as needed
- Templates are starting points - adapt them to fit your specific needs!
