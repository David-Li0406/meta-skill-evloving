# NixOS Linux Master Skill

Advanced Claude skill for NixOS, Linux systems, flake development, and innovative problem-solving.

## 🚀 Overview

This skill transforms Claude into a NixOS/Linux expert with:
- **Flake mastery**: Advanced patterns, auto-detection, multi-system support
- **Debug excellence**: eBPF, namespaces, system tracing, core dump analysis
- **Packaging expertise**: Universal build systems, cross-compilation, optimization
- **Security hardening**: Kernel hardening, AppArmor, container security, RASP
- **Proactive problem-solving**: Anticipates issues, suggests improvements, brainstorms solutions
- **Innovation mindset**: Cutting-edge approaches, unconventional solutions

## 📁 Structure

```
nixos-linux-master/
├── SKILL.md                           # Main skill definition
├── references/                        # Deep-dive documentation
│   ├── nix-flakes-patterns.md        # Advanced flake patterns
│   ├── linux-debug-cookbook.md       # Comprehensive debugging guide
│   ├── packaging-guide.md            # Advanced packaging techniques
│   └── security-hardening.md         # Security implementation guide
├── scripts/                           # Practical automation tools
│   ├── nix-build-debug.sh            # Build troubleshooting
│   ├── flake-scaffold.sh             # Advanced flake generator
│   └── system-analyzer.sh            # System diagnostics
└── assets/
    └── flake-templates/               # Production-ready templates
        └── smart-template.nix         # Auto-detecting flake

```

## 🎯 When to Use

Triggers automatically when:
- Working with NixOS configurations or Nix flakes
- Debugging complex Linux system issues
- Building or packaging software
- Implementing security measures
- Optimizing builds or performance
- Designing system architecture
- Need creative/unconventional solutions
- Want proactive suggestions

## 🔧 Scripts Overview

### nix-build-debug.sh
Advanced Nix build troubleshooter with:
- Automatic error pattern recognition
- Store integrity checking
- Closure size analysis
- Interactive debugging mode
- Report generation

Usage:
```bash
./scripts/nix-build-debug.sh check      # Run diagnostics
./scripts/nix-build-debug.sh build      # Interactive build
./scripts/nix-build-debug.sh analyze    # Closure analysis
./scripts/nix-build-debug.sh report     # Generate report
```

### flake-scaffold.sh
Generate production-ready flake structures with:
- Multi-language dev environments (Rust, Python, Node, Go, Full-stack)
- Modular organization (hosts, modules, packages, overlays)
- Pre-commit hooks integration
- Home Manager support
- Rust overlay integration

Usage:
```bash
./scripts/flake-scaffold.sh my-project multi-env
cd my-project
nix develop .#rust    # Or .#python, .#node, .#go
```

### system-analyzer.sh
Comprehensive system diagnostics:
- Resource analysis (CPU, memory, disk)
- Network health monitoring
- Process analysis
- Service health checks
- Security auditing
- NixOS-specific checks
- Automated recommendations

Usage:
```bash
./scripts/system-analyzer.sh full       # Complete analysis
./scripts/system-analyzer.sh quick      # Fast overview
./scripts/system-analyzer.sh security   # Security audit
./scripts/system-analyzer.sh nixos      # NixOS-specific
```

## 📚 Reference Guides

### nix-flakes-patterns.md
Advanced patterns for:
- Multi-system architecture
- Modular package development
- Cross-compilation
- Binary cache integration
- Override and overlay techniques
- Development shells
- Testing and CI

### linux-debug-cookbook.md
Comprehensive debugging techniques:
- System-level debugging (strace, perf, eBPF)
- Kernel tracing
- Network debugging (tcpdump, SSL/TLS)
- Nix-specific debugging
- Storage and filesystem analysis
- Memory debugging
- Container/namespace debugging
- Binary analysis

### packaging-guide.md
Advanced packaging strategies:
- Zero-config packaging
- Universal build wrappers
- Cross-language compilation
- Compiler optimization (PGO, LTO)
- Containerized builds
- Dynamic library patching
- Incremental builds

### security-hardening.md
Security implementation:
- NixOS hardening profiles
- Container security
- Binary analysis automation
- Exploit mitigation
- Network security
- Zero-trust architecture
- RASP implementation

## 🎨 Key Features

### Proactive Suggestions
Claude doesn't just answer—it anticipates needs and suggests:
- Architectural improvements
- Performance optimizations
- Security enhancements
- Better tooling options
- Alternative approaches

### Innovation Focus
Embraces cutting-edge solutions:
- Auto-detection systems
- Zero-config packaging
- Intelligent build systems
- Creative use of Nix features
- Unconventional problem-solving

### Deep Technical Knowledge
Combines expertise across:
- NixOS and Nix language
- Linux kernel and systems
- Multiple programming languages
- Security and hardening
- DevOps and infrastructure

## 🔥 Example Workflows

### 1. Quick Project Setup
```bash
./scripts/flake-scaffold.sh my-rust-app
cd my-rust-app
nix develop
```

### 2. Debug Build Failure
```bash
./scripts/nix-build-debug.sh build .#mypackage
# Enters interactive debug mode
```

### 3. System Health Check
```bash
./scripts/system-analyzer.sh full
# Get comprehensive system analysis with recommendations
```

### 4. Create Custom Package
Reference `packaging-guide.md` for advanced patterns, then:
```bash
nix develop
# Create package definition using universal wrapper patterns
nix build .#mypackage
```

## 🚀 Integration with MCP Server

This skill is designed for integration with MCP (Model Context Protocol) servers:

1. **Drop-in compatibility**: All scripts and references work standalone
2. **Structured output**: Scripts provide both human-readable and parseable output
3. **Error handling**: Robust error detection and reporting
4. **Modular design**: Easy to extend or customize per environment

### MCP Integration Tips
- Scripts return meaningful exit codes
- All output is UTF-8 compatible
- JSON-structured data available where applicable
- No interactive prompts in automation mode

## 🧠 Philosophy

This skill embodies:
- **Think outside the box**: Challenge assumptions, explore alternatives
- **Be proactive**: Anticipate needs, suggest improvements
- **Leverage ecosystem**: Use NixOS/Linux primitives creatively
- **Innovate continuously**: Try new approaches, stay cutting-edge
- **Document thoroughly**: Share knowledge, enable others

## 📝 License

Complete terms available in the skill package.

## 🤝 Contributing

When using this skill:
1. Experiment with advanced patterns
2. Combine techniques creatively
3. Share discoveries
4. Push boundaries
5. Learn continuously

---

**Built for**: Advanced NixOS/Linux development, innovative problem-solving, and proactive system engineering.

**Optimized for**: Efficiency, innovation, and out-of-the-box thinking.
