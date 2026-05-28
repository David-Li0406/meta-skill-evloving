#!/usr/bin/env python3
"""
Beginner Example 02: Element Discovery

Learning Objectives:
- Discover all interactive elements on a page
- Use different selector strategies (tag, class, ID, attribute)
- Filter visible vs hidden elements
- Extract element attributes

This example demonstrates how to explore a page before automating it.
This "scout first, then act" approach is a best practice in web automation.
"""

import os
from playwright.sync_api import sync_playwright


def discover_elements():
    """Discover and catalog all interactive elements on the page"""

    # Setup file URL
    current_dir = os.path.dirname(os.path.abspath(__file__))
    html_file_path = os.path.join(current_dir, 'sample.html')
    file_url = f'file://{html_file_path}'

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Navigate to the page
        page.goto(file_url)
        print(f"Loaded: {file_url}\n")

        # ===== DISCOVER BUTTONS =====
        print("=" * 50)
        print("BUTTONS")
        print("=" * 50)

        # Find all buttons on the page
        buttons = page.locator('button').all()
        print(f"✓ Found {len(buttons)} total buttons\n")

        # Inspect each button
        for i, button in enumerate(buttons, 1):
            # Check if button is visible
            is_visible = button.is_visible()

            # Get button text
            text = button.inner_text() if is_visible else "[hidden]"

            # Get button classes
            classes = button.get_attribute('class') or "no classes"

            # Display results
            visibility = "👁️  visible" if is_visible else "🚫 hidden"
            print(f"Button {i}:")
            print(f"  Text: {text}")
            print(f"  Classes: {classes}")
            print(f"  Visibility: {visibility}\n")

        # ===== DISCOVER LINKS =====
        print("=" * 50)
        print("LINKS")
        print("=" * 50)

        # Find all links with href attribute
        links = page.locator('a[href]').all()
        print(f"✓ Found {len(links)} links\n")

        for i, link in enumerate(links, 1):
            text = link.inner_text()
            href = link.get_attribute('href')
            target = link.get_attribute('target') or "(same window)"

            print(f"Link {i}:")
            print(f"  Text: {text}")
            print(f"  URL: {href}")
            print(f"  Target: {target}\n")

        # ===== DISCOVER INPUT FIELDS =====
        print("=" * 50)
        print("INPUT FIELDS")
        print("=" * 50)

        # Find different types of inputs
        text_inputs = page.locator('input[type="text"], input[type="email"], input[type="password"]').all()
        print(f"✓ Found {len(text_inputs)} text-based inputs\n")

        for i, input_field in enumerate(text_inputs, 1):
            input_type = input_field.get_attribute('type')
            name = input_field.get_attribute('name')
            placeholder = input_field.get_attribute('placeholder')
            input_id = input_field.get_attribute('id')

            print(f"Input {i}:")
            print(f"  Type: {input_type}")
            print(f"  ID: {input_id}")
            print(f"  Name: {name}")
            print(f"  Placeholder: {placeholder}\n")

        # ===== DISCOVER SELECT DROPDOWNS =====
        print("=" * 50)
        print("DROPDOWNS")
        print("=" * 50)

        selects = page.locator('select').all()
        print(f"✓ Found {len(selects)} dropdown(s)\n")

        for i, select in enumerate(selects, 1):
            name = select.get_attribute('name')
            select_id = select.get_attribute('id')

            # Find all options in the dropdown
            options = select.locator('option').all()

            print(f"Select {i}:")
            print(f"  ID: {select_id}")
            print(f"  Name: {name}")
            print(f"  Options ({len(options)}):")

            for option in options:
                value = option.get_attribute('value')
                text = option.inner_text()
                print(f"    - {text} (value: {value})")
            print()

        # ===== DISCOVER TEXTAREAS =====
        print("=" * 50)
        print("TEXTAREAS")
        print("=" * 50)

        textareas = page.locator('textarea').all()
        print(f"✓ Found {len(textareas)} textarea(s)\n")

        for i, textarea in enumerate(textareas, 1):
            name = textarea.get_attribute('name')
            rows = textarea.get_attribute('rows')
            placeholder = textarea.get_attribute('placeholder')

            print(f"Textarea {i}:")
            print(f"  Name: {name}")
            print(f"  Rows: {rows}")
            print(f"  Placeholder: {placeholder}\n")

        # ===== DISCOVER HEADINGS =====
        print("=" * 50)
        print("HEADINGS")
        print("=" * 50)

        # Find all headings (h1, h2, h3, etc.)
        headings = page.locator('h1, h2').all()
        print(f"✓ Found {len(headings)} heading(s)\n")

        for heading in headings:
            # Get the tag name by checking which selector matches
            tag = "h1" if heading.evaluate('el => el.tagName') == "H1" else "h2"
            text = heading.inner_text()
            print(f"<{tag}>: {text}")

        # ===== TEST VISIBILITY =====
        print("\n" + "=" * 50)
        print("VISIBILITY TESTING")
        print("=" * 50)

        # Find all spans in the visibility section
        visibility_section = page.locator('.section').nth(3)  # 4th section (0-indexed)
        spans = visibility_section.locator('span').all()

        print(f"✓ Found {len(spans)} span elements\n")

        for i, span in enumerate(spans, 1):
            is_visible = span.is_visible()
            text = span.inner_text() if is_visible else "[cannot get text - hidden]"
            visibility = "✓ Visible" if is_visible else "✗ Hidden"

            print(f"Span {i}: {visibility}")
            if is_visible:
                print(f"  Text: {text}\n")
            else:
                print()

        # ===== SUMMARY =====
        print("=" * 50)
        print("DISCOVERY SUMMARY")
        print("=" * 50)
        print(f"Total buttons: {len(buttons)}")
        print(f"Total links: {len(links)}")
        print(f"Total text inputs: {len(text_inputs)}")
        print(f"Total dropdowns: {len(selects)}")
        print(f"Total textareas: {len(textareas)}")
        print(f"Total headings: {len(headings)}")

        browser.close()

    print("\n✓ Element discovery completed!")


if __name__ == '__main__':
    discover_elements()
