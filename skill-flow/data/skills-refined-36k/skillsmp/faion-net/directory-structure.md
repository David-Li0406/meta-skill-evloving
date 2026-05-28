# SDD Directory Structure

```
.aidocs/
├── constitution.md
├── roadmap.md
│
├── product_docs/
│   ├── idea-validation.md
│   ├── prd.md
│   ├── market-research.md
│   ├── competitive-analysis.md
│   ├── user-personas.md
│   ├── problem-validation.md
│   ├── pricing-research.md
│   ├── executive-summary.md
│   ├── mlp-analysis-report.md
│   ├── mlp-implementation-order.md
│   └── gtm-manifest/
│
├── tasks/
│   ├── backlog/
│   ├── todo/
│   ├── in-progress/
│   └── done/
│
└── features/
    ├── backlog/{NN}-{feature}/
    │   └── spec.md
    ├── todo/{NN}-{feature}/
    │   ├── spec.md
    │   ├── design.md
    │   ├── implementation-plan.md
    │   └── tasks/{backlog,todo,in-progress,done}/
    ├── in-progress/{NN}-{feature}/
    └── done/{NN}-{feature}/
```

## Feature Lifecycle

`backlog/` → `todo/` → `in-progress/` → `done/`

## Key Files

| File | Purpose |
|------|---------|
| `constitution.md` | Project vision, principles, constraints |
| `roadmap.md` | Features and milestones |
| `spec.md` | Feature requirements and acceptance criteria |
| `design.md` | Technical design and architecture |
| `implementation-plan.md` | Task breakdown and dependencies |
| `TASK_*.md` | Individual executable tasks |
