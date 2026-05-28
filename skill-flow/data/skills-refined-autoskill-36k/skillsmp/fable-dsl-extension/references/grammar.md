# DSL Grammar Reference

## Core Grammar Structure

The FableDSL grammar is defined using Ohm-JS and follows this structure:

```
FableDSL {
  Fable = Page+

  Page = "page" number "{" Statement* "}"

  Statement = VisualStatement | ControlStatement | AnimationStatement

  VisualStatement = VisualAgent "at" Position Properties?

  ControlStatement = IfStatement | ForStatement | WaitStatement

  AnimationStatement = AnimationCommand "on" Selector Properties?
}
```

## Existing Commands

### Visual Agents
- `text` - Display text content
- `button` - Interactive buttons
- `image` - Image display
- `video` - Video playback

### Control Flow
- `if/then/else` - Conditional execution
- `for/each/in/do/end` - Loop iteration
- `wait` - Time delays

### Animations
- `fade_in` - Fade in effect
- `slide_left/right/up/down` - Slide animations
- `scale` - Scale transformations

## Adding New Commands

### Grammar Pattern
```
NewCommand = "command_name" Parameters? Properties?
```

### Semantic Actions
```typescript
NewCommand: function(arg1, arg2) {
  return {
    type: 'new_command',
    param1: arg1.parse(),
    param2: arg2.parse()
  };
}
```

## Syntax Rules

### Naming Conventions
- Commands: lowercase with underscores
- Properties: camelCase
- Types: PascalCase

### Parameter Types
- `number` - Numeric values
- `string` - Quoted strings
- `boolean` - true/false
- `position` - [x, y] coordinates
- `size` - [width, height] dimensions

### Optional Parameters
Use `?` suffix for optional elements:
```
Command = "name" RequiredParam OptionalParam?
```