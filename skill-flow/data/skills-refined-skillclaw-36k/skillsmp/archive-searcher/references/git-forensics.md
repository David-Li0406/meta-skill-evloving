# Git Forensics Deep Dive
> **Detailed technical reference for advanced historical analysis.**

## 1. Advanced Pickaxe (-S) vs. G-regex (-G)
While the main `SKILL.md` covers the basics, forensics often requires nuanced choice between these two.

### When to use -S:
- **String Tracking**: You are looking for a literal string that is not a common word.
- **Count Invariants**: You want to see when the *number* of times a variable is used changed.
- **Performance**: Generally faster than -G because it uses a pre-indexed search for strings.

### When to use -G:
- **Pattern Matching**: You are looking for a shape (e.g., an email address or an IP range).
- **Structural Changes**: You want to see any commit that *touched* lines matching the pattern, even if the count didn't change (e.g., changing `const x = 1` to `let x = 1`).

## 2. Internal Object Analysis with `cat-file`
Git is a content-addressable filesystem. Every object is identified by its SHA-1 hash.

### Object Types:
- **blob**: File content.
- **tree**: A directory listing (maps names to blob/tree hashes).
- **commit**: Links a tree to a parent commit and adds metadata (author, message).
- **tag**: An anchor to a specific commit.

### Forensic Command:
```bash
# Extract the content of a file from a hash without checking it out
git cat-file -p <hash> > recovered_file.ts
```

## 3. The `bisect` Automation
If you can write a script that exits with `0` for good and `1-127` for bad, you can automate the search.

```bash
git bisect run ./test_script.sh
```

## 4. Recovering from "Dangling Blobs"
If you added files to the index but never committed them, and then ran `git reset --hard`, they might be "dangling."

```bash
# Find all unreachable objects
git fsck --full --unreachable --dangling

# Inspect each dangling blob
git cat-file -p <blob_hash>
```

---
*Updated: January 22, 2026 - 15:18*