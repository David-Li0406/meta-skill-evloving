---
name: kenya-hara-white-design
description: Create refined, contemplative UI/UX designs inspired by Kenya Hara's philosophy of "White" (白) and Emptiness (空). Use this skill when building interfaces that embrace Japanese aesthetics of ma (間), yohaku (余白), and receptive simplicity. Ideal for creating meditative web applications, minimalist dashboards, product showcases, portfolios, landing pages, or any interface seeking profound simplicity that invites user interpretation rather than imposing meaning.
---

# Kenya Hara "White" Design Philosophy for UI/UX

This skill guides the creation of UI/UX designs based on Kenya Hara's philosophy articulated in his seminal work "白" (White). The approach transcends mere minimalism—it creates interfaces as receptive vessels that invite user imagination.

## Core Philosophy

### White (白) is Not a Color—It is Receptivity

> "白があるのではない。白いと感じる感受性があるのだ"
> "White does not exist. What exists is the sensibility that perceives white."

White is not the absence of color but the presence of infinite potential. Design interfaces as "empty vessels" (器) that users fill with their own meaning, like a Shinto shrine that awaits the divine.

### Emptiness (エンプティネス) vs. Simplicity

| Simplicity (西洋的) | Emptiness (日本的) |
|---------------------|-------------------|
| Reduction by removal | Potential through absence |
| Minimizes to essentials | Creates space for possibility |
| Closed, complete | Open, inviting |
| Designer's statement | User's interpretation |

Emptiness is not "nothing"—it is "anything." Like the MUJI horizon campaign: a vast empty landscape that each viewer fills with their own meaning.

## Design Principles

### 1. Ma (間) — Meaningful Interval

Space is not emptiness to fill but presence to respect. Every pause, gap, and silence carries meaning.

```
WRONG: Cramming content to "use" space
RIGHT: Generous spacing that creates rhythm and breath
```

**Implementation:**
- Use asymmetric, generous margins (min 48-64px between major sections)
- Let single elements breathe in vast space
- Create visual pauses between content blocks
- Silence (empty space) speaks louder than noise

### 2. Yohaku (余白) — Active Emptiness

Empty space is not background—it is foreground. The white of a page is as important as what is written on it.

**Implementation:**
- Design the negative space first, content second
- White space should feel intentional, not leftover
- Use emptiness to guide the eye and create hierarchy
- Consider what is NOT shown as carefully as what IS

### 3. Shibui (渋い) — Refined Restraint

Beauty in understated elegance. Not flashy, not dull—simply present.

**Implementation:**
- Reject decoration that doesn't serve meaning
- Choose materials (colors, fonts) for their inherent quality
- Prefer natural, honest expressions over artificial polish
- Let imperfections exist when they add character

### 4. Kanso (簡素) — Elegant Simplicity

Simplicity that emerges from depth, not laziness.

**Implementation:**
- Every element must justify its existence
- Complexity should be absorbed, not displayed
- The interface should feel effortless despite underlying sophistication

## Visual Language

### Color Philosophy

**Primary Palette:**
- Pure white (#FFFFFF) — not as background but as presence
- Off-whites with subtle warmth (#FAFAFA, #F5F5F4) — like washi paper
- Ink black (#1A1A1A) — decisive but not harsh
- Gray spectrum — soft, contemplative tones

**Accent Philosophy:**
- One accent color maximum, used sparingly
- Color should emerge from content, not decoration
- Natural, material-derived colors (earth, wood, stone, sky)

```css
:root {
  /* White spectrum - like varying densities of mist */
  --shiro: #FFFFFF;
  --washi: #FAF9F7;
  --kumo: #F0EFED;  /* cloud */
  
  /* Ink spectrum */
  --sumi: #1A1A1A;  /* ink */
  --usuzumi: #4A4A4A;  /* light ink */
  --hai: #8A8A8A;  /* ash */
  
  /* Natural accents - use ONE sparingly */
  --akane: #C73E3A;  /* madder red */
  --ai: #2E4A62;  /* indigo */
  --matcha: #5B6E4E;  /* tea green */
}
```

### Typography

**Selection Criteria:**
- Fonts with inherent quietness and dignity
- Japanese aesthetics favor asymmetry and organic rhythm
- Sans-serif for modernity, serif for contemplation

**Recommended Approach:**
- Display: Elegant, characterful fonts (Cormorant, Freight Display, Spectral)
- Body: Quiet, readable fonts (Karla, DM Sans, IBM Plex Sans)
- Japanese: Noto Sans JP, Shippori Mincho for traditional feel
- Generous line-height (1.7-2.0 for body text)
- Letter-spacing that allows characters to breathe

### Spatial Composition

**Grid Philosophy:**
- Asymmetry over symmetry
- Off-center focal points
- Diagonal or unexpected flows
- Large areas of intentional emptiness

**Spacing Scale (8px base):**
```
xs: 8px   — intimate
sm: 16px  — related
md: 32px  — grouped  
lg: 64px  — separated
xl: 128px — contemplative
2xl: 256px — vast
```

### Motion & Interaction

**Principles:**
- Movement should be like breath—natural, unhurried
- Transitions reveal rather than decorate
- Micro-interactions should feel discovered, not announced

**Timing:**
- Slow, contemplative transitions (400-800ms)
- Ease curves that feel organic
- Staggered reveals that create rhythm
- Hover states that suggest rather than shout

```css
/* Contemplative transitions */
.element {
  transition: all 600ms cubic-bezier(0.23, 1, 0.32, 1);
}

/* Gentle reveal */
@keyframes emerge {
  from { 
    opacity: 0; 
    transform: translateY(20px); 
  }
  to { 
    opacity: 1; 
    transform: translateY(0); 
  }
}
```

## Component Patterns

### Hero Sections
- Vast empty space with minimal, centered content
- Single powerful image or pure typography
- Like MUJI's Horizon campaign—let emptiness speak

### Navigation
- Hidden or minimal until needed
- Text-only, generous spacing
- Appears as whisper, not announcement

### Cards & Containers
- Borderless or single subtle line
- No shadows or very subtle elevation
- Content floats in space rather than sits in boxes

### Buttons & CTAs
- Text-based or minimal outline
- No aggressive fills or gradients
- Action emerges from context, not decoration

### Forms
- Generous field spacing
- Minimal borders (bottom-only or subtle)
- Labels as quiet guides, not demands

## Anti-Patterns (何をしないか)

NEVER use:
- Drop shadows for visual interest
- Gradient backgrounds
- Decorative icons without function
- Multiple accent colors competing
- Dense, cramped layouts
- Aggressive CTAs or urgency signals
- Stock photography that fills space
- Animations that demand attention
- Rounded corners everywhere (choose deliberately)
- Dark patterns or manipulative UI

## Implementation Checklist

Before finalizing any design, verify:

- [ ] Could this element be removed without loss of meaning?
- [ ] Does the white space feel active, not neglected?
- [ ] Would the design feel complete with LESS?
- [ ] Does interaction invite discovery rather than demand attention?
- [ ] Is there room for user interpretation?
- [ ] Does the design feel quiet yet present?
- [ ] Are colors derived from necessity, not decoration?
- [ ] Does typography have room to breathe?
- [ ] Would Kenya Hara approve of this restraint?

## Reference: Kenya Hara's Work

Study these for inspiration:
- MUJI corporate identity and advertising
- MUJI Horizon campaign (地平線)
- Book designs: "白", "白百", "デザインのデザイン"
- GINZA SIX visual identity
- Tsutaya Books brand design

## Final Thought

The goal is not to create "minimal" interfaces but to create **receptive** interfaces—designs that, like a well-made ceramic bowl, derive their beauty from what they can receive, not from what they display.

> "シンボルの規模はその受容力に比例する"
> "The magnitude of a symbol is proportional to its capacity for reception."

Design interfaces that are vessels for meaning, not declarations of it.
