## 7-Level Hierarchy

**Impact:** CRITICAL

Understand the strict priority order from lowest (1) to highest (7). Higher levels always override lower levels.

**Incorrect:**

**Mixing Levels**
Defining user-specific programs in a shared common module, making it hard to opt-out for other users.

**Correct:**

**Strict Layering**

1.  **Common modules** - Cross-platform base functionality
2.  **Platform modules** - OS-specific (nixos/darwin)
3.  **Home modules** - User-space programs
4.  **Suite modules** - Grouped functionality with defaults
5.  **Archetype modules** - High-level use case profiles
6.  **Host configs** - Host-specific overrides
7.  **User configs** - User-specific customizations (Highest Priority)
