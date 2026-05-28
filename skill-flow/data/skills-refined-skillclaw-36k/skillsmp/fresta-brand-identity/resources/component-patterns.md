# Component Patterns - Fresta Design System

Anatomia detalhada de componentes reutilizáveis para manter consistência visual.

## 📐 Anatomia de Componentes

### 1. Cards

#### Feature Card (Estilo Solidroad)
```
┌──────────────────────────────────────┐
│  [Background: Pastel Color]          │
│                                      │
│  ┌────────┐                          │
│  │ Icon   │  <- 56x56px, rounded-2xl │
│  └────────┘     bg-white/50          │
│                                      │
│  Título Grande                       │
│  ─────────────                       │
│  text-2xl font-bold                  │
│                                      │
│  Descrição com no máximo             │
│  2-3 linhas de texto.                │
│  text-neutral-text-secondary         │
│                                      │
│  ════════════════════════════════    │ <- Borda animada no hover
└──────────────────────────────────────┘

Specs:
- min-height: 420px
- padding: 32px
- border-radius: 24px (rounded-3xl)
- background: card-beige | card-turquoise | card-green | card-pink
- hover: translateY(-8px) + shadow-lg
```

#### Stats Card
```
┌─────────────────────────┐
│  ┌────┐                 │
│  │Icon│ <- 56x56px      │
│  └────┘    bg-muted/50  │
│                         │
│  1,234                  │ <- text-4xl font-black
│  ─────                  │
│  LABEL                  │ <- text-xs uppercase tracking-wide
│                         │
└─────────────────────────┘

Specs:
- padding: 32px
- border-radius: 32px (rounded-[2rem])
- hover: border-primary/30
```

#### Action Card
```
┌─────────────────────────────────────────┐
│  ┌────┐                                 │
│  │Icon│  <- 56x56px                     │
│  └────┘     highlight: bg-primary       │
│             normal: bg-muted            │
│                                         │
│  Título do Card                         │
│  ─────────────                          │
│  text-xl font-black                     │
│                                         │
│  Descrição curta do card                │
│  text-sm text-muted-foreground          │
│                                         │
└─────────────────────────────────────────┘

Specs:
- padding: 32px
- border-radius: 40px (rounded-[2.5rem])
- gap entre ícone e texto: 24px
- hover: scale(1.02) + border-primary/40
```

### 2. Buttons

#### Primary Button
```
┌─────────────────────────────────┐
│  [Icon]  Label Text  [→]        │
└─────────────────────────────────┘

States:
- Default: bg-accent-warm text-white
- Hover: bg-accent-bright shadow-colored-warm translateY(-2px)
- Active: scale(0.98)
- Disabled: opacity-50 cursor-not-allowed

Sizes:
- sm: px-4 py-2 text-sm rounded-lg
- md: px-6 py-3 text-base rounded-xl
- lg: px-8 py-4 text-lg rounded-2xl
```

#### Secondary Button
```
┌─────────────────────────────────┐
│  Label Text                     │
└─────────────────────────────────┘

States:
- Default: bg-white border-2 border-primary text-primary
- Hover: bg-primary/10
- Active: bg-primary/20
```

#### Ghost Button
```
┌─────────────────────────────────┐
│  Label Text                     │
└─────────────────────────────────┘

States:
- Default: bg-transparent text-primary
- Hover: bg-primary/10
```

#### Icon Button
```
┌─────┐
│  ☰  │
└─────┘

States:
- Default: bg-muted/50 border-border/50
- Hover: bg-muted

Sizes:
- sm: w-8 h-8 rounded-lg
- md: w-10 h-10 rounded-xl
- lg: w-12 h-12 rounded-2xl
```

### 3. Forms

#### Input Field
```
┌─────────────────────────────────────────┐
│  Label (optional)                       │
│  ┌───────────────────────────────────┐  │
│  │ Placeholder text...               │  │
│  └───────────────────────────────────┘  │
│  Helper text (optional)                 │
└─────────────────────────────────────────┘

Specs:
- height: 48-56px
- padding: 16px
- border-radius: 12px (rounded-xl)
- border: 2px solid border
- focus: border-primary ring-2 ring-primary/20
- error: border-error
```

#### Search Input
```
┌─────────────────────────────────────────┐
│  🔍  Buscar...                          │
└─────────────────────────────────────────┘

Specs:
- icon: 16x16px text-muted-foreground
- padding-left: 48px (para ícone)
- background: bg-muted/50
- border: border-border/50
- focus: border-primary/50
```

### 4. Navigation

#### Sidebar Item
```
┌─────────────────────────────────────────┐
│  [Icon]  Label                     [→]  │
└─────────────────────────────────────────┘

States:
- Default: text-muted-foreground
- Hover: bg-muted text-foreground
- Active: bg-primary/10 text-primary border-l-2 border-primary

Specs:
- height: 48px
- padding: 12px 16px
- border-radius: 12px
- icon: 20x20px
```

#### Tab Navigation
```
┌───────┐ ┌───────┐ ┌───────┐
│ Tab 1 │ │ Tab 2 │ │ Tab 3 │
└───────┘ └───────┘ └───────┘
═════════

States:
- Default: text-muted-foreground
- Active: text-primary + underline (via pseudo-element)
- Hover: text-foreground

Specs:
- padding: 12px 16px
- gap: 8px
- active indicator: 2px height, bg-primary, animated width
```

### 5. Modals

#### Standard Modal
```
┌────────────────────────────────────────────┐
│  ┌──────────────────────────────────────┐  │
│  │                                      │  │
│  │  [×]                          Title  │  │
│  │  ────────────────────────────────    │  │
│  │                                      │  │
│  │  Content goes here with proper       │  │
│  │  spacing and readable text.          │  │
│  │                                      │  │
│  │  ┌────────────┐  ┌────────────┐      │  │
│  │  │  Cancel    │  │   Save     │      │  │
│  │  └────────────┘  └────────────┘      │  │
│  │                                      │  │
│  └──────────────────────────────────────┘  │
│                                            │
└────────────────────────────────────────────┘
   ↑ Backdrop: bg-black/60 backdrop-blur-sm

Specs:
- max-width: 400-600px
- padding: 24px
- border-radius: 24px (rounded-3xl)
- shadow: shadow-2xl
- animation: scale(0.9) → scale(1) + fade
```

### 6. Avatars

#### User Avatar
```
┌─────────────────┐
│                 │
│   [Image or     │
│    Initials]    │
│                 │
└─────────────────┘

Sizes:
- xs: 24x24px rounded-md
- sm: 32x32px rounded-lg
- md: 40x40px rounded-xl
- lg: 64x64px rounded-2xl
- xl: 96x96px rounded-3xl

Fallback:
- DiceBear API: lorelei style
- Background colors: pastel gradient
```

#### Avatar with Status
```
┌─────────────────┐
│                 │
│   [Avatar]   ●  │ <- Status indicator
│                 │    (online/offline)
└─────────────────┘

Status colors:
- online: bg-green-500
- offline: bg-gray-400
- busy: bg-red-500
- away: bg-yellow-500
```

## 🎨 Color Applications

### Card Background Colors
```
beige:     #FFF8E8  → Features gerais
turquoise: #D4F4F0  → Recursos técnicos
green:     #E8F5E0  → Sucesso/crescimento
pink:      #FFE5EC  → Relacionamentos/romance
```

### Gradient Applications
```
hero:    from-primary-deep to-primary     → Hero sections
accent:  from-accent-warm to-accent-bright → CTAs primários
cool:    from-primary to-accent-cool       → Features tech
sunset:  from-accent-warm to-accent-sunrise → Promoções
```

## 🔄 Animation Patterns

### Hover Effects
```typescript
// Card hover
whileHover={{ y: -8, scale: 1.02 }}
transition={{ duration: 0.3 }}

// Button hover
whileHover={{ y: -2 }}
whileTap={{ scale: 0.98 }}

// Icon hover
whileHover={{ scale: 1.1, rotate: 5 }}
```

### Entrance Animations
```typescript
// Fade up
initial={{ opacity: 0, y: 20 }}
animate={{ opacity: 1, y: 0 }}
transition={{ duration: 0.5 }}

// Stagger children
variants={{
  show: { transition: { staggerChildren: 0.1 } }
}}

// Scale in
initial={{ scale: 0.9, opacity: 0 }}
animate={{ scale: 1, opacity: 1 }}
```

### Micro-interactions
```typescript
// Glow pulse
animate={{ boxShadow: ['0 0 20px rgba(255,209,102,0.4)', '0 0 40px rgba(255,209,102,0.6)'] }}
transition={{ duration: 2, repeat: Infinity }}

// Float
animate={{ y: [0, -10, 0] }}
transition={{ duration: 6, repeat: Infinity }}

// Rotate continuously
animate={{ rotate: 360 }}
transition={{ duration: 20, repeat: Infinity, ease: 'linear' }}
```

## 📏 Spacing Guidelines

### Section Padding
```
Mobile:  py-16 (64px)
Tablet:  py-24 (96px)
Desktop: py-32 (128px)
```

### Card Padding
```
Compact: p-4 (16px)
Normal:  p-6 (24px)
Spacious: p-8 (32px)
```

### Gap Between Elements
```
Tight:   gap-2 (8px)   → Items em lista
Normal:  gap-4 (16px)  → Elementos relacionados
Medium:  gap-6 (24px)  → Cards em grid
Wide:    gap-8 (32px)  → Seções distintas
```

## 🔲 Border Radius Guide

| Componente | Radius | Class |
|------------|--------|-------|
| Ícones pequenos | 8px | rounded-lg |
| Inputs | 12px | rounded-xl |
| Cards pequenos | 16px | rounded-2xl |
| Cards médios | 24px | rounded-3xl |
| Cards grandes | 32px | rounded-[2rem] |
| Modais | 24px | rounded-3xl |
| Hero sections | 32-48px | rounded-[2-3rem] |
| Avatars | Full | rounded-full |

## 📱 Responsive Patterns

### Container Width
```
sm:  max-w-screen-sm  (640px)
md:  max-w-screen-md  (768px)
lg:  max-w-screen-lg  (1024px)
xl:  max-w-screen-xl  (1280px)
2xl: max-w-[1600px]   (1600px)
```

### Grid Columns
```
Mobile:  grid-cols-1
Tablet:  grid-cols-2
Desktop: grid-cols-3 ou grid-cols-4
```

### Stack to Row
```tsx
<div className="flex flex-col md:flex-row gap-4">
  {/* Stacks vertically on mobile, horizontal on tablet+ */}
</div>
```
