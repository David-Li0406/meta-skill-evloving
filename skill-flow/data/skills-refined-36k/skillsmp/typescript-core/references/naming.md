# Naming Cheatsheet

Based on [kettanaito/naming-cheatsheet](https://github.com/kettanaito/naming-cheatsheet).

## Core Principles

### Use English

Use English consistently. Writing code in English dramatically increases its cohesiveness.

### Pick One Convention

Choose one naming convention (camelCase, PascalCase, snake_case) and remain consistent throughout your codebase.

### S-I-D Criteria

Names should be:

| Criterion       | Description                                           |
| --------------- | ----------------------------------------------------- |
| **Short**       | Easy to type and remember                             |
| **Intuitive**   | Reads naturally, matching common speech               |
| **Descriptive** | Efficiently reflects what something does or possesses |

### Avoid Contractions

Spell out full words for readability.

```ts
// Bad
onItmClk
setBgClr

// Good
onItemClick
setBackgroundColor
```

### Eliminate Context Duplication

Remove redundant context from names.

```ts
// Bad - in MenuItem class
class MenuItem {
  handleMenuItemClick() {}
}

// Good
class MenuItem {
  handleClick() {}
}
```

### Reflect Expected Results

Name variables for what they represent.

```ts
// Bad - double negative
const isNotDisabled = true

// Good
const isEnabled = true
```

---

## Function Naming Pattern: A/HC/LC

Structure: `prefix? + action (A) + high context (HC) + low context? (LC)`

| Name                   | Prefix   | Action    | High Context | Low Context |
| ---------------------- | -------- | --------- | ------------ | ----------- |
| `getUser`              |          | `get`     | `User`       |             |
| `getUserMessages`      |          | `get`     | `User`       | `Messages`  |
| `shouldDisplayMessage` | `should` | `Display` | `Message`    |             |
| `handleClickOutside`   |          | `handle`  | `Click`      | `Outside`   |

---

## Action Verbs

### get

Access data immediately (sync) or with a delay (async).

```ts
function getUser(id: string): User {
  return users.find(user => user.id === id)
}
```

### set

Assign a value declaratively.

```ts
function setName(name: string): void {
  user.name = name
}
```

### reset

Return something to its initial state.

```ts
function resetForm(): void {
  form.values = initialValues
}
```

### remove

Extract something from a collection (item still exists elsewhere).

```ts
function removeFilter(filter: Filter): void {
  filters = filters.filter(f => f !== filter)
}
```

### delete

Permanently erase something.

```ts
function deleteUser(id: string): void {
  database.users.delete(id)
}
```

### compose

Create new data from existing sources.

```ts
function composePageUrl(pageName: string, pageId: string): string {
  return `${pageName.toLowerCase()}-${pageId}`
}
```

### handle

Process callbacks or events.

```ts
function handleLinkClick(event: MouseEvent): void {
  event.preventDefault()
  navigate(event.target.href)
}
```

### fetch

Request data from a remote source.

```ts
function fetchUsers(): Promise<User[]> {
  return api.get('/users')
}
```

### create

Create a new instance.

```ts
function createUser(data: UserInput): User {
  return { id: generateId(), ...data }
}
```

### update

Modify existing data.

```ts
function updateUser(id: string, data: Partial<User>): User {
  return { ...users[id], ...data }
}
```

---

## Boolean Prefixes

### is

Describes a characteristic or state.

```ts
const isDisabled = true
const isLoading = false
const isVisible = true
```

### has

Indicates possession of a value or feature.

```ts
const hasProducts = products.length > 0
const hasError = error !== null
const hasPermission = user.permissions.includes('admin')
```

### should

Reflects a conditional action (often used for rendering).

```ts
const shouldUpdateUrl = pathname !== currentPath
const shouldShowBanner = !user.hasDismissedBanner
const shouldRenderChildren = isOpen && hasContent
```

### can

Indicates ability or permission.

```ts
const canEdit = user.role === 'editor' || user.role === 'admin'
const canSubmit = isValid && !isSubmitting
```

### will

Indicates something that will happen.

```ts
const willRedirect = response.status === 302
```

---

## Boundaries

### min/max

Denote inclusive boundaries or limits.

```ts
const minPrice = 0
const maxPrice = 1000

function validateAge(age: number): boolean {
  return age >= minAge && age <= maxAge
}
```

### prev/next

Signal state transitions in navigation or iteration.

```ts
function goToNextPage(): void {
  currentPage = nextPage
}

function getPrevItem<T>(items: T[], index: number): T {
  return items[index - 1]
}
```

---

## Singular vs. Plural

Match naming to data structure.

```ts
// Singular for single values
const friend = 'Bob'
const user = { name: 'Alice' }

// Plural for collections
const friends = ['Bob', 'Tony']
const users = [{ name: 'Alice' }, { name: 'Bob' }]
```

---

## React-Specific Naming

### Components

Use PascalCase.

```ts
function UserProfile() {}
function DataTableHeader() {}
```

### Props Interfaces

Suffix with `Props`.

```ts
interface UserProfileProps {
  userId: string
  onUpdate: (user: User) => void
}
```

### Event Handlers

Prefix with `on` for props, `handle` for implementations.

```ts
// Props (what the parent passes)
interface ButtonProps {
  onClick: () => void;
  onHover: () => void;
}

// Implementation (what the component does)
function Button({ onClick }: ButtonProps) {
  const handleClick = () => {
    trackEvent('click');
    onClick();
  };
  return <button onClick={handleClick} />;
}
```

### Hooks

Prefix with `use`.

```ts
function useUser(id: string) {}
function useLocalStorage<T>(key: string) {}
function useDebounce<T>(value: T, delay: number) {}
```

### State Variables

Name for what they represent, with setter using `set` prefix.

```ts
const [isOpen, setIsOpen] = useState(false)
const [users, setUsers] = useState<User[]>([])
const [selectedId, setSelectedId] = useState<string | null>(null)
```
