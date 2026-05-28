# Submodule Detach Procedure

If `src/` is a submodule, detach it while keeping the working tree so it can be archived.

```bash
# Remove the submodule entry from .git/config
git submodule deinit -f src

# Remove the gitlink from the index but keep the working tree
git rm -f --cached src

# Remove the src entry from .gitmodules
git config -f .gitmodules --remove-section submodule.src || true
git add .gitmodules

# Detach the submodule working tree so it becomes a normal folder
rm -f src/.git

# Remove the submodule's git metadata after detaching
rm -rf .git/modules/src
```

Verify `git status -s` shows `src/` as untracked before moving it.
