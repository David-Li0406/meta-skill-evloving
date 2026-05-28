---
name: epic-ui-guidelines
description: Use this skill when you need to create accessible UI components and follow design patterns for the Epic Stack.
---

# Epic Stack: UI Guidelines

## When to use this skill

Use this skill when you need to:
- Create accessible UI components
- Follow Epic Stack design patterns
- Use Tailwind CSS effectively
- Implement semantic HTML
- Add ARIA attributes correctly
- Create responsive layouts
- Ensure proper form accessibility
- Follow Epic Stack's UI component conventions

## Patterns and conventions

### UI Philosophy

Following Epic Web principles:

**Software is built for people, by people** - Accessibility isn't about checking boxes or meeting standards. It's about creating software that works for real people with diverse needs, abilities, and contexts. Every UI decision should prioritize the human experience over technical convenience.

Accessibility is not optional - it's how we ensure our software serves all users, not just some. When you make UI accessible, you're making it better for everyone: clearer labels help all users, keyboard navigation helps power users, and semantic HTML helps search engines.

**Example - Human-centered approach:**
```typescript
// ✅ Good - Built for people
function NoteForm() {
	return (
		<Form method="POST">
			<Field
				labelProps={{
					htmlFor: fields.title.id,
					children: 'Note Title', // Clear, human-readable label
				}}
				inputProps={{
					...getInputProps(fields.title),
					placeholder: 'Enter a descriptive title', // Helpful guidance
					autoFocus: true, // Saves time for users
				}}
				errors={fields.title.errors} // Clear error messages
			/>
		</Form>
	)
}

// ❌ Avoid - Technical convenience over user experience
function NoteForm() {
	return (
		<Form method="POST">
			<input name="title" /> {/* No label, no guidance, no accessibility */}
		</Form>
	)
}
```

### Semantic HTML

**✅ Good - Use semantic elements:**
```typescript
function UserCard({ user }: { user: User }) {
	return (
		<article>
			<header>
				<h2>{user.name}</h2>
			</header>
			<p>{user.bio}</p>
			<footer>
				<time dateTime={user.createdAt}>{formatDate(user.createdAt)}</time>
			</footer>
		</article>
	)
}
```

**❌ Avoid - Generic divs:**
```typescript
// ❌ Don't use divs for everything
<div>
	<div>{user.name}</div>
	<div>{user.bio}</div>
	<div>{formatDate(user.createdAt)}</div>
</div>
```

### Form Accessibility

**✅ Good - Always use labels:**
```typescript
// Example code for form accessibility
```