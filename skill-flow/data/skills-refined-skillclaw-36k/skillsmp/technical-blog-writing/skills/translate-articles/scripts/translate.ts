#!/usr/bin/env npx -y tsx

import { readdir, readFile, writeFile } from "fs/promises";
import { execSync } from "child_process";
import { join } from "path";

const BLOG_DIR = "data/blog";
const GEMINI_MODEL = "gemini-3-pro-preview";

interface TranslationTarget {
  slug: string;
  sourcePath: string;
  content: string;
  missingLangs: ("es" | "ca")[];
}

// Technical terms that should remain in English (engineers are used to these)
const TECHNICAL_TERMS = [
  // General programming
  "flag",
  "flags",
  "commit",
  "merge",
  "rebase",
  "branch",
  "pull request",
  "push",
  "bug",
  "debug",
  "fix",
  "build",
  "deploy",
  "release",
  "cache",
  "buffer",
  "callback",
  "promise",
  "async",
  "await",
  "framework",
  "library",
  "runtime",
  "script",
  "shebang",
  "stack",
  "heap",
  "queue",
  "string",
  "array",
  "object",
  "map",
  "set",
  "type",
  "interface",
  "enum",
  "variable",
  "constant",
  "function",
  "method",
  "class",
  // Web & frontend
  "API",
  "REST",
  "GraphQL",
  "CLI",
  "terminal",
  "shell",
  "component",
  "props",
  "state",
  "hooks",
  "DOM",
  "event",
  "handler",
  "frontend",
  "backend",
  "fullstack",
  "middleware",
  "endpoint",
  "render",
  "hydrate",
  "router",
  "route",
  // Tools & technologies
  "TypeScript",
  "JavaScript",
  "React",
  "Node.js",
  "Deno",
  "Bun",
  "npm",
  "yarn",
  "pnpm",
  "Git",
  "GitHub",
  "GitLab",
  "Docker",
  "Kubernetes",
  "VS Code",
  "IDE",
  // DevOps & infrastructure
  "CI/CD",
  "pipeline",
  "container",
  "pod",
  "environment",
  "staging",
  "production",
  "log",
  "logging",
  "server",
  "serverless",
  "test",
  "unit test",
  "integration test",
];

const TRANSLATION_PROMPTS = {
  es: `Translate this blog article from English to Spanish (Castellano from Spain).

RULES:
- Translate the "title" and "spoiler" fields in the YAML frontmatter
- Keep "tags" in English exactly as they are (site requirement)
- Keep all other frontmatter fields unchanged (date, draft, etc.)
- Preserve all markdown formatting, code blocks, and links exactly
- Keep these technical terms in English (engineers are used to them): ${TECHNICAL_TERMS.join(", ")}
- Use informal "tú" form
- Use Castellano conventions from Spain (not Latin American Spanish)

Return ONLY the translated markdown file, nothing else. Start with the --- frontmatter delimiter.`,

  ca: `Translate this blog article from English to Catalan.

RULES:
- Translate the "title" and "spoiler" fields in the YAML frontmatter
- Keep "tags" in English exactly as they are (site requirement)
- Keep all other frontmatter fields unchanged (date, draft, etc.)
- Preserve all markdown formatting, code blocks, and links exactly
- Keep these technical terms in English (engineers are used to them): ${TECHNICAL_TERMS.join(", ")}
- Use informal "tu" form
- Use standard Catalan conventions

Return ONLY the translated markdown file, nothing else. Start with the --- frontmatter delimiter.`,
};

async function findArticlesToTranslate(): Promise<TranslationTarget[]> {
  const files = await readdir(BLOG_DIR);

  const baseArticles = files.filter(
    (f) =>
      f.endsWith(".mdx") && !f.endsWith(".es.mdx") && !f.endsWith(".ca.mdx"),
  );

  const targets: TranslationTarget[] = [];

  for (const file of baseArticles) {
    const sourcePath = join(BLOG_DIR, file);
    const content = await readFile(sourcePath, "utf-8");

    // Check if draft
    const frontmatterMatch = content.match(/^---\n([\s\S]*?)\n---/);
    if (frontmatterMatch) {
      const frontmatter = frontmatterMatch[1];
      if (frontmatter.includes("draft: true")) {
        continue;
      }
    }

    const slug = file.replace(".mdx", "");
    const missingLangs: ("es" | "ca")[] = [];

    if (!files.includes(`${slug}.es.mdx`)) {
      missingLangs.push("es");
    }
    if (!files.includes(`${slug}.ca.mdx`)) {
      missingLangs.push("ca");
    }

    if (missingLangs.length > 0) {
      targets.push({ slug, sourcePath, content, missingLangs });
    }
  }

  return targets;
}

function cleanGeminiOutput(output: string): string {
  // Find the frontmatter start
  const frontmatterStart = output.indexOf("---");
  if (frontmatterStart === -1) {
    throw new Error("No frontmatter delimiter found in output");
  }

  // Extract from first --- onwards
  let cleaned = output.slice(frontmatterStart);

  // Remove trailing markdown code fence if present
  cleaned = cleaned.replace(/\n```\s*$/, "");

  return cleaned.trim() + "\n";
}

async function translateArticle(
  content: string,
  lang: "es" | "ca",
): Promise<string> {
  const prompt = TRANSLATION_PROMPTS[lang];
  const fullPrompt = `${prompt}\n\n---\n\n${content}`;

  // Write prompt to temp file to avoid shell escaping issues
  const tempFile = `/tmp/translate-prompt-${Date.now()}-${lang}.txt`;
  await writeFile(tempFile, fullPrompt);

  try {
    const result = execSync(`cat "${tempFile}" | gemini -m ${GEMINI_MODEL}`, {
      encoding: "utf-8",
      maxBuffer: 10 * 1024 * 1024, // 10MB
      timeout: 120000, // 2 minutes
    });

    return cleanGeminiOutput(result);
  } finally {
    // Clean up temp file
    try {
      execSync(`rm "${tempFile}"`, { encoding: "utf-8" });
    } catch {
      // Ignore cleanup errors
    }
  }
}

async function main() {
  console.log("🔍 Scanning for articles to translate...\n");

  const targets = await findArticlesToTranslate();

  if (targets.length === 0) {
    console.log("✅ All publishable articles have translations!");
    return;
  }

  console.log(
    `Found ${targets.length} article(s) with missing translations:\n`,
  );

  for (const target of targets) {
    console.log(`  📄 ${target.slug}`);
    console.log(`     Missing: ${target.missingLangs.join(", ")}`);
  }

  console.log("\n🌐 Starting translations...\n");

  const results: {
    slug: string;
    lang: string;
    success: boolean;
    error?: string;
  }[] = [];

  for (const target of targets) {
    // Translate both languages in parallel
    const translations = await Promise.allSettled(
      target.missingLangs.map(async (lang) => {
        console.log(
          `  ⏳ Translating ${target.slug} to ${lang.toUpperCase()}...`,
        );

        try {
          const translated = await translateArticle(target.content, lang);
          const outputPath = join(BLOG_DIR, `${target.slug}.${lang}.mdx`);
          await writeFile(outputPath, translated);

          console.log(`  ✅ ${target.slug}.${lang}.mdx created`);
          return { slug: target.slug, lang, success: true };
        } catch (error) {
          const errorMsg =
            error instanceof Error ? error.message : String(error);
          console.log(`  ❌ ${target.slug} (${lang}): ${errorMsg}`);
          return { slug: target.slug, lang, success: false, error: errorMsg };
        }
      }),
    );

    for (const result of translations) {
      if (result.status === "fulfilled") {
        results.push(result.value);
      } else {
        results.push({
          slug: target.slug,
          lang: "unknown",
          success: false,
          error: result.reason?.message || "Unknown error",
        });
      }
    }
  }

  console.log("\n📊 Summary:");
  const successful = results.filter((r) => r.success).length;
  const failed = results.filter((r) => !r.success).length;

  console.log(`  ✅ Successful: ${successful}`);
  if (failed > 0) {
    console.log(`  ❌ Failed: ${failed}`);
  }
}

main().catch((error) => {
  console.error("Fatal error:", error);
  process.exit(1);
});
