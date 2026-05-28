# Test Scenarios for setting-up-devcontainers

## Contents

- [Generate devcontainer for simple marketplace](#scenario-generate-devcontainer-for-simple-marketplace) (Easy)
- [Handle marketplace with multiple plugins](#scenario-handle-marketplace-with-multiple-plugins) (Medium)
- [Handle missing marketplace.json](#scenario-handle-missing-marketplacejson) (Edge-case)
- [Handle existing .devcontainer directory](#scenario-handle-existing-devcontainer-directory) (Edge-case)
- [Marketplace with nested plugin directories](#scenario-marketplace-with-nested-plugin-directories) (Hard)
- [Explain devcontainer architecture](#scenario-explain-devcontainer-architecture) (Easy)
- [Generate devcontainer with Codex CLI support](#scenario-generate-devcontainer-with-codex-cli-support) (Medium)

---

## Scenario: Generate devcontainer for simple marketplace

**Difficulty:** Easy

**Query:** Set up a devcontainer for my marketplace at this project root.

**Test files:**
- `.claude-plugin/marketplace.json` with 1 plugin

**Expected behaviors:**

1. Reads marketplace.json correctly
   - **Minimum:** Reads the file without errors
   - **Quality criteria:**
     - Parses JSON and extracts marketplace name
     - Extracts plugins array with source paths
     - Handles optional fields gracefully
   - **Haiku pitfall:** Fails to parse nested structure, reports file not found incorrectly
   - **Weight:** 4

2. Discovers plugins and skills
   - **Minimum:** Lists at least one plugin
   - **Quality criteria:**
     - Follows source path to plugin directory
     - Reads plugin.json or checks skills/ directory
     - Builds complete list of skill names
     - Handles skills without plugin.json
   - **Haiku pitfall:** Only reads marketplace.json, misses individual skills
   - **Weight:** 5

3. Generates valid devcontainer.json
   - **Minimum:** Creates syntactically valid JSON
   - **Quality criteria:**
     - Uses named volumes for ~/.claude and ~/.local/share/claude (NOT host mount)
     - Includes both postCreateCommand and postStartCommand
     - Volume name includes marketplace name for uniqueness
   - **Haiku pitfall:** Uses host mount for ~/.claude, forgets postStartCommand
   - **Weight:** 5

4. Generates functional Dockerfile
   - **Minimum:** Creates file with FROM ubuntu:latest
   - **Quality criteria:**
     - Installs curl, git, jq, ca-certificates, sudo, zsh
     - Creates non-root vscode user with zsh as default shell
     - Handles existing UID/GID 1000 in base image (ubuntu user)
     - Sets PATH for ~/.local/bin (always)
     - If Codex enabled: Adds VOLTA_HOME env and extends PATH with $VOLTA_HOME/bin
     - Configures passwordless sudo for vscode user
     - Installs Claude Code at build time
     - If Codex enabled: Installs Volta, Node.js, and Codex CLI via volta install
   - **Haiku pitfall:** Missing sudo/zsh, hardcodes user creation without checking existing UID, uses npm instead of volta for Codex, sets VOLTA_HOME when Codex not enabled
   - **Weight:** 4

5. Generates post-create.sh with correct structure
   - **Minimum:** Creates executable shell script
   - **Quality criteria:**
     - Exports PATH with VOLTA_HOME/bin and $HOME/.local/bin
     - Fixes volume ownership with sudo chown before accessing (including ~/.codex if enabled)
     - Assumes Claude Code is already available in PATH from the base image (does not attempt to install it)
     - Generates settings.json with enabledPlugins as OBJECT (not array)
     - Includes all discovered skills in permissions.allow
     - Registers marketplace and installs plugins
     - If Codex enabled: Syncs skills to ~/.codex/skills/ via sync-codex-skills.sh
   - **Haiku pitfall:** Uses array format for enabledPlugins, missing PATH export, missing sudo chown for volume, forgets Codex skill sync
   - **Weight:** 5

6. Generates reinstall-marketplace.sh
   - **Minimum:** Creates script that can be executed
   - **Quality criteria:**
     - Exports PATH with VOLTA_HOME/bin and $HOME/.local/bin
     - Handles --quiet flag
     - Uses $HOME/.claude for config directory
     - Properly quotes paths and handles edge cases
     - If Codex enabled: Also syncs skills to Codex after marketplace reinstall
   - **Haiku pitfall:** Hardcodes paths, missing PATH export, missing error handling, forgets Codex sync
   - **Weight:** 3

7. Generates sync-codex-skills.sh (if Codex enabled)
   - **Minimum:** Creates executable script
   - **Quality criteria:**
     - Copies skills from plugins/*/skills/*/ to ~/.codex/skills/
     - Uses rm -rf and cp -r to ensure fresh copy (Codex ignores symlinks)
     - Handles --quiet flag
     - Reports count of synced skills
   - **Haiku pitfall:** Uses symlinks (Codex ignores them), wrong skill path discovery
   - **Weight:** 3

**Output validation:**
- Directory: `.devcontainer/` exists
- Files: `devcontainer.json`, `Dockerfile`, `post-create.sh`, `reinstall-marketplace.sh`
- Files (if Codex enabled): `sync-codex-skills.sh`
- Pattern in devcontainer.json: `"type": "volume"` (not bind mount)
- Pattern in devcontainer.json (if Codex): `codex-config-` volume mount
- Pattern in Dockerfile: `zsh` in apt-get install list
- Pattern in Dockerfile: `-s /bin/zsh` in useradd/usermod command
- Pattern in Dockerfile: `getent group` and `getent passwd` for UID/GID handling
- Pattern in Dockerfile: `sudoers.d` for passwordless sudo
- Pattern in Dockerfile: `PATH="/home/vscode/.local/bin:$PATH"` (always present)
- Pattern in Dockerfile (if Codex): `VOLTA_HOME` and extended `PATH` with `$VOLTA_HOME/bin`
- Pattern in Dockerfile (if Codex): `volta install node` and `volta install @openai/codex`
- Pattern in post-create.sh: `export VOLTA_HOME` and `export PATH` with both paths
- Pattern in post-create.sh: `sudo chown` for volume ownership (including ~/.codex)
- Pattern in post-create.sh: `"enabledPlugins": {` (object, not array)
- Pattern in post-create.sh (if Codex): `sync-codex-skills.sh` call
- Pattern in reinstall-marketplace.sh: `export VOLTA_HOME` and `export PATH`
- Pattern in reinstall-marketplace.sh (if Codex): `sync-codex-skills.sh` call
- Pattern in sync-codex-skills.sh (if Codex): `cp -r` (NOT symlink)

---

## Scenario: Handle marketplace with multiple plugins

**Difficulty:** Medium

**Query:** Create devcontainer for a marketplace with skills-helper, marketplace-helper, and skills-helper-experimental plugins.

**Test files:**
- `.claude-plugin/marketplace.json` with 3 plugins
- Each plugin has 2-4 skills

**Expected behaviors:**

1. Enumerates skills from ALL plugins
   - **Minimum:** Lists skills from at least 2 plugins
   - **Quality criteria:**
     - Reads each plugin's source directory
     - Discovers skills from each plugin's skills/ directory
     - Handles different plugin structures (skills array vs directory)
     - No duplicate skills in final list
   - **Haiku pitfall:** Only processes first plugin, misses skills from later plugins
   - **Weight:** 5

2. Generates correct enabledPlugins for all plugins
   - **Minimum:** Includes at least 2 plugins
   - **Quality criteria:**
     - Uses format: `"plugin-name@marketplace-name": true`
     - All 3 plugins included
     - Object format, NOT array
   - **Haiku pitfall:** Array format, missing plugins, wrong marketplace suffix
   - **Weight:** 5

3. Generates permissions for all skills
   - **Minimum:** Includes skills from at least 2 plugins
   - **Quality criteria:**
     - Uses format: `"Skill(skill-name)"`
     - All skills from all plugins included
     - No duplicates
     - Properly formatted JSON array
   - **Haiku pitfall:** Missing skills from some plugins, syntax errors
   - **Weight:** 4

4. Generates plugin install commands
   - **Minimum:** At least 1 install command
   - **Quality criteria:**
     - One command per plugin
     - Uses correct format: `claude plugin install plugin@marketplace --scope user`
     - Commands in logical order
   - **Haiku pitfall:** Wrong install command syntax, missing --scope
   - **Weight:** 3

**Output validation:**
- enabledPlugins has exactly 3 entries
- permissions.allow has all skills from all plugins

---

## Scenario: Handle missing marketplace.json

**Difficulty:** Edge-case

**Query:** Set up devcontainer at /path/that/does/not/exist

**Expected behaviors:**

1. Reports error clearly
   - **Minimum:** Says file or path not found
   - **Quality criteria:**
     - Attempts to read .claude-plugin/marketplace.json
     - Reports specific path that was checked
     - Does NOT generate partial/broken devcontainer files
     - Clear error message for user
   - **Haiku pitfall:** Generates empty config anyway, unclear error
   - **Weight:** 5

2. Offers recovery options
   - **Minimum:** Asks for correct path
   - **Quality criteria:**
     - Suggests checking current directory
     - Offers to search for marketplace.json
     - Explains what marketplace.json should contain
   - **Haiku pitfall:** Just errors and stops without guidance
   - **Weight:** 3

**Output validation:**
- No .devcontainer/ directory created
- Error message includes "marketplace.json"

---

## Scenario: Handle existing .devcontainer directory

**Difficulty:** Edge-case

**Query:** Generate devcontainer for my marketplace (already has .devcontainer/)

**Expected behaviors:**

1. Detects existing files
   - **Minimum:** Notices files exist
   - **Quality criteria:**
     - Checks for existing .devcontainer/ directory
     - Lists which files would be overwritten
     - Does NOT silently overwrite
   - **Haiku pitfall:** Overwrites without warning
   - **Weight:** 4

2. Asks before overwriting
   - **Minimum:** Asks user
   - **Quality criteria:**
     - Offers backup option
     - Shows diff or summary of changes
     - Respects user's choice
   - **Haiku pitfall:** Proceeds without confirmation
   - **Weight:** 4

**Output validation:**
- User prompted before any writes if files exist

---

## Scenario: Marketplace with nested plugin directories

**Difficulty:** Hard

**Query:** Generate devcontainer for marketplace with plugins at ./plugins/category/plugin-name structure

**Expected behaviors:**

1. Correctly resolves relative paths
   - **Minimum:** Finds at least one plugin
   - **Quality criteria:**
     - Handles source paths like `"./plugins/helpers/skill-helper"`
     - Resolves paths relative to marketplace root
     - Validates each path exists before proceeding
   - **Haiku pitfall:** Path resolution errors, wrong base directory
   - **Weight:** 5

2. Handles deep plugin.json discovery
   - **Minimum:** Finds at least one plugin.json
   - **Quality criteria:**
     - Checks .claude-plugin/plugin.json in each source directory
     - Falls back to skills/ directory if plugin.json missing
     - Parses skills path correctly from plugin.json
   - **Haiku pitfall:** Doesn't check nested .claude-plugin/ directories
   - **Weight:** 4

3. Generates correct workspace paths
   - **Minimum:** Creates functional scripts
   - **Quality criteria:**
     - Paths in post-create.sh resolve correctly
     - Paths in reinstall-marketplace.sh work from /workspaces
     - No hardcoded absolute host paths
   - **Haiku pitfall:** Mixes host and container paths
   - **Weight:** 4

**Output validation:**
- All paths in generated files start with /workspaces or use $WORKSPACE variable

---

## Scenario: Explain devcontainer architecture

**Difficulty:** Easy

**Query:** How does the devcontainer setup work for Claude Code?

**Expected behaviors:**

1. Explains named volume strategy
   - **Minimum:** Mentions named volumes for persistence
   - **Quality criteria:**
     - Explains using named volumes for ~/.claude and ~/.local/share/claude
     - If Codex enabled: Also explains ~/.codex volume for Codex persistence
     - Describes what's stored (credentials, settings, plugins config, Codex skills)
     - Notes Claude binary is installed to ~/.local/bin (not in volume)
     - Explains volume persistence benefits across container rebuilds
   - **Haiku pitfall:** Vague explanation, confuses binary location with config, doesn't mention volume persistence
   - **Weight:** 4

2. Explains startup sequence
   - **Minimum:** Lists key steps
   - **Quality criteria:**
     - Describes postCreateCommand vs postStartCommand difference
     - Explains when Claude Code is installed
     - Explains when marketplace is synced
     - If Codex enabled: Explains skill sync to ~/.codex/skills/
   - **Haiku pitfall:** Conflates the two commands, incomplete sequence
   - **Weight:** 3

3. Explains credential persistence
   - **Minimum:** Mentions credentials persist
   - **Quality criteria:**
     - Named volume vs bind mount comparison
     - Explains why credentials survive container rebuild
     - Notes user needs to login once (both Claude and Codex if enabled)
   - **Haiku pitfall:** Doesn't explain why named volume chosen
   - **Weight:** 3

4. Explains Codex skill sync (if Codex enabled)
   - **Minimum:** Mentions skills are synced
   - **Quality criteria:**
     - Explains why copy instead of symlink (Codex ignores symlinks)
     - Describes sync-codex-skills.sh purpose
     - Notes skills need re-sync after editing
   - **Haiku pitfall:** Suggests symlinks, forgets sync step
   - **Weight:** 3

**Output validation:**
- Response mentions: named volume, ~/.claude, postCreateCommand, postStartCommand
- If Codex: mentions ~/.codex, skill sync, copy (not symlink)

---

## Scenario: Generate devcontainer with Codex CLI support

**Difficulty:** Medium

**Query:** Set up a devcontainer for my marketplace with Codex CLI support enabled.

**Test files:**
- `.claude-plugin/marketplace.json` with 1-2 plugins

**Expected behaviors:**

1. Asks about Codex CLI support
   - **Minimum:** Mentions Codex as an option
   - **Quality criteria:**
     - Explicitly asks user if they want Codex CLI support
     - Explains what Codex adds (Volta, Node.js, Codex CLI, skill sync)
     - Clarifies this is optional
   - **Haiku pitfall:** Assumes Codex without asking, or forgets to ask
   - **Weight:** 3

2. Generates Dockerfile with Volta and Codex
   - **Minimum:** Includes Volta installation
   - **Quality criteria:**
     - Sets VOLTA_HOME and PATH environment variables
     - Uses `volta install node` (not npm/nvm)
     - Uses `volta install @openai/codex` (not npm i -g)
     - Installs after USER switch (as vscode user, not root)
   - **Haiku pitfall:** Uses npm instead of volta, installs as root, missing VOLTA_HOME
   - **Weight:** 5

3. Generates devcontainer.json with Codex volume
   - **Minimum:** Includes codex-config volume
   - **Quality criteria:**
     - Adds third volume for ~/.codex
     - Volume name includes marketplace name for uniqueness
     - Format matches existing claude volumes
   - **Haiku pitfall:** Forgets Codex volume, wrong mount path
   - **Weight:** 4

4. Generates sync-codex-skills.sh
   - **Minimum:** Creates the script
   - **Quality criteria:**
     - Uses cp -r (NOT symlinks - Codex ignores them)
     - Discovers skills from plugins/*/skills/*/
     - Checks for SKILL.md in each directory
     - Removes existing target before copy (rm -rf)
     - Handles --quiet flag
   - **Haiku pitfall:** Uses symlinks, wrong skill discovery path
   - **Weight:** 5

5. Updates post-create.sh for Codex
   - **Minimum:** Includes Codex section
   - **Quality criteria:**
     - Adds ~/.codex to chown loop
     - Calls sync-codex-skills.sh
     - Adds codex-f alias
     - Updates completion message to mention Codex
   - **Haiku pitfall:** Missing chown for ~/.codex, forgets skill sync call
   - **Weight:** 4

6. Updates reinstall-marketplace.sh for Codex
   - **Minimum:** Includes Codex sync
   - **Quality criteria:**
     - Checks if codex command exists before sync
     - Calls sync-codex-skills.sh with --quiet flag passthrough
   - **Haiku pitfall:** Syncs without checking codex exists
   - **Weight:** 3

**Output validation:**
- Pattern in Dockerfile: `ENV VOLTA_HOME="/home/vscode/.volta"`
- Pattern in Dockerfile: `PATH="$VOLTA_HOME/bin` (VOLTA_HOME in PATH)
- Pattern in Dockerfile: `volta install node`
- Pattern in Dockerfile: `volta install @openai/codex`
- Pattern in devcontainer.json: `codex-config-`
- File exists: `sync-codex-skills.sh`
- Pattern in sync-codex-skills.sh: `cp -r` (NOT `ln -s`)
- Pattern in post-create.sh: `sync-codex-skills.sh`
- Pattern in post-create.sh: `codex-f`
- Pattern in reinstall-marketplace.sh: `command -v codex`
