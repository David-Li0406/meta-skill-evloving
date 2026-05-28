# Skill Creator Guidelines

**Version 1.0.0**  
aytordev  
January 2026

> **Note:**  
> This document is mainly for agents and LLMs to follow when creating,  
> maintaining, or refactoring AI agent skills. Humans may also find  
> it useful, but guidance here is optimized for automation and  
> consistency by AI-assisted workflows.

---

## Abstract

Guide for configuring theming in aytordev's system using Stylix and Catppuccin.

---

## Table of Contents

1. [Core Principles](#1-core-principles) — **CRITICAL**
   - 1.1 [Centralized SOT (Source Of Truth)](#11-centralized-sot-source-of-truth)
2. [Consumption](#2-consumption) — **HIGH**
   - 2.1 [App Themes & Variants](#21-app-themes--variants)
   - 2.2 [Using the Palette](#22-using-the-palette)
3. [Implementation](#3-implementation) — **MEDIUM**
   - 3.1 [Library Helpers](#31-library-helpers)
   - 3.2 [Polarity Logic](#32-polarity-logic)

---

## 1. Core Principles

**Impact: CRITICAL**

Centralized source of truth and provider/consumer pattern.

### 1.1 Centralized SOT (Source Of Truth)

**Impact: MEDIUM**

The `aytordev.theme` module is the single source of truth for all theming data. It abstracts the underlying colors (Kanagawa) and provides a unified API for all other modules to consume. Never hardcode colors or imports in individual modules.

**Incorrect:**

**Fragmented definitions**

Importing `colors.nix` directly in module files or defining local color variables like `blue = "#..."`.

**Correct:**

```nix
{ config, lib, ... }:
let
  cfg = config.aytordev.theme;
in
{
  # Access palette through the central config
  programs.foo.color = cfg.palette.accent.hex;
}
```

**Provider Consumption**

Consume `config.aytordev.theme` to access all theme data. This ensures consistent polarity and variant switching across the entire system.

---

## 2. Consumption

**Impact: HIGH**

Consuming the palette, variants, and application-specific theme names.

### 2.1 App Themes & Variants

**Impact: MEDIUM**

For applications that need a named theme (e.g., "Kanagawa Wave" vs "kanagawa-wave"), use the convenience accessors in `config.aytordev.theme.appTheme`. This avoids string formatting errors.

**Incorrect:**

**String Interpolation**

Manually constructing theme names like `"Kanagawa ${config.aytordev.theme.variant}"`.

**Correct:**

```nix
# Returns "Kanagawa Wave" or "Kanagawa Lotus"
theme = config.aytordev.theme.appTheme.capitalized;

# Returns "kanagawa-wave" or "kanagawa-lotus"
theme = config.aytordev.theme.appTheme.kebab;
```

**Standardized Names**

Use the pre-calculated formats provided by the module.

### 2.2 Using the Palette

**Impact: MEDIUM**

The palette is exposed at `config.aytordev.theme.palette`. It provides semantic colors relative to the active variant (Wave/Dragon/Lotus) and polarity (Dark/Light). Do not switch on variants inside modules; rely on the palette to provide the correct color for the current state.

**Incorrect:**

**Manual Variant Switching**

Using `if variant == "lotus"` inside a module configuration to select colors.

**Correct:**

```nix
# BAD
color = if config.aytordev.theme.variant == "lotus" then "#..." else "#...";

# GOOD
color = config.aytordev.theme.palette.bg.main.hex;
```

**Semantic Access**

Trust `theme.palette` to provide the correct color.

---

## 3. Implementation

**Impact: MEDIUM**

Using library helpers and handling polarity logic.

### 3.1 Library Helpers

**Impact: MEDIUM**

Use `config.aytordev.theme.lib` for common transformations, such as converting hex colors to Sketchybar format (`0xff...`) or extracting subsets of the palette.

**Incorrect:**

**Regex Magic**

Manually replacing `#` with `0xff` using string manipulation functions in every module.

**Correct:**

```nix
let
  themeLib = config.aytordev.theme.lib;
  accent = config.aytordev.theme.palette.accent.hex;
in
{
  # Correctly formats as 0xffRRGGBB
  color = themeLib.hexToSketchybar accent;
}
```

**Standard Functions**

Use the provided helpers for consistency.

### 3.2 Polarity Logic

**Impact: MEDIUM**

When you explicitly need to know if the theme is light or dark (e.g. for boolean flags), use `config.aytordev.theme.isLight`. This handles edge cases (like "lotus" variant implying light mode even if polarity wasn't explicitly set).

**Incorrect:**

**Fragile Checks**

Checking `config.aytordev.theme.polarity == "light"` directly, which misses the case where variant="lotus" forces light mode.

**Correct:**

```nix
programs.bat.config = {
  # Some apps need a boolean flag for light mode
  "--light" = lib.mkIf config.aytordev.theme.isLight;
};
```

**Computed Boolean**

Use the robust computed value.

---

