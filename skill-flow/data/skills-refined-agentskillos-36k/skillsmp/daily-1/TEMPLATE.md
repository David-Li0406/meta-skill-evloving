---
title: "Daily Summary - {DATE}"
date: {DATE}
categories: [daily-summary]
tags: [commits, github, {relevant-tags}]
---

# Daily Summary - {DATE}

> Last updated: {TIMESTAMP}

## TL;DR

{1-2 sentences summarizing the day for non-technical readers. Focus on outcomes, not activities.}

## Highlights

{2-4 sentences on main themes and accomplishments. What actually moved forward today? What decisions were made?}

## Commits

| Repo | Commits | Focus |
|------|:-------:|-------|
| [{org/repo}](https://github.com/{org/repo}) | {n} | {What changed and why} |

{If repos were added to ~/dev, include a table:}

### Added Repos

| Repo | Type | Purpose |
|------|------|---------|
| [{org/repo}](https://github.com/{org/repo}) | {Created/Cloned/Forked} | {Why - what you're building, exploring, or referencing} |

## Open Threads

{Track actionable items - things awaiting response, next steps, blockers. Only include if there's something to track.}

| Status | Item | Context |
|--------|------|---------|
| Awaiting review | [{org/repo}#N](url) | {what the PR does} |
| Filed | [{org/repo}#N](url) | {what needs to happen next} |
| Merged | [{org/repo}#N](url) | {why it matters} |
| Blocked | {thing} | {what's blocking and next step} |

Status options: `Awaiting review`, `Filed`, `Merged`, `Closed`, `Blocked`, `In progress`

## Also Today

{Capture work that doesn't show in git: codebase exploration, research, architecture discussions, debugging sessions, learning. Omit if empty.}

- {What you explored/researched and what you learned or decided}

## Stats

| Commits | Repos | PRs | Issues | Reviews |
|:-------:|:-----:|:---:|:------:|:-------:|
| {n} | {n} | {n} | {n} | {n} |

## Companion Activity

{Optional section - include when RPG data adds context to the day's work. Pull from ~/.claude-rpg/data/companions.json}

| Companion | Level | XP Today | Tools | Focus |
|-----------|:-----:|:--------:|:-----:|-------|
| {repo-name} | {n} | +{n} | {top 2-3 tools} | {What drove the activity} |

**Session Highlights:**
- {n} prompts across {n} repos
- Top tools: {tool1} ({n}), {tool2} ({n})
- {Streak info if active}

---

Template notes (remove in actual posts):
- Jekyll front matter is REQUIRED: title, date, categories, tags
- Tags should include repo names and key topics (e.g., x402, claude-rpg, citycoins)
- TL;DR is for sharing with non-technical teammates - outcomes not activities
- Highlights answer "what moved forward" not "what did I touch"
- Commits table: repo links, focus on "what and why"
- Open Threads: VERIFY PR status with `gh pr view` before listing - don't trust raw data
- Also Today: research, exploration, conversations - the non-git work
- Stats at bottom - reference data, not the headline
- Companion Activity: optional, adds context when Claude sessions were active
- Omit any section that would be empty
