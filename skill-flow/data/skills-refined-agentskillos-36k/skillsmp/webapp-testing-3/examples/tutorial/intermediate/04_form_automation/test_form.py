#!/usr/bin/env python3
"""
Intermediate Example 04: Form Automation

Learning Objectives:
- Fill text inputs programmatically
- Select dropdown options
- Check/uncheck checkboxes and radio buttons
- Submit forms and verify submission
- Capture before/after states with screenshots

Forms are one of the most common elements to automate in web testing.
This example demonstrates all the key form interaction patterns.
"""

import os
from playwright.sync_api import sync_playwright


def test_form_automation():
    """Demonstrate comprehensive form automation"""

    # Setup
    current_dir = os.path.dirname(os.path.abspath(__file__))
    html_file_path = os.path.join(current_dir, 'form_app.html')
    file_url = f'file://{html_file_path}'

    # Create screenshots directory
    screenshots_dir = os.path.join(current_dir, 'screenshots')
    os.makedirs(screenshots_dir, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        print("=" * 70)
        print("FORM AUTOMATION TEST")
        print("=" * 70)
        print()

        # Navigate to the form
        page.goto(file_url)
        print(f"✓ Loaded form: {file_url}")
        print()

        # Take a screenshot of the empty form
        before_screenshot = os.path.join(screenshots_dir, '01_form_empty.png')
        page.screenshot(path=before_screenshot, full_page=True)
        print(f"📸 Screenshot (empty form): {before_screenshot}")
        print()

        # ===== FILL TEXT INPUTS =====
        print("Step 1: Filling Text Inputs")
        print("-" * 70)

        # Fill the name field
        name_value = "John Doe"
        page.fill('#name', name_value)
        print(f"✓ Name field filled: '{name_value}'")

        # Fill the email field
        email_value = "john.doe@example.com"
        page.fill('#email', email_value)
        print(f"✓ Email field filled: '{email_value}'")

        # Fill the phone field (optional field)
        phone_value = "+1 (555) 123-4567"
        page.fill('#phone', phone_value)
        print(f"✓ Phone field filled: '{phone_value}'")

        print()

        # ===== SELECT DROPDOWN OPTION =====
        print("Step 2: Selecting Dropdown Option")
        print("-" * 70)

        # Select a country from the dropdown
        # You can select by value, label, or index
        country_value = "us"
        page.select_option('#country', value=country_value)

        # Verify the selection
        selected_option = page.locator('#country option:checked').inner_text()
        print(f"✓ Country selected: '{selected_option}' (value: {country_value})")
        print()

        # ===== SELECT RADIO BUTTON =====
        print("Step 3: Selecting Radio Button")
        print("-" * 70)

        # Select a radio button
        # Radio buttons are exclusive - only one can be selected
        page.check('#source-social')
        print(f"✓ Radio button selected: 'Social Media'")

        # Verify which radio is selected
        selected_radio = page.locator('input[name="source"]:checked')
        radio_value = selected_radio.get_attribute('value')
        print(f"  Verified selection: {radio_value}")
        print()

        # ===== FILL TEXTAREA =====
        print("Step 4: Filling Textarea")
        print("-" * 70)

        message_value = """Hi there!

I'm interested in learning more about your web testing services.
I found your website through social media and would love to discuss
how you can help automate our testing processes.

Thanks!"""

        page.fill('#message', message_value)
        print(f"✓ Message textarea filled ({len(message_value)} characters)")
        print()

        # ===== CHECK CHECKBOXES =====
        print("Step 5: Checking Checkboxes")
        print("-" * 70)

        # Check the newsletter checkbox
        page.check('#newsletter')
        is_newsletter_checked = page.is_checked('#newsletter')
        print(f"✓ Newsletter checkbox: {'✅ Checked' if is_newsletter_checked else '❌ Unchecked'}")

        # Check the terms checkbox (required)
        page.check('#terms')
        is_terms_checked = page.is_checked('#terms')
        print(f"✓ Terms checkbox: {'✅ Checked' if is_terms_checked else '❌ Unchecked'}")
        print()

        # ===== SCREENSHOT BEFORE SUBMISSION =====
        print("Step 6: Capturing Filled Form")
        print("-" * 70)

        filled_screenshot = os.path.join(screenshots_dir, '02_form_filled.png')
        page.screenshot(path=filled_screenshot, full_page=True)
        print(f"📸 Screenshot (filled form): {filled_screenshot}")
        print()

        # ===== VERIFY FORM DATA =====
        print("Step 7: Verifying Form Data Before Submission")
        print("-" * 70)

        # Read back the values to verify they were set correctly
        name_verify = page.input_value('#name')
        email_verify = page.input_value('#email')
        phone_verify = page.input_value('#phone')
        country_verify = page.input_value('#country')
        message_verify = page.input_value('#message')

        print("Form Data Summary:")
        print(f"  Name:       {name_verify}")
        print(f"  Email:      {email_verify}")
        print(f"  Phone:      {phone_verify}")
        print(f"  Country:    {country_verify}")
        print(f"  Source:     {radio_value}")
        print(f"  Newsletter: {is_newsletter_checked}")
        print(f"  Terms:      {is_terms_checked}")
        print(f"  Message:    {len(message_verify)} characters")
        print()

        # ===== SUBMIT THE FORM =====
        print("Step 8: Submitting the Form")
        print("-" * 70)

        # Click the submit button
        submit_button = page.locator('button[type="submit"]')
        submit_button.click()

        # Wait a moment for JavaScript to process the submission
        page.wait_for_timeout(500)

        print("✓ Form submitted")
        print()

        # ===== VERIFY SUBMISSION SUCCESS =====
        print("Step 9: Verifying Submission Success")
        print("-" * 70)

        # Check if the success message is visible
        success_message = page.locator('#successMessage')
        is_visible = success_message.is_visible()

        print(f"Success message visible: {'✅ Yes' if is_visible else '❌ No'}")

        if is_visible:
            # Get the success message text
            heading = page.locator('#successMessage h2').inner_text()
            message = page.locator('#successMessage > p').inner_text()

            print(f"  Heading: {heading}")
            print(f"  Message: {message}")

            # Verify the submitted data is displayed correctly
            submitted_data = page.locator('#submittedData').inner_text()
            print(f"\n  Submitted data preview:")
            for line in submitted_data.split('\n')[:3]:
                print(f"    {line}")

        print()

        # ===== SCREENSHOT AFTER SUBMISSION =====
        print("Step 10: Capturing Success State")
        print("-" * 70)

        success_screenshot = os.path.join(screenshots_dir, '03_form_submitted.png')
        page.screenshot(path=success_screenshot, full_page=True)
        print(f"📸 Screenshot (after submission): {success_screenshot}")
        print()

        # ===== SUMMARY =====
        print("=" * 70)
        print("TEST SUMMARY")
        print("=" * 70)
        print("Actions Completed:")
        print("  ✓ Filled 3 text inputs (name, email, phone)")
        print("  ✓ Selected dropdown option (country)")
        print("  ✓ Selected radio button (source)")
        print("  ✓ Filled textarea (message)")
        print("  ✓ Checked 2 checkboxes (newsletter, terms)")
        print("  ✓ Submitted form")
        print("  ✓ Verified success message")
        print()
        print("Screenshots Captured:")
        print(f"  1. Empty form")
        print(f"  2. Filled form (before submission)")
        print(f"  3. Success page (after submission)")
        print()
        print(f"📁 Screenshots saved to: {screenshots_dir}")

        browser.close()

    print()
    print("✅ Form automation test completed successfully!")


if __name__ == '__main__':
    test_form_automation()
