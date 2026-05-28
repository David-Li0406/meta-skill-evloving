# Troubleshooting

## OneDrive Sync Workaround

If Edit tool fails with "File has been unexpectedly modified" due to OneDrive sync:

```python
import re
file_path = "C:/Users/julien/OneDrive/Documents/PowerShell/Microsoft.PowerShell_profile.ps1"
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Modify content with regex
content = re.sub(r'old_pattern', 'new_content', content, flags=re.DOTALL)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
```

## Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Edit tool fails | OneDrive sync conflict | Use Python workaround above |
| Function not found after `rup` | Wrong section placement | Check section number in profile-structure.md |
| Lazy function not loading | Missing .ps1 file | Verify file exists at `$CLI_ENV_ROOT/profile/functions/` |
| Alias conflicts | Name already exists | Check existing aliases with `Get-Alias` |
| Changes not applied | Profile not reloaded | Run `rup` or open new terminal |

## Testing Changes

```powershell
# Reload profile without restarting terminal
rup

# Or manually
. $PROFILE

# Check if function exists
Get-Command myfunction -ErrorAction SilentlyContinue

# Check loaded lazy functions
$global:LoadedFunctions
```
