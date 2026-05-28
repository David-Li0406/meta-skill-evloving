# Behavioral Guidance

Techniques to influence user decisions.

---

## Nudge Effect

**Definition**: Non-coercive techniques to guide user decisions toward desired outcomes.

**Implementation Guidelines**:
- Implement recommendation features
- Set optimal default values
- Use visual hints to encourage actions

```jsx
// Nudge implementation example
<ProductRecommendation>
  <Title>Recommended for You</Title>
  <ProductList items={recommendations} />
</ProductRecommendation>
```

---

## Default Bias

**Definition**: The tendency to stick with default options.

**Implementation Guidelines**:
- Set the optimal choice as default
- Design opt-in/opt-out appropriately
- Use strategic preset values

```jsx
// Leveraging default effect
<SubscriptionOptions>
  <Option selected={true}>Annual Plan (Save 20%)</Option>
  <Option>Monthly Plan</Option>
</SubscriptionOptions>
```

---

## Decoy Effect

**Definition**: Introducing a decoy option to make other options appear more attractive.

**Implementation Guidelines**:
- Present 3 pricing options
- Design the middle option as a decoy
- Highlight the plan you want to sell most

```jsx
// Decoy effect pricing table
<PricingTable>
  <Plan name="Basic" price="$9">Basic features</Plan>
  <Plan name="Standard" price="$24" decoy>Partial features</Plan>
  <Plan name="Premium" price="$29" recommended>All features</Plan>
</PricingTable>
```

---

## Foot in the Door Effect

**Definition**: After accepting a small request, people are more likely to accept larger requests.

**Implementation Guidelines**:
- Start with simple actions
- Gradually deepen commitment
- Apply to cross-sell and upsell

```jsx
// Foot in the door implementation
<CheckoutFlow>
  <Step1>Add to Cart</Step1>
  <Step2>
    <CrossSell>Frequently Bought Together</CrossSell>
  </Step2>
  <Step3>Complete Purchase</Step3>
</CheckoutFlow>
```

---

## Framing Effect

**Definition**: How the presentation of information influences decisions.

**Implementation Guidelines**:
- Use positive expressions
- Present numbers strategically
- Organize information with categories

```jsx
// Framing example
// Bad
<Message>10% chance of failure</Message>

// Good
<Message>90% success rate</Message>
```

---

## Priming Effect

**Definition**: How prior stimuli unconsciously influence subsequent behavior.

**Implementation Guidelines**:
- Ask about satisfaction before review requests
- Start with positive questions
- Use visual suggestions

```jsx
// Priming implementation (review request)
<ReviewPrompt>
  <SatisfactionCheck>
    Are you enjoying the app?
    <StarRating value={5} display />
  </SatisfactionCheck>
  <PositiveButton>Yes, I love it!</PositiveButton>
  <NegativeButton>Not really</NegativeButton>
</ReviewPrompt>
```
