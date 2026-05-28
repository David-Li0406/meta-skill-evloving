#!/usr/bin/env bun
/**
 * Converts markdown to styled HTML for pasting into Google Docs.
 * Uses pandoc with custom CSS for clean tables, code blocks, etc.
 *
 * Usage: bun md-to-html.ts <markdown-file>
 */

import { writeFile, unlink } from "fs/promises";
import { spawn } from "child_process";
import { basename, dirname } from "path";
import { tmpdir } from "os";
import { join } from "path";

const CSS = `
body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  line-height: 1.6;
  max-width: 900px;
  margin: 0 auto;
  padding: 2rem;
  color: #333;
}
h1, h2, h3, h4 {
  color: #1a1a1a;
  margin-top: 1.5em;
}
h1 { border-bottom: 2px solid #eee; padding-bottom: 0.3em; }
h2 { border-bottom: 1px solid #eee; padding-bottom: 0.2em; }
table {
  border-collapse: collapse;
  margin: 1em 0;
  font-size: 0.9em;
}
th, td {
  border: 1px solid #ddd;
  padding: 6px 10px;
  text-align: left;
}
th {
  background: #f8f9fa;
  font-weight: 600;
}
code {
  background: #f4f4f4;
  padding: 2px 6px;
  border-radius: 3px;
  font-size: 0.9em;
}
pre {
  background: #f8f9fa;
  padding: 1rem;
  border-radius: 6px;
  overflow-x: auto;
}
pre code {
  background: none;
  padding: 0;
}
blockquote {
  border-left: 4px solid #ddd;
  margin: 1em 0;
  padding-left: 1em;
  color: #666;
}
img { max-width: 100%; height: auto; }
`;

function runCommand(
  command: string,
  args: string[]
): Promise<{ code: number; stdout: string; stderr: string }> {
  return new Promise((resolve) => {
    const proc = spawn(command, args, { shell: true });
    let stdout = "";
    let stderr = "";

    proc.stdout.on("data", (data: Buffer) => {
      stdout += data.toString();
    });
    proc.stderr.on("data", (data: Buffer) => {
      stderr += data.toString();
    });
    proc.on("close", (code) => {
      resolve({ code: code ?? 1, stdout, stderr });
    });
  });
}

async function hasPandoc(): Promise<boolean> {
  const result = await runCommand("which", ["pandoc"]);
  return result.code === 0;
}

async function main(): Promise<void> {
  const filePath = process.argv[2];

  if (!filePath) {
    console.error("Usage: bun md-to-html.ts <markdown-file>");
    process.exit(1);
  }

  const fileDir = dirname(filePath);
  const fileBasename = basename(filePath, ".md");
  const outputPath = join(tmpdir(), `${fileBasename}.html`);
  const cssPath = join(tmpdir(), "md-to-html-style.css");

  await writeFile(cssPath, CSS);

  const pandocArgs = [
    `"${filePath}"`,
    "-o",
    `"${outputPath}"`,
    `--resource-path="${fileDir}"`,
    "--embed-resources",
    "--standalone",
    `--css="${cssPath}"`,
  ];

  const usesNix = !(await hasPandoc());
  const command = usesNix
    ? `nix run nixpkgs#pandoc -- ${pandocArgs.join(" ")}`
    : `pandoc ${pandocArgs.join(" ")}`;

  console.log(usesNix ? "Using nix run for pandoc..." : "Using system pandoc...");
  console.log(`Converting ${filePath}...`);

  const result = await runCommand(command, []);

  if (result.stderr && !result.stderr.includes("Deprecated")) {
    console.error(result.stderr);
  }

  if (result.code !== 0) {
    console.error("Pandoc failed");
    process.exit(1);
  }

  await unlink(cssPath);

  console.log(`Created ${outputPath}`);
  console.log("Opening in browser...");

  await runCommand("open", [`"${outputPath}"`]);

  console.log("\nNext steps:");
  console.log("1. Cmd+A to select all in browser");
  console.log("2. Cmd+C to copy");
  console.log("3. Paste into Google Docs");
}

main().catch((error: unknown) => {
  console.error(error instanceof Error ? error.message : error);
  process.exit(1);
});
