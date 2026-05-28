# BRAND.md Full Template

Use this template when generating BRAND.md files.

---

# [Project Name] Brand Guidelines

## Brand Personality

### Character Description
[2-3 sentences describing the brand's personality as if it were a person]

### Brand Attributes
| Attribute | Description |
|-----------|-------------|
| [Attribute 1] | [How this manifests in design/communication] |
| [Attribute 2] | [How this manifests] |
| [Attribute 3] | [How this manifests] |

### Brand Spectrum
- Modern ←――――●―――――→ Classic
- Minimal ←――――●―――――→ Bold
- Professional ←――●―――――→ Playful
- Serious ←―――――●――――→ Friendly

## Color Palette

### Primary Colors
| Role | Name | Hex | HSL | RGB | Usage |
|------|------|-----|-----|-----|-------|
| Primary 50 | [Name] | #[HEX] | hsl(H, S%, L%) | rgb(R,G,B) | Lightest background |
| Primary 100 | [Name] | #[HEX] | hsl(H, S%, L%) | rgb(R,G,B) | Light background |
| Primary 200 | [Name] | #[HEX] | hsl(H, S%, L%) | rgb(R,G,B) | Light accent |
| Primary 300 | [Name] | #[HEX] | hsl(H, S%, L%) | rgb(R,G,B) | Border color |
| Primary 400 | [Name] | #[HEX] | hsl(H, S%, L%) | rgb(R,G,B) | Disabled state |
| Primary 500 | [Name] | #[HEX] | hsl(H, S%, L%) | rgb(R,G,B) | Primary (buttons, links) |
| Primary 600 | [Name] | #[HEX] | hsl(H, S%, L%) | rgb(R,G,B) | Hover state |
| Primary 700 | [Name] | #[HEX] | hsl(H, S%, L%) | rgb(R,G,B) | Active state |
| Primary 800 | [Name] | #[HEX] | hsl(H, S%, L%) | rgb(R,G,B) | Dark accent |
| Primary 900 | [Name] | #[HEX] | hsl(H, S%, L%) | rgb(R,G,B) | Darkest |

### Neutral Colors
| Role | Hex | Usage |
|------|-----|-------|
| Gray 50 | #[HEX] | Page background |
| Gray 100 | #[HEX] | Card background |
| Gray 200 | #[HEX] | Dividers |
| Gray 300 | #[HEX] | Borders |
| Gray 400 | #[HEX] | Placeholder text |
| Gray 500 | #[HEX] | Secondary text |
| Gray 600 | #[HEX] | Muted text |
| Gray 700 | #[HEX] | Body text |
| Gray 800 | #[HEX] | Headings |
| Gray 900 | #[HEX] | Dark text |

### Semantic Colors
| Role | Light | Base | Dark | Usage |
|------|-------|------|------|-------|
| Success | #[HEX] | #[HEX] | #[HEX] | Positive actions, confirmations |
| Warning | #[HEX] | #[HEX] | #[HEX] | Warnings, cautions |
| Error | #[HEX] | #[HEX] | #[HEX] | Errors, destructive actions |
| Info | #[HEX] | #[HEX] | #[HEX] | Information, tips |

### Color Accessibility
- All text must meet WCAG 2.1 AA contrast requirements
- Primary 500 on white: [Contrast ratio]
- Gray 700 on white: [Contrast ratio]

## Typography

### Font Stack
```css
--font-heading: '[Heading Font]', system-ui, sans-serif;
--font-body: '[Body Font]', system-ui, sans-serif;
--font-mono: '[Mono Font]', ui-monospace, monospace;
```

### Type Scale
| Name | Size | Line Height | Weight | Letter Spacing | Use |
|------|------|-------------|--------|----------------|-----|
| Display | 60px | 1.1 | 700 | -0.02em | Hero headings |
| H1 | 48px | 1.1 | 700 | -0.02em | Page titles |
| H2 | 36px | 1.2 | 600 | -0.01em | Section titles |
| H3 | 24px | 1.3 | 600 | 0 | Subsection titles |
| H4 | 20px | 1.4 | 600 | 0 | Card titles |
| H5 | 18px | 1.4 | 600 | 0 | Small headings |
| Body Large | 18px | 1.6 | 400 | 0 | Lead paragraphs |
| Body | 16px | 1.5 | 400 | 0 | Default text |
| Body Small | 14px | 1.5 | 400 | 0 | Secondary text |
| Caption | 12px | 1.4 | 400 | 0.01em | Labels, meta |
| Overline | 12px | 1.4 | 600 | 0.05em | Category labels |

### Font Weights
| Weight | Value | Usage |
|--------|-------|-------|
| Regular | 400 | Body text |
| Medium | 500 | Subtle emphasis, buttons |
| Semibold | 600 | Headings, labels |
| Bold | 700 | Strong emphasis |

## Tone of Voice

### Personality in Writing
[Description of how the brand communicates]

### Voice Characteristics
| Characteristic | Description | Example |
|----------------|-------------|---------|
| [Trait 1] | [Description] | "[Example sentence]" |
| [Trait 2] | [Description] | "[Example sentence]" |

### Do
- [Writing guideline 1]
- [Writing guideline 2]
- [Writing guideline 3]

### Don't
- [Anti-pattern 1]
- [Anti-pattern 2]
- [Anti-pattern 3]

### Example Copy
| Context | Example |
|---------|---------|
| Button | [Example] |
| Error message | [Example] |
| Success message | [Example] |
| Empty state | [Example] |

## Spacing System

### 4px Grid
| Token | Value | Tailwind | Usage |
|-------|-------|----------|-------|
| 0 | 0 | p-0 | None |
| px | 1px | p-px | Borders |
| 0.5 | 2px | p-0.5 | Micro |
| 1 | 4px | p-1 | Tight |
| 2 | 8px | p-2 | Small gaps |
| 3 | 12px | p-3 | Compact |
| 4 | 16px | p-4 | Default |
| 5 | 20px | p-5 | Comfortable |
| 6 | 24px | p-6 | Section gaps |
| 8 | 32px | p-8 | Large gaps |
| 10 | 40px | p-10 | Extra large |
| 12 | 48px | p-12 | Major separation |
| 16 | 64px | p-16 | Hero spacing |

### Component Spacing Guidelines
| Component | Padding | Gap |
|-----------|---------|-----|
| Button | 8px 16px | - |
| Card | 16px-24px | - |
| Form field | 12px 16px | 8px |
| Section | 48px-64px | 24px |

## Shadow Scale

| Level | CSS Value | Usage |
|-------|-----------|-------|
| xs | 0 1px 2px 0 rgb(0 0 0 / 0.05) | Subtle elevation |
| sm | 0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1) | Buttons, inputs |
| md | 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1) | Cards |
| lg | 0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1) | Dropdowns |
| xl | 0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1) | Modals |
| 2xl | 0 25px 50px -12px rgb(0 0 0 / 0.25) | Hero elements |

## Border Radius

| Size | Value | Usage |
|------|-------|-------|
| none | 0 | Sharp edges |
| sm | 4px | Small elements |
| md | 6px | Default (buttons, inputs) |
| lg | 8px | Cards |
| xl | 12px | Large cards |
| 2xl | 16px | Modals |
| full | 9999px | Pills, avatars |

## Iconography

### Style
- [Outline/Filled/Duotone]
- Stroke width: [Value]
- Size: [Default size]

### Icon Set
- Recommended: [Icon library name]
- Fallback: [Alternative]

## Animation

### Timing
| Type | Duration | Easing |
|------|----------|--------|
| Micro | 100ms | ease-out |
| Small | 150ms | ease-out |
| Medium | 200ms | ease-in-out |
| Large | 300ms | ease-in-out |
| Page | 400ms | ease-in-out |

### Principles
- Use motion purposefully
- Keep animations subtle
- Respect reduced motion preferences

---
*Generated with /brand-guide on [DATE]*
*Reference: PROJECT.md*
