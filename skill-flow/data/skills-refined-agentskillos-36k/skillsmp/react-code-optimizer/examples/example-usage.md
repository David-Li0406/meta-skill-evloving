# React Code Optimizer - Example Usage

## Example 1: Full Project Analysis

**User Request:**
```
Use react-code-optimizer to analyze my entire project
```

**What the Skill Does:**
1. Scans all `.tsx` and `.ts` files in `src/`
2. Identifies large files (>500 lines)
3. Checks for React.memo usage
4. Analyzes Context providers
5. Generates optimization plan

**Output:**
- `task.md` with checklist of issues
- `implementation_plan.md` with detailed solutions

---

## Example 2: Focus on Performance

**User Request:**
```
Use react-code-optimizer focusing only on performance issues
```

**What the Skill Does:**
1. Checks React.memo usage
2. Analyzes useCallback/useMemo usage
3. Identifies expensive re-renders
4. Checks for proper key usage
5. Suggests code splitting opportunities

---

## Example 3: Specific Directory

**User Request:**
```
Analyze components in src/pages/edit using react-code-optimizer
```

**What the Skill Does:**
1. Scans only files under `src/pages/edit/`
2. Performs full analysis on that subset
3. Generates focused optimization plan

---

## Example 4: After Optimization

**User Request:**
```
Verify my optimizations using react-code-optimizer
```

**What the Skill Does:**
1. Re-runs analysis
2. Compares with previous findings
3. Shows improvements made
4. Identifies remaining issues

---

## Sample Output Structure

```markdown
# Optimization Plan for MyReactApp

## Executive Summary
- 12 components need React.memo
- 3 files over 1000 lines
- Context re-renders 47 times per action
- Estimated 40% performance improvement

## Phase 1: Quick Wins (1-2 days)
### Add React.memo
- src/components/Header.tsx
- src/components/Sidebar.tsx
- src/components/DataGrid.tsx

### Optimize Context
- Split EditorContext into 3 contexts
- Add proper useMemo dependencies

## Phase 2: Refactoring (3-4 days)
### Split Large Files
- PropertyPanel.tsx (4684 lines) → 5 files
- CanvasItem.tsx (1539 lines) → 4 files

### Extract Hooks
- useDataFetch
- useSelection
- useDragAndDrop
```

---

## Integration with Development Workflow

### During Development
```
"I just created a new feature, can you check if I need optimizations?"
→ Skill analyzes new code and suggests improvements
```

### Before Release
```
"Review my code for performance before I deploy"
→ Comprehensive analysis with focus on critical paths
```

### During Code Review
```
"Analyze the changes in src/features/dashboard"
→ Focused analysis on specific changes
```

---

## Customization Examples

### Example: Only Check Large Files
```
"Find all components over 300 lines that should be split"
```

### Example: TypeScript Focus
```
"Check my project for TypeScript type safety issues"
```

### Example: Context-Specific
```
"Analyze all my Context providers for performance"
```
