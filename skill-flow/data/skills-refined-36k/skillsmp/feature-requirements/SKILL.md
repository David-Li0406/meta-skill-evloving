---
name: feature-requirements
description: Product requirements for FanHub features. Use when creating new pages, components, or user-facing functionality to ensure features meet product standards.
---

# FanHub Feature Requirements

When building new features or components for FanHub, ensure the following product requirements are met:

## 1. Error Handling

- **Error Boundaries**: Wrap all public pages in error boundaries
- **Async Error Handling**: Use try-catch for all async operations
- **User-Friendly Messages**: Show meaningful errors, not stack traces
- **Error Logging**: Log errors to console in development mode

Example:
```javascript
try {
  const data = await fetchCharacters();
  setCharacters(data);
} catch (error) {
  console.error('Failed to load characters:', error);
  toast.error('Unable to load characters. Please try again.');
}
```

## 2. User Feedback

- **Loading States**: Use skeleton screens, not spinners
- **Success Notifications**: Toast notifications for successful actions
- **Error Notifications**: Toast notifications for failures
- **Confirmations**: Dialog prompts before destructive actions

Example (loading state):
```jsx
{isLoading ? (
  <CharacterCardSkeleton count={6} />
) : (
  <CharacterGrid characters={characters} />
)}
```

## 3. Analytics & Tracking

- **Page Views**: Track on component mount
- **User Events**: Track all interactions (clicks, form submissions, etc.)
- **Naming Convention**: Use format: `fanhub_[page]_[action]`

Example:
```javascript
useEffect(() => {
  trackPageView('characters_list');
}, []);

const handleCharacterClick = (character) => {
  trackEvent('fanhub_characters_list_character_clicked', {
    character_id: character.id
  });
};
```

## 4. Accessibility

- **Semantic HTML**: Use proper elements (`<button>`, `<nav>`, `<main>`)
- **ARIA Labels**: Add where semantic HTML isn't enough
- **Keyboard Navigation**: Ensure tab order and keyboard shortcuts
- **Focus Management**: Handle focus on modals, navigation

Example:
```jsx
<button
  onClick={handleClick}
  aria-label={`View details for ${character.name}`}
>
  <CharacterCard character={character} />
</button>
```

## 5. Responsive Design

- **Mobile-First**: Design for mobile, enhance for desktop
- **Breakpoints**: 640px (sm), 768px (md), 1024px (lg)
- **Touch Targets**: Minimum 44px for interactive elements
- **Flexible Layouts**: Use flexbox/grid, avoid fixed widths

## When to Apply

Use this skill when:
- Creating new pages or routes
- Building new React components
- Implementing user interactions
- Adding forms or data entry
- Building modal dialogs or overlays
