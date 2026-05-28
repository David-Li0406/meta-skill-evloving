# Detailed Phase Instructions

This file contains detailed step-by-step instructions for each phase of the establishing-benchmark-baseline skill.

## Phase 1: Analyze Language Implementation

**Objective**: Understand the current language's characteristics to determine appropriate comparisons

**Process**:

1. **Examine project structure and documentation**
   - Read CLAUDE.md, README files
   - Analyze build configuration (pom.xml, package.json, Cargo.toml, etc.)
   - Review language grammar and parser files

2. **Determine type system**
   - Static typing vs. dynamic typing
   - Type inference capabilities
   - Type checking approach (compile-time, runtime, gradual)

3. **Identify execution model**
   - Pure interpreter (AST walking)
   - Bytecode VM with interpreter
   - JIT compilation (method-based, tracing, tier-based)
   - AOT compilation
   - Hybrid approaches (interpreter + JIT)

4. **Assess implementation platform**
   - Native implementation (C/C++/Rust)
   - JVM-based (Truffle, Graal, standard JVM)
   - LLVM-based
   - Custom VM
   - Existing runtime (Node.js, CPython, Ruby VM, etc.)

5. **Evaluate language complexity**
   - Minimal (basic types, control flow, functions)
   - Moderate (OO, closures, arrays, basic libraries)
   - Full-featured (modules, metaprogramming, advanced features)

6. **Identify runtime characteristics**
   - Garbage collection (mark-sweep, generational, reference counting, etc.)
   - Memory management approach
   - Concurrency model (single-threaded, multi-threaded, async)
   - Standard library richness

**Output Example**:
```
Language: [Your Language Name]
Type System: [static/dynamic] typing
Execution Model: [interpreter/bytecode VM/JIT/AOT/hybrid description]
Platform: [native/JVM-based/LLVM-based/custom VM]
Paradigm: [Object-oriented/functional/imperative/multi-paradigm]
Complexity: [minimal/moderate/full-featured] ([key features])
GC: [GC strategy and approach]
Optimization: [Specific optimizations available]
```

## Phase 2: Identify Comparable Languages

**Objective**: Find languages that match the analyzed characteristics for meaningful comparison

**Process**:

1. **Match by execution model (highest priority)**
   - **First priority**: Same execution model (e.g., bytecode VM + JIT)
   - **Second priority**: Similar execution model (e.g., interpreted dynamic languages)
   - **Third priority**: Aspirational targets (same platform, e.g., other JVM languages)
   - **Special**: Prefer GraalVM Truffle languages if applicable (JavaScript/Node, Ruby, Python/GraalPython)

2. **Match by type system**
   - Prioritize languages with same typing discipline
   - Dynamic-typed implementations → compare with dynamic languages
   - Static-typed implementations → compare with static languages
   - Use opposite typing only as aspirational comparisons

3. **Match by paradigm and complexity**
   - Similar language features (OO support, closures, first-class functions)
   - Similar complexity level (don't compare minimal with full-featured)
   - Similar abstraction capabilities

4. **Validate availability**
   - Check if languages exist on Benchmarks Game
   - Verify sufficient benchmark coverage (at least 5-10 benchmarks)
   - Ensure recent measurements available (not outdated)

5. **Select 1-2 comparable languages**
   - One "most similar" language (primary comparison)
   - Optionally one aspirational target (stretch goal)

**Output Example**:
```
Primary Comparisons:

1. Lua - Dynamic typing, bytecode VM + JIT (LuaJIT)
   Rationale: Most similar execution model and abstraction level
   URL: https://benchmarksgame-team.pages.debian.net/benchmarksgame/measurements/lua.html

2. Python 3 - Dynamic typing, bytecode VM (CPython)
   Rationale: Similar paradigm and complexity, common comparison point
   URL: https://benchmarksgame-team.pages.debian.net/benchmarksgame/measurements/python3.html
```

## Phase 3: Retrieve Benchmark Data from Benchmarks Game

**Objective**: Fetch performance measurements and source code from Computer Language Benchmarks Game

**Process**:

1. **Query Benchmarks Game for comparable languages**
   - Use WebFetch to retrieve measurement pages
   - URL format: `https://benchmarksgame-team.pages.debian.net/benchmarksgame/measurements/{language}.html`
   - Examples: `lua.html`, `python3.html`, `ruby.html`, `javavm.html`

2. **Extract available benchmark programs**

   Parse benchmark categories:

   **Insignificant I/O** (pure computation - prefer these):
   - fannkuch-redux: Indexed access to tiny integer-sequence
   - n-body: Double-precision N-body simulation
   - spectral-norm: Eigenvalue using power method
   - mandelbrot: Generate Mandelbrot set bitmap file

   **Significant I/O**:
   - fasta: Generate and write random DNA sequences
   - k-nucleotide: Hashtable update and k-nucleotide strings
   - reverse-complement: Read DNA sequences, write reverse-complement

   **Contentious** (complex dependencies):
   - binary-trees: Allocate and deallocate many binary trees
   - pidigits: Streaming arbitrary-precision arithmetic
   - regex-redux: Match DNA sequences with regex

   Note benchmark variants (#1, #2, etc.) and their characteristics.

3. **Collect performance metrics**

   For each benchmark and language, extract:

   - **Elapsed Time**: Wall-clock execution time (seconds)
   - **CPU Time**: Actual CPU consumption with confidence interval (e.g., "24.17–25.73")
   - **Memory**: Peak memory usage (bytes or KB/MB)
   - **Test Parameter (N)**: Input size/scale (e.g., N=21 for binary-trees)

4. **Select 3-5 benchmarks for local implementation**

   Selection criteria:
   - **Coverage**: Different computational patterns (loops, recursion, allocation, numerics)
   - **Computational focus**: Prefer "insignificant I/O" benchmarks
   - **Language features**: Exercise arrays, objects, recursion, floating-point
   - **Reference quality**: Good implementations available in comparable languages
   - **Existing work**: Count existing implementations toward 3-5 total; only implement missing ones

5. **Understand measurement methodology**

   From https://benchmarksgame-team.pages.debian.net/benchmarksgame/how-programs-are-measured.html:

   - Tool: BenchExec with Linux cgroups
   - Hardware: Quad-core 3.0GHz Intel i5-3330, 15.8GB RAM
   - OS: Ubuntu 24.04
   - Protocol: 12 runs, first excluded, lowest elapsed OR 95% CI of CPU time
   - Isolated environment with cleared file system caches

**URL Formats**:
- Algorithm descriptions: `https://benchmarksgame-team.pages.debian.net/benchmarksgame/description/{benchmark}.html`
- Performance measurements: `https://benchmarksgame-team.pages.debian.net/benchmarksgame/performance/{benchmark}.html`
- Source code: `https://benchmarksgame-team.pages.debian.net/benchmarksgame/programs/{benchmark}-{language}.html`

## Phase 4: Implement Benchmarks from Benchmarks Game Locally

**Objective**: Create verified, executable local implementations of selected Benchmarks Game benchmarks

**Process**:

1. **Check for existing implementations**
   - **CRITICAL**: Before implementing, check if benchmark file already exists
   - If exists, note in report and skip to next benchmark
   - Only implement missing benchmarks

2. **Fetch implementation description**
   - Retrieve algorithm description from Benchmarks Game
   - URL: `https://benchmarksgame-team.pages.debian.net/benchmarksgame/description/{benchmark}.html`
   - Understand computational pattern, expected outputs, verification criteria

3. **Fetch reference implementations**
   - Get source code from comparable languages (Phase 2 results)
   - URL: `https://benchmarksgame-team.pages.debian.net/benchmarksgame/programs/{benchmark}-{language}.html`
   - Focus on idiomatic implementations (not heavily optimized variants #1)
   - Examine algorithm structure, data structures, approach

4. **Analyze project conventions**

   Examine existing benchmarks to understand:
   - File organization (directory structure, naming)
   - Benchmark harness/framework usage
   - Entry point patterns (main function, class structure, module export)
   - Setup/teardown patterns
   - Result verification methods
   - Command-line argument handling
   - Output formatting

5. **Translate algorithm to target language**
   - Convert reference implementation to target language syntax
   - Adapt data structures (arrays, objects, primitives)
   - Adapt control flow (loops, conditionals, recursion)
   - Follow project conventions exactly
   - Include verification logic with expected outputs
   - Add appropriate parameter handling

6. **Write to local file**
   - Create file with appropriate extension
   - Place in same location as existing benchmarks
   - Use descriptive filename matching benchmark name
   - Include verification logic to check correctness

7. **Run and verify benchmark**
   - **REQUIRED**: Test benchmark locally
   - Verify output correctness against expected results
   - **If verification fails**:
     - Debug the translation
     - Check algorithm logic
     - Compare with reference implementation
     - Query Benchmarks Game for clarification
     - **MUST FIX** - failures block workflow
   - Only skip if genuinely unfixable after multiple attempts
   - Document skip reason in baseline report

8. **Collect performance data**
   - **REQUIRED**: Run benchmark with appropriate iterations to measure performance
   - Use project's benchmark harness/framework for timing
   - Capture execution time (total runtime, average per iteration)
   - Run multiple iterations for statistical reliability (e.g., 10-100 iterations)
   - Record timestamp of measurement
   - Example command: `<language-launcher> <harness> <benchmark> <iterations> <inner-iterations>`
   - Parse output to extract timing data (e.g., "Total Runtime: 12345678us")

9. **Append performance to baseline**
   - **REQUIRED**: Update BENCHMARK_BASELINE.md with performance results
   - Add entry to "Actual Performance Results" section
   - Include: benchmark name, date/time, iterations, total time, average time
   - Format as markdown table for easy comparison
   - Keep historical data (append, don't overwrite)
   - If baseline file doesn't exist yet, note data for Phase 7

10. **Document execution instructions**
   - Command to run benchmark
   - Iteration counts/parameters
   - Expected N parameter matching Benchmarks Game
   - Expected output for verification

## Phase 5: Retrieve Benchmark Data from AreWeFastYet

**Objective**: Discover micro-benchmarks from AreWeFastYet repository

**Process**:

1. **Query AreWeFastYet README**
   - URL: `https://raw.githubusercontent.com/smarr/are-we-fast-yet/refs/heads/master/README.md`
   - Extract list of micro-benchmarks
   - Note: Focus on micro-benchmarks, ignore macro benchmarks
   - Skip benchmarks also in Benchmarks Game (avoid duplication)

2. **Query AreWeFastYet guidelines**
   - URL: `https://raw.githubusercontent.com/smarr/are-we-fast-yet/refs/heads/master/docs/guidelines.md`
   - Understand benchmark design principles
   - Note verification requirements

3. **Discover available languages**
   - Check available language folders
   - Base URL: `https://raw.githubusercontent.com/smarr/are-we-fast-yet/refs/heads/master/benchmarks/`
   - Match against comparable languages from Phase 2
   - Common languages: Python, JavaScript, Ruby, Lua, Java, SOM

**Typical Micro-Benchmarks** (AreWeFastYet):
- Bounce: Ball bouncing simulation
- List: List creation and traversal
- Permute: Array permutation generation
- Queens: N-queens problem solver
- Sieve: Sieve of Eratosthenes
- Storage: Tree of arrays (GC stress test)
- Towers: Towers of Hanoi

## Phase 6: Implement Benchmarks from AreWeFastYet Locally

**Objective**: Create ALL AreWeFastYet micro-benchmark implementations with verification

**Process**:

1. **Check for existing implementations**
   - **CRITICAL**: Before implementing, check if benchmark file already exists
   - If exists, note in report and skip to next benchmark
   - Only implement missing benchmarks

2. **Fetch ALL micro-benchmark implementations**
   - **Implement ALL micro-benchmarks** (they're specifically designed for language analysis)
   - URL format: `https://raw.githubusercontent.com/smarr/are-we-fast-yet/refs/heads/master/benchmarks/{language}/{benchmark}.{ext}`
   - Get implementations from comparable languages
   - Extract verification logic and test parameters
   - Understand expected outputs

3. **Analyze project conventions** (same as Phase 4)
   - File organization
   - Harness structure
   - Entry points
   - Verification patterns

4. **Translate benchmarks to target language**
   - Convert ALL micro-benchmarks (not just a selection)
   - Translate algorithm exactly - don't modify logic
   - Adapt to target language features
   - Follow project conventions
   - Include verification logic
   - Add test parameters

5. **Run and verify each benchmark**
   - **REQUIRED**: Test every benchmark locally
   - Verify output correctness
   - **If verification fails**:
     - Debug translation
     - Query AreWeFastYet for clarification
     - Compare with reference implementation
     - **MUST FIX** - failures block workflow
   - Only skip if genuinely unfixable after multiple attempts
   - Document skip reason in baseline report

6. **Collect performance data**
   - **REQUIRED**: Run benchmark with appropriate iterations to measure performance
   - Use project's benchmark harness/framework for timing
   - Capture execution time (total runtime, average per iteration)
   - Run multiple iterations for statistical reliability (e.g., 100-1000 iterations)
   - Record timestamp of measurement
   - Example command: `<language-launcher> <harness> <benchmark> <iterations> <inner-iterations>`
   - Parse output to extract timing data

7. **Append performance to baseline**
   - **REQUIRED**: Update BENCHMARK_BASELINE.md with performance results
   - Add entry to "Actual Performance Results" section
   - Include: benchmark name, date/time, iterations, total time, average time
   - Format as markdown table for easy comparison
   - Keep historical data (append, don't overwrite)
   - If baseline file doesn't exist yet, note data for Phase 7

8. **Document execution**
   - Commands for each benchmark
   - Iteration parameters
   - Verification criteria

**Important Notes**:
- AreWeFastYet benchmarks are micro-benchmarks (small, focused)
- Designed specifically for language implementation performance analysis
- More relevant for profiling than Benchmarks Game
- Should implement ALL of them (usually 7-10 benchmarks)

## Phase 7: Generate and Save Baseline Report

**Objective**: Create comprehensive `BENCHMARK_BASELINE.md` report

See [EXAMPLES.md](EXAMPLES.md) for a complete example report structure.

**Output**: Saved markdown file `BENCHMARK_BASELINE.md` in project root
