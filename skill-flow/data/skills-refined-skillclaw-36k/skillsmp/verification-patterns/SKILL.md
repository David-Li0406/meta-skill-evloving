---
name: verification-patterns
description: Auto-loads during /verify or when validating compositions
auto_trigger:
  - "/verify"
  - "validate"
  - "test"
  - "check"
  - "verification"
---

# Verification Patterns Skill

Evidence-based verification workflow for EtherDAW.

## Two-Layer Validation System

### Layer 1: Schema Validation
File: `etherscore.schema.json`
- JSON structure validation
- Required fields check
- Type validation

### Layer 2: Semantic Validation
File: `src/validation/validator.ts`
- Pattern reference resolution
- Instrument preset validation
- Note syntax parsing
- Chord name validation
- Drum kit existence
- Time signature validation

## Verification Workflow

### Step 1: Schema + Semantic Validation
```bash
npx tsx src/cli.ts validate <file.etherscore.json>
```

**Expected output (success):**
```
Validating: examples/my-track.etherscore.json
✓ Schema validation passed
✓ Semantic validation passed
✓ All 5 patterns valid
✓ All 3 instruments valid
Validation complete: No issues found
```

### Step 2: Build Verification
```bash
npm run build
npm run build:browser
```

**Expected output:**
```
# TypeScript build - no errors
# Browser build
dist/etherdaw-browser.js  78.0kb
```

### Step 3: Test Suite
```bash
npm run test:run
```

**Expected output:**
```
✓ note-parser.test.ts (23 tests)
✓ chord-parser.test.ts (18 tests)
✓ pattern-expander.test.ts (45 tests)
...
Test Files: 12 passed
Tests: 127 passed
```

### Step 4: Audio Verification
1. Open `player.html`
2. Load composition
3. Click Play
4. Verify:
   - [ ] Expected instruments audible
   - [ ] Correct timing/rhythm
   - [ ] No clicks or pops
   - [ ] Proper dynamics
   - [ ] No frequency masking

### Step 5: Benchmark Analysis (Advanced)
```typescript
// src/analysis/benchmark-verifier.ts
verifyFrequencyContent(audio, { minHz: 60, maxHz: 16000 });
verifyTiming(audio, expectedOnsets);
verifyDynamics(audio, expectedEnvelope);
detectArtifacts(audio); // clicks, pops, DC offset
```

## Evidence Requirements

| Claim | Required Evidence |
|-------|-------------------|
| "Tests pass" | Show actual test output with counts |
| "Build works" | Show build command output |
| "Validation passes" | Show validator output |
| "Plays correctly" | Describe audio or screenshot |
| "No errors" | Show empty error output |

## Common Validation Errors

### Unknown Preset
```
Error: Unknown instrument preset 'fake_synth'
```
**Fix:** Check `src/synthesis/presets.ts` for valid names

### Invalid Note Syntax
```
Error: Invalid note syntax 'X4:q' in pattern 'melody'
```
**Fix:** Use format `<pitch><octave>:<duration>` (C4:q, D#5:h)

### Missing Pattern
```
Error: Pattern 'missing_pattern' referenced but not defined
```
**Fix:** Add pattern to `patterns` array

### Invalid Chord
```
Error: Unknown chord 'Xmaj7' in pattern 'progression'
```
**Fix:** Use valid chord names (Am7, Dm9, G7, Cmaj7)

### Invalid Drum Kit
```
Error: Unknown drum kit 'fake_kit'
```
**Fix:** Use: `808`, `909`, `acoustic`, `lofi`

## Pre-Commit Checklist

- [ ] `npm run build` - No TypeScript errors
- [ ] `npm run test:run` - All tests pass
- [ ] `npx tsx src/cli.ts validate <file>` - Validation passes
- [ ] Audio tested in player.html
- [ ] No console errors in browser
- [ ] CHANGELOG.md updated (if version change)

## Evidence Report Template

```markdown
## Verification Report

### Build
✓ TypeScript compiled with no errors
✓ Browser bundle: XX.Xkb

### Tests
✓ XXX tests passed in X.Xs
  - note-parser: XX passed
  - pattern-expander: XX passed

### Validation
✓ <filename>: All patterns valid

### Audio Check
✓ Loaded in player.html
✓ Playback: [describe what you heard]
✓ No audio artifacts detected

### Files Changed
- file1.ts (+XX lines)
- file2.json (modified)
```

## Quick Commands Reference

| Command | Purpose |
|---------|---------|
| `npx tsx src/cli.ts validate <file>` | Validate single file |
| `npm run test:run` | Run all tests |
| `npm run build` | Compile TypeScript |
| `npm run build:browser` | Build browser bundle |
| `open player.html` | Open audio player |
