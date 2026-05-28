# vision: jq-transforms

## the problem

ai agents need to do json transformations constantly but:
- jq syntax is dense and error-prone for ai to generate
- no clear contracts (what goes in, what comes out)
- hard to compose transformations
- testing is ad-hoc
- every project reimplements the same patterns

humans (skogix) can't read jq fluently, so debugging ai-generated jq is painful.

## the solution

a library of json transformations where:
- each transformation has a clear schema (input/output contract)
- transformations are tested directly (no wrapper magic)
- code is minimal and readable
- ai can understand what each transformation does
- ai can compose transformations correctly
- humans can verify behavior without reading jq internals

## core insight

**this is made for ai agents, not humans**

the goal isn't to make jq easier for humans to write.
the goal is to make json transformations:
1. **discoverable** - ai can find the right transformation
2. **understandable** - schema tells ai what it does
3. **composable** - ai can chain transformations
4. **verifiable** - tests show it works
5. **extensible** - ai can add new transformations following the pattern

## use cases

### structured i/o across projects
projects need consistent json shapes. schemas ensure:
- api responses match expected format
- config files validate correctly
- data pipelines have contracts
- ai can generate correct json

### chat-history project
already has 50+ jq transformations doing things like:
- extract messages from different formats
- normalize timestamps
- filter by date ranges
- deduplicate by content
- build conversation threading

these should be in this library, not scattered in ad-hoc scripts.

### future projects
any project doing:
- config management
- data transformation pipelines
- api response handling
- log processing
- file format conversion

## success criteria

ai agent can:
1. read schema, understand what transformation does
2. generate correct invocation without examples
3. add new transformation by following existing pattern
4. compose multiple transformations
5. debug failures by reading test cases

human can:
1. verify transformation works by reading tests
2. understand intent by reading schema
3. add transformation without knowing jq deeply

## non-goals

- making jq easier to write by hand
- complex wrapper frameworks
- runtime that adds abstraction
- language-specific bindings
- performance optimization (jq is already fast)

## what makes this different

existing approaches:
- jq libraries: no schemas, hard to discover
- json tools: language-specific, not composable
- data pipelines: heavyweight, complex setup

this approach:
- schemas as documentation
- direct jq invocation (no runtime)
- minimal dependencies (jq + bash)
- git-friendly (plain text, easy to diff)
- ai-first design

## principles

1. **schema-driven**: every transformation has input/output/args schema
2. **test-first**: tests show usage, verify behavior
3. **minimal**: less code, fewer bugs, easier to understand
4. **composable**: transformations chain via pipes
5. **direct**: no wrappers hiding what actually runs
6. **isolated**: each transformation is self-contained

## the long game

phase 1 (now):
- establish pattern (crud operations)
- prove testing strategy works
- validate schema approach

phase 2:
- extract transformations from chat-history
- categorize by type (filter, map, validation, etc)
- document composition patterns

phase 3:
- schema validation in tests (ajv)
- transformation generator/template
- documentation generator from schemas

phase 4:
- used by multiple projects
- ai agents use it naturally
- community contributions following pattern

## key questions

### do we need a runner?
maybe not. could just document piping:
```bash
jq -f transform1.jq input.json | jq -f transform2.jq
```

or maybe a simple runner that validates schemas between steps?

### schema format?
json-schema is standard but verbose.
custom format could be simpler for ai.
need to validate this with real transformations.

### file-based vs in-memory?
current approach: files in, files out.
could support streaming/pipes for performance.
but simplicity first.

### how to handle errors?
jq errors are cryptic.
schemas could generate better error messages.
but adds complexity.

### composition patterns?
some transformations need multiple steps.
document patterns? create helpers? stay manual?

## success looks like

6 months from now:
- 50+ transformations covering common patterns
- chat-history uses this library
- 2-3 other projects adopted it
- ai agents use it without human intervention
- adding new transformation takes 10 minutes
- schemas accurately describe behavior

12 months:
- 100+ transformations
- community contributions
- schema validation works smoothly
- composition patterns documented
- performance is good enough
- maintained without much effort

## why this might fail

1. schemas don't actually help ai understand
2. testing strategy doesn't scale
3. jq limitations force complexity
4. composition is too manual
5. not actually reusable across projects
6. maintenance burden too high

## mitigations

- validate with real ai usage early
- keep transformations simple
- don't force reuse where it doesn't fit
- automate what can be automated
- document patterns as they emerge
- be willing to change approach

## next steps

see backlog.md for concrete tasks.
