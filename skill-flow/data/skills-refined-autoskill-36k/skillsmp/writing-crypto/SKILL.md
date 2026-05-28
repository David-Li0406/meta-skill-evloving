---
name: writing-crypto
description: |
  Write cryptography prose and notation using the project's bibsp.sty + preamble.tex conventions (acro + biblatex footnote citations and standardized math macros). Use proactively when: (1) writing/editing cryptography sections in .tex files, (2) introducing or using crypto acronyms such as IND-CPA, IND-CCA, AE, MAC, PRF, ZK, and DH, (3) defining schemes/algorithms/variables in math notation, (4) adding citations for security notions or standard primitives, (5) writing security proofs or reductions, (6) user mentions biblatex, crypto notation, or security proof in cryptographic context.
---

# Writing Crypto With bibsp

## Overview

This project uses `bibsp.sty` (loaded from `preamble.tex`) to keep cryptography writing consistent: acronyms expand correctly and cite the right source, and common crypto notation is standardized via macro factories.

## Quick Start

1. Load the standard preamble (already done in the thesis):

```latex
\input{preamble}
```

2. Use acronyms for crypto terms and security notions:

```latex
We model the adversary as \ac{PPT} and require \ac{IND-CPA} security.
We use \ac{DH} to establish a shared key and authenticate with a \ac{MAC}.
```

3. Use `\autocite{...}` for non-acronym citations in running text.

## Core Conventions

### Acronyms With Built-in Citations (acro + biblatex)

- `bibsp.sty` declares many crypto acronyms via `\DeclareAcronym{...}{...}`.
- Many entries include `cite = {<bibkey>}`. When the acronym is used, `acro` can attach a citation.
- In this project, `preamble.tex` should set:
  - `\usepackage{bibsp}`
  - `\acsetup{cite/cmd=\autocite}`
  - `biblatex` is configured so `\autocite{...}` produces footnote citations.

Practical rule: if an acronym exists in `bibsp.sty`, prefer `\ac{...}` over spelling it out manually, and let the citation happen automatically when configured.

### Crypto Notation Macro Factories (Schemes, Algorithms, Variables, Sets)

Use the `bibsp.sty` factories to define consistent notation in the preamble for each paper/chapter.

#### Schemes

Define a scheme identifier that typesets as `\mathsf{...}` and supports optional “method” suffixes:

```latex
\NewScheme{\AE}{AE}
```

Use it like:

```latex
\AE[Enc] \textand \AE[Dec]
```

#### Algorithms and Functions

Define algorithm/function macros that behave like operators and accept optional argument lists.

```latex
\NewAlgorithm{\Enc}{Enc}
\NewAlgorithm{\Dec}{Dec}
\NewFunction{\Hash}{H}
```

Usage patterns:

```latex
c \gets \Enc[m]
\qquad
m \gets \Dec[c]
\qquad
h \gets \Hash[m]
```

The [...] optional argument adds parentheses, automatically using \left and \right.

Star form convention: most of these macros support a starred form (e.g., `\Enc*`) that draws an overline, used for “idealized/modified/adversarial” variants when you need that notation.

#### Variables and Sets

```latex
\NewVariable{\pk}{pk}
\NewVariable{\sk}{sk}
\NewSet{\UU}{U}
```

Variables typeset as math italic; sets as calligraphic.

### Proof(-Of-Knowledge) Notation

Prefer the built-in statement macros for proofs:

```latex
We use a \ac{ZKPK} of knowledge:
$\PK[(w)]{\mathrm{stmt}(w)}$.

For Schnorr-style statements, use $\SPK[...]$ when appropriate.
```

(Exact `\PK`/`\SPK` usage depends on whether you include a witness list and/or side conditions; see `bibsp.sty` definitions if you need a specific shape.)

## Common Patterns

### Security Notions

- Prefer the acronym if available: `\ac{IND-CPA}`, `\ac{IND-CCA}`, `\ac{SUF-CMA}`, `\ac{INT-CTXT}`, etc.
- If you need the plain text tag in math/prose (without acronym management), `bibsp.sty` also provides helpers like `\indcpa`, `\indcca`.

### Crypto Citations

- If the concept is an acronym with a `cite` field in `bibsp.sty`, use `\ac{...}` and avoid adding a second manual citation.
- Otherwise use `\autocite{BibKey}` in prose.

## Notes For This Repository

- Source of truth for the setup:
  - `/home/dbosk/phd/thesis/preamble.tex`
  - `/home/dbosk/phd/thesis/bibsp.sty`
- Typical usage in body text across the thesis: `.tex` files use `\autocite{...}`, `\citeauthor{...}`, and `\ac{...}`.
