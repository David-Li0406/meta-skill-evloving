# Windows

## Setup

- Create the dotfiles root (default: `C:\Users\<user>\dotfiles`).
- Create `mappings.txt` in the dotfiles root. Use `mappings.example.txt` as a template.
- Run the PowerShell script.

## Example

```powershell
powershell -ExecutionPolicy Bypass -File scripts\link_dotfiles.ps1 `
  -DotfilesRoot "$env:USERPROFILE\dotfiles" `
  -MappingFile "$env:USERPROFILE\dotfiles\mappings.txt"
```

## Notes

- Symbolic links may require Administrator privileges.
- The script falls back to hardlinks for files and junctions for directories.
- Hardlinks require source and destination to be on the same drive.
