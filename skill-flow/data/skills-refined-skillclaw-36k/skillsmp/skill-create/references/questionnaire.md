# skill questionnaire

use these prompts to design a new skill before scaffolding.

## skill brief template

| field | target | notes |
|-------|--------|-------|
| name | kebab-case | becomes folder name |
| description | "This skill should be used when..." | include triggers |
| triggers | 3-6 phrases | match user language |
| anti-triggers | 2-4 phrases | avoid misfires |
| archetype | workflow/tool/domain/hybrid | use decision tree |
| complexity | simple/medium/full | based on thresholds |
| inputs | paths, APIs, artifacts | name exact locations |
| outputs | files, summaries, commands | define success |
| references | 2-6 files | each >= 50 lines |
| scripts | 0-4 helpers | for repeated commands |
| assets | 0-3 templates | sample inputs/outputs |
| tools | 2+ command examples | for integration |
| verification | commands + artifacts | prove success |
| in scope | 3-5 bullets | what is covered |
| out of scope | 3-5 bullets | what is excluded |

## general intake

- what problem does the skill solve and who uses it?
- what triggers should activate it (exact phrases)?
- what should NOT trigger it (anti-triggers)?
- what inputs are required (paths, APIs, credentials)?
- what outputs should exist when done (files, commands, decisions)?
- what must be validated (tests, scripts, artifacts)?

## archetype selection prompts

| question | yes → | no → |
|----------|-------|------|
| 3+ ordered steps or 2+ gates? | workflow | → |
| deterministic input → output in <= 2 steps? | tool | → |
| 3+ docs/policies or FAQ lookup? | domain | → |
| 2+ archetypes apply? | hybrid | pick primary |

## complexity sizing prompts

| signal | yes → | no → |
|--------|-------|------|
| 6+ trigger phrases? | medium+ | simple |
| 2+ archetypes apply? | full-featured | medium |
| 3+ external tools referenced? | full-featured | medium |
| domain expertise required? | full-featured | medium |

## workflow archetype prompts

- list numbered steps with inputs/outputs per step
- identify checkpoints (approval, tests, validation)
- note gates that must pass before proceeding
- define "done" artifacts and commands

## tool archetype prompts

- what are the supported formats/endpoints?
- list constraints (size, schema, rate limits)
- what deterministic script runs the core action?
- what artifact validates the output?

## domain archetype prompts

- what knowledge areas are in scope?
- what docs must be loaded together?
- what is the lookup workflow?
- what FAQs must be surfaced first?

## tool integration prompts

- which commands must be shown as examples (2+)?
- what repeated commands should become scripts?
- what external CLIs are required or optional?

## validation + artifacts

- what command confirms success?
- what file or output proves completion?
- what warnings should block completion?

## naming + voice

- is the name unique and descriptive?
- is the description third-person with triggers?
- are headers lowercase (except acronyms)?

## anti-pattern prompts

- where might this skill be misused?
- what common mistakes should be prevented?
- what is the fix for each mistake?
