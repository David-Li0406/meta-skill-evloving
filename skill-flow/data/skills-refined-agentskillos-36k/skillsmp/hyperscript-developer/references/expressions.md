# Hyperscript Expression Reference

## Element References

### me / myself
The current element with the `_` attribute.

```html
<button _="on click add .active to me">I'm me</button>
<div _="on click toggle .open on myself">Same as me</div>
```

### you
The target of the current event (event.target).

```html
<ul _="on click from li add .selected to you">Click target</ul>
```

### it / result
The result of the last expression or command.

```html
<button _="on click fetch /api then put it into #output">
<button _="on click call getValue() set :x to it">
```

## Variables

### Local Variables (`:name`)
Scoped to the current element/handler.

```html
<button _="on click set :count to 0 then increment :count">
<div _="on click set :items to [] then append 'a' to :items">
```

### Global Variables (`$name`)
Available across all elements.

```html
<button _="on click set $user to 'guest'">
<div _="on load if $user is empty go to /login">
```

### Element Properties
Access properties directly.

```html
<input _="on input put my value into #preview">
<div _="on click set me.innerHTML to ''">
<button _="on click log #input.value">
```

## Selectors

### ID Selector (`#id`)
```html
<button _="on click toggle .open on #menu">
<button _="on click put 'hello' into #greeting">
```

### Class Selector (`.class`)
Returns all matching elements.

```html
<button _="on click add .highlight to .item">
<button _="on click for el in .active remove .active from el">
```

### Tag Selector (`<tag/>`)
Query by tag name.

```html
<button _="on click hide <dialog/>">
<ul _="on click from <li/> toggle .selected on you">
```

### Attribute Selector
```html
<button _="on click toggle .active on [data-tab='settings']">
<div _="on click show [aria-hidden='true']">
```

## Positional Expressions

### first / last
```html
<button _="on click remove first .item">
<button _="on click add .active to last <li/>">
```

### next / previous
Relative to current element or selection.

```html
<button _="on click add .active to next .sibling">
<input _="on tab focus next <input/>">
<button _="on click show previous .panel">
```

### closest
Find nearest ancestor matching selector.

```html
<button _="on click add .active to closest .card">
<span _="on click toggle .expanded on closest <details/>">
```

### parent
Direct parent element.

```html
<button _="on click remove parent">Remove parent</button>
<span _="on click add .highlight to parent">
```

## Attribute Access

### @attribute
Read or check attributes.

```html
<button _="on click if @disabled return">
<a _="on click go to @href">
<div _="on click set :id to @data-id">
```

## Property Access

### Possessive Syntax (`element's property`)
```html
<button _="on click put #input's value into #preview">
<div _="on click if me's classList contains 'active' ...">
<span _="on click set me's textContent to 'clicked'">
```

### Dot Notation
```html
<button _="on click log me.className">
<input _="on change set :val to me.value">
```

## Comparisons

### Equality
```html
<input _="on blur if my value is empty add .error">
<button _="on click if :count is 0 return">
<div _="on click if :status is not 'active' return">
```

### Numeric Comparisons
```html
<button _="on click if :count > 10 log 'high'">
<input _="on input if my value.length < 3 add .error">
<div _="on load if :items.length >= 5 show #more-button">
```

### matches (CSS Selector)
Check if element matches a selector.

```html
<button _="on click if me matches .active remove .active">
<ul _="on click from li if you matches .disabled return">
```

### contains
Check membership.

```html
<button _="on click if :items contains 'apple' log 'has apple'">
<div _="on click if my classList contains 'open' hide me">
```

### exists / is empty
```html
<button _="on click if #modal exists show #modal">
<input _="on blur if my value is empty add .required">
```

## Logical Operators

### and / or / not
```html
<button _="on click if :a and :b log 'both'">
<input _="on blur if my value is empty or my value.length < 3 add .error">
<button _="on click if not me matches .disabled toggle .active">
```

## Arithmetic

```html
<button _="on click set :total to :price * :quantity">
<button _="on click set :avg to :sum / :count">
<button _="on click set :next to :current + 1">
<button _="on click set :remaining to :total - :used">
```

## Type Conversion

### as keyword
```html
<button _="on click fetch /api as json">
<form _="on submit fetch /api { body: me as FormData }">
<input _="on input set :num to my value as Int">
<div _="on click set :str to :count as String">
```

## String Operations

### Template Literals
```html
<button _="on click put `Hello, ${:name}!` into #greeting">
<div _="on click append `<li>${:item}</li>` to #list">
```

### String Methods
```html
<input _="on input set :upper to my value.toUpperCase()">
<button _="on click if :name.includes('test') log 'test mode'">
```

## Array Operations

```html
<button _="on click set :items to []">
<button _="on click append :newItem to :items">
<button _="on click set :first to :items[0]">
<button _="on click set :len to :items.length">
```
