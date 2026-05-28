---
name: functional-testing
description: Use when implementing tests, writing test cases, discussing test strategy, or reviewing test code. Guides testing to bridge design documents and implementation, focusing on system boundaries.
allowed-tools: [Read, Glob, Grep, Write, Edit, Bash]
---

# Functional Testing Skill

## Core: Three-Layer Consistency

```
Design Doc  →  Scaffold/Template  →  Runtime
   (約束)         (生成物)           (実行)
        ↘          ↓          ↙
              TEST (検証)
```

テストは単一層でなく**3つの真実の源**を突き合わせる。2つが一致しても残り1つが乖離すれば契約違反。

## 1. Test Categories

### A. Contract Tests (設計契約)

```typescript
/** @design_ref agents/docs/design/08_step_flow.md */
Deno.test("stepId follows c2.c3 pattern", () => {
  assertMatch(step.stepId, /^[a-z]+\.[a-z]+$/);
});
```

### B. Enforcement Tests (強制検証)

契約の「存在」と「強制」は別問題。違反時に**警告で終わるか、エラーで止まるか**をテスト:

```typescript
// Design says: "initial steps must not emit handoff"
Deno.test("initial step handoff is rejected, not just warned", async () => {
  await assertRejects(
    () => processStep("initial.start", { handoff: true }),
    HandoffNotAllowedError,  // not just console.warn
  );
});
```

### C. Drift Detection (乖離検出)

| Layer Pair | What to Check |
|------------|---------------|
| Spec ↔ Scaffold | 生成物が仕様のフィールドを含むか |
| Spec ↔ Runtime | 実行時が仕様の制約を守るか |
| Scaffold ↔ Runtime | 生成物が実行時に尊重されるか |
| Doc A ↔ Doc B | 複数ドキュメント間の矛盾 |

```typescript
Deno.test("scaffold includes intentSchemaRef as spec requires", () => {
  const scaffold = generateScaffold("step");
  assertExists(scaffold.structuredGate?.intentSchemaRef);
});
```

### D. Dead Reference Detection (陳腐化検出)

ドキュメントが参照するAPIやクラスが「生きているか」を検証:

```typescript
Deno.test("documented FlowController is actually used", () => {
  // If docs reference FlowController but code uses WorkflowRouter,
  // either docs or code needs updating
  assertExists(mod.FlowController);
  assert(isUsedInRunner(mod.FlowController));
});
```

### E. Flow Path Verification (経路検証)

設計図のフロー（状態遷移）が実際のコードパスと一致するか:

```typescript
Deno.test("repeat routes back to work step, not closure", async () => {
  const result = await router.handleRepeat("closure.verify");
  assertEquals(result.nextStep, "work.implement");  // not "closure.default"
});
```

## 2. Boundary Testing Quick Ref

| Boundary | Test Focus |
|----------|------------|
| API | Input/output shape, error types |
| Config | Schema validation, defaults |
| FileSystem | Required files exist |
| Value Pass | Variables substituted correctly |

```typescript
// API boundary
Deno.test("returns PromptResult shape", async () => {
  const result = await resolveStepPrompt(stepId, vars);
  assertExists(result.content);
  assertExists(result.path);
});

// Error boundary
Deno.test("invalid input throws typed error", async () => {
  await assertRejects(() => fn("invalid"), SpecificError);
});
```

## 3. Test Structure

```typescript
/** @design_ref path/to/design.md */

// 1. Existence (files, exports, config keys)
Deno.test("required components exist", ...);

// 2. Contract (input/output shapes)
Deno.test("function returns expected shape", ...);

// 3. Enforcement (violations are blocked, not warned)
Deno.test("constraint violation throws error", ...);

// 4. Alignment (confirm what IS working)
Deno.test("tool isolation matches design", ...);
```

## 4. Checklist

- [ ] Design document referenced (`@design_ref`)
- [ ] Tests verify contracts, not implementation details
- [ ] Enforcement tested (error, not just warning)
- [ ] Cross-layer consistency checked (spec ↔ scaffold ↔ runtime)
- [ ] Dead references detected
- [ ] Flow paths match diagrams
- [ ] Alignments reported (what works correctly)
- [ ] No absolute paths in test code
