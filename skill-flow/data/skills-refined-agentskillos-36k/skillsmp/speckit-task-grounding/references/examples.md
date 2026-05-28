# Task Grounding Scoring Examples

Real-world examples of task grounding validation with different scoring levels.

## Example 1: Perfect Grounding (100%)
**Task**: Add `LifelineAutoRoleAssignment` to `TenantFeatureFlag` enum
**Status**: 🟢 **Documented** (Fully Grounded)
**Evidence**:
• data-model.md: Explicit enum addition with Display attribute
• plan.md: Feature flag controls tenant enablement
• quickstart.md: Implementation checklist item
• api-contracts.md: Display name mapping
**Assessment**: ✅ Ready to implement - explicit specification with exact location and format

## Example 2: Pattern-Based (70%)
**Task**: Add role name constants following FSHRoles.cs pattern
**Status**: 🟡 **Inferred** (Partially Grounded)
**Evidence**:
• Assumed FSHRoles.cs pattern exists (follows FSHPermissions.cs)
• data-model.md: Shows hardcoded strings in examples
• plan.md: No explicit FSHRoles.cs reference
**Gap**: FSHRoles.cs existence not verified
**Assessment**: ⚠️ BLOCKED - Pattern existence unverified, requires codebase inspection

## Example 3: Weak Inference (50%)
**Task**: Define `SessionGroupParticipantInvitationSentEvent`
**Status**: 🟡 **Inferred** (Partially Grounded)
**Evidence**:
• api-contracts.md: Schema reference only
• research.md: Only mentions AcceptedEvent
• plan.md: No SentEvent specification
**Gap**: No detailed spec for SentEvent requirements
**Assessment**: ⚠️ BLOCKED - Spec requirements unclear, verify FR-001 requires SentEvent

## Example 4: Ungrounded (20%)
**Task**: Add logging for performance monitoring
**Status**: 🔴 **Missing** (Ungrounded)
**Evidence**: None found in any artifact
**Gap**: Task appears to be developer assumption without specification
**Assessment**: 🔴 BLOCK - No evidence found, likely should be removed or specified