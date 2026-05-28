---
name: foundry-nextgen-frontend
description: Use this skill when building elegant frontend UIs that adhere to Microsoft Foundry's NextGen Design System, particularly for applications like dashboards and data management interfaces.
---

# Microsoft Foundry NextGen Frontend Skill

Build elegant, production-ready interfaces following Microsoft Foundry's NextGen Design System - a refined **neutral dark-themed** design language with **minimal purple accents** for primary actions only.

## ⚠️ CRITICAL: Color Usage Rules

**Purple (#8251EE / #A37EF5) is ONLY for:**
- Primary action buttons (filled background)
- Active tab indicators (2px underline)
- Row selection indicators (left border bar)
- Active sidebar navigation icons
- Links and interactive text
- Progress indicators and sliders (track fill)
- Focus rings on inputs

**Everything else uses NEUTRAL DARK GREYS:**
- Backgrounds: Near-black and dark greys (#0A0A0A, #141414, #1C1C1C)
- Cards/Surfaces: Dark grey (NOT purple-tinted)
- Text: White (#FFFFFF), grey (#A1A1A1), muted (#6B6B6B)
- Secondary buttons: Grey outline with white text (NOT purple)
- Borders: Subtle dark grey (#2A2A2A, #333333)
- Inactive tabs: Grey text (#6B6B6B)

## Preferred Stack

```bash
pnpm create vite@latest my-foundry-app --template react-ts
cd my-foundry-app
pnpm install
pnpm add framer-motion lucide-react recharts
```

**Required packages:**
- `framer-motion` - for subtle, elegant animations
- `lucide-react` - for icons
- `recharts` - for data visualization

## ⚠️ CRITICAL: Spacing & Padding Rules

**Consistent spacing is non-negotiable. Use the spacing scale:**

```css
:root {
  --space-1: 4px;
  --space-2: 8px;
  --space-3: 12px;
  --space-4: 16px;
  --space-5: 20px;
  --space-6: 24px;
  --space-8: 32px;
  --space-10: 40px;
  --space-12: 48px;
}
```

**Standard padding patterns:**
| Element | Padding |
|---------|---------|
| Page content | 32px (--space-8) |
| Card | 20px (--space-5) |
| Card header | 16px 20px |
| Button | 8px 16px |
| Input | 10px 12px |
| Table cell | 12px 16px |
| Modal body | 24px |
| Badge/Tag | 4px 10px |

**Grid gaps:**
| Layout | Gap |
|--------|-----|
| Card grid | 16px (--space-4) |
| Form fields | 20px (--space-5) |
| Button group | 12px (--space-3) |
| Tag group | 8px (--space-2) |

## Core Design Tokens

```css
:root {
  /* BACKGROUNDS - Neutral Darks */
  --bg-page: #0A0A0A;
  --bg-sidebar: #0D0D0D;
  --bg-card: #141414;
  --bg-surface: #1C1C1C;
  --bg-elevated: #242424;
  --bg-hover: rgba(255, 255, 255, 0.05);
  --bg-active: rgba(255, 255, 255, 0.08);
}
```