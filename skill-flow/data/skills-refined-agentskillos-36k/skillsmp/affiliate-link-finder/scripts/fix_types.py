#!/usr/bin/env python3
"""Fix type issues in library_screen.dart"""

import re

file_path = "/Users/lycanbeats/Desktop/adhd_supplement_app/lib/presentation/views/library_screen.dart"

with open(file_path, 'r') as f:
    content = f.read()

# Add Supplement import at the top
if "import '../../domain/entities/supplement.dart';" not in content:
    # Find the last import line
    imports_end = content.rfind("import ")
    line_end = content.find("\n", imports_end)
    content = content[:line_end+1] + "import '../../domain/entities/supplement.dart';\n" + content[line_end+1:]
    print("✓ Added Supplement import")

# Fix method signatures
content = re.sub(
    r'void _showAddToStackSheet\(BuildContext context, supplement\)',
    'void _showAddToStackSheet(BuildContext context, Supplement supplement)',
    content
)
print("✓ Fixed _showAddToStackSheet signature")

# Save
with open(file_path, 'w') as f:
    f.write(content)

print("✅ Type fixes applied to library_screen.dart")
