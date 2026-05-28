# Al-Huda Visual Guidelines

**Theme:** Emerald Night  
**Design Philosophy:** Premium, serene Islamic aesthetic with modern dark-mode UI

---

## Design Principles

### 1. Spiritual Serenity
- Deep dark backgrounds evoke peaceful night reading
- Emerald green (#13ec5b) represents Islamic heritage and growth
- Gold accents (#d4af37) add premium warmth for achievements

### 2. Readability First
- High contrast for Quranic text
- Generous whitespace around Arabic ayahs
- Clear visual hierarchy for navigation

### 3. Glowing Emphasis
- Primary buttons feature green glow shadows (`0 10px 30px rgba(19, 236, 91, 0.25)`)
- Progress bars have subtle glow (`0 0 10px rgba(19, 236, 91, 0.5)`)
- Creates a "blessing" or "nur (light)" effect

---

## Color Palette

### Primary Colors
| Name | Hex | Usage |
|------|-----|-------|
| Emerald Primary | `#13ec5b` | CTAs, active states, progress, success |
| Emerald Light | `#4ff285` | Hover states, highlights |
| Emerald Glow | `rgba(19, 236, 91, 0.3)` | Button/element shadows |

### Accent Colors
| Name | Hex | Usage |
|------|-----|-------|
| Gold | `#d4af37` | Hasanat, achievements, Qibla icon |
| Orange | `#f97316` | Streak fire, alerts |

### Background Colors
| Name | Hex | Usage |
|------|-----|-------|
| Deep Forest (Dark BG) | `#102216` | Main background |
| Surface Dark | `#1c271f` | Cards, elevated surfaces |
| Surface Elevated | `#23482f` | Stat cards with highlight |

### Text Colors
| Name | Value | Usage |
|------|-------|-------|
| Primary | `#ffffff` | Headings, important text |
| Secondary | `#9db9a6` | Body text, descriptions |
| Tertiary | `#92c9a4` | Labels, captions |
| Muted | `rgba(255, 255, 255, 0.4)` | Hints, placeholders |

---

## Typography

### Font Families
1. **Lexend** - Display font for headings and navigation
2. **Manrope** - Body font for general text
3. **Noto Sans Arabic** - Quranic text and Arabic content

### Arabic Text Guidelines
- Always use RTL (right-to-left) direction
- Line height: 1.8 for comfortable reading
- Size: 36px for main ayah display
- Font weight: 700 (bold) for Quranic verses

### Type Scale
| Size Token | Value | Usage |
|------------|-------|-------|
| xs | 10px | Badges, tab labels |
| sm | 12px | Captions, secondary info |
| base | 14px | Body text |
| md | 16px | Large body text |
| lg | 18px | Subheadings |
| xl | 20px | Section headers |
| 2xl | 24px | Stat numbers |
| 3xl | 30px | Large numbers |
| 4xl | 36px | Arabic ayahs |

---

## Component Specifications

### Buttons

**Primary Button:**
```
Background: #13ec5b
Text: #102216 (dark on bright)
Border Radius: 16px
Height: 64px (large CTA), 48px (standard)
Shadow: 0 10px 30px rgba(19, 236, 91, 0.25)
Hover: scale(0.98) transition
```

**Secondary Button:**
```
Background: transparent
Text: #ffffff
Border: 1px solid rgba(255, 255, 255, 0.1)
Border Radius: 12px
```

### Cards
```
Background: #1c271f
Border: 1px solid rgba(255, 255, 255, 0.05)
Border Radius: 12px
Padding: 20px
```

### Progress Bars
```
Track Background: #3b5443
Fill: #13ec5b
Height: 12px (large), 8px (standard)
Border Radius: 9999px (full round)
Glow: 0 0 10px rgba(19, 236, 91, 0.5)
```

### Bottom Navigation
```
Background: rgba(16, 34, 22, 0.8)
Backdrop Blur: 12px
Height: 80px
Border Top: 1px solid rgba(255, 255, 255, 0.05)
Active Icon: #13ec5b
Inactive Icon: rgba(255, 255, 255, 0.5)
```

### Input Fields
```
Background: #1c271f
Border: 1px solid rgba(255, 255, 255, 0.1)
Border Radius: 8px
Padding: 12px 16px
Focus Border: #13ec5b
```

---

## Animations & Interactions

### Duration Scale
- Fast: 150ms (button presses, toggles)
- Normal: 300ms (page transitions, modals)
- Slow: 500ms (celebrations, confetti)

### Easing Functions
- Default: `ease-out`
- Bounce: `cubic-bezier(0.68, -0.55, 0.265, 1.55)` - for celebratory moments
- Smooth: `cubic-bezier(0.4, 0, 0.2, 1)` - for natural movements

### Recommended Animations
1. **Goal Completion:** Confetti + scale bounce
2. **Hasanat Increment:** Number counter animation with sparkle
3. **Progress Update:** Smooth width transition with glow pulse
4. **Button Press:** Scale to 0.98 + shadow reduction
5. **Screen Transitions:** Fade + slight slide

---

## Background Patterns

### Islamic Dots Pattern
For subtle texture on dark backgrounds:
```css
background-color: #102216;
background-image: radial-gradient(#1c271f 1px, transparent 1px);
background-size: 20px 20px;
```

---

## Spacing System

Based on 4px unit:
- 1 = 4px
- 2 = 8px
- 3 = 12px
- 4 = 16px (base spacing)
- 5 = 20px
- 6 = 24px
- 8 = 32px

---

## Icon Guidelines

- Use Material Symbols Outlined
- Icon size: 24px (standard), 20px (small), 32px (feature icons)
- Active color: `#13ec5b`
- Inactive color: `rgba(255, 255, 255, 0.5)`
- Special icons (Qibla, stars): `#d4af37` gold

---

## Mockup Reference

All mockups are located in: `Stich designs/`

Key screens for reference:
- `home_dashboard/` - Main dashboard layout
- `focused_ayah_reading/` - Reading experience
- `daily_goal_achieved/` - Celebration screen
- `prayer_times_&_qibla/` - Prayer features
- `community_feed/` - Social features
