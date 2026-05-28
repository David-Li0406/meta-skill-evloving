---
name: ribh_design
description: Create premium, high-converting dashboard and landing pages for RIBH following the brand's visual identity.
---

# Ribh Design System

Use this skill to create new pages or components for the RIBH application. The aesthetic is "Apple-style Premium" with glassmorphism, clean typography, and vibrant gradients.

## 🎨 Brand Tokens

- **Primary Color**: `#10B981` (Emerald Green)
- **Secondary/Accent**: `#EC4899` (Pink)
- **Background**: `#F8FAFC` (Light Slate)
- **Card Background**: `#FFFFFF` with `border: 1px solid #E2E8F0`
- **Typography**: 
  - Arabic: `Noto Kufi Arabic`
  - English: `Inter` or `System Sans-Serif`

## 🧱 Key Components

### 1. Sidebar Layout
- Width: `240px`
- Position: Fixed (Right for RTL, Left for LTR)
- Items: Nav links with icons and active states.

### 2. Glass Cards
```css
.glass-card {
    background: rgba(255, 255, 255, 0.7);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.3);
    border-radius: 16px;
}
```

### 3. Action Buttons
- **Primary**: Gradient background (`linear-gradient(135deg, #EC4899, #DB2777)`), white text, rounded.
- **Secondary**: Light emerald background (`rgba(16, 185, 129, 0.1)`), emerald text.

## 🚀 Execution Instructions

1.  **Read `resources/template.html`** in this skill folder to get the base layout.
2.  **Define the page purpose**: Is it a dashboard tool, a settings page, or a landing page?
3.  **Use `resources/components.css`** for consistent styling.
4.  **Incorporate Behavioral Logic**: RIBH is about "Behavioral Hooks". Every page should solve a human psychology problem (scarcity, urgency, social proof).

## 📁 Resources
- `resources/template.html`: Base boilerplate.
- `resources/components.css`: Pre-baked styles.
