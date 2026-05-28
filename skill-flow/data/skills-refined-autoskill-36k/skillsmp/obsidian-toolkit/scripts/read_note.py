import argparse
import os
import sys

def read_note(vault_path, note_name):
    # Ensure .md extension
    if not note_name.endswith('.md'):
        note_name += '.md'
    
    full_path = os.path.join(vault_path, note_name)
    
    if not os.path.exists(full_path):
        print(f"Error: Note '{note_name}' not found in {vault_path}")
        sys.exit(1)
        
    try:
        with open(full_path, 'r', encoding='utf-8') as f:
            print(f.read())
    except Exception as e:
        print(f"Error reading note: {e}")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Read a note from Obsidian vault")
    parser.add_argument("--vault", required=True, help="Path to the Obsidian vault root")
    parser.add_argument("--name", required=True, help="Name of the note (relative path)")
    
    args = parser.parse_args()
    read_note(args.vault, args.name)
