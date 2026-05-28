# Accessibility-First Design

### Problem

70-80% of accessibility issues can be avoided at design stage.

### Solution: Design for Accessibility from Day 1

**Color & Contrast:**
| Element | Minimum Ratio |
|---------|---------------|
| Body text | 4.5:1 |
| Large text (18pt+) | 3:1 |
| UI components | 3:1 |
| Focus indicators | 3:1 |

**Design Checklist:**
- [ ] Color is not only indicator of meaning
- [ ] Text readable on all backgrounds
- [ ] Focus states clearly visible
- [ ] Touch targets 44x44px minimum
- [ ] Sufficient spacing between interactive elements
- [ ] No time limits (or adjustable)
- [ ] Animations can be paused/reduced

**Semantic Structure:**
```html
<!-- Good: Semantic structure -->
<nav>
  <ul>
    <li><a href="/">Home</a></li>
  </ul>
</nav>
<main>
  <article>
    <h1>Main Title</h1>
    <section>
      <h2>Section Title</h2>
    </section>
  </article>
</main>

<!-- Bad: Div soup -->
<div class="nav">
  <div class="link">Home</div>
</div>
```
