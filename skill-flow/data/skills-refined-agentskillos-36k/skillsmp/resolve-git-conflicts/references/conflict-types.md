# Conflict Types

## 1. Overlapping Edits

Both sides modified the same lines differently.

**Markers show:**
```
<<<<<<< HEAD
function calculate(x) {
  return x * 2;
}
=======
function calculate(x) {
  return x * 3;
}
>>>>>>> feature
```

**Resolution options:**
- Pick one version entirely
- Combine logic (e.g., make configurable)
- Rewrite to satisfy both intents

## 2. Edit vs Delete

One side modified a file/function, other side deleted it.

**Git shows:**
```
CONFLICT (modify/delete): file.js deleted in HEAD and modified in feature
```

**Questions to ask user:**
- Should the file/code exist? (keep modified version)
- Was deletion intentional? (accept deletion)
- Was modification essential? (keep and possibly relocate)

**Resolution:**
```bash
# Keep the modified version
git add <file>

# Accept the deletion
git rm <file>
```

## 3. Rename Conflicts

Same file renamed differently on each branch.

**Git shows:**
```
CONFLICT (rename/rename): file.js renamed to new1.js in HEAD and to new2.js in feature
```

**Resolution:**
- Choose one name
- May need to merge content if both also modified

## 4. Add/Add Conflicts

Both branches created a file with the same name but different content.

**Git shows:**
```
CONFLICT (add/add): Merge conflict in newfile.js
```

**Resolution:**
- Merge the contents
- Keep one, rename the other
- Delete one if duplicate

## 5. Binary Conflicts

Non-text files (images, compiled files, etc.) can't be merged.

**Git shows:**
```
CONFLICT (content): Merge conflict in image.png
```

**Resolution - pick one:**
```bash
git checkout --ours image.png
# or
git checkout --theirs image.png
```

## 6. Submodule Conflicts

Submodule pointer changed on both sides.

**Resolution:**
```bash
# Check which commit each side wants
git diff

# Choose one or manually set the desired commit
cd submodule && git checkout <desired-commit>
cd .. && git add submodule
```

## 7. Whitespace/EOL Conflicts

Often caused by different editors or OS line endings.

**Prevention:**
```bash
git config --global core.autocrlf input  # Linux/Mac
git config --global core.autocrlf true   # Windows
```

**Detection:**
```bash
git diff --check
```
