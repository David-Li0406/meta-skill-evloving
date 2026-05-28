---
name: web-design-reviewer
description: 'Expert-level UI/UX design review. Phân tích design mockups, live websites để đưa ra actionable feedback về visual design, UX, accessibility, responsive design.'
---

# Web Design Reviewer Skill

Skill này provide comprehensive design review methodology cho web designs, đưa ra expert-level feedback và actionable recommendations.

## Khi Nào Sử Dụng

- Review design mockups trước development
- Analyze live websites cho improvements
- Audit UI/UX của existing products
- Prepare feedback cho design team
- Validate accessibility compliance
- Check responsive design implementation

---

## Review Framework

### 1. First Impressions (5 giây đầu)

| Aspect | Question |
|--------|----------|
| Clarity | Purpose của page rõ ràng không? |
| Hierarchy | Visual priority có đúng không? |
| Brand | Có nhận ra brand identity không? |
| Trust | Design có professional không? |

### 2. Visual Design Analysis

#### Typography Review
- [ ] Font pairing có harmonious không?
- [ ] Hierarchy rõ ràng (H1 > H2 > body)?
- [ ] Line height comfortable (1.4-1.6 cho body)?
- [ ] Font sizes responsive?
- [ ] Contrast đủ cho readability?

#### Color Review
- [ ] Palette có cohesive không?
- [ ] Contrast ratio đạt WCAG (4.5:1 text, 3:1 UI)?
- [ ] Meaning của colors consistent?
- [ ] Không rely chỉ vào color để convey information?
- [ ] Dark/light mode supported?

#### Spacing & Layout
- [ ] Spacing consistent (8px grid)?
- [ ] White space adequate?
- [ ] Visual grouping logical?
- [ ] Content width comfortable (45-75 characters)?
- [ ] Alignment precise?

#### Imagery & Icons
- [ ] Images high quality, relevant?
- [ ] Icon style consistent?
- [ ] Alt text for images?
- [ ] Loading states for media?

### 3. UX Analysis

#### Navigation
- [ ] Nav structure intuitive?
- [ ] Current location clear?
- [ ] Breadcrumbs where needed?
- [ ] Search easily accessible?
- [ ] Mobile nav works well?

#### Interactions
- [ ] Clickable areas obvious?
- [ ] Hover/active states clear?
- [ ] Loading feedback present?
- [ ] Error states helpful?
- [ ] Success confirmations clear?

#### Forms
- [ ] Labels clear and visible?
- [ ] Input validation helpful?
- [ ] Error messages specific?
- [ ] Required fields marked?
- [ ] Auto-complete where appropriate?

### 4. Accessibility Audit

#### Visual
- [ ] Color contrast WCAG AA
- [ ] Text resizable to 200%
- [ ] Focus indicators visible
- [ ] No flashing content

#### Semantic
- [ ] Proper heading hierarchy
- [ ] ARIA labels where needed
- [ ] Alt text meaningful
- [ ] Skip links present

#### Interaction
- [ ] Keyboard navigable
- [ ] Touch targets 44px+
- [ ] No hover-only content
- [ ] Form labels associated

### 5. Responsive Review

| Breakpoint | Check |
|------------|-------|
| Mobile (375px) | Touch-friendly, readable |
| Tablet (768px) | Layout adapts, not just shrunk |
| Desktop (1280px) | Uses space effectively |
| Wide (1920px+) | Content not too stretched |

---

## Review Output Format

### Summary
- Overall score (1-10)
- Top 3 strengths
- Top 3 areas for improvement
- Priority issues

### Detailed Findings

```markdown
## [Category]: [Issue Title]

**Severity**: High/Medium/Low
**Location**: [Page/Component]

**Issue**: 
[Description của problem]

**Impact**:
[Tại sao đây là problem]

**Recommendation**:
[Cách fix cụ thể]

**Reference**:
[Link to guideline/best practice]
```

---

## Severity Levels

| Level | Criteria | Action |
|-------|----------|--------|
| **Critical** | Blocks users, accessibility violation | Fix immediately |
| **High** | Significant UX issue | Fix before launch |
| **Medium** | Notable improvement | Plan to fix |
| **Low** | Nice-to-have | Consider for future |

---

## Review Checklist Quick Reference

### Must Have (Critical)
- [ ] Content readable
- [ ] Navigation works
- [ ] Forms functional
- [ ] Mobile usable
- [ ] Key actions accessible

### Should Have (High)
- [ ] Visual hierarchy clear
- [ ] Feedback on actions
- [ ] Error handling graceful
- [ ] Loading states present
- [ ] Consistent styling

### Nice to Have (Medium/Low)
- [ ] Micro-interactions
- [ ] Animation polish
- [ ] Edge case handling
- [ ] Advanced accessibility
- [ ] Performance optimization

---

## Design Principles Reference

### Visual Hierarchy
1. Size - Larger = more important
2. Color - Bolder/brighter = more important
3. Position - Top/left = first seen
4. Spacing - More white space = emphasis
5. Typography - Weight and style differentiate

### Gestalt Principles
- **Proximity** - Group related items
- **Similarity** - Similar appearance = related
- **Continuity** - Eye follows lines/curves
- **Closure** - Brain completes incomplete shapes
- **Figure/Ground** - Distinguish foreground from background

### F-Pattern & Z-Pattern
- F-pattern for text-heavy pages
- Z-pattern for minimal content
- Place important elements in these scan paths

---

## Common Issues Catalog

### Typography Issues
| Issue | Impact | Fix |
|-------|--------|-----|
| Too many fonts | Chaotic look | Max 2-3 fonts |
| Poor contrast | Hard to read | Min 4.5:1 ratio |
| Long lines | Eye strain | Max 75 characters |
| Tight spacing | Dense, hard to scan | Increase line height |

### Layout Issues
| Issue | Impact | Fix |
|-------|--------|-----|
| No visual hierarchy | Confusion | Size/weight variation |
| Cramped spacing | Overwhelming | 8px grid system |
| Misalignment | Unprofessional | Strict alignment grid |
| Inconsistent margins | Disjointed | Design tokens |

### UX Issues
| Issue | Impact | Fix |
|-------|--------|-----|
| Hidden navigation | Lost users | Visible, clear nav |
| No feedback | Uncertainty | Loading/success states |
| Unclear CTAs | Low conversion | Clear, contrasting buttons |
| Complex forms | Abandonment | Progressive disclosure |

---

## Tools for Review

| Tool | Purpose |
|------|---------|
| Browser DevTools | Inspect elements, test responsive |
| WAVE | Accessibility audit |
| Lighthouse | Performance + accessibility |
| Contrast Checker | Color accessibility |
| Responsively | Multi-device preview |
