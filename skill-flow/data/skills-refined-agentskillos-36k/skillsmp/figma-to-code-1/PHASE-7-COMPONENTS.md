# Phase 7: Component Generation

**CRITICAL:** Every component must:
1. Accept ALL content via props — ZERO hardcoded strings
2. Include `data-cms-entry` and `data-cms-field` on ALL editable elements

> **IMPORTANT:** The examples below show PATTERNS.
> Create components ONLY for what exists in YOUR Figma.

## Step 0: Reference Component Inventory (Do First)

**BEFORE building any component, check `/project-config/components.md`.**

This file was generated in Phase 1 and contains:
- All components discovered in the Figma Components page
- Node IDs for each component (use with `get_design_context`)
- Variant information (Default, Hover, Disabled, etc.)
- Which pages use each component

### Workflow for Each Component

1. **Check inventory first:**
   ```
   Does this component exist in /project-config/components.md?
   → YES: Get the node ID and use get_design_context for exact specs
   → NO: This might be a page-specific section, not a reusable component
   ```

2. **Use correct node ID:**
   ```typescript
   // Get design specs from Figma using the node ID from components.md
   const designContext = await mcp__figma__get_design_context({
     fileKey,
     nodeId: "123:456"  // From components.md inventory
   });
   ```

3. **Build all variants:**
   If components.md shows variants (Default, Hover, Active), implement all states.

### Why This Matters

- **Prevents duplicate work** - Don't rebuild components that exist
- **Ensures consistency** - Use the same node ID across the build
- **Catches missing components** - If something isn't in inventory, it might need to be added to Figma

## Structural Fidelity Check

1. For each page, check if PDF exists in `/docs/figma-exports/`
2. Document structure in `/docs/component-inventory.md`
3. **Reference `/docs/design-tokens.md`** — use token values (colors, spacing, typography) instead of hardcoded pixels/hex values

## UI Components Pattern

All UI components must accept text via props:

```typescript
// ✗ WRONG - hardcoded text
export function Button({ onClick }) {
  return <button onClick={onClick}>Submit</button>;
}

// ✓ CORRECT - text via props
export function Button({ children, onClick }) {
  return <button onClick={onClick}>{children}</button>;
}
```

## Layout Component Pattern

```typescript
// EXAMPLE ONLY - adapt to YOUR design
interface NavigationProps {
  menuLinks: Array<{ label: string; href: string }>;
  logoUrl: string;
  logoAlt: string;
  // Add props based on YOUR navigation
}

export function Navigation({ menuLinks, logoUrl, logoAlt }: NavigationProps) {
  return (
    <nav>
      <Image
        src={logoUrl}
        alt={logoAlt}
        data-cms-entry="global-settings"
        data-cms-field="logoUrl"
        data-cms-type="image"
      />
      <ul>
        {menuLinks.map((link, index) => (
          <li key={link.href}>
            <Link
              href={link.href}
              data-cms-entry="global-navigation"
              data-cms-field={`menuLinks[${index}].label`}
            >
              {link.label}
            </Link>
          </li>
        ))}
      </ul>
    </nav>
  );
}
```

## Page Section Pattern

```typescript
// EXAMPLE - create sections based on YOUR Figma
interface SectionProps {
  entry: string;  // CMS entry slug for this page
  title: string;
  description?: string;
  imageSrc?: string;
}

export function HeroSection({ entry, title, description, imageSrc }: SectionProps) {
  return (
    <section>
      {imageSrc && (
        <Image
          src={imageSrc}
          alt=""
          data-cms-entry={entry}
          data-cms-field="hero.image"
          data-cms-type="image"
        />
      )}
      <h1 data-cms-entry={entry} data-cms-field="hero.title">
        {title}
      </h1>
      {description && (
        <p data-cms-entry={entry} data-cms-field="hero.description">
          {description}
        </p>
      )}
    </section>
  );
}
```

## Array Section Pattern

```typescript
// EXAMPLE - for team, FAQ, products, etc.
interface ArraySectionProps {
  entry: string;
  sectionTitle: string;
  items: Array<{ name: string; description: string; imageSrc?: string }>;
}

export function ArraySection({ entry, sectionTitle, items }: ArraySectionProps) {
  return (
    <section
      data-cms-entry={entry}
      data-cms-field="items"
      data-cms-type="array"
    >
      <h2 data-cms-entry={entry} data-cms-field="sectionTitle">
        {sectionTitle}
      </h2>
      {items.map((item, index) => (
        <div key={index}>
          <h3 data-cms-entry={entry} data-cms-field={`items[${index}].name`}>
            {item.name}
          </h3>
          <p data-cms-entry={entry} data-cms-field={`items[${index}].description`}>
            {item.description}
          </p>
        </div>
      ))}
    </section>
  );
}
```

## Verification Checklist

For EVERY component:
- [ ] No quoted strings render to users
- [ ] Every rendered string is a prop
- [ ] No default values contain user-facing text
- [ ] ALL elements with CMS content have `data-cms-entry`
- [ ] ALL elements with CMS content have `data-cms-field`
- [ ] Array items use indexed paths: `field[0].property`
- [ ] Images have `data-cms-type="image"` (NOT "url" - that shows text input instead of image picker)

## Git Commit

```bash
git commit -m "feat: components generated with zero hardcoded content and data attributes"
```

## Checkpoint

```bash
osascript -e 'display notification "Phase 7: Components generated" with title "Claude Code" sound name "Ping"'
```

**Next:** Proceed to [PHASE-8-PAGE-CONTENT.md](PHASE-8-PAGE-CONTENT.md)
