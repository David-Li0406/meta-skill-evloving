# Indicator to Metric Mapping

## CSV Indicators → dbt Metrics

| # | CSV Indicator | Metric ID(s) | Source Model |
|---|---------------|--------------|--------------|
| 1 | Active users | `active_providers` | active_providers |
| 2 | Percent of active users | `percent_active_providers` | active_providers |
| 3 | Total Users | `provider_count` | practitioners |
| 4 | Clients registered | `patient_count` | patient |
| 5 | Encounters | `client_encounters` | encounters |
| 6 | Number of IPC sessions | `sessions_ipc` | intervention_sessions |
| 7 | Number of client eligible for IPC | `clients_eligible_for_ipc` | clients_eligible_for_ipc |
| 8 | Number of client eligible for SBIRT-MI | `clients_sbirt_mi_eligible` | clients_sbirt_mi_eligible |
| 9 | Number of client potentially eligible for SPI | `clients_eligible_spi` | clients_eligible_spi |
| 10 | Number of client eligible for referral | `clients_eligible_referral` | clients_eligible_referral |
| 11 | Number of client eligible for FWS | `clients_eligible_fws` | clients_eligible_fws |
| 13 | Number of client who accepted IPC | `clients_accepted_ipc` | clients_accepted_ipc |
| 15 | Number of client who accepted SBIRT-MI | `clients_accepted_sbirt` | clients_accepted_sbirt |
| 17 | Number of client who accepted FWS | `clients_accepted_fws` | clients_accepted_fws |
| 19 | Number of client accepted referral | `clients_accepted_referral` | clients_accepted_referral |
| 20 | Refusal rate | `service_refusal_rate` | service_refusal |
| 21 | % access to care (Reach) | `mwtool_*_conversion_rate` | mwtool_to_intervention |
| 22 | Comorbidities | `mwtool_comorbidity_rate` | mwtool_comorbidities |
| 23 | Service delivery modality | `encounters_in_person`, `encounters_video_telehealth`, `encounters_phone_telehealth` | encounters_by_delivery_format |
| 24-26 | Assessment risk levels | `phq9_clients_severe/moderate_high/low`, `gad7_clients_*` | int_assessment_scores |
| 27 | Assessment scores subsequent sessions | `phq9_improvement_rate`, `phq9_remission_rate` | assessment_scores_all_sessions |
| 28 | % finish all sessions IPC | `ipc_completion_rate` | client_ipc_progress |
| 29 | % follow-up | `follow_up_completion_rate` | follow_up_1month |
| 32 | Screening location setting | `screenings_total`, `screening_locations_count` | screenings_by_location |

## Metric Categories

### Count Metrics
Simple counts using `expression: "count(distinct field)"`

### Percent Metrics
Ratios using `numerator` and `denominator` fields, calculated as `(numerator / denominator) * 100`

## Key Data Sources

| Source | Questionnaire ID | Used For |
|--------|-----------------|----------|
| Mental Wellness Tool (mwTool) | `Questionnaire/1613532` | IPC/SBIRT/SPI/Referral eligibility |
| Financial Wellness Tool | `Questionnaire/q-financial-wellness-tool` | FWS eligibility |
| Planning Next Steps | `Questionnaire/q-planning-next-steps` | Service acceptance/refusal |
| IPC Sessions 1-4 | `Questionnaire/55`, `58`, `208`, `63` | IPC completion tracking |
| PHQ-9 Sessions 1-4 | `Questionnaire/54`, `57`, `61`, `211` | Depression scores |
| GAD-7 Sessions 1-4 | `Questionnaire/202`, `205`, `59`, `62` | Anxiety scores |
| Tasks (code 040) | Task resource | 1-month follow-up |
