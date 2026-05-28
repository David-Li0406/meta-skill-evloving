# Engagement

Driving continued use and habit formation.

---

## Gamification

**Definition**: Incorporating game elements to increase motivation.

**Implementation Guidelines**:
- Introduce points and badge systems
- Implement leaderboards and rankings
- Create sense of achievement

```jsx
// Gamification implementation
<UserProgress>
  <Level>Lv.15</Level>
  <XPBar current={750} max={1000} />
  <Streak days={7} />
  <Badges>
    <Badge name="Beginner" />
    <Badge name="7-Day Streak" />
  </Badges>
</UserProgress>
```

---

## Variable Reward

**Definition**: Unpredictable rewards that increase engagement.

**Implementation Guidelines**:
- Provide irregular bonuses
- Add surprise elements
- Create uncertainty about what comes next

---

## Goal Gradient Effect

**Definition**: Increased effort as goals approach.

**Implementation Guidelines**:
- Display progress bars
- Show remaining steps clearly
- Give initial progress boost

```jsx
// Goal gradient effect implementation
<LoyaltyCard>
  <Title>2 more for a free drink!</Title>
  <Progress current={8} total={10} />
  <Stamps filled={8} empty={2} />
</LoyaltyCard>
```

---

## Zeigarnik Effect

**Definition**: Incomplete tasks are remembered better than completed ones.

**Implementation Guidelines**:
- Use checklists
- Highlight incomplete tasks
- Display completion percentage

```jsx
// Zeigarnik effect implementation
<OnboardingChecklist>
  <Title>Complete your setup</Title>
  <Task completed>Profile settings</Task>
  <Task completed>Notification settings</Task>
  <Task>Add payment method</Task>
  <Task>Create first post</Task>
  <Progress>50% complete</Progress>
</OnboardingChecklist>
```

---

## Curiosity Gap

**Definition**: Creating information gaps that drive action to fill them.

**Implementation Guidelines**:
- Hide partial information to spark interest
- Use teaser content
- Implement "See more" patterns

```jsx
// Curiosity gap implementation
<MatchPreview>
  <BlurredImage src={match.photo} />
  <Message>Someone liked you</Message>
  <CTA>Upgrade to see who</CTA>
</MatchPreview>
```
