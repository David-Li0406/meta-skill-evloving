/**
 * Claude Code SDK 桥接
 * 核心：调用 CC SDK 的 query 函数
 */

import { query } from "@anthropic-ai/claude-code";
import { execSync } from "child_process";

// 检测 Claude CLI 路径
function detectClaudeCliPath(): string {
  try {
    return execSync("which claude", { encoding: "utf-8" }).trim();
  } catch {
    return "/usr/local/bin/claude"; // fallback
  }
}

const CLAUDE_CLI_PATH = detectClaudeCliPath();

export interface ChatOptions {
  message: string;
  sessionId?: string;
  cwd?: string;
  onMessage: (msg: unknown) => void;
  onDone: (sessionId: string) => void;
  onError: (error: string) => void;
}

/**
 * 执行 CC 对话
 */
export async function executeChat(options: ChatOptions): Promise<void> {
  const { message, sessionId, cwd, onMessage, onDone, onError } = options;

  let currentSessionId = sessionId || "";

  try {
    for await (const sdkMessage of query({
      prompt: message,
      options: {
        // 指定 CLI 路径，确保完整加载配置（包括 skills）
        executable: "node" as const,
        pathToClaudeCodeExecutable: CLAUDE_CLI_PATH,
        cwd: cwd || process.cwd(),
        resume: sessionId || undefined,
        // 小程序端无法交互确认权限，使用 bypassPermissions
        // 注意：这需要用户信任，后续可以改成更安全的模式
        permissionMode: "bypassPermissions",
      },
    })) {
      // 提取 session_id
      if (
        sdkMessage &&
        typeof sdkMessage === "object" &&
        "type" in sdkMessage &&
        sdkMessage.type === "system" &&
        "session_id" in sdkMessage
      ) {
        currentSessionId = sdkMessage.session_id as string;
      }

      // 流式发送消息
      onMessage(sdkMessage);
    }

    // 完成
    onDone(currentSessionId);
  } catch (error) {
    onError(error instanceof Error ? error.message : String(error));
  }
}

/**
 * 检查 CC CLI 是否可用
 */
export async function checkCCAvailable(): Promise<boolean> {
  try {
    const { execSync } = await import("child_process");
    execSync("claude --version", { stdio: "pipe" });
    return true;
  } catch {
    return false;
  }
}
