# PDS GitHub Label → Release Notes Mapping

_Derived from PDS label scheme (columns B: Label, C: Description)._


**Sections used**: Breaking changes, Security, New, Improvements, Fixes. Labels not mapped are omitted by default, or used for grouping/triage.


| Label | Description | Maps to Release Notes Section | Include by default? | Notes |
|---|---|---|---|---|
| backwards-incompatible | backwards incompatible change. will require major tag | Breaking changes | Yes |  |
| security | bug identified as a potential security issue or coding no-no | Security | Yes |  |
| requirement | user story or formal requirement for new feature | New | Yes | Represents a user story/requirement; categorize as **New** when delivered. |
| enhancement | improvements | Improvements | Yes | If this introduces a brand‑new capability, consider listing under **New**. |
| bug | its a bug. gross | Fixes | Yes |  |
| maintenance | maintenance theme | Improvements | No | Internal/maintenance; usually omit unless user‑visible. |
| (e.g c.doi-search) |  | — | No |  |
| B11.0 |  | — | No | Build/version placeholder; not a release‑notes category. |
| B11.1 |  | — | No | Build/version placeholder; not a release‑notes category. |
| B12.0 |  | — | No | Build/version placeholder; not a release‑notes category. |
| c.<component_name> |  | — | No | Component/area tag; use to group bullets within sections. |
| duplicate | duplicate to another issue | — | No | Housekeeping; exclude from release notes. |
| etc. |  | — | No | Build/version placeholder; not a release‑notes category. |
| etc. | Open bugs associated with vX of the software  | — | No | Build/version placeholder; not a release‑notes category. |
| i&t-backlog | all features and bugs ready for I&T | — | No |  |
| i&t.automated | I&T-related ticket | — | No | Internal Integration & Test label; omit from user notes. |
| i&t.done | Initial testing complete from I&T team. | — | No | Internal Integration & Test label; omit from user notes. |
| i&t.issue | I&T-related ticket | — | No | Internal Integration & Test label; omit from user notes. |
| i&t.skip | Skip I&T either due to a related ticket being tested or trivial closeout. | — | No | Internal Integration & Test label; omit from user notes. |
| icebox | backlog. will be planned for future release | — | No | Housekeeping; exclude from release notes. |
| invalid | feature or bug is invalid | — | No | Housekeeping; exclude from release notes. |
| needs:dependency | some other dependency needed before we can close this out. | — | No | Planning/triage metadata; exclude from release notes. |
| needs:more-info | team can tag tickets that need more info / details from product-owner in order to proceed. | — | No | Planning/triage metadata; exclude from release notes. |
| needs:receivable | external receivables and/or tasks reliant on someone outside of EN in order to complete. this triggers product owner to follow up with external customers/stakeholders. | — | No | Planning/triage metadata; exclude from release notes. |
| needs:requirement | team can tag tickets if it is unclear if a story is associated with this ticket | — | No | Planning/triage metadata; exclude from release notes. |
| needs:scheduling | ticket is created and triaged but needs a Release Theme to be scheduled | — | No | Planning/triage metadata; exclude from release notes. |
| needs:triage | new tickets will be auto-tagged with this, or team can tag for triage by product-owner | — | No | Planning/triage metadata; exclude from release notes. |
| open.v3.0.0 | Open bugs associated with v3.0.0 of the software  | — | No | Tracking label; not a release‑notes category. |
| open.v3.1.0 | Open bugs associated with v3.1.0 of the software  | — | No | Tracking label; not a release‑notes category. |
| p.could-have | medium priority, may impact current release backlog | — | No | Planning/triage metadata; exclude from release notes. |
| p.must-have | nice-to-have that isn't nice enough to be low priority | — | No | Planning/triage metadata; exclude from release notes. |
| p.should-have | low priority, most likey to be added to product backlog | — | No | Planning/triage metadata; exclude from release notes. |
| p.wont-have | high priority, high likelihood of impacting current release backlog | — | No | Planning/triage metadata; exclude from release notes. |
| pending-scr | pending PDS4 SCR | — | No |  |
| product-backlog | all features and bugs associated with a product | — | No |  |
| proj.cloud-project | PDS Cloud Initiative project | — | No | Project grouping; can be used to sub‑group bullets by project if desired. |
| proj.deep-archive | PDS Deep Archive | — | No | Project grouping; can be used to sub‑group bullets by project if desired. |
| proj.devops | DevOps Project | — | No | Project grouping; can be used to sub‑group bullets by project if desired. |
| proj.dldd-mgmt | dLDD Managment Project | — | No | Project grouping; can be used to sub‑group bullets by project if desired. |
| proj.doi-service | DOI Service Project | — | No | Project grouping; can be used to sub‑group bullets by project if desired. |
| proj.nucleus | PDS Nucleus | — | No | Project grouping; can be used to sub‑group bullets by project if desired. |
| proj.pds-ux | PDS User Experience Project | — | No | Project grouping; can be used to sub‑group bullets by project if desired. |
| proj.pds4-scrs | PDS4 Software Change Requests (SCRs) | — | No | Project grouping; can be used to sub‑group bullets by project if desired. |
| proj.plaid | PLAID-related tasks | — | No | Project grouping; can be used to sub‑group bullets by project if desired. |
| proj.registry+api | Registry and API tasks | — | No | Project grouping; can be used to sub‑group bullets by project if desired. |
| proj.validate | PDS Validate Tool tasks | — | No | Project grouping; can be used to sub‑group bullets by project if desired. |
| proj.web-modern | PDS Web Modernization Project | — | No | Project grouping; can be used to sub‑group bullets by project if desired. |
| release-backlog | all features and bugs planned for the current release | — | No |  |
| s.critical | critical priority, will impact current sprint backlog | — | No | Planning/triage metadata; exclude from release notes. |
| s.high | high priority, will impact current sprint backlog | — | No | Planning/triage metadata; exclude from release notes. |
| s.low | low severity | — | No | Planning/triage metadata; exclude from release notes. |
| s.medium | medium priority, may impact current release backlog | — | No | Planning/triage metadata; exclude from release notes. |
| sprint-backlog | all features and bugs planned for the current sprint | — | No |  |
| task | task or work item, most often a sub-tasks of a bug, enhancement, or requirement Epic | — | No |  |
| theme | release plan theme to group together user stories, where applicable | — | No |  |
| wontfix | feature or bug wont be fixed either because of priority or some other rationale. | — | No | Housekeeping; exclude from release notes. |