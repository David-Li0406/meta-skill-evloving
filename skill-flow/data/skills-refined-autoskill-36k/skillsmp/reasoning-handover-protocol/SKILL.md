---
name: reasoning-handover-protocol
description: Protocol for cognitive pattern handovers during complex reasoning sessions. Defines .reasoning/ directory structure, handover schemas, and IR-v2 orchestration integration. Use when reasoning sessions require mid-stream pattern transitions, parallel branch merging, state checkpointing, or multi-pattern orchestration. Essential for complex problems where ToT, BoT, HE, or other patterns must hand off work to each other.
license: MIT
---

# Reasoning Handover Protocol

**Purpose**: Standardized protocol for preserving and transferring cognitive state between reasoning patterns during complex analysis sessions. Enables seamless handovers between ToT, BoT, SRC, HE, AR, DR, AT, RTR, and NDF patterns while maintaining evidence chains, confidence scores, and exploration history.

## When to Use This Protocol

**Use the Reasoning Handover Protocol when:**
- IR-v2 orchestrator transitions between patterns mid-session
- Parallel reasoning branches need to merge results
- Long-running analysis requires checkpointing
- Multiple patterns collaborate on the same problem
- Sessions need to be paused and resumed
- Post-hoc audit of reasoning process is required

**Do not use when:**
- Single-pattern analysis is sufficient
- Analysis completes within one interaction
- No state preservation needed

---

## Part 1: Directory Structure Specification

### 1.1 Root Directory: `.reasoning/`

The `.reasoning/` directory serves as the persistent workspace for cognitive reasoning sessions. It maintains session state, handover files, and evidence chains across pattern transitions.

```
.reasoning/
├── sessions/
│   └── session-{uuid}/
│       ├── manifest.json              # Session metadata and state
│       ├── pattern-state/             # Per-pattern working state
│       │   ├── tot/
│       │   │   ├── state.json         # ToT-specific state
│       │   │   └── branches/          # Branch exploration data
│       │   ├── bot/
│       │   │   ├── state.json         # BoT-specific state
│       │   │   └── approaches/        # Approach exploration data
│       │   ├── he/
│       │   │   ├── state.json         # HE-specific state
│       │   │   └── hypotheses/        # Hypothesis tracking
│       │   └── {pattern}/             # Other patterns follow same structure
│       ├── handovers/                 # Pattern-to-pattern handover records
│       │   └── {sequence}-{from}-to-{to}.json
│       ├── checkpoints/               # Mid-reasoning save points
│       │   └── checkpoint-{timestamp}.json
│       ├── evidence/                  # Shared evidence repository
│       │   ├── gathered/              # Evidence files
│       │   └── index.json             # Evidence registry
│       └── synthesis/                 # Final outputs
│           └── conclusion-{timestamp}.json
├── templates/                         # Reusable handover templates
│   └── {pattern}-handover-template.json
└── config.json                        # Global configuration
```

### 1.2 Session Directory: `session-{uuid}/`

Each reasoning session gets a unique directory identified by UUID.

**Session UUID Format**: `YYYYMMDD-HHMMSS-{random8}`
Example: `20260118-143052-a7b3c9d2`

**Directory Lifecycle:**
1. **Created**: When IR-v2 orchestrator initiates multi-pattern analysis
2. **Active**: During reasoning (state updated continuously)
3. **Completed**: When synthesis finalized
4. **Archived**: After 30 days (move to `.reasoning/archive/`)

### 1.3 Manifest File: `manifest.json`

The manifest tracks session-level metadata and current state.

```json
{
  "session_id": "20260118-143052-a7b3c9d2",
  "created_at": "2026-01-18T14:30:52Z",
  "last_updated": "2026-01-18T15:45:23Z",
  "status": "active|completed|paused|failed",

  "problem": {
    "statement": "Design authentication system for multi-tenant SaaS",
    "constraints": ["SOC2 compliance", "< 100ms latency", "10M users"],
    "success_criteria": ["Security validated", "Performance tested", "Cost acceptable"]
  },

  "orchestration": {
    "strategy": "sequential|parallel|nested",
    "planned_patterns": ["BoT", "ToT", "AR"],
    "current_pattern": "ToT",
    "pattern_history": [
      {"pattern": "BoT", "started": "...", "completed": "...", "handover_to": "ToT"}
    ]
  },

  "dimensions": {
    "sequential_dependencies": 2,
    "criteria_clarity": 4,
    "solution_space_known": 3,
    "single_answer_needed": 4,
    "evidence_available": 3,
    "opposing_valid_views": 3,
    "problem_novelty": 3,
    "robustness_required": 5,
    "solution_exists": 2,
    "time_pressure": 2,
    "stakeholder_complexity": 2
  },

  "confidence": {
    "overall": 0.72,
    "by_pattern": {
      "BoT": 0.75,
      "ToT": 0.78
    }
  },

  "checkpoints": ["checkpoint-20260118-150000.json"],
  "active_handover": null
}
```

---

## Part 2: Handover Schema Specification

### 2.1 Universal Handover Format

All pattern-to-pattern handovers follow this base schema:

```json
{
  "$schema": "reasoning-handover-v1",
  "handover_id": "003-bot-to-tot",
  "timestamp": "2026-01-18T15:00:00Z",

  "source_pattern": {
    "name": "BoT",
    "version": "1.0",
    "session_state_path": "./pattern-state/bot/state.json"
  },

  "target_pattern": {
    "name": "ToT",
    "version": "1.0",
    "recommended_entry_point": "step-3-evaluation"
  },

  "context_transfer": {
    "problem_understanding": "...",
    "constraints_identified": ["..."],
    "assumptions_made": ["..."]
  },

  "deliverables": {
    "type": "approaches|branches|hypotheses|synthesis",
    "items": [],
    "confidence_scores": {}
  },

  "evidence_chain": {
    "sources_used": ["..."],
    "key_findings": ["..."],
    "reference_paths": ["./evidence/gathered/..."]
  },

  "recommendations": {
    "focus_areas": ["..."],
    "avoid_areas": ["..."],
    "open_questions": ["..."]
  },

  "metadata": {
    "duration_minutes": 25,
    "branches_explored": 8,
    "branches_retained": 5,
    "confidence_at_handover": 0.75
  }
}
```

### 2.2 Pattern-Specific Handover Extensions

#### BoT (Breadth of Thought) Handover

When BoT hands off to another pattern:

```json
{
  "bot_specific": {
    "exploration_summary": {
      "level_0_approaches": 8,
      "level_1_subapproaches": 32,
      "total_explored": 40,
      "retained_above_40pct": 18
    },

    "approach_registry": [
      {
        "id": "approach-1",
        "name": "Write-through caching",
        "level": 0,
        "confidence": 0.72,
        "status": "retained",
        "strengths": ["..."],
        "weaknesses": ["..."],
        "best_for": "Strong consistency requirements",
        "subapproaches": ["1.1", "1.2", "1.3"]
      }
    ],

    "pruned_approaches": [
      {
        "id": "approach-6",
        "name": "Blockchain-based cache",
        "pruned_reason": "Complexity exceeds benefit, confidence 28%",
        "pruned_at": "level-0"
      }
    ],

    "top_5_viable": ["approach-2", "approach-1", "approach-4", "approach-3", "approach-7"],

    "handover_recommendation": {
      "to_tot": "Evaluate top 3 approaches against defined criteria",
      "to_he": "If problem is diagnosis, use approaches as hypothesis set",
      "to_ar": "Validate top approach before implementation"
    }
  }
}
```

#### ToT (Tree of Thoughts) Handover

When ToT hands off to another pattern:

```json
{
  "tot_specific": {
    "tree_structure": {
      "total_levels": 4,
      "branches_per_level": [5, 5, 5, 5],
      "winning_path": ["branch-2", "branch-2.3", "branch-2.3.4", "branch-2.3.4.2"]
    },

    "branch_scores": {
      "branch-2": {
        "novelty": 18,
        "feasibility": 19,
        "completeness": 17,
        "confidence": 18,
        "alignment": 19,
        "total": 91
      }
    },

    "winning_solution": {
      "path": "L0:Eventual-consistency > L1:CRDTs > L2:OR-Set > L3:Tombstone-compaction",
      "final_score": 91,
      "confidence": 0.88,
      "key_insight": "CRDTs provide eventual consistency without coordination overhead"
    },

    "alternatives_considered": [
      {
        "path": "L0:Write-through > L1:Redis-cluster",
        "final_score": 78,
        "why_not_selected": "Latency requirements not met under load"
      }
    ],

    "handover_recommendation": {
      "to_ar": "Validate CRDT approach against adversarial scenarios",
      "to_src": "Trace implementation steps for CRDT integration",
      "to_he": "If issues arise, use pruned branches as hypothesis set"
    }
  }
}
```

#### HE (Hypothesis-Elimination) Handover

When HE hands off to another pattern:

```json
{
  "he_specific": {
    "hypothesis_registry": [
      {
        "id": "H1",
        "name": "Memory leak in connection pool",
        "initial_probability": 0.3,
        "current_probability": 0.05,
        "status": "eliminated",
        "eliminated_by": "evidence-003",
        "elimination_reason": "Memory stable at 2GB, no growth over 4 hours"
      },
      {
        "id": "H3",
        "name": "Slow external API response",
        "initial_probability": 0.2,
        "current_probability": 0.85,
        "status": "confirmed",
        "confirmed_by": ["evidence-005", "evidence-007"],
        "mechanism": "Payment gateway P99 latency increased from 50ms to 800ms"
      }
    ],

    "evidence_chain": [
      {
        "id": "evidence-001",
        "type": "log_analysis",
        "source": "application-logs",
        "finding": "No OOM errors in last 24h",
        "hypotheses_affected": {
          "H1": "eliminated",
          "H2": "unchanged"
        }
      }
    ],

    "elimination_path": {
      "started_with": 12,
      "remaining": 1,
      "elimination_sequence": ["H1", "H5", "H2", "H8", "H4", "H6", "H7", "H9", "H10", "H11", "H12"]
    },

    "root_cause": {
      "hypothesis": "H3",
      "confidence": 0.85,
      "mechanism": "External payment API degradation causing request queuing",
      "confirmation_test": "Timeout reduction test showed immediate improvement"
    },

    "handover_recommendation": {
      "to_tot": "Evaluate mitigation options for external API dependency",
      "to_ar": "Stress-test proposed timeout configuration",
      "to_src": "Trace exact failure path through code"
    }
  }
}
```

#### SRC (Self-Reflecting Chain) Handover

When SRC hands off to another pattern:

```json
{
  "src_specific": {
    "chain_trace": [
      {
        "step": 1,
        "action": "Trace user click to event handler",
        "result": "Event handler found in UserSubmit.tsx:45",
        "confidence": 0.92,
        "dependencies": [],
        "backtracked": false
      },
      {
        "step": 2,
        "action": "Analyze event handler logic",
        "result": "Handler calls validateForm() then submitToAPI()",
        "confidence": 0.88,
        "dependencies": ["step-1"],
        "backtracked": false
      },
      {
        "step": 3,
        "action": "Check validateForm() return value",
        "result": "Validation passes, returns true",
        "confidence": 0.45,
        "dependencies": ["step-2"],
        "backtracked": true,
        "backtrack_reason": "Assumption about validation logic was wrong"
      },
      {
        "step": "3-revised",
        "action": "Re-examine validateForm() with edge case inputs",
        "result": "Validation fails silently on special characters",
        "confidence": 0.82,
        "dependencies": ["step-2"],
        "backtracked": false
      }
    ],

    "chain_confidence": {
      "overall": 0.82,
      "weakest_link": "step-3-revised",
      "strongest_link": "step-1"
    },

    "backtrack_log": [
      {
        "from_step": 3,
        "to_step": 3,
        "reason": "Logic error - assumed validation was comprehensive",
        "resolution": "Re-examined with edge cases"
      }
    ],

    "handover_recommendation": {
      "to_he": "If bug persists, generate hypotheses from chain findings",
      "to_tot": "Evaluate fix approaches for validation issue",
      "to_ar": "Test fix against adversarial inputs"
    }
  }
}
```

#### AR (Adversarial Reasoning) Handover

When AR hands off to another pattern:

```json
{
  "ar_specific": {
    "threat_model_summary": {
      "target": "JWT authentication system",
      "attack_categories_analyzed": ["Spoofing", "Tampering", "Information Disclosure", "Elevation"],
      "total_attacks_identified": 24,
      "critical": 2,
      "high": 5,
      "medium": 10,
      "low": 7
    },

    "critical_attacks": [
      {
        "id": "ATK-001",
        "name": "JWT algorithm confusion",
        "category": "Spoofing",
        "impact": 5,
        "feasibility": 4,
        "risk_score": 20,
        "description": "Attacker changes alg header from RS256 to HS256, signs with public key",
        "current_mitigation": "None",
        "recommended_mitigation": "Explicitly validate algorithm server-side",
        "status": "unmitigated"
      }
    ],

    "edge_cases_identified": [
      {
        "id": "EDGE-001",
        "category": "Timing",
        "scenario": "Token expiry during long request",
        "potential_failure": "Request fails midway through multi-step process",
        "test_case": "Submit 5-minute workflow with token expiring at minute 3"
      }
    ],

    "residual_risk": {
      "score": 0.25,
      "description": "After mitigations, supply chain and social engineering remain",
      "accepted_risks": ["Insider threat with DB access"],
      "deferred_risks": ["Nation-state level attacks"]
    },

    "handover_recommendation": {
      "to_tot": "Evaluate mitigation implementation approaches",
      "to_he": "If breach occurs, use attack paths as hypothesis starting point",
      "to_src": "Trace attack path through code for fix verification"
    }
  }
}
```

### 2.3 Confidence Score Transfer

Confidence scores must be recalibrated during handover:

```json
{
  "confidence_transfer": {
    "source_confidence": {
      "pattern": "BoT",
      "score": 0.75,
      "basis": "18 of 40 approaches retained above 40% threshold"
    },

    "transfer_adjustments": {
      "scope_change": -0.05,
      "information_loss": -0.03,
      "pattern_alignment": +0.02
    },

    "target_starting_confidence": {
      "pattern": "ToT",
      "score": 0.69,
      "rationale": "Starting ToT with pre-filtered approaches, slight uncertainty from scope narrowing"
    },

    "shared_assumption_discount": {
      "applied": true,
      "discount": -0.05,
      "reason": "Same LLM, same problem framing, potential shared blind spots"
    }
  }
}
```

---

## Cycle Detection

**Max Handover Chain Length**: 5 (prevents runaway chains)

**Cycle Detection Rules**:
1. Track all (from_pattern, to_pattern) pairs in manifest
2. If any pair repeats -> BLOCK handover
3. If chain length exceeds 5 -> BLOCK and synthesize current state

**Example Blocked Cycles**:
- AR -> BoT -> ToT -> AR (AR repeated)
- BoT -> ToT -> BoT (BoT repeated)

---

## Part 3: Integration Points

### 3.1 IR-v2 Orchestrator Integration

The IR-v2 orchestrator manages handovers through these integration points:

#### Orchestrator State Machine

```
                    +------------------+
                    |  Problem Input   |
                    +--------+---------+
                             |
                             v
                    +--------+---------+
                    |  IR-v2 Scoring   |
                    |  (11 dimensions) |
                    +--------+---------+
                             |
              +--------------+---------------+
              |                              |
              v                              v
     +--------+--------+            +--------+--------+
     | Single Pattern  |            | Multi-Pattern   |
     |   Execution     |            |  Orchestration  |
     +--------+--------+            +--------+--------+
              |                              |
              v                    +---------+---------+
     +--------+--------+           |                   |
     |    Result       |           v                   v
     +--------+--------+  +--------+--------+ +--------+--------+
              |           |   Sequential    | |    Parallel     |
              v           |   Orchestration | |  Orchestration  |
     +--------+--------+  +--------+--------+ +--------+--------+
     |   Synthesis     |           |                   |
     +-----------------+           v                   v
                          +--------+--------+ +--------+--------+
                          |    Handover     | |  Branch Merge   |
                          |    Protocol     | |    Protocol     |
                          +--------+--------+ +--------+--------+
                                   |                   |
                                   v                   v
                          +--------+-------------------+--------+
                          |          15-min Checkpoint          |
                          +-----------------+-------------------+
                                            |
                                            v
                          +-----------------+-------------------+
                          |              Synthesis              |
                          +------------------------------------+
```

#### Orchestrator Handover Commands

```python
# Pseudo-code for IR-v2 orchestrator integration

class ReasoningOrchestrator:

    def initiate_handover(self, from_pattern: str, to_pattern: str):
        """
        Trigger handover from one pattern to another.
        """
        # 1. Signal current pattern to prepare handover
        handover_data = self.active_pattern.prepare_handover()

        # 2. Write handover file
        handover_path = self.write_handover(
            from_pattern=from_pattern,
            to_pattern=to_pattern,
            data=handover_data
        )

        # 3. Update manifest
        self.manifest.pattern_history.append({
            "pattern": from_pattern,
            "completed": timestamp(),
            "handover_to": to_pattern,
            "handover_file": handover_path
        })

        # 4. Initialize target pattern with handover context
        self.active_pattern = self.load_pattern(to_pattern)
        self.active_pattern.load_handover(handover_path)

        # 5. Set checkpoint
        self.create_checkpoint()

    def merge_parallel_branches(self, branch_results: list):
        """
        Merge results from parallel pattern executions.
        """
        # 1. Validate all branches completed
        for branch in branch_results:
            if branch.status != "completed":
                raise IncompleteHandoverError(branch.id)

        # 2. Apply agreement analysis (from IR-v2)
        agreement = self.analyze_agreement(branch_results)

        # 3. Calculate merged confidence
        if agreement.type == "FULL_AGREEMENT":
            merged_confidence = max(b.confidence for b in branch_results) + 0.05
        elif agreement.type == "PARTIAL_AGREEMENT":
            agreeing = [b for b in branch_results if b.conclusion == agreement.majority]
            merged_confidence = (avg(b.confidence for b in agreeing) * 0.7 +
                               avg(b.confidence for b in disagreeing) * 0.15)
        else:
            merged_confidence = min(b.confidence for b in branch_results) - 0.10

        # 4. Create merge record
        merge_record = self.write_merge_record(
            branches=branch_results,
            agreement_type=agreement.type,
            merged_confidence=min(merged_confidence, 0.95)
        )

        return merge_record

    def checkpoint(self, reason: str = "scheduled"):
        """
        Create checkpoint for session recovery.
        """
        checkpoint = {
            "timestamp": timestamp(),
            "reason": reason,
            "manifest_snapshot": self.manifest.to_dict(),
            "active_pattern_state": self.active_pattern.get_state(),
            "evidence_index": self.evidence_repository.get_index(),
            "recovery_instructions": self.generate_recovery_instructions()
        }

        checkpoint_path = f"checkpoints/checkpoint-{timestamp()}.json"
        self.write_json(checkpoint_path, checkpoint)

        self.manifest.checkpoints.append(checkpoint_path)
```

### 3.2 Parallel Branch Merge Protocol

When patterns run in parallel (AT + BoT, for example), results must merge:

```json
{
  "$schema": "parallel-merge-v1",
  "merge_id": "merge-001",
  "timestamp": "2026-01-18T16:30:00Z",

  "branches": [
    {
      "pattern": "AT",
      "branch_id": "at-001",
      "conclusion": "Use microservices with event sourcing (analogous to banking ledgers)",
      "confidence": 0.72,
      "key_insight": "Financial audit trails provide proven pattern for event logs"
    },
    {
      "pattern": "BoT",
      "branch_id": "bot-001",
      "conclusion": "Top 3: Event sourcing (0.78), CQRS (0.71), Saga pattern (0.68)",
      "confidence": 0.78,
      "key_insight": "Event sourcing emerged as top approach from 8 explored"
    }
  ],

  "agreement_analysis": {
    "type": "FULL_AGREEMENT",
    "agreeing_on": "Event sourcing architecture",
    "confidence_boost": "+5%"
  },

  "merged_result": {
    "conclusion": "Event sourcing architecture (validated by both exploration and analogy)",
    "confidence": 0.83,
    "confidence_calculation": "max(0.72, 0.78) + 0.05 = 0.83",
    "synthesis": "Both analytical and analogical approaches converged on event sourcing. AT found banking analogy, BoT found it as top approach from systematic exploration."
  },

  "next_step": {
    "pattern": "AR",
    "rationale": "High-confidence solution needs adversarial validation before implementation"
  }
}
```

### 3.3 Checkpoint Protocol

Checkpoints enable session recovery and mid-reasoning pauses:

```json
{
  "$schema": "checkpoint-v1",
  "checkpoint_id": "checkpoint-20260118-150000",
  "created_at": "2026-01-18T15:00:00Z",
  "trigger": "scheduled|manual|error|handover",

  "session_state": {
    "session_id": "20260118-143052-a7b3c9d2",
    "active_pattern": "ToT",
    "pattern_phase": "step-3-evaluation",
    "elapsed_minutes": 30,
    "patterns_completed": ["BoT"],
    "patterns_pending": ["AR"]
  },

  "pattern_snapshot": {
    "pattern": "ToT",
    "current_level": 2,
    "branches_at_current_level": 5,
    "winning_branch_so_far": "branch-2.3",
    "confidence_so_far": 0.78,
    "work_remaining": "Levels 3-4 exploration, final synthesis"
  },

  "evidence_snapshot": {
    "evidence_count": 12,
    "evidence_index_path": "./evidence/index.json",
    "key_evidence": ["evidence-003", "evidence-007", "evidence-011"]
  },

  "recovery_instructions": {
    "to_resume": [
      "1. Load manifest from ./manifest.json",
      "2. Restore ToT state from ./pattern-state/tot/state.json",
      "3. Resume at Level 2, branch-2.3 expansion",
      "4. Continue ToT methodology step 4 (recursive depth)"
    ],
    "expected_time_to_complete": "20-30 minutes",
    "dependencies": "None - can resume independently"
  },

  "integrity_check": {
    "manifest_hash": "sha256:abc123...",
    "pattern_state_hash": "sha256:def456...",
    "evidence_hash": "sha256:ghi789..."
  }
}
```

---

## Part 4: Pattern-Specific State Formats

### 4.1 ToT State Format (`pattern-state/tot/state.json`)

```json
{
  "pattern": "ToT",
  "version": "1.0",
  "started_at": "2026-01-18T15:00:00Z",
  "current_phase": "step-4-recursive-depth",

  "tree": {
    "root": {
      "problem": "Design distributed caching system",
      "evaluation_criteria": ["latency", "consistency", "cost", "scalability"]
    },
    "levels": [
      {
        "level": 0,
        "branches": [
          {
            "id": "branch-1",
            "name": "Write-through caching",
            "analysis": "...",
            "self_reflection": {
              "confidence": 75,
              "strengths": ["Strong consistency"],
              "weaknesses": ["Higher latency"],
              "recommendation": "Continue if consistency is priority"
            },
            "scores": {
              "novelty": 12,
              "feasibility": 18,
              "completeness": 17,
              "confidence": 15,
              "alignment": 16,
              "total": 78
            },
            "status": "explored",
            "selected_for_depth": false
          }
        ],
        "winner": "branch-2",
        "winner_score": 85
      }
    ],
    "current_level": 2,
    "winning_path": ["branch-2", "branch-2.3"]
  },

  "exploration_stats": {
    "total_branches_explored": 15,
    "total_time_minutes": 25,
    "average_branch_confidence": 72
  }
}
```

### 4.2 BoT State Format (`pattern-state/bot/state.json`)

```json
{
  "pattern": "BoT",
  "version": "1.0",
  "started_at": "2026-01-18T14:30:00Z",
  "current_phase": "step-3-conservative-pruning",

  "exploration": {
    "problem": "Identify all viable data pipeline architectures",
    "level_0": {
      "approaches_generated": 8,
      "approaches": [
        {
          "id": "approach-1",
          "name": "Batch processing (ETL)",
          "overview": "Traditional extract-transform-load...",
          "strengths": ["Mature tooling", "Cost-effective for large batches"],
          "weaknesses": ["High latency", "Not real-time"],
          "feasibility": {
            "technical": "High",
            "operational": "Medium",
            "business": "High"
          },
          "confidence": 68,
          "status": "retained"
        }
      ],
      "pruned": ["approach-6", "approach-8"],
      "retained": 6
    },
    "level_1": {
      "expanded_from": ["approach-1", "approach-2", "approach-3", "approach-4", "approach-5", "approach-7"],
      "total_subapproaches": 30,
      "retained_above_40pct": 18
    }
  },

  "top_5_solutions": [
    {
      "path": "approach-2 > approach-2.3",
      "name": "Kafka + Flink streaming",
      "confidence": 78,
      "best_for": "Real-time analytics with exactly-once semantics"
    }
  ],

  "exploration_stats": {
    "total_branches_explored": 38,
    "pruned_count": 20,
    "retained_count": 18,
    "diversity_score": 0.85
  }
}
```

### 4.3 HE State Format (`pattern-state/he/state.json`)

```json
{
  "pattern": "HE",
  "version": "2.0",
  "started_at": "2026-01-18T14:00:00Z",
  "current_phase": "phase-4-confirmation",

  "symptom": "API returning 500 errors intermittently since 14:00",

  "hypotheses": [
    {
      "id": "H1",
      "name": "Memory exhaustion",
      "mechanism": "Container OOM causing crashes",
      "initial_probability": 0.25,
      "current_probability": 0.02,
      "status": "eliminated",
      "evidence_trail": [
        {"evidence": "E001", "impact": "eliminated", "timestamp": "14:15"}
      ]
    },
    {
      "id": "H3",
      "name": "External API timeout",
      "mechanism": "Payment gateway slow, causing request backup",
      "initial_probability": 0.20,
      "current_probability": 0.88,
      "status": "leading",
      "evidence_trail": [
        {"evidence": "E003", "impact": "strengthened", "timestamp": "14:25"},
        {"evidence": "E007", "impact": "strengthened", "timestamp": "14:40"}
      ]
    }
  ],

  "evidence_hierarchy": [
    {
      "id": "E001",
      "source": "Container metrics",
      "discrimination_power": 4,
      "acquisition_cost": 2,
      "priority_score": 2.0,
      "finding": "Memory stable at 2GB, no OOM events",
      "gathered_at": "14:15"
    }
  ],

  "elimination_progress": {
    "started_with": 10,
    "eliminated": 9,
    "remaining": 1,
    "elimination_sequence": ["H1", "H5", "H2", "H8", "H4", "H6", "H7", "H9", "H10"]
  },

  "confirmation_status": {
    "hypothesis": "H3",
    "prediction": "Reducing timeout from 30s to 5s will reduce 500 errors",
    "test_result": "500 errors dropped 95% after timeout change",
    "confidence": 0.88
  }
}
```

---

## Part 5: Evidence Repository

### 5.1 Evidence Index (`evidence/index.json`)

```json
{
  "session_id": "20260118-143052-a7b3c9d2",
  "evidence_count": 15,
  "last_updated": "2026-01-18T15:30:00Z",

  "evidence": [
    {
      "id": "E001",
      "type": "metric",
      "source": "prometheus:container_memory",
      "gathered_at": "2026-01-18T14:15:00Z",
      "gathered_by_pattern": "HE",
      "file_path": "./gathered/E001-memory-metrics.json",
      "summary": "Container memory stable at 2GB, no OOM events",
      "used_by_patterns": ["HE"],
      "hypotheses_affected": ["H1:eliminated", "H2:unchanged"]
    },
    {
      "id": "E003",
      "type": "log_analysis",
      "source": "application:logs:error",
      "gathered_at": "2026-01-18T14:25:00Z",
      "gathered_by_pattern": "HE",
      "file_path": "./gathered/E003-error-logs.txt",
      "summary": "Timeout errors spike at 14:02, correlates with payment gateway",
      "used_by_patterns": ["HE", "SRC"],
      "hypotheses_affected": ["H3:strengthened"]
    }
  ],

  "evidence_by_type": {
    "metric": ["E001", "E005", "E009"],
    "log_analysis": ["E002", "E003", "E006"],
    "code_analysis": ["E004", "E007"],
    "external_status": ["E008"],
    "reproduction": ["E010"]
  }
}
```

---

## Part 6: Usage Examples

### 6.1 Sequential Orchestration: BoT to ToT to AR

```markdown
## Session: Design authentication system
## Strategy: Sequential (BoT -> ToT -> AR)

### Phase 1: BoT Exploration

**Started**: 2026-01-18T14:30:00Z
**Duration**: 25 minutes

BoT explored 8 authentication approaches:
1. JWT with refresh tokens
2. Session-based with Redis
3. OAuth2 with external provider
4. Passwordless (magic links)
5. WebAuthn/FIDO2
6. Certificate-based (mTLS)
7. API keys with HMAC
8. Blockchain identity

**Retained (>40%)**: Approaches 1, 2, 3, 5, 6 (5 retained)
**Pruned (<40%)**: Approaches 4, 7, 8

**Handover to ToT**: ./handovers/001-bot-to-tot.json
**Deliverable**: Top 5 approaches for evaluation

---

### Phase 2: ToT Optimization

**Started**: 2026-01-18T14:55:00Z
**Duration**: 30 minutes

ToT evaluated top 3 approaches through 4 levels:

Level 0: JWT vs Session vs OAuth2
  Winner: JWT (Score: 85/100)

Level 1: JWT variants
  - Asymmetric (RS256) vs Symmetric (HS256) vs EdDSA
  Winner: RS256 (Score: 88/100)

Level 2: RS256 implementation
  - Self-signed vs CA-signed vs JWKS rotation
  Winner: JWKS rotation (Score: 91/100)

Level 3: JWKS rotation strategy
  - Manual vs Automated vs Vault-managed
  Winner: Vault-managed (Score: 93/100)

**Winning Path**: JWT > RS256 > JWKS rotation > Vault-managed
**Confidence**: 88%

**Handover to AR**: ./handovers/002-tot-to-ar.json
**Deliverable**: Optimal solution for validation

---

### Phase 3: AR Validation

**Started**: 2026-01-18T15:25:00Z
**Duration**: 20 minutes

AR attacked JWT/RS256/JWKS/Vault solution:

**Critical Attacks Found**: 2
- ATK-001: Algorithm confusion (RS256->HS256)
- ATK-002: JWKS endpoint poisoning

**Mitigations Designed**: 2
- Explicit algorithm validation server-side
- JWKS endpoint pinning with certificate validation

**Edge Cases Found**: 4
- Token expiry during long requests
- Clock skew between services
- Key rotation during request processing
- Vault unavailable scenario

**Residual Risk**: 15% (acceptable)

**Final Confidence**: 85% (reduced from 88% due to attack findings)

---

### Synthesis

**Session Complete**: 2026-01-18T15:45:00Z
**Total Duration**: 75 minutes
**Patterns Used**: BoT -> ToT -> AR

**Final Recommendation**:
Implement JWT with RS256 algorithm, JWKS rotation managed by HashiCorp Vault.
Include algorithm validation middleware and JWKS endpoint pinning.

**Confidence**: 85%
**Handovers Created**: 2
**Evidence Items**: 15
**Checkpoints**: 3
```

### 6.2 Parallel Orchestration: AT + BoT Merge

```markdown
## Session: Design data platform architecture
## Strategy: Parallel (AT || BoT -> Merge -> ToT)

### Phase 1: Parallel Exploration

**AT Branch** (Analogical Transfer):
- Problem: Novel data platform for real-time analytics
- Analogy found: Stock exchange trading systems
- Insight: Event-driven architecture with in-memory state
- Confidence: 0.72

**BoT Branch** (Breadth of Thought):
- Explored 8 architectures
- Top 3: Event sourcing (0.78), Lambda (0.71), Lakehouse (0.68)
- Insight: Event sourcing emerged as highest-confidence approach
- Confidence: 0.78

### Phase 2: Merge

**Agreement Type**: FULL_AGREEMENT
- Both patterns converged on event-driven/event-sourcing architecture
- AT found it via stock exchange analogy
- BoT found it via systematic exploration

**Merged Confidence**: 0.83 (max + 5%)

**Synthesis**: Event sourcing architecture validated by both analytical and analogical approaches. Stock exchange systems provide proven pattern for high-throughput event processing with strong consistency guarantees.

### Phase 3: ToT Optimization (on merged result)

[Continue with ToT to optimize event sourcing implementation details...]
```

---

## Part 7: Implementation Checklist

### For IR-v2 Orchestrator Developers

- [ ] Implement session directory creation with UUID generation
- [ ] Implement manifest file management (create, update, validate)
- [ ] Implement handover file writing with schema validation
- [ ] Implement checkpoint creation at 15-minute intervals
- [ ] Implement checkpoint recovery (session resume)
- [ ] Implement parallel branch merge with agreement analysis
- [ ] Implement evidence repository indexing
- [ ] Add hooks for pattern-specific state serialization

### For Pattern Implementers

- [ ] Implement `prepare_handover()` method returning pattern-specific data
- [ ] Implement `load_handover()` method accepting incoming handover data
- [ ] Implement `get_state()` method for checkpoint serialization
- [ ] Implement `restore_state()` method for checkpoint recovery
- [ ] Add evidence registration to evidence repository during gathering
- [ ] Update confidence scores according to transfer protocol

### For Session Recovery

- [ ] Validate checkpoint integrity hashes before restore
- [ ] Log recovery operations for audit trail
- [ ] Handle partial state gracefully (continue from last valid checkpoint)
- [ ] Notify user of any state loss during recovery

---

## Part 8: Configuration

### Global Configuration (`.reasoning/config.json`)

```json
{
  "version": "1.0",

  "session_defaults": {
    "checkpoint_interval_minutes": 15,
    "auto_checkpoint_on_handover": true,
    "max_session_duration_hours": 4,
    "archive_after_days": 30
  },

  "handover_settings": {
    "validate_schema": true,
    "require_confidence_transfer": true,
    "shared_assumption_discount": 0.05
  },

  "evidence_settings": {
    "max_evidence_file_size_mb": 10,
    "index_update_on_gather": true
  },

  "parallel_settings": {
    "max_parallel_branches": 5,
    "merge_timeout_minutes": 30
  },

  "logging": {
    "log_level": "INFO",
    "log_handovers": true,
    "log_checkpoints": true,
    "log_pattern_transitions": true
  }
}
```

---

## Summary

The Reasoning Handover Protocol provides:

1. **Standardized Directory Structure**: `.reasoning/session-{uuid}/` with clear organization for pattern state, handovers, evidence, and checkpoints

2. **Universal Handover Schema**: Base format plus pattern-specific extensions for ToT, BoT, HE, SRC, AR, DR, AT, RTR, and NDF

3. **Confidence Transfer**: Calibrated confidence scores with adjustments for scope changes and shared assumptions

4. **IR-v2 Integration**: State machine for orchestration, commands for handover initiation, and parallel merge protocol

5. **Checkpoint Protocol**: Mid-reasoning save points with integrity validation and recovery instructions

6. **Evidence Repository**: Shared evidence storage with cross-pattern indexing

Use this protocol whenever multi-pattern reasoning requires state preservation, pattern transitions, or audit trails.
