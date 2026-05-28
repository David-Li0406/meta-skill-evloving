---
name: frontend-ui-builder
description: Use this skill when you need to build responsive frontend pages and reusable UI components with clean layouts and modern styling.
---

# Skill body

## Instructions

### 1. Page & Layout Structure
- Create complete pages (Home, About, Blog, Dashboard) using semantic HTML (`header`, `main`, `section`, `footer`).
- Follow given design or wireframe with full-width or container-based layouts.
- Maintain a clear visual hierarchy using Grid or Flexbox for positioning.

### 2. Components
- Build reusable UI components (Navbar, Card, Button, Footer) with a component-first mindset.
- Use props for dynamic data and ensure consistent spacing and typography.
- Keep components small, focused, and easy to scale and modify.

### 3. Styling
- Follow a mobile-first CSS approach using Flexbox and CSS Grid.
- Utilize CSS variables for colors, spacing, and fonts, and ensure clean hover, focus, and active states.
- Avoid inline styles unless necessary and follow a design system or theme.

### 4. Responsiveness
- Ensure designs work across mobile, tablet, and desktop with breakpoints for layout changes.
- Implement fluid typography and spacing for a consistent look.

## Best Practices
- Keep components reusable and isolated.
- Follow mobile-first design principles.
- Maintain a consistent spacing system and ensure accessible color contrast.
- Use clear and predictable class names.
- Write clean and readable code.

## Example Structure
```html
<header class="navbar">
  <div class="container">
    <h1 class="logo">Brand</h1>
    <nav class="nav-links">
      <a href="#">Home</a>
      <a href="#">Features</a>
      <a href="#">Contact</a>
    </nav>
  </div>
</header>

<main class="container">
  <section class="card-grid">
    <div class="card">
      <h2>Card Title</h2>
      <p>Reusable component content.</p>
      <button class="btn-primary">Action</button>
    </div>
  </section>
</main>