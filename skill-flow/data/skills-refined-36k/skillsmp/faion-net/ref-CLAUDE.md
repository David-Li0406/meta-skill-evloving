# References Folder

Domain-specific reference documentation for the Faion Network orchestrator skill.

## Overview

This folder contains detailed documentation for workflow processes, directory structure, quality assurance practices, and all 9 knowledge domains with their agents, skills, and methodologies.

## Files

### Workflow and Structure

| File | Description |
|------|-------------|
| `workflow.md` | SDD workflow phases from idea discovery through feature completion. Covers project selection, new project bootstrap, feature selection, grooming, execution, and completion. |
| `directory-structure.md` | SDD folder layout (`.aidocs/`). Defines constitution, roadmap, product_docs, tasks, and features lifecycle (backlog -> todo -> in-progress -> done). |
| `quality-assurance.md` | Confidence checks before each phase, hallucination prevention checklist, and reflexion learning for storing patterns/mistakes in `~/.sdd/memory/`. |

### Domain Reference Files

| File | Domain | Key Content |
|------|--------|-------------|
| `sdd-domain.md` | Specification-Driven Development | 7 agents (task-executor, task-creator, spec-reviewer, design-reviewer, impl-plan-reviewer, tasks-reviewer, hallucination-checker). 8 methodologies covering SDD workflow. |
| `research-domain.md` | Research | 10 agents (idea-generator, market-researcher, competitor-analyzer, persona-builder, pricing-researcher, problem-validator, niche-evaluator, pain-point-researcher, name-generator, domain-checker). 20 methodologies covering research activities. |
| `product-domain.md` | Product Management | 6 agents (mvp-scope-analyzer, mlp-spec-analyzer, mlp-gap-finder, mlp-spec-updater, mlp-feature-proposer, mlp-impl-planner). 18 methodologies covering product management. |
| `development-domain.md` | Software Development | 6 agents (code, test, devops, browser, api, api-designer). 10 technical skills (Python, JS, backend, API, testing, AWS, K8s, Terraform, Docker, browser automation). 68 methodologies covering Python, JavaScript, backend languages, DevOps. |
| `marketing-domain.md` | Marketing | 5 agents (ads, content, social, email, seo). 4 technical skills (Google Ads, Meta Ads, SEO, Analytics). 72 methodologies across GTM, landing pages, content, SEO, paid ads, email. |
| `pm-domain.md` | Project Management (Project Management Framework 7/8) | 1 agent (pm-agent). 1 technical skill (pm-tools-skill). 20 methodologies covering stakeholder, team, planning, delivery, measurement, uncertainty management. |
| `ba-domain.md` | Business Analysis (Business Analysis Framework) | 1 agent (ba-agent). 30 methodologies across 6 Knowledge Areas: Planning & Monitoring, Elicitation & Collaboration, Requirements Lifecycle, Strategy Analysis, Requirements Analysis & Design, Solution Evaluation. |
| `ux-domain.md` | UX/UI Design | 2 agents (ux-researcher, usability). 32 methodologies covering research methods, analysis & synthesis, design, evaluation, strategy. Includes 10 Usability Heuristics. |
| `ai-llm-domain.md` | AI/LLM | 14 agents (rag, embedding, finetuner, prompt-engineer, cost-optimizer, llm-cli, autonomous-agent-builder, voice-agent-builder, multimodal, image-generator, image-editor, video-generator, tts, stt). 11 technical skills. 42 methodologies across LLM fundamentals, RAG, embeddings, fine-tuning, prompt engineering, multimodal. |

## Usage

Reference these files when working within specific domains:

- Starting a new project -> `workflow.md`, `directory-structure.md`
- Quality gates -> `quality-assurance.md`
- Writing specs/designs -> `sdd-domain.md`
- Market research -> `research-domain.md`
- MVP/MLP planning -> `product-domain.md`
- Coding -> `development-domain.md`
- GTM/marketing -> `marketing-domain.md`
- Project management -> `pm-domain.md`
- Requirements analysis -> `ba-domain.md`
- User experience -> `ux-domain.md`
- AI/LLM applications -> `ai-llm-domain.md`
