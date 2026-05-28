import sys
import re
import os

def parse_design(file_path):
    if not os.path.exists(file_path):
        print(f"Error: File not found: {file_path}")
        sys.exit(1)

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    lines = content.splitlines()
    output_lines = []
    
    current_section_header = None
    current_file_path = None
    current_content = []

    for line in lines:
        stripped_line = line.strip()
        # Check for #### header
        if stripped_line.startswith('####'):
            # If we were processing a section, save it
            if current_section_header and current_file_path:
                output_lines.append(format_section(current_section_header, current_file_path, current_content))
            
            # Reset for new potential section
            current_section_header = None
            current_file_path = None
            current_content = []
            
            # Check if this header is a file section
            extracted_path = extract_file_path(stripped_line)
            if extracted_path:
                current_section_header = stripped_line
                current_file_path = extracted_path
            else:
                # It's a header, but not a file header. 
                # We ignore it and don't start a new section.
                pass
                
        else:
            # Check if we hit a higher level header (e.g. #, ##, ###) which would end the current section
            if line.startswith('#') and not line.startswith('####'):
                 if current_section_header and current_file_path:
                    output_lines.append(format_section(current_section_header, current_file_path, current_content))
                    current_section_header = None
                    current_file_path = None
                    current_content = []
            
            if current_section_header:
                current_content.append(line)

    # Append the last section
    if current_section_header and current_file_path:
        output_lines.append(format_section(current_section_header, current_file_path, current_content))

    output_content = '\n'.join(output_lines)
    
    output_path = os.path.join(os.path.dirname(file_path), 'detailed-design-by-file.md')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(output_content)
    
    print(f"Created {output_path}")

def extract_file_path(line):
    # 1. Check inside backticks first
    backtick_matches = re.findall(r'`([^`]+)`', line)
    for match in backtick_matches:
        if is_valid_path(match):
            return match

    # 2. Check inside parentheses
    paren_matches = re.findall(r'\(([^)]+)\)', line)
    for match in paren_matches:
        # Remove potential backticks inside parentheses
        clean_match = match.replace('`', '').strip()
        if is_valid_path(clean_match):
            return clean_match
            
    return None

def is_valid_path(text):
    # Must contain '/' (as per instructions <Repo>/path)
    # Must contain '.' (extension) OR be a known filename without extension (LICENSE, Dockerfile, Makefile)
    # Should not contain spaces
    
    if ' ' in text:
        return False
        
    if '/' not in text:
        return False
        
    if '.' in text:
        return True
        
    # Allow specific files without extension
    filename = text.split('/')[-1]
    known_files = {'LICENSE', 'Dockerfile', 'Makefile', 'NOTICE', 'CNAME'}
    if filename in known_files:
        return True
        
    return False

def format_section(header, file_path, content_lines):
    # Remove leading/trailing empty lines from content
    while content_lines and not content_lines[0].strip():
        content_lines.pop(0)
    while content_lines and content_lines and not content_lines[-1].strip():
        content_lines.pop()
        
    content = '\n'.join(content_lines)
    
    # Clean up header
    # header is the full line e.g. "#### 4.4. Title (Path)"
    # We want to clean it up to "#### Title (Path)"
    
    # Strip ####
    clean_header_text = header.strip()[4:].strip()
    
    # Remove numbering at the start
    # e.g. "4.4. Title (Path)" -> "Title (Path)"
    clean_header_text = re.sub(r'^\d+(\.\d+)*\.?\s+', '', clean_header_text)
    
    new_header = f"#### {clean_header_text}"
    
    return f"""
{new_header}

**File Path:**
```
{file_path}
```

**Changes:**
````markdown
{content}
````

---
"""

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python parse_design.py <file_path>")
        sys.exit(1)
    
    parse_design(sys.argv[1])
