# Physical Construction Domain Invariants

Extends: [[system-invariants]]
Domain: Buildings, infrastructure, physical fabrication

---

## When to Use

Load this domain for:
- House construction (Kanyakumari)
- Renovation projects
- Infrastructure builds
- Physical product manufacturing

**Note**: For remote oversight, also load [[remote-management]]

---

## Domain Invariants (16-21)

### 16. Material Properties Must Be Climate-Validated

**Principle**: Every material must be proven for local environment

**Violation**: Specifying materials without climate validation

**Examples**:
- ❌ "Use exterior paint"
- ❌ "Install wooden doors"
- ❌ "Apply waterproofing"
- ✅ "Exterior paint: heat_resistant(≤50°C) + humidity_resistant(≤95%) + salt_resistant(coastal) → Brand: Asian_Paints_WeatherProof"
- ✅ "Wooden doors: teak + termite_treatment + monsoon_seal + UV_coating → Supplier: verified_coastal_experience"
- ✅ "Waterproofing: Fosroc_system + coastal_grade + 10yr_warranty + installer_certified"

**Enforcement**: Materials must specify: climate_properties + test_validation + local_sourcing → Otherwise REJECT

---

### 17. Vendor Capabilities Must Be Validated

**Principle**: No spec that assumes unverified contractor expertise

**Violation**: Specifying techniques without capability verification

**Examples**:
- ❌ "Install waterproofing system"
- ❌ "Lay Italian marble"
- ❌ "Build exposed concrete walls"
- ✅ "Waterproofing: Fosroc_DR_Newcoat → require contractor_certification + past_coastal_projects(3+) + warranty_10yr"
- ✅ "Italian marble: contractor_marble_experience(5yr+) + reference_projects(2) + insurance_coverage"
- ✅ "Exposed concrete: contractor_portfolio_review + test_panel_first + finish_approval_gate"

**Enforcement**: Specialty work must specify: required_certification + past_projects + insurance → Otherwise REJECT

---

### 18. Temporal Constraints Must Account for Climate

**Principle**: Scheduling must consider weather/seasons

**Violation**: Calendar dates without climate consideration

**Examples**:
- ❌ "Start construction in June"
- ❌ "Complete in 6 months"
- ❌ "Foundation by December"
- ✅ "Start: post-monsoon(Oct-Nov) + pre-summer(before_March) → window: Oct15-Feb28"
- ✅ "Duration: 6mo_base + 2mo_monsoon_buffer + 1mo_material_delay_buffer = 9mo_total"
- ✅ "Foundation: complete_before_monsoon(May) + 28-day_cure_buffer + inspection_gate"

**Enforcement**: Schedules must include: season_constraints + weather_buffers + monsoon_plan → Otherwise REJECT

---

### 19. Inspection Gates Must Be Explicit

**Principle**: Every phase must have validation checkpoint

**Violation**: No inspection, unclear inspector, no failure plan

**Examples**:
- ❌ "Complete foundation"
- ❌ "Inspector will check"
- ❌ "Quality to be verified"
- ✅ "Foundation complete → structural_engineer_signoff + compression_test(≥25N/mm²) + photo_documentation → PASS: proceed_to_columns | FAIL: remediation_plan_required"
- ✅ "Waterproofing → independent_inspector + water_test(24hr) + warranty_activation → FAIL: redo_at_contractor_cost"
- ✅ "Electrical → licensed_inspector + continuity_test + grounding_test → FAIL: rework_before_concealment"

**Enforcement**: Phase completion must specify: who_inspects + test_criteria + pass/fail_actions → Otherwise REJECT

---

### 20. Material Failure Modes Must Be Documented

**Principle**: Every material must state how it can fail and recovery cost

**Violation**: No failure analysis for critical materials

**Examples**:
- ❌ "Use M25 concrete for foundation"
- ❌ "Install marble flooring"
- ❌ "Apply waterproof coating"
- ✅ "M25 concrete: failure_mode(insufficient_strength) → detection(compression_test) → recovery(demolish+repour, ₹8L, +8wk)"
- ✅ "Marble flooring: failure_mode(cracking) → detection(visual) → recovery(replace_section, ₹2L, +2wk)"
- ✅ "Waterproofing: failure_mode(leakage) → detection(monsoon_test) → recovery(reapply, ₹50K, +1wk)"

**Enforcement**: Critical materials must specify: failure_mode + detection_method + recovery_cost → Otherwise REJECT

---

### 21. Supply Chain Must Be Stress-Tested

**Principle**: Material specs must include sourcing constraints

**Violation**: Specifying materials without availability validation

**Examples**:
- ❌ "Use Italian marble"
- ❌ "Install imported fixtures"
- ❌ "Source specialty lumber"
- ✅ "Italian marble: lead_time(8wk) + monsoon_shipping_risk + storage_needs(dry_warehouse) → fallback: Rajasthani_marble(2wk)"
- ✅ "Fixtures: local_availability_verified + 2_supplier_quotes + 4wk_delivery → fallback: alternative_equivalent"
- ✅ "Teak doors: supplier_confirmed + advance_booking(12wk) + storage_at_site → fallback: local_hardwood"

**Enforcement**: Imported/specialty materials must specify: lead_time + risks + fallbacks + storage → Otherwise REJECT

---

## Construction-Specific Sub-Invariants

### 21a. Concrete Specifications

- Grade must be specified (M20, M25, M30)
- Cure time must be enforced (typically 28 days)
- Slump test required before pour
- Compression test required after cure

### 21b. Steel Specifications

- Grade must be specified (Fe415, Fe500, Fe550)
- Mill certificate required
- No site welding without engineer approval
- Lap length per structural drawings

### 21c. Waterproofing Specifications

- System must be specified (not just "waterproof")
- Warranty period required (minimum 5 years)
- Water test before concealment
- Drainage path must be defined

---

## Quick Reference

| # | Invariant | Key Test |
|---|-----------|----------|
| 16 | Material Properties Must Be Climate-Validated | Materials have climate specs |
| 17 | Vendor Capabilities Must Be Validated | Contractors have verified credentials |
| 18 | Temporal Constraints Must Account for Climate | Schedule includes monsoon buffer |
| 19 | Inspection Gates Must Be Explicit | Every phase has pass/fail criteria |
| 20 | Material Failure Modes Must Be Documented | Failure + detection + recovery cost |
| 21 | Supply Chain Must Be Stress-Tested | Lead times + fallbacks documented |

---

*Domain: Physical Construction*
*Invariants: 16-21 (plus sub-invariants)*
*Use with: Core invariants 1-10*
*Often combined with: remote-management.md*
