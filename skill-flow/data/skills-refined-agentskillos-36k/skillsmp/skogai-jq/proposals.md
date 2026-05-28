# proposals

ideas under consideration. not committed to any of these yet.

## proposal: transformation runner

### problem
running transformations requires knowing jq syntax:
```bash
jq -f crud-get/transform.jq --arg path "user.name" --arg default "" input.json
```

ai agents might generate this wrong (flag order, quoting, etc).

### option 1: no runner
document the pattern, trust ai to get it right.
pros: simple, no abstraction
cons: ai will make mistakes

### option 2: minimal runner
```bash
transform run crud-get input.json --path "user.name" --default ""
```
pros: simpler interface, validates args
cons: another layer, need to maintain

### option 3: schema-aware runner
```bash
transform run crud-get input.json '{"path":"user.name","default":""}'
```
reads schema, validates input, runs transform, validates output.
pros: catches errors early
cons: complex, slow

### decision
start with no runner. add minimal runner if ai consistently fails.

---

## proposal: schema format

### current approach
custom json format:
```json
{
  "input": {"type": "object"},
  "args": {"path": {"type": "string"}},
  "output": {"type": "string"}
}
```

### option 1: json schema
use standard json schema for everything.
pros: tooling exists (ajv), well-documented
cons: verbose, complex for simple cases

### option 2: simplified custom format
```json
{
  "in": "object",
  "args": {"path": "string", "default": "string?"},
  "out": "string|null"
}
```
pros: concise, easy for ai to read
cons: need to write validator, less standard

### option 3: typescript-style types
```
(input: object, args: {path: string, default?: string}) => string | null
```
pros: familiar to developers, very concise
cons: not json, need parser

### decision
stick with current approach. test with ajv. refine if too verbose.

---

## proposal: composition helpers

### problem
common pattern: apply transformation to each array item.

current:
```bash
jq '.items | map(fromjson)' input.json | jq -f transform.jq | jq -s '.'
```

### option 1: built-in map transformation
```bash
transform map crud-set items --path "name" --value "updated"
```
applies crud-set to each item in array at path.

### option 2: jq wrapper functions
create helper.jq:
```jq
def apply_to(path; transform):
  getpath(path) | map(transform) as $result |
  setpath(path; $result);
```

### option 3: document patterns only
show examples of composition, let users figure it out.

### decision
start with option 3. build helpers if pattern emerges clearly.

---

## proposal: transformation discovery

### problem
ai needs to find the right transformation.

### option 1: list command
```bash
transform list
transform search "get value"
```
reads all schemas, shows matches.

### option 2: documentation site
generated from schemas, searchable.

### option 3: embedding search
embed schema descriptions, semantic search.

### option 4: just read the directories
transformations are well-named, schemas are readable.

### decision
option 4 first. ai can read directory structure easily.

---

## proposal: versioning

### problem
transformations might change, break existing usage.

### option 1: no versioning
breaking changes allowed, users update usage.

### option 2: version in directory name
```
crud-get-v1/
crud-get-v2/
```

### option 3: git tags/branches
use git for versioning.

### option 4: semantic versioning in schema
```json
{
  "version": "1.2.0",
  ...
}
```

### decision
option 1 for now. reconsider if multiple projects depend on this.

---

## proposal: transformation categories

### problem
50+ transformations gets messy fast.

### option 1: flat directory
```
crud-get/
crud-set/
array-map/
...
```
simple, but cluttered.

### option 2: categorize by type
```
crud/
  get/
  set/
array/
  map/
  filter/
string/
  split/
  join/
```
organized, but adds depth.

### option 3: tags in schema
```json
{
  "tags": ["crud", "object", "read"],
  ...
}
```
flexible, searchable, still flat directory.

### decision
flat directory while small. categorize if >20 transformations.

---

## proposal: error messages

### problem
jq errors are cryptic:
```
jq: error (at <stdin>:1): Cannot index string with string "name"
```

### option 1: wrap transformations with better errors
add error checking jq code to each transformation.
cons: bloats transformations, slow.

### option 2: validate schemas pre/post
runner validates input matches schema, output matches schema.
gives clear "input must be object" message.

### option 3: documentation
document common errors and solutions.

### decision
option 3 + maybe option 2 if we build a runner.

---

## proposal: testing strategy

### current
single test.sh runs all tests, exits on first failure.

### option 1: per-transformation tests
```
crud-get/test.sh
crud-set/test.sh
```
isolated, can run individually.

### option 2: test framework
use bats or similar.

### option 3: generated tests
read schema, generate basic tests automatically.

### decision
current approach works. reconsider at 10+ transformations.

---

## proposal: documentation

### problem
how do users learn to use transformations?

### option 1: readme per transformation
crud-get/README.md explains usage.

### option 2: examples in schema
```json
{
  "examples": [
    {
      "input": {...},
      "args": {...},
      "output": {...}
    }
  ]
}
```

### option 3: generate docs from schema + tests
read schema + test files, generate usage docs.

### option 4: usage comments in transform.jq
```jq
# Get value at path with optional default
# Usage: jq -f crud-get/transform.jq --arg path "user.name" --arg default ""
```

### decision
option 4 (already doing this) + option 2 for complex transformations.

---

## proposal: mcp integration

### problem
could expose transformations as mcp tools for ai agents.

### approach
create mcp server that:
- lists available transformations
- reads schemas
- executes transformations
- validates i/o

ai agent calls tool, gets transformation result.

### pros
- clean interface for ai
- schema validation automatic
- discoverability built-in

### cons
- another layer of abstraction
- requires mcp server running
- adds complexity

### decision
interesting, but after we have 20+ transformations working.

---

## proposal: transformation generator

### problem
creating new transformation requires:
1. create directory
2. write transform.jq
3. write schema.json
4. create test files
5. update test.sh

tedious, easy to forget steps.

### approach
```bash
transform new array-sum \
  --description "sum numeric array" \
  --input "array" \
  --output "number"
```

generates template with:
- directory structure
- basic transform.jq
- schema from args
- test placeholders

### decision
build this after pattern is solid and we've created 5+ manually.

---

## proposal: performance benchmarks

### problem
no idea if transformations are fast or slow.

### approach
benchmark each transformation with varying input sizes.
document performance characteristics in schema.

### decision
premature. jq is generally fast enough.

---

## proposal: streaming support

### problem
large json files don't fit in memory.

### approach
use jq --stream mode for transformations that support it.
document which transformations work with streaming.

### decision
not needed yet. revisit when we hit file size issues.

---

## wild ideas

### transformation algebra
compose transformations symbolically before execution.
optimize pipelines automatically.
probably overkill.

### visual transformation builder
drag-and-drop transformations, generates jq.
fun idea, but not our use case.

### ai generates transformations
describe what you want, ai writes the jq + schema + tests.
could work, but need solid examples first.

### transformation marketplace
community-contributed transformations.
nice long-term vision.

### type inference
infer output schema from input schema + transformation.
hard problem, probably not worth it.

---

## questions to explore

1. can we generate schemas from jq code?
2. can we validate jq syntax before running?
3. how to handle side effects (file i/o, network)?
4. should transformations be pure functions only?
5. what about stateful transformations?
6. how to handle secrets in transformations?
7. caching transformation results?
8. parallel execution of independent transformations?
9. transformation dependencies (one requires another)?
10. how to test composition patterns?

---

## rejected ideas

### complex type system
tried to add full type checking. too complex for benefit.

### language-specific bindings
python/node wrappers for transformations. adds dependencies.

### web ui
not our use case, ai doesn't need it.

### graphql-style query language
interesting but jq already exists and works.
