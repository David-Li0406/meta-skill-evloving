# Dumping Compiler Graphs

Detailed instructions for generating BGV files with Graal compiler graph dumps.

## Basic Dump Commands

### Level 1: Basic Graphs (Recommended Start)

```bash
<launcher> --vm.Djdk.graal.Dump=Truffle:1 \
  --vm.Djdk.graal.PrintGraph=File \
  --vm.Djdk.graal.DumpPath=compiler_graphs \
  <program>
```

- Dumps: After parsing, After TruffleTier
- Output: `compiler_graphs/` directory with BGV files

### Level 2: Detailed Phases

```bash
<launcher> --vm.Djdk.graal.Dump=Truffle:2 \
  --vm.Djdk.graal.MethodFilter='*hotFunction*' \
  --vm.Djdk.graal.DumpPath=compiler_graphs \
  <program>
```

- Shows all optimization phases
- 5-10x more output than Level 1
- Use only for investigating specific phase failures

## Focused Dumps

### Filter by Method (Highly Recommended)

```bash
<launcher> --vm.Djdk.graal.Dump=Truffle:1 \
  --vm.Djdk.graal.MethodFilter='*hotFunction*' \
  --vm.Djdk.graal.DumpPath=compiler_graphs \
  --engine.CompileOnly='*hotFunction*' <program>
```

- `--engine.CompileOnly` ensures only this function is compiled
- Dramatically reduces output volume
- Essential for manageable analysis

### With Source Positions

```bash
<launcher> --vm.Djdk.graal.Dump=Truffle:1 \
  --vm.Djdk.graal.TrackNodeSourcePosition=true \
  --vm.Djdk.graal.DumpPath=compiler_graphs \
  --engine.NodeSourcePositions <program>
```

- Enables source location tracking
- Required for `seafoam source` command
- Shows inlining call stacks

## Dump Level Explanation

The numbers after the colon (`:1`, `:2`, `:3`) control verbosity:

| Level | Description | Use Case |
|-------|-------------|----------|
| `:1` | Fewer phases (basic dumps) | Default, most common |
| `:2` | More phases (intermediate) | Phase-specific debugging |
| `:3` | Most phases (comprehensive) | Low-level IR debugging |

`Truffle:1` with `PrintGraph=Network` shows Truffle ASTs, guest-language call graphs, and Graal graphs as they leave the Truffle phase.

`Truffle:2` dumps Graal graphs between each compiler phase.

## Output Management

### Compress BGV Files

```bash
# BGV files are huge, compress them
gzip compiler_graphs/*.bgv

# bgv2json and seafoam read .bgv.gz natively
```

### Clean Previous Dumps

```bash
# Always clean before dumping to ensure data isolation
rm -rf compiler_graphs/
```

## Combined with Tracing

```bash
<launcher> --vm.Djdk.graal.Dump=Truffle:1 \
  --vm.Djdk.graal.DumpPath=compiler_graphs \
  --experimental-options \
  --compiler.TracePerformanceWarnings=all \
  --engine.TraceCompilation \
  <program> 2>&1 | tee combined.log
```

## Typical Workflow

1. **Profile to identify hot function**
   ```bash
   <launcher> --cpusampler --cpusampler.ShowTiers=true <program>
   ```

2. **Clean previous dumps**
   ```bash
   rm -rf compiler_graphs/
   ```

3. **Dump graphs for hot function only**
   ```bash
   <launcher> --vm.Djdk.graal.Dump=Truffle:1 \
     --vm.Djdk.graal.MethodFilter='*hotFunction*' \
     --vm.Djdk.graal.DumpPath=compiler_graphs \
     --engine.CompileOnly='*hotFunction*' <program>
   ```

4. **Convert to JSON**
   ```bash
   bgv2json compiler_graphs/*.bgv > graphs.json
   ```

5. **Analyze with seafoam or jq**
