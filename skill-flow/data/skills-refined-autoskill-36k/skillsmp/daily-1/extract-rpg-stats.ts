#!/usr/bin/env bun
/**
 * Extract RPG stats for daily summaries from claude-rpg data
 * Usage: bun extract-rpg-stats.ts [date]
 *        bun extract-rpg-stats.ts 2026-01-21
 *        bun extract-rpg-stats.ts --companions  (just companion overview)
 *
 * Output: Markdown sections for daily summary
 */

import { existsSync, readFileSync } from "fs";
import { join } from "path";

// XP values from claude-rpg shared/xp.ts
const XP_TABLE: Record<string, number> = {
  Read: 1,
  Edit: 3,
  Write: 5,
  Bash: 2,
  Grep: 1,
  Glob: 1,
  Task: 5,
  TodoWrite: 1,
  WebFetch: 2,
  WebSearch: 2,
  AskUserQuestion: 1,
  Skill: 1,
  EnterPlanMode: 1,
  ExitPlanMode: 1,
};

interface CompanionStats {
  toolsUsed: Record<string, number>;
  promptsReceived: number;
  sessionsCompleted: number;
  git: {
    commits: number;
    pushes: number;
    prsCreated: number;
    prsMerged: number;
  };
  commands: {
    testsRun: number;
    buildsRun: number;
    deploysRun: number;
    lintsRun: number;
  };
  blockchain: {
    clarinetChecks: number;
    clarinetTests: number;
    testnetDeploys: number;
    mainnetDeploys: number;
  };
}

interface Companion {
  id: string;
  name: string;
  repo: { path: string; org?: string; name: string };
  level: number;
  experience: number;
  totalExperience: number;
  stats: CompanionStats;
  streak: { current: number; longest: number; lastActiveDate: string };
  lastActivity: number;
}

interface HookEvent {
  session_id: string;
  cwd: string;
  hook_event_name: string;
  tool_name?: string;
  timestamp: number;
}

interface DailyStats {
  companion: string;
  events: number;
  xpEarned: number;
  toolsUsed: Record<string, number>;
  prompts: number;
}

const DATA_DIR = join(process.env.HOME || "", ".claude-rpg", "data");
const COMPANIONS_FILE = join(DATA_DIR, "companions.json");
const EVENTS_FILE = join(DATA_DIR, "events.jsonl");

function readCompanions(): Companion[] {
  if (!existsSync(COMPANIONS_FILE)) {
    console.error("No companions.json found at", COMPANIONS_FILE);
    return [];
  }
  const data = JSON.parse(readFileSync(COMPANIONS_FILE, "utf-8"));
  return data.companions || [];
}

function readEventsForDate(dateStr: string): HookEvent[] {
  if (!existsSync(EVENTS_FILE)) return [];

  const events: HookEvent[] = [];
  const lines = readFileSync(EVENTS_FILE, "utf-8").split("\n");

  for (const line of lines) {
    if (!line.trim()) continue;
    try {
      const event: HookEvent = JSON.parse(line);
      const eventDate = new Date(event.timestamp).toISOString().split("T")[0];
      if (eventDate === dateStr) {
        events.push(event);
      }
    } catch {
      // Skip malformed lines
    }
  }
  return events;
}

function calculateDailyStats(events: HookEvent[]): Map<string, DailyStats> {
  const statsByRepo = new Map<string, DailyStats>();

  for (const event of events) {
    // Extract repo name from cwd (e.g., /home/user/dev/org/repo -> org/repo)
    const cwdParts = event.cwd.split("/");
    const devIdx = cwdParts.indexOf("dev");
    const repo = devIdx >= 0 ? cwdParts.slice(devIdx + 1, devIdx + 3).join("/") : cwdParts.slice(-2).join("/");

    if (!statsByRepo.has(repo)) {
      statsByRepo.set(repo, {
        companion: repo,
        events: 0,
        xpEarned: 0,
        toolsUsed: {},
        prompts: 0,
      });
    }

    const stats = statsByRepo.get(repo)!;
    stats.events++;

    // Count tool usage and XP for PostToolUse events (successful tool calls)
    if (event.hook_event_name === "PostToolUse" && event.tool_name) {
      const tool = event.tool_name;
      stats.toolsUsed[tool] = (stats.toolsUsed[tool] || 0) + 1;
      stats.xpEarned += (XP_TABLE[tool] || 1) + 1; // tool XP + success bonus
    }

    // Count prompts
    if (event.hook_event_name === "UserPromptSubmit") {
      stats.prompts++;
    }
  }

  return statsByRepo;
}

function formatCompanionOverview(companions: Companion[]): string {
  const active = companions
    .filter((c) => c.totalExperience > 0)
    .sort((a, b) => b.totalExperience - a.totalExperience);

  if (active.length === 0) return "";

  const lines: string[] = [
    "## Companions",
    "",
    "| Companion | Level | Total XP | Commits | Streak |",
    "|-----------|:-----:|:--------:|:-------:|:------:|",
  ];

  for (const c of active) {
    const streak = c.streak.current > 0 ? `${c.streak.current}d` : "-";
    lines.push(
      `| ${c.name} | ${c.level} | ${c.totalExperience.toLocaleString()} | ${c.stats.git.commits} | ${streak} |`
    );
  }

  return lines.join("\n");
}

function formatDailyActivity(dateStr: string, dailyStats: Map<string, DailyStats>): string {
  if (dailyStats.size === 0) return `\nNo RPG activity recorded for ${dateStr}\n`;

  const sorted = Array.from(dailyStats.values()).sort((a, b) => b.xpEarned - a.xpEarned);

  let totalXP = 0;
  let totalPrompts = 0;
  const allTools: Record<string, number> = {};

  for (const s of sorted) {
    totalXP += s.xpEarned;
    totalPrompts += s.prompts;
    for (const [tool, count] of Object.entries(s.toolsUsed)) {
      allTools[tool] = (allTools[tool] || 0) + count;
    }
  }

  const topTools = Object.entries(allTools)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 5);

  const lines: string[] = [
    "## Companion Activity",
    "",
    "| Companion | XP Earned | Tools | Top Activity |",
    "|-----------|:---------:|:-----:|--------------|",
  ];

  for (const s of sorted) {
    const tools = Object.entries(s.toolsUsed)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 3)
      .map(([t, n]) => `${t}(${n})`)
      .join(", ");
    const topTool = Object.entries(s.toolsUsed).sort((a, b) => b[1] - a[1])[0];
    const activity = topTool ? `${topTool[0]} focused` : "-";
    lines.push(`| ${s.companion} | +${s.xpEarned} | ${tools} | ${activity} |`);
  }

  lines.push("");
  lines.push("**Session Highlights:**");
  lines.push(`- ${totalPrompts} prompts across ${sorted.length} repos`);
  lines.push(`- +${totalXP} XP earned`);
  if (topTools.length > 0) {
    lines.push(`- Top tools: ${topTools.map(([t, n]) => `${t} (${n})`).join(", ")}`);
  }

  return lines.join("\n");
}

// Main
const args = process.argv.slice(2);

if (args[0] === "--help") {
  console.log(`Usage:
  bun extract-rpg-stats.ts [date]       Daily activity for date (default: today)
  bun extract-rpg-stats.ts --companions Companion overview only

Output: Markdown sections for daily summary`);
  process.exit(0);
}

const companions = readCompanions();

if (args[0] === "--companions") {
  console.log(formatCompanionOverview(companions));
  process.exit(0);
}

const dateStr = args[0] || new Date().toISOString().split("T")[0];
const events = readEventsForDate(dateStr);
const dailyStats = calculateDailyStats(events);

console.log(formatDailyActivity(dateStr, dailyStats));
