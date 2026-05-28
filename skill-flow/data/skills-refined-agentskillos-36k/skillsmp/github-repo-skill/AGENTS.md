# AGENTS.md for cmm-ai-automation

AI-assisted automation for Critical Mineral Metabolism (CMM) data curation using LinkML, OBO Foundry tools, and Google Sheets integration.

## Repo management

This repo uses `uv` for managing dependencies. Never use commands like `pip` to add or manage dependencies.
`uv run` is the best way to run things, unless you are using `justfile` targets.

`mkdocs` is used for documentation.

`just` is used for build recipes. Run `just` or `just --list` to see available commands.

## Project structure

- `src/cmm_ai_automation/schema/` - LinkML schema (edit this)
- `src/cmm_ai_automation/datamodel/` - Generated Python datamodel (do not edit)
- `project/` - Generated project files (do not edit)
- `tests/` - Python tests
- `docs/` - mkdocs-managed documentation

## Key dependencies

- LinkML for schema-driven data modeling
- gspread for Google Sheets integration
- Click for CLI (typer also acceptable per bbop-skills)

## Testing

Run tests with:
```bash
just test
# or
uv run pytest
```

Use `@pytest.mark.integration` for tests that depend on external APIs (Google Sheets, etc).

## CLI

The package provides CLI commands via Click:
- `download-sheets` - Download Google Sheets tabs as TSV

## Related repositories

- [CultureBotAI/CMM-AI](https://github.com/CultureBotAI/CMM-AI) - Collaborating project for AI-driven CMM discovery
- [Knowledge-Graph-Hub/kg-microbe](https://github.com/Knowledge-Graph-Hub/kg-microbe) - Microbial knowledge graph
- [berkeleybop/metpo](https://github.com/berkeleybop/metpo) - Microbial Phenotype Ontology

## Skills

This repo follows [berkeleybop/bbop-skills](https://github.com/berkeleybop/bbop-skills) best practices.

**IMPORTANT**: Read [SKILL.md](SKILL.md) for the complete BBOP github-repo-skill guidelines on engineering practices, testing, CLI conventions, documentation, and more.
