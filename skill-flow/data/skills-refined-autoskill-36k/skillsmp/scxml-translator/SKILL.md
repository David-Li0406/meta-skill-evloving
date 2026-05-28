---
name: scxml-translator
description: Translate SCXML test suite (.txml files in pkg/scxml_test_suite) to Go unit tests for statechart.go. Build equivalent State trees, generate table-driven tests verifying transitions/entry/exit/history. Use for conformance testing without parser.
allowed-tools: Read, Grep, Glob, Write, Edit, Bash
---

# SCXML to statechart.go Test Translator

## When to Use
- User requests SCXML test translation, conformance, or statechart validation.
- Analyze pkg/scxml_test_suite/[num]/test*.txml → mimic in new `statechart_scxml_[category]_test.go`.

## Workflow
1. **Gather Context**:
   - Glob `pkg/scxml_test_suite/**/test*.txml`
   - Read target .txml + `statechart.go` + `statechart_test.go` (patterns).
   - Grep .txml for `<state>`, `<transition event=`, `<onentry><raise>`, `conf:pass`.

2. **Map SCXML → Go State Tree**:
   | SCXML | Go |
   |-------|----|
   | `<state id=\"s1\"><transition event=\"e\" target=\"s2\"/></state>` | `&State{ID:\"s1\", Transitions:[]*Transition{{Event:\"e\", Target:\"s2\"}}}` |
   | `<onentry><raise event=\"foo\"/></onentry>` | `OnEntry: func(ctx, _,_,_,_) { rt.SendEvent(ctx, \"foo\") }` |
   | `initial=\"s0\"` | `Initial: states[\"s0\"]` |
   | `conf:pass` state | Assert `rt.IsInState(\"pass\")` |

3. **Generate Test**:
   - Table-driven: `[]struct{Name string; Root *State; Events []Event; WantPass bool}`
   - New file: `statechart_scxml_tests.go` (no existing edits).
   - Helpers: `buildSCXMLTree(map[string]string)` func.

4. **Validate**:
   - Bash `go test ./... -v -race`
   - Skip unsupported (data/invoke): `t.Skip(\"Needs datamodel\")`
   - Output: Files created, coverage gaps.

## Examples
**Input**: test144.txml (raise FIFO)
**Output Test**:
```go
t.Run(\"144\", func(t *testing.T) {
  // built tree with OnEntry raises
  rt.Start(ctx)
  require.True(t, rt.IsInState(\"pass\"))
})
```

## Limitations
- Shallow history only.
- No data model/expr (stub guards).
- Batch 10-20 tests/file.

Activate for all SCXML tasks. Combine w/ golang-development skill.
