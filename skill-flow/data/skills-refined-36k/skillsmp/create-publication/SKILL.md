---
name: create-publication
description: Create a new publication post for the Jekyll academic website from a paper URL or metadata
---

## What I do

Create publication posts in the `_publications/` directory for this Jekyll academic website. Each publication is a Markdown file with YAML frontmatter containing metadata about the paper.

## File location

Create files in `_publications/` with a descriptive kebab-case filename (e.g., `vibe-coding.md`, `expat.md`).

## Required frontmatter fields

```yaml
---
cite: |-
  Author1, FirstName, Author2, FirstName, ... Year. "Title." Journal/Working Paper. DOI-or-URL
links:
  - text: "Full text"
    url: "https://..."
  - text: "PDF"
    url: "https://..."
statement: ""
team:
  - "author-username"  # from _data/team.csv
grants:
  - grant-id  # from _data/grants.yaml
title: "Paper Title"
date: "YYYY-MM-DD"
tags:
  - working  # or: published
  - macromanagers  # optional: for papers linked to macromanagers.eu
description: "Abstract text"
---
```

## Tags

Publications should have at least one status tag:
- `working` - Working papers, preprints, or under review
- `published` - Published in a journal or conference

Optional tags:
- `macromanagers` - Papers that should be featured on macromanagers.eu (typically related to the ERC Advanced Grant MACROMGR project)

## Body content

After the frontmatter, include the abstract as plain text (same as description field).

## Data sources

### Team members (`_data/team.csv`)
CSV with columns: username, name, affiliation, title, url, image
Use the `username` field in the `team` array.

### Grants (`_data/grants.yaml`)
Available grant IDs include:
- `erc-starting-2012` - ERC Starting Grant KNOWLEDGEFLOWS (313164)
- `erc-advanced-2022` - ERC Advanced Grant MACROMGR (101097789)
- `elvonal` - Hungarian NKFIH (144193)
- `rethink` - Horizon 2020 RETHINK-GSC (101061123)
- `respect` - Horizon 2020 RESPECT (770680)

## Citation format

For arXiv papers:
```
Author, First, Author2, First2. Year. "Title." arXiv:XXXX.XXXXX. https://doi.org/10.48550/arXiv.XXXX.XXXXX
```

For journal articles:
```
Author, First, Author2, First2. Year. "Title." Journal Name Volume(Issue): Pages. https://doi.org/...
```

For working papers:
```
Author, First, Author2, First2. Year. "Title." Working Paper.
```

## Workflow

1. Fetch paper metadata from provided URL (arXiv, journal page, etc.)
2. Extract: title, authors, abstract, date, DOI
3. Look up funding acknowledgements in the paper
4. Match authors to team members in `_data/team.csv`
5. Match grants to `_data/grants.yaml`
6. Create the publication file with all metadata

## Example

```yaml
---
cite: |-
  Koren, Miklós, Gábor Békés, Julian Hinz and Aaron Lohmann. 2026. "Vibe Coding Kills Open Source." arXiv:2601.15494. https://doi.org/10.48550/arXiv.2601.15494
links:
  - text: "Full text"
    url: "https://arxiv.org/abs/2601.15494"
  - text: "PDF"
    url: "https://arxiv.org/pdf/2601.15494"
statement: ""
team:
  - "koren"
  - "bekes"
  - "hinz"
  - "lohmann"
grants:
  - erc-advanced-2022
  - elvonal
title: "Vibe Coding Kills Open Source"
date: "2026-01-21"
tags:
  - working
description: "Abstract text here..."
---

Abstract text here...
```
