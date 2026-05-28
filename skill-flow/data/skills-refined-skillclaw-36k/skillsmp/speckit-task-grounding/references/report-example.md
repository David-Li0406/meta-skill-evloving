# Task Grounding Analysis: Phase 1 & Phase 2
**Feature**: 007-lifeline-invitation-auto-role-mvp
**Date**: January 12, 2026
**Focus**: Grounding validation against planning artifacts

---

## Executive Summary

| Phase                 | Grounding Status     | Tasks     | Coverage                 | Next Action                 |
| --------------------- | -------------------- | --------- | ------------------------ | --------------------------- |
| Phase 1: Setup        | 🟢 Mostly Documented  | T001-T003 | 2/3 Fully, 1/3 Partially | Validate T003 pattern       |
| Phase 2: Foundational | 🟡 Partially Inferred | T004-T005 | 0/2 Fully, 2/2 Partially | Verify spec.md requirements |

**Overall Assessment**: 🟡 **NEEDS CLARIFICATION**  
**Rationale**:
- Phase 1 has one blocked task requiring pattern verification
- Phase 2 has two blocked tasks requiring specification clarification

---

## Task Grounding Matrix

| Task                                                                                                    | Grounding Status                        | Primary Evidence                                                                                                                                                                                                           | Gaps                                            | Next Step                                             |
| ------------------------------------------------------------------------------------------------------- | --------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------- | ----------------------------------------------------- |
| **T001**<br/>Add `LifelineAutoRoleAssignment` to `TenantFeatureFlag` enum                               | 🟢 **Documented**<br/>(Fully Grounded)   | • data-model.md: Explicit enum addition with Display attribute<br>• plan.md: Feature flag controls tenant enablement<br>• quickstart.md: Implementation checklist item<br>• api-contracts.md: Display name mapping         | None                                            | Ready to implement                                    |
| **T002**<br/>Define `LifelineCoHost` and `LifelineParticipant` permission sets                          | 🟢 **Documented**<br/>(Fully Grounded)   | • data-model.md: Complete permission definitions (14 CoHost, 4 Participant)<br>• plan.md: Role seeder with permission counts<br>• api-contracts.md: Exact permission mappings<br>• quickstart.md: Implementation checklist | None                                            | Ready to implement                                    |
| **T003**<br/>Add role name constants `LifelineCoHost` and `LifelineParticipant` in FSHRoles.cs          | 🟡 **Inferred**<br/>(Partially Grounded) | • Assumed FSHRoles.cs pattern exists (follows FSHPermissions.cs)<br>• data-model.md: Shows hardcoded strings in examples<br>• plan.md: No explicit FSHRoles.cs reference                                                   | FSHRoles.cs existence not verified              | **BLOCKED**: Verify FSHRoles.cs exists in codebase    |
| **T004**<br/>Define `SessionGroupParticipantInvitationSentEvent`                                        | 🟡 **Inferred**<br/>(Partially Grounded) | • api-contracts.md: Schema reference only<br>• research.md: Only mentions AcceptedEvent<br>• plan.md: No SentEvent specification                                                                                           | No detailed spec for SentEvent requirements     | **BLOCKED**: Verify spec.md FR-001 requires SentEvent |
| **T005**<br/>Ensure `SessionGroup.InviteParticipant` emits `SessionGroupParticipantInvitationSentEvent` | 🟡 **Inferred**<br/>(Partially Grounded) | • plan.md: Domain event pattern documented<br>• research.md: Outbox pattern for events<br>• Depends on T004 completion                                                                                                     | No explicit InviteParticipant event requirement | **BLOCKED**: Depends on T004 + codebase inspection    |

## Observations

### Gaps
- **Gap 1: FSHRoles.cs Pattern (T003)**  
  *Impact*: T003 assumes FSHRoles.cs exists but pattern not documented  
  *Evidence*: data-model.md and api-contracts.md use hardcoded role strings  
  *Resolution*: Inspect `src/Core/Shared/Authorization/` for FSHRoles.cs

- **Gap 2: SentEvent Requirements (T004-T005)**  
  *Impact*: Domain events may be unnecessary if AcceptedEvent suffices  
  *Evidence*: Only AcceptedEvent explicitly mentioned in research.md  
  *Resolution*: Read spec.md FR-001 to confirm SentEvent need

- **Gap 3: Hardcoded Role Strings**  
  *Impact*: Architectural inconsistency if FSHRoles constants exist  
  *Evidence*: Planning artifacts show hardcoded "Lifeline CoHost" strings  
  *Resolution*: Update examples to use constants if T003 proceeds

### Action Plan
**Immediate (Before Any Implementation)**
- Verify FSHRoles.cs existence - Inspect authorization directory
- Read spec.md FR-001 - Confirm SentEvent requirements
- Check SessionGroup domain - See existing event emissions

**Phase 1 Execution (After Verification)**
- T001 & T002: Implement immediately (fully grounded)
- T003: Implement only if FSHRoles.cs exists, otherwise create it

**Phase 2 Execution (After Spec Verification)**
- T004: Implement only if spec.md requires SentEvent
- T005: Implement only if T004 needed and InviteParticipant doesn't already emit

### Risks
| Task | Level    | Mitigation                       |
| ---- | -------- | -------------------------------- |
| T001 | 🟢 Low    | Straightforward enum addition    |
| T002 | 🟢 Low    | Well-documented permission lists |
| T003 | 🟡 Medium | Pattern existence unverified     |
| T004 | 🟡 Medium | Spec requirements unclear        |
| T005 | 🟡 Medium | Depends on T004 + codebase state |

---