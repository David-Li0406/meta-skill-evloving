# Design Tokens

## Color Palette

### Backgrounds
```css
bg-zinc-950    /* Primary background - darkest */
bg-zinc-900    /* Secondary background */
bg-zinc-800    /* Tertiary background / hover states */
```

### Borders
```css
border-zinc-800    /* Default border */
border-zinc-700    /* Lighter border */
border-zinc-600    /* Hover border */
```

### Text
```css
text-white         /* Primary text */
text-zinc-300      /* Secondary text / labels */
text-zinc-400      /* Tertiary text / descriptions */
text-zinc-500      /* Placeholder text */
```

### Accent (Emerald)
```css
bg-emerald-500     /* Primary accent */
bg-emerald-400     /* Hover accent */
bg-emerald-500/10  /* Subtle accent background */
text-emerald-500   /* Accent text */
border-emerald-500 /* Focus/active borders */
```

### States
```css
/* Error */
border-red-500
text-red-400
bg-red-500/10

/* Success */
text-emerald-400
bg-emerald-500/10

/* Disabled */
opacity-50
cursor-not-allowed
```

## Border Radius

```css
rounded-lg    /* 8px - small elements */
rounded-xl    /* 12px - inputs, buttons */
rounded-2xl   /* 16px - cards, large buttons */
rounded-full  /* Pills, avatars */
```

## Spacing

```css
/* Gaps */
gap-2    /* 8px - tight spacing */
gap-3    /* 12px - default spacing */
gap-4    /* 16px - comfortable spacing */
gap-6    /* 24px - section spacing */
gap-8    /* 32px - large spacing */

/* Padding */
px-4 py-3    /* Input padding */
px-6 py-3    /* Button padding */
px-8 py-4    /* Large button padding */
p-4          /* Card padding */
p-6          /* Large card padding */
```

## Typography

```css
/* Sizes */
text-xs      /* 12px - labels, captions */
text-sm      /* 14px - body text, descriptions */
text-base    /* 16px - default */
text-lg      /* 18px - headings */
text-xl      /* 20px - large headings */
text-2xl     /* 24px - page titles */

/* Weights */
font-medium  /* 500 - labels */
font-semibold /* 600 - subheadings */
font-bold    /* 700 - headings, buttons */

/* Line Height */
leading-none    /* Tight */
leading-tight   /* Headings */
leading-normal  /* Body text */
```

## Shadows

```css
shadow-lg                    /* Standard elevation */
shadow-emerald-500/10        /* Accent glow */
shadow-xl                    /* High elevation */
```

## Transitions

```css
transition-colors    /* Color changes */
transition-all       /* All properties */
duration-150         /* Fast */
duration-300         /* Standard */
```

## Component Patterns

### Input Field
```typescript
className="w-full bg-zinc-950 border border-zinc-800 rounded-xl px-4 py-3 text-white outline-none focus:border-emerald-500 transition-colors"
```

### Button (Primary)
```typescript
className="bg-emerald-500 hover:bg-emerald-400 text-black font-bold px-6 py-3 rounded-xl transition-colors"
```

### Button (Secondary)
```typescript
className="bg-zinc-900 hover:bg-zinc-800 border border-zinc-800 text-white font-medium px-6 py-3 rounded-xl transition-colors"
```

### Card
```typescript
className="bg-zinc-900 border border-zinc-800 rounded-2xl p-6"
```

### Label
```typescript
className="text-sm font-medium text-zinc-300"
```

### Description
```typescript
className="text-xs text-zinc-500"
```

### Error Message
```typescript
className="flex items-center gap-2 text-red-400 text-sm"
```

### Icon Container
```typescript
className="w-10 h-10 rounded-xl bg-emerald-500/10 flex items-center justify-center text-emerald-500"
```

## Usage Examples

### Form Input with Label
```tsx
<div className="space-y-2">
    <label className="text-sm font-medium text-zinc-300">
        Field Name
    </label>
    <input
        type="text"
        className="w-full bg-zinc-950 border border-zinc-800 rounded-xl px-4 py-3 text-white outline-none focus:border-emerald-500 transition-colors"
    />
</div>
```

### Primary Action Button
```tsx
<button className="bg-emerald-500 hover:bg-emerald-400 text-black font-bold px-8 py-4 rounded-2xl shadow-lg shadow-emerald-500/10 transition-colors">
    Continue
</button>
```

### Card with Icon Header
```tsx
<div className="bg-zinc-900 border border-zinc-800 rounded-2xl p-6">
    <div className="flex items-center gap-3 mb-4">
        <div className="w-10 h-10 rounded-xl bg-emerald-500/10 flex items-center justify-center text-emerald-500">
            <Icon size={20} />
        </div>
        <div>
            <h3 className="text-lg font-bold">Title</h3>
            <p className="text-sm text-zinc-400">Description</p>
        </div>
    </div>
    {/* Content */}
</div>
```

### Select Dropdown
```tsx
<select className="w-full bg-zinc-950 border border-zinc-800 rounded-xl px-4 py-3 text-white outline-none focus:border-emerald-500 transition-colors">
    <option value="">Select option</option>
    <option value="1">Option 1</option>
</select>
```
