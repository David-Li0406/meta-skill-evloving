# Practical Examples

## Buttons

### Primary Button

```tsx
<button className="
  bg-blue-600
  hover:bg-blue-700
  active:bg-blue-800
  text-white
  font-medium
  px-4
  py-2
  rounded-lg
  transition-colors
  focus:outline-none
  focus:ring-2
  focus:ring-blue-500
  focus:ring-offset-2
  disabled:opacity-50
  disabled:cursor-not-allowed
">
  Primary Button
</button>
```

### Secondary Button

```tsx
<button className="
  bg-gray-100
  hover:bg-gray-200
  active:bg-gray-300
  text-gray-900
  font-medium
  px-4
  py-2
  rounded-lg
  transition-colors
  focus:outline-none
  focus:ring-2
  focus:ring-gray-500
  focus:ring-offset-2
">
  Secondary Button
</button>
```

### Outline Button

```tsx
<button className="
  border-2
  border-blue-600
  text-blue-600
  hover:bg-blue-50
  active:bg-blue-100
  font-medium
  px-4
  py-2
  rounded-lg
  transition-colors
  focus:outline-none
  focus:ring-2
  focus:ring-blue-500
  focus:ring-offset-2
">
  Outline Button
</button>
```

### Icon Button

```tsx
<button className="
  p-2
  rounded-full
  text-gray-500
  hover:text-gray-700
  hover:bg-gray-100
  transition-colors
  focus:outline-none
  focus:ring-2
  focus:ring-gray-500
">
  <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
    {/* icon path */}
  </svg>
</button>
```

## Cards

### Basic Card

```tsx
<div className="
  bg-white
  dark:bg-gray-800
  rounded-xl
  shadow-sm
  border
  border-gray-200
  dark:border-gray-700
  p-6
">
  <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
    Card Title
  </h3>
  <p className="mt-2 text-gray-600 dark:text-gray-400">
    Card description goes here.
  </p>
</div>
```

### Hoverable Card

```tsx
<div className="
  bg-white
  dark:bg-gray-800
  rounded-xl
  shadow-sm
  hover:shadow-md
  border
  border-gray-200
  dark:border-gray-700
  p-6
  transition-shadow
  cursor-pointer
">
  <h3 className="text-lg font-semibold">Hoverable Card</h3>
  <p className="mt-2 text-gray-600">Hover to see shadow change.</p>
</div>
```

### Feature Card

```tsx
<div className="
  bg-gradient-to-br
  from-blue-500
  to-purple-600
  rounded-xl
  p-6
  text-white
">
  <div className="
    w-12
    h-12
    bg-white/20
    rounded-lg
    flex
    items-center
    justify-center
    mb-4
  ">
    <FeatureIcon className="w-6 h-6" />
  </div>
  <h3 className="text-xl font-semibold">Feature Title</h3>
  <p className="mt-2 text-blue-100">
    Feature description with some details.
  </p>
</div>
```

### Pricing Card

```tsx
<div className="
  bg-white
  rounded-2xl
  shadow-lg
  border-2
  border-blue-500
  p-8
  relative
">
  <div className="
    absolute
    -top-4
    left-1/2
    -translate-x-1/2
    bg-blue-500
    text-white
    text-sm
    font-medium
    px-4
    py-1
    rounded-full
  ">
    Most Popular
  </div>

  <h3 className="text-2xl font-bold text-center">Pro Plan</h3>

  <div className="mt-4 text-center">
    <span className="text-4xl font-bold">$29</span>
    <span className="text-gray-500">/month</span>
  </div>

  <ul className="mt-6 space-y-3">
    {features.map(feature => (
      <li key={feature} className="flex items-center gap-2">
        <CheckIcon className="w-5 h-5 text-green-500" />
        <span>{feature}</span>
      </li>
    ))}
  </ul>

  <Button className="w-full mt-8">Get Started</Button>
</div>
```

## Forms

### Input Field

```tsx
<div className="space-y-2">
  <label
    htmlFor="email"
    className="block text-sm font-medium text-gray-700 dark:text-gray-300"
  >
    Email
  </label>
  <input
    type="email"
    id="email"
    className="
      w-full
      px-4
      py-2
      border
      border-gray-300
      dark:border-gray-600
      rounded-lg
      bg-white
      dark:bg-gray-800
      text-gray-900
      dark:text-white
      placeholder-gray-400
      focus:outline-none
      focus:ring-2
      focus:ring-blue-500
      focus:border-transparent
      transition-colors
    "
    placeholder="you@example.com"
  />
</div>
```

### Input with Error

```tsx
<div className="space-y-2">
  <label className="block text-sm font-medium text-gray-700">
    Email
  </label>
  <input
    type="email"
    className="
      w-full
      px-4
      py-2
      border-2
      border-red-500
      rounded-lg
      bg-red-50
      text-gray-900
      placeholder-gray-400
      focus:outline-none
      focus:ring-2
      focus:ring-red-500
      focus:border-transparent
    "
    placeholder="you@example.com"
  />
  <p className="text-sm text-red-600">
    Please enter a valid email address.
  </p>
</div>
```

### Checkbox

```tsx
<label className="flex items-center gap-3 cursor-pointer">
  <input
    type="checkbox"
    className="
      w-5
      h-5
      rounded
      border-gray-300
      text-blue-600
      focus:ring-blue-500
      focus:ring-2
      focus:ring-offset-2
    "
  />
  <span className="text-gray-700">Remember me</span>
</label>
```

### Toggle Switch

```tsx
<button
  role="switch"
  aria-checked={enabled}
  onClick={() => setEnabled(!enabled)}
  className={`
    relative
    inline-flex
    h-6
    w-11
    items-center
    rounded-full
    transition-colors
    focus:outline-none
    focus:ring-2
    focus:ring-blue-500
    focus:ring-offset-2
    ${enabled ? 'bg-blue-600' : 'bg-gray-200'}
  `}
>
  <span
    className={`
      inline-block
      h-4
      w-4
      transform
      rounded-full
      bg-white
      transition-transform
      ${enabled ? 'translate-x-6' : 'translate-x-1'}
    `}
  />
</button>
```

## Navigation

### Navbar

```tsx
<nav className="
  bg-white
  dark:bg-gray-900
  border-b
  border-gray-200
  dark:border-gray-800
">
  <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
    <div className="flex h-16 items-center justify-between">
      <div className="flex items-center gap-8">
        <Logo />
        <div className="hidden md:flex items-center gap-6">
          <NavLink href="/features">Features</NavLink>
          <NavLink href="/pricing">Pricing</NavLink>
          <NavLink href="/docs">Docs</NavLink>
        </div>
      </div>

      <div className="flex items-center gap-4">
        <Button variant="ghost" className="hidden md:inline-flex">
          Log in
        </Button>
        <Button>Sign up</Button>
      </div>
    </div>
  </div>
</nav>
```

### Sidebar Navigation

```tsx
<nav className="space-y-1">
  {navItems.map(item => (
    <a
      key={item.href}
      href={item.href}
      className={`
        flex
        items-center
        gap-3
        px-3
        py-2
        rounded-lg
        text-sm
        font-medium
        transition-colors
        ${
          item.active
            ? 'bg-blue-50 text-blue-700 dark:bg-blue-900/50 dark:text-blue-300'
            : 'text-gray-700 hover:bg-gray-100 dark:text-gray-300 dark:hover:bg-gray-800'
        }
      `}
    >
      <item.icon className="w-5 h-5" />
      {item.label}
    </a>
  ))}
</nav>
```

### Breadcrumbs

```tsx
<nav className="flex items-center gap-2 text-sm">
  <a href="/" className="text-gray-500 hover:text-gray-700">
    Home
  </a>
  <ChevronRightIcon className="w-4 h-4 text-gray-400" />
  <a href="/products" className="text-gray-500 hover:text-gray-700">
    Products
  </a>
  <ChevronRightIcon className="w-4 h-4 text-gray-400" />
  <span className="text-gray-900 font-medium">
    Product Name
  </span>
</nav>
```

## Badges & Tags

### Status Badge

```tsx
<span className="
  inline-flex
  items-center
  gap-1
  px-2.5
  py-0.5
  rounded-full
  text-xs
  font-medium
  bg-green-100
  text-green-800
  dark:bg-green-900
  dark:text-green-300
">
  <span className="w-1.5 h-1.5 rounded-full bg-green-500" />
  Active
</span>
```

### Category Tag

```tsx
<span className="
  inline-flex
  items-center
  px-3
  py-1
  rounded-full
  text-sm
  font-medium
  bg-blue-100
  text-blue-800
  hover:bg-blue-200
  transition-colors
  cursor-pointer
">
  Technology
</span>
```

### Removable Tag

```tsx
<span className="
  inline-flex
  items-center
  gap-1
  pl-3
  pr-1.5
  py-1
  rounded-full
  text-sm
  bg-gray-100
  text-gray-800
">
  React
  <button className="
    p-0.5
    rounded-full
    hover:bg-gray-200
    transition-colors
  ">
    <XIcon className="w-3.5 h-3.5" />
  </button>
</span>
```

## Alerts

### Info Alert

```tsx
<div className="
  flex
  items-start
  gap-3
  p-4
  rounded-lg
  bg-blue-50
  border
  border-blue-200
  text-blue-800
">
  <InfoIcon className="w-5 h-5 flex-shrink-0 mt-0.5" />
  <div>
    <p className="font-medium">Information</p>
    <p className="mt-1 text-sm text-blue-700">
      This is an informational message.
    </p>
  </div>
</div>
```

### Error Alert

```tsx
<div className="
  flex
  items-start
  gap-3
  p-4
  rounded-lg
  bg-red-50
  border
  border-red-200
  text-red-800
">
  <AlertCircleIcon className="w-5 h-5 flex-shrink-0 mt-0.5" />
  <div>
    <p className="font-medium">Error</p>
    <p className="mt-1 text-sm text-red-700">
      Something went wrong. Please try again.
    </p>
  </div>
</div>
```

### Success Alert

```tsx
<div className="
  flex
  items-start
  gap-3
  p-4
  rounded-lg
  bg-green-50
  border
  border-green-200
  text-green-800
">
  <CheckCircleIcon className="w-5 h-5 flex-shrink-0 mt-0.5" />
  <div>
    <p className="font-medium">Success</p>
    <p className="mt-1 text-sm text-green-700">
      Your changes have been saved.
    </p>
  </div>
</div>
```

## Loading States

### Spinner

```tsx
<div className="
  w-8
  h-8
  border-4
  border-blue-200
  border-t-blue-600
  rounded-full
  animate-spin
" />
```

### Skeleton

```tsx
<div className="animate-pulse space-y-4">
  <div className="h-4 bg-gray-200 rounded w-3/4" />
  <div className="h-4 bg-gray-200 rounded w-1/2" />
  <div className="h-4 bg-gray-200 rounded w-5/6" />
</div>
```

### Skeleton Card

```tsx
<div className="
  bg-white
  rounded-lg
  shadow-sm
  p-6
  animate-pulse
">
  <div className="h-40 bg-gray-200 rounded-lg mb-4" />
  <div className="h-4 bg-gray-200 rounded w-3/4 mb-2" />
  <div className="h-4 bg-gray-200 rounded w-1/2" />
</div>
```

## Empty States

```tsx
<div className="
  flex
  flex-col
  items-center
  justify-center
  py-12
  px-4
  text-center
">
  <div className="
    w-16
    h-16
    bg-gray-100
    rounded-full
    flex
    items-center
    justify-center
    mb-4
  ">
    <InboxIcon className="w-8 h-8 text-gray-400" />
  </div>
  <h3 className="text-lg font-medium text-gray-900">
    No items yet
  </h3>
  <p className="mt-1 text-gray-500 max-w-sm">
    Get started by creating your first item.
  </p>
  <Button className="mt-6">
    Create Item
  </Button>
</div>
```

## Avatar

### Basic Avatar

```tsx
<img
  src={user.avatar}
  alt={user.name}
  className="
    w-10
    h-10
    rounded-full
    object-cover
    border-2
    border-white
    shadow-sm
  "
/>
```

### Avatar with Status

```tsx
<div className="relative">
  <img
    src={user.avatar}
    alt={user.name}
    className="w-10 h-10 rounded-full object-cover"
  />
  <span className="
    absolute
    bottom-0
    right-0
    w-3
    h-3
    bg-green-500
    border-2
    border-white
    rounded-full
  " />
</div>
```

### Avatar Group

```tsx
<div className="flex -space-x-2">
  {users.slice(0, 4).map(user => (
    <img
      key={user.id}
      src={user.avatar}
      alt={user.name}
      className="
        w-8
        h-8
        rounded-full
        border-2
        border-white
        object-cover
      "
    />
  ))}
  {users.length > 4 && (
    <span className="
      flex
      items-center
      justify-center
      w-8
      h-8
      rounded-full
      bg-gray-100
      border-2
      border-white
      text-xs
      font-medium
      text-gray-600
    ">
      +{users.length - 4}
    </span>
  )}
</div>
```
