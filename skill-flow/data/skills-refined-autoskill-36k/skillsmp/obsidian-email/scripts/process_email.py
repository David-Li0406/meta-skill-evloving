#!/usr/bin/env python3
"""
Process Obsidian email chain notes.

Usage:
    python process_email.py <email_note_file.md>

This script:
1. Extracts unique participants from email From headers
2. Creates missing People profiles with email addresses
3. Updates Participants section with linked names
4. Generates summary from email chain content
5. Updates Summary section in the note
"""

import re
import sys
from pathlib import Path
from typing import List, Dict, Tuple, Optional


def extract_participants(email_chain: str) -> List[Tuple[str, str]]:
    """
    Extract unique senders from email chain.
    
    Returns list of (name, email) tuples in order of first appearance.
    Name format: "Last, First" or "Last, First Middle"
    """
    participants = []
    seen_emails = set()
    seen_names = set()
    
    # Pattern to match From headers (both plain and bold)
    # Matches: "From: Last, First <email@domain.com>"
    # Or: "**From:** Last, First <email@domain.com>"
    from_pattern = r'\*?\*?From:\*?\*?\s+([^<\n]+?)\s*<([^>]+)>'
    
    for match in re.finditer(from_pattern, email_chain):
        name_raw = match.group(1).strip()
        email_raw = match.group(2).strip()
        
        # Clean email - handle markdown links [email](mailto:email)
        # Extract just the email address
        email_match = re.search(r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})', email_raw)
        if not email_match:
            continue
        email = email_match.group(1)
        
        # Skip if we've seen this email before
        if email in seen_emails:
            continue
        
        # Clean name - remove role descriptions in parentheses
        # e.g., "McKee, Heidi L (GreenLake Manager)" -> "McKee, Heidi L"
        name = re.sub(r'\s*\([^)]+\)\s*', '', name_raw).strip()
        
        # Validate name format (should contain comma for "Last, First")
        if ',' not in name:
            continue
        
        # Skip if we've seen this name before (avoid duplicates)
        if name in seen_names:
            continue
        
        seen_emails.add(email)
        seen_names.add(name)
        participants.append((name, email))
    
    return participants


def format_name_for_link(name: str) -> Tuple[str, str]:
    """
    Convert "Last, First" to ("Last, First", "First Last").
    Handles middle names: "Last, First Middle" -> "First Middle Last"
    """
    if ',' not in name:
        return name, name
    
    parts = [p.strip() for p in name.split(',', 1)]
    last_name = parts[0]
    first_parts = parts[1] if len(parts) > 1 else ""
    
    # Display format: "First Middle Last"
    display_name = f"{first_parts} {last_name}".strip()
    
    return name, display_name


def check_profile_exists(name: str, people_dir: Path) -> Optional[Path]:
    """Check if a People profile exists for the given name."""
    profile_path = people_dir / f"{name}.md"
    return profile_path if profile_path.exists() else None


def create_people_profile(name: str, email: str, people_dir: Path) -> bool:
    """Create a new People profile with email address."""
    profile_path = people_dir / f"{name}.md"
    
    _, display_name = format_name_for_link(name)
    
    content = f"""---
tags:
  - person
---

# {name}

## Contact
- Email: {email}

## Aliases
- [[{name}|{display_name}]]
"""
    
    try:
        with open(profile_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"ERROR: Failed to create profile for {name}: {e}")
        return False


def add_email_to_profile(profile_path: Path, email: str) -> bool:
    """Add email to existing profile if not already present."""
    try:
        with open(profile_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if email already exists
        if email in content:
            return False
        
        # Check if Contact section exists
        if '## Contact' in content:
            # Add email to existing Contact section
            content = re.sub(
                r'(## Contact\n)',
                f'\\1- Email: {email}\n',
                content,
                count=1
            )
        else:
            # Add Contact section after the heading
            name_match = re.search(r'^# (.+)$', content, re.MULTILINE)
            if name_match:
                insert_pos = content.find('\n', name_match.end())
                content = (content[:insert_pos + 1] + 
                          f'\n## Contact\n- Email: {email}\n' +
                          content[insert_pos + 1:])
        
        with open(profile_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"ERROR: Failed to add email to profile: {e}")
        return False


def update_participants_section(content: str, participants: List[Tuple[str, str]]) -> str:
    """Update the Participants section with linked names."""
    # Build participant list
    participant_lines = []
    for name, _ in participants:
        full_name, display_name = format_name_for_link(name)
        participant_lines.append(f"- [[{full_name}|{display_name}]]")
    
    participant_text = '\n'.join(participant_lines)
    
    # Replace Participants section
    pattern = r'(# Participants\n)\s*(\n# )'
    replacement = f'\\1\n{participant_text}\n\\2'
    
    new_content = re.sub(pattern, replacement, content)
    
    return new_content


def generate_summary(email_chain: str, participants: List[Tuple[str, str]]) -> str:
    """
    Generate a summary of the email chain.
    This is a placeholder - in practice, you might use AI or more sophisticated analysis.
    """
    # Extract subject line
    subject_match = re.search(r'Subject:\s*(.+?)(?:\n|$)', email_chain, re.IGNORECASE)
    subject = subject_match.group(1).strip() if subject_match else "Email Discussion"
    
    # Count emails
    num_emails = len(participants)
    
    # Extract mentioned issues/tickets
    tickets = re.findall(r'GLCP-\d+|\[\[GLCP-\d+\]\]', email_chain)
    unique_tickets = list(set(tickets))
    
    # Build summary
    summary = f"""## Overview
Email thread regarding: {subject}

Thread contains {num_emails} messages from {len(participants)} participants.

## Key Points
- Discussion involves multiple stakeholders across teams
"""
    
    if unique_tickets:
        summary += f"- References tickets: {', '.join(unique_tickets)}\n"
    
    summary += """
## Action Items
- Review email chain for specific action items and deadlines
- Follow up on open issues discussed

## Context
See full email chain below for complete discussion details.
"""
    
    return summary


def update_summary_section(content: str, summary: str) -> str:
    """Update the Summary section with generated content."""
    pattern = r'(# Summary\n)\s*(\n# )'
    replacement = f'\\1\n{summary}\n\\2'
    
    new_content = re.sub(pattern, replacement, content)
    
    return new_content


def extract_email_chain(content: str) -> Optional[str]:
    """Extract the Email Chain section content."""
    match = re.search(r'# Email Chain\n(.+)', content, re.DOTALL)
    return match.group(1) if match else None


def main():
    if len(sys.argv) != 2:
        print("Usage: process_email.py <email-note-file.md>")
        sys.exit(1)
    
    filepath = Path(sys.argv[1])
    
    if not filepath.exists():
        print(f"ERROR: File not found: {filepath}")
        sys.exit(1)
    
    # Determine People directory
    # Assuming structure: .../Obsidian/HPE/Notes/file.md -> .../Obsidian/HPE/People/
    people_dir = filepath.parent.parent / "People"
    
    if not people_dir.exists():
        print(f"ERROR: People directory not found: {people_dir}")
        sys.exit(1)
    
    # Read the note file
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract email chain
    email_chain = extract_email_chain(content)
    if not email_chain:
        print("ERROR: No email chain section found")
        sys.exit(1)
    
    # Extract participants
    participants = extract_participants(email_chain)
    
    if not participants:
        print("ERROR: No participants extracted from email chain")
        print("Ensure emails have 'From: Name <email>' format")
        sys.exit(1)
    
    print(f"✓ Extracted {len(participants)} unique participants")
    for name, email in participants:
        print(f"  - {name} ({email})")
    
    # Process participants - create/update profiles
    new_profiles = 0
    updated_profiles = 0
    
    for name, email in participants:
        profile_path = check_profile_exists(name, people_dir)
        
        if profile_path:
            # Profile exists, check if email needs to be added
            if add_email_to_profile(profile_path, email):
                updated_profiles += 1
        else:
            # Create new profile
            if create_people_profile(name, email, people_dir):
                new_profiles += 1
    
    if new_profiles > 0:
        print(f"✓ Created {new_profiles} new People profiles")
    if updated_profiles > 0:
        print(f"✓ Updated {updated_profiles} profiles with email addresses")
    
    # Update Participants section
    content = update_participants_section(content, participants)
    print("✓ Updated Participants section")
    
    # Generate and update summary
    summary = generate_summary(email_chain, participants)
    content = update_summary_section(content, summary)
    
    # Count summary sections
    summary_sections = len(re.findall(r'^##', summary, re.MULTILINE))
    print(f"✓ Generated summary ({summary_sections} sections)")
    
    # Write updated content
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✓ Updated {filepath.name}")


if __name__ == '__main__':
    main()
