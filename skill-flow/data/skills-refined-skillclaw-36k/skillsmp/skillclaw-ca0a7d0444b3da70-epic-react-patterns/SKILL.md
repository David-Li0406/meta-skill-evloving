---
name: epic-react-patterns
description: Use this skill when you need to write efficient React components, optimize performance, and follow best practices in Epic Stack applications.
---

# Epic Stack: React Patterns and Guidelines

## When to use this skill

Use this skill when you need to:
- Write efficient React components in Epic Stack applications
- Optimize performance and bundle size
- Follow React Router patterns and conventions
- Avoid common React anti-patterns
- Implement proper code splitting
- Optimize re-renders and data fetching
- Use React hooks correctly

## Philosophy

Following Epic Web principles:
- **Make it work, make it right, make it fast** - In that order. First make it functional, then refactor for clarity, then optimize for performance.
- **Pragmatism over purity** - Choose practical solutions that work well in your context rather than theoretically perfect ones.
- **Optimize for sustainable velocity** - Write code that's easy to maintain and extend, not just fast to write initially.
- **Do as little as possible** - Only add complexity when it provides real value.

## Patterns and conventions

### Data Fetching in React Router

Epic Stack uses React Router loaders for data fetching, not `useEffect`.

**✅ Good - Use loaders:**
```typescript
// app/routes/users/$username.tsx
export async function loader({ params }: Route.LoaderArgs) {
	const user = await prisma.user.findUnique({
		where: { username: params.username },
	})
	return { user }
}

export default function UserRoute({ loaderData }: Route.ComponentProps) {
	return <div>{loaderData.user.name}</div>
}
```

**❌ Avoid - Don't fetch in useEffect:**
```typescript
// ❌ Don't do this
export default function UserRoute({ params }: Route.ComponentProps) {
	const [user, setUser] = useState(null)

	useEffect(() => {
		fetch(`/api/users/${params.username}`)
			.then(res => res.json())
			.then(setUser)
	}, [params.username])

	return user ? <div>{user.name}</div> : <div>Loading...</div>
}
```

### Avoid useEffect for Side Effects

Instead of using `useEffect`, use event handlers, CSS, ref callbacks, or `useSyncExternalStore`.

**✅ Good - Use event handlers:**
```typescript
function ProductPage({ product, addToCart }: Route.ComponentProps) {
	function buyProduct() {
		addToCart(product)
		showNotification(`Added ${product.name} to cart!`)
	}

	function handleBuyClick() {
		buyProduct()
	}
}
```