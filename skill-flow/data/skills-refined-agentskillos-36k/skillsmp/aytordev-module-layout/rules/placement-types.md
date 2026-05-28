## Module Placement

**Impact:** HIGH

Place modules in the correct subdirectory based on their type. Incorrect placement confuses the auto-discovery mechanism.

**Incorrect:**

**Random Location**
Putting `docker.nix` in the root of `modules/nixos/` instead of `modules/nixos/services/docker/`.

**Correct:**

**Semantic Paths**

- System service (Linux) -> `modules/nixos/services/docker/`
- System service (macOS) -> `modules/darwin/services/yabai/`
- User application -> `modules/home/programs/terminal/tools/git/`
- Cross-platform shared -> `modules/common/ai-tools/`
