## Host Configuration Structure

**Impact:** HIGH

Host configurations live in `systems/{arch}/{hostname}/`. They define the hardware and system-level settings specific to a single machine.

**Incorrect:**

**Host logic in modules**
Checking `networking.hostName == "foo"` inside a generic module. Use the host config file instead.

**Correct:**

**Standard Path**
`systems/x86_64-linux/khanelimain/default.nix` imports specific modules and sets host-specific values.

```nix
{ pkgs, ... }:
{
  imports = [ ./hardware.nix ];
  networking.hostName = "khanelimain";
}
```
