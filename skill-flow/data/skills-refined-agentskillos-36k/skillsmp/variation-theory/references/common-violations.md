# Common Variation Theory Violations

This reference documents common violations of variation theory principles in educational materials, with detailed examples and fixes.

## Table of Contents

1. [Why Generalization-Before-Example Is Harmful](#why-generalization-before-example-is-harmful)
2. [Violation Types](#violation-types)
3. [How to Review for Violations](#how-to-review-for-violations)

---

## Why Generalization-Before-Example Is Harmful

**CRITICAL**: When generalizations precede examples, students cannot discern the pattern because they haven't experienced the necessary variation.

### Problems

1. **No experiential basis**: Students receive abstract principles with no concrete variation to map them onto
2. **Meaningless abstractions**: Without experiencing variation, generalizations remain empty words
3. **Missed learning opportunity**: The discernment that should happen through variation is bypassed
4. **Backwards pedagogy**: Violates the fundamental principle that variation enables discernment

**Remember**: You cannot discern an invariant pattern without first experiencing variation in that dimension.

---

## Violation Types

### Type 1: Generic/Placeholder Code Before Concrete Examples

**Problem**: Showing abstract code with placeholder values (like `"filename"`, `transformera()`) before concrete working examples.

**Why it's harmful**: The generic code is itself a generalization. Students need to see real, working code with actual filenames and functions before the pattern can be abstracted.

**BAD:**
```latex
% Abstract code with placeholders first
\begin{frame}[fragile]
  \begin{minted}{python}
file = open("filename", "r")
print(file.read())
file.close()
  \end{minted}
\end{frame}

% Then concrete example
\begin{frame}[fragile]
  \begin{example}[open_close.py]
    \inputminted{python}{examples/open_close.py}
  \end{example}
\end{frame}
```

**GOOD:**
```latex
% Concrete example first
\begin{frame}[fragile]
  \begin{example}[open_close.py]
    Manuell filhantering med open() och close():
    \inputminted{python}{examples/open_close.py}
  \end{example}
\end{frame}

% Optional: Pattern summary AFTER if needed
\begin{frame}
  \begin{remark}[Filhanteringsmönster]
    All filläsning följer mönstret: open(filnamn, läge) → read() → close()
  \end{remark}
\end{frame}
```

---

### Type 2: Block/Remark Environments Before Examples

**Problem**: Using semantic environments (block, remark, definition) to state principles before showing examples that demonstrate those principles.

**Why it's harmful**: The semantic environment signals "this is important," but students have no context to understand WHY it's important or WHAT it means.

**BAD:**
```latex
% Principle stated first
\begin{frame}
  \begin{block}{Filer}
    Vi har alla erfarenhet av filer. Python-program är också filer.
  \end{block}

  \begin{example}[Pythonprogram]
    Filer med .py-ändelse innehåller Python-kod...
  \end{example}

  \begin{example}[Bilder]
    Filer med .jpg eller .png innehåller bilddata...
  \end{example}
\end{frame}
```

**GOOD:**
```latex
% Examples create variation first
\begin{frame}
  \begin{example}[Pythonprogram]
    Filer med .py-ändelse innehåller Python-kod...
  \end{example}

  \pause

  \begin{example}[Bilder]
    Filer med .jpg eller .png innehåller bilddata...
  \end{example}

  \pause

  \begin{example}[Dokument]
    Filer med .pdf eller .docx innehåller textdokument...
  \end{example}

  % Optional synthesis AFTER examples
  \pause

  \begin{block}{Mönstret}
    Filer lagrar olika typer av data. Ändelsen indikerar innehållstyp.
  \end{block}
\end{frame}
```

---

### Type 3: Incomplete Skeletons Before Complete Solutions

**Problem**: Showing incomplete code scaffolding with comments like `# TODO` or `# Uppdatera räknaren` before showing complete working implementations.

**Why it's harmful**: The skeleton IS a generalization (the structure without the details). Students need to see complete solutions before the general structure becomes discernible.

**BAD:**
```latex
% Incomplete skeleton first
\begin{frame}[fragile]
  \begin{example}[Ordräkning --- grundstruktur]
    \begin{minted}{python}
def räkna_ord(text):
    ord_antal = {}
    for rad in text.split("\n"):
        for ord in rad.split(" "):
            # Uppdatera räknaren
    return ord_antal
    \end{minted}
  \end{example}
\end{frame}

% Then complete solutions
\begin{frame}[fragile]
  \begin{example}[Uppdatera räknaren --- try-except]
    \begin{minted}{python}
try:
    ord_antal[ord] += 1
except KeyError:
    ord_antal[ord] = 1
    \end{minted}
  \end{example}
\end{frame}
```

**GOOD:**
```latex
% Complete solution first
\begin{frame}[fragile]
  \begin{example}[Ordräkning med try-except]
    \begin{minted}{python}
def räkna_ord(text):
    ord_antal = {}
    for rad in text.split("\n"):
        for ord in rad.split(" "):
            try:
                ord_antal[ord] += 1
            except KeyError:
                ord_antal[ord] = 1
    return ord_antal
    \end{minted}
  \end{example}
\end{frame}

% Alternative complete solution
\begin{frame}[fragile]
  \begin{example}[Ordräkning med if-kontroll]
    \begin{minted}{python}
def räkna_ord(text):
    ord_antal = {}
    for rad in text.split("\n"):
        for ord in rad.split(" "):
            if ord not in ord_antal:
                ord_antal[ord] = 1
            else:
                ord_antal[ord] += 1
    return ord_antal
    \end{minted}
  \end{example}
\end{frame}

% NOW students can see the pattern
\begin{frame}
  \begin{remark}[Mönstret]
    Båda lösningarna följer samma grundstruktur: iterera över enheter,
    kontrollera om nyckel finns, uppdatera eller initiera värde.
  \end{remark>
\end{frame>
```

---

### Type 4: Explanatory Principles Before Demonstrating Examples

**Problem**: Explaining how something works or why it's needed before showing concrete examples where it solves a real problem.

**Why it's harmful**: Abstract explanations lack meaning without concrete context. Students can't appreciate "why" without first experiencing the problem.

**BAD:**
```latex
% Explanation first
\begin{frame}[fragile]
  \begin{remark}
    Att läsa från filer utan att känna till strukturen är som att gå i
    bäcksvarta mörkret --- vi måste veta exakt var alla saker finns.
  \end{remark>
\end{frame}

% Then example
\begin{frame}
  \begin{activity}[SCB]
    Ladda ner SCB:s namnstatistik och skriv ett program som söker namn.
  \end{activity}
\end{frame>
```

**GOOD:**
```latex
% Problem/activity first - students experience the difficulty
\begin{frame}
  \begin{activity}[SCB]
    Ladda ner SCB:s namnstatistik och skriv ett program som söker namn.

    Hur vet du var i filen namnen finns? Hur vet du var antalet börjar?
  \end{activity}
\end{frame}

% AFTER students have wrestled with the problem, articulate it
\begin{frame}
  \begin{remark}[Varför filformat behövs]
    Utan överenskommen struktur är filen meningslös --- vi vet inte var
    information finns. Filformat löser detta genom att definiera WHERE
    varje dataelement finns.
  \end{remark>
\end{frame>
```

---

## How to Review for Violations

### Checklist

When reviewing educational materials, check for:

- [ ] Does generic/abstract code appear before concrete examples?
- [ ] Do block/remark/definition environments state principles before examples demonstrate them?
- [ ] Are incomplete code skeletons shown before complete working solutions?
- [ ] Are explanations of "why" or "how" given before students experience the problem?
- [ ] Do file modes (r/w/a) get explained before examples show their use?
- [ ] Are categorizations (text vs binary) stated before contrasting examples?

### Fix Pattern

For each violation found:

1. **Remove** the generalization from its current position
2. **Ensure** 2-3 concrete examples exist creating necessary variation
3. **Add back** the generalization AFTER examples (in semantic environment if appropriate)
4. **Verify** students can now discern the pattern from the variation

**Remember**: Every generalization should answer the implicit question: "What invariant pattern do these examples share?"
