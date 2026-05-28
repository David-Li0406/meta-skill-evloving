# Pandoc YAML Variables Reference

Comprehensive guide to YAML frontmatter variables for Pandoc document conversion.

## Core Metadata

### title
**Type:** String
**Usage:** Document title
**Example:**
```yaml
title: "My Research Paper"
```

### author
**Type:** String or List
**Usage:** Author name(s)
**Examples:**
```yaml
author: "John Smith"

# Multiple authors
author:
  - "John Smith"
  - "Jane Doe"
```

### date
**Type:** String
**Usage:** Publication/document date
**Examples:**
```yaml
date: "November 2024"
date: "2024-11-16"
date: "16 November 2024"
```

### lang
**Type:** String (BCP 47 language code)
**Usage:** Document language for hyphenation, quotes, citations
**Examples:**
```yaml
lang: en-GB  # British English
lang: en-US  # American English
lang: en-IE  # Irish English
lang: de     # German
lang: fr     # French
```

## Bibliography and Citations

### bibliography
**Type:** String or List
**Usage:** Path to BibTeX (.bib) file(s)
**Examples:**
```yaml
bibliography: references.bib

# Multiple files
bibliography:
  - references.bib
  - additional.bib
```

### csl
**Type:** String
**Usage:** Path to Citation Style Language (.csl) file
**Examples:**
```yaml
csl: harvard.csl
csl: apa.csl
csl: ieee.csl
```

**Download CSL styles:** https://github.com/citation-style-language/styles

### link-citations
**Type:** Boolean
**Usage:** Make citations clickable links to bibliography
**Example:**
```yaml
link-citations: true
```

### citeproc
**Type:** Boolean (command-line option, not frontmatter)
**Usage:** Enable citation processing
**Command:**
```bash
pandoc doc.md -o doc.pdf --citeproc
```

## PDF Output Settings

### documentclass
**Type:** String
**Usage:** LaTeX document class
**Options:**
- `article` - Short documents, papers
- `report` - Longer documents with chapters
- `book` - Books with front matter
- `beamer` - Presentations

**Example:**
```yaml
documentclass: report
```

### fontsize
**Type:** String
**Usage:** Base font size
**Options:** `10pt`, `11pt`, `12pt`
**Example:**
```yaml
fontsize: 12pt
```

### geometry
**Type:** String
**Usage:** Page layout and margins
**Examples:**
```yaml
geometry: margin=1in
geometry: margin=2cm
geometry: "left=1.5in, right=1in, top=1in, bottom=1in"
geometry: "a4paper, margin=2.5cm"
```

### linestretch
**Type:** Number
**Usage:** Line spacing multiplier
**Examples:**
```yaml
linestretch: 1.0   # Single spacing
linestretch: 1.5   # 1.5 spacing
linestretch: 2.0   # Double spacing
```

### papersize
**Type:** String
**Usage:** Paper size
**Options:** `a4`, `letter`, `legal`, `executive`
**Example:**
```yaml
papersize: a4
```

## Table of Contents

### toc
**Type:** Boolean
**Usage:** Include table of contents
**Example:**
```yaml
toc: true
```

### toc-depth
**Type:** Integer (1-5)
**Usage:** Maximum heading level in TOC
**Example:**
```yaml
toc-depth: 3  # Include h1, h2, h3
```

### toc-title
**Type:** String
**Usage:** Custom TOC heading
**Example:**
```yaml
toc-title: "Contents"
```

### lof
**Type:** Boolean
**Usage:** Include list of figures
**Example:**
```yaml
lof: true
```

### lot
**Type:** Boolean
**Usage:** Include list of tables
**Example:**
```yaml
lot: true
```

## Section Numbering

### numbersections
**Type:** Boolean
**Usage:** Number section headings automatically
**Example:**
```yaml
numbersections: true
```

### secnumdepth
**Type:** Integer
**Usage:** Maximum heading level to number
**Example:**
```yaml
secnumdepth: 3  # Number up to h3
```

## LaTeX Customization

### header-includes
**Type:** String (multiline)
**Usage:** Custom LaTeX commands and packages
**Example:**
```yaml
header-includes: |
  \usepackage{graphicx}
  \usepackage{float}
  \usepackage{hyperref}
  \usepackage{amsmath}
```

### include-before
**Type:** String (multiline)
**Usage:** Content before document body
**Example:**
```yaml
include-before: |
  \begin{abstract}
  This is the abstract.
  \end{abstract}
```

### include-after
**Type:** String (multiline)
**Usage:** Content after document body
**Example:**
```yaml
include-after: |
  \appendix
  # Appendix content
```

## Typography

### mainfont
**Type:** String
**Usage:** Main document font (requires XeLaTeX or LuaLaTeX)
**Example:**
```yaml
mainfont: "Times New Roman"
```

### sansfont
**Type:** String
**Usage:** Sans-serif font
**Example:**
```yaml
sansfont: "Arial"
```

### monofont
**Type:** String
**Usage:** Monospace font for code
**Example:**
```yaml
monofont: "Courier New"
```

### fontfamily
**Type:** String
**Usage:** LaTeX font package
**Example:**
```yaml
fontfamily: palatino
```

## Presentation (Beamer)

### theme
**Type:** String
**Usage:** Beamer theme
**Options:** Madrid, Berlin, Copenhagen, Dresden, Frankfurt, Singapore, Warsaw
**Example:**
```yaml
theme: Madrid
```

### colortheme
**Type:** String
**Usage:** Beamer color scheme
**Options:** default, dolphin, beaver, crane, seahorse
**Example:**
```yaml
colortheme: default
```

### fonttheme
**Type:** String
**Usage:** Beamer font theme
**Options:** default, serif, structurebold, structureitalicserif
**Example:**
```yaml
fonttheme: default
```

### aspectratio
**Type:** Integer
**Usage:** Slide aspect ratio
**Options:** `43` (4:3), `169` (16:9), `1610` (16:10)
**Example:**
```yaml
aspectratio: 169
```

### navigation
**Type:** String
**Usage:** Navigation symbols
**Options:** horizontal, vertical, frame
**Example:**
```yaml
navigation: horizontal
```

## HTML Output

### css
**Type:** String or List
**Usage:** CSS stylesheet path(s)
**Examples:**
```yaml
css: style.css

# Multiple stylesheets
css:
  - style.css
  - syntax.css
```

### self-contained
**Type:** Boolean (command-line)
**Usage:** Embed all resources in HTML
**Command:**
```bash
pandoc doc.md -o doc.html --self-contained
```

## Code Highlighting

### highlight-style
**Type:** String
**Usage:** Syntax highlighting theme
**Options:** tango, pygments, kate, monochrome, espresso, zenburn, haddock, breezedark
**Example:**
```yaml
highlight-style: tango
```

## Custom Variables

### Custom Title Page Fields

**For thesis/academic work:**
```yaml
supervisor: "Dr. Jane Smith"
institution: "University Name"
department: "Department of Computer Science"
degree: "BSc Computer Science"
```

**Student Information:**
```yaml
student-id: "C21348423"
programme: "TU856"
module: "COMP4060"
```

**Contact Information:**
```yaml
email: "student@example.com"
website: "https://example.com"
```

## BibTeX Reference

### Entry Types

**Article:**
```bibtex
@article{citekey,
  author  = {Smith, John and Doe, Jane},
  title   = {Paper Title},
  journal = {Journal Name},
  year    = {2024},
  volume  = {42},
  number  = {3},
  pages   = {123--145},
  doi     = {10.1234/example}
}
```

**Book:**
```bibtex
@book{citekey,
  author    = {Johnson, Alice},
  title     = {Book Title},
  publisher = {Publisher Name},
  year      = {2023},
  edition   = {2nd},
  address   = {City},
  isbn      = {978-0-12-345678-9}
}
```

**Conference Paper:**
```bibtex
@inproceedings{citekey,
  author    = {Brown, Robert},
  title     = {Paper Title},
  booktitle = {Conference Proceedings},
  year      = {2024},
  pages     = {45--52},
  publisher = {ACM},
  doi       = {10.1145/example}
}
```

**PhD Thesis:**
```bibtex
@phdthesis{citekey,
  author  = {Williams, Michael},
  title   = {Thesis Title},
  school  = {University Name},
  year    = {2023},
  address = {City, Country}
}
```

**Master's Thesis:**
```bibtex
@mastersthesis{citekey,
  author  = {Davis, Sarah},
  title   = {Thesis Title},
  school  = {University Name},
  year    = {2024}
}
```

**Website:**
```bibtex
@misc{citekey,
  author = {Organization},
  title  = {Page Title},
  year   = {2024},
  url    = {https://example.com},
  note   = {Accessed: 2024-11-16}
}
```

### BibTeX Field Reference

**Required vs Optional varies by entry type**

**Common Fields:**
- `author` - Author names (use "and" to separate)
- `title` - Work title
- `year` - Publication year
- `journal` - Journal name (article)
- `booktitle` - Book/conference name
- `publisher` - Publisher name
- `school` - University (thesis)
- `pages` - Page range (use double dash: 123--145)
- `volume` - Volume number
- `number` - Issue number
- `edition` - Edition (2nd, 3rd, etc.)
- `address` - Location (city, country)
- `doi` - Digital Object Identifier
- `url` - Web address
- `note` - Additional information

**Author Formatting:**
```bibtex
author = {Lastname, Firstname}
author = {Lastname1, Firstname1 and Lastname2, Firstname2}
author = {Firstname Lastname}  # Auto-parsed
```

**Special Characters:**
```bibtex
title = {Study of {DNA} Sequencing}  # Protect caps
title = {Analysis of {IoT} Systems}
author = {M{\"u}ller, Hans}  # Umlaut
```

## Example Complete Frontmatter

### Academic Paper
```yaml
---
title: "Research Paper Title"
author: "Author Name"
date: "November 2024"
lang: en-GB

bibliography: references.bib
csl: harvard.csl
link-citations: true

documentclass: report
fontsize: 12pt
geometry: margin=1in
linestretch: 1.5
numbersections: true

toc: true
toc-depth: 3

header-includes: |
  \usepackage{graphicx}
  \usepackage{float}
  \usepackage{hyperref}
---
```

### Thesis
```yaml
---
title: "Thesis Title"
author: "Student Name"
date: "Month Year"
supervisor: "Dr. Supervisor Name"
institution: "University Name"
department: "Department Name"
degree: "BSc Computer Science"
lang: en-GB

bibliography: references.bib
csl: harvard.csl
link-citations: true

documentclass: report
fontsize: 12pt
geometry: margin=1in
linestretch: 1.5
numbersections: true
secnumdepth: 3

toc: true
toc-depth: 3
lof: true
lot: true
---
```

### Simple Article
```yaml
---
title: "Article Title"
author: "Author Name"
date: "Date"
lang: en-GB
documentclass: article
fontsize: 11pt
geometry: margin=1in
---
```

## Variable Precedence

1. **Command-line variables** (`-V key=value`) override
2. **Frontmatter variables**
3. **Defaults file variables**
4. **Pandoc built-in defaults**

## Resources

- **Pandoc Manual:** https://pandoc.org/MANUAL.html
- **CSL Styles:** https://github.com/citation-style-language/styles
- **BibTeX Reference:** https://www.bibtex.com/
- **LaTeX Packages:** https://ctan.org/
