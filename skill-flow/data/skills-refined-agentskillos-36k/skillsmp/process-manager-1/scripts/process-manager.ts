#!/usr/bin/env -S deno run --allow-run --allow-read --allow-net

/**
 * process-manager.ts - Manage dev servers and long-running processes
 *
 * A utility for starting, stopping, and monitoring Node.js dev servers.
 * Uses port-based detection (lsof) as ground truth - never trusts PID files.
 *
 * Usage:
 *   deno run --allow-run --allow-read --allow-net scripts/process-manager.ts <command> [options]
 *
 * Commands:
 *   list                    List all configured processes
 *   status [name|--all]     Check process status
 *   ports                   Show port usage summary
 *   start <name|group>      Start a process or group
 *   stop <name|group>       Stop a process or group
 *   restart <name|group>    Restart a process or group
 *
 * Options:
 *   --json                  Output as JSON
 *   --all                   Apply to all processes (for status)
 *   -h, --help              Show help
 */

// ============================================================================
// Types
// ============================================================================

interface HealthCheck {
  url: string;
  timeout?: number;
}

interface ProcessConfig {
  name?: string;
  port: number;
  command: string;
  cwd?: string;
  healthCheck?: HealthCheck;
  startupTime?: number;
  group?: string;
}

interface Config {
  processes: Record<string, ProcessConfig>;
  groups?: Record<string, string[]>;
  defaults?: {
    startupTime?: number;
    healthCheckTimeout?: number;
  };
}

interface ProcessStatus {
  id: string;
  name: string;
  port: number;
  status: "RUNNING" | "STOPPED" | "CONFLICT";
  pid?: number;
  healthy?: boolean;
  command?: string;
}

// ============================================================================
// Constants
// ============================================================================

const VERSION = "1.0.0";
const DEFAULT_STARTUP_TIME = 3000;
const DEFAULT_HEALTH_TIMEOUT = 5000;
const STOP_TIMEOUT = 5000;
const COMMON_PORTS = [3000, 4000, 4001, 5173, 5174, 8000, 8080];

// ============================================================================
// Config Loading
// ============================================================================

async function findProjectRoot(): Promise<string> {
  let dir = Deno.cwd();
  while (dir !== "/") {
    try {
      await Deno.stat(`${dir}/package.json`);
      return dir;
    } catch {
      dir = dir.split("/").slice(0, -1).join("/") || "/";
    }
  }
  return Deno.cwd();
}

async function loadConfig(): Promise<{ config: Config; projectRoot: string }> {
  const projectRoot = await findProjectRoot();
  const configPath = `${projectRoot}/.claude/process-config.json`;

  try {
    const text = await Deno.readTextFile(configPath);
    const config = JSON.parse(text) as Config;
    return { config, projectRoot };
  } catch (error) {
    if (error instanceof Deno.errors.NotFound) {
      console.error(`Config not found: ${configPath}`);
      console.error("Create .claude/process-config.json with your process definitions.");
      Deno.exit(1);
    }
    throw error;
  }
}

// ============================================================================
// Port Detection
// ============================================================================

async function getPortPid(port: number): Promise<number | null> {
  try {
    const cmd = new Deno.Command("lsof", {
      args: ["-i", `:${port}`, "-t", "-sTCP:LISTEN"],
      stdout: "piped",
      stderr: "piped",
    });
    const { stdout } = await cmd.output();
    const output = new TextDecoder().decode(stdout).trim();
    if (!output) return null;
    return parseInt(output.split("\n")[0], 10);
  } catch {
    return null;
  }
}

async function getProcessCommand(pid: number): Promise<string | null> {
  try {
    const cmd = new Deno.Command("ps", {
      args: ["-p", String(pid), "-o", "command="],
      stdout: "piped",
      stderr: "piped",
    });
    const { stdout } = await cmd.output();
    const output = new TextDecoder().decode(stdout).trim();
    return output || null;
  } catch {
    return null;
  }
}

// ============================================================================
// Health Check
// ============================================================================

async function checkHealth(url: string, timeout: number): Promise<boolean> {
  try {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), timeout);
    const response = await fetch(url, { signal: controller.signal });
    clearTimeout(timeoutId);
    return response.ok;
  } catch {
    return false;
  }
}

// ============================================================================
// Process Control
// ============================================================================

async function startProcess(
  id: string,
  proc: ProcessConfig,
  projectRoot: string,
  defaults: Config["defaults"]
): Promise<{ success: boolean; pid?: number; message: string }> {
  const startupTime = proc.startupTime ?? defaults?.startupTime ?? DEFAULT_STARTUP_TIME;

  // Check if already running
  const existingPid = await getPortPid(proc.port);
  if (existingPid) {
    return {
      success: true,
      pid: existingPid,
      message: `Already running on port ${proc.port} (PID: ${existingPid})`,
    };
  }

  // Start process detached with nohup
  const cwd = proc.cwd ? `${projectRoot}/${proc.cwd}` : projectRoot;
  const cmd = new Deno.Command("sh", {
    args: ["-c", `cd "${cwd}" && nohup ${proc.command} > /dev/null 2>&1 &`],
    cwd: projectRoot,
    stdout: "null",
    stderr: "null",
  });
  await cmd.output();

  // Wait for startup
  await new Promise((resolve) => setTimeout(resolve, startupTime));

  // Verify started
  const pid = await getPortPid(proc.port);
  if (pid) {
    return {
      success: true,
      pid,
      message: `Started on port ${proc.port} (PID: ${pid})`,
    };
  }

  return {
    success: false,
    message: `Failed to start - port ${proc.port} not listening after ${startupTime}ms`,
  };
}

async function stopProcess(
  id: string,
  proc: ProcessConfig
): Promise<{ success: boolean; pid?: number; message: string }> {
  const pid = await getPortPid(proc.port);
  if (!pid) {
    return { success: true, message: "Not running" };
  }

  // Send SIGTERM
  try {
    const kill = new Deno.Command("kill", {
      args: [String(pid)],
      stdout: "null",
      stderr: "null",
    });
    await kill.output();
  } catch {
    // Ignore errors
  }

  // Wait for port to be free
  const deadline = Date.now() + STOP_TIMEOUT;
  while (Date.now() < deadline) {
    const stillRunning = await getPortPid(proc.port);
    if (!stillRunning) {
      return { success: true, pid, message: `Stopped (was PID: ${pid})` };
    }
    await new Promise((resolve) => setTimeout(resolve, 200));
  }

  // Force kill
  try {
    const kill9 = new Deno.Command("kill", {
      args: ["-9", String(pid)],
      stdout: "null",
      stderr: "null",
    });
    await kill9.output();
    await new Promise((resolve) => setTimeout(resolve, 500));
  } catch {
    // Ignore errors
  }

  const stillExists = await getPortPid(proc.port);
  if (stillExists) {
    return { success: false, pid, message: `Failed to stop PID ${pid}` };
  }

  return { success: true, pid, message: `Force stopped (was PID: ${pid})` };
}

// ============================================================================
// Commands
// ============================================================================

async function cmdList(config: Config, jsonOutput: boolean): Promise<void> {
  const processes = Object.entries(config.processes).map(([id, proc]) => ({
    id,
    name: proc.name ?? id,
    port: proc.port,
    command: proc.command,
    group: proc.group,
    hasHealthCheck: !!proc.healthCheck,
  }));

  if (jsonOutput) {
    console.log(JSON.stringify({ processes, groups: config.groups ?? {} }, null, 2));
    return;
  }

  console.log("\nConfigured Processes:");
  console.log("─".repeat(80));
  console.log(
    "ID".padEnd(20) +
      "Port".padEnd(8) +
      "Group".padEnd(12) +
      "Command"
  );
  console.log("─".repeat(80));

  for (const p of processes) {
    console.log(
      p.id.padEnd(20) +
        String(p.port).padEnd(8) +
        (p.group ?? "-").padEnd(12) +
        p.command.slice(0, 38)
    );
  }

  if (config.groups && Object.keys(config.groups).length > 0) {
    console.log("\nGroups:");
    console.log("─".repeat(40));
    for (const [name, members] of Object.entries(config.groups)) {
      console.log(`  ${name}: ${members.join(", ")}`);
    }
  }
  console.log();
}

async function cmdStatus(
  config: Config,
  target: string | null,
  all: boolean,
  jsonOutput: boolean
): Promise<void> {
  const defaults = config.defaults;
  const healthTimeout = defaults?.healthCheckTimeout ?? DEFAULT_HEALTH_TIMEOUT;

  let processIds: string[];
  if (all) {
    processIds = Object.keys(config.processes);
  } else if (target) {
    // Check if it's a group
    if (config.groups?.[target]) {
      processIds = config.groups[target];
    } else if (config.processes[target]) {
      processIds = [target];
    } else {
      console.error(`Unknown process or group: ${target}`);
      Deno.exit(1);
    }
  } else {
    console.error("Specify a process name, group, or use --all");
    Deno.exit(1);
  }

  const statuses: ProcessStatus[] = [];

  for (const id of processIds) {
    const proc = config.processes[id];
    if (!proc) continue;

    const pid = await getPortPid(proc.port);
    const status: ProcessStatus = {
      id,
      name: proc.name ?? id,
      port: proc.port,
      status: pid ? "RUNNING" : "STOPPED",
      pid: pid ?? undefined,
    };

    if (pid && proc.healthCheck) {
      status.healthy = await checkHealth(proc.healthCheck.url, healthTimeout);
    }

    if (pid) {
      status.command = (await getProcessCommand(pid)) ?? undefined;
    }

    statuses.push(status);
  }

  if (jsonOutput) {
    console.log(JSON.stringify({ processes: statuses }, null, 2));
    return;
  }

  console.log("\nProcess Status:");
  console.log("─".repeat(80));

  for (const s of statuses) {
    const statusStr =
      s.status === "RUNNING"
        ? s.healthy === undefined
          ? `RUNNING (PID: ${s.pid})`
          : s.healthy
          ? `RUNNING (PID: ${s.pid}) [healthy]`
          : `RUNNING (PID: ${s.pid}) [unhealthy]`
        : "STOPPED";

    const color = s.status === "RUNNING" ? "\x1b[32m" : "\x1b[31m";
    const reset = "\x1b[0m";

    console.log(`  ${s.name.padEnd(20)} :${s.port}  ${color}${statusStr}${reset}`);
  }
  console.log();

  // Exit with error if any process is stopped (useful for scripts)
  const allRunning = statuses.every((s) => s.status === "RUNNING");
  if (!allRunning) {
    Deno.exit(1);
  }
}

async function cmdPorts(config: Config, jsonOutput: boolean): Promise<void> {
  const configuredPorts = new Set(
    Object.values(config.processes).map((p) => p.port)
  );
  const allPorts = new Set([...configuredPorts, ...COMMON_PORTS]);

  const portInfo: Array<{
    port: number;
    configured: boolean;
    processId?: string;
    pid?: number;
    command?: string;
  }> = [];

  for (const port of [...allPorts].sort((a, b) => a - b)) {
    const pid = await getPortPid(port);
    const configEntry = Object.entries(config.processes).find(
      ([, p]) => p.port === port
    );

    portInfo.push({
      port,
      configured: configuredPorts.has(port),
      processId: configEntry?.[0],
      pid: pid ?? undefined,
      command: pid ? (await getProcessCommand(pid)) ?? undefined : undefined,
    });
  }

  if (jsonOutput) {
    console.log(JSON.stringify({ ports: portInfo }, null, 2));
    return;
  }

  console.log("\nPort Usage:");
  console.log("─".repeat(80));

  for (const p of portInfo) {
    const status = p.pid ? `PID ${p.pid}` : "free";
    const configured = p.configured
      ? `[${p.processId}]`
      : p.pid
      ? "[unknown]"
      : "";

    const color = p.pid ? (p.configured ? "\x1b[32m" : "\x1b[33m") : "\x1b[90m";
    const reset = "\x1b[0m";

    console.log(
      `  ${color}:${String(p.port).padEnd(6)} ${status.padEnd(12)} ${configured}${reset}`
    );
  }
  console.log();
}

async function cmdStart(
  config: Config,
  projectRoot: string,
  target: string,
  jsonOutput: boolean
): Promise<void> {
  // Resolve target to process IDs
  let processIds: string[];
  if (config.groups?.[target]) {
    processIds = config.groups[target];
  } else if (config.processes[target]) {
    processIds = [target];
  } else {
    console.error(`Unknown process or group: ${target}`);
    Deno.exit(1);
  }

  const results: Array<{
    id: string;
    success: boolean;
    pid?: number;
    message: string;
  }> = [];

  for (const id of processIds) {
    const proc = config.processes[id];
    if (!proc) continue;

    if (!jsonOutput) {
      console.log(`Starting ${proc.name ?? id}...`);
    }

    const result = await startProcess(id, proc, projectRoot, config.defaults);
    results.push({ id, ...result });

    if (!jsonOutput) {
      const color = result.success ? "\x1b[32m" : "\x1b[31m";
      const reset = "\x1b[0m";
      console.log(`  ${color}${result.message}${reset}`);
    }
  }

  if (jsonOutput) {
    console.log(JSON.stringify({ results }, null, 2));
  }

  const allSuccess = results.every((r) => r.success);
  if (!allSuccess) {
    Deno.exit(1);
  }
}

async function cmdStop(
  config: Config,
  target: string,
  jsonOutput: boolean
): Promise<void> {
  // Resolve target to process IDs
  let processIds: string[];
  if (config.groups?.[target]) {
    processIds = config.groups[target];
  } else if (config.processes[target]) {
    processIds = [target];
  } else {
    console.error(`Unknown process or group: ${target}`);
    Deno.exit(1);
  }

  const results: Array<{
    id: string;
    success: boolean;
    pid?: number;
    message: string;
  }> = [];

  for (const id of processIds) {
    const proc = config.processes[id];
    if (!proc) continue;

    if (!jsonOutput) {
      console.log(`Stopping ${proc.name ?? id}...`);
    }

    const result = await stopProcess(id, proc);
    results.push({ id, ...result });

    if (!jsonOutput) {
      const color = result.success ? "\x1b[32m" : "\x1b[31m";
      const reset = "\x1b[0m";
      console.log(`  ${color}${result.message}${reset}`);
    }
  }

  if (jsonOutput) {
    console.log(JSON.stringify({ results }, null, 2));
  }

  const allSuccess = results.every((r) => r.success);
  if (!allSuccess) {
    Deno.exit(1);
  }
}

async function cmdRestart(
  config: Config,
  projectRoot: string,
  target: string,
  jsonOutput: boolean
): Promise<void> {
  if (!jsonOutput) {
    console.log(`\nRestarting ${target}...\n`);
  }

  // Stop first
  await cmdStop(config, target, jsonOutput);

  // Wait for ports to clear
  await new Promise((resolve) => setTimeout(resolve, 1000));

  // Then start
  await cmdStart(config, projectRoot, target, jsonOutput);
}

// ============================================================================
// Help
// ============================================================================

function printHelp(): void {
  console.log(`
process-manager v${VERSION} - Manage dev servers and long-running processes

Usage:
  deno run --allow-run --allow-read --allow-net scripts/process-manager.ts <command> [options]

Commands:
  list                    List all configured processes
  status [name|--all]     Check process status
  ports                   Show port usage summary
  start <name|group>      Start a process or group
  stop <name|group>       Stop a process or group
  restart <name|group>    Restart a process or group

Options:
  --json                  Output as JSON
  --all                   Apply to all processes (for status)
  -h, --help              Show this help

Examples:
  # Check all processes
  deno run --allow-run --allow-read --allow-net scripts/process-manager.ts status --all

  # Start the authoring API
  deno run --allow-run --allow-read --allow-net scripts/process-manager.ts start authoring-api

  # Start all authoring processes
  deno run --allow-run --allow-read --allow-net scripts/process-manager.ts start authoring

  # Stop everything
  deno run --allow-run --allow-read scripts/process-manager.ts stop all

  # Check ports
  deno run --allow-run --allow-read scripts/process-manager.ts ports

Configuration:
  Place your process definitions in .claude/process-config.json
`);
}

// ============================================================================
// Main
// ============================================================================

async function main(): Promise<void> {
  const args = Deno.args;

  // Parse flags
  const jsonOutput = args.includes("--json");
  const showAll = args.includes("--all");
  const showHelp = args.includes("-h") || args.includes("--help");

  // Remove flags from args
  const positional = args.filter(
    (a) => !a.startsWith("-") || (a !== "--json" && a !== "--all" && a !== "-h" && a !== "--help")
  );

  if (showHelp || positional.length === 0) {
    printHelp();
    Deno.exit(0);
  }

  const command = positional[0];
  const target = positional[1];

  // Load config
  const { config, projectRoot } = await loadConfig();

  switch (command) {
    case "list":
      await cmdList(config, jsonOutput);
      break;

    case "status":
      await cmdStatus(config, target, showAll, jsonOutput);
      break;

    case "ports":
      await cmdPorts(config, jsonOutput);
      break;

    case "start":
      if (!target) {
        console.error("Specify a process or group to start");
        Deno.exit(1);
      }
      await cmdStart(config, projectRoot, target, jsonOutput);
      break;

    case "stop":
      if (!target) {
        console.error("Specify a process or group to stop");
        Deno.exit(1);
      }
      await cmdStop(config, target, jsonOutput);
      break;

    case "restart":
      if (!target) {
        console.error("Specify a process or group to restart");
        Deno.exit(1);
      }
      await cmdRestart(config, projectRoot, target, jsonOutput);
      break;

    default:
      console.error(`Unknown command: ${command}`);
      printHelp();
      Deno.exit(1);
  }
}

// Run
main();
