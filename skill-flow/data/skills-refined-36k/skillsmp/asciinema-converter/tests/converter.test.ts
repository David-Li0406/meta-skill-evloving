/**
 * Unit tests for asciinema-converter skill utilities
 *
 * Run with: bun test plugins/asciinema-tools/skills/asciinema-converter/tests/
 */

import { describe, expect, it, beforeAll, afterAll } from "bun:test";
import { existsSync, mkdirSync, rmSync, writeFileSync, statSync } from "fs";
import { join } from "path";

const FIXTURES_DIR = join(import.meta.dir, "fixtures");
const TMP_DIR = join(import.meta.dir, "tmp");

// Test fixture: minimal valid .cast file
const MINIMAL_CAST = `{"version": 2, "width": 80, "height": 24, "timestamp": 1705600000, "duration": 5.0}
[0.0, "o", "Hello"]
[1.0, "o", " World"]
[2.0, "o", "\\r\\n"]
[3.0, "o", "$ exit"]
[4.0, "o", "\\r\\n"]
`;

// iTerm2 filename format test cases
const ITERM2_FILENAMES = [
  {
    filename:
      "20260118_232025.Claude Code.w0t1p1.70C05103-2F29-4B42-8067-BE475DB6126A.68721.4013739999.cast",
    expected: {
      timestamp: "20260118_232025",
      profile: "Claude Code",
      termid: "w0t1p1",
      uuid: "70C05103-2F29-4B42-8067-BE475DB6126A",
      pid: "68721",
      autoLogId: "4013739999",
    },
  },
  {
    filename:
      "20260119_120000.Default.w1t0p0.AAAAAAAA-BBBB-CCCC-DDDD-EEEEEEEEEEEE.12345.9999999999.cast",
    expected: {
      timestamp: "20260119_120000",
      profile: "Default",
      termid: "w1t0p0",
      uuid: "AAAAAAAA-BBBB-CCCC-DDDD-EEEEEEEEEEEE",
      pid: "12345",
      autoLogId: "9999999999",
    },
  },
  {
    filename:
      "20260101_000000.my.profile.name.w0t0p0.12345678-ABCD-1234-5678-ABCDEF012345.999.1.cast",
    expected: {
      timestamp: "20260101_000000",
      profile: "my.profile.name",
      termid: "w0t0p0",
      uuid: "12345678-ABCD-1234-5678-ABCDEF012345",
      pid: "999",
      autoLogId: "1",
    },
  },
];

/**
 * Parse iTerm2 auto-log filename (right-to-left parsing)
 */
function parseITerm2Filename(filename: string): Record<string, string> | null {
  // Remove .cast extension
  const base = filename.replace(/\.cast$/, "");
  const parts = base.split(".");

  // Need at least 6 parts: timestamp, profile (1+), termid, uuid, pid, autoLogId
  if (parts.length < 6) return null;

  // Parse from right
  const autoLogId = parts.pop()!;
  const pid = parts.pop()!;

  // UUID has hyphens, find it
  const uuidIndex = parts.findIndex((p) =>
    /^[A-F0-9]{8}-[A-F0-9]{4}-[A-F0-9]{4}-[A-F0-9]{4}-[A-F0-9]{12}$/i.test(p)
  );

  if (uuidIndex === -1) return null;

  const uuid = parts[uuidIndex];
  const termid = parts[uuidIndex - 1];

  // Everything before termid is timestamp.profile
  const beforeTermid = parts.slice(0, uuidIndex - 1);
  const timestamp = beforeTermid[0];
  const profile = beforeTermid.slice(1).join(".");

  return { timestamp, profile, termid, uuid, pid, autoLogId };
}

/**
 * Calculate compression ratio
 */
function calculateCompressionRatio(
  inputSize: number,
  outputSize: number
): number {
  if (outputSize <= 0) return 0;
  return Math.floor(inputSize / outputSize);
}

/**
 * Check if .txt file exists for given .cast file
 */
function txtExists(castPath: string, outputDir: string): boolean {
  const basename = castPath.replace(/\.cast$/, "");
  const txtPath = join(outputDir, `${basename}.txt`);
  return existsSync(txtPath);
}

describe("iTerm2 Filename Parsing", () => {
  for (const testCase of ITERM2_FILENAMES) {
    it(`should parse ${testCase.filename}`, () => {
      const result = parseITerm2Filename(testCase.filename);
      expect(result).not.toBeNull();
      expect(result!.timestamp).toBe(testCase.expected.timestamp);
      expect(result!.profile).toBe(testCase.expected.profile);
      expect(result!.termid).toBe(testCase.expected.termid);
      expect(result!.uuid).toBe(testCase.expected.uuid);
      expect(result!.pid).toBe(testCase.expected.pid);
      expect(result!.autoLogId).toBe(testCase.expected.autoLogId);
    });
  }

  it("should return null for invalid filename", () => {
    expect(parseITerm2Filename("invalid.cast")).toBeNull();
    expect(parseITerm2Filename("simple.cast")).toBeNull();
    expect(parseITerm2Filename("no-uuid.here.cast")).toBeNull();
  });
});

describe("Compression Ratio Calculation", () => {
  it("should calculate correct ratio", () => {
    expect(calculateCompressionRatio(1000, 10)).toBe(100);
    expect(calculateCompressionRatio(950000, 1000)).toBe(950);
    expect(calculateCompressionRatio(100, 100)).toBe(1);
  });

  it("should handle edge cases", () => {
    expect(calculateCompressionRatio(1000, 0)).toBe(0);
    expect(calculateCompressionRatio(0, 100)).toBe(0);
    expect(calculateCompressionRatio(0, 0)).toBe(0);
  });

  it("should floor the result", () => {
    expect(calculateCompressionRatio(100, 3)).toBe(33);
    expect(calculateCompressionRatio(1000, 7)).toBe(142);
  });
});

describe("Skip Existing Logic", () => {
  beforeAll(() => {
    // Create tmp directory
    if (!existsSync(TMP_DIR)) {
      mkdirSync(TMP_DIR, { recursive: true });
    }
    // Create a test .txt file
    writeFileSync(join(TMP_DIR, "existing.txt"), "test content");
  });

  afterAll(() => {
    // Cleanup
    if (existsSync(TMP_DIR)) {
      rmSync(TMP_DIR, { recursive: true });
    }
  });

  it("should detect existing .txt file", () => {
    expect(txtExists("existing.cast", TMP_DIR)).toBe(true);
  });

  it("should return false for missing .txt file", () => {
    expect(txtExists("missing.cast", TMP_DIR)).toBe(false);
  });
});

describe("Fixture Validation", () => {
  it("should have valid fixtures directory", () => {
    expect(existsSync(FIXTURES_DIR)).toBe(true);
  });

  it("minimal.cast fixture should be valid NDJSON", () => {
    const lines = MINIMAL_CAST.trim().split("\n");

    // First line is header
    const header = JSON.parse(lines[0]);
    expect(header.version).toBe(2);
    expect(header.width).toBe(80);
    expect(header.height).toBe(24);

    // Remaining lines are events
    for (let i = 1; i < lines.length; i++) {
      const event = JSON.parse(lines[i]);
      expect(Array.isArray(event)).toBe(true);
      expect(event.length).toBe(3);
      expect(typeof event[0]).toBe("number"); // timestamp
      expect(typeof event[1]).toBe("string"); // event type
      expect(typeof event[2]).toBe("string"); // data
    }
  });
});

describe("Path Handling", () => {
  it("should handle paths with spaces", () => {
    const pathWithSpaces = "/path/to/my file.cast";
    const basename = pathWithSpaces.split("/").pop()!.replace(/\.cast$/, "");
    expect(basename).toBe("my file");
  });

  it("should handle paths with special characters", () => {
    const specialPath = "/path/to/file-with_special.chars!.cast";
    const basename = specialPath.split("/").pop()!.replace(/\.cast$/, "");
    expect(basename).toBe("file-with_special.chars!");
  });

  it("should extract basename correctly", () => {
    const paths = [
      { input: "/a/b/c.cast", expected: "c" },
      { input: "simple.cast", expected: "simple" },
      { input: "/path/to/file.cast", expected: "file" },
    ];

    for (const { input, expected } of paths) {
      const basename = input.split("/").pop()!.replace(/\.cast$/, "");
      expect(basename).toBe(expected);
    }
  });
});

describe("Size Calculations", () => {
  beforeAll(() => {
    if (!existsSync(TMP_DIR)) {
      mkdirSync(TMP_DIR, { recursive: true });
    }
    // Create test files with known sizes
    writeFileSync(join(TMP_DIR, "small.txt"), "x".repeat(100));
    writeFileSync(join(TMP_DIR, "medium.txt"), "x".repeat(10000));
  });

  afterAll(() => {
    if (existsSync(TMP_DIR)) {
      rmSync(TMP_DIR, { recursive: true });
    }
  });

  it("should get correct file sizes", () => {
    const smallSize = statSync(join(TMP_DIR, "small.txt")).size;
    const mediumSize = statSync(join(TMP_DIR, "medium.txt")).size;

    expect(smallSize).toBe(100);
    expect(mediumSize).toBe(10000);
  });

  it("should calculate ratio from file sizes", () => {
    const inputSize = 100000;
    const outputSize = 100;
    const ratio = calculateCompressionRatio(inputSize, outputSize);
    expect(ratio).toBe(1000);
  });
});
