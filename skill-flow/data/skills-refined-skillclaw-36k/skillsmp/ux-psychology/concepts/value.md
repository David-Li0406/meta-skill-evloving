# Value Perception

Creating and communicating perceived value.

---

## Loss Aversion

**Definition**: The emotional preference to avoid losses over acquiring gains.

**Implementation Guidelines**:
- Show what users will lose on cancellation
- Display limited-time offer deadlines
- Use "Don't miss out" messaging

```jsx
// Loss aversion implementation
<CancellationModal>
  <Warning>
    You will lose access to:
    <List>
      <Item>Your favorites (128 items)</Item>
      <Item>Watch history</Item>
      <Item>Exclusive content</Item>
    </List>
  </Warning>
</CancellationModal>
```

---

## Scarcity Effect

**Definition**: Perceiving limited availability items as more valuable.

**Implementation Guidelines**:
- Display stock quantities
- Emphasize limited-time offers
- Show popularity indicators

```jsx
// Scarcity display
<ProductCard>
  <Badge type="rare">Rare Find</Badge>
  <Stock>Only 3 left</Stock>
  <Timer>Sale ends in 2:34:56</Timer>
</ProductCard>
```

---

## Endowment Effect

**Definition**: Overvaluing things we already possess.

**Implementation Guidelines**:
- Offer personalization
- Implement customization features
- Use "Your own" expressions

```jsx
// Endowment effect implementation
<Onboarding>
  <Question>How will you use this?</Question>
  <Options>
    <Option>Personal</Option>
    <Option>Team</Option>
    <Option>Enterprise</Option>
  </Options>
  <Message>Preparing your personalized setup...</Message>
</Onboarding>
```

---

## Sunk Cost Effect

**Definition**: The tendency to continue investing to justify past investments.

**Implementation Guidelines**:
- Visualize progress
- Show invested time and effort
- Provide incentives for continuation
