# How to Use Code Refactoring Assistant

Hey Claude—I just added the code-refactoring-assistant skill. Analyze the current codebase for refactoring opportunities by impact scope.

## Example Invocations

**Example 1: Generate Checklist**
@[code-refactoring-assistant] Scan repo with Glob(&quot;**/*.py&quot;), create low-impact refactor checklist for modularity.

**Example 2: Interactive Review**
After checklist: Approve item 0 (yes), skip item 1 (no), feedback on item 2: &quot;Reduce scope&quot;.

**Example 3: Execute & Report**
Execute approved refactors, run QA with pytest, generate before/after report.

## What to Provide
- Repo context (use @codebase-analyzer or Glob/Grep)
- Goals: &quot;improve performance&quot;, &quot;add tests&quot;
- Review decisions as JSON

## What You&#x27;ll Get
- Impact-sorted checklist
- Diffs for changes
- QA metrics (tests/style/perf)
- Markdown report with tables/comparisons

Test with sample_input.json via Python stdin.
