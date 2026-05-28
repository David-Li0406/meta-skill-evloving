---
name: Screenshot Testing
description: This skill should be used when the user asks to "test UI with screenshots", "screenshot testing", "visual testing", "compare UI screenshots", "verify UI layout", "take screenshot for testing", or when using screenshot MCP tools (list_windows, list_displays, screenshot_window, screenshot_screen, screenshot_region) for testing purposes. Provides guidance on effective screenshot-based UI testing workflows.
---

# Screenshot Testing

A guide for conducting effective UI testing using screenshots. This skill covers the screenshot-mcp tools, testing workflows, and comparison strategies for native application testing.

## Configuration

Check for plugin settings at `.claude/screenshot.local.md` before taking screenshots.

**Settings file format:**
```markdown
---
default_save_dir: /path/to/screenshots
---
```

When settings file exists:
1. Read the file using the Read tool
2. Parse YAML frontmatter to extract `default_save_dir`
3. Use this path as `save_dir` when user wants to save screenshots
4. If user specifies a different path, use their path instead

When settings file does not exist:
- Ask user if they want screenshots saved
- If yes, ask for save location or suggest creating settings file

## Available MCP Tools

The screenshot MCP server provides 5 tools:

| Tool | Purpose | Key Parameters |
|------|---------|----------------|
| `list_windows` | Discover all visible windows | None |
| `list_displays` | List all monitors/displays | None |
| `screenshot_window` | Capture specific window | `window_id` or `window_title`, `save_dir` |
| `screenshot_screen` | Capture entire display | `display_id`, `save_dir` |
| `screenshot_region` | Capture screen region | `x`, `y`, `width`, `height`, `save_dir` |

## Testing Workflow

### Step 1: Identify Target Window

Before capturing, identify the correct window:

```
1. Call list_windows to get all visible windows
2. Find target by app name or title
3. Note the window ID for screenshot_window
```

Window matching strategies:
- **By app name**: Look for `app` field (e.g., "Electron", "Simulator")
- **By title**: Use `window_title` parameter for fuzzy matching
- **By bounds**: Check `bounds` to identify window by size/position

### Step 2: Capture Screenshot

Choose the appropriate capture method:

- **Single window**: Use `screenshot_window` with window ID or title
- **Full screen**: Use `screenshot_screen` for entire display
- **Specific area**: Use `screenshot_region` for precise coordinates

### Step 3: Analyze Results

After capturing, analyze the screenshot for:
- Layout correctness (element positions, spacing)
- Visual elements (colors, fonts, icons)
- Content accuracy (text, data display)
- Responsive behavior (proper sizing)

## Comparison Testing

For detecting UI changes between versions:

### Baseline Workflow

1. **Create baseline**: Capture screenshots with `save_dir` parameter
2. **Store organized**: Screenshots save as `{save_dir}/YYYY-MM-DD/YYYYMMDD_HHMMSS.png`
3. **Compare later**: Capture new screenshots and compare visually

### Visual Comparison Approach

When comparing screenshots:

1. Capture current state screenshot
2. Load baseline screenshot from saved location
3. Compare visually for differences:
   - Layout shifts
   - Missing/extra elements
   - Color or style changes
   - Text content differences

Report findings with specific observations about what changed.

## Multi-Display Testing

For applications spanning multiple monitors:

1. Call `list_displays` to see all available displays
2. Note display IDs and bounds for positioning context
3. Use `screenshot_screen` with specific `display_id`
4. Consider window positions relative to display bounds

## Platform Support

| Platform | Status | Notes |
|----------|--------|-------|
| macOS | Supported | Requires Screen Recording permission |
| Windows | Planned | Future release |
| Linux | Planned | Future release |

On macOS, grant Screen Recording permission in System Settings > Privacy & Security > Screen Recording.

## Best Practices

### Window Identification

- Always call `list_windows` before `screenshot_window` to get fresh window IDs
- Window IDs can change when windows close/reopen
- Use `window_title` for more stable identification

### Screenshot Organization

- Use `save_dir` parameter for regression testing
- Screenshots auto-organize by date
- Keep baseline screenshots in version control

### Testing Strategy

- Capture at consistent window sizes for comparison
- Test on single display first, then multi-display
- Document expected visual state before testing

## Additional Resources

### Examples

For practical testing examples, see:
- **`examples/electron-app-testing.md`** - Testing an Electron application login flow

### Reference Files

For detailed patterns:
- **`references/testing-patterns.md`** - Common UI testing patterns and strategies
