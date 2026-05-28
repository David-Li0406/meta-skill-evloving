---
name: draft-release-notes
description: Drafts release notes from git history for release changelogs. Use when you have to compose a changelog for a new version of this template package.
license: MIT
compatibility: opencode, claude code, copilot
metadata:
  author: Vasil Kotsev
  audience: contributors
  version: "1.0.0"
---

# Generate changelog

When you're asked to generate a changelog for a new release for the
`StackedDeck.Project.Templates` package, review the `git` log for this
repository to determine the delta between the previous release and the
latest commit.

Use the following algorithm:

1. Determine the previously released version.
   1.1 Check the `<PackageVersion>` in `../../../StackedDeck.Project.Templates.csproj`
   1.2 Determine the commit delta between the previous release version and the
   current one
   1.3 Feel free to use `git blame`, `git log` or `git tags` to determine the delta
2. Analyze the commit messages and collect information for the changes
3. If there are multiple `chore` related tasks like bumping dependencies, etc.,
   consolidate that into a single point in the change log
4. Write the change log in a nice human readable format, try to use lists,
   sections, etc. Attach a reference to a short version of the commit SHA
5. Make use of emojis semantically to prefix the changes; Use them to prefix the
   section headers as well as the individual change entries;
6. Keep the change entries as concise as possible, try to have one entry per
   major/minor change
7. After you've composed the list, update the `<PackageReleaseNotes>` section in
   `../../../StackedDeck.Project.Templates.csproj`. Make sure that the previous
   changelog is deleted/overwritten entirely. Don't skip this step.

## Format

```txt
✨ Features
- Introduce parameter for API styles (241342a)
- Add initial support for cloud providers (167c46c)

🚀 Improvements
- Introduce CI/CD pipeline parameter (989419a)
- Add HEALTHCHECK instruction to Dockerfile (5ea1e1b)
- Refactor template symbols (02c923f)

🐛 Fixes
- Fix incorrect log parameter (0066f45)

🔧 Chores
- Extract TFMs to Directory.Build.props (5894eae)
- Migrate solution to SLNX format (3a48190, 4de8796)
- Bump NUKE to v10.0.0 (efd74f0)
- Upgrade GitVersion.Tool to v6.5.0 (3b6b1d0)
- Bump ASP.NET runtime Alpine image to v10 (b87f3d1)
- Upgrade TFMs to .NET 10 and update NuGet packages (61a494a, c0520c9, 5a2c16f, and 12+ dependency bumps)
- Opt-out of .NET CLI telemetry in GitHub Actions (942a532)
- Update concurrency group expression (035fa5c)
- Remove incorrect registries section (999cc40)

📝 Documentation
- Extend AGENTS.md (342e943, d1db88e)
- Update README reference to base ASP.NET image (0b1479f)

🤖 Development Tools
- Introduce skill for drafting changelog notes (69df6c3)
- Extend staging guidelines for git-commit skill (5da2e7f)
- Trim down AGENTS.md to reduce token context (11dd88b)
- Introduce AI agent skills (9b9ddc8)
- Add human readable display names for test scenarios (d2de90c)
```
