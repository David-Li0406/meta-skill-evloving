---
name: orchestrating-knowledge-workflows
description: Use when implementing plan-build-improve cycles for content updates. Triggers on "knowledge workflow", "plan then build", "spec-driven implementation".
---

# Orchestrating Knowledge Workflows

Guide for managing the complete plan-build-improve cycle when making knowledge base updates. The spec-as-contract pattern ensures review before implementation.

## Instructions

### Step 1: Plan Stage - Create Specification

Before any implementation, create a spec document:

1. **Analyze the requirement**
   - Identify core concepts and learning
   - Search existing content with Grep/Glob to assess coverage
   - Determine entry strategy: new file vs extend existing

2. **Write spec to `.claude/.cache/specs/knowledge/{slug}-spec.md`**
   ```markdown
   # Spec: {Title}

   ## Requirement
   {Original user requirement}

   ## Analysis
   - Existing coverage: {files that touch this topic}
   - Gap identified: {what's missing}
   - Entry strategy: {new | extend | journal}

   ## Plan
   - Target file: {absolute path}
   - Changes: {bullet list of content additions}
   - Cross-references: {other files to update}
   - Voice notes: {tone guidance from existing content}

   ## Verification
   - [ ] Content aligns with STYLE_GUIDE.md
   - [ ] Frontmatter updated (last_updated, tags)
   - [ ] Cross-references added
   ```

### Step 2: Review Stage - User Approval

Present spec to user before proceeding:

- Show spec location and summary
- Ask: "Ready to proceed with implementation?"
- Options: Yes / No (review first) / Edit spec then continue

**If user declines**: Save spec path, report how to resume later. This is valid - not an error.

### Step 3: Build Stage - Implement from Spec

Execute the spec faithfully:

1. **Load specification** - Read the spec file
2. **Review target context** - Read existing content if extending
3. **Implement content changes**
   - New file: Create with proper frontmatter
   - Extend: Add sections preserving voice
   - Journal: Add dated entry
4. **Add cross-references** - Update related files
5. **Update metadata** - Set `last_updated` in frontmatter
6. **Verify** - Check spec verification items

### Step 4: Improve Stage - Update Expert Knowledge

After successful build, extract learnings:

1. **Review what was built** - Compare spec to implementation
2. **Extract patterns**
   - What worked well?
   - What was harder than expected?
   - Any anti-patterns discovered?
3. **Update expertise** - Record learnings for future workflows
4. **Document anti-patterns** - What to avoid next time

**Note**: Improve stage is optional. If it fails, log but don't fail overall workflow.

### Step 5: Report Results

```markdown
## Knowledge Workflow Complete

**Requirement:** {original requirement}

### Stages

| Stage | Status | Output |
|-------|--------|--------|
| Plan | Complete | {spec_path} |
| Build | Complete | {file_count} files modified |
| Improve | Complete/Skipped | {expertise notes} |

### Files Modified

- {list of absolute paths with brief descriptions}

### Specification

Saved at: {spec_path}

Resume later with: "Build from spec at {spec_path}"
```

## Key Principles

**Spec-as-Contract Pattern**
- Spec is the single source of truth for what to build
- User reviews spec before implementation begins
- Changes to scope require spec update first
- Spec persists even if build fails (can retry)

**Sequential Execution**
- Plan -> Review -> Build -> Improve runs in order
- Each stage depends on previous stage output
- Don't parallelize this workflow

**User Control Points**
- Review after plan, before build
- User can edit spec and continue
- Declining to proceed is valid outcome

**Graceful Degradation**
- Build failure: Preserve spec, suggest retry
- Improve failure: Log but don't fail workflow
- Partial success is reported, not hidden

## Examples

### Example 1: Capture new insight
```
User: "Add insight about prompt caching to chapter 4"

Plan:
- Grep chapter 4 for existing caching content
- Determine best section to extend
- Write spec with specific additions

Build:
- Read target section
- Add caching insight preserving voice
- Update frontmatter

Report: "Added to chapters/4-context/2-context-strategies.md"
```

### Example 2: New mental model
```
User: "Create entry for 'specs as source code' mental model"

Plan:
- Check chapter 8 structure
- Identify next section number
- Write spec for new file

Build:
- Create chapters/8-mental-models/3-specs-as-source-code.md
- Add proper frontmatter
- Write content following STYLE_GUIDE

Report: "Created new entry with frontmatter order 3.8.3"
```

### Example 3: Resume from spec
```
User: "Build from spec at .claude/.cache/specs/knowledge/prompt-caching-spec.md"

Skip plan stage (spec exists)
Skip review stage (user explicitly requesting build)
Execute build from spec
Run improve stage
```

### Example 4: User declines at review
```
Plan stage completes, spec written
User: "No, stop here - I'll review the spec first"

Report:
- Spec location: {path}
- Resume with: "Build from spec at {path}"
- Workflow paused (valid outcome)
```
