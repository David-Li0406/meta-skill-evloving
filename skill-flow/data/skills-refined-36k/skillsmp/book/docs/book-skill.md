# Book skill

## Purpose

To write a book in markdown, built up from parts, chapters, sections, subsections, etc. Optionally, translate it into latex.

## Commands

Commands

- Initialise
  - {template} which template to use
  - {use-parts} whether parts should be used or not. Defaults to true.
  - {install cli} whether to install the booktool cli
- New chapter
  - {where} specify where the new chapter will be created
  - {prompt} specify what the new chapter will be about in the prompt
- latex
  - {action} compile or translate, default value is compile
  - {chapter} path to chapter, if not set do the action for the whole book
  - create main run the

## Structure

A book follows a pre-made structure:

- src
  - md
    - 100-frontmatter
      - docs
      - figures
      - references
      - frontmatter.md
    - 2XX-part-name-of-part
      - XX-ch-name-of-chapter
        - docs
        - figures
        - references
        - chXX-name-of-chapter.md
        - secXX-name-of-section.md
    - 3XX-appendix
      - docs
      - figures
      - references
      - appXX.md
    - 400-backmatter
      - docs
      - figures
      - references
      - backmatter.md
    - config.yaml
    - outline.md
    - main.md

Variants:
    ⁃    skip parts, only use chapters - use a variable to toggle parts on and off

Comments
    ⁃    config.yaml contains all the configuration parameters for the project
    ⁃    frontmatter.md - contains all the frontmatter parts like coverpage, colophone, toc, preface etc
    ⁃    backmatter.mf - contains all the backmatter parts like bibliography, list of figures, index, etc
    ⁃    docs-folder contains any non-scientific source used for the content creation
    ⁃    references-folder contains all scientific sources used in the parent folder.. Each has a summary file: `<name-of-source>`-summary.md and optionally an exact source file, saved as `<name-of-source>`-source.md. In addition, there is a references.bib file, holding the shortcut references, used to cite the references:
    ⁃    references
    ⁃    references.bib
    ⁃    `<name-of-source>`-source.md
    ⁃    `<name-of-source>`-summary.md

How to create main.md

Run a script: create-main.py

    ⁃    concatenates from top to bottom

    ◦    Add language to the skill - this is the language the book is written in
    ◦    Template - this is the template of the book uses to create the book

## PK-rutine

1. Nytt kapittel 2 (første iterasjon)
   1. Si hva det dreier seg om - les de 11 områdene - lag kap 2 ihh skill
   2. SKILL
   3. Som i kap 1
   4. Tilsvarende kap 2
2. Endringsprosess (iterativ)
   1. Leser gjennom selv
   2. Halvside per halvside
   3. Tar gjerne bilde og påpeker endring
   4. Dette tar tid
   5. Fagterm - punchline - forklaring - må si ifra
3. Referanser legge til til SLUTT
   1. Vanlige referanser i tekst som skal bakerst
   2. Spesifikke anbefalte referanser som er relevant til slutt i kapittelet
   3. PK. Sjekker at linkene eksisterer
   4. BIB fikser AI ihht APA 7
