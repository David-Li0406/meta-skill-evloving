import argparse
import os
import sys

def create_note(vault_path, note_name, content, overwrite=False):
    # Ensure .md extension
    if not note_name.endswith('.md'):
        note_name += '.md'
    
    full_path = os.path.join(vault_path, note_name)
    
    # Check if file exists
    if os.path.exists(full_path) and not overwrite:
        print(f"Error: Note '{note_name}' already exists. Use --overwrite to force.")
        sys.exit(1)
        
    # Ensure directory exists
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    
    try:
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Successfully created note: {full_path}")
    except Exception as e:
        print(f"Error creating note: {e}")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a new note in Obsidian vault")
    parser.add_argument("--vault", required=True, help="Path to the Obsidian vault root")
    parser.add_argument("--name", required=True, help="Name of the note (relative path)")
    parser.add_argument("--content", required=True, help="Content of the note")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite if exists")
    
    args = parser.parse_args()
    create_note(args.vault, args.name, args.content, args.overwrite)
