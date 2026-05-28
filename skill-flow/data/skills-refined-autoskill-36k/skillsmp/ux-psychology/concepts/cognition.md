# Cognition & Perception

Managing mental effort and attention in user interfaces.

---

## Cognitive Load

**Definition**: The mental energy required for users to process and understand information.

**Implementation Guidelines**:
- Split forms with many fields across multiple pages
- Group items by category
- Remove unnecessary fields to minimize cognitive burden

```jsx
// Bad: Requesting all inputs at once
<Form>
  <Input name="name" />
  <Input name="email" />
  <Input name="phone" />
  <Input name="address" />
  <Input name="city" />
  <Input name="postalCode" />
  <Input name="country" />
  <Input name="cardNumber" />
  // ... many more fields
</Form>

// Good: Split into steps
<MultiStepForm>
  <Step title="Basic Info">
    <Input name="name" />
    <Input name="email" />
  </Step>
  <Step title="Shipping">
    <Input name="address" />
    <Input name="city" />
  </Step>
</MultiStepForm>
```

---

## Selective Attention

**Definition**: The tendency to focus on relevant information while ignoring irrelevant stimuli in information-rich environments.

**Implementation Guidelines**:
- Make important information visually prominent
- Establish clear information hierarchy
- Avoid overusing banners and CTAs

---

## Banner Blindness

**Definition**: The unconscious tendency to ignore banner-like content on websites.

**Implementation Guidelines**:
- Don't display critical information in banner format
- Use designs that integrate with content
- Consider native content formats
