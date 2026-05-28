## User Configuration Structure

**Impact:** HIGH

User configurations live in `homes/{arch}/{user@host}/`. They define the highest priority personal preferences and user-specific packages.

**Incorrect:**

**Shared Home Manager**
Using a single `home.nix` for all users on all machines.

**Correct:**

**Per-User-Per-Host**
`homes/x86_64-linux/khanelimain@khanelimain/default.nix` allows granular control.

```nix
{ pkgs, ... }:
{
  # Only this user on this machine gets these packages
  home.packages = [ pkgs.spotify ];
}
```
