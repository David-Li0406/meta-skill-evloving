---
name: frontend-development
description: Use this skill when you need to build responsive frontend pages and reusable UI components with clean layouts and modern styling.
---

# Frontend Development Skill

## Instructions

### 1. Page Building & Layout Structure
- Create complete pages (e.g., Home, About, Blog, Dashboard) following given designs or wireframes.
- Use semantic HTML (`header`, `main`, `section`, `footer`) and maintain a clear visual hierarchy.
- Implement full-width or container-based layouts using Flexbox and CSS Grid.
- Ensure the structure is clean, readable, and responsive across mobile, tablet, and desktop.

### 2. Components
- Build reusable UI components (e.g., Navbar, Card, Button, Footer) with a component-first mindset.
- Use props for dynamic data and keep components small, focused, and easy to scale.
- Maintain consistent spacing, typography, and class naming.

### 3. Styling
- Follow a mobile-first CSS approach, utilizing CSS, Tailwind, or styled components.
- Use CSS variables for colors, spacing, and fonts, and ensure clean hover, focus, and active states.
- Avoid inline styles unless necessary and follow a design system or theme.

### 4. Responsiveness
- Implement breakpoints for layout changes and ensure fluid typography and spacing.
- Design for accessibility, ensuring color contrast and semantic HTML.

## Best Practices
- Keep components reusable and isolated.
- Follow mobile-first design principles and maintain a consistent spacing system.
- Ensure accessible HTML and clean, readable code.

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
```