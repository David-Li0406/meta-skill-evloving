---
name: zoxide-guide
description: Zoxide smart directory navigation configured via home-manager including usage examples and troubleshooting
---

# zoxide

[zoxide](https://github.com/ajeetdsouza/zoxide) is a smarter `cd` command that learns your most-used directories.

This repository enables zoxide for zsh via home-manager and loads it from the zsh tool config.

## Configuration Location

- zsh init: `home-manager/shell/zsh/config/zoxide.zsh`
- tool config symlink: `home-manager/shell/zsh/default.nix` (installs to `~/.config/zsh/config/tools/206-zoxide.zsh`)
- package install: `home-manager/default.nix` (`home.packages` includes `zoxide`)

## Usage

Basic - jump to a directory:

```sh
z <query>
```

Examples:

```sh
z dotfiles
z git
z src
```

List matches:

```sh
zoxide query <query>
```

Interactive selection (optional, requires `fzf`):

```sh
zoxide query -i
```

## Troubleshooting

### `z` command not found

1. Apply home-manager:

```sh
make home-manager-apply
```

2. Restart the shell:

```sh
exec zsh
```

3. Confirm zoxide is available:

```sh
command -v zoxide
zoxide --version
```

## Related Documentation

- [Installation](docs/10_installation.md)
- [Nix operations](docs/20_nix.md)
- [Atuin shell history](docs/52_atuin.md)
