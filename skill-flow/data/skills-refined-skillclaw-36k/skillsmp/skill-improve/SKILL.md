---
name: skill-improve
description: This skill should be used when improving existing Claude Code skills. Triggers include "improve this skill", "skill feels shallow", "upgrade skill", or when self-evaluating skill quality. Codifies the self-eval -> research -> rewrite -> validate -> artifact pattern.
---

# skill-improve

systematic improvement of claude code skills. turns shallow guidance into decision-ready playbooks with validated artifacts.

## philosophy

> "a skill is only as good as the decision it enables"

| principle | application |
|-----------|-------------|
| primary sources | read real code and official docs, not summaries |
| decision trees | express if/then logic for common scenarios |
| concrete values | cite constants with file/line or URL |
| tool integration | connect to the user's existing CLI and workflows |
| evidence over vibes | every claim has a source or example |
| validation required | pair review before declaring done |
| reusable prose lives in prompts | keep SKILL.md tight, link to prompts |

## when to use

| use | skip |
|-----|------|
| skill feels shallow or generic | skill is newly created (use skill-create) |
| weighted score < 8 on self-eval | minor typo or formatting fixes |
| missing decision trees or values | deleting a skill |
| periodic skill audits | skill has recent validation evidence |
| skill-audit identified gaps | cosmetic changes only |

## decision tree: improvement scope

```
Should I patch or rewrite?
├── Weighted score >= 8 and only 1-2 gaps?
│   └── patch (surgical edits, keep structure)
├── Weighted score 5-7 or missing core sections?
│   └── rewrite (replace structure, keep intent)
├── Weighted score <= 4 or wrong domain fit?
│   └── rebuild (new structure + new sources)
└── Conflicting instructions?
    └── ask user for direction
```

## decision tree: skill type assessment

```
What type of skill is this?
├── Orchestrates multi-step workflows?
│   └── workflow skill (loop, auto, skill-compose)
│       └── needs: phases, decision trees, tool integration
├── Provides domain expertise?
│   └── domain skill (emil-kowalski, imessage)
│       └── needs: concrete values, examples, voice guidance
├── Wraps a tool or CLI?
│   └── tool skill (test-pilot, pr-audit)
│       └── needs: command reference, patterns, error handling
├── Meta (about skills)?
│   └── meta skill (skill-create, skill-improve, skill-audit)
│       └── needs: evaluation criteria, process steps
└── External integration?
    └── integration skill (slack, context)
        └── needs: API patterns, auth, error handling
```

## decision tree: gap prioritization

```
Which gaps should I fix first?
├── 0 decision trees?
│   └── CRITICAL: add decision trees first (skill is broken)
├── No concrete values?
│   └── HIGH: extract values from sources
├── Missing when-to-use table?
│   └── HIGH: add trigger conditions
├── No anti-patterns?
│   └── MEDIUM: document common mistakes
├── Thin references (<50 lines)?
│   └── MEDIUM: expand with patterns
├── Missing tool integration?
│   └── MEDIUM: add CLI examples
└── Workflow unclear?
    └── LOW: restructure phases
```

## decision tree: research depth

```
How deep should research go?
├── Missing concrete values or defaults?
│   └── Tier 1: source code required
├── New domain or tool?
│   └── Tier 1 + Tier 2: code + official docs
├── Wording or structure only?
│   └── Tier 2: docs sufficient
├── Need patterns from codebase?
│   └── Reference: arbor/koto/kumori patterns
└── Unsure?
    └── Default to Tier 1 + Tier 2
```

## decision tree: source selection

```
Where should I look for sources?
├── Tool/CLI skill?
│   ├── Source code → `outline --search=X src/`
│   ├── Config files → glob for *.config.*
│   └── Tests → fd -e test.ts
├── Domain skill?
│   ├── Reference implementations → arbor, koto, kumori
│   ├── Industry standards → web search
│   └── User patterns → git log of related changes
├── Workflow skill?
│   ├── Existing workflows → loop, auto, pair
│   ├── User's AGENTS.md → ~/AGENTS.md
│   └── CLI tools → utils help output
└── Integration skill?
    ├── API docs → ref_search_documentation
    ├── SDK source → outline of SDK
    └── Error messages → grep for throw/error
```

## decision tree: validation routing

```
What validation is required?
├── Major rewrite or new decision trees?
│   └── pair thorough + artifact + pair quick
├── Medium edits with new values?
│   └── pair thorough (or quick if confidence >= 8)
├── Small patch?
│   └── pair quick
└── Confidence < 7?
    └── ask user or HIL
```

## decision tree: artifact selection

```
What artifact should I create?
├── Tool skill?
│   └── Working command examples with real output
├── Domain skill?
│   └── Example applying domain expertise
├── Workflow skill?
│   └── Trace of workflow execution
├── Integration skill?
│   └── Successful API call or integration test
└── Meta skill?
    └── Self-application (improve the improver)
```

## concrete values

| metric | target | source |
|--------|--------|--------|
| decision tree count | >= 5 covering 80% scenarios | gold standard skills (loop: 35, pair: 14) |
| concrete values count | >= 5 with sources | healthy skills have 5-10 |
| anti-pattern count | >= 5 with fixes | healthy skills have 5-10 |
| reference depth | >= 50 lines each | meaningful patterns, not stubs |
| SKILL.md length | 200-400 lines | enough depth, not overwhelming |
| when-to-use table | >= 4 use cases | clear triggers |
| self-eval threshold | < 8 triggers improvement | `references/evaluation-rubric.md` |
| validation confidence | >= 8 to pass | pair skill routing |

## self-evaluation rubric (quick)

```
| dimension | weight | scoring |
|-----------|--------|---------|
| decision trees | 2x | 0=none, 5=1-2, 10=5+ |
| concrete values | 2x | 0=none, 5=generic, 10=sourced |
| anti-patterns | 1x | 0=none, 5=3-4, 10=5+ |
| references | 1x | 0=stubs, 5=<50 lines, 10=50+ |
| tool integration | 1x | 0=none, 5=basic, 10=comprehensive |
| when-to-use | 1x | 0=none, 5=vague, 10=clear table |

Weighted score = sum(score × weight) / sum(weights)
```

quick scoring template:
```
Skill: [name]
Date: [YYYY-MM-DD]

| dimension | score | weight | notes |
|-----------|-------|--------|-------|
| decision trees | /10 | 2x | |
| concrete values | /10 | 2x | |
| anti-patterns | /10 | 1x | |
| references | /10 | 1x | |
| tool integration | /10 | 1x | |
| when-to-use | /10 | 1x | |

Weighted: /10
Action: [patch/rewrite/rebuild]
```

## workflow

### phase 1: assess

```bash
# read the skill
Read /Users/luke/Developer/skills/{skill}/SKILL.md

# check references
ls /Users/luke/Developer/skills/{skill}/references/

# count decision trees
grep -c "decision tree" SKILL.md

# score using rubric
```

### phase 2: diagnose gaps

| signal | gap | action |
|--------|-----|--------|
| no decision tree | missing control flow | add decision tree for top scenarios |
| vague values | no concrete constants | extract from source code |
| generic tooling | no user integration | add CLI commands |
| no anti-patterns | missing failure guidance | add pitfalls + fixes |
| thin references | stubs or <50 lines | expand with patterns |

### phase 3: research

```bash
# for tool skills - read source
outline --callers=functionName src/

# for domain skills - check reference projects
layer ~/Developer/arbor/arbor-xyz
fd -e ts . ~/Developer/arbor/arbor-xyz/packages/backend/convex | head -20

# for workflow skills - check existing patterns
Read /Users/luke/Developer/skills/loop/SKILL.md

# for any skill - search docs
ref_search_documentation "{tool} {feature} guide"
```

### phase 4: rewrite

structure template:
```markdown
---
name: skill-name
description: trigger description
---

# skill-name

one-line purpose.

## philosophy
| principle | application |

## when to use
| use | skip |

## decision tree: {scenario}
```
{tree}
```

## concrete values
| item | value | source |

## workflow
### phase N: name
{steps}

## anti-patterns
| pattern | problem | fix |

## output contract
```json
{schema}
```

## references
- [references/X.md](references/X.md) - description
```

### phase 5: validate

use pair skill for external validation:

```bash
# pair thorough for major rewrites
cat <<'EOF' | codex exec - --full-auto -o /tmp/skill-review.json
Skill depth review.

Skill: {skill_name}
Content: {SKILL.md content}

Validate:
1. Decision trees present and actionable?
2. Concrete values from primary sources?
3. Tool integration with user's setup?
4. Anti-patterns documented?
5. Would domain expert recognize as informed?

Output JSON only:
{"pass":true,"depth_score":8,"issues":[],"confidence":9}
EOF

# poll for response
while [ ! -f /tmp/skill-review.json ]; do sleep 5; done
```

### phase 6: finalize

- verify line counts (aim for 200-400 in SKILL.md)
- ensure references are substantive (>50 lines each)
- update references with new findings
- commit with descriptive message

## tool integration

| tool | command | purpose |
|------|---------|---------|
| layer | `layer /Users/luke/Developer/skills` | skill structure overview |
| outline | `outline src/ --stats` | code analysis for tool skills |
| codex | `codex exec - --full-auto -o /tmp/response.json` | deep validation |
| copilot | `copilot -p --model gemini-3-pro` | quick assessment |
| ref | `ref_search_documentation`, `ref_read_url` | documentation lookup |
| trails | `trails trail record` | improvement history persistence |

### trails integration

persist improvement sessions for progress tracking:

```bash
# record improvement completion
trails trail record --agent claude --action completed \
  --task "skill-improve: $SKILL_NAME - score $BEFORE→$AFTER" \
  --confidence $CONFIDENCE --json -q
```

**trails enables**:
- tracking skill improvement velocity
- measuring score progression
- correlating improvements with usage

### example commands

```bash
# exploration
layer /Users/luke/Developer/skills    # structure
outline src/ --stats                   # if applicable

# reference projects
layer ~/Developer/arbor/arbor-xyz     # gold standard repo
fd -e ts . packages/backend/convex    # find patterns

# documentation
ref_search_documentation "{tool} {feature}"
ref_read_url "https://docs.example.com/path"

# validation
cat prompt | codex exec - --full-auto -o /tmp/response.json
copilot -p --model gemini-3-pro --output-format json "prompt"
```

## anti-patterns

| pattern | problem | fix |
|---------|---------|-----|
| web-scrape only | misses implementation details | read source code or official docs |
| philosophy without action | no executable decisions | add if/then decision tree |
| generic values | vague ranges without source | cite exact constants from code |
| skip validation | no proof of depth | require pair review |
| improvement without artifact | no applied proof | create real artifact |
| burying prose in SKILL.md | hard to reuse | move to prompts and link |
| endless rewrite loops | no new sources | cap to 2 cycles, then ask |
| counting without quality | trees exist but useless | trees must have conditional logic |
| over-engineering | 50 decision trees | 5-15 is healthy range |
| stale references | referenced files don't exist | verify all links |

## output contract

```json
{
  "mode": "improve",
  "status": "success | partial | blocked",
  "summary": "improved {skill}: added 5 decision trees, 8 concrete values, expanded references",
  "confidence": 8,
  "artifacts": [
    { "type": "file", "path": "skills/{skill}/SKILL.md", "status": "updated" },
    { "type": "file", "path": "skills/{skill}/references/X.md", "status": "created" }
  ],
  "sources": {
    "prompts": [],
    "files_read": ["loop/SKILL.md", "pair/SKILL.md"]
  },
  "verification": {
    "before_score": 6,
    "after_score": 8,
    "pair_review": "passed",
    "decision_trees_added": 5
  }
}
```

## references

- [references/evaluation-rubric.md](references/evaluation-rubric.md) - detailed scoring criteria
- [references/research-patterns.md](references/research-patterns.md) - primary source methodology
- [references/artifact-examples.md](references/artifact-examples.md) - validation artifacts by type
- [references/skill-anatomy.md](references/skill-anatomy.md) - ideal skill structure
