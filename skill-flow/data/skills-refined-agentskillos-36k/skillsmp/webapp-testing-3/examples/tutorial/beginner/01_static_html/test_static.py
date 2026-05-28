#!/usr/bin/env python3
"""
Beginner Example 01: Static HTML Testing

Learning Objectives:
- Load local HTML files using file:// URLs
- Navigate to pages and extract basic information
- Understand the Playwright context manager pattern
- Verify page content programmatically

This is your first Playwright test! It demonstrates the fundamentals
of loading a static HTML file and inspecting its content.
"""

import os
from playwright.sync_api import sync_playwright


def test_static_html():
    """Test basic navigation and content extraction from a static HTML file"""

    # Step 1: Get the absolute path to our HTML file
    # Playwright needs an absolute path for file:// URLs
    current_dir = os.path.dirname(os.path.abspath(__file__))
    html_file_path = os.path.join(current_dir, 'sample.html')

    # Convert to file:// URL format
    file_url = f'file://{html_file_path}'

    # Step 2: Use the Playwright context manager
    # This ensures proper cleanup even if errors occur
    with sync_playwright() as p:

        # Step 3: Launch browser in headless mode
        # headless=True means no visible browser window (good for automation)
        browser = p.chromium.launch(headless=True)

        # Step 4: Create a new page (tab)
        page = browser.new_page()

        # Step 5: Navigate to our HTML file
        page.goto(file_url)
        print(f"✓ Loaded: {file_url}")

        # Step 6: Extract the page title
        # The <title> tag in the HTML <head>
        title = page.title()
        print(f"✓ Page title: {title}")

        # Step 7: Extract text from the main heading
        # Using a CSS selector to find the <h1> element
        heading = page.locator('h1').inner_text()
        print(f"✓ Main heading: {heading}")

        # Step 8: Extract text from the info box
        # .inner_text() gets the visible text content
        info_text = page.locator('.info strong').inner_text()
        print(f"✓ Info message: {info_text}")

        # Step 9: Count list items
        # .all() returns a list of all matching elements
        list_items = page.locator('ul li').all()
        print(f"✓ Found {len(list_items)} learning objectives")

        # Step 10: Print each learning objective
        print("\nLearning objectives:")
        for i, item in enumerate(list_items, 1):
            text = item.inner_text()
            print(f"  {i}. {text}")

        # Step 11: Close the browser
        # Good practice to clean up resources
        browser.close()

    print("\n✓ Test completed successfully!")


if __name__ == '__main__':
    test_static_html()
