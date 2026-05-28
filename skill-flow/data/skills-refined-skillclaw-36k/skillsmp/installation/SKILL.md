---
name: installation
description: Step-by-step installation guide for Nix and dotfiles setup including nix.conf configuration, channel updates, home-manager, and nix-darwin
---

# Installation

- [1. Manually craete a directory that matches the ghq root.](#1-manually-craete-a-directory-that-matches-the-ghq-root)
- [2. Set up nix.conf](#2-set-up-nixconf)
- [3. Install nix](#3-install-nix)
- [4. Update nix channel](#4-update-nix-channel)
- [5. Apply nix config](#5-apply-nix-config)
- [6. Launch zsh](#6-launch-zsh)
- [7. Apply darwin config](#7-apply-darwin-config)

## 1. Craete a directory that matches the ghq root.

```sh
cd ~
mkdir -p git_repos/github.com/barleytea
cd git_repos/github.com/barleytea
git clone https://github.com/barleytea/dotfiles.git
```

## 2. Set up local nix.conf

```sh
mkdir -p "$HOME/.config/nix"
echo 'experimental-features = nix-command flakes' > "$HOME/.config/nix/nix.conf"
echo 'use-xdg-base-directories = true' >> "$HOME/.config/nix/nix.conf"
echo 'warn-dirty = false' >> "$HOME/.config/nix/nix.conf"
```

## 3. Install nix

```sh
curl --proto '=https' --tlsv1.2 -sSf -L https://install.determinate.systems/nix | sh -s -- install --no-confirm
source /nix/var/nix/profiles/default/etc/profile.d/nix-daemon.sh
```

## 4. Set up global nix.conf

1. edit /etc/nix/nix.conf

```sh
sudo vi /etc/nix/nix.conf
```

1. add the following to the file

```sh
extra-trusted-users = miyoshi_s
use-xdg-base-directories = true
```

1. restart nix-daemon

```sh
sudo launchctl unload /Library/LaunchDaemons/org.nixos.nix-daemon.plist
sudo launchctl load /Library/LaunchDaemons/org.nixos.nix-daemon.plist
```

## 5. Update nix channel

```sh
nix-channel --add https://nixos.org/channels/nixpkgs-unstable
nix-channel --update
```

## 6. Apply nix config

```sh
nix flake update
nix run nixpkgs#home-manager -- switch --flake .#home --impure
```

## 7. Launch zsh

```sh
zsh
```

## 8. Apply darwin config

```sh
make nix-darwin-apply
```
