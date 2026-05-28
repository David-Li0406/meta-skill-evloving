import os
import re

def check_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Check for hardcoded hex colors (simplified)
    hex_pattern = r'#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})'
    found_hex = re.findall(hex_pattern, content)
    
    # Exclude styles.py itself from the check or common legitimate hexes
    if "styles.py" not in filepath:
        if found_hex:
            print(f"⚠️ [WARNING] Found hardcoded Hex colors in {filepath}: {found_hex}")
            print("👉 Use Color.NAME instead of hex strings.")

    # Check for accessibility min-height on inputs
    if "rx.input" in content and "min_height" not in content:
         print(f"⚠️ [WARNING] Found rx.input without min_height in {filepath}.")
         print("👉 Every input should have min_height='44px' for accessibility.")

if __name__ == "__main__":
    # Example check on a specific file
    # check_file("path/to/file.py")
    pass
