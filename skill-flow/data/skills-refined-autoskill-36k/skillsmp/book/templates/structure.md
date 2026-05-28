# Book Structure Guide

This document describes the folder and file naming conventions for creating structured books. The structure is **format-agnostic** - it works with any markup language (.tex, .md, .html, etc.).

---

## Overview

```
type/
├── main.xx                          # Root file - includes all parts
├── localsettings.xx                 # Global settings/styles
├── 100-frontmatter/                 # Front matter section
├── 200-bodymatter/                  # Main content
│   ├── part01-name/                 # Part 1
│   │   └── chXX-name/               # Chapters (roman numerals for intro)
│   │       └── secXX-name.xx        # Sections
│   └── part02-name/                 # Part 2
│       └── chXX-name/               # Chapters (arabic numerals)
├── 300-backmatter/                  # Back matter section
└── bib/                             # Bibliography/references
```

---

**type** could be any language in which the book is written:

* latex - which means xx=tex
* markdown - which means xx=md
* html - which means xx =html
* etc

## Naming Conventions

### Numeric Prefixes

All folders and files use **3-digit numeric prefixes** for sorting:

| Prefix Range | Purpose                    |
| ------------ | -------------------------- |
| `100-199`  | Front matter               |
| `200-299`  | Body matter (main content) |
| `300-399`  | Back matter                |

Within ranges, use **10-unit increments** to allow insertions:

- `100`, `110`, `120`, `130`... (not 101, 102, 103)

### Slug Format

After the numeric prefix, use **lowercase descriptive names**:

- Words separated by hyphens: `ch01-ettersporselprognoser`
- No special characters (ø → o, æ → ae, å → a)
- Keep reasonably short (max ~30 chars)

---

## Hierarchy Levels

### Level 1: Root

```
main.xx                    # Root document
localsettings.xx           # Global configuration
```

### Level 2: Major Sections (Frontmatter, Bodymatter, Backmatter)

```
100-frontmatter/
├── frontmatter.xx         # Aggregator - includes all frontmatter files
├── 100-frontpage.xx       # Title page
├── 110-preface.xx         # Preface
├── 120-about.xx           # About this book
├── 130-acknowledgements.xx
└── 140-toc.xx             # Table of contents
```

```
200-bodymatter/
├── bodymatter.xx          # Aggregator - includes all parts
├── part01-innledning/     # Part 1: Introduction
└── part02-omrader/        # Part 2: Topics
```

```
300-backmatter/
├── backmatter.xx          # Aggregator
├── 100-bibliography.xx    # References list
├── 110-index.xx           # Index
├── app01-name/            # Appendix A
└── app02-name/            # Appendix B
```

### Level 3: Parts

Parts are numbered folders within bodymatter:

```
200-bodymatter/
├── part01-innledning/     # Part 1
│   └── part01.xx          # Part aggregator
└── part02-omrader/        # Part 2
    └── part02.xx          # Part aggregator
```

### Level 4: Chapters

Chapters use prefixes that match their numbering scheme:

**Part 1 (Introduction) - Roman numerals:**

```
part01-innledning/
├── chi-begreper/                           # Chapter I
│   └── chi-begreper.xx
├── chii-arbeidsflyt-og-ki/                 # Chapter II
│   └── chii-arbeidsflyt-og-ki.xx
└── chiii-prosjektgjennomforing-med-ki/     # Chapter III
    └── chiii-prosjektgjennomforing-med-ki.xx
```

**Part 2 (Main content) - Arabic numerals:**

```
part02-omrader/
├── ch01-ettersporselprognoser/     # Chapter 1
│   └── ch01-ettersporselprognoser.xx
├── ch02-lagerstyring/              # Chapter 2
│   └── ch02-lagerstyring.xx
└── ch03-produksjonsplanlegging/    # Chapter 3
    └── ch03-produksjonsplanlegging.xx
```

### Level 5: Sections

Sections are files within chapter folders:

```
ch01-ettersporselprognoser/
├── ch01-ettersporselprognoser.xx      # Chapter file (aggregator)
├── sec01-omrade.xx                    # Section 1.1
├── sec02-problemstilling.xx           # Section 1.2
├── sec03-modell.xx                    # Section 1.3
├── sec04-prosess.xx                   # Section 1.4
├── sec05-metode.xx                    # Section 1.5
├── sec06-eksempel-kampanjestyring.xx  # Section 1.6
├── sec07-eksempel-lagerstyring-ml.xx  # Section 1.7
└── sec08-anbefalt-fordypning.xx       # Section 1.8
```

### Level 6: Supporting Folders

Each chapter can have supporting folders:

```
ch01-ettersporselprognoser/
├── ch01-ettersporselprognoser.xx
├── sec01-omrade.xx
├── figures/          # Images for this chapter
├── docs/             # Source documents, notes
└── references/       # Chapter-specific references
```

---

## Complete Example

Based on "Kvantitative metoder i logistikk":

```
latex/
├── main.xx
├── localsettings.xx
├── bib/
│   └── references.bib
│
├── 100-frontmatter/
│   ├── frontmatter.xx
│   ├── 100-frontpage.xx
│   ├── 110-preface.xx
│   ├── 120-about.xx
│   ├── 130-acknowledgements.xx
│   └── 140-toc.xx
│
├── 200-bodymatter/
│   ├── bodymatter.xx
│   │
│   ├── part01-innledning/
│   │   ├── part01.xx
│   │   │
│   │   ├── chi-begreper/
│   │   │   ├── chi-begreper.xx
│   │   │   ├── sec01-omrade.xx
│   │   │   ├── sec02-problemstilling.xx
│   │   │   ├── sec03-modell.xx
│   │   │   ├── sec04-prosess.xx
│   │   │   ├── sec05-metoder.xx
│   │   │   └── figures/
│   │   │
│   │   ├── chii-arbeidsflyt-og-ki/
│   │   │   ├── chii-arbeidsflyt-og-ki.xx
│   │   │   ├── sec01-arbeidsflyt.xx
│   │   │   ├── sec02-ki.xx
│   │   │   └── figures/
│   │   │
│   │   └── chiii-prosjektgjennomforing-med-ki/
│   │       ├── chiii-prosjektgjennomforing-med-ki.xx
│   │       ├── sec01-rolleavklaring.xx
│   │       ├── sec02-fire-faser.xx
│   │       └── figures/
│   │
│   └── part02-omrader/
│       ├── part02.xx
│       │
│       ├── ch01-ettersporselprognoser/
│       │   ├── ch01-ettersporselprognoser.xx
│       │   ├── sec01-omrade.xx
│       │   ├── sec02-problemstilling.xx
│       │   ├── sec03-modell.xx
│       │   ├── sec04-prosess.xx
│       │   ├── sec05-metode.xx
│       │   ├── sec06-eksempel-kampanjestyring.xx
│       │   ├── sec07-eksempel-lagerstyring-ml.xx
│       │   ├── sec08-anbefalt-fordypning.xx
│       │   ├── figures/
│       │   └── docs/
│       │
│       ├── ch02-lagerstyring/
│       │   ├── ch02-lagerstyring.xx
│       │   ├── sec01-kvantitative-utfordringer.xx
│       │   ├── sec02-metoder-lagerstyring.xx
│       │   ├── sec03-lagerstyring-eksempel-metode-1.xx
│       │   ├── sec04-lagerstyring-eksempel-metode-2.xx
│       │   ├── sec05-lagerstyring-eksempel-metode-3.xx
│       │   ├── sec06-lagerstyring-eksempel-metode-4.xx
│       │   └── sec07-lagerstyring-eksempel-metode-5.xx
│       │
│       └── ... (ch03 through ch11 follow same pattern)
│
└── 300-backmatter/
    ├── backmatter.xx
    ├── 100-bibliography.xx
    ├── 110-index.xx
    ├── app01-sjekklister/
    └── app02-types/
```

---

## Naming Pattern Summary

| Element                 | Pattern           | Example                           |
| ----------------------- | ----------------- | --------------------------------- |
| Major section folder    | `NNN-name/`     | `100-frontmatter/`              |
| Frontmatter file        | `NNN-name.xx`   | `120-about.xx`                  |
| Part folder             | `partNN-name/`  | `part01-innledning/`            |
| Chapter folder (roman)  | `chR-name/`     | `chi-begreper/`                 |
| Chapter folder (arabic) | `chNN-name/`    | `ch01-ettersporselprognoser/`   |
| Chapter file            | `chNN-name.xx`  | `ch01-ettersporselprognoser.xx` |
| Section file            | `secNN-name.xx` | `sec01-omrade.xx`               |
| Appendix folder         | `appNN-name/`   | `app01-sjekklister/`            |
| Aggregator file         | `name.xx`       | `bodymatter.xx`                 |

---

## Key Principles

1. **Folder = File**: The main file inside a folder has the same name as the folder

   - `ch01-ettersporselprognoser/ch01-ettersporselprognoser.xx`
2. **Aggregators**: Each container folder has an aggregator file that includes its children

   - `frontmatter.xx` includes all frontmatter files
   - `part01.xx` includes all chapters in Part 1
   - `ch01-ettersporselprognoser.xx` includes all sections
3. **Numeric sorting**: Prefixes ensure correct display order in file browsers
4. **Self-contained chapters**: Each chapter folder contains everything it needs:

   - Main chapter file
   - Section files
   - figures/ folder
   - docs/ folder (optional)
5. **Consistent depth**: All content follows the same hierarchy depth:

   - main → bodymatter → part → chapter → section
