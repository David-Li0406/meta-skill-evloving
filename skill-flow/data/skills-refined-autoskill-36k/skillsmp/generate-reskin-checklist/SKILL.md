---
name: generate-reskin-checklist
description: Generate a checklist for the legacy reskin given a specific criteria
---

First, understand the definition of "legacy reskin" as described in docs\refactor-plan\reskin-definition.md.
Explore the FundViewGit codebase and generate a comprehensive checklist for reskinning legacy services and repositories based on the user defined scope or module.
For a more concrete reference of reskinning legacy services, see docs\refactor-plan\gl-ap-playbooks.md.
Separate legacy items into two sections:
- Services: legacy static service classes in FundView.MVC4.UI, typically under Areas/*/Services or any MVC4.UI class ending in Service.cs (exclude tests). These go in the Services table.
- Repositories: legacy repository classes still located in FundView.MVC4.UI, typically under **/Repository/** or **/Repositories/**, or MVC4.UI classes ending in Repo.cs or Repository.cs. These go in the Repositories table.
Each checklist item represents a specific service or repository that requires reskinning.
Mark an item as reskinned only if the legacy code delegates to a non-static helper service (services) or the repository has been moved out of MVC4.UI into a dual-targeting project (repositories).
Write the output to docs\progress\checklist.md using the existing table format and section order:
- Services table columns: Service Name | Legacy Service Path | Tests Implemented | Reskinned (Yes/No)
- Repositories table columns: Repository Name | Legacy Repository Path | Tests Implemented | Reskinned (Yes/No)
- Use a checkbox in the Tests Implemented and Reskinned columns: [ ] for not done, [x] for done.