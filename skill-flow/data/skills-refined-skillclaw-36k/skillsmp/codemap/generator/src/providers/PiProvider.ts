/**
 * Pi CLI 提供者
 */

import { spawn } from "child_process";
import { BaseProvider } from "./BaseProvider.js";
import type { CodeMap } from "../types.js";

export class PiProvider extends BaseProvider {
  name = "pi";

  async generate(
    prompt: string,
    modelTier: "fast" | "smart",
  ): Promise<CodeMap> {
    console.error("Calling Pi CLI...");
    console.error("Prompt length:", prompt.length);
    console.error("Model tier:", modelTier);

    const systemPrompt = `You are a code architecture analyst. Generate a structured CodeMap JSON based on the provided code and query.

Required format:
{
  "schemaVersion": 1,
  "title": "Title",
  "description": "Description",
  "created_at": "ISO8601 timestamp",
  "traces": [
    {
      "id": "1",
      "title": "Step title",
      "description": "Step description",
      "locations": [
        {
          "id": "1a",
          "path": "File path",
          "lineNumber": 1,
          "lineContent": "Code line",
          "title": "Node title",
          "description": "Node description"
        }
      ],
      "traceTextDiagram": "Tree diagram",
      "traceGuide": "Markdown format guide"
    }
  ]
}

Rules:
- Plain JSON only, no markdown code blocks
- Ensure all quotes and brackets are properly closed
- Must include schemaVersion field (number 1)`;

    const args = [
      "--print",
      "--model",
      "z-ai/glm4.7",
      "--provider",
      "nvidia",
      "--no-skills",
      "--system-prompt",
      systemPrompt,
      prompt,
    ];

    const output = await this.executeCommand("pi", args);
    const codemap = this.parseOutput(output);
    return this.validateCodemap(codemap);
  }

  async analyze(prompt: string): Promise<any> {
    console.error("Analyzing with Pi CLI...");

    const args = ["--print", "--model", "z-ai/glm4.7", prompt];

    const output = await this.executeCommand("pi", args);
    return JSON.parse(output);
  }

  private async executeCommand(cmd: string, args: string[]): Promise<string> {
    return new Promise((resolve, reject) => {
      console.error("Executing command:", cmd, args.join(" "));

      const cli = spawn(cmd, args, {
        stdio: ["pipe", "pipe", "pipe"],
      });

      let stdout = "";
      let stderr = "";
      let outputBuffer = "";

      cli.stdout.on("data", (data) => {
        const chunk = data.toString();
        stdout += chunk;
        outputBuffer += chunk;
        console.error("stdout chunk:", chunk.substring(0, 200));
      });

      cli.stderr.on("data", (data) => {
        const chunk = data.toString();
        stderr += chunk;
        console.error("stderr:", chunk);
      });

      cli.on("close", (code) => {
        console.error("Pi CLI exit code:", code);
        console.error("Total stdout length:", stdout.length);
        console.error("Total stderr length:", stderr.length);

        if (code !== 0) {
          const errorMsg = `Pi CLI exited with code ${code}`;
          console.error(errorMsg);
          console.error("Full stderr:", stderr);
          reject(new Error(`${errorMsg}: ${stderr || "Unknown error"}`));
          return;
        }

        if (!stdout.trim()) {
          console.error("No stdout output");
          reject(new Error("Pi CLI produced no output"));
          return;
        }

        resolve(stdout);
      });

      cli.on("error", (error) => {
        console.error("Pi CLI spawn error:", error);
        reject(new Error(`Failed to spawn Pi CLI: ${error.message}`));
      });

      // 120 秒超时
      const timeoutMs = 120000;
      setTimeout(() => {
        console.error(`Pi CLI timeout after ${timeoutMs / 1000} seconds`);
        cli.kill("SIGTERM");
        setTimeout(() => cli.kill("SIGKILL"), 5000);
        reject(new Error(`Pi CLI timeout after ${timeoutMs / 1000} seconds`));
      }, timeoutMs);
    });
  }

  private parseOutput(stdout: string): any {
    console.error("Pi CLI output length:", stdout.length);

    // 检查是否是流式 JSON（每行都是 JSON）
    const lines = stdout
      .trim()
      .split("\n")
      .filter((line) => line.trim());
    const isStreaming = lines.every((line) => {
      try {
        JSON.parse(line);
        return true;
      } catch {
        return false;
      }
    });

    if (isStreaming && lines.length > 1) {
      console.error("Detected streaming JSON format, parsing...");
      return this.parseStreamingOutput(stdout);
    } else {
      console.error("Detected plain JSON format, parsing directly...");
      return this.parsePlainOutput(stdout);
    }
  }

  private parseStreamingOutput(stdout: string): any {
    const lines = stdout
      .trim()
      .split("\n")
      .filter((line) => line.trim());
    console.error("Total lines:", lines.length);

    let fullContent = "";

    // 解析流式 JSON
    for (const line of lines) {
      try {
        const json = JSON.parse(line);

        if (json.type === "message_update" && json.assistantMessageEvent) {
          const event = json.assistantMessageEvent;

          // 优先提取 delta
          if (event.delta && typeof event.delta === "string") {
            fullContent += event.delta;
          }

          // 提取 content
          if (event.content && Array.isArray(event.content)) {
            for (const item of event.content) {
              if (item.type === "text" && item.text) {
                fullContent += item.text;
              }
            }
          }
        }

        // 提取最终消息
        if (
          json.message &&
          json.message.content &&
          Array.isArray(json.message.content)
        ) {
          for (const item of json.message.content) {
            if (item.type === "text" && item.text) {
              fullContent += item.text;
            }
          }
        }
      } catch (e) {
        console.error("Failed to parse line:", line.substring(0, 100));
      }
    }

    console.error("Extracted content length:", fullContent.length);

    // 如果没有提取到内容，尝试直接使用原始输出
    if (!fullContent.trim()) {
      console.error("Using raw stdout");
      fullContent = stdout;
    }

    // 尝试提取 JSON
    return this.extractJson(fullContent);
  }

  private parsePlainOutput(stdout: string): any {
    // 直接解析 JSON
    return this.extractJson(stdout);
  }

  private extractJson(content: string): any {
    console.error(
      "Extracting JSON from content (length: " + content.length + ")",
    );

    // 尝试从 markdown 代码块提取
    try {
      return this.extractJsonFromMarkdown(content);
    } catch (e) {
      console.error("Markdown extraction failed, trying direct parse");
    }

    // 尝试直接解析
    try {
      return JSON.parse(content.trim());
    } catch (e2) {
      console.error("Direct parse failed, trying first object extraction");
    }

    // 尝试提取第一个 JSON 对象
    return this.extractFirstJsonObject(content);
  }

  /**
   * 尝试修复截断的 JSON
   */
  private attemptJsonRepair(content: string): any {
    console.error("Attempting JSON repair...");

    try {
      const lastBrace = content.lastIndexOf("}");

      if (lastBrace === -1) {
        throw new Error("No closing brace found");
      }

      let openBraces = 0;
      let openBrackets = 0;
      let inString = false;
      let escape = false;

      for (let i = content.indexOf("{"); i <= lastBrace; i++) {
        const char = content[i];

        if (escape) {
          escape = false;
          continue;
        }

        if (char === "\\") {
          escape = true;
          continue;
        }

        if (char === '"') {
          inString = !inString;
        }

        if (!inString) {
          if (char === "{") openBraces++;
          if (char === "}") openBraces--;
          if (char === "[") openBrackets++;
          if (char === "]") openBrackets--;
        }
      }

      let repaired = content;

      if (inString) {
        repaired =
          repaired.substring(0, lastBrace) +
          '"' +
          repaired.substring(lastBrace);
      }

      while (openBrackets > 0) {
        repaired += "]";
        openBrackets--;
      }
      while (openBraces > 0) {
        repaired += "}";
        openBraces--;
      }

      console.error("JSON repair completed");
      return JSON.parse(repaired);
    } catch (e) {
      console.error("JSON repair failed:", e);
      throw e;
    }
  }

  /**
   * 从内容中提取第一个完整的 JSON 对象
   */
  protected extractFirstJsonObject(content: string): any {
    console.error("Trying extractFirstJsonObject...");

    try {
      return this.attemptJsonRepair(content);
    } catch (e) {
      console.error("Extract/repair failed, trying simple extraction...");
    }

    const firstBrace = content.indexOf("{");
    const lastBrace = content.lastIndexOf("}");
    if (firstBrace !== -1 && lastBrace !== -1 && lastBrace > firstBrace) {
      return JSON.parse(content.substring(firstBrace, lastBrace + 1));
    }
    throw new Error("Could not extract JSON object");
  }
}
