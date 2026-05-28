# composition examples

detailed examples of multi-skill workflows.

## example 1: skill improvement pipeline

**goal:** create and validate a new skill end-to-end

**skills involved:**
1. create-skill - scaffold new skill
2. skill-improve - enhance with primary sources
3. consult-deep - thorough validation
4. artifact creation - prove it works
5. consult-light - validate artifact
6. slack - notify completion

**execution:**

```bash
# step 1: create-skill
# [invoke create-skill, produces ~/.claude/skills/new-skill/]

# step 2: skill-improve
# [invoke skill-improve on new-skill]
# output: improved SKILL.md, references/

# step 3: consult-deep
VALIDATION=$(cat <<'EOF' | codex exec --model "gpt-5.2-codex xhigh"
Skill depth review.
Skill: new-skill
Content: [improved SKILL.md]
Output JSON: {pass, depth_score, confidence}
EOF
)

# check: if depth_score < 8, loop back to step 2

# step 4: create artifact
# [create something using the skill]

# step 5: consult-light
ARTIFACT_CHECK=$(cat <<'EOF' | copilot -p --model gemini-3-pro
Artifact validation.
Artifact: [description]
Principles: [from skill]
Output JSON: {pass, score, confidence}
EOF
)

# step 6: notify
echo "New skill created and validated: new-skill
- Depth: ${VALIDATION.depth_score}/10
- Artifact: ${ARTIFACT_CHECK.score}/10" | slack dm send --user luke
```

**handoffs:**

| step | produces | consumed by |
|------|----------|-------------|
| create-skill | skill directory | skill-improve |
| skill-improve | improved content | consult-deep |
| consult-deep | validation JSON | decision gate |
| artifact | real usage | consult-light |
| consult-light | validation JSON | slack |

## example 2: autonomous issue work

**goal:** pick up Linear issue and work until done

**skills involved:**
1. issue-context - enrich issue
2. consult-light - validate approach
3. loop - autonomous execution
4. pr-audit - review changes
5. slack - notify completion

**execution:**

```bash
# step 1: enrich issue
CONTEXT=$(linear issue view ARB-123 --json | issue-context)

# step 2: consult on approach
APPROACH=$(cat <<'EOF' | copilot -p --model gemini-3-pro
Approach check.
Issue: ARB-123 - [title]
Context: $CONTEXT
Question: Is this approach sound?
Output JSON: {approved: bool, concerns: [], confidence}
EOF
)

# gate: if not approved or confidence < 7, escalate to human

# step 3: loop execution
# [invoke loop skill with issue context]
# produces: code changes, tests, PR

# step 4: pr-audit
AUDIT=$(pr-audit --pr=456)

# gate: if audit fails, loop back to fix issues

# step 5: notify
echo "ARB-123 complete
- PR: #456
- Audit: ${AUDIT.status}
- Tests: passing" | slack dm send --user luke
```

## example 3: research and synthesis

**goal:** answer complex question with multi-source research

**skills involved:**
1. deep-ask - gather requirements
2. parallel research - multiple sources
3. consult-deep - synthesize
4. metaprompt-factory - create reusable prompt

**execution:**

```bash
# step 1: deep-ask to clarify
# [invoke deep-ask, get user answers]

# step 2: parallel research
# run concurrently:
REF_DOCS=$(mcp__Ref__ref_search_documentation "topic")
CODEBASE=$(outline --search=topic src/)
SLACK_CONTEXT=$(slack search messages -q "topic" -w workspace)

# step 3: synthesize
SYNTHESIS=$(cat <<'EOF' | codex exec --model "gpt-5.2-codex xhigh"
Synthesis task.
Question: [from deep-ask]
Sources:
- Documentation: $REF_DOCS
- Codebase: $CODEBASE
- Discussions: $SLACK_CONTEXT
Synthesize comprehensive answer.
EOF
)

# step 4: create reusable prompt
# [invoke metaprompt-factory with synthesis as input]
```

## example 4: skill audit and batch improve

**goal:** audit all skills and improve lowest-scoring ones

**skills involved:**
1. skill-audit - inventory all skills
2. skill-improve (batch) - improve each
3. consult-deep - validate improvements
4. slack - report results

**execution:**

```bash
# step 1: audit
AUDIT_RESULTS=$(skill-audit)

# step 2: filter to low-scoring
LOW_SKILLS=$(echo $AUDIT_RESULTS | jq '[.skills[] | select(.depth < 6)]')

# step 3: improve each (sequential)
for skill in $LOW_SKILLS; do
  # invoke skill-improve
  # invoke consult-deep
  # if passed, continue; else flag for manual review
done

# step 4: report
echo "Skill improvement batch complete
- Audited: ${AUDIT_RESULTS.total}
- Improved: ${#LOW_SKILLS[@]}
- Still need work: [list]" | slack dm send --user luke
```

## composition decision tree

```
What kind of task?
├── Create something new
│   └── create-skill → skill-improve → validate
├── Improve existing
│   └── skill-audit → skill-improve → validate
├── Execute work
│   └── issue-context → consult-light → loop → pr-audit
├── Research
│   └── deep-ask → parallel sources → consult-deep
└── Communicate
    └── [any skill] → format → slack/imessage
```
