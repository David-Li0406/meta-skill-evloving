# Playwright API Reference

Quick reference for autonomous browser control using Playwright.

## Page Navigation

```python
page.goto(url, wait_until='networkidle')  # Navigate
page.go_back()  # Browser back button
page.reload()  # Refresh page
page.wait_for_url(pattern)  # Wait for navigation
```

## Element Selectors

### Semantic Selectors (Recommended)

```python
page.get_by_role("button", name="Submit")  # By ARIA role
page.get_by_label("Email address")  # By form label
page.get_by_text("Welcome")  # By visible text
page.get_by_placeholder("Enter name")  # By placeholder
page.get_by_test_id("login-button")  # By data-testid
```

### CSS Selectors

```python
page.locator("#element-id")  # ID
page.locator(".class-name")  # Class
page.locator("button")  # Tag
page.locator("[data-custom]")  # Attribute
```

## Element Actions

```python
element.click()  # Click element
element.fill("text")  # Fill input
element.clear()  # Clear input
element.press("Enter")  # Press key
element.select_option("value")  # Select dropdown option
element.check()  # Check checkbox
element.uncheck()  # Uncheck checkbox
```

## Element State

```python
element.is_visible()  # Visibility check
element.is_enabled()  # Enabled check
element.is_checked()  # Checkbox state
element.inner_text()  # Get text content
element.get_attribute("href")  # Get attribute
element.count()  # Count matching elements
```

## Waiting

```python
page.wait_for_selector("#element")  # Wait for element
page.wait_for_timeout(1000)  # Wait milliseconds
page.wait_for_load_state("networkidle")  # Wait for network
element.wait_for()  # Wait for element state
```

## Console & Network

```python
# Monitor console
page.on("console", lambda msg: print(msg.text))

# Track requests
page.on("request", lambda req: print(req.url))

# Track responses
page.on("response", lambda res: print(res.status))
```

## Evaluation

```python
# Execute JavaScript
result = page.evaluate("() => document.title")

# Get element property
value = element.evaluate("el => el.value")
```

## Viewport

```python
page.set_viewport_size({"width": 375, "height": 667})  # Mobile
page.set_viewport_size({"width": 1920, "height": 1080})  # Desktop
```

## Screenshots (Optional)

```python
page.screenshot(path="page.png")  # Full page
element.screenshot(path="element.png")  # Element only
```

## Multi-tab

```python
page2 = context.new_page()  # Open new tab
pages = context.pages  # Get all pages
page.close()  # Close tab
```

## Best Practices

1. Use semantic selectors over CSS when possible
2. Always check `is_visible()` before interaction
3. Use `wait_until='networkidle'` for dynamic content
4. Monitor console errors for JavaScript failures
5. Set appropriate timeouts for slow networks
