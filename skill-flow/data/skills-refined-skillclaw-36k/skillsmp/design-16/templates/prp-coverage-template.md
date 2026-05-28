# PRP Coverage Matrix (TDD Mode)

## Metadata

| Field | Value |
|-------|-------|
| PRP | {prp_id} |
| Spec | {spec_id} |
| Journey | {journey_id} |
| Mode | TDD (INV-L007) |
| Generated | {timestamp} |

---

## Success Criteria → Test Mapping

**Every SC-* must have a corresponding test.** No exceptions.

| SC | Description | Test File | Test Function | Lines | Status |
|----|-------------|-----------|---------------|-------|--------|
| SC-1 | {description} | test_01_*.py | test_endpoint_exists | 45-52 | ✓ |
| SC-2 | {description} | test_02_*.py | test_save_data | 60-75 | ✓ |
| SC-3 | {description} | test_03_*.py | test_compare | 80-95 | ✓ |
| ... | ... | ... | ... | ... | ... |

**Coverage:** {covered}/{total} ({percentage}%)

---

## Deliverable → Test Mapping

| Phase | Deliverable ID | Description | Test File | Gate |
|-------|----------------|-------------|-----------|------|
| 0 | F0.1 | {description} | test_01_*.py | gate_1.py |
| 0 | F0.2 | {description} | test_02_*.py | gate_1.py |
| 1 | F1.1 | {description} | test_03_*.py | gate_2.py |
| ... | ... | ... | ... | ... |

---

## Implementation Target Files

**These files must be created by the AI to pass tests:**

| Test | Target File | Purpose |
|------|-------------|---------|
| test_01_*.py | sa-intel-app/backend/routers/{feature}.py | API router |
| test_02_*.py | sa-intel-app/backend/services/{feature}.py | Business logic |
| test_03_*.py | sa-intel-app/frontend/src/components/{Feature}.tsx | UI component |

---

## Integration Test Verification

**INV-L009:** Integration test must cover full workflow.

| Workflow Step | SC Covered | Test Function |
|---------------|------------|---------------|
| 1. {Initial state} | SC-1 | test_full_workflow:line_40 |
| 2. {Main action} | SC-2, SC-3 | test_full_workflow:line_55 |
| 3. {Verify effects} | SC-4 | test_full_workflow:line_70 |
| 4. {Query results} | SC-5 | test_full_workflow:line_85 |

---

## Appendix → Test Mapping

| Appendix | Content | Verified In |
|----------|---------|-------------|
| B | Database schema | test_schema_matches_prp() |
| C | API endpoints | test_endpoint_defined() |
| D | Column mappings | test_field_transformations() |
| E | UI wireframes | test_component_structure() |
| F | Error messages | test_error_messages() |

---

## Validation Gates

| Gate | Phase | Tests | Status |
|------|-------|-------|--------|
| gate_1.py | Phase 0 | test_01, test_02 | ⏳ Pending |
| gate_2.py | Phase 1 | test_03, test_04, test_05 | ⏳ Pending |
| gate_3.py | Phase 2 | test_06, test_07 | ⏳ Pending |

---

## Notes

- **No step files in TDD mode** - Tests are the contract
- **AI writes code to pass tests** - Implementation emerges
- **Integration test required** - Full workflow verification
- **100% SC coverage required** - No untested criteria
