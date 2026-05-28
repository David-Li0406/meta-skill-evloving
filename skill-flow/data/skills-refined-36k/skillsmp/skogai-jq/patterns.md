# patterns

common patterns in json transformations and how to handle them.

## access patterns

### get nested value
```jq
.user.profile.name
```
problem: fails if intermediate keys missing
solution: use `//` for default or `?` for optional

```jq
.user.profile.name // "unknown"
.user?.profile?.name
```

### get by path string
```jq
getpath(["user", "profile", "name"])
```
works with dynamic paths from args

### set nested value
```jq
setpath(["user", "profile", "name"]; "value")
```
creates intermediate objects automatically

### check existence
```jq
has("key")
.key != null
```
different semantics: has checks key exists, != null checks not null

## transformation patterns

### map over array
```jq
.items | map(.name)
```
transform each item

### filter array
```jq
.items | map(select(.active))
```
keep items matching condition

### reduce array
```jq
.items | reduce .[] as $item (0; . + $item.value)
```
fold array to single value

### group by
```jq
group_by(.category)
```
groups into array of arrays

### index by key
```jq
INDEX(.id)
```
creates object keyed by field

## composition patterns

### pipeline
```bash
cat input.json | jq -f transform1.jq | jq -f transform2.jq
```
chain transformations via pipes

### multiple inputs
```bash
jq -s -f transform.jq file1.json file2.json
```
slurp multiple files into array

### arguments
```bash
jq -f transform.jq --arg name "value" --argjson obj '{"key":"val"}'
```
pass arguments to transformation

### file includes
```jq
include "helpers";
some_helper_function
```
reuse common functions (need -L flag for library path)

## common operations

### merge objects
```jq
. + {new: "field"}  # shallow merge
. * {new: "field"}  # recursive merge
```

### conditional
```jq
if .type == "user" then .user else .guest end
```

### try/catch
```jq
try .field catch "default"
```

### exists check with default
```jq
.field // "default"
```

### array to object
```jq
[.items[] | {key: .id, value: .name}] | from_entries
```

### object to array
```jq
to_entries | map({id: .key, name: .value})
```

## schema patterns

### required fields
```json
{
  "input": {
    "type": "object",
    "required": ["field1", "field2"]
  }
}
```

### optional fields with defaults
```json
{
  "input": {
    "type": "object",
    "properties": {
      "optional": {"type": "string", "default": "value"}
    }
  }
}
```

### union types
```json
{
  "output": {
    "type": ["string", "null"]
  }
}
```

### array items
```json
{
  "input": {
    "type": "array",
    "items": {"type": "object"}
  }
}
```

## testing patterns

### exact match
```bash
result=$(jq -c -f transform.jq input.json)
expected=$(jq -c . expected.json)
[[ "$result" == "$expected" ]] || exit 1
```

### field presence
```bash
jq -e '.field' result.json >/dev/null || exit 1
```

### type check
```bash
[[ $(jq -r '.field | type' result.json) == "string" ]] || exit 1
```

### array length
```bash
[[ $(jq '. | length' result.json) -eq 3 ]] || exit 1
```

### contains check
```bash
jq -e '.array | contains(["item"])' result.json >/dev/null || exit 1
```

## error handling patterns

### validate input
```jq
if (.field | type) != "string" then
  error("field must be string")
else
  .field
end
```

### provide defaults
```jq
.field // "default" // error("field required")
```

### skip invalid items
```jq
.items | map(select(.valid == true))
```

### collect errors
```jq
[.items[] | try .field catch {error: ., item: .}]
```

## performance patterns

### avoid repeated work
```jq
(.field | expensive_operation) as $result |
{
  a: $result,
  b: $result
}
```

### stream large files
```bash
jq --stream -f transform.jq large.json
```

### limit processing
```jq
.items | first(10)  # only process first 10
```

## anti-patterns

### nested pipes
```jq
# bad
.field | .nested | .deep | .value

# good
.field.nested.deep.value
```

### string concatenation for paths
```jq
# bad
."user_" + $name

# good
.["user_" + $name]
```

### imperative loops
```jq
# bad (can't do this anyway)
for item in items:
  transform(item)

# good
.items | map(transform)
```

### complex logic in jq
if transformation logic gets complex, consider:
- breaking into multiple simple transformations
- moving complex logic to separate script
- using a real programming language

## discovered patterns

as we build more transformations, document new patterns here:
- when do we need streaming?
- how to handle pagination?
- what about rate limiting?
- error retry strategies?
- caching expensive operations?

## questions

- when to use --arg vs --argjson?
- how to handle binary data?
- unicode normalization?
- timezone handling?
- large number precision?
