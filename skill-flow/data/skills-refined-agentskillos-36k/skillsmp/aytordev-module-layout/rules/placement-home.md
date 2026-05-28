## Home Module Categories

**Impact:** HIGH

Organize user modules (Home Manager) into specific categories: `programs` (graphical/terminal), `services`, `desktop`, or `suites`.

**Incorrect:**

**Flat Structure**
Dumping everything into `modules/home/programs/` without distinguishing between GUI and CLI tools.

**Correct:**

**Categorized Tree**

```
modules/home/
├── programs/
│   ├── graphical/        # GUI: browsers, editors, tools
│   └── terminal/         # CLI: editors, shells, tools
├── services/             # User services
├── desktop/              # Desktop environment config
└── suites/               # Grouped functionality
```
