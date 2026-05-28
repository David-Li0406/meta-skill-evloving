# Agent Performance Report Card

**Agent:** {{ agent_name | default(project_name | default("Unknown Agent")) }}
**Review Date:** {{ timestamp | default(date_utc | default("1970-01-01 00:00:00 UTC")) }}
**Reviewer:** {{ agent_id | default(author | default("Scribe")) }}
**Project:** {{ project_name | default(PROJECT_NAME | default("Unknown Project")) }}
**Stage:** {{ stage | default("unspecified") }}
**Report Type:** Performance Evaluation

---

<!-- ID: executive_summary -->
## Executive Summary

**Overall Grade:** {{ overall_grade | default(metadata.overall_grade | default('[Score]%')) }}
**Performance Level:** {{ performance_level | default(metadata.performance_level | default('[EXCELLENT/GOOD/SATISFACTORY/NEEDS_IMPROVEMENT/POOR]')) }}
**Recommendation:** {{ recommendation | default(metadata.recommendation | default('[CONTINUE_TRAINING/RETRAIN/DISMISS]')) }}

---

<!-- ID: detailed_assessment -->
## Detailed Assessment

### 1. Scribe Protocol Compliance
**Grade:** {{ protocol_compliance_grade | default('[Score]%') }}
**Weight:** 30%

- [ ] {{ protocol_check_1 | default('append_entry usage frequency and quality') }}
- [ ] {{ protocol_check_2 | default('manage_docs tool usage and effectiveness') }}
- [ ] {{ protocol_check_3 | default('Documentation creation and maintenance') }}
- [ ] {{ protocol_check_4 | default('Enhanced search capability utilization') }}
- [ ] {{ protocol_check_5 | default('Cross-project learning application') }}

### 2. Technical Quality
**Grade:** {{ technical_quality_grade | default('[Score]%') }}
**Weight:** 25%

- [ ] {{ technical_check_1 | default('Code analysis accuracy and depth') }}
- [ ] {{ technical_check_2 | default('Technical decision quality and justification') }}
- [ ] {{ technical_check_3 | default('Implementation approach soundness') }}
- [ ] {{ technical_check_4 | default('Error handling and edge case consideration') }}
- [ ] {{ technical_check_5 | default('Best practices adherence') }}

### 3. Documentation Quality
**Grade:** {{ documentation_quality_grade | default('[Score]%') }}
**Weight:** 20%

- [ ] {{ documentation_check_1 | default('Document completeness and accuracy') }}
- [ ] {{ documentation_check_2 | default('Structure and organization quality') }}
- [ ] {{ documentation_check_3 | default('Technical clarity and precision') }}
- [ ] {{ documentation_check_4 | default('Evidence and reasoning quality') }}
- [ ] {{ documentation_check_5 | default('Consistency with established standards') }}

### 4. Communication and Collaboration
**Grade:** {{ communication_grade | default('[Score]%') }}
**Weight:** 15%

- [ ] {{ communication_check_1 | default('Clear and concise reporting') }}
- [ ] {{ communication_check_2 | default('Proper stakeholder communication') }}
- [ ] {{ communication_check_3 | default('Effective handoff to next phase') }}
- [ ] {{ communication_check_4 | default('Collaboration with other agents') }}
- [ ] {{ communication_check_5 | default('Responsiveness to feedback') }}

### 5. Problem Solving and Critical Thinking
**Grade:** {{ problem_solving_grade | default('[Score]%') }}
**Weight:** 10%

- [ ] {{ problem_solving_check_1 | default('Issue identification and analysis depth') }}
- [ ] {{ problem_solving_check_2 | default('Creative and effective solutions') }}
- [ ] {{ problem_solving_check_3 | default('Risk assessment and mitigation') }}
- [ ] {{ problem_solving_check_4 | default('Adaptability to changing requirements') }}
- [ ] {{ problem_solving_check_5 | default('Learning from previous experiences') }}

---

<!-- ID: strengths -->
## Strengths

- [ ] {{ strength_1 | default('Strength 1') }}
- [ ] {{ strength_2 | default('Strength 2') }}
- [ ] {{ strength_3 | default('Strength 3') }}

---

<!-- ID: areas_for_improvement -->
## Areas for Improvement

- [ ] {{ improvement_area_1 | default('Improvement Area 1') }}
- [ ] {{ improvement_area_2 | default('Improvement Area 2') }}
- [ ] {{ improvement_area_3 | default('Improvement Area 3') }}

---

<!-- ID: specific_feedback -->
## Specific Feedback

### Positive Feedback
- [ ] {{ positive_feedback_1 | default('Specific positive observation 1') }}
- [ ] {{ positive_feedback_2 | default('Specific positive observation 2') }}

### Constructive Feedback
- [ ] {{ constructive_feedback_1 | default('Specific improvement suggestion 1') }}
- [ ] {{ constructive_feedback_2 | default('Specific improvement suggestion 2') }}

### Action Items
- [ ] {{ action_item_1 | default('[Action item 1]') }}
- [ ] {{ action_item_2 | default('[Action item 2]') }}

---

<!-- ID: performance_metrics -->
## Performance Metrics

| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| append_entry calls | ≥10 | {{ append_entry_count | default('[count]') }} | {{ append_entry_status | default('[PASS/FAIL]') }}
| manage_docs usage | Required | {{ manage_docs_count | default('[count]') }} | {{ manage_docs_status | default('[PASS/FAIL]') }}
| Document quality | High | {{ document_quality_rating | default('[rating]') }} | {{ document_quality_status | default('[PASS/FAIL]') }}
| Technical accuracy | High | {{ technical_accuracy_rating | default('[rating]') }} | {{ technical_accuracy_status | default('[PASS/FAIL]') }}
| Protocol compliance | 100% | {{ protocol_compliance_percentage | default('[percentage]') }} | {{ protocol_compliance_status | default('[PASS/FAIL]') }}

---

<!-- ID: training_recommendations -->
## Training Recommendations

### Immediate Focus Areas
1. {{ training_focus_1 | default('[Training focus area 1]') }}
2. {{ training_focus_2 | default('[Training focus area 2]') }}
3. {{ training_focus_3 | default('[Training focus area 3]') }}

### Long-term Development
1. {{ development_goal_1 | default('[Development goal 1]') }}
2. {{ development_goal_2 | default('[Development goal 2]') }}

---

<!-- ID: next_evaluation -->
## Next Evaluation

**Scheduled Review Date:** {{ next_review_date | default('[Date]') }}
**Evaluation Criteria:** {{ evaluation_criteria | default('[Criteria]') }}
**Expected Improvements:** {{ expected_improvements | default('[Expected outcomes]') }}

---

<!-- ID: final_assessment -->
## Final Assessment

**Overall Recommendation:** {{ final_recommendation | default('[RECOMMENDATION]') }}

**Summary:** {{ performance_summary | default('[Brief summary of agent\'s performance and future outlook]') }}

**Confidence in Assessment:** {{ assessment_confidence | default('[High/Medium/Low]') }}

---

*This agent report card is part of the performance management system for {{ project_name }}.*
