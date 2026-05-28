---
name: constructors
description: Use config structs in constructor functions.
---

# Overview

Non-trivial structs should be configured with a config struct, like so:

```
func NewX(cfg XConfig) {
    // Apply defaults
    // Validate
}

struct XConfig {
    // All config parameters here
}

## When to use

Any time there is a struct to be construct that...

- Is either non trivial
- Is especially likely to evolve