---
name: foundry-nextgen-frontend
description: Build elegant frontend UIs following Microsoft Foundry's NextGen Design System using Vite + React + pnpm. Use when creating dashboards, agent builders, data grids, entity management interfaces, or any application matching Foundry's refined dark-themed aesthetic.
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

## Core Design Tokens

```css
:root {
  /* BACKGROUNDS - Neutral Darks */
  --bg-page: #0A0A0A;
  --bg-sidebar: #0D0D0D;
  --bg-card: #141414;
  --bg-surface: #1C1C1C;
  --bg-elevated: #242424;
  --bg-hover: #2A2A2A;
  --bg-active: #333333;

  /* TEXT */
  --text-primary: #FFFFFF;
  --text-secondary: #A1A1A1;
  --text-muted: #6B6B6B;
  --text-disabled: #4A4A4A;
  --text-link: #A37EF5;

  /* BRAND - Use Sparingly! */
  --brand-primary: #8251EE;
  --brand-hover: #9366F5;
  --brand-light: #A37EF5;

  /* BORDERS - Keep Subtle! */
  --border-subtle: #1F1F1F;
  --border-default: #2A2A2A;
  --border-strong: #333333;

  /* STATUS */
  --success: #10B981;
  --warning: #F59E0B;
  --error: #EF4444;
  --info: #3B82F6;

  /* RADIUS */
  --radius-sm: 4px;
  --radius-md: 6px;
  --radius-lg: 8px;
  --radius-xl: 12px;
}
```

## ⚠️ CRITICAL: Animation with Framer Motion

**Always add subtle animations. Never skip animations.**

```jsx
import { motion } from 'framer-motion';

// Page/container fade in
const pageVariants = {
  hidden: { opacity: 0 },
  visible: { 
    opacity: 1,
    transition: { duration: 0.3, ease: 'easeOut' }
  }
};

// Stagger children (for lists, grids)
const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.05,
      delayChildren: 0.1
    }
  }
};

// Individual item animation
const itemVariants = {
  hidden: { opacity: 0, y: 8 },
  visible: { 
    opacity: 1, 
    y: 0,
    transition: { duration: 0.3, ease: 'easeOut' }
  }
};

// Hover scale for cards/buttons
const hoverScale = {
  whileHover: { scale: 1.01 },
  whileTap: { scale: 0.99 },
  transition: { duration: 0.15 }
};
```

## Card Component (Correct Implementation)

**Cards should have NO visible borders or very subtle ones.**

```jsx
import { motion } from 'framer-motion';

function Card({ title, description, status, tags, meta }) {
  return (
    <motion.div 
      className="card"
      whileHover={{ 
        scale: 1.01,
        backgroundColor: 'rgba(255, 255, 255, 0.02)'
      }}
      transition={{ duration: 0.15 }}
    >
      <div className="card-header">
        <h3 className="card-title">{title}</h3>
        {status && <StatusBadge status={status} />}
      </div>
      
      <p className="card-description">{description}</p>
      
      {tags && (
        <div className="card-tags">
          {tags.map(tag => (
            <span key={tag} className="tag">{tag}</span>
          ))}
        </div>
      )}
      
      {meta && (
        <div className="card-meta">
          {meta}
        </div>
      )}
    </motion.div>
  );
}
```

```css
.card {
  background: var(--bg-card);
  border-radius: var(--radius-lg);
  padding: var(--space-5);  /* 20px */
  border: 1px solid transparent;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
}

.card:hover {
  border-color: var(--border-subtle);
}
```

## Critical Don'ts ❌

- **Don't use visible card borders** - cards blend into background
- **Don't use inconsistent padding** - follow the spacing scale
- **Don't forget animations** - every list, modal, page needs motion
- **Don't use purple for cards/backgrounds** - neutral greys only
- **Don't skip hover states** - everything interactive needs feedback
- **Don't use hard-coded pixel values** - use CSS variables

## Critical Do's ✅

- Use Framer Motion for all animations
- Use consistent spacing scale (4, 8, 12, 16, 20, 24, 32px)
- Use 32px padding for page content areas
- Use 16px gap for card grids
- Use transparent or very subtle borders
- Add hover animations to interactive elements
- Stagger list/grid item animations

## File References

- **Design Tokens**: See `references/design-tokens.md`
- **Components**: See `references/components.md`
- **Patterns**: See `references/patterns.md`