# Component Patterns Reference

Quick reference for building components with zero hardcoded content and inline editor support.

## Data Attribute Quick Reference

```tsx
// Required on ALL editable elements
data-cms-entry="entry-slug"     // e.g., "homepage", "global-navigation"
data-cms-field="path.to.field"  // e.g., "hero.title", "menuLinks[0].label"

// Optional
data-cms-type="fieldType"       // text, richtext, image, array, object
data-cms-label="Display Name"   // Human-readable label
data-cms-readonly="true"        // Show but don't allow editing
```

## Common Patterns

### Simple Text
```tsx
<h1 data-cms-entry={entry} data-cms-field="hero.title">
  {title}
</h1>
```

### Image

**IMPORTANT:** Always use `data-cms-type="image"` for image fields. Do NOT use `"url"` - it will render as a text input instead of the image picker.

```tsx
<Image
  src={imageSrc}
  alt={imageAlt}
  data-cms-entry={entry}
  data-cms-field="hero.image"
  data-cms-type="image"
/>
```

For Next.js Image components inside wrapper divs, put the CMS attributes on the wrapper:

```tsx
<div
  data-cms-entry={entry}
  data-cms-field="hero.image"
  data-cms-type="image"
  data-cms-label="Hero Image"
>
  <Image src={imageSrc} alt="" fill className="object-cover" />
</div>
```

### Link with Text
```tsx
<Link
  href={link.href}
  data-cms-entry={entry}
  data-cms-field={`menuLinks[${index}].label`}
>
  {link.label}
</Link>
```

### Button
```tsx
<Button
  onClick={handleClick}
  data-cms-entry={entry}
  data-cms-field="hero.buttonText"
>
  {buttonText}
</Button>
```

### Rich Text / HTML
```tsx
<div
  data-cms-entry={entry}
  data-cms-field="content.body"
  data-cms-type="richtext"
  dangerouslySetInnerHTML={{ __html: bodyHtml }}
/>
```

### Array Container
```tsx
<section
  data-cms-entry={entry}
  data-cms-field="team"
  data-cms-type="array"
  data-cms-label="Team Members"
>
  {items.map((item, index) => (
    <div key={index}>
      <h3 data-cms-entry={entry} data-cms-field={`team[${index}].name`}>
        {item.name}
      </h3>
    </div>
  ))}
</section>
```

### Form Placeholder (Read-only)
```tsx
<input
  placeholder={placeholder}
  data-cms-entry={entry}
  data-cms-field="form.emailPlaceholder"
  data-cms-readonly="true"
/>
```

### Global Content
```tsx
// Navigation
<span data-cms-entry="global-navigation" data-cms-field="ctaButtonText">
  {ctaButtonText}
</span>

// Footer
<span data-cms-entry="global-footer" data-cms-field="copyrightText">
  {copyrightText}
</span>

// Site Settings
<Image
  src={logoUrl}
  alt={logoAlt}
  data-cms-entry="global-settings"
  data-cms-field="logoUrl"
  data-cms-type="image"
/>
```

## Entry Slug Conventions

| Content | Entry Slug |
|---------|------------|
| Site Settings | `global-settings` |
| Navigation | `global-navigation` |
| Footer | `global-footer` |
| Homepage | `homepage` or `home` |
| About Page | `about` |
| Contact Page | `contact` |
| 404 Page | `404` |

## Field Path Syntax

```
hero.title              → entry.data.hero.title
hero.images[0].src      → entry.data.hero.images[0].src
sections[2].items[0]    → entry.data.sections[2].items[0]
info.hours.weekday      → entry.data.info.hours.weekday
```

## Editable Helper Component

Use for cleaner JSX:

```tsx
import { Editable } from '@/components/shared/Editable';

<Editable entry="homepage" field="hero.title" as="h1" className="text-4xl">
  {hero.title}
</Editable>
```
