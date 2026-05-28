# Experience Design

Creating memorable moments and interactions.

---

## Peak-End Rule

**Definition**: Experiences are evaluated by their peak moments and endings.

**Implementation Guidelines**:
- Add special effects at key moments
- Provide memorable completion experiences
- Handle errors gracefully

```jsx
// Peak-end implementation
<PurchaseComplete>
  <Confetti />
  <Message>Thank you for your purchase!</Message>
  <Illustration type="celebration" />
  <NextAction>View your order</NextAction>
</PurchaseComplete>
```

---

## User Delight

**Definition**: Joy and surprise from exceeding expectations.

**Implementation Guidelines**:
- Add micro-interactions
- Include easter eggs
- Provide unexpected pleasant features

```jsx
// Micro-interaction example
<LikeButton
  onClick={handleLike}
  animation={{
    scale: [1, 1.2, 1],
    transition: { duration: 0.3 }
  }}
>
  <HeartIcon filled={liked} />
</LikeButton>
```

---

## Labor Illusion

**Definition**: Showing effort increases perceived value.

**Implementation Guidelines**:
- Display processing steps during loading
- Show search generation process
- Intentionally add slight delays

```jsx
// Labor illusion implementation
<SearchLoading>
  <Spinner />
  <Status>
    <Step active>Searching 100+ sites...</Step>
    <Step>Comparing prices...</Step>
    <Step>Organizing results...</Step>
  </Status>
</SearchLoading>
```
