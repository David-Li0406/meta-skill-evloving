/**
 * AI 提供者基类
 */

import type { CodeMap } from "../types.js";

export abstract class BaseProvider implements AIProvider {
  abstract name: string;
  abstract generate(
    prompt: string,
    modelTier: "fast" | "smart",
  ): Promise<CodeMap>;
  abstract analyze(prompt: string): Promise<any>;

  /**
   * 验证 CodeMap 结构
   */
  protected validateCodemap(codemap: any): CodeMap {
    console.error("Validating codemap...");

    // 添加缺失的必需字段
    if (!codemap.created_at) {
      codemap.created_at = new Date().toISOString();
    }

    if (!codemap.title) {
      codemap.title = "Untitled CodeMap";
    }

    if (!codemap.description) {
      codemap.description = codemap.title;
    }

    // 验证 schemaVersion
    if (!codemap.schemaVersion) {
      codemap.schemaVersion = 1;
    }

    // 确保 traces 是数组
    if (!codemap.traces || !Array.isArray(codemap.traces)) {
      console.error("Codemap has no traces, creating empty array");
      codemap.traces = [];
    }

    console.error("✅ Codemap validated:", {
      schemaVersion: codemap.schemaVersion,
      title: codemap.title,
      tracesCount: codemap.traces?.length || 0,
    });

    return codemap as CodeMap;
  }

  /**
   * 从 Markdown 代码块中提取 JSON
   */
  protected extractJsonFromMarkdown(content: string): any {
    const jsonMatch = content.match(/```(?:json)?\s*(\{[\s\S]*?\n\})\s*```/);
    if (jsonMatch) {
      return JSON.parse(jsonMatch[1]);
    }
    throw new Error("Could not extract JSON from markdown block");
  }

  /**
   * 从内容中提取第一个完整的 JSON 对象
   */
  protected extractFirstJsonObject(content: string): any {
    const firstBrace = content.indexOf("{");
    const lastBrace = content.lastIndexOf("}");
    if (firstBrace !== -1 && lastBrace !== -1 && lastBrace > firstBrace) {
      return JSON.parse(content.substring(firstBrace, lastBrace + 1));
    }
    throw new Error("Could not extract JSON object");
  }
}
