---
name: conference-talk-builder
description: Use this skill when you need to create structured conference talk outlines and iA Presenter markdown slides using the Story Circle narrative framework.
---

# Conference Talk Builder

This skill helps create compelling conference talk outlines and iA Presenter markdown slides using the Story Circle narrative framework.

## Process

Follow these steps in order when building a conference talk:

### 1. Gather Information

Ask the user for:
- Talk title and topic
- Target audience and their expected knowledge level
- Main points they want to cover
- Brain dump of everything they know about the topic
- Problem they're solving or story they're telling
- Any constraints (time limit, specific technologies, etc.)

### 2. Read the Story Circle Framework

Load `references/story-circle.md` to understand the eight-step narrative structure. The framework maps tech talks to:
- Top half: Established practices and order
- Bottom half: Disruption and experimentation

### 3. Create the Outline

Structure the talk using the eight Story Circle steps:

1. **Introduction** - Current status quo
2. **Problem Statement** - What needs solving
3. **Exploration** - Initial attempts
4. **Experimentation** - Deep investigation
5. **Solution** - The breakthrough
6. **Challenges** - Implementation difficulties
7. **Apply Knowledge** - Integration into project
8. **Results & Insights** - Lessons learned

Map the user's content to these steps. Show this outline to the user and refine based on feedback.

### 4. Generate iA Presenter Slides

Read `references/ia-presenter-syntax.md` for markdown formatting rules. Create slides that:
- Use `---` to separate slides
- Add tabs (`⇥`) before content that should be visible on slides
- Leave speaker notes without tabs (spoken text only)
- Include comments with `//` for reminders
- Format code blocks with proper syntax highlighting
- Keep slides focused on one concept each

Structure the slide deck:
- Title slide
- Introduction slide with your photo/bio
- One or more slides per Story Circle step
- Code examples broken across multiple slides for readability
- Closing slide with contact info and resources

### 5. Refine and Iterate

After showing the slides:
- Ask if sections need expansion or compression
- Check if code examples need better formatting
- Verify the story flow makes sense
- Adjust based on user feedback

## Key Principles

- **Tell a Story**: Focus on how you approached a problem and solved it.
- **Keep It Readable**: Break code across slides. Test on bad projectors.
- **Engage the Audience**: Use humor where appropriate. Ask questions.
- **Make Follow-up Easy**: Include memorable URL or QR code linking to resources.