# LaTeX Examples for Didactic Notes

This reference provides detailed LaTeX code examples for using didactic notes in educational materials.

## Table of Contents

1. [Learning Objectives with Restatable](#learning-objectives-with-restatable)
2. [Referencing Learning Objectives](#referencing-learning-objectives)
3. [Citing Pedagogical Research](#citing-pedagogical-research)
4. [Complete Example Sections](#complete-example-sections)

---

## Learning Objectives with Restatable

### Defining Learning Objectives

Use `\begin{restatable}{lo}{MnemonicLabel}\label{MnemonicLabel}...\end{restatable}` in your abstract or learning objectives section:

```latex
\begin{restatable}{lo}{FilesLOPersistence}\label{FilesLOPersistence}%
  Förklara skillnaden mellan primärminne och sekundärminne samt varför filer
  behövs för persistens.
\end{restatable}

\begin{restatable}{lo}{FilesLOOperations}\label{FilesLOOperations}%
  Använda filoperationer (\mintinline{python}{open()},
  \mintinline{python}{read()}, \mintinline{python}{write()},
  \mintinline{python}{close()}) korrekt.
\end{restatable}
```

**Key points:**
- Use **mnemonic labels** (e.g., `FilesLOPersistence`, not `FilesLO1`)
- Labels describe the objective content, not just numbers
- **CRITICAL**: Add `\label{MnemonicLabel}` matching the restatable name for `\cref{}` support
- The `%` after the opening brace prevents unwanted whitespace

### Setup for Restatable Learning Objectives

Ensure your preamble includes:

```latex
\usepackage{thmtools,thm-restate}
\usepackage{didactic}

\ProvideSemanticEnv{lo}{Learning Objective}
  [style=definition,numbered=yes]
  {LO}{LO}
  {Learning objective}{Learning objectives}

% Translations for Swedish
\ProvideTranslation{swedish}{Learning Objective}{Lärandemål}
\ProvideTranslation{swedish}{LO}{lm}
\ProvideTranslation{swedish}{Learning objective}{Lärandemål}
\ProvideTranslation{swedish}{Learning objectives}{Lärandemål}
```

---

## Referencing Learning Objectives

### Method 1: Using `\cref{}` (Recommended for Expanded Notes)

When writing more detailed pedagogical notes, use `\cref{Label}` to reference learning objectives explicitly:

```latex
\ltnote{%
  Relevanta lärandemål:
  \cref{FilesLOPersistence}

  \textbf{Variationsmönster}: Kontrast

  \textbf{Vad som varierar}: Typ av minne (primär vs sekundär)...

  \textbf{Kritiska aspekter för} \cref{FilesLOPersistence}:
  \begin{itemize}
    \item \textbf{Persistens som koncept}: Studenten måste urskilja...
  \end{itemize}
}
```

**Advantages of `\cref{}`:**
- More natural in prose: "Kritiska aspekter för \cref{FilesLOOperations}:"
- Cleaner when referencing multiple times in the same note
- Better for expanded, detailed pedagogical annotations
- Works in lists and other environments

### Method 2: Using Starred Commands (Compact Version)

For more concise notes, use the starred command `\LabelName*` which expands to the full LO text:

```latex
\ltnote{%
  Relevanta lärandemål:
  \FilesLOPersistence*

  \textbf{Kontrast}: Typ av minne (primär vs sekundär)...
}
```

**Key formatting rules:**
1. **Use header**: Begin with "Relevanta lärandemål:" (or "Relevant learning objectives:" in English)
2. **Each LO on its own line**: Don't use commas between multiple LOs
3. **No trailing punctuation**: Don't add periods after LO commands
4. **Blank line after LOs**: Separate LOs from the rest of the note content

### Multiple Learning Objectives

**With `\cref{}`:**
```latex
\ltnote{%
  Relevanta lärandemål:
  \cref{FilesLOOperations}, \cref{FilesLOContextMgr}, \cref{FilesLOFileTypes}

  \textbf{Variationsmönster}: Generalisering + Kontrast

  \textbf{Kontrast för} \cref{FilesLOContextMgr}: Resurshanteringsmetod...

  \textbf{Separation för} \cref{FilesLOOperations} \textbf{och}
  \cref{FilesLOFileTypes}: Läsa vs skriva...
}
```

**With starred commands:**
```latex
\ltnote{%
  Relevanta lärandemål:
  \FilesLOOperations*
  \FilesLOContextMgr*
  \FilesLOFileTypes*

  \textbf{Generalisering + Kontrast}: Koppling till...
}
```

### Learning Objectives Cannot Be in Lists

**CRITICAL**: Learning objective commands created by `restatable` are like theorem environments—they cannot be placed inside `\begin{itemize}` or other list environments.

**Wrong:**
```latex
\ltnote{%
  \textbf{Kritiska aspekter}:
  \begin{itemize}
    \item \FilesLOOperations* --- Resurshantering
    \item \FilesLOContextMgr* --- Automatisk stängning
  \end{itemize}
}
```

**Correct - Move LO commands outside lists:**
```latex
\ltnote{%
  \FilesLOOperations*, \FilesLOContextMgr*.

  \textbf{Kritiska aspekter}:
  \begin{itemize}
    \item \textbf{Resurshantering}: Filer måste stängas.
    \item \textbf{Kontexthanterare}: Automatisk stängning även vid fel.
  \end{itemize}
}
```

---

## Citing Pedagogical Research

### Separate Bibliography for Pedagogical References

**Best practice**: Use a separate `.bib` file for pedagogical and learning theory references (e.g., `ltnotes.bib`), distinct from domain-specific references.

**In your preamble:**
```latex
\usepackage[natbib,style=alphabetic,maxbibnames=99]{biblatex}
\addbibresource{bibliography.bib}  % Domain references
\addbibresource{ltnotes.bib}        % Pedagogical references
```

### Creating ltnotes.bib

Create a separate file with pedagogical references:

```bibtex
@article{MartonPang2006,
  author    = {Marton, Ference and Pang, Ming Fai},
  title     = {On Some Necessary Conditions of Learning},
  journal   = {Journal of the Learning Sciences},
  year      = {2006},
  volume    = {15},
  number    = {2},
  pages     = {193--220},
  doi       = {10.1207/s15327809jls1502_2}
}

@book{Marton2015,
  author    = {Marton, Ference},
  title     = {Necessary Conditions of Learning},
  publisher = {Routledge},
  address   = {London},
  year      = {2015},
  isbn      = {978-0-415-739139}
}
```

### Using Citations in Didactic Notes

**Use biblatex citation commands** instead of hardcoded references:

**Wrong:**
```latex
\ltnote{%
  Following Marton & Pang (2006), we vary the operation while keeping
  the pattern invariant...
}
```

**Correct:**
```latex
\ltnote{%
  Following \textcite{MartonPang2006}, we vary the operation while keeping
  the pattern invariant...
}
```

**Common biblatex commands for pedagogical notes:**
- `\textcite{key}` → "Marton and Pang (2006)"
- `\parencite{key}` → "(Marton and Pang 2006)"
- `\citeauthor{key}` → "Marton and Pang"
- `\citeyear{key}` → "2006"

---

## Complete Example Sections

### Example: Complete Section with Notes

First, define learning objectives in your abstract:

```latex
\begin{restatable}{lo}{RecursionLOConcept}%
  Förklara rekursionsbegreppet och identifiera basfall och rekursivt steg.
\end{restatable}

\begin{restatable}{lo}{RecursionLOImplementation}%
  Implementera enkla rekursiva funktioner korrekt.
\end{restatable}
```

Then use them in your content:

```latex
\section{Introduction to Recursion}

Let's start with your intuition.

\ltnote{%
  Relevanta lärandemål:
  \cref{RecursionLOConcept}

  \textbf{Variationsmönster}: Try-first pedagogy

  Vi börjar med utforskning av förkunskaper för att aktivera studenternas
  intuitiva förståelse. Studenten förbinder rekursion med konkreta exempel
  (ryska dockor, fraktaler) innan formell definition introduceras.
}

\begin{activity}\label{WhatIsRecursion}
  Have you seen anything in everyday life that contains smaller versions
  of itself?
\end{activity}

Now let's look at how this appears in programming.

\ltnote{%
  \textbf{Variationsmönster}: Generalisering

  Vi rör oss från konkreta vardagsexempel till kod, vilket ger en bro mellan
  intuitiv och formell förståelse.

  Enligt \textcite{MartonPang2006} underlättar denna progression från bekanta
  till abstrakta kontexter lärande genom att skapa variation i representation
  medan konceptet hålls invariant.
}

Here's a simple recursive function:

\begin{minted}{python}
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)
\end{minted}

\ltnote{%
  Relevanta lärandemål:
  \cref{RecursionLOConcept}, \cref{RecursionLOImplementation}

  \textbf{Variationsmönster}: Generalisering (helhet före delar)

  \textbf{Kritiska aspekter för} \cref{RecursionLOConcept}:
  \begin{itemize}
    \item \textbf{Rekursiv struktur}: Funktionen anropar sig själv med
      modifierat argument. Studenten måste urskilja självreferensen.
    \item \textbf{Basfall}: Villkoret \mintinline{python}{n <= 1} stoppar
      rekursionen. Utan detta blir det oändlig loop.
  \end{itemize}

  \textbf{Pedagogisk sekvens}: Vi börjar med den kompletta funktionen
  (helheten) enligt variation theory. I senare avsnitt bryter vi ner
  basfallet och det rekursiva steget (delarna), genom att variera vad vi
  fokuserar på medan andra aspekter hålls invarianta.
}
```

### Detailed Pattern with Variation Theory

```latex
\ltnote{%
  Relevanta lärandemål:
  \cref{FilesLOPersistence}

  \textbf{Variationsmönster}: Kontrast

  \textbf{Vad som varierar}: Typ av minne (primär vs sekundär), egenskaper
  (flyktigt vs oflyktigt).

  \textbf{Vad som hålls invariant}: Behovet att lagra data.

  \textbf{Kritiska aspekter för} \cref{FilesLOPersistence}:
  \begin{itemize}
    \item \textbf{Persistens som koncept}: Primärminne försvinner vid
      avstängning, sekundärminne består. Studenten måste urskilja att filer
      löser problemet med datapersistens.
    \item \textbf{Avvägning}: Primärminne snabbt men temporärt, sekundärminne
      långsammare men permanent.
  \end{itemize}

  Enligt \textcite{MartonPang2006} gör denna kontrast de kritiska aspekterna
  av persistens urskiljbara för studenter.
}
```

### Compact Pattern

```latex
\ltnote{%
  Relevanta lärandemål:
  \FilesLOPersistence*

  \textbf{Kontrast}: Typ av minne (primär vs sekundär). Invariant: Behovet att
  lagra data.
}
```
