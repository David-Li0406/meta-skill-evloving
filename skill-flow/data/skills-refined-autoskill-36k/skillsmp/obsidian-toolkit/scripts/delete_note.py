import argparse
import os
import sys

def delete_note(vault_path, note_name):
    # Ensure .md extension
    if not note_name.endswith('.md'):
        note_name += '.md'
    
    full_path = os.path.join(vault_path, note_name)
    
    if not os.path.exists(full_path):
        print(f"Error: Note '{note_name}' not found.")
        sys.exit(1)
        
    try:
        os.remove(full_path)
        print(f"Successfully deleted note: {full_path}")
    except Exception as e:
        print(f"Error deleting note: {e}")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Delete a note from Obsidian vault")
    parser.add_argument("--vault", required=True, help="Path to the Obsidian vault root")
    parser.add_argument("--name", required=True, help="Name of the note (relative path)")
    
    args = parser.parse_args()
    delete_note(args.vault, args.name)
