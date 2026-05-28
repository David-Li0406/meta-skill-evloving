# Beamer Patterns for Didactic Materials

This reference describes Beamer-specific patterns for creating educational materials that work as both slides and articles.

## Table of Contents

1. [Notes in Slides vs Instructor Notes](#notes-in-slides-vs-instructor-notes)
2. [Article Prose Outside Frames](#article-prose-outside-frames)
3. [Overlay Specifications](#overlay-specifications)
4. [Verbose Environments](#verbose-environments)
5. [Side-by-Side with \textbytext](#side-by-side-with-textbytext)
6. [Figures and Tables with sidecaption](#figures-and-tables-with-sidecaption)
7. [Toggling Notes for Different Audiences](#toggling-notes-for-different-audiences)

---

## Notes in Slides vs Instructor Notes

### Visibility in Beamer Slides

In typical workflows, didactic notes are written once in shared content and are only intended to be visible in instructor/article builds.

**Practical rule:** You normally do not need to add any special guards to hide `\ltnote{...}` in Beamer slides; notes are off by default for the slide build in this workflow.

---

## Article Prose Outside Frames

When producing both slides and an article/notes version:

- **Prefer writing expanded prose outside `frame` environments**. Text outside frames is ignored in Beamer presentation mode.
- Use `\only<article>{...}` / `\only<presentation>{...}` inside a frame when you must mix article-only and slide-only material.
- Prefer `\only` inside frames to deduplicate content: keep a single frame with a shared structure (e.g., a `definition` title) and switch only the body between slide bullets and article prose.
- Avoid overusing `\mode<article>` / `\mode<presentation>`; reserve it for structural switches.

---

## Overlay Specifications

### Issue with Didactic Environments

Didactic package's semantic environments don't support Beamer's `<overlay>` syntax directly.

**Problem:** Writing `\begin{definition}<1,3>[Title]` or `\begin{definition}[Title]<1,3>` causes the overlay spec to appear as text in notes.

**Solution:** Wrap in `uncoverenv`:

```latex
\begin{frame}
  \begin{uncoverenv}<1,3>
    \begin{definition}[Primärminne]
      Datorns arbetsminne där exekverande program lagras...
    \end{definition}
  \end{uncoverenv}

  \begin{uncoverenv}<2,3>
    \begin{definition}[Sekundärminne]
      Oflyktigt minne där filer lagras...
    \end{definition}
  \end{uncoverenv}
\end{frame}
```

### Correct Approach for Multiple Examples

```latex
\begin{frame}[fragile]
  \begin{uncoverenv}<+->
    \begin{example}[Write to file]
      Skriva text till en fil:
      \inputminted{python}{write.py}
    \end{example}
  \end{uncoverenv}

  \begin{uncoverenv}<+->
    \begin{example}[Read from file]
      Läsa från fil:
      \inputminted{python}{read.py}
    \end{example}
  \end{uncoverenv}
\end{frame}
```

**Note:** For side-by-side definitions, use `\textbytext` with mode splits instead of overlay specs—the spatial contrast is more effective than temporal uncovering.

---

## Verbose Environments

### Issue

Semantic environments (definition, remark, example, block) can become too verbose for slides when they contain multiple sentences or paragraphs.

### Solution

Use `\mode<presentation>` and `\mode<article>` to provide concise versions for slides and full explanations for articles.

**When to split:**
- **Verbose prose**: More than 2-3 lines of running text in an environment
- **Multiple paragraphs**: Any environment with 2+ paragraphs
- **Complex examples**: Scenarios with extensive context that can be summarized

### Pattern

```latex
\begin{frame}
  \mode<presentation>{%
    \begin{remark}[Title]
      \begin{itemize}
        \item Concise bullet point 1
        \item Concise bullet point 2
        \item Concise bullet point 3
      \end{itemize}
    \end{remark}
  }
  \mode<article>{%
    \begin{remark}[Title]
      Full explanatory text with multiple sentences providing
      detailed context and reasoning.

      Additional paragraphs can explain nuances that would
      overwhelm a slide but are valuable in written form.
    \end{remark}
  }
\end{frame}
```

### Example: Verbose Remark Becomes Bullets

```latex
\begin{frame}
  \mode<presentation>{%
    \begin{remark}[Kontrastpunkten: Garanterad resurshantering]
      \begin{itemize}
        \item \mintinline{python}{with}: Filen stängs alltid, även vid exception
        \item Manuell hantering: Risk att filen lämnas öppen vid fel
        \item Automatisk cleanup när blocket lämnas
      \end{itemize}
    \end{remark}
  }
  \mode<article>{%
    \begin{remark}[Kontrastpunkten: Garanterad resurshantering]
      Båda metoderna fungerar när allt går som planerat. Men
      with-satsen har en avgörande fördel: den garanterar att
      filen alltid stängs korrekt, även om ett exception uppstår.

      Med manuell hantering riskerar vi att filen lämnas öppen
      om något går fel. With-satsen implementerar
      kontexthanterare-protokollet och anropar close()
      automatiskt när blocket lämnas.
    \end{remark}
  }
\end{frame>
```

### Example: Long Example Becomes Concise

```latex
\begin{frame}
  \mode<presentation>{%
    \begin{example}[Spara spelets progress]
      Spel måste minnas poäng och achievements mellan
      sessioner—löses genom att spara data i fil.
    \end{example}
  }
  \mode<article>{%
    \begin{example}[Spara spelets progress]
      Ett spel behöver komma ihåg spelarens poäng, nivå,
      och upplåsta achievements mellan olika spelsessioner.
      När spelaren stänger ner programmet och startar det
      igen nästa dag ska all progress finnas kvar. Detta
      löses genom att spara data i en fil på hårddisken.
    \end{example}
  }
\end{frame>
```

**Key principle:** Slides need visual clarity and conciseness; articles can provide depth and explanation. Design for both audiences.

---

## Side-by-Side with \textbytext

### Purpose

Place two semantic environments side-by-side for immediate visual contrast.

The didactic.sty package provides `\textbytext{...}{...}` and `\textbytext*{...}{...}` to create side-by-side layouts:

**Key differences:**
- **\textbytext*** (starred): Uses fullwidth for maximum space—for article mode
- **\textbytext** (non-starred): Uses normal column width—works in Beamer presentations

### CRITICAL - Beamer Compatibility

- `\textbytext*` (starred) does NOT work inside `\begin{frame}...\end{frame}`, even with `[fragile]`
- **Solution**: Use `\mode<presentation>` and `\mode<article>` to split:
  - Presentation mode: `\textbytext` (non-starred)
  - Article mode: `\textbytext*` (starred, fullwidth)

### Example (Beamer-compatible with Mode Splits)

```latex
\begin{frame}
  \mode<presentation>{%
    \textbytext{%
      \begin{definition}[Primärminne]
        Datorns arbetsminne där exekverande program lagras.
        Flyktigt minne med snabb åtkomst (nanosekunder).
      \end{definition}
    }{%
      \begin{definition}[Sekundärminne]
        Oflyktigt minne där filer lagras.
        Långsammare åtkomst (mikro- till millisekunder).
      \end{definition}
    }
  }
  \mode<article>{%
    \textbytext*{%
      \begin{definition}[Primärminne]
        Datorns arbetsminne där exekverande program lagras.
        Flyktigt minne med snabb åtkomst (nanosekunder).
      \end{definition}
    }{%
      \begin{definition}[Sekundärminne]
        Oflyktigt minne där filer lagras.
        Långsammare åtkomst (mikro- till millisekunder).
      \end{definition}
    }
  }
\end{frame}

\ltnote{%
  Relevanta lärandemål:
  \cref{FilesLOPersistence}

  \textbf{Variationsmönster}: Kontrast (spatial, inte temporal)

  Side-by-side layout skapar omedelbar visuell kontrast mellan flyktigt/oflyktigt,
  snabbt/långsamt. Studenter kan scanna fram och tillbaka mellan definitionerna
  vilket gör de kontrasterande aspekterna urskiljbara.
}
```

### When to Use

- Concepts defined in relation to each other (primärminne/sekundärminne)
- Creating simultaneous contrast in variation theory
- Comparing two approaches side-by-side (manual vs automatic)

**Works with:** definition, example, remark, block, any semantic environment

**For article-only documents** (not using Beamer), you can use `\textbytext*` directly without mode splits.

---

## Figures and Tables with sidecaption

### Principle

Images and tables should use memoir's sidecaption for better layout and accessibility.

### For Figures

```latex
\begin{frame}
  \begin{figure}
    \begin{sidecaption}{Clear description of image content}[fig:label]
      \includegraphics[width=0.7\textwidth]{path/to/image}
    \end{sidecaption}
  \end{figure}
\end{frame>
```

### For Tables

```latex
\begin{frame}
  \begin{table}
    \begin{sidecaption}{Description of table contents}[tab:label]
      \begin{tabular}{ll}
        ... table content ...
      \end{tabular}
    \end{sidecaption}
  \end{table}
\end{frame}
```

### Benefits

- Caption alongside content (better use of horizontal space)
- Improved accessibility (screen readers)
- Context provided in notes/handouts

### Caption Guidelines

- **Describe content**: "Python documentation for file I/O operations"
- **Be specific**: "File modes available in open() function" not "Documentation screenshot"
- **Explain relevance**: "CSV module methods showing reader and writer classes"

### Anti-pattern (Standalone Image Without Caption)

```latex
% BAD: No context or caption
\begin{frame}
  \includegraphics[width=\columnwidth]{docs-files.png}
\end{frame>
```

---

## Toggling Notes for Different Audiences

Notes can be hidden or shown depending on the audience:

```latex
% In instructor version (notes visible)
\ltnoteon  % This is the default

% In student version (notes hidden)
\ltnoteoff
```

### Use Cases

- **Students**: Hide notes to avoid distraction
- **Instructors**: Show notes to understand pedagogical design
- **Co-authors**: Show notes during material development
- **Researchers**: Show notes when analyzing instructional design
