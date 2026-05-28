# Components Reference

## Contents
- Card Patterns
- Button Patterns
- Form Elements
- Navigation Elements
- Feedback States

## Card Patterns

### Service Card (Homepage)

The signature card pattern with gradient top bar and purple bottom border:

```tsx
<div className="service-card rounded-lg cursor-pointer group animate-fadeIn flex flex-col h-full border-4 border-gray-800 border-b-purple-500 bg-gray-900 overflow-hidden">
  {/* Gradient shimmer bar */}
  <div className="h-3 bg-gradient-to-r from-green-500 to-green-400 shimmer"></div>
  
  <div className="p-6 flex-1 flex flex-col">
    <div className="flex items-center justify-between mb-4">
      <div className="flex items-center gap-3">
        <span className="text-3xl animate-pulse-slow">{icon}</span>
        <h3 className="text-xl font-semibold group-hover:text-green-400 transition-colors">
          {title}
        </h3>
      </div>
      <span className="text-gray-400 text-2xl">{isExpanded ? '−' : '+'}</span>
    </div>
    <p className="text-gray-400 text-sm">{description}</p>
  </div>
</div>
```

### Feature Card (Solutions pages)

```tsx
<div className="bg-black/50 border border-gray-800 rounded-lg p-6 hover:border-yellow-500/50 transition-all animate-fadeIn">
  <div className="flex items-start gap-4">
    <CheckCircle className="w-6 h-6 text-yellow-400 flex-shrink-0 mt-1" />
    <div>
      <h3 className="text-xl font-semibold mb-3 text-yellow-400">{title}</h3>
      <p className="text-gray-300">{description}</p>
    </div>
  </div>
</div>
```

### Info Card (Contact page)

```tsx
<div className="bg-gray-900 rounded-lg p-8">
  <h2 className="text-2xl font-semibold mb-6">{title}</h2>
  {/* Content */}
</div>
```

## Button Patterns

### Primary CTA

```tsx
<Link
  href="/contact"
  className="cta-button bg-gradient-to-r from-purple-600 to-pink-600 px-8 py-4 rounded-full font-semibold hover:shadow-lg hover:shadow-purple-500/50 transform hover:scale-105 transition-all relative overflow-hidden"
>
  Primary Action
</Link>
```

### Secondary Button

```tsx
<Link
  href="/contact"
  className="cta-button bg-gray-800 px-8 py-4 rounded-full font-semibold hover:bg-gray-700 hover:shadow-lg transform hover:scale-105 transition-all"
>
  Secondary Action
</Link>
```

### Icon Button with Gradient

```tsx
<Link 
  href="/solutions/voice-agents" 
  className="group relative bg-gradient-to-r from-green-600 to-emerald-500 p-4 rounded-xl font-semibold text-center hover:shadow-lg hover:shadow-green-500/50 transform hover:scale-105 transition-all overflow-hidden"
>
  <div className="absolute inset-0 bg-gradient-to-r from-emerald-500 to-green-600 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
  <span className="relative z-10 flex items-center justify-center gap-2">
    <span className="text-2xl">📞</span>
    Voice AI Agents
  </span>
</Link>
```

### WARNING: Missing Transition Classes

**The Problem:**
```tsx
// BAD - No transition
<button className="bg-purple-600 hover:bg-purple-500">Click</button>
```

**Why This Breaks:** Abrupt color changes feel jarring. The site uses smooth transitions everywhere.

**The Fix:**
```tsx
// GOOD - Add transition-all or transition-colors
<button className="bg-purple-600 hover:bg-purple-500 transition-colors">Click</button>
```

## Form Elements

### Text Input

```tsx
<input
  type="text"
  className="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg focus:outline-none focus:border-[#8BC34A] transition-colors"
/>
```

### Textarea

```tsx
<textarea
  rows={6}
  className="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg focus:outline-none focus:border-[#8BC34A] transition-colors resize-none"
/>
```

### Submit Button with Loading State

```tsx
<button
  type="submit"
  disabled={isSubmitting}
  className="w-full bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-500 hover:to-pink-500 disabled:opacity-50 disabled:cursor-not-allowed px-6 py-3 rounded-full font-semibold transition-colors flex items-center justify-center gap-2"
>
  {isSubmitting ? (
    <>
      <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
      Sending...
    </>
  ) : (
    'Send Message'
  )}
</button>
```

## Navigation Elements

### Dropdown Menu

```tsx
<div className="absolute top-full left-0 mt-2 w-80 bg-gray-900 border border-gray-800 rounded-lg shadow-xl z-50">
  {items.map((item) => (
    <Link
      key={item.href}
      href={item.href}
      className="flex items-center gap-3 px-4 py-3 hover:bg-gray-800 hover:text-green-400 transition-colors first:rounded-t-lg last:rounded-b-lg"
    >
      <span className="text-lg">{item.icon}</span>
      <span>{item.name}</span>
    </Link>
  ))}
</div>
```

## Feedback States

### Error Message

```tsx
<div className="bg-red-900/20 border border-red-500/30 rounded-lg p-4 text-red-300">
  {error}
</div>
```

### Success Message

```tsx
<div className="bg-green-900/20 border border-green-500/30 rounded-lg p-4 text-green-300">
  Thank you! We'll be in touch soon.
</div>
```

### Highlight Box

```tsx
<div className="bg-gradient-to-r from-yellow-900/20 to-orange-900/20 border border-yellow-500/30 rounded-lg p-6">
  <p className="text-lg text-yellow-400 font-semibold">{message}</p>
</div>