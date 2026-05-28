# LaTeX Examples for Variation Theory

This reference provides detailed LaTeX code examples demonstrating variation theory patterns in educational materials.

## Table of Contents

1. [Side-by-Side Contrast with \textbytext*](#side-by-side-contrast-with-textbytext)
2. [Generalizations in Semantic Environments](#generalizations-in-semantic-environments)
3. [Documenting Variation Patterns](#documenting-variation-patterns)

---

## Side-by-Side Contrast with \textbytext*

### Purpose

Create simultaneous visual contrast when two concepts need immediate comparison. This implements the Contrast pattern spatially rather than temporally.

### When to Use

Concepts that are defined **in relation to each other** and whose critical aspects are best understood through direct juxtaposition.

### Tool

LaTeX didactic.sty provides `\textbytext*{...}{...}` to place environments side-by-side:
- **Starred version** (`\textbytext*`): Uses fullwidth for maximum space
- **Non-starred** (`\textbytext`): Uses normal column width

### IMPORTANT - Beamer Compatibility

- `\textbytext*` (starred) does NOT work inside `\begin{frame}...\end{frame}`, even with `[fragile]`
- **Solution**: Use mode-specific versions:
  - `\mode<presentation>` with `\textbytext` (non-starred)
  - `\mode<article>` with `\textbytext*` (starred, fullwidth)

### Example: Primärminne vs Sekundärminne

```latex
\begin{frame}
  \mode<presentation>{%
    \textbytext{%
      \begin{definition}[Primärminne]
        Datorns arbetsminne där exekverande program lagras.
        Detta är flyktigt minne med mycket snabb åtkomst
        (storleksordning nanosekunder).
      \end{definition}
    }{%
      \begin{definition}[Sekundärminne]
        Oflyktigt minne där icke-exekverande program och
        data (filer) lagras. Långsammare åtkomst än primärminne
        (storleksordning mikro- till millisekunder).
      \end{definition}
    }
  }
  \mode<article>{%
    \textbytext*{%
      \begin{definition}[Primärminne]
        Datorns arbetsminne där exekverande program lagras.
        Detta är flyktigt minne med mycket snabb åtkomst
        (storleksordning nanosekunder).
      \end{definition}
    }{%
      \begin{definition}[Sekundärminne]
        Oflyktigt minne där icke-exekverande program och
        data (filer) lagras. Långsammare åtkomst än primärminne
        (storleksordning mikro- till millisekunder).
      \end{definition}
    }
  }
\end{frame}
```

### Variation Pattern Analysis

- **What varies**: Memory type (primary vs secondary) and all associated characteristics
- **What remains invariant**: The concept of computer memory storing data
- **Critical aspects made discernible**: Volatility (flyktigt/oflyktigt), speed (nanosekunder/millisekunder), purpose (executing/stored programs)

### Why This Works

Side-by-side presentation allows students to scan back and forth between the definitions, making the contrasting features immediately apparent. The spatial arrangement reinforces the conceptual opposition.

### For Article-Only Documents

You can use `\textbytext*` directly without mode splits:

```latex
\textbytext*{%
  \begin{definition}[Primärminne]
    ...
  \end{definition}
}{%
  \begin{definition}[Sekundärminne]
    ...
  \end{definition}
}
```

---

## Generalizations in Semantic Environments

### Principle

When generalizing from examples, capture the generalization in a semantic environment (definition, remark, block) placed AFTER the examples.

### Environment Selection

| Environment | Use for |
|-------------|---------|
| `definition` | Formal concept definitions |
| `remark` | Important observations, principles, implications |
| `block` | Key takeaways, summaries, synthesis points |
| `example` | When generalization is best shown through code pattern |

### Anti-pattern: Buried in Prose

```latex
% BAD: Important principle lost in prose
När vi arbetar med filer måste vi alltid öppna dem först,
sedan arbeta med innehållet, och till sist stänga dem.
Detta mönster återkommer i all filhantering.

\begin{example}[Läsa fil]
  ...
\end{example}
```

### Good Pattern: Highlighted in Environment

```latex
% GOOD: Examples first, then generalization in environment
\begin{example}[Läsa fil]
  with open("data.txt", "r") as fil:
      innehåll = fil.read()
\end{example}

\begin{example}[Skriva fil]
  with open("data.txt", "w") as fil:
      fil.write(text)
\end{example}

\begin{remark}[Filhanteringsmönster]
  All filhantering följer mönstret: öppna → bearbeta → stäng.
  Funktionen \mintinline{python}{with} garanterar att filen stängs
  automatiskt även om fel uppstår.
\end{remark}
```

### Integration with Variation Theory

The semantic environment containing the generalization represents the discernible **invariant pattern** that emerged from the **variation** in the examples.

---

## Documenting Variation Patterns

### Language Consistency

**CRITICAL**: Match the language of variation theory annotations to the document's instructional language.

### Swedish Terminology

| English | Swedish |
|---------|---------|
| Variation Pattern | Variationsmönster |
| Contrast | Kontrast |
| Generalization | Generalisering |
| Fusion | Fusion |
| What varies | Vad som varierar |
| What remains invariant | Vad som hålls invariant |
| Critical aspects to discern | Kritiska aspekter att urskilja |
| Learning Objectives | Lärandemål |

### Example: Swedish Documentation

```latex
\ltnote{%
  \textbf{Variationsmönster}: Kontrast

  \textbf{Vad som varierar}: Implementeringsmetod (dict-baserad vs klassbaserad)

  \textbf{Vad som hålls invariant}: Problemet (telefonbokshantering) och
  funktionaliteten

  \textbf{Kritiska aspekter att urskilja}: Genom att se samma problem
  löst både med och utan klasser kan studenter urskilja vad en klass ÄR
  kontra vad den INTE är.

  \textbf{Varför denna variation fungerar}: Enligt Marton \& Pang (2006)
  varierar vi implementeringsmetoden medan vi håller problemet invariant.
}
```

### Example: English Documentation

```latex
\ltnote{%
  \textbf{Variation Pattern}: Contrast

  \textbf{What varies}: Implementation approach (dict-based vs class-based)

  \textbf{What remains invariant}: The problem domain and functionality

  \textbf{Critical aspects to discern}: By seeing the same problem solved
  with and without classes, students can discern what a class IS versus
  what it is NOT.

  \textbf{Why this variation works}: Following Marton \& Pang (2006), we
  vary the implementation approach while keeping the problem invariant...
}
```
