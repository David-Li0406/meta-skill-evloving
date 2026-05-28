#!/usr/bin/env python3
"""
Beginner Example 03: Screenshots

Learning Objectives:
- Capture full-page screenshots
- Take element-specific screenshots
- Set custom viewport sizes for responsive testing
- Organize screenshot outputs
- Use screenshots for debugging and documentation

Screenshots are one of the most valuable tools in web testing:
- Visual verification of UI state
- Before/after comparisons
- Debugging what went wrong
- Generating documentation
- Visual regression testing
"""

import os
from playwright.sync_api import sync_playwright


def test_screenshots():
    """Demonstrate various screenshot techniques"""

    # Setup
    current_dir = os.path.dirname(os.path.abspath(__file__))
    html_file_path = os.path.join(current_dir, 'sample.html')
    file_url = f'file://{html_file_path}'

    # Create screenshots directory if it doesn't exist
    screenshots_dir = os.path.join(current_dir, 'screenshots')
    os.makedirs(screenshots_dir, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        print("=" * 60)
        print("SCREENSHOT TESTING DEMO")
        print("=" * 60)
        print()

        # ===== TEST 1: Full-Page Screenshot (Default Viewport) =====
        print("Test 1: Full-Page Screenshot (Desktop)")
        print("-" * 60)

        page = browser.new_page()
        page.goto(file_url)

        # Take a full-page screenshot
        # full_page=True captures everything, even content below the fold
        screenshot_path = os.path.join(screenshots_dir, '01_full_page_desktop.png')
        page.screenshot(path=screenshot_path, full_page=True)

        print(f"✓ Screenshot saved: {screenshot_path}")
        print(f"  Viewport: {page.viewport_size['width']}x{page.viewport_size['height']}")
        print()

        page.close()

        # ===== TEST 2: Mobile Viewport Screenshot =====
        print("Test 2: Mobile Viewport Screenshot")
        print("-" * 60)

        # Create a new page with mobile viewport
        page = browser.new_page()

        # Set viewport to mobile dimensions (iPhone 12 Pro)
        page.set_viewport_size({"width": 390, "height": 844})

        page.goto(file_url)

        screenshot_path = os.path.join(screenshots_dir, '02_full_page_mobile.png')
        page.screenshot(path=screenshot_path, full_page=True)

        print(f"✓ Screenshot saved: {screenshot_path}")
        print(f"  Viewport: 390x844 (iPhone 12 Pro)")
        print()

        page.close()

        # ===== TEST 3: Tablet Viewport Screenshot =====
        print("Test 3: Tablet Viewport Screenshot")
        print("-" * 60)

        page = browser.new_page()

        # Set viewport to tablet dimensions (iPad)
        page.set_viewport_size({"width": 768, "height": 1024})

        page.goto(file_url)

        screenshot_path = os.path.join(screenshots_dir, '03_full_page_tablet.png')
        page.screenshot(path=screenshot_path, full_page=True)

        print(f"✓ Screenshot saved: {screenshot_path}")
        print(f"  Viewport: 768x1024 (iPad)")
        print()

        page.close()

        # ===== TEST 4: Element-Specific Screenshots =====
        print("Test 4: Element-Specific Screenshots")
        print("-" * 60)

        page = browser.new_page()
        page.goto(file_url)

        # Screenshot the header only
        header = page.locator('#main-header')
        header_path = os.path.join(screenshots_dir, '04_element_header.png')
        header.screenshot(path=header_path)
        print(f"✓ Header screenshot: {header_path}")

        # Screenshot the highlight box
        highlight = page.locator('.highlight-box')
        highlight_path = os.path.join(screenshots_dir, '05_element_highlight_box.png')
        highlight.screenshot(path=highlight_path)
        print(f"✓ Highlight box screenshot: {highlight_path}")

        # Screenshot the first card
        first_card = page.locator('.card').first
        card_path = os.path.join(screenshots_dir, '06_element_first_card.png')
        first_card.screenshot(path=card_path)
        print(f"✓ First card screenshot: {card_path}")

        print()

        # ===== TEST 5: Screenshot Before/After Pattern =====
        print("Test 5: Before/After Pattern")
        print("-" * 60)
        print("This pattern is useful for verifying UI changes")
        print()

        # Take "before" screenshot
        before_path = os.path.join(screenshots_dir, '07_before_interaction.png')
        page.screenshot(path=before_path, full_page=True)
        print(f"✓ Before screenshot: {before_path}")

        # Simulate an interaction (in a real test, you might click a button)
        # Here we'll just scroll to demonstrate
        page.evaluate('window.scrollTo(0, document.body.scrollHeight / 2)')

        # Take "after" screenshot
        after_path = os.path.join(screenshots_dir, '08_after_interaction.png')
        page.screenshot(path=after_path)  # Not full_page - just visible area
        print(f"✓ After screenshot: {after_path}")
        print()

        # ===== TEST 6: Ultra-Wide Desktop Screenshot =====
        print("Test 6: Ultra-Wide Desktop Screenshot")
        print("-" * 60)

        page.set_viewport_size({"width": 1920, "height": 1080})
        page.goto(file_url)

        ultrawide_path = os.path.join(screenshots_dir, '09_ultrawide_desktop.png')
        page.screenshot(path=ultrawide_path, full_page=True)

        print(f"✓ Screenshot saved: {ultrawide_path}")
        print(f"  Viewport: 1920x1080")
        print()

        # ===== SUMMARY =====
        print("=" * 60)
        print("SUMMARY")
        print("=" * 60)

        # Count screenshots
        screenshot_files = [f for f in os.listdir(screenshots_dir) if f.endswith('.png')]
        print(f"✓ Total screenshots taken: {len(screenshot_files)}")
        print(f"✓ Screenshots directory: {screenshots_dir}")
        print()

        print("Screenshot Types Demonstrated:")
        print("  • Full-page screenshots (desktop, tablet, mobile)")
        print("  • Element-specific screenshots")
        print("  • Before/after comparison screenshots")
        print("  • Multiple viewport sizes")
        print()

        print("Common Use Cases:")
        print("  📸 Visual regression testing")
        print("  🐛 Debugging UI issues")
        print("  📱 Responsive design verification")
        print("  📚 Automated documentation generation")
        print("  ✅ Before/after interaction verification")

        page.close()
        browser.close()

    print()
    print("✓ Screenshot testing completed successfully!")
    print(f"  View your screenshots in: {screenshots_dir}")


if __name__ == '__main__':
    test_screenshots()
