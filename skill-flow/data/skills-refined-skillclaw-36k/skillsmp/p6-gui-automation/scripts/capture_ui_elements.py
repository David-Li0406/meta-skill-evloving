#!/usr/bin/env python3
"""
Capture P6 UI Elements.

Utility to discover and document P6 Professional UI controls for automation.
Outputs the window hierarchy and control identifiers.

Usage:
    python capture_ui_elements.py
    python capture_ui_elements.py --output p6_controls.json
"""

import sys
import json
import argparse
from datetime import datetime

def main():
    parser = argparse.ArgumentParser(description="Capture P6 UI Elements")
    parser.add_argument("--output", "-o", help="Output JSON file", default=None)
    parser.add_argument("--depth", "-d", type=int, help="Max depth to traverse", default=3)
    args = parser.parse_args()
    
    print("=" * 60)
    print("P6 UI Element Capture Tool")
    print("=" * 60)
    print()
    
    # Check pywinauto
    try:
        from pywinauto import Application
        from pywinauto.findwindows import ElementNotFoundError
    except ImportError:
        print("ERROR: pywinauto not installed. Run: pip install pywinauto")
        return 1
    
    # Find P6
    print("Searching for P6 Professional...")
    
    patterns = [
        ".*Primavera P6 Professional.*",
        ".*Primavera P6.*",
        ".*Oracle Primavera P6.*",
    ]
    
    app = None
    main_window = None
    
    for pattern in patterns:
        try:
            app = Application(backend="uia").connect(title_re=pattern, timeout=2)
            main_window = app.window(title_re=pattern)
            print(f"Found P6 window: {main_window.window_text()}")
            break
        except Exception:
            continue
    
    if not main_window:
        print("ERROR: P6 Professional not found. Please start P6 first.")
        return 1
    
    print()
    print(f"Capturing UI elements (depth={args.depth})...")
    print()
    
    # Capture element tree
    elements = []
    
    def capture_element(element, depth=0, path=""):
        if depth > args.depth:
            return
        
        try:
            info = {
                "path": path,
                "depth": depth,
                "control_type": element.element_info.control_type,
                "name": element.element_info.name[:100] if element.element_info.name else "",
                "class_name": element.element_info.class_name,
                "automation_id": element.element_info.automation_id,
                "is_enabled": element.is_enabled() if hasattr(element, 'is_enabled') else None,
                "is_visible": element.is_visible() if hasattr(element, 'is_visible') else None,
            }
            
            # Try to get rectangle
            try:
                rect = element.rectangle()
                info["rect"] = {
                    "left": rect.left,
                    "top": rect.top,
                    "right": rect.right,
                    "bottom": rect.bottom
                }
            except Exception:
                pass
            
            elements.append(info)
            
            # Print summary
            indent = "  " * depth
            name_display = info["name"][:40] if info["name"] else "(no name)"
            print(f"{indent}[{info['control_type']}] {name_display}")
            
            # Recursively capture children
            try:
                children = element.children()
                for i, child in enumerate(children[:20]):  # Limit children
                    child_path = f"{path}/{i}" if path else str(i)
                    capture_element(child, depth + 1, child_path)
            except Exception:
                pass
                
        except Exception as e:
            pass
    
    capture_element(main_window)
    
    # Summary
    print()
    print("-" * 60)
    print(f"Captured {len(elements)} elements")
    
    # Count by type
    type_counts = {}
    for el in elements:
        ct = el.get("control_type", "Unknown")
        type_counts[ct] = type_counts.get(ct, 0) + 1
    
    print()
    print("Control types found:")
    for ct, count in sorted(type_counts.items(), key=lambda x: -x[1]):
        print(f"  {ct}: {count}")
    
    # Save to file if requested
    if args.output:
        output_data = {
            "captured_at": datetime.now().isoformat(),
            "window_title": main_window.window_text(),
            "element_count": len(elements),
            "max_depth": args.depth,
            "type_counts": type_counts,
            "elements": elements
        }
        
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        
        print()
        print(f"Saved to: {args.output}")
    
    print()
    print("Done!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
