# Wikilink + Checkbox Bug Analysis

This documents the bug where adding a wikilink to a todo line would break checkbox rendering.

## Symptoms

1. Todo with wikilink shows raw markdown `- [ ] text [[link]]` instead of checkbox
2. Clicking checkbox results in `[x] ` (missing the `- `)
3. Wikilinks disappear when toggling checkboxes

## Root Causes

### Cause 1: `textBetween` with `leafText: "\n"`

In `buildTodoDecorations()`:

```typescript
// BUGGY CODE
const text = node.textBetween(0, node.content.size, undefined, "\n");
```

For a paragraph with structure:
```
[text: "- [ ] test "] [wiki_link: {title: "Note"}] [text: " "]
```

This returns: `"- [ ] test \n "` (wiki_link becomes `\n`)

The regex `TODO_REGEX = /^(\s*)- \[([ xX])\] ?(.*)$/` then fails:
- `(.*)` matches `"test "` then stops at `\n`
- `$` expects end-of-string but finds `\n `
- No match = no decoration = raw markdown visible

**Fix:** Use empty string for leafText:
```typescript
const text = node.textBetween(0, node.content.size, undefined, "");
```

### Cause 2: Full-line replacement destroys inline nodes

In `toggleTodoWithinRange()`:

```typescript
// BUGGY CODE
const lineText = state.doc.textBetween(range.lineStart, range.lineEnd);
const replacement = computeTodoReplacement(lineText);
transaction.replaceWith(range.lineStart, range.lineEnd,
    state.schema.text(replacement)  // Plain text!
);
```

The `textBetween()` without leafText uses empty string by default, so wiki_link content is invisible:
- Input doc: `[text: "- [ ] test "] [wiki_link] [text: " "]`
- `textBetween` returns: `"- [ ] test  "`
- `computeTodoReplacement` returns: `"- [x] test  "`
- Full line replaced with plain text - wiki_link node destroyed!

**Fix:** For existing todos, only replace the checkbox character:
```typescript
if (todoMatch) {
    const checkboxPos = range.lineStart + indent.length + 3;
    transaction.replaceWith(
        checkboxPos,
        checkboxPos + 1,
        state.schema.text(newChecked)
    );
}
```

## Why the PR Fix Was Incomplete

The PR (claude/issue-51-20260119-1946) fixed:
- The serializer (for saving to markdown)
- The toggle function (for preserving inline nodes)

But missed:
- The `buildTodoDecorations` function's `leafText: "\n"` parameter

This meant decorations never applied when wikilinks were present, so:
- Raw `- [ ] ` was visible (no decoration hiding it)
- Checkbox widget wasn't rendered
- The toggle fix was irrelevant because there was nothing to click

## Document Structure Reference

A paragraph with `- [ ] text [[link]] more`:

```json
{
  "type": "paragraph",
  "content": [
    { "type": "text", "text": "- [ ] text " },
    {
      "type": "wiki_link",
      "attrs": { "href": "link", "title": "link" }
    },
    { "type": "text", "text": " more" }
  ]
}
```

Key insight: `wiki_link` is an **atom node** - it has no `content` property, just `attrs`. It's not a container, it's a leaf.

## Additional Bugs Fixed

### Bug: Enter Creates Bullet Instead of Checkbox

**Symptom:** Pressing Enter at end of todo line creates `• ` bullet instead of new checkbox.

**Root Cause:** `handleTodoEnter` wasn't using `leafText: ""` in `textBetween()`, AND wasn't handling `LIST_TODO_REGEX` format.

**Fix:**
1. Add `leafText: ""` to textBetween call
2. Add handling for both `TODO_REGEX` and `LIST_TODO_REGEX`

### Bug: Backspace Doesn't Delete Empty Todos

**Symptom:** Can't delete empty checkbox lines with Backspace, especially indented ones.

**Root Causes:**
1. `handleTodoBackspace` only checked `TODO_REGEX`, not `LIST_TODO_REGEX`
2. Position check was too strict - only worked if cursor at exact content start
3. Indented todos have different marker offsets

**Fix:**
1. Handle both `TODO_REGEX` and `LIST_TODO_REGEX` formats
2. Allow backspace if todo is empty/whitespace-only AND cursor is anywhere at or after marker
3. Calculate marker lengths correctly for each format:
   - Standalone: `indent.length + 6` (or 5 without trailing space)
   - List item: `4` (or 3 without trailing space)

## Testing Procedure

1. Start fresh: `bun run dev`
2. Open a note
3. Type `- [ ] test ` (creates todo with checkbox visible)
4. Type `[[` to trigger autocomplete
5. Select a note
6. **Verify:** Checkbox still renders (not raw `- [ ] `)
7. Click checkbox to toggle
8. **Verify:** Wikilink still present, checkbox toggles correctly
9. Press Enter at end of todo
10. **Verify:** New empty checkbox created (not bullet `• `)
11. Press Backspace on empty checkbox
12. **Verify:** Checkbox marker removed, empty line remains
13. Test with indented todos (add 2 spaces before `- [ ]`)
14. **Verify:** All operations work on indented todos too
15. Save note, reload
16. **Verify:** Content preserved correctly
