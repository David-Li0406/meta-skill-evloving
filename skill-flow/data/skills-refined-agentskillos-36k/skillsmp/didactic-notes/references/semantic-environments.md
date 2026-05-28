# Semantic Environments in Didactic Materials

This reference describes how to use semantic environments effectively in educational LaTeX materials.

## Table of Contents

1. [Available Environments](#available-environments)
2. [Environment Selection Guide](#environment-selection-guide)
3. [Generalizations in Semantic Environments](#generalizations-in-semantic-environments)
4. [Cross-References](#cross-references)
5. [Integration with \ltnote](#integration-with-ltnote)

---

## Available Environments

The `didactic` package provides semantic environments that pair well with `\ltnote`:

| Environment | Purpose | Use for |
|-------------|---------|---------|
| `activity` | Active learning tasks | Tasks requiring student engagement |
| `exercise` | Practice problems | Structured problems with solutions |
| `question` | Discussion questions | Open-ended thinking prompts |
| `remark` | Side notes for students | Important observations, principles |
| `summary` | Section summaries | Consolidation of key points |
| `definition` | Formal definitions | Mathematical and conceptual definitions |
| `theorem` | Mathematical theorems | Formal statements requiring proof |
| `example` | Illustrative examples | Code samples, worked examples |
| `block` | Key takeaways | Highlights, synthesis points |

---

## Environment Selection Guide

When choosing an environment, consider the pedagogical purpose:

### For Formal Concept Definitions

Use **definition**:
```latex
\begin{definition}[Fil]
  En fil är en namngiven samling data som lagras i sekundärminnet.
\end{definition}
```

### For Important Observations and Principles

Use **remark**:
```latex
\begin{remark}[Filhanteringsmönster]
  All filhantering följer mönstret: öppna → bearbeta → stäng.
  Funktionen \mintinline{python}{with} garanterar att filen stängs
  automatiskt även om fel uppstår.
\end{remark}
```

### For Key Takeaways and Summaries

Use **block**:
```latex
\begin{block}{Återkommande mönster}
  \begin{itemize}
    \item Validera input
    \item Dict för räkning
    \item Läs-bearbeta-skriv
  \end{itemize}
\end{block}
```

### For Code Patterns and Demonstrations

Use **example**:
```latex
\begin{example}[Läsa fil]
  with open("data.txt", "r") as fil:
      innehåll = fil.read()
\end{example>
```

### For Student Activities

Use **activity**:
```latex
\begin{activity}
  Try implementing this function before reading further.
\end{activity>
```

---

## Generalizations in Semantic Environments

### Principle

When generalizing from examples, capture the generalization in a semantic environment placed AFTER the examples.

### Why Use Semantic Environments for Generalizations

1. **Highlights importance**: Visual distinction signals "this is a key takeaway"
2. **Makes referenceable**: Can be cited in pedagogical notes and student materials
3. **Suitable for notes**: Environments appear cleanly in article mode/handouts
4. **Searchable**: Students can scan for definitions/remarks when reviewing

### Integration with Variation Theory

The semantic environment containing the generalization represents the discernible **invariant pattern** that emerged from the **variation** in the examples.

### Anti-pattern: Generalizations Buried in Prose

```latex
% BAD: Important principle lost in prose
När vi arbetar med filer måste vi alltid öppna dem först,
sedan arbeta med innehållet, och till sist stänga dem.
Detta mönster återkommer i all filhantering.

\begin{example}[Läsa fil]
  ...
\end{example}
```

### Good Pattern: Generalization Highlighted

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

---

## Cross-References

Use `\label` and `\cref` to reference activities in notes:

```latex
\begin{activity}\label{FirstAttempt}
  What do you think this function does?
\end{activity}

\ltnote{%
  The purpose of \cref{FirstAttempt} is to activate prior knowledge
  before we formally define the concept.
}
```

### Referencing Multiple Environments

```latex
\begin{example}\label{ex:read}
  Reading from a file...
\end{example}

\begin{example}\label{ex:write}
  Writing to a file...
\end{example}

\ltnote{%
  \cref{ex:read,ex:write} demonstrate the generalization pattern
  that students should discern: both operations follow the same
  open-process-close structure.
}
```

---

## Integration with \ltnote

### Pattern: Activity with Pedagogical Note

```latex
\begin{activity}
  Try implementing this function before reading further.
\end{activity}

\ltnote{%
  This activity uses try-first pedagogy to engage students before
  providing the solution.
}
```

### Pattern: Example with Variation Theory Note

```latex
\begin{example}[Läsa fil]
  with open("data.txt", "r") as fil:
      innehåll = fil.read()
\end{example}

\ltnote{%
  Relevanta lärandemål:
  \cref{FilesLOOperations}

  \textbf{Variationsmönster}: Kontrast

  Vi visar först läsning, sedan skrivning. Invariant: filhanteringsmönstret.
  Varierar: operationsriktningen.
}
```

### Pattern: Definition with Critical Aspects

```latex
\begin{definition}[Fil]
  En fil är en namngiven samling data som lagras i sekundärminnet.
\end{definition}

\ltnote{%
  \textbf{Kritiska aspekter att urskilja}:
  \begin{itemize}
    \item \textbf{Namngiven}: Filer identifieras med namn (sökvägar)
    \item \textbf{Sekundärminne}: Persistent lagring (överlever avstängning)
    \item \textbf{Samling data}: Strukturerad information, inte slumpmässiga bytes
  \end{itemize}
}
```

### Pattern: Documenting Assessment Purpose

```latex
\begin{question}\label{q:prior}
  What do you think "file system" means?
\end{question}

\ltnote{%
  We want to investigate how many students have heard of this concept.
  This will give us baseline statistics and help understand the
  correctness of answers in \cref{FollowUpActivity}.
}
```

### Pattern: Explaining Omissions

```latex
\begin{remark}[Grundläggande modell]
  Vi arbetar med textfiler i detta avsnitt.
\end{remark}

\ltnote{%
  We deliberately omit binary files here to avoid cognitive overload.
  Students should first grasp text file handling before encountering
  the additional complexity of binary modes.
}
```
