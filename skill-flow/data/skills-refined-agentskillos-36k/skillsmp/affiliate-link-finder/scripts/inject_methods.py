#!/usr/bin/env python3
"""
Script to inject methods into LibraryScreen and DoctorExportScreen files.
This handles the whitespace-sensitive insertions that failed with replace_file_content.
"""

import sys

def inject_library_methods():
    """Inject _showAddToStackSheet and _buildStackOption into library_screen.dart"""
    
    file_path = "/Users/lycanbeats/Desktop/adhd_supplement_app/lib/presentation/views/library_screen.dart"
    
    with open(file_path, 'r') as f:
        lines = f.readlines()
    
    # Find the line with "Widget _buildFilterChip("
    insert_index = None
    for i, line in enumerate(lines):
        if "Widget _buildFilterChip(" in line:
            insert_index = i
            break
    
    if insert_index is None:
        print("Could not find insertion point in library_screen.dart")
        return False
    
    # Read the methods from the helper file
    with open("/Users/lycanbeats/Desktop/adhd_supplement_app/lib/presentation/views/_library_screen_methods.dart", 'r') as f:
        helper_content = f.read()
    
    # Extract just the methods (skip the comment header)
    methods_start = helper_content.find("void _showAddToStackSheet")
    methods_code = helper_content[methods_start:]
    
    # Insert the methods before _buildFilterChip
    lines.insert(insert_index, methods_code + "\n\n  ")
    
    # Write back
    with open(file_path, 'w') as f:
        f.writelines(lines)
    
    print("✓ Injected methods into library_screen.dart")
    return True

def inject_doctor_export_methods():
    """Inject _emailDoctor and _shareReport into doctor_export_screen.dart"""
    
    file_path = "/Users/lycanbeats/Desktop/adhd_supplement_app/lib/presentation/views/doctor_export_screen.dart"
    
    with open(file_path, 'r') as f:
        lines = f.readlines()
    
    # Find the line with "@override" after the member variables
    insert_index = None
    for i, line in enumerate(lines):
        if i > 15 and "@override" in line and "Widget build" in lines[i+1]:
            insert_index = i
            break
    
    if insert_index is None:
        print("Could not find insertion point in doctor_export_screen.dart")
        return False
    
    # Read the methods from the helper file
    with open("/Users/lycanbeats/Desktop/adhd_supplement_app/lib/presentation/views/_doctor_export_methods.dart", 'r') as f:
        helper_content = f.read()
    
    # Extract just the methods (skip the comment header)
    methods_start = helper_content.find("Future<void> _emailDoctor")
    methods_code = helper_content[methods_start:]
    
    # Insert the methods before @override
    lines.insert(insert_index, "\n  " + methods_code + "\n\n  ")
    
    # Write back
    with open(file_path, 'w') as f:
        f.writelines(lines)
    
    print("✓ Injected methods into doctor_export_screen.dart")
    return True

if __name__ == "__main__":
    success = True
    
    if not inject_library_methods():
        success = False
    
    if not inject_doctor_export_methods():
        success = False
    
    if success:
        print("\n✅ All methods injected successfully!")
        sys.exit(0)
    else:
        print("\n❌ Some injections failed")
        sys.exit(1)
