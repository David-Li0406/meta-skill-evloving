import argparse
import subprocess
import sys
from pathlib import Path

def get_changed_files(since_ref):
    """Returns a list of changed files since the given ref."""
    try:
        cmd = ["git", "diff", "--name-only", since_ref]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return [f for f in result.stdout.splitlines() if f.strip()]
    except subprocess.CalledProcessError as e:
        print(f"Error running git diff: {e}")
        return []

def scan_docs_for_mentions(doc_dir, changed_files):
    """Scans specific doc files for mentions of the changed filenames."""
    mentions = {}
    doc_files = list(Path(doc_dir).glob("*.md")) + list(Path(".").glob("*.md"))
    
    for doc in doc_files:
        if not doc.exists(): continue
        try:
            content = doc.read_text(encoding="utf-8", errors="ignore")
            found = []
            for cf in changed_files:
                # Simple check: filename in content
                if Path(cf).name in content:
                    found.append(cf)
            if found:
                mentions[str(doc)] = found
        except Exception:
            pass # Ignore read errors
    return mentions

def main():
    parser = argparse.ArgumentParser(description="Analyze documentation impact.")
    parser.add_argument("--since", default="HEAD~1", help="Git ref to digest changes from.")
    args = parser.parse_args()

    print(f"--- Doc Impact Analysis (Since {args.since}) ---")
    
    changed = get_changed_files(args.since)
    if not changed:
        print("No file changes detected.")
        return

    print(f"Changed Files ({len(changed)}):")
    for f in changed:
        print(f"  - {f}")

    print("\nDocumentation References:")
    mentions = scan_docs_for_mentions(".", changed)
    if mentions:
        for doc, files in mentions.items():
            print(f"  📄 {doc} mentions:")
            for f in files:
                print(f"     -> {f}")
    else:
        print("  No direct references found in markdown files.")
        
    print("\n--- Recommendation ---")
    print("Please review the logic changes in the files above and update the documentation if:")
    print("1. Public API signatures have changed.")
    print("2. Configuration parameters were added/removed.")
    print("3. Setup instructions are no longer valid.")

if __name__ == "__main__":
    main()
