# Fluid Sizing (f- prefix)

## How It Works

Uses CSS `clamp()` to scale values between viewport widths:

```css
/* f-p-md generates: */
padding: clamp(24px, calc(24px + (32 - 24) * (100vw - 320px) / (1920 - 320)), 32px);
```

- **Min viewport**: 320px (mobile)
- **Max viewport**: 1920px (desktop)
- Value scales linearly between min/max

## Spacing Scale

| Size | Min→Max | Usage |
|------|---------|-------|
| `2xs` | 8→12px | Tight gaps |
| `xs` | 12→16px | Small gaps |
| `sm` | 16→24px | Default spacing |
| `md` | 24→32px | Section gaps |
| `lg` | 32→48px | Large sections |
| `xl` | 48→72px | Hero spacing |
| `2xl` | 72→96px | Major sections |
| `3xl` | 96→128px | Full sections |

## Font Size Scale

| Size | Min→Max |
|------|---------|
| `3xs` | 9→11px |
| `2xs` | 10→12px |
| `xs` | 12→14px |
| `sm` | 14→16px |
| `md` | 16→16px (fixed) |
| `lg` | 16→18px |
| `xl` | 18→22px |
| `2xl` | 22→26px |
| `3xl` | 26→32px |
| `4xl` | 32→44px |

## Border Radius Scale

| Size | Min→Max |
|------|---------|
| `xs` | 2→4px |
| `sm` | 4→6px |
| `md` | 6→8px |
| `lg` | 8→12px |
| `xl` | 12→16px |
| `2xl` | 16→24px |

## Utility Patterns

### Padding
```vue
<div f-p-md>                    <!-- all sides -->
<div f-px-sm f-py-xs>           <!-- horizontal + vertical -->
<div f-pt-2xl f-pb-lg>          <!-- top + bottom -->
<div f-pl-md f-pr-sm>           <!-- left + right -->
```

### Margin
```vue
<div f-m-sm>
<div f-mt-lg f-mb-md>
<div f-mx-auto>                 <!-- not fluid, just auto -->
```

### Text
```vue
<span text="f-xl">              <!-- in attribute -->
<span f-text-sm>                <!-- as class -->
<h1 f-text-4xl>
```

### Gap
```vue
<div flex="~ gap-f-sm">         <!-- doesn't exist, use: -->
<div f-gap-md>                  <!-- fluid gap -->
```

### Border Radius
```vue
<div f-rounded-md>
<div f-rounded-xl>
```

### Custom Min/Max Values

```vue
<!-- f-{util}-min-{n} f-{util}-max-{n} -->
<div f-p-min-16 f-p-max-32>     <!-- 16px→32px -->
<div f-text-min-14 f-text-max-20>

<!-- Slash syntax -->
<div f-p-16/32>                 <!-- same as above -->
<div f-text-14/20>
```

## CSS Variable Support

```vue
<!-- Creates --f-px CSS variable -->
<div f-$px-16/24>
<div style="padding-left: var(--f-px); padding-right: var(--f-px);">
```

## With Responsive Breakpoints

```vue
<!-- Fluid + responsive -->
<div f-px-sm md:f-px-lg>        <!-- sm on mobile, lg from md breakpoint -->
<div f-pt-md lg:f-pt-2xl>
```

## All Supported Utilities

`text`, `w`, `h`, `size`, `p`, `px`, `py`, `pt`, `pb`, `pl`, `pr`, `m`, `mx`, `my`, `mt`, `mb`, `ml`, `mr`, `gap`, `gap-x`, `gap-y`, `rounded`, `rounded-t`, `rounded-b`, `rounded-l`, `rounded-r`, `leading`, `tracking`, `indent`, `top`, `right`, `bottom`, `left`, `inset`, `translate-x`, `translate-y`, `basis`, `min-w`, `max-w`, `min-h`, `max-h`, `border`, `outline`, `stroke`, `columns`, `scroll-m`, `scroll-p`
