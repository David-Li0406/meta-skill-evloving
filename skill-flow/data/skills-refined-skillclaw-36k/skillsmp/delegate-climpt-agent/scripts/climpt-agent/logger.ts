/**
 * @fileoverview JSONL Logger for Climpt Agent
 * @module climpt-plugins/skills/delegate-climpt-agent/scripts/logger
 */

import { ensureDir } from "@std/fs";
import { join } from "@std/path";

import type { LogEntry, LogLevel, LogSummary } from "./types.ts";

/**
 * Logger that writes JSONL to file
 */
export class Logger {
  private logFile: Deno.FsFile | null = null;
  private logPath: string = "";
  private assistantMessages: string[] = [];
  private resultCost: number = 0;
  private resultStatus: "success" | "error" | "pending" = "pending";

  async init(logDir: string, maxFiles: number = 100): Promise<void> {
    await ensureDir(logDir);
    await this.rotateLogs(logDir, maxFiles);

    const timestamp = new Date().toISOString().replace(/[:.]/g, "-");
    this.logPath = join(logDir, `climpt-agent-${timestamp}.jsonl`);
    this.logFile = await Deno.open(this.logPath, {
      write: true,
      create: true,
      truncate: true,
    });
    await this.writeLog("info", "Log started", { logPath: this.logPath });
  }

  /**
   * Rotate logs: keep only the most recent N files
   */
  private async rotateLogs(logDir: string, maxFiles: number): Promise<void> {
    const files: Array<{ name: string; mtime: Date }> = [];

    try {
      for await (const entry of Deno.readDir(logDir)) {
        if (entry.isFile && entry.name.endsWith(".jsonl")) {
          const filePath = join(logDir, entry.name);
          const stat = await Deno.stat(filePath);
          files.push({ name: filePath, mtime: stat.mtime || new Date(0) });
        }
      }
    } catch {
      return;
    }

    files.sort((a, b) => b.mtime.getTime() - a.mtime.getTime());

    for (let i = maxFiles; i < files.length; i++) {
      try {
        // deno-lint-ignore no-await-in-loop
        await Deno.remove(files[i].name);
      } catch {
        // Ignore deletion errors
      }
    }
  }

  private async writeLog(
    level: LogLevel,
    message: string,
    metadata?: Record<string, unknown>,
  ): Promise<void> {
    const entry: LogEntry = {
      timestamp: new Date().toISOString(),
      level,
      message,
      ...(metadata && { metadata }),
    };

    if (this.logFile) {
      const line = JSON.stringify(entry) + "\n";
      await this.logFile.write(new TextEncoder().encode(line));
    }
  }

  async write(
    message: string,
    metadata?: Record<string, unknown>,
  ): Promise<void> {
    await this.writeLog("info", message, metadata);
  }

  async writeAssistant(message: string): Promise<void> {
    this.assistantMessages.push(message);
    await this.writeLog("assistant", message);
  }

  async writeSystem(
    message: string,
    metadata?: Record<string, unknown>,
  ): Promise<void> {
    await this.writeLog("system", message, metadata);
  }

  async writeResult(
    status: "success" | "error",
    cost?: number,
    metadata?: Record<string, unknown>,
  ): Promise<void> {
    this.resultStatus = status;
    if (cost !== undefined) {
      this.resultCost = cost;
    }
    await this.writeLog(
      "result",
      status === "success" ? "Completed" : "Failed",
      {
        status,
        ...(cost !== undefined && { cost }),
        ...metadata,
      },
    );
  }

  async writeError(
    message: string,
    metadata?: Record<string, unknown>,
  ): Promise<void> {
    await this.writeLog("error", message, metadata);
  }

  async writeSection(title: string, content: string): Promise<void> {
    await this.writeLog("info", title, { content });
  }

  async close(): Promise<void> {
    if (this.logFile) {
      await this.writeLog("info", "Log ended");
      this.logFile.close();
      this.logFile = null;
    }
  }

  getLogPath(): string {
    return this.logPath;
  }

  getSummary(): LogSummary {
    return {
      status: this.resultStatus,
      cost: this.resultCost,
      messageCount: this.assistantMessages.length,
    };
  }
}
