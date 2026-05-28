# Template Cloning Workflow

Step-by-step process for cloning and customizing templates.

---

## Phase 1: Research Templates

### Find Candidates

**Search strategy**:
```
GitHub: "{framework} landing page template" stars:>500
GitHub: "{framework} dashboard template" stars:>500
Awesome lists: "awesome-{framework}-templates"
```

**Evaluation criteria**:
| Criteria | Weight | Check |
|----------|--------|-------|
| Stars/Activity | High | Recent commits, active issues |
| Tech Stack Match | High | Same framework, compatible UI library |
| Design Quality | Medium | Screenshots, demo site |
| Documentation | Medium | README, setup instructions |
| License | High | MIT/Apache for commercial use |

### Document Selection

```markdown
## Template Selection: {Project Name}

**Chosen**: {template name} ({url})
**Stars**: {count}
**Stack**: {React/Vue/etc} + {Tailwind/etc}
**Why**: {1-2 sentences}

**Alternatives considered**:
- {template 2}: {why not chosen}
- {template 3}: {why not chosen}
```

---

## Phase 2: Analyze Reference Site

### Extract Design Tokens

**Colors**:
```javascript
// Browser DevTools Console
// Get computed background color
getComputedStyle(document.body).backgroundColor
// "rgb(14, 14, 14)" → HSL: 0 0% 5.5%
```

**Convert to HSL** (for CSS variables):
```
RGB → HSL converter: https://www.rapidtables.com/convert/color/rgb-to-hsl.html
```

**Fonts**:
```javascript
// Get font family
getComputedStyle(document.querySelector('h1')).fontFamily
// "Satoshi, system-ui, sans-serif"

// Get font weight
getComputedStyle(document.querySelector('h1')).fontWeight
// "300" (light)
```

**Spacing**:
```javascript
// Get section padding
getComputedStyle(document.querySelector('section')).padding
// "96px 0px" → py-24 in Tailwind
```

### Automated Extraction (Optional)

Use Playwright for comprehensive extraction:

```python
# analyze_website.py
from playwright.sync_api import sync_playwright

def extract_styles(url):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url, wait_until="networkidle")

        # Extract colors
        bg_color = page.evaluate('''
            getComputedStyle(document.body).backgroundColor
        ''')

        # Extract fonts
        heading_font = page.evaluate('''
            getComputedStyle(document.querySelector('h1')).fontFamily
        ''')

        # Take screenshot
        page.screenshot(path="reference.png", full_page=True)

        browser.close()
        return {"bg": bg_color, "heading_font": heading_font}
```

### Document Findings

```markdown
## Style Analysis: {reference site}

### Colors
- Background: #0E0E0E (HSL: 0 0% 5.5%)
- Foreground: #E8E4DE (HSL: 38 25% 90%)
- Primary: #DAC5A7 (HSL: 38 35% 75%)
- Border: #2A2520 (HSL: 38 15% 18%)

### Typography
- Heading: Satoshi (font-light, tracking-wide)
- Body: Satoshi (font-normal)
- Accent: Georgia (italic)
- Letter-spacing: 0.05em (elegant), 0.1em (wide)

### Spacing
- Section padding: py-24 (96px)
- Container max-width: 1280px
- Card gap: gap-6 (24px)

### Patterns
- Hero: Centered, circular image, split title
- CTA: Gold button, arrow icon on hover
- Cards: Subtle border, bg-card on hover
```

---

## Phase 3: Clone Template

### Setup

```bash
# Clone template
git clone {template-url} {project-name}
cd {project-name}

# Remove git history (start fresh)
rm -rf .git

# Install dependencies
npm install

# Verify it runs
npm run dev
```

### Strip Placeholder Content

```bash
# Find placeholder text
grep -r "Lorem" src/
grep -r "example.com" src/
grep -r "placeholder" src/

# Find placeholder images
grep -r "via.placeholder" src/
grep -r "unsplash" src/
```

---

## Phase 4: Create Content Configuration

### Structure

```typescript
// src/config/content.ts

// Site-wide configuration
export const siteConfig = {
  name: "Your Name",
  title: "Your Title",
  titleAccent: "& Specialty",  // Italic accent
  tagline: "Your value proposition...",
  cta: {
    text: "Get Started",
    href: "https://calendly.com/...",
  },
};

// Navigation
export const navLinks = [
  { label: "Services", href: "#services" },
  { label: "About", href: "#about" },
];

// Typed arrays with interfaces
export interface Service {
  title: string;
  description: string;
  icon: string;
}

export const services: Service[] = [
  {
    title: "Service 1",
    description: "Description...",
    icon: "IconName",
  },
];

// Continue for all content sections...
```

### Content Sections Checklist

- [ ] `siteConfig` - Name, title, tagline, CTA
- [ ] `navLinks` - Navigation menu items
- [ ] `services` - Service offerings
- [ ] `testimonials` - Customer quotes
- [ ] `faqItems` - FAQ questions/answers
- [ ] `footerLinks` - Footer navigation
- [ ] `aboutContent` - About section text + stats

---

## Phase 5: Apply Theme

### CSS Variables

```css
/* src/App.css or globals.css */
.dark {
  /* Background colors */
  --background: 0 0% 5.5%;
  --foreground: 38 25% 90%;

  /* Primary accent */
  --primary: 38 35% 75%;
  --primary-foreground: 0 0% 5%;

  /* Card styling */
  --card: 0 0% 8%;
  --card-foreground: 38 25% 90%;

  /* Borders */
  --border: 38 15% 18%;

  /* Muted text */
  --muted: 0 0% 12%;
  --muted-foreground: 38 10% 60%;
}
```

### Tailwind Config

```javascript
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      fontFamily: {
        sans: ['Satoshi', 'system-ui', 'sans-serif'],
        display: ['Georgia', 'serif'],
      },
      letterSpacing: {
        elegant: '0.05em',
        wide: '0.1em',
      },
    },
  },
};
```

### Font Loading

```html
<!-- index.html -->
<link href="https://api.fontshare.com/v2/css?f[]=satoshi@300,400,500,700&display=swap" rel="stylesheet">
```

---

## Phase 6: Update Components

### Pattern: Import from Config

```tsx
// Before
const services = [
  { title: "Service 1", description: "Lorem ipsum..." },
];

// After
import { services } from "@/config/content";

export const Services = () => {
  return (
    <section>
      {services.map((service) => (
        <ServiceCard key={service.title} {...service} />
      ))}
    </section>
  );
};
```

### Component Update Checklist

For each component:
- [ ] Import relevant config
- [ ] Replace hardcoded content with config values
- [ ] Apply theme classes (font-light, tracking-elegant, etc.)
- [ ] Update colors to use CSS variables (text-primary, bg-card)
- [ ] Remove unused imports

---

## Phase 7: Verify

### Build Check

```bash
# TypeScript + build
npm run build

# Should complete without errors
```

### Visual Check

```bash
npm run dev
# Open http://localhost:5173
```

**Verify at each breakpoint**:
- [ ] Mobile (320px)
- [ ] Tablet (768px)
- [ ] Desktop (1024px)
- [ ] Wide (1440px)

### Content Check

```bash
# No placeholder content
grep -r "Lorem" src/
grep -r "placeholder" src/
# Should return empty
```

### Font Check

1. Open DevTools → Network tab
2. Filter by "Font"
3. Verify font files loaded (Satoshi, etc.)

---

## Artifacts

After completing workflow, you should have:

1. **Content config** (`src/config/content.ts`)
2. **Theme CSS** (CSS variables in App.css)
3. **Tailwind config** (fonts, spacing)
4. **Updated components** (using config imports)
5. **Successful build** (no TS errors)

---

## Time Estimates

| Phase | Typical Time |
|-------|-------------|
| Research | 15-30 min |
| Analyze | 30-60 min |
| Clone | 5-10 min |
| Configure | 30-45 min |
| Theme | 15-30 min |
| Customize | 1-2 hours |
| Verify | 15-30 min |
| **Total** | **3-5 hours** |

Compare to building from scratch: 2-4 days
