# UI Design Principles

Visual and interaction patterns based on psychology.

---

## Doherty Threshold

**Definition**: Waiting over 0.4 seconds increases disengagement risk.

**Implementation Guidelines**:
- Keep response time under 400ms
- Show skeleton UI for slow loads
- Provide immediate feedback

```jsx
// Skeleton UI implementation
<Card>
  {isLoading ? (
    <Skeleton>
      <SkeletonImage />
      <SkeletonText lines={3} />
    </Skeleton>
  ) : (
    <Content data={data} />
  )}
</Card>
```

---

## Progressive Disclosure

**Definition**: Revealing information and features gradually.

**Implementation Guidelines**:
- Start simple
- Show details on demand
- Hide advanced features initially

```jsx
// Progressive disclosure implementation
<Navigation>
  <MainMenu>
    <MenuItem>Products</MenuItem>
    <MenuItem>
      Categories
      <SubMenu> {/* Shows on hover */}
        <SubItem>Men's</SubItem>
        <SubItem>Women's</SubItem>
      </SubMenu>
    </MenuItem>
  </MainMenu>
</Navigation>
```

---

## Visual Hierarchy

**Definition**: Organizing information with visual priority.

**Implementation Guidelines**:
- Make important elements larger and more prominent
- Consider F-pattern and Z-pattern eye movement
- Use whitespace effectively

```css
/* Visual hierarchy CSS example */
.heading-1 { font-size: 2.5rem; font-weight: 700; }
.heading-2 { font-size: 1.75rem; font-weight: 600; }
.body-text { font-size: 1rem; font-weight: 400; }
.caption { font-size: 0.875rem; color: #666; }

.cta-primary { background: #007AFF; color: white; }
.cta-secondary { background: transparent; border: 1px solid #007AFF; }
```

---

## Visual Anchor

**Definition**: Using visual emphasis to draw attention to specific elements.

**Implementation Guidelines**:
- Make CTA buttons stand out
- Use contrast effectively
- Use motion to capture attention

---

## Serial Position Effect

**Definition**: First and last items in a list are remembered best.

**Implementation Guidelines**:
- Place important items first or last
- Keep navigation to 5 items or fewer
- Put primary functions at menu edges

```jsx
// Navigation considering serial position effect
<BottomNav>
  <NavItem icon="home" important />  {/* First */}
  <NavItem icon="search" />
  <NavItem icon="notifications" />
  <NavItem icon="profile" important />  {/* Last */}
</BottomNav>
```

---

## Skeuomorphism

**Definition**: Mimicking real-world objects in digital UI.

**Implementation Guidelines**:
- Useful when introducing new concepts
- Promotes intuitive interaction
- Avoid overuse

---

## Aesthetic-Usability Effect

**Definition**: Beautiful designs are perceived as more usable.

**Implementation Guidelines**:
- Pursue visual beauty
- Pay attention to details
- Maintain consistent style
