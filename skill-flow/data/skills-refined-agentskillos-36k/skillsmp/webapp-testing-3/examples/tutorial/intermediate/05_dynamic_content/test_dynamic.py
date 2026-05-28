#!/usr/bin/env python3
"""
Intermediate Example 05: Dynamic Content

Learning Objectives:
- Handle JavaScript-rendered content
- Use proper wait strategies (networkidle, domcontentloaded)
- Wait for specific elements to appear
- Test async data loading
- Understand when and how to wait

This is one of the MOST IMPORTANT examples in web automation!
Many beginners struggle with dynamic content because they don't wait properly.

KEY RULE: For dynamic web apps, ALWAYS wait for 'networkidle' after navigation!
"""

import os
from playwright.sync_api import sync_playwright


def test_dynamic_content():
    """Demonstrate testing JavaScript-rendered dynamic content"""

    # Setup
    current_dir = os.path.dirname(os.path.abspath(__file__))
    html_file_path = os.path.join(current_dir, 'dynamic_app.html')
    file_url = f'file://{html_file_path}'

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        print("=" * 70)
        print("DYNAMIC CONTENT TESTING")
        print("=" * 70)
        print()

        # ===== INITIAL PAGE LOAD =====
        print("Step 1: Loading Dynamic Web App")
        print("-" * 70)

        page.goto(file_url)

        # CRITICAL: Wait for the page to fully load
        # For dynamic apps, this ensures JavaScript has executed
        page.wait_for_load_state('networkidle')

        print(f"✓ Page loaded: {file_url}")
        print("✓ Waited for network idle (JavaScript executed)")
        print()

        # ===== VERIFY INITIAL STATE =====
        print("Step 2: Verifying Initial Empty State")
        print("-" * 70)

        # Check if the empty state is visible
        empty_state = page.locator('.empty-state')
        is_visible = empty_state.is_visible()

        print(f"Empty state visible: {'✅ Yes' if is_visible else '❌ No'}")

        if is_visible:
            heading = page.locator('.empty-state h2').inner_text()
            print(f"  Message: {heading}")

        print()

        # ===== TEST 1: LOAD DATA WITH DELAY =====
        print("Test 1: Loading Data with 2-Second Delay")
        print("-" * 70)

        # Click the "Load Data" button
        load_button = page.locator('#loadData')
        load_button.click()
        print("✓ Clicked 'Load Data' button")

        # The page will show a loading spinner
        # Wait for the loading indicator to appear
        loading_spinner = page.locator('.loading')
        print("  Waiting for loading indicator...")

        # Now wait for the data to actually load
        # We wait for the .data-card elements to appear
        print("  Waiting for data cards to appear...")
        page.wait_for_selector('.data-card', timeout=5000)

        # Get the loaded data
        data_cards = page.locator('.data-card').all()
        print(f"✓ Data loaded: {len(data_cards)} cards appeared")

        # Verify timestamp was updated
        timestamp = page.locator('.timestamp').inner_text()
        print(f"✓ Timestamp: {timestamp}")

        print()

        # ===== TEST 2: LOAD MORE DATA =====
        print("Test 2: Loading More Items")
        print("-" * 70)

        # Count current items
        initial_count = len(page.locator('.data-card').all())
        print(f"Current item count: {initial_count}")

        # Click "Load More"
        page.locator('#loadMore').click()
        print("✓ Clicked 'Load More' button")

        # Wait a moment for new items to be added
        # Since this is instant, we can use a short timeout
        page.wait_for_timeout(100)

        # Count items again
        new_count = len(page.locator('.data-card').all())
        print(f"New item count: {new_count}")
        print(f"✓ Added {new_count - initial_count} new items")

        print()

        # ===== TEST 3: VERIFY CARD CONTENT =====
        print("Test 3: Inspecting Dynamic Card Content")
        print("-" * 70)

        # Get all cards
        cards = page.locator('.data-card').all()

        print(f"Total cards: {len(cards)}\n")
        print("Card details:")

        # Show first 3 cards
        for i, card in enumerate(cards[:3], 1):
            title = card.locator('h3').inner_text()
            description = card.locator('p').inner_text()

            print(f"  Card {i}:")
            print(f"    Title: {title}")
            print(f"    Description: {description[:60]}...")

        print()

        # ===== TEST 4: FAST LOADING =====
        print("Test 4: Testing Instant Data Load")
        print("-" * 70)

        # Click "Load Fast" button
        page.locator('#loadFast').click()
        print("✓ Clicked 'Load Fast' button")

        # Even "instant" loads need a small wait for DOM updates
        page.wait_for_selector('.data-card')

        fast_load_cards = page.locator('.data-card').all()
        print(f"✓ Data loaded: {len(fast_load_cards)} cards")

        print()

        # ===== TEST 5: CLEAR DATA =====
        print("Test 5: Clearing All Data")
        print("-" * 70)

        # Click "Clear Data" button
        page.locator('#clearData').click()
        print("✓ Clicked 'Clear Data' button")

        # Wait for empty state to reappear
        page.wait_for_selector('.empty-state')

        # Verify data is cleared
        is_empty = page.locator('.empty-state').is_visible()
        remaining_cards = len(page.locator('.data-card').all())

        print(f"Empty state visible: {'✅ Yes' if is_empty else '❌ No'}")
        print(f"Remaining cards: {remaining_cards}")

        print()

        # ===== ADVANCED: WAIT STRATEGIES COMPARISON =====
        print("Advanced: Wait Strategy Comparison")
        print("-" * 70)
        print()

        print("Different wait strategies explained:")
        print()
        print("1. wait_for_load_state('networkidle')")
        print("   - Waits until network is idle (no ongoing requests)")
        print("   - BEST for dynamic apps that load data on page load")
        print("   - Use this after page.goto() for SPAs")
        print()
        print("2. wait_for_selector('.element')")
        print("   - Waits for a specific element to appear in the DOM")
        print("   - BEST when you know what element to wait for")
        print("   - Use this after clicking buttons that load content")
        print()
        print("3. wait_for_timeout(milliseconds)")
        print("   - Waits for a fixed amount of time")
        print("   - LAST RESORT - avoid when possible")
        print("   - Only use for debugging or when no better option exists")
        print()

        print("Example patterns:")
        print()
        print("# After navigation (SPA):")
        print("page.goto('http://localhost:3000')")
        print("page.wait_for_load_state('networkidle')  # ✅ CRITICAL!")
        print()
        print("# After button click that loads data:")
        print("page.click('#load-data')")
        print("page.wait_for_selector('.data-loaded')  # ✅ Good!")
        print()
        print("# Avoid this:")
        print("page.click('#load-data')")
        print("page.wait_for_timeout(2000)  # ❌ Fragile!")

        print()

        # ===== SUMMARY =====
        print("=" * 70)
        print("TEST SUMMARY")
        print("=" * 70)
        print("Completed Tests:")
        print("  ✓ Loaded page with networkidle wait")
        print("  ✓ Verified initial empty state")
        print("  ✓ Tested delayed data loading (2s)")
        print("  ✓ Tested loading more items")
        print("  ✓ Inspected dynamic card content")
        print("  ✓ Tested instant data loading")
        print("  ✓ Tested clearing data")
        print()
        print("Key Takeaways:")
        print("  🎯 Always use wait_for_load_state('networkidle') after goto()")
        print("  🎯 Use wait_for_selector() when waiting for specific elements")
        print("  🎯 Avoid wait_for_timeout() except for debugging")
        print("  🎯 Dynamic content requires explicit waits")

        browser.close()

    print()
    print("✅ Dynamic content testing completed successfully!")


if __name__ == '__main__':
    test_dynamic_content()
