# Hyperscript Command Reference

## DOM Manipulation

### toggle
Toggle a class, attribute, or visibility on elements.

```html
<button _="on click toggle .active">Toggle class</button>
<button _="on click toggle @disabled on #input">Toggle attribute</button>
<button _="on click toggle #menu">Toggle visibility</button>
```

### add
Add a class, attribute, or style to elements.

```html
<button _="on click add .highlight to me">Add class</button>
<button _="on click add @required to #email">Add attribute</button>
<button _="on click add *background-color:red to me">Add style</button>
```

### remove
Remove a class, attribute, style, or element.

```html
<button _="on click remove .error from #form">Remove class</button>
<button _="on click remove @disabled from #submit">Remove attribute</button>
<button _="on click remove me">Remove element</button>
```

### show
Show hidden elements with optional transition.

```html
<button _="on click show #modal">Show instantly</button>
<button _="on click show #modal with *opacity">Fade in</button>
<button _="on click show #panel with *height over 300ms">Slide open</button>
```

### hide
Hide elements with optional transition.

```html
<button _="on click hide #modal">Hide instantly</button>
<button _="on click hide me with *opacity">Fade out</button>
<button _="on click hide #dropdown with *height over 200ms">Slide closed</button>
```

### put
Set content or value of elements.

```html
<button _="on click put 'Hello' into #greeting">Set text</button>
<button _="on click put it into #result">Set from result</button>
<button _="on click put '<b>Bold</b>' into #output">Set HTML</button>
```

### append
Add content to end of element.

```html
<button _="on click append '<li>New</li>' to #list">Append HTML</button>
<button _="on click append it to #container">Append result</button>
```

### swap
Replace element content using different strategies.

```html
<button _="on click fetch /new-content swap #target innerHTML">Replace inner</button>
<button _="on click fetch /replacement swap #target outerHTML">Replace entire</button>
```

## Data Commands

### set
Set a variable or element property.

```html
<button _="on click set :count to 0">Set local variable</button>
<button _="on click set $user to 'guest'">Set global variable</button>
<button _="on click set #input.value to ''">Set property</button>
<button _="on click set :total to :price * :quantity">Set expression</button>
```

### get
Get a value from an element or API.

```html
<button _="on click get #email.value">Get property</button>
<button _="on click get @data-id from me">Get attribute</button>
```

### increment / decrement
Modify numeric values.

```html
<button _="on click increment :count">Add 1</button>
<button _="on click decrement :count">Subtract 1</button>
<button _="on click increment :total by 10">Add 10</button>
<button _="on click increment #counter.textContent">Modify element</button>
```

## Events

### send / trigger
Dispatch custom events.

```html
<button _="on click send refresh to #list">Send to element</button>
<button _="on click trigger submit on #form">Trigger on target</button>
<button _="on click send myEvent(detail: 'data')">Send with detail</button>
```

## Async Commands

### wait
Pause execution.

```html
<button _="on click wait 1s then hide me">Wait seconds</button>
<button _="on click wait 500ms">Wait milliseconds</button>
<button _="on click wait for animationend">Wait for event</button>
```

### fetch
Make HTTP requests.

```html
<button _="on click fetch /api/data">GET request</button>
<button _="on click fetch /api/data as json">Parse as JSON</button>
<button _="on click fetch /api/data as json put it.name into #name">Use result</button>
<button _="on click fetch /api/save { method: 'POST', body: form as FormData }">POST form</button>
```

## Control Flow

### if / else
Conditional execution.

```html
<button _="on click if me matches .active remove .active else add .active">
<input _="on blur if my value is empty add .error to me else remove .error from me">
<button _="on click if :count > 10 log 'high' else if :count > 5 log 'medium' else log 'low'">
```

### repeat
Loop a fixed number of times.

```html
<button _="on click repeat 5 times append '<li/>' to #list">
<button _="on click repeat :count times increment :total">
```

### for each
Iterate over collections.

```html
<ul _="on load for item in items append <li>{item.name}</li> to me">
<div _="on click for el in .items add .highlight to el">
```

### while
Loop while condition is true.

```html
<button _="on click while :loading wait 100ms">Poll until ready</button>
```

## Navigation

### go
Navigate to URL.

```html
<button _="on click go to /dashboard">Navigate</button>
<button _="on click go to url in @href">Use attribute</button>
<a _="on click.prevent go to @href">SPA navigation</a>
```

## Utility Commands

### log
Debug output to console.

```html
<button _="on click log me">Log element</button>
<button _="on click log 'clicked:' me :count">Log multiple</button>
```

### focus / blur
Control element focus.

```html
<button _="on click focus #input">Focus input</button>
<input _="on escape blur me">Blur on escape</input>
```

### call
Call JavaScript functions.

```html
<button _="on click call myFunction()">Call global function</button>
<button _="on click call me.scrollIntoView()">Call method</button>
<button _="on click call validate(me.value)">Pass arguments</button>
```

### return
Exit current handler with optional value.

```html
<button _="on click if :disabled return">Exit early</button>
<button _="on click return 'done'">Return value</button>
```

## Animation

### transition
Animate CSS properties.

```html
<div _="on click transition *opacity to 0.5 over 300ms">
<div _="on mouseenter transition *transform to 'scale(1.1)' over 200ms">
```

### settle
Wait for CSS transitions to complete.

```html
<div _="on click add .expanded settle then scroll into view">
```
