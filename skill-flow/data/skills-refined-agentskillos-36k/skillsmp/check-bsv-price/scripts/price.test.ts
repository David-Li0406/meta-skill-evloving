import { describe, expect, it } from "bun:test";
import { existsSync } from "fs";

describe("check-bsv-price", () => {
  const scriptPath = "skills/check-bsv-price/scripts/price.ts";

  it("script exists", () => {
    expect(existsSync(scriptPath)).toBe(true);
  });

  it("--help exits with code 0", async () => {
    const proc = Bun.spawn(["bun", "run", scriptPath, "--help"], {
      stdout: "pipe",
      stderr: "pipe",
    });
    const exitCode = await proc.exited;
    expect(exitCode).toBe(0);
  });

  it("--help shows usage information", async () => {
    const proc = Bun.spawn(["bun", "run", scriptPath, "--help"], {
      stdout: "pipe",
      stderr: "pipe",
    });
    const output = await new Response(proc.stdout).text();
    await proc.exited;
    expect(output.toLowerCase()).toContain("usage");
  });

  it("fetches price successfully (live API)", async () => {
    const proc = Bun.spawn(["bun", "run", scriptPath], {
      stdout: "pipe",
      stderr: "pipe",
    });
    const output = await new Response(proc.stdout).text();
    const exitCode = await proc.exited;
    expect(exitCode).toBe(0);
    expect(output.toLowerCase()).toMatch(/price|usd|\$/);
  });

  it("--json returns valid JSON", async () => {
    const proc = Bun.spawn(["bun", "run", scriptPath, "--json"], {
      stdout: "pipe",
      stderr: "pipe",
    });
    const output = await new Response(proc.stdout).text();
    const exitCode = await proc.exited;
    expect(exitCode).toBe(0);
    const json = JSON.parse(output);
    expect(json).toHaveProperty("price");
    expect(typeof json.price).toBe("number");
  });
});
