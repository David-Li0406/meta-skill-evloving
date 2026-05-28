# Config-Driven Content Pattern

Centralize all editable content in a single configuration file.

**Related skill**: For conversion-optimized content structure, see [sales-landing-page](../sales-landing-page/) skill which provides a 14-section psychological framework.

---

## Why Config-Driven?

### Problems with Scattered Content

```tsx
// Hero.tsx
<h1>Welcome to Our Platform</h1>
<p>We help businesses grow with AI automation.</p>

// Footer.tsx
<span>Welcome to Our Platform</span>  // Duplicated!
```

**Issues**:
- Content scattered across 10+ files
- Duplicated strings (name, tagline)
- Non-developers can't edit content
- Risk of inconsistency
- Hard to A/B test copy

### Solution: Single Config File

```typescript
// src/config/content.ts
export const siteConfig = {
  name: "Our Platform",
  tagline: "We help businesses grow with AI automation.",
};

// Hero.tsx
import { siteConfig } from "@/config/content";
<h1>Welcome to {siteConfig.name}</h1>
<p>{siteConfig.tagline}</p>

// Footer.tsx
<span>{siteConfig.name}</span>
```

**Benefits**:
- Single source of truth
- Easy content updates
- Non-developers can edit
- Consistent across components
- Simple A/B testing

---

## Config File Structure

### Complete Template

```typescript
// src/config/content.ts

/**
 * Landing Page Content Configuration
 * Edit this file to customize all content on the landing page
 */

// ============================================
// Site Configuration
// ============================================
export const siteConfig = {
  name: "Your Name",
  title: "Your Title",
  titleAccent: "& Specialty",  // Displayed in italic/accent font
  tagline: "Your value proposition in one sentence.",
  cta: {
    text: "Get Started",
    href: "https://calendly.com/your-link",
  },
  available: true,  // Shows availability indicator
};

// ============================================
// Navigation
// ============================================
export const navLinks = [
  { label: "Services", href: "#services" },
  { label: "Process", href: "#process" },
  { label: "About", href: "#about" },
  { label: "FAQ", href: "#faq" },
];

// ============================================
// Client Logos (Social Proof)
// ============================================
export const clientLogos = [
  { name: "Company 1", logo: "/logos/company1.svg" },
  { name: "Company 2", logo: "/logos/company2.svg" },
  // Add more...
];

// ============================================
// Services
// ============================================
export interface Service {
  title: string;
  description: string;
  icon: string;  // Lucide icon name
}

export const services: Service[] = [
  {
    title: "Service Name",
    description: "What this service does and the value it provides.",
    icon: "Zap",  // From lucide-react
  },
  // Add more...
];

// ============================================
// Process Steps (Timeline)
// ============================================
export interface ProcessStep {
  step: string;      // "01", "02", etc.
  title: string;
  subtitle: string;  // Short label above title
  description: string;
  duration?: string; // e.g., "1 HOUR", "FREE"
  items: string[];   // Bullet points
}

export const processSteps: ProcessStep[] = [
  {
    step: "01",
    title: "Discovery Call",
    subtitle: "LET'S TALK",
    description: "We discuss your goals and challenges.",
    duration: "FREE 30 MIN",
    items: [
      "Understand your business",
      "Identify opportunities",
      "Determine if we're a fit",
    ],
  },
  // Add more...
];

// ============================================
// Testimonials
// ============================================
export interface Testimonial {
  companyLogo: string;
  quote: string;
  description: string;
  author: {
    name: string;
    title: string;
    image: string;
  };
}

export const testimonials: Testimonial[] = [
  {
    companyLogo: "/logos/client1.svg",
    quote: "The headline testimonial quote.",
    description: "More detailed testimonial text...",
    author: {
      name: "John Smith",
      title: "CEO at Company",
      image: "/avatars/john.jpg",
    },
  },
  // Add more...
];

// ============================================
// FAQ
// ============================================
export interface FAQItem {
  question: string;
  answer: string;
}

export const faqItems: FAQItem[] = [
  {
    question: "How does it work?",
    answer: "We follow a simple 3-step process...",
  },
  // Add more...
];

// ============================================
// Footer
// ============================================
export const footerLinks = {
  social: [
    { label: "LinkedIn", href: "https://linkedin.com/...", icon: "Linkedin" },
    { label: "Twitter", href: "https://twitter.com/...", icon: "Twitter" },
  ],
  legal: [
    { label: "Privacy Policy", href: "/privacy" },
    { label: "Terms of Service", href: "/terms" },
  ],
};

// ============================================
// About Section
// ============================================
export const aboutContent = {
  title: "About",
  description: `Your story and background.
    Can be multi-line using template literals.`,
  stats: [
    { value: "100+", label: "Projects" },
    { value: "50+", label: "Clients" },
    { value: "5+", label: "Years" },
  ],
};
```

---

## Usage in Components

### Basic Import

```tsx
// components/Hero.tsx
import { siteConfig } from "@/config/content";

export const Hero = () => {
  return (
    <section>
      <h1>{siteConfig.title}</h1>
      <p>{siteConfig.tagline}</p>
      <a href={siteConfig.cta.href}>{siteConfig.cta.text}</a>
    </section>
  );
};
```

### Mapping Arrays

```tsx
// components/Services.tsx
import { services } from "@/config/content";

export const Services = () => {
  return (
    <section>
      {services.map((service, index) => (
        <ServiceCard key={index} {...service} />
      ))}
    </section>
  );
};
```

### Icon Mapping

For dynamic icons (Lucide, etc.):

```tsx
import { services, Service } from "@/config/content";
import * as Icons from "lucide-react";

// Type-safe icon lookup
const iconMap: Record<string, React.ComponentType<{ className?: string }>> = {
  Zap: Icons.Zap,
  Bot: Icons.Bot,
  Send: Icons.Send,
  // Add icons used in config
};

export const ServiceCard = ({ title, description, icon }: Service) => {
  const Icon = iconMap[icon] || Icons.HelpCircle;

  return (
    <div>
      <Icon className="h-6 w-6" />
      <h3>{title}</h3>
      <p>{description}</p>
    </div>
  );
};
```

---

## TypeScript Benefits

### Type Safety

```typescript
// Interfaces ensure correct structure
export interface Service {
  title: string;      // Required
  description: string; // Required
  icon: string;        // Required
}

// TypeScript catches errors
const services: Service[] = [
  { title: "Test" },  // Error: missing description, icon
];
```

### Autocomplete

```tsx
// IDE shows available properties
siteConfig.  // Shows: name, title, tagline, cta, etc.
```

### Refactoring Support

```typescript
// Rename property → updates all usages
siteConfig.tagline → siteConfig.subtitle
```

---

## Best Practices

### DO

- **Group related content** (site, nav, services, etc.)
- **Use interfaces** for complex types
- **Use template literals** for multi-line text
- **Keep config flat** (avoid deep nesting)
- **Document with comments** (section headers)

### DON'T

- **Don't put logic in config** (only data)
- **Don't include components** (just strings/objects)
- **Don't duplicate values** (use references)
- **Don't nest too deeply** (max 2 levels)

---

## A/B Testing

Config-driven content enables easy A/B testing:

```typescript
// src/config/content.ts
const variant = localStorage.getItem('ab_variant') || 'A';

export const siteConfig = {
  tagline: variant === 'A'
    ? "Transform your business with AI"
    : "Scale efficiently with automation",
  // ...
};
```

Or separate config files:

```typescript
// src/config/content-a.ts
// src/config/content-b.ts

// App.tsx
import { siteConfig } from `@/config/content-${variant}`;
```

---

## Migration Checklist

When converting existing components:

- [ ] Create `src/config/content.ts`
- [ ] Add `siteConfig` with name, title, tagline, CTA
- [ ] Add `navLinks` array
- [ ] Add content arrays (services, testimonials, FAQ)
- [ ] Add `footerLinks` and `aboutContent`
- [ ] Update each component to import from config
- [ ] Search for hardcoded strings: `grep -r "Lorem" src/`
- [ ] Verify no placeholder content remains
- [ ] Test all sections render correctly
