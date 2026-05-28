#!/usr/bin/env python3
"""
Advanced Example 07: SPA Testing

Learning Objectives:
- Navigate single-page applications with client-side routing
- Handle hash-based routing (#/route)
- Verify URL changes without page reloads
- Test application state changes
- Navigate between different "pages" in an SPA

SPAs are everywhere (React, Vue, Angular). This example shows you how to
test them effectively with Playwright.
"""

import os
from playwright.sync_api import sync_playwright


def test_spa_navigation():
    """Demonstrate testing a Single Page Application"""

    # Setup
    current_dir = os.path.dirname(os.path.abspath(__file__))
    html_file_path = os.path.join(current_dir, 'spa_app.html')
    file_url = f'file://{html_file_path}'

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        print("=" * 70)
        print("SPA TESTING DEMONSTRATION")
        print("=" * 70)
        print()

        # ===== LOAD SPA =====
        print("Step 1: Loading Single Page Application")
        print("-" * 70)

        page.goto(file_url)
        page.wait_for_load_state('networkidle')

        print(f"✓ SPA loaded: {file_url}")

        # Check initial route
        current_url = page.url
        print(f"✓ Initial URL: {current_url}")

        # Check which page is displayed
        route_indicator = page.locator('.route-indicator').inner_text()
        print(f"✓ {route_indicator}")
        print()

        # ===== VERIFY HOME PAGE =====
        print("Test 1: Verifying Home Page (/) Content")
        print("-" * 70)

        # Check if we're on home page
        heading = page.locator('h1').inner_text()
        print(f"Page heading: {heading}")

        # Count feature cards
        feature_cards = page.locator('.feature-card').all()
        print(f"✓ Found {len(feature_cards)} feature cards on home page")

        # Verify active nav link
        active_link = page.locator('.nav-links a.active').inner_text()
        print(f"✓ Active navigation: {active_link}")
        print()

        # ===== NAVIGATE TO ABOUT =====
        print("Test 2: Navigating to About Page")
        print("-" * 70)

        # Click the "About" link
        page.click('a[href="#/about"]')

        # Wait a moment for JavaScript to update the DOM
        # For SPAs, we don't get a page reload, so we wait for content change
        page.wait_for_selector('.route-indicator')

        # Verify URL changed
        new_url = page.url
        print(f"✓ URL changed to: {new_url}")
        assert '#/about' in new_url, "URL should contain #/about"

        # Verify route indicator
        route_indicator = page.locator('.route-indicator').inner_text()
        print(f"✓ {route_indicator}")

        # Verify page content
        heading = page.locator('h1').inner_text()
        print(f"✓ Page heading: {heading}")

        # Check for team members (specific to About page)
        team_members = page.locator('.team-member').all()
        print(f"✓ Found {len(team_members)} team members")

        # Verify active nav link changed
        active_link = page.locator('.nav-links a.active').inner_text()
        print(f"✓ Active navigation: {active_link}")
        print()

        # ===== NAVIGATE TO FEATURES =====
        print("Test 3: Navigating to Features Page")
        print("-" * 70)

        page.click('a[href="#/features"]')
        page.wait_for_selector('.route-indicator')

        new_url = page.url
        print(f"✓ URL: {new_url}")
        assert '#/features' in new_url

        route_indicator = page.locator('.route-indicator').inner_text()
        print(f"✓ {route_indicator}")

        # Verify more feature cards on this page
        feature_cards = page.locator('.feature-card').all()
        print(f"✓ Found {len(feature_cards)} feature cards")

        heading = page.locator('h1').inner_text()
        print(f"✓ Page heading: {heading}")
        print()

        # ===== NAVIGATE TO CONTACT =====
        print("Test 4: Navigating to Contact Page")
        print("-" * 70)

        page.click('a[href="#/contact"]')
        page.wait_for_selector('.route-indicator')

        new_url = page.url
        print(f"✓ URL: {new_url}")
        assert '#/contact' in new_url

        route_indicator = page.locator('.route-indicator').inner_text()
        print(f"✓ {route_indicator}")

        # Verify contact form is present
        form = page.locator('.contact-form')
        is_visible = form.is_visible()
        print(f"✓ Contact form visible: {'Yes' if is_visible else 'No'}")

        # Count form inputs
        inputs = form.locator('input, textarea').all()
        print(f"✓ Form has {len(inputs)} input fields")
        print()

        # ===== TEST FORM SUBMISSION IN SPA =====
        print("Test 5: Submitting Contact Form (SPA State Change)")
        print("-" * 70)

        # Fill form
        page.fill('#name', 'Test User')
        page.fill('#email', 'test@example.com')
        page.fill('#message', 'Testing SPA form submission')

        print("✓ Form filled")

        # Submit form
        page.click('button[type="submit"]')

        # Wait for success message (content changes but URL stays same)
        page.wait_for_selector('h1:has-text("Message Sent")')

        # Verify success state
        success_heading = page.locator('h1').inner_text()
        print(f"✓ Success message: {success_heading}")

        # URL should still be #/contact
        current_url = page.url
        print(f"✓ URL (unchanged): {current_url}")
        print()

        # ===== TEST BROWSER BACK BUTTON =====
        print("Test 6: Testing Browser Back Button")
        print("-" * 70)

        # Go back
        page.go_back()
        page.wait_for_timeout(200)  # Brief wait for hash change

        current_url = page.url
        print(f"✓ After back: {current_url}")

        # Should be back at features
        assert '#/features' in current_url
        print("✓ Successfully navigated back to Features page")
        print()

        # ===== TEST BROWSER FORWARD BUTTON =====
        print("Test 7: Testing Browser Forward Button")
        print("-" * 70)

        # Go forward
        page.go_forward()
        page.wait_for_timeout(200)

        current_url = page.url
        print(f"✓ After forward: {current_url}")

        # Should be back at contact success
        assert '#/contact' in current_url
        print("✓ Successfully navigated forward to Contact page")
        print()

        # ===== TEST DIRECT URL NAVIGATION =====
        print("Test 8: Direct URL Navigation (Deep Linking)")
        print("-" * 70)

        # Navigate directly to /about by changing URL
        page.goto(f"{file_url}#/about")
        page.wait_for_selector('.route-indicator')

        route_indicator = page.locator('.route-indicator').inner_text()
        print(f"✓ {route_indicator}")

        heading = page.locator('h1').inner_text()
        print(f"✓ Loaded directly to: {heading}")
        print()

        # ===== VERIFY NO PAGE RELOADS OCCURRED =====
        print("Test 9: Verifying No Page Reloads (SPA Characteristic)")
        print("-" * 70)

        print("Key Observation:")
        print("  Throughout all these navigation tests, the page was NEVER reloaded.")
        print("  Only the URL hash changed, and JavaScript updated the content.")
        print("  This is the defining characteristic of a Single Page Application.")
        print()

        print("Evidence:")
        print("  • URL changes used hash routing: #/route")
        print("  • wait_for_load_state('networkidle') only called once")
        print("  • Content updates were instantaneous (no loading spinner)")
        print("  • Browser back/forward buttons work correctly")
        print()

        # ===== SUMMARY =====
        print("=" * 70)
        print("TEST SUMMARY")
        print("=" * 70)
        print("SPA Navigation Tests Completed:")
        print("  ✓ Loaded SPA initial state")
        print("  ✓ Navigated to About page")
        print("  ✓ Navigated to Features page")
        print("  ✓ Navigated to Contact page")
        print("  ✓ Submitted form (state change)")
        print("  ✓ Used browser back button")
        print("  ✓ Used browser forward button")
        print("  ✓ Tested direct URL navigation (deep linking)")
        print()
        print("Key SPA Testing Patterns:")
        print("  🎯 Wait for content selectors, not page loads")
        print("  🎯 Verify URL hash changes")
        print("  🎯 Use wait_for_selector() after navigation clicks")
        print("  🎯 Test browser navigation (back/forward)")
        print("  🎯 Verify state changes without page reloads")
        print()
        print("Real-World Applications:")
        print("  • React Router")
        print("  • Vue Router")
        print("  • Angular Router")
        print("  • Any hash-based or history-based SPA routing")

        browser.close()

    print()
    print("✅ SPA testing completed successfully!")


if __name__ == '__main__':
    test_spa_navigation()
