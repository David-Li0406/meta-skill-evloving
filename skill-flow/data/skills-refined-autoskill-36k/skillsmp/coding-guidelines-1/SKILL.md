---
name: coding-guidelines
description: Coding patterns and guidelines for TypeScript/JavaScript, Rust, and frontend frameworks. Use this skill when writing TypeScript/JavaScript or Rust code, or working with SolidJS, Tailwind CSS, daisyUI, React Native, Expo, or NativeWind. Provides idiomatic patterns and best practices.
---

This skill provides coding patterns. Load references based on what you're working with.

## Formatting

Detect project formatter from config files (biome.json, .prettierrc, .eslintrc, pyproject.toml, rustfmt.toml, etc.) and follow its conventions.

General rules:
- Empty line at end of files
- Whitespace between logical blocks
- Property ordering: alphabetical by default (primitives first, then nested for mixed objects)

## References

| Technology | Reference | Load When |
|------------|-----------|-----------|
| TypeScript/JS | [references/typescript.md](references/typescript.md) | Writing TypeScript or JavaScript code |
| Rust | [references/rust.md](references/rust.md) | Writing Rust code |
| SolidJS | [references/solidjs.md](references/solidjs.md) | Writing SolidJS components or JSX with SolidJS patterns |
| Tailwind CSS | [references/tailwind.md](references/tailwind.md) | Using Tailwind utility classes |
| daisyUI | [references/daisyui.md](references/daisyui.md) | Using daisyUI component classes |
| React Native | [references/react-native.md](references/react-native.md) | Writing React Native components (View, Text, etc.) |
| Expo | [references/expo.md](references/expo.md) | Using Expo Router, Expo packages, or app.json config |
| NativeWind | [references/nativewind.md](references/nativewind.md) | Using className prop in React Native |

## When to Load References

Load a reference when:
- The code you're writing uses that technology
- You see imports or patterns from that framework
- The user mentions working with that technology

Each reference contains:
- Core principles for that framework
- Research guidance (use context7 to query current docs)
- Research checklist before implementing

## Research-First Approach

These frameworks evolve - class names, APIs, and patterns change between versions. Each reference emphasizes:
- **Principles** over specific syntax
- **Research checklists** to verify current behavior
- **context7** for querying up-to-date documentation
