#!/usr/bin/env python3
"""Fix remaining type issue in _buildSupplementCard"""

import re

file_path = "/Users/lycanbeats/Desktop/adhd_supplement_app/lib/presentation/views/library_screen.dart"

with open(file_path, 'r') as f:
    content = f.read()

# Fix _buildSupplementCard parameter type
content = re.sub(
    r'Widget _buildSupplementCard\(\s+BuildContext context, \{\s+required supplement,',
    '''Widget _buildSupplementCard(
    BuildContext context, {
    required Supplement supplement,''',
    content
)
print("✓ Fixed _buildSupplementCard signature")

# Save
with open(file_path, 'w') as f:
    f.write(content)

print("\n✅ All type fixes applied!")
