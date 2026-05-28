# Nebu Processor Builder Skill

Claude Code skill for interactively building Nebu processors.

## What It Does

Guides you through creating origin, transform, or sink processors with:
- Proper Go module structure (no replace directives!)
- Official CLI helper usage
- Skeleton code with helpful TODOs
- README with usage examples
- Optional registry entry

## Installation

### Option 1: Project-Level (Recommended)

Add to your nebu repository so the skill is available to anyone working on the project:

```bash
mkdir -p .claude/skills
cd .claude/skills
git clone https://github.com/withObsrvr/nebu-processor-registry.git
ln -s nebu-processor-registry/skills/nebu-processor-builder nebu-processor-builder
```

### Option 2: Personal (Your Machine Only)

Add to your personal Claude Code skills directory:

```bash
mkdir -p ~/.claude/skills
cd ~/.claude/skills
git clone https://github.com/withObsrvr/nebu-processor-registry.git
ln -s nebu-processor-registry/skills/nebu-processor-builder nebu-processor-builder
```

Claude Code will automatically discover the skill at startup.

## Usage

In Claude Code:

```
/nebu-processor-builder
```

The skill will ask:
1. **Processor type?** (origin/transform/sink)
2. **What does it do?** (one-line description)
3. **Name?** (kebab-case, e.g., "my-filter")
4. **Create registry entry?** (y/n)

## Example Session

```
User: /nebu-processor-builder

Skill: What type of processor are you building?
  - origin: Extract data from Stellar ledgers
  - transform: Filter or modify event streams
  - sink: Write events to external systems

User: transform

Skill: What does your transform processor do? (one-line description)

User: Filters token transfers to only USDC over $10,000

Skill: Processor name? (kebab-case)

User: large-usdc-filter

Skill: Create registry entry? (y/n)

User: y

Skill: ✓ Created examples/processors/large-usdc-filter/
      ✓ Updated go.work
      ✓ Created registry entry

Next steps:
1. Implement filter logic (see TODOs in main.go)
2. Test build: cd examples/processors/large-usdc-filter && go build ./cmd/large-usdc-filter
3. Test run: token-transfer | ./large-usdc-filter
```

## What Gets Generated

### For All Processors

```
examples/processors/{name}/
├── cmd/{name}/main.go    # CLI entry point with proper helpers
├── go.mod                # Standalone module (no replace!)
├── README.md             # Usage documentation
└── {other files}
```

**Plus:**
- Updated `go.work` (if exists)
- Registry entry in `nebu-processor-registry/` (if requested)

### Type-Specific

**Origin:**
- Uses `cli.RunProtoOriginCLI()` or `cli.RunGenericOriginCLI()`
- Implements `ProcessLedger()` method
- Emitter for typed events

**Transform:**
- Uses `cli.RunTransformCLI()`
- Implements `transformEvent()` function
- Stdin → Filter/Modify → Stdout

**Sink:**
- Uses `cli.RunSinkCLI()`
- Implements `processEvent()` function
- Connection management helpers

## File Structure

```
skills/nebu-processor-builder/
├── skill.md                          # Main skill definition
├── instructions/
│   ├── processor-patterns.md         # General patterns
│   ├── origin-processors.md          # Origin-specific guide
│   ├── transform-processors.md       # Transform-specific guide
│   └── sink-processors.md            # Sink-specific guide
├── templates/
│   ├── origin-template.go            # Reference origin code
│   ├── transform-template.go         # Reference transform code
│   └── sink-template.go              # Reference sink code
└── README.md                         # This file
```

## Key Features

### ✓ Follows Best Practices
- No replace directives in go.mod
- Uses official CLI helpers
- Proper module structure
- Compiles immediately

### ✓ Helpful Guidance
- Type-specific instructions
- Reference existing processors
- Clear TODOs for implementation
- Usage examples in README

### ✓ Registry Integration
- Optional registry entry generation
- Proper YAML format
- Includes examples and docs

## Requirements

- Must be in nebu repository directory
- Go 1.25+ installed
- Claude Code with skills support

## Validation

Generated processors are validated to ensure:
- [x] Code compiles: `go build ./cmd/{name}`
- [x] Module path correct
- [x] NO replace directives
- [x] Uses CLI helpers (not custom cobra)
- [x] Version set to "0.1.0"
- [x] TODOs mark implementation points
- [x] README has examples

## Processor Types

### Origin
Extracts data from Stellar ledgers.

**Use for:**
- Token transfer events
- Contract invocations
- Ledger state changes

**Reference:** `token-transfer`, `contract-events`

### Transform
Filters or modifies event streams.

**Use for:**
- Filtering by criteria
- Enriching events
- Deduplication
- Aggregation

**Reference:** `amount-filter`, `dedup`, `usdc-filter`

### Sink
Writes events to external systems.

**Use for:**
- Database storage
- Message queue publishing
- File output
- API calls

**Reference:** `json-file-sink`, `postgres-sink`, `nats-sink`

## Next Steps After Generation

1. **Implement logic:** Follow TODOs in generated code
2. **Test build:** `go build ./cmd/{name}`
3. **Test run:** Use in a pipeline
4. **Add tests:** Write unit/integration tests
5. **Document:** Update README with specifics
6. **Commit:** Add to version control

## Troubleshooting

### "Not in nebu repository"
- Ensure you're in `/home/tillman/Documents/nebu` (or your nebu repo path)
- Check with `pwd`

### "Processor name already exists"
- Choose a different name
- Check `examples/processors/` directory

### Build fails with "ambiguous import"
- This is expected in go.work mode during development
- Build still works: `go build ./cmd/{name}`
- For installation, use `go install` (no go.work)

### Generated code doesn't compile
- Check Go version (needs 1.25+)
- Run `go mod tidy` in processor directory
- Verify dependencies in go.mod

## Contributing

To improve this skill:

1. Update instruction files in `instructions/`
2. Update templates in `templates/`
3. Update `skill.md` workflow
4. Test by generating sample processors
5. Submit PR to nebu-processor-registry

## Resources

- [Nebu Documentation](https://github.com/withObsrvr/nebu)
- [Processor Registry](https://github.com/withObsrvr/nebu-processor-registry)
- [CLI Helpers](https://github.com/withObsrvr/nebu/tree/main/pkg/processor/cli)
- [Example Processors](https://github.com/withObsrvr/nebu/tree/main/examples/processors)

## License

MIT

## Support

- **Skill Issues:** [nebu-processor-registry issues](https://github.com/withObsrvr/nebu-processor-registry/issues)
- **Nebu Questions:** [nebu discussions](https://github.com/withObsrvr/nebu/discussions)
- **Processor Help:** See instruction files in `instructions/`
