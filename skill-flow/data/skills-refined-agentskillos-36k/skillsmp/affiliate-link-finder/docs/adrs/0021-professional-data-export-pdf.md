# ADR 0021: Professional Data Export (PDF)

**Date:** 2026-01-20  
**Status:** Accepted  
**Deciders:** Development Team

## Context

To make the application a viable "Gold Standard" tool for ADHD management, users needed a way to share their progress with healthcare providers. Simple CSV exports are often difficult for doctors to read quickly during a 15-minute consultation.

## Decision

Implement a professional-grade PDF generation service (`ReportPdfService`) for data sharing.

Key features:
1. **Aggregated Stats**: Automatic calculation of consistency, focus averages, and mood stability over custom date ranges.
2. **Tabular Logs**: A clear, daily breakdown of supplement adherence and focus scores.
3. **Medical Disclaimer**: Standardized disclaimer on every report footer to manage liability.
4. **Direct Sharing**: Integration with `printing` and `url_launcher` (mailto) to allow immediate delivery to a doctor's inbox.

## Rationale
- **Trust & Authority**: A well-formatted PDF carries more authority than raw data and positions the app as a serious management tool.
- **Consultation Efficiency**: Doctors can scan a PDF with charts and tables much faster than viewing individual app screens.
- **Portability**: PDFs can be easily attached to Electronic Health Records (EHRs).

## Consequences

**Positive:**
- High perceived value for premium users.
- Facilitates better doctor-patient communication.
- Offline availability of reports once generated.

**Negative:**
- Dependency on external packages (`pdf`, `printing`).
- Maintenance cost of keeping the report layout aligned with branding updates.
- Potential performance impact when generating reports for very large date ranges (mitigated by asynchronous generation).

## Alternatives Considered

| Option | Rejected Because |
|--------|------------------|
| CSV/JSON Export Only | Too raw for medical professional review; lacks branding and summary stats. |
| Web Dashboard (Doctor Portal) | High technical overhead; concerns about data privacy and HIPAA compliance for a 3rd party portal. |
| Screenshot Sharing | unprofessional; difficult to capture a full month of data in one view. |
