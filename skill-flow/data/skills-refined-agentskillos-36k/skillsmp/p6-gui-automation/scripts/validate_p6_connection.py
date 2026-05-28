#!/usr/bin/env python3
"""
Validate P6 Professional connection.

Quick utility to test pywinauto connection to P6 Professional.
Run this script to verify automation is working before using the voice agent.

Usage:
    python validate_p6_connection.py
"""

import sys
import time

def main():
    print("=" * 60)
    print("P6 Professional Connection Validator")
    print("=" * 60)
    print()
    
    # Check pywinauto installation
    print("[1/4] Checking pywinauto installation...")
    try:
        from pywinauto import Application
        from pywinauto.findwindows import ElementNotFoundError
        print("      OK - pywinauto is installed")
    except ImportError:
        print("      FAIL - pywinauto not installed")
        print("      Run: pip install pywinauto")
        return 1
    
    # Check for P6 window
    print()
    print("[2/4] Searching for P6 Professional window...")
    
    p6_patterns = [
        ".*Primavera P6 Professional.*",
        ".*Primavera P6.*",
        ".*Oracle Primavera P6.*",
        ".*P6 Professional.*"
    ]
    
    app = None
    main_window = None
    
    for pattern in p6_patterns:
        try:
            app = Application(backend="uia").connect(title_re=pattern, timeout=2)
            main_window = app.window(title_re=pattern)
            print(f"      FOUND - Pattern matched: {pattern}")
            break
        except ElementNotFoundError:
            continue
        except Exception as e:
            continue
    
    if not main_window:
        print("      NOT FOUND - P6 Professional is not running")
        print()
        print("      Please start P6 Professional and try again.")
        print("      Make sure a project is open.")
        return 1
    
    # Get window info
    print()
    print("[3/4] Gathering window information...")
    
    try:
        title = main_window.window_text()
        print(f"      Window Title: {title}")
    except Exception as e:
        print(f"      Could not get title: {e}")
        title = "Unknown"
    
    try:
        rect = main_window.rectangle()
        print(f"      Position: ({rect.left}, {rect.top})")
        print(f"      Size: {rect.width()} x {rect.height()}")
    except Exception as e:
        print(f"      Could not get size: {e}")
    
    try:
        is_visible = main_window.is_visible()
        is_enabled = main_window.is_enabled()
        print(f"      Visible: {is_visible}")
        print(f"      Enabled: {is_enabled}")
    except Exception as e:
        print(f"      Could not get state: {e}")
    
    # Test keyboard input
    print()
    print("[4/4] Testing keyboard input capability...")
    
    try:
        # Try to focus the window
        main_window.set_focus()
        time.sleep(0.2)
        print("      OK - Window focused successfully")
        
        # Note: We don't actually send keys to avoid disrupting P6
        print("      OK - Keyboard input should work (ESC key ready)")
        print()
        print("      NOTE: No keys were sent to avoid disrupting your work.")
        
    except Exception as e:
        print(f"      WARNING - Could not focus window: {e}")
        print("      Keyboard automation may not work correctly.")
    
    # Summary
    print()
    print("=" * 60)
    print("RESULT: Connection Successful!")
    print("=" * 60)
    print()
    print("P6 Professional is running and accessible for automation.")
    print()
    print("Detected project:", title.replace("Primavera P6 Professional - ", ""))
    print()
    print("You can now run:")
    print('  python "P6 GUI Automation/main.py" --safe-mode')
    print()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
