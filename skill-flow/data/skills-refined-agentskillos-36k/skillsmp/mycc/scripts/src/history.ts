/**
 * 历史记录处理
 * 读取 ~/.claude/projects/{encodedProjectName}/ 下的 JSONL 文件
 */

import { readFileSync, readdirSync, existsSync } from "fs";
import { homedir } from "os";
import { join } from "path";

// JSONL 行结构
interface RawHistoryLine {
  type: "user" | "assistant" | "system" | "result";
  message?: {
    role?: string;
    content?: unknown;
    id?: string;
  };
  sessionId: string;
  timestamp: string;
  uuid: string;
  parentUuid?: string | null;
  isSidechain?: boolean;
  cwd?: string;
}

// 对话摘要
export interface ConversationSummary {
  sessionId: string;
  startTime: string;
  lastTime: string;
  messageCount: number;
  lastMessagePreview: string;
}

// 对话详情
export interface ConversationHistory {
  sessionId: string;
  messages: RawHistoryLine[];
}

/**
 * 过滤系统标签
 */
function stripSystemTags(text: string): string {
  if (!text) return "";
  return text
    .replace(/<user-prompt-submit-hook[^>]*>[\s\S]*?<\/user-prompt-submit-hook>/g, "")
    .replace(/<short-term-memory[^>]*>[\s\S]*?<\/short-term-memory>/g, "")
    .replace(/<current-time[^>]*>[\s\S]*?<\/current-time>/g, "")
    .replace(/<system-reminder[^>]*>[\s\S]*?<\/system-reminder>/g, "")
    .replace(/<command-name[^>]*>[\s\S]*?<\/command-name>/g, "")
    .trim();
}

/**
 * 将项目路径编码为 Claude 使用的目录名
 * /Users/aster/AIproject/mylife → -Users-aster-AIproject-mylife
 */
export function encodeProjectPath(projectPath: string): string {
  return projectPath.replace(/\/$/, "").replace(/[/\\:._]/g, "-");
}

/**
 * 获取历史记录目录
 */
export function getHistoryDir(cwd: string): string {
  const encodedName = encodeProjectPath(cwd);
  return join(homedir(), ".claude", "projects", encodedName);
}

/**
 * 获取对话列表
 */
export function getConversationList(cwd: string): ConversationSummary[] {
  const historyDir = getHistoryDir(cwd);

  if (!existsSync(historyDir)) {
    return [];
  }

  const files = readdirSync(historyDir).filter(f => f.endsWith(".jsonl"));
  const conversations: ConversationSummary[] = [];

  for (const file of files) {
    const filePath = join(historyDir, file);
    const sessionId = file.replace(".jsonl", "");

    try {
      const summary = parseConversationSummary(filePath, sessionId);
      if (summary) {
        conversations.push(summary);
      }
    } catch (err) {
      console.error(`[History] Failed to parse ${file}:`, err);
    }
  }

  // 按最后时间倒序排列（无日期的排到最后）
  conversations.sort((a, b) => {
    const timeA = a.lastTime ? new Date(a.lastTime).getTime() : 0;
    const timeB = b.lastTime ? new Date(b.lastTime).getTime() : 0;
    return timeB - timeA;
  });

  return conversations;
}

/**
 * 解析对话摘要
 */
function parseConversationSummary(
  filePath: string,
  sessionId: string
): ConversationSummary | null {
  const content = readFileSync(filePath, "utf-8");
  const lines = content.trim().split("\n").filter(line => line.trim());

  if (lines.length === 0) {
    return null;
  }

  let startTime = "";
  let lastTime = "";
  let lastMessagePreview = "";
  let messageCount = 0;

  for (const line of lines) {
    try {
      const parsed = JSON.parse(line) as RawHistoryLine;
      messageCount++;

      // 跟踪时间戳
      if (!startTime || parsed.timestamp < startTime) {
        startTime = parsed.timestamp;
      }
      if (!lastTime || parsed.timestamp > lastTime) {
        lastTime = parsed.timestamp;
      }

      // 提取最后一条消息预览（user 消息，过滤系统标签）
      if (parsed.type === "user" && parsed.message?.content) {
        const content = parsed.message.content;
        let rawPreview = "";
        if (typeof content === "string") {
          rawPreview = content;
        } else if (Array.isArray(content)) {
          for (const item of content) {
            if (typeof item === "object" && item && "text" in item) {
              rawPreview = String((item as { text: string }).text);
              break;
            }
          }
        }
        // 过滤系统标签后截取
        const cleanPreview = stripSystemTags(rawPreview);
        if (cleanPreview) {
          lastMessagePreview = cleanPreview.substring(0, 100);
        }
      }
    } catch {
      // 忽略解析错误的行
    }
  }

  return {
    sessionId,
    startTime,
    lastTime,
    messageCount,
    lastMessagePreview: lastMessagePreview || "(无预览)",
  };
}

/**
 * 获取具体对话内容
 */
export function getConversation(
  cwd: string,
  sessionId: string
): ConversationHistory | null {
  // 验证 sessionId 格式（防止路径遍历攻击）
  if (!sessionId || /[<>:"|?*\x00-\x1f\/\\]/.test(sessionId)) {
    return null;
  }

  const historyDir = getHistoryDir(cwd);
  const filePath = join(historyDir, `${sessionId}.jsonl`);

  if (!existsSync(filePath)) {
    return null;
  }

  const content = readFileSync(filePath, "utf-8");
  const lines = content.trim().split("\n").filter(line => line.trim());
  const messages: RawHistoryLine[] = [];

  for (const line of lines) {
    try {
      const parsed = JSON.parse(line) as RawHistoryLine;
      messages.push(parsed);
    } catch {
      // 忽略解析错误的行
    }
  }

  return {
    sessionId,
    messages,
  };
}
