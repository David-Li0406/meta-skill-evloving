# Go Service Hexagonal: References Index

Use these files as needed; do not load everything by default.

- `references/layout-base.md`: Shared directory structure and what each folder is for
- `references/layout-http-rest.md`: HTTP REST/JSON service layout (net/http baseline)
- `references/layout-http-echo.md`: HTTP REST/JSON service layout (Echo framework)
- `references/layout-grpc.md`: gRPC service layout (proto + generated code conventions)
- `references/layout-worker.md`: Worker/consumer/scheduler layout (queues, cron, jobs)
- `references/layout-cli.md`: CLI/tooling layout (cobra-style without assuming deps)
- `references/architecture-rules.md`: Dependency rules and package boundary checklist
- `references/refactor-workflow.md`: Step-by-step refactor workflow for existing Go projects
- Refactor plans should be tracked in a checkboxed `REFACTORING.md` at repo root (see refactor workflow).
- `references/refactor-testing.md`: Minimal, necessary testing guidance during refactors
- `references/refactor-plan-template.md`: Plan template for user-approved refactors
