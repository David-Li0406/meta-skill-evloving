---
name: idea-writer
description: Create new "idea" entries - product/service concepts with marketing flair. Use when the user says "add an idea", "new idea", "write an idea", or mentions wanting to capture a product or service concept.
allowed-tools:
  - Write
  - Read
  - Bash
---

# Idea Writer

This skill creates new "idea" entries - structured product/service concepts with a Mad Men inspired advertising aesthetic. Ideas are rendered with a distinctive "FREE IDEA!" badge and category-specific color schemes.

## File Location

Create new ideas in: `src/content/idea/`

## Filename Format

Use descriptive kebab-case filenames (no specific date format required).

Examples: `agent-dash.md`, `newsletter-optimizer.md`, `api-gateway.md`

## Frontmatter Schema

```yaml
---
title: "Product or Service Name"  # required, max 80 characters
subtitle: "Brief description"     # optional, max 120 characters
date: YYYY-MM-DD                  # required
category: "product"               # optional: product, service, campaign, strategy, innovation
draft: false                      # optional, defaults to false
author: Nikola Balić              # optional, defaults to Nikola Balić
---
```

**Field details:**
- `title`: Required, max 80 characters. Use quotes.
- `date`: Required, YYYY-MM-DD format.
- `subtitle`: Optional, max 120 characters. Use quotes.
- `category`: Optional enum value for color scheme styling.
- `draft`: Optional, defaults to false.
- `author`: Optional, defaults to "Nikola Balić".

## Categories

Ideas support 5 category types, each with a distinct color scheme:

| Category | Use for | Example |
|----------|---------|---------|
| `product` | Software, hardware, tools, platforms | AI Agents Dashboard |
| `service` | Consulting, maintenance, support, hosting | DevOps Advisory |
| `campaign` | Marketing initiatives, launches, promotions | "AI for Everyone" |
| `strategy` | Business models, partnerships, frameworks | API-First Design |
| `innovation` | Research, experimental concepts, moonshots | Quantum-Enhanced LLMs |

## Content Style Guidelines

Ideas use a marketing-oriented pitch style:

1. **Lead with the value proposition** - Start with "Simplify/Streamline/Transform..." and bold the product name
2. **Include a tagline** - Add a memorable quote in italics: *"Tagline here."*
3. **Link to technologies** - Reference relevant tools, frameworks, or services with markdown links
4. **Define the target market** - End with a "**Target market:**" section

## Example

**File:** `src/content/idea/agent-dash.md`

```markdown
---
title: "AI Agents Dashboard"
subtitle: "A web UI for deploying and managing AI agents in containers"
date: 2025-06-06
category: "product"
draft: false
---

Simplify AI operations with **AI Agents Dashboard**—a single web interface that combines [container-use](https://github.com/dagger/container-use), [Coder AgentAPI](https://github.com/coder/agentapi), and [Claude](https://www.anthropic.com/claude-code). Launch a primary agent instance from the dashboard, which then spins up additional isolated agent environments in containers. Monitor resource usage, health, and logs in real time, and start, stop, or scale any agent without using the command line.

*"Orchestrate AI at scale, one container at a time."*

**Target market:**
DevOps teams, AI researchers, and software engineers who need an easy way to deploy, observe, and control multiple Claude agents within containerized workflows.
```

## When to Use Ideas vs Other Content Types

| Type | When to use | Format |
|------|-------------|--------|
| **Idea** | Product/service concept with marketing flair | Structured frontmatter, pitch style |
| **Thought** | Quick insight, observation, philosophical reflection | Minimal frontmatter, blockquote style |
| **Now Entry** | Life update with multiple focus areas | YYMMDD.md, ## sections |
| **Article** | Full blog post with narrative/technical depth | Complete frontmatter (tags, topics, etc.) |

## How It Works

- Ideas appear on the homepage (`/`) in the main feed
- Rendered with Mad Men inspired advertising aesthetic
- "FREE IDEA!" badge displayed in header
- Category-specific color schemes and gradients
- Integrated with search at `/search`

## Process

When the user wants to add an idea:

1. **Gather the concept**: What problem does it solve? What's the value proposition?
2. **Choose a category**: product, service, campaign, strategy, or innovation
3. **Write the frontmatter**:
   - Title (max 80 chars)
   - Subtitle (optional, max 120 chars)
   - Category
   - Today's date
4. **Draft the content** following the style guidelines:
   - Lead paragraph with bolded product name
   - Technology links where relevant
   - Tagline in italics
   - Target market section
5. **Choose a filename** using descriptive kebab-case
6. **Create the file** in `src/content/idea/`
7. **Confirm creation** with the user
