# Diátaxis Documentation Structure Blueprint

Initialize the project documentation using the following structure:

```bash
doc/
├── explanation/   # Understanding-oriented (Why & How it works)
│   ├── README.md
│   ├── architecture.md
│   └── system-dev.md
├── specs/         # Information-oriented (API & Protocols)
│   ├── README.md
│   └── [subsystem].md
├── how-to/        # Problem-oriented (Step-by-step guides)
│   ├── README.md
│   └── workflows/
├── tutorials/     # Learning-oriented (Onboarding)
│   └── quick-start.md
└── archive/       # Historical logs & dead decisions
```

## Maintenance Rules
- **Rule One**: The Constitution (`.agent/rules/rule-one.md`).
- **Memory**: The Project Map (`doc/memory.md`).
- **Standard**: Follow `doc/explanation/system-dev.md` for all documentation updates.
