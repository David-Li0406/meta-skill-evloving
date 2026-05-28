---
name: jikime-migration-jquery-to-react
description: |
  jQuery to React 19 migration specialist. Converts legacy jQuery applications
  to modern React with hooks, TypeScript, and component-based architecture.
  Use when migrating jQuery projects, converting $() patterns to React,
  or asking about jQuery to React conversion.
argument-hint: [source-path]
version: 2.1.0
tags: ["migration", "jquery", "react", "javascript", "typescript", "legacy"]
triggers:
  keywords: ["jquery", "$", "$.ajax", "jquery-to-react", "migrate jquery", "convert jquery", "제이쿼리"]
  phases: ["plan", "run"]
  agents: ["manager-migrate-react", "frontend"]
  languages: ["javascript", "typescript"]
# Progressive Disclosure Configuration
progressive_disclosure:
  enabled: true
  level1_tokens: ~100
  level2_tokens: ~5000
user-invocable: false
context: fork
agent: Explore
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
  - TodoWrite
---

# jQuery → React Migration

## Quick Reference

| jQuery | React |
|--------|-------|
| `$('#id')` | `useRef()` |
| `$('.class')` | Component props/state |
| `.html()` | JSX rendering |
| `.text()` | `{variable}` |
| `.click()` | `onClick` |
| `.on('event')` | `onEvent` prop |
| `$.ajax()` | `fetch()` + `useEffect` |
| `$(document).ready()` | `useEffect(() => {}, [])` |
| `.show()/.hide()` | Conditional rendering |
| `.addClass()` | Conditional className |

## Dynamic Context (auto-loaded)

### Current Dependencies
!`cat package.json 2>/dev/null | grep -A 20 '"dependencies"' || echo "No package.json found"`

### jQuery Usage Detection
!`grep -r "\\\$(" --include="*.js" --include="*.html" . 2>/dev/null | head -10 || echo "No jQuery patterns found"`

### Source Structure
!`ls -la src/ 2>/dev/null | head -15 || ls -la . | head -15`

## Target Stack

| Technology | Version | Purpose |
|------------|---------|---------|
| Framework | React 19 | Component-based UI |
| Language | TypeScript 5.x | Type safety |
| Build Tool | Vite | Fast development |
| Styling | Tailwind CSS 4.x | Utility-first CSS |
| State | Zustand / useState | State management |
| Forms | react-hook-form | Form handling |
| Animation | Framer Motion | Animations |

## Migration Process

### 1. Analyze
Identify jQuery patterns in $ARGUMENTS:
- DOM selectors (`$()`, `document.getElementById`)
- Event handlers (`.on()`, `.click()`, `.submit()`)
- AJAX calls (`$.ajax`, `$.get`, `$.post`)
- Plugins and their alternatives

### 2. Plan
Map jQuery patterns to React equivalents:
- Selectors → useRef or state
- Events → React event handlers
- AJAX → useEffect + fetch
- Plugins → React component libraries

### 3. Execute
Transform code incrementally:
- Set up React alongside jQuery (coexistence)
- Migrate leaf components first
- Work up to container components
- Replace plugins last

### 4. Verify
Test behavior preservation:
- Same user interactions work
- Same data flows correctly
- No visual regressions

## Plugin Replacement Guide

| jQuery Plugin | React Alternative |
|---------------|-------------------|
| jQuery UI | Radix UI, shadcn/ui |
| jQuery Validation | react-hook-form + zod |
| Select2 | react-select |
| DataTables | TanStack Table |
| Slick Carousel | Swiper, Embla |
| Lightbox | yet-another-react-lightbox |
| DatePicker | react-datepicker |

## Module Reference

For detailed patterns, see:
- [jQuery Patterns](modules/jquery-patterns.md) - DOM manipulation, events, AJAX, lifecycle, animations

## Examples

### Before (jQuery)
```javascript
$(document).ready(function() {
  $('#button').click(function() {
    $.get('/api/data', function(data) {
      $('#content').html(data);
    });
  });
});
```

### After (React)
```tsx
import { useState, useEffect } from 'react';

function Component() {
  const [content, setContent] = useState('');

  const handleClick = async () => {
    const response = await fetch('/api/data');
    const data = await response.text();
    setContent(data);
  };

  return (
    <>
      <button onClick={handleClick}>Load</button>
      <div dangerouslySetInnerHTML={{ __html: content }} />
    </>
  );
}
```

## Troubleshooting

### Skill not triggering
- Try phrases like "migrate jQuery to React" or "convert $() patterns"
- Use `/migrate-jquery-to-react` directly

### Common Migration Issues
| Issue | Solution |
|-------|----------|
| `$` undefined | Remove jQuery import, use refs/state instead |
| Event not firing | Check React synthetic event naming (`onClick`, not `onclick`) |
| DOM not updated | Use state to trigger re-renders, not direct DOM manipulation |
| Plugin not working | Find React alternative in Plugin Replacement Guide above |

### Build Errors
- Run `npm uninstall jquery @types/jquery` after migration
- Check for remaining `$` patterns: `grep -r "\\$(" --include="*.tsx" src/`

## Quality Checklist

- [ ] All jQuery selectors replaced with refs/state
- [ ] Event handlers converted to React patterns
- [ ] AJAX calls use fetch with proper cleanup
- [ ] No direct DOM manipulation in React components
- [ ] jQuery plugins replaced with React alternatives
- [ ] TypeScript types added
- [ ] No jQuery in final bundle
- [ ] Tests passing

---

Version: 2.1.0
Last Updated: 2026-01-25
Source: React Official Docs, jQuery Migration Guide
