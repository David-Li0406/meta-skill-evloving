import os
import re

def migrate_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Regex for .withOpacity(value) -> .withValues(alpha: value)
    # Handles simple cases. Nested parentheses in value might need simpler approach if complex.
    # Assuming value is typically a number or scalar variable.
    new_content = re.sub(r'\.withOpacity\(([^)]+)\)', r'.withValues(alpha: \1)', content)
    
    if content != new_content:
        with open(filepath, 'w') as f:
            f.write(new_content)
        print(f"Migrated: {filepath}")

def main():
    root_dir = 'lib'
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.dart'):
                migrate_file(os.path.join(root, file))

if __name__ == '__main__':
    main()
