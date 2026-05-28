# Bold Pricing: A Manifesto

## The Problem

Users are tired of seeing the same manipulative 3-tier pricing everywhere. They know they're being boxed into the "recommended" middle option. **They see
through it.**

![The tired pattern](./tired-tiered-pricing.png)

Every SaaS looks like this. It's lazy. It's manipulative. And users are over it.

## Our Proposal

**Single tier. Annual. Honestly priced.**

No games. No "most popular" badges. No artificial scarcity. Just great software at a fair price.

### The New Pricing Component

```jsx live
const Container =
  ({ children }) => <div className="bold-pricing">{children}</div>;
const Card =
  ({ children }) => <article>{children}</article>;

export function BoldPricing() {
  return (
    <Container>
      <h2>One plan. Full access.</h2>
      <p>No tiers. No tricks. No "contact sales."</p>

      <Card>
        <small>Annual</small>
        <div className="price-row">
          <strong>$149</strong> /year
        </div>
        <p className="highlight">Less than 4 lattes a month.</p>

        <ul>
          <li>Unlimited projects</li>
          <li>100 GB storage</li>
          <li>Priority support</li>
          <li>Advanced analytics</li>
          <li>Custom integrations</li>
          <li>SSO</li>
        </ul>

        <button>Get Started →</button>
      </Card>

      <footer>
        <p>90 days to decide. Take your time.</p>
        <small>Cancel from your account. No hoops.</small>
      </footer>
    </Container>
  );
}
```

#### Design Tokens
The base design tokens are defined in the [Elementary Design System](../../../references/token-system.md). The component-specific styling is in [bold-pricing.css](./bold-pricing.css).

```css live
@import '../../../assets/elementary/tokens/polished.css';
@import './bold-pricing.css';

.bold-pricing {
  color-scheme: light ;
  /* INK */
  --c-text: light-dark(var(--c-slate-800), var(--c-slate-050));
  --c-muted: light-dark(var(--c-slate-500), var(--c-slate-400));

  /* ACCENT */
  --c-primary: light-dark(var(--c-rose-400), var(--c-emerald-400));
  --c-primary-hover: light-dark(var(--c-rose-500), var(--c-emerald-500));
  --c-on-primary: light-dark(var(--c-white), var(--c-slate-050));
}
```

## Next Steps

- [ ] Validate pricing with finance team
- [ ] A/B test against current 3-tier layout
- [ ] Prepare stakeholder presentation

> **Break out of the herd.**

---
*Created with [Reactive MD](https://marketplace.visualstudio.com/items?itemName=million-views.reactive-md)*
