---
name: readme
description: Makeing of README.md files for ROBOLIBS libraries
license: MIT
compatibility: opencode
metadata:
  audience: coders
---

# README Scaffold Instructions

This document defines the standard structure for README.md files across all ROBOLIBS libraries.

**Note:** These libraries are primarily designed for robotics applications, but this doesn't need to be heavily emphasized in every section.

**IMPORTANT: README.md must be between 350-400 lines of text (empty lines don't count)**

## Standard README Structure

```markdown
<img align="right" width="26%" src="./misc/logo.png">

# [Library Name]

[One-line description - clear, concise value proposition]

## Development Status

See [TODO.md](./TODO.md) for the complete development plan and current progress.

## Overview

[2-3 paragraph description of the library]
- What it does?
- Why it exists?
- Key design principles?

### Architecture Diagrams

**REQUIRED:** After the overview, include ASCII diagrams showing component architecture.

Use one or more ASCII diagrams to illustrate:
- How components connect
- Data flow between modules
- Library structure / layers

**Example ASCII diagram:**
```
┌─────────────────────────────────────────────────────────────┐
│                        YOUR LIBRARY                          │
├──────────────┬──────────────┬──────────────┬────────────────┤
│   Module 1   │   Module 2   │   Module 3   │   Module 4     │
│              │              │              │                │
│  ┌────────┐  │  ┌────────┐  │  ┌────────┐  │  ┌──────────┐  │
│  │ Part A │  │  │ Part B │  │  │ Part C │  │  │  Part D  │  │
│  └────────┘  │  └────────┘  │  └────────┘  │  └──────────┘  │
└──────────────┴──────────────┴──────────────┴────────────────┘
       │               │               │              │
       └───────────────┴───────────────┴──────────────┘
                            │
                    ┌───────▼────────┐
                    │  Your App/Lib  │
                    └────────────────┘
```

Keep diagrams clean, simple, and informative.

## Installation

**NOTE:** Get the actual repository URL using:
```bash
cd your_repo
git remote -v | head -1 | awk '{print $2}' | sed 's/git@github.com:/https:\/\/github.com\//' | sed 's/\.git$//'
```

### Quick Start (CMake FetchContent)

```cmake
include(FetchContent)
FetchContent_Declare(
  [library_name]
  GIT_REPOSITORY [actual_github_url_from_git_remote]
  GIT_TAG main
)
FetchContent_MakeAvailable([library_name])

target_link_libraries(your_target PRIVATE [library_name])
```

### Recommended: XMake

[XMake](https://xmake.io/) is a modern, fast, and cross-platform build system.

**Install XMake:**
```bash
curl -fsSL https://xmake.io/shget.text | bash
```

**Add to your xmake.lua:**
```lua
add_requires("[library_name]")

target("your_target")
    set_kind("binary")
    add_packages("[library_name]")
    add_files("src/*.cpp")
```

**Build:**
```bash
xmake
xmake run
```

### Complete Development Environment (Nix + Direnv + Devbox)

For the ultimate reproducible development environment:

**1. Install Nix (package manager from NixOS):**
```bash
# Determinate Nix Installer (recommended)
curl --proto '=https' --tlsv1.2 -sSf -L https://install.determinate.systems/nix | sh -s -- install
```
[Nix](https://nixos.org/) - Reproducible, declarative package management

**2. Install direnv (automatic environment switching):**
```bash
sudo apt install direnv

# Add to your shell (~/.bashrc or ~/.zshrc):
eval "$(direnv hook bash)"  # or zsh
```
[direnv](https://direnv.net/) - Load environment variables based on directory

**3. Install Devbox (Nix-powered development environments):**
```bash
curl -fsSL https://get.jetpack.io/devbox | bash
```
[Devbox](https://www.jetpack.io/devbox/) - Portable, isolated dev environments

**4. Use the environment:**
```bash
cd [library_name]
direnv allow  # Allow .envrc (one-time)
# Environment automatically loaded! All dependencies available.

xmake        # or cmake, make, etc.
```

## Usage

### Basic Usage

```cpp
// Simple, minimal example showing core functionality
```

### Advanced Usage

```cpp
// More complex example demonstrating advanced features
```

## Features

- **Feature 1** - Description with use case and `inline_code()`
  ```cpp
  // Optional code example
  ```
- **Feature 2** - Description highlighting benefits

**Consider including relevant benefits such as:**
- Performance characteristics
- Memory efficiency
- API design philosophy
- Integration capabilities
- Platform support

## License

MIT License - see [LICENSE](./LICENSE) for details.

## Acknowledgments

Made possible thanks to [these amazing projects](./ACKNOWLEDGMENTS.md).
```

## Required Files

Every library repository must have:

1. **README.md** - Following above structure (350-400 lines of text)
2. **TODO.md** - Development roadmap and status
3. **LICENSE** - MIT license file with "Copyright (c) 2025 ROBOLIBS Contributors"
4. **ACKNOWLEDGMENTS.md** - Credit to dependencies and inspirations
5. **.envrc** (if using direnv) - Environment setup
6. **devbox.json** (if using devbox) - Nix-based dependencies

**LICENSE Template:**
```
MIT License

Copyright (c) 2025 ROBOLIBS Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## Style Guidelines

- **Target length** - Between 350-400 lines of text (empty lines excluded)
- **ASCII diagrams required** - Show component architecture after overview section
- Use clear, concise language
- Link to TODO.md at the top for development status
- Keep installation simple but offer advanced options
- Always credit dependencies and inspirations
- Linux-focused (macOS users can adapt)
- Highlight performance characteristics where relevant
- **Use actual git remote URL** - Convert from SSH to HTTPS format in installation section

## Tool Links

- **XMake**: https://xmake.io/
- **Nix**: https://nixos.org/
- **direnv**: https://direnv.net/
- **Devbox**: https://www.jetpack.io/devbox/
- **CMake**: https://cmake.org/

