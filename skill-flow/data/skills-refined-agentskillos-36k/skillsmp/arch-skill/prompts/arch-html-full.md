---
description: "16) Arch HTML (full fidelity): render doc with zero omissions."
argument-hint: <doc path or guidance>
---
# /prompts:arch-html-full — $ARGUMENTS
Execution rule: do not block on unrelated dirty files in git; ignore unrecognized changes. If committing, stage only files you touched (or as instructed).
Do not preface with a plan or restate these instructions. Begin work immediately. If a tool-call preamble is required by system policy, keep it to a single terse line with no step list. Console output must ONLY use the specified format; no extra narrative.

Goal: Generate a clean, static HTML view of an architecture doc using the framework in
`~/.codex/templates/arch_skill/arch_doc_template.html`, with ZERO omissions (every line of source content must appear somewhere).

1) Resolve DOC_PATH:
# COMMUNICATING WITH AMIR (IMPORTANT)

- Start console output with a 1 line reminder of our North Star.
- Then give the punch line in plain English.
- Then give me bulleted data (3-10 bullets). If I want more data, I'll ask.
- Never be pedantic. Assume shorthand is intentional (long day); optimize for the real goal.
- Put deep details (commands, logs, exhaustive lists) in DOC_PATH / WORKLOG_PATH, not in console output.

   - If $ARGUMENTS includes a docs/<...>.md path, use it.
   - Otherwise infer the most relevant arch doc from $ARGUMENTS + conversation.
   - If ambiguous, ask the user to choose from the top 2–3 candidates.

2) Use a subagent (Codex CLI) to produce HTML and write it to disk:
   - Profile: yolo (gpt-5.2-codex, xhigh, full access)
   - The subagent must:
     - Read DOC_PATH fully.
     - Read `~/.codex/templates/arch_skill/arch_doc_template.html` and follow its structure.
     - Compute WORKLOG_PATH as `<DOC_BASENAME>_WORKLOG.md` in the same directory as DOC_PATH and fill the {{WORKLOG_PATH}} placeholder.
     - Produce a static HTML file (no React/JS interactivity).
     - Preserve full content with ZERO omissions.
     - If any text does not fit a section, include it in a final “Unclassified content” block.
     - Append a final “Full Source (verbatim)” appendix that includes the entire doc inside a <pre>.
     - Write the HTML to: `docs/prototypes/<DOC_BASENAME>_full.html` (relative to repo root).
     - After writing, print ONLY the output path to stdout.

   Command:
   `codex exec -c profile="yolo" "<SUBAGENT_PROMPT>"`

3) Write output to:
   `docs/prototypes/<DOC_BASENAME>_full.html`
4) Open in Chrome.

OUTPUT FORMAT (console only; Amir-style):
<1 line north star reminder>
<1 line punchline (HTML rendered or blocked)>
- Doc: <path>
- Output: <path>
- Notes: <any important caveat>
- Next: <what to do next>
