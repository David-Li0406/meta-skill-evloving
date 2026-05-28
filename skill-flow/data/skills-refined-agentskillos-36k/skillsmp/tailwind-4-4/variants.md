# Tailwind 4.1+ — Variants

## Form (post-interaction)
`user-valid:` `user-invalid:` — triggers after user interacts, not on page load

## Structural
`nth-*:` `nth-last-*:` — `nth-3:`, `nth-[3n+1]:`, `nth-last-2:`

## Ancestor (replaces group)
`in-[.sidebar]:` `in-[[data-open]]:` `in-hover:`

## Has (child matching)
`has-[:checked]:` `has-[input:focus]:` `has-[[data-active]]:`

## Pseudo-elements
`selection:` `marker:` `file:` `backdrop:` `first-letter:`

## State
`open:` `starting:` `inert:` `modal:`

## Accessibility
`contrast-more:` `forced-colors:`

## Media
`noscript:`

## Device
`pointer-fine:` `pointer-coarse:` `hover-hover:` `hover-none:`

## Negation
`not-hover:` `not-focus:` `not-disabled:` `not-first:` `not-has-[]:`

## Descendants
`*:` (direct) `**:` (all) `details-content:`

## Container Queries
`@container` `@sm:` `@md:` `@lg:` `@xl:`

Named: `@container/card` + `@md/card:flex-row`
Range: `@min-sm:@max-lg:hidden`

## Custom Variants

```css
@custom-variant scrolled (&:where([data-scrolled], [data-scrolled] *));
```

Usage: `scrolled:shadow-lg scrolled:border-border`
