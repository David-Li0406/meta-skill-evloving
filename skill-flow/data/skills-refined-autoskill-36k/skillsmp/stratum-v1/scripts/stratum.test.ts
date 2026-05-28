import { describe, expect, it } from "bun:test";
import { existsSync } from "fs";

describe("stratum-v1", () => {
  const basePath = "skills/stratum-v1/scripts";

  it("parse-message.ts exists", () => {
    expect(existsSync(`${basePath}/parse-message.ts`)).toBe(true);
  });

  it("parse-message --help exits 0", async () => {
    const proc = Bun.spawn(["bun", "run", `${basePath}/parse-message.ts`, "--help"], {
      stdout: "pipe",
      stderr: "pipe",
    });
    const exitCode = await proc.exited;
    expect(exitCode).toBe(0);
  });

  it("parse-message --help shows usage", async () => {
    const proc = Bun.spawn(["bun", "run", `${basePath}/parse-message.ts`, "--help"], {
      stdout: "pipe",
      stderr: "pipe",
    });
    const output = await new Response(proc.stdout).text();
    await proc.exited;
    expect(output.toLowerCase()).toContain("usage");
  });

  it("parse-message decodes mining.subscribe", async () => {
    const msg = '{"id":1,"method":"mining.subscribe","params":["Agent/1.0"]}';
    const proc = Bun.spawn(["bun", "run", `${basePath}/parse-message.ts`, msg], {
      stdout: "pipe",
      stderr: "pipe",
    });
    const output = await new Response(proc.stdout).text();
    const exitCode = await proc.exited;
    expect(exitCode).toBe(0);
    expect(output.toLowerCase()).toContain("subscribe");
  });

  it("parse-message rejects invalid JSON", async () => {
    const proc = Bun.spawn(["bun", "run", `${basePath}/parse-message.ts`, "not-json"], {
      stdout: "pipe",
      stderr: "pipe",
    });
    const exitCode = await proc.exited;
    expect(exitCode).not.toBe(0);
  });

  it("build-coinbase.ts exists", () => {
    expect(existsSync(`${basePath}/build-coinbase.ts`)).toBe(true);
  });

  it("build-coinbase --help exits 0", async () => {
    const proc = Bun.spawn(["bun", "run", `${basePath}/build-coinbase.ts`, "--help"], {
      stdout: "pipe",
      stderr: "pipe",
    });
    const exitCode = await proc.exited;
    expect(exitCode).toBe(0);
  });

  it("calculate-share.ts exists", () => {
    expect(existsSync(`${basePath}/calculate-share.ts`)).toBe(true);
  });

  it("calculate-share --help exits 0", async () => {
    const proc = Bun.spawn(["bun", "run", `${basePath}/calculate-share.ts`, "--help"], {
      stdout: "pipe",
      stderr: "pipe",
    });
    const exitCode = await proc.exited;
    expect(exitCode).toBe(0);
  });
});
