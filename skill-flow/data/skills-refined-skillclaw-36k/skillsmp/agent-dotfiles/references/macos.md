# macOS

## Setup

- Create the dotfiles root (default: `~/dotfiles`).
- Create `mappings.txt` in the dotfiles root. Use `mappings.example.txt` as a template.
- Make the script executable and run it.

## Example

```bash
chmod +x scripts/link_dotfiles.sh
./scripts/link_dotfiles.sh --root "$HOME/dotfiles" --map "$HOME/dotfiles/mappings.txt"
```
