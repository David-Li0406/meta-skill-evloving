# Biases

Leveraging cognitive shortcuts in decision-making.

---

## Anchor Effect

**Definition**: The tendency to evaluate subsequent information based on initially presented information.

**Implementation Guidelines**:
- Display original price before discounted price
- Show recommended plans first
- Clearly establish reference points in comparison tables

```jsx
// Price anchoring example
<PriceDisplay>
  <OriginalPrice>$100</OriginalPrice>
  <CurrentPrice>$79.80</CurrentPrice>
  <Discount>20% OFF</Discount>
</PriceDisplay>
```

---

## Confirmation Bias

**Definition**: The tendency to favor information that confirms existing beliefs.

**Implementation Guidelines**:
- Collect objective data through A/B testing
- Analyze user feedback without bias
- Use data to inform design decisions

---

## Expectation Bias

**Definition**: How prior expectations influence actual experience evaluation.

**Implementation Guidelines**:
- Build positive impressions through branding
- Create anticipation before loading
- Maintain consistent high-quality UI

---

## Familiarity Bias

**Definition**: The tendency to prefer designs and features previously experienced.

**Implementation Guidelines**:
- Adopt common UI patterns
- Place navigation at the top
- Use standard icons

```jsx
// Navigation considering familiarity
<Header>
  <Logo />
  <Navigation>
    <NavItem>Home</NavItem>
    <NavItem>Services</NavItem>
    <NavItem>Contact</NavItem>
  </Navigation>
  <UserMenu />
</Header>
```
