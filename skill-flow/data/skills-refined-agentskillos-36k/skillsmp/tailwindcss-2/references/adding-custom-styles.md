# Adding custom styles

Often the biggest challenge when working with a framework is figuring out what you’re supposed to do when there’s something you need that the framework doesn’t handle for you.

Tailwind has been designed from the ground up to be extensible and customizable, so that no matter what you’re building you never feel like you’re fighting the framework.

This guide covers topics like customizing your design tokens, how to break out of those constraints when necessary, adding your own custom CSS, and extending the framework with plugins.

## [Customizing your theme](#customizing-your-theme)

If you want to change things like your color palette, spacing scale, typography scale, or breakpoints, add your customizations using the `@theme` directive in your CSS:

CSS

```css
@theme {
  --font-display: "Satoshi", "sans-serif";
  --breakpoint-3xl: 120rem;
  --color-avocado-100: oklch(0.99 0 0);
  --color-avocado-200: oklch(0.98 0.04 113.22);
  --color-avocado-300: oklch(0.94 0.11 115.03);
  --color-avocado-400: oklch(0.92 0.19 114.08);
  --color-avocado-500: oklch(0.84 0.18 117.33);
  --color-avocado-600: oklch(0.53 0.12 118.34);
  --ease-fluid: cubic-bezier(0.3, 0, 0, 1);
  --ease-snappy: cubic-bezier(0.2, 0, 0, 1); /* ... */
}
```

## [Using custom CSS](#using-custom-css)

While Tailwind is designed to handle the bulk of your styling needs, there is nothing stopping you from just writing plain CSS when you need to:

CSS

```css
@import "tailwindcss";
.my-custom-style {
  /* ... */
}
```

### [Adding base styles](#adding-base-styles)

If you just want to set some defaults for the page (like the text color, background color, or font family), the easiest option is just adding some classes to the `html` or `body` elements:

HTML

```html
<!doctype html>
<html lang="en" class="bg-gray-100 font-serif text-gray-900">
  <!-- ... -->
</html>
```

This keeps your base styling decisions in your markup alongside all of your other styles, instead of hiding them in a separate file.

If you want to add your own default base styles for specific HTML elements, use the `@layer` directive to add those styles to Tailwind ' s `base` layer:

CSS

```css
@layer base {
  h1 {
    font-size: var(--text-2xl);
  }
  h2 {
    font-size: var(--text-xl);
  }
}
```

### [Adding component classes](#adding-component-classes)

Use the `components` layer for any more complicated classes you want to add to your project that you ' d still like to be able to override with utility classes.

Traditionally these would be classes like `card`, `btn`, `badge` — that kind of thing.

CSS

```css
@layer components {
  .card {
    background-color: var(--color-white);
    border-radius: var(--radius-lg);
    padding: --spacing(6);
    box-shadow: var(--shadow-xl);
  }
}
```

By defining component classes in the `components` layer, you can still use utility classes to override them when necessary:

HTML

```html
<!-- Will look like a card, but with square corners -->
<div class="card rounded-none"><!-- ... --></div>
```

Using Tailwind you probably don ' t need these types of classes as often as you think. Read our guide on [managing duplication](/docs/styling-with-utility-classes#managing-duplication) for our recommendations.

The `components` layer is also a good place to put custom styles for any third-party components you ' re using:

CSS

```css
@layer components {
  .select2-dropdown {
    /* ... */
  }
}
```

### [Using variants](#using-variants)

Use the `@variant` directive to apply a Tailwind variant within custom CSS:

app.css

```css
.my-element {
  background: white;
  @variant dark {
    background: black;
  }
}
```

Compiled CSS

```css
.my-element {
  background: white;
  @media (prefers-color-scheme: dark) {
    background: black;
  }
}
```

If you need to apply multiple variants at the same time, use nesting:

app.css

```css
.my-element {
  background: white;
  @variant dark {
    @variant hover {
      background: black;
    }
  }
}
```

Compiled CSS

```css
.my-element {
  background: white;
  @media (prefers-color-scheme: dark) {
    &:hover {
      @media (hover: hover) {
        background: black;
      }
    }
  }
}
```

## [Adding custom utilities](#adding-custom-utilities)

### [Simple utilities](#simple-utilities)

In addition to using the utilities that ship with Tailwind, you can also add your own custom utilities. This can be useful when there ' s a CSS feature you ' d like to use in your project that Tailwind doesn ' t include utilities for out of the box.

Use the `@utility` directive to add a custom utility to your project:

CSS

```css
@utility content-auto {
  content-visibility: auto;
}
```

You can now use this utility in your HTML:

HTML

```css
<div class="content-auto">  <!-- ... --></div>
```

It will also work with variants like `hover`, `focus` and `lg`:

HTML

```css
<div class="hover:content-auto">  <!-- ... --></div>
```

Custom utilities are automatically inserted into the `utilities` layer along with all of the built-in utilities in the framework.

### [Complex utilities](#complex-utilities)

If your custom utility is more complex than a single class name, use nesting to define the utility:

CSS

```css
@utility scrollbar-hidden {
  &::-webkit-scrollbar {
    display: none;
  }
}
```

### [Functional utilities](#functional-utilities)

In addition to registering simple utilities with the `@utility` directive, you can also register functional utilities that accept an argument:

CSS

```css
@utility tab-* {
  tab-size: --value(--tab-size-*);
}
```

The special `--value()` function is used to resolve the utility value.

#### [Matching theme values](#matching-theme-values)

Use the `--value(--theme-key-*)` syntax to resolve the utility value against a set of theme keys:

CSS

```css
@theme {
  --tab-size-2: 2;
  --tab-size-4: 4;
  --tab-size-github: 8;
}
@utility tab-* {
  tab-size: --value(--tab-size-*);
}
```

This will match utilities like `tab-2`, `tab-4`, and `tab-github`.

#### [Bare values](#bare-values)

To resolve the value as a bare value, use the `--value({type})` syntax, where `{type}` is the data type you want to validate the bare value as:

CSS

```css
@utility tab-* {
  tab-size: --value(integer);
}
```

This will match utilities like `tab-1` and `tab-76`.

Available bare value data types are: `number`, `integer`, `ratio`, and `percentage`.

#### [Literal values](#literal-values)

To support literal values, use the `--value( ' literal ')` syntax (notice the quotes):

CSS

```css
@utility tab-* {
  tab-size: --value("inherit", "initial", "unset");
}
```

This will match utilities like `tab-inherit`, `tab-initial`, and `tab-unset`.

#### [Negative values](#negative-values)

To support negative values, register separate positive and negative utilities into separate declarations:

CSS

```css
@utility inset-* {
  inset: --spacing(--value(integer));
  inset: --value([percentage], [length]);
}
@utility -inset-* {
  inset: --spacing(--value(integer) * -1);
  inset: calc(--value([percentage], [length]) * -1);
}
```

#### [Modifiers](#modifiers)

Modifiers are handled using the `--modifier()` function which works exactly like the `--value()` function but operates on a modifier if present:

CSS

```css
@utility text-* {
  font-size: --value(--text-*, [length]);
  line-height: --modifier(--leading-*, [length], [*]);
}
```

If a modifier isn ' t present, any declaration depending on a modifier is just not included in the output.

#### [Fractions](#fractions)

To handle fractions, we rely on the CSS `ratio` data type. If this is used with `--value()`, it ' s a signal to Tailwind to treat the value and modifier as a single value:

CSS

```css
@utility aspect-* {
  aspect-ratio: --value(--aspect-ratio-*, ratio, [ratio]);
}
```

This will match utilities like `aspect-square`, `aspect-3/4`, and `aspect-[7/9]`.

## [Adding custom variants](#adding-custom-variants)

In addition to using the variants that ship with Tailwind, you can also add your own custom variants using the `@custom-variant` directive:

```css
@custom-variant theme-midnight {
  &:where([data-theme="midnight"] *) {
    @slot;
  }
}
```

Now you can use the `theme-midnight: < utility >` variant in your HTML:

```css
<html data-theme="midnight">  <button class="theme-midnight:bg-black ..."></button></html>
```

You can create variants using the shorthand syntax when nesting isn ' t required:

```css
@custom-variant theme-midnight (&:where([data-theme="midnight"] *));
```

When a custom variant has multiple rules, they can be nested within each other:

```css
@custom-variant any-hover {
  @media (any-hover: hover) {
    &:hover {
      @slot;
    }
  }
}
```
