#!/usr/bin/env python3
"""
Intermediate Example 06: Console Debugging

Learning Objectives:
- Capture browser console messages
- Filter by message type (log, error, warning, info, debug)
- Debug JavaScript errors and warnings
- Save console logs to file for analysis
- Monitor console output during automation

Console monitoring is CRITICAL for debugging web applications!
Many bugs only show up in the console, not in the UI.
"""

import os
from playwright.sync_api import sync_playwright


def test_console_debugging():
    """Demonstrate capturing and analyzing browser console output"""

    # Setup
    current_dir = os.path.dirname(os.path.abspath(__file__))
    html_file_path = os.path.join(current_dir, 'buggy_app.html')
    file_url = f'file://{html_file_path}'

    # Storage for console messages
    console_messages = []
    console_errors = []
    console_warnings = []

    # Create logs directory
    logs_dir = os.path.join(current_dir, 'logs')
    os.makedirs(logs_dir, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        print("=" * 70)
        print("CONSOLE DEBUGGING TEST")
        print("=" * 70)
        print()

        # ===== SETUP CONSOLE LISTENERS =====
        print("Step 1: Setting Up Console Listeners")
        print("-" * 70)

        # Define console message handler
        def handle_console_message(msg):
            """Handle all console messages"""
            message_text = msg.text
            message_type = msg.type

            # Store all messages
            console_messages.append({
                'type': message_type,
                'text': message_text
            })

            # Also categorize by type
            if message_type == 'error':
                console_errors.append(message_text)
            elif message_type == 'warning':
                console_warnings.append(message_text)

            # Print to our test output (optional - for visibility)
            type_prefix = {
                'log': '📝',
                'info': 'ℹ️',
                'warning': '⚠️',
                'error': '❌',
                'debug': '🔍'
            }.get(message_type, '📋')

            # Only print during initial load (to avoid spam)
            # In real tests, you'd typically just collect and analyze later

        # Attach the console listener BEFORE navigating
        page.on("console", handle_console_message)

        print("✓ Console listener attached")
        print("  Capturing: log, info, warning, error, debug")
        print()

        # ===== LOAD PAGE =====
        print("Step 2: Loading Page (Console Messages Will Be Captured)")
        print("-" * 70)

        page.goto(file_url)
        page.wait_for_load_state('networkidle')

        print(f"✓ Page loaded: {file_url}")
        print(f"✓ Initial console messages captured: {len(console_messages)}")
        print()

        # Show initial messages
        print("Initial page load messages:")
        for msg in console_messages[:5]:  # Show first 5
            print(f"  [{msg['type']}] {msg['text'][:60]}...")
        if len(console_messages) > 5:
            print(f"  ... and {len(console_messages) - 5} more")
        print()

        # ===== TEST DIFFERENT CONSOLE LEVELS =====
        print("Test 1: Triggering Different Console Log Levels")
        print("-" * 70)

        # Clear previous messages for this test
        initial_count = len(console_messages)

        # Click each log level button
        actions = [
            ('log', '#logMessage', 'btn-log'),
            ('info', '#logInfo', 'btn-info'),
            ('warn', '#logWarning', 'btn-warn'),
            ('error', '#logError', 'btn-error'),
        ]

        for level, selector, _ in actions:
            # Click button and wait briefly for JS to execute
            page.click(selector)
            page.wait_for_timeout(100)

        new_messages = len(console_messages) - initial_count
        print(f"✓ Triggered 4 different console log levels")
        print(f"✓ New messages captured: {new_messages}")
        print()

        # ===== TEST ERROR SCENARIOS =====
        print("Test 2: Capturing JavaScript Errors")
        print("-" * 70)

        error_count_before = len(console_errors)

        # Trigger failed API call
        page.click('button:has-text("Failed API Call")')
        page.wait_for_timeout(600)  # Wait for the setTimeout

        # Trigger error throw
        page.click('button:has-text("Throw Error")')
        page.wait_for_timeout(400)

        error_count_after = len(console_errors)
        new_errors = error_count_after - error_count_before

        print(f"✓ Triggered error scenarios")
        print(f"✓ New errors captured: {new_errors}")
        print()

        if new_errors > 0:
            print("Error messages captured:")
            for error in console_errors[-new_errors:]:
                print(f"  ❌ {error[:80]}...")
        print()

        # ===== TEST WARNING SCENARIOS =====
        print("Test 3: Capturing Warnings")
        print("-" * 70)

        warning_count_before = len(console_warnings)

        # Trigger deprecated feature warning
        page.click('button:has-text("Use Deprecated Feature")')
        page.wait_for_timeout(100)

        warning_count_after = len(console_warnings)
        new_warnings = warning_count_after - warning_count_before

        print(f"✓ Triggered warning scenarios")
        print(f"✓ New warnings captured: {new_warnings}")
        print()

        if new_warnings > 0:
            print("Warning messages captured:")
            for warning in console_warnings[-new_warnings:]:
                print(f"  ⚠️  {warning[:80]}...")
        print()

        # ===== TEST SUCCESSFUL OPERATIONS =====
        print("Test 4: Monitoring Successful Operations")
        print("-" * 70)

        messages_before = len(console_messages)

        # Trigger successful operations
        page.click('button:has-text("Load User Data")')
        page.wait_for_timeout(600)

        page.click('button:has-text("Successful Operation")')
        page.wait_for_timeout(600)

        messages_after = len(console_messages)
        new_messages = messages_after - messages_before

        print(f"✓ Triggered successful operations")
        print(f"✓ Messages captured: {new_messages}")
        print()

        # ===== ANALYZE CONSOLE OUTPUT =====
        print("Step 5: Analyzing Console Output")
        print("-" * 70)

        # Count by type
        type_counts = {}
        for msg in console_messages:
            msg_type = msg['type']
            type_counts[msg_type] = type_counts.get(msg_type, 0) + 1

        print("Console message breakdown:")
        for msg_type, count in sorted(type_counts.items()):
            print(f"  {msg_type:10} : {count:3} messages")

        print()
        print(f"Total errors:   {len(console_errors)}")
        print(f"Total warnings: {len(console_warnings)}")
        print()

        # ===== SAVE LOGS TO FILE =====
        print("Step 6: Saving Console Logs to File")
        print("-" * 70)

        # Save all messages
        all_logs_file = os.path.join(logs_dir, 'all_console_messages.txt')
        with open(all_logs_file, 'w', encoding='utf-8') as f:
            f.write("=" * 70 + "\n")
            f.write("CONSOLE LOG CAPTURE\n")
            f.write("=" * 70 + "\n\n")

            for i, msg in enumerate(console_messages, 1):
                f.write(f"[{i}] [{msg['type'].upper()}] {msg['text']}\n")

        print(f"✓ All messages saved: {all_logs_file}")

        # Save errors only
        if console_errors:
            errors_file = os.path.join(logs_dir, 'errors_only.txt')
            with open(errors_file, 'w', encoding='utf-8') as f:
                f.write("ERRORS ONLY\n")
                f.write("=" * 70 + "\n\n")
                for i, error in enumerate(console_errors, 1):
                    f.write(f"[{i}] {error}\n\n")

            print(f"✓ Errors saved: {errors_file}")

        # Save warnings only
        if console_warnings:
            warnings_file = os.path.join(logs_dir, 'warnings_only.txt')
            with open(warnings_file, 'w', encoding='utf-8') as f:
                f.write("WARNINGS ONLY\n")
                f.write("=" * 70 + "\n\n")
                for i, warning in enumerate(console_warnings, 1):
                    f.write(f"[{i}] {warning}\n\n")

            print(f"✓ Warnings saved: {warnings_file}")

        print()

        # ===== DEMONSTRATION OF FILTERING =====
        print("Advanced: Filtering Console Messages")
        print("-" * 70)
        print()

        # Example: Find specific error messages
        api_errors = [msg for msg in console_messages
                      if msg['type'] == 'error' and 'API' in msg['text']]

        print(f"API-related errors: {len(api_errors)}")
        for error in api_errors:
            print(f"  - {error['text'][:70]}...")

        print()

        # Example: Find deprecation warnings
        deprecation_warnings = [msg for msg in console_messages
                               if 'deprecated' in msg['text'].lower()]

        print(f"Deprecation warnings: {len(deprecation_warnings)}")
        for warning in deprecation_warnings:
            print(f"  - {warning['text'][:70]}...")

        print()

        # ===== SUMMARY =====
        print("=" * 70)
        print("TEST SUMMARY")
        print("=" * 70)
        print("Console Monitoring Results:")
        print(f"  Total messages captured: {len(console_messages)}")
        print(f"  Errors found: {len(console_errors)}")
        print(f"  Warnings found: {len(console_warnings)}")
        print()
        print("Actions Performed:")
        print("  ✓ Set up console message listener")
        print("  ✓ Captured messages during page load")
        print("  ✓ Triggered various console log levels")
        print("  ✓ Captured JavaScript errors")
        print("  ✓ Captured deprecation warnings")
        print("  ✓ Saved logs to files")
        print("  ✓ Demonstrated message filtering")
        print()
        print("Use Cases:")
        print("  🐛 Debugging JavaScript errors")
        print("  🔍 Finding deprecation warnings")
        print("  📊 Analyzing application behavior")
        print("  ✅ Verifying expected log output")
        print("  📝 Generating test reports with console data")
        print()
        print(f"📁 Log files saved to: {logs_dir}")

        browser.close()

    print()
    print("✅ Console debugging test completed successfully!")


if __name__ == '__main__':
    test_console_debugging()
