import argparse
import os
import sys

def search_notes(vault_path, query, case_sensitive=False):
    matches = []
    
    if not os.path.exists(vault_path):
        print(f"Error: Vault path '{vault_path}' does not exist.")
        sys.exit(1)
        
    for root, dirs, files in os.walk(vault_path):
        # Exclude hidden directories (like .obsidian, .git)
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        
        for file in files:
            if file.endswith('.md'):
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, vault_path)
                
                try:
                    with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                        lines = f.readlines()
                        
                    for i, line in enumerate(lines):
                        content_to_check = line if case_sensitive else line.lower()
                        query_to_check = query if case_sensitive else query.lower()
                        
                        if query_to_check in content_to_check:
                            matches.append({
                                'file': rel_path,
                                'line': i + 1,
                                'content': line.strip()
                            })
                            # To avoid too many matches per file, maybe break? 
                            # But user might want all. I'll just keep them.
                except Exception as e:
                    print(f"Warning: Could not read {rel_path}: {e}", file=sys.stderr)
    
    # Print results
    print(f"Found {len(matches)} matches for '{query}':")
    for match in matches[:50]: # Limit to 50 matches for safety
        print(f"{match['file']}:{match['line']}  {match['content']}")
    
    if len(matches) > 50:
        print(f"... and {len(matches) - 50} more matches.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Search for text in Obsidian vault notes")
    parser.add_argument("--vault", required=True, help="Path to the Obsidian vault root")
    parser.add_argument("--query", required=True, help="Text to search for")
    parser.add_argument("--case-sensitive", action="store_true", help="Enable case-sensitive search")
    
    args = parser.parse_args()
    search_notes(args.vault, args.query, args.case_sensitive)
