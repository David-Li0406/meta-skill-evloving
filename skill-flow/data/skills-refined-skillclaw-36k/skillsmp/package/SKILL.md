---
name: package
description: Guide for increasing the version and packaging a VSIX extension, used when creating a new package release
---
# Plus One Publish

Increment the extension version and create a VSIX package.

## Steps

1. Read the current version from `package.json`
2. Increment the patch version by 0.0.1 (e.g., 0.1.4 → 0.1.5)
3. Update `package.json` with the new version
4. Create the `.vsix` folder if it doesn't exist
5. Run `vsce package` to create the VSIX file in the `.vsix` folder

## Commands

```powershell
# Ensure .vsix folder exists
New-Item -ItemType Directory -Force -Path ".vsix"

# Package the extension into .vsix folder
vsce package -o .vsix/
```

## Notes

- Requires `@vscode/vsce` to be installed (`npm install -g @vscode/vsce`)
- The VSIX file will be named `markco-<version>.vsix`
- Commit the version bump before publishing
