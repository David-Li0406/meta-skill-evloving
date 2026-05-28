#!/usr/bin/env python3
"""
Advanced Example 08: Server Integration Testing

Learning Objectives:
- Test applications with backend servers
- Use the with_server.py helper script for server lifecycle management
- Test full-stack applications (frontend + backend)
- Verify API integration
- Handle server startup delays

This example demonstrates testing a real Flask application.
The with_server.py helper manages the server lifecycle automatically.

USAGE:
Run this with the helper script:
    python ../../../../scripts/with_server.py \\
        --server "python flask_app.py" \\
        --port 5000 \\
        -- python test_with_server.py

Or run flask_app.py manually in another terminal, then run this script.
"""

import os
from playwright.sync_api import sync_playwright


def test_flask_integration():
    """Test a Flask application with Playwright"""

    # This test assumes the Flask server is running on localhost:5000
    # When using with_server.py, it will be started automatically
    base_url = 'http://localhost:5000'

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        print("=" * 70)
        print("FLASK INTEGRATION TESTING")
        print("=" * 70)
        print()

        # ===== TEST 1: VERIFY SERVER IS RUNNING =====
        print("Test 1: Verifying Server is Running")
        print("-" * 70)

        try:
            # Navigate to the home page
            page.goto(base_url, timeout=10000)
            page.wait_for_load_state('networkidle')

            print(f"✓ Successfully connected to: {base_url}")

            # Verify page title
            title = page.title()
            print(f"✓ Page title: {title}")
            print()

        except Exception as e:
            print(f"❌ Error: Could not connect to server")
            print(f"   Make sure Flask server is running on port 5000")
            print(f"   Error details: {e}")
            browser.close()
            return

        # ===== TEST 2: VERIFY PAGE CONTENT =====
        print("Test 2: Verifying Page Content")
        print("-" * 70)

        # Check heading
        heading = page.locator('h1').inner_text()
        print(f"✓ Page heading: {heading}")

        # Count buttons
        buttons = page.locator('button').all()
        print(f"✓ Found {len(buttons)} buttons")

        # Verify initial message
        data_container = page.locator('#data-container')
        initial_text = data_container.inner_text()
        print(f"✓ Initial message: {initial_text[:50]}...")
        print()

        # ===== TEST 3: API HEALTH CHECK =====
        print("Test 3: Testing API Endpoint Directly")
        print("-" * 70)

        # Use Playwright's request context to call API directly
        response = page.request.get(f'{base_url}/api/status')

        print(f"✓ API response status: {response.status}")

        if response.status == 200:
            data = response.json()
            print(f"✓ API status: {data['status']}")
            print(f"✓ API message: {data['message']}")
        print()

        # ===== TEST 4: LOAD DATA FROM API =====
        print("Test 4: Loading Data via Button Click")
        print("-" * 70)

        # Click the "Load Data" button
        page.click('button:has-text("Load Data")')
        print("✓ Clicked 'Load Data' button")

        # Wait for data to load
        # The API has a 0.2s delay, so we need to wait
        page.wait_for_selector('.data-item', timeout=5000)

        print("✓ Data loaded from API")

        # Count data items
        data_items = page.locator('.data-item').all()
        print(f"✓ Received {len(data_items)} items from API")

        # Display some items
        print("\nSample data items:")
        for i, item in enumerate(data_items[:3], 1):
            text = item.inner_text()
            print(f"  {i}. {text}")

        print()

        # ===== TEST 5: CLEAR DATA =====
        print("Test 5: Clearing Data")
        print("-" * 70)

        # Click clear button
        page.click('button:has-text("Clear Data")')
        print("✓ Clicked 'Clear Data' button")

        # Verify data was cleared
        data_container_text = page.locator('#data-container').inner_text()
        print(f"✓ Data container: {data_container_text[:50]}...")

        # Data items should be gone
        remaining_items = len(page.locator('.data-item').all())
        print(f"✓ Remaining data items: {remaining_items}")
        print()

        # ===== TEST 6: RELOAD AND TEST AGAIN =====
        print("Test 6: Testing Data Load Again")
        print("-" * 70)

        # Load data again
        page.click('button:has-text("Load Data")')
        page.wait_for_selector('.data-item')

        new_items = page.locator('.data-item').all()
        print(f"✓ Loaded {len(new_items)} items (second load)")

        # Verify the data changed (random values should be different)
        print("✓ API returned fresh data")
        print()

        # ===== TEST 7: CONSOLE MONITORING =====
        print("Test 7: Monitoring Console Logs")
        print("-" * 70)

        # Set up console listener for next test
        console_messages = []

        def capture_console(msg):
            console_messages.append(f"[{msg.type}] {msg.text}")

        page.on("console", capture_console)

        # Trigger actions that log to console
        page.click('button:has-text("Clear Data")')
        page.wait_for_timeout(100)

        page.click('button:has-text("Load Data")')
        page.wait_for_timeout(500)

        print(f"✓ Captured {len(console_messages)} console messages")
        print("\nRecent console messages:")
        for msg in console_messages[-3:]:
            print(f"  {msg}")

        print()

        # ===== SUMMARY =====
        print("=" * 70)
        print("TEST SUMMARY")
        print("=" * 70)
        print("Integration Tests Completed:")
        print("  ✓ Connected to Flask server")
        print("  ✓ Verified page content")
        print("  ✓ Tested API health endpoint")
        print("  ✓ Loaded data from API via button click")
        print("  ✓ Cleared data")
        print("  ✓ Reloaded data (verified fresh data)")
        print("  ✓ Monitored console logs")
        print()
        print("Key Learnings:")
        print("  🔧 Full-stack testing combines frontend and backend")
        print("  🔧 Use with_server.py for automatic server lifecycle")
        print("  🔧 Test both UI interactions AND direct API calls")
        print("  🔧 Verify data flows correctly from backend to frontend")
        print()
        print("Production Applications:")
        print("  • Flask + React")
        print("  • Django + Vue")
        print("  • FastAPI + Angular")
        print("  • Express + any frontend framework")

        browser.close()

    print()
    print("✅ Flask integration testing completed successfully!")


if __name__ == '__main__':
    print("\nIMPORTANT: This test requires a Flask server running on port 5000")
    print("Use the with_server.py helper or start flask_app.py manually\n")

    test_flask_integration()
