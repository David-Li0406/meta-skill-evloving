# Amendment Process

## Phase 1 - Analyze Current State

1. **Read Constitution**
   - Load `.specify/memory/constitution.md`
   - Parse all 9 principles
   - Identify version and last update date

2. **Detect Context**
   - Violation: Implementation conflicts with principle
   - Gap: New pattern not covered by existing principles
   - Clarification: Existing principle ambiguous
   - Update: Principle needs refinement

## Phase 2 - Propose Changes

3. **Generate Proposal**
   - **For Violations**: Suggest code fix vs principle amendment
   - **For Gaps**: Draft new principle or extend existing
   - **For Clarification**: Propose clarifying language
   - **For Updates**: Show before/after comparison

4. **Rationale**
   - Explain why change is needed
   - Show impact on existing code
   - Identify affected templates and docs

## Phase 3 - User Approval

5. **Present Proposal**

   ```markdown
   ## Constitution Amendment Proposal

   **Type**: [Violation Fix | New Principle | Clarification | Update]
   **Affected Principle**: [Principle Number/Name]

   ### Current State
   [Show existing principle text]

   ### Proposed Change
   [Show new/updated principle text]

   ### Rationale
   [Why this change is needed]

   ### Impact Analysis
   - Affected files: [count]
   - Breaking changes: [yes/no]
   - Template updates required: [list]

   ### Recommendation
   [Approve | Reject | Modify]
   ```

6. **User Decision**
   - Approve → Proceed to Phase 4
   - Reject → Exit with explanation
   - Modify → Iterate on proposal

## Phase 4 - Apply Changes

7. **Update Constitution**
   - Bump version (v1.1.0 → v1.2.0 for new principles)
   - Update last modified date
   - Add changelog entry
   - Write to `.specify/memory/constitution.md`

8. **Synchronize Templates**
   - Update affected templates in `.claude/commands/speckit.*.md`
   - Sync principle references in `help.md`
   - Update `README.md` if needed
   - Regenerate any auto-generated docs

9. **Validate Consistency**
   - Verify all templates reference correct version
   - Check no orphaned principle references
   - Ensure numbering consistency

## Phase 5 - Report

10. **Generate Change Summary**

    ```markdown
    ✅ Constitution Updated: v1.2.0

    **Changes**:
    - Updated Principle VII: Type Safety
      - Added exception for RPC type assertions

    **Synchronized Templates**:
    - .claude/commands/speckit.specify.md
    - .claude/commands/help.md
    - README.md

    **Next Steps**:
    - Review changes: git diff .specify/memory/constitution.md
    - Commit: "docs(constitution): Update Principle VII - Type Safety"
    - Inform team of new version
    ```

## Violation Handling

### Critical Violations (NON-NEGOTIABLE)

1. **Stop implementation immediately**
2. Invoke `skill:constitution` with violation context
3. **Options**:
   - Fix code to comply
   - Propose Constitution amendment (requires strong rationale)
4. **Never proceed** without resolution

### Minor Violations (FLEXIBLE)

1. **Document exception** in code comments
2. Invoke `skill:constitution` for clarification
3. **Options**:
   - Add exception to principle
   - Fix code if straightforward
4. **May proceed** with documented justification
