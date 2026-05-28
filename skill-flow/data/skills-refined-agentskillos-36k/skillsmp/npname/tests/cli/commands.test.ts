import {
  afterEach,
  beforeEach,
  describe,
  expect,
  it,
  mock,
  spyOn,
} from "bun:test";

import {
  determineExitCode,
  outputResults,
  processAvailability,
  processFullCheck,
  processValidateOnly,
} from "../../src/cli/commands";
import { EXIT_CODES } from "../../src/cli/constants";
import { type CliFlags, type CliResult } from "../../src/cli/types";
import npname from "../../src/index";

const createCliResult = (overrides: Partial<CliResult> = {}): CliResult => ({
  available: null,
  errors: [],
  name: "test-package",
  valid: true,
  validForNewPackages: true,
  warnings: [],
  ...overrides,
});

const createFlags = (overrides: Partial<CliFlags> = {}): CliFlags => ({
  check: false,
  concurrency: 5,
  json: false,
  quiet: false,
  timeout: 5000,
  validate: false,
  ...overrides,
});

describe("processValidateOnly", () => {
  it("should return CliResult array for valid names", () => {
    const results = processValidateOnly(["valid-package"]);

    expect(results).toHaveLength(1);
    expect(results[0].name).toBe("valid-package");
    expect(results[0].valid).toBe(true);
    expect(results[0].validForNewPackages).toBe(true);
    expect(results[0].errors).toEqual([]);
    expect(results[0].warnings).toEqual([]);
  });

  it("should return CliResult array for invalid names", () => {
    const results = processValidateOnly([""]);

    expect(results).toHaveLength(1);
    expect(results[0].name).toBe("");
    expect(results[0].valid).toBe(false);
    expect(results[0].validForNewPackages).toBe(false);
    expect(results[0].errors.length).toBeGreaterThan(0);
  });

  it("should handle multiple names", () => {
    const results = processValidateOnly(["valid-pkg", "another-valid"]);

    expect(results).toHaveLength(2);
    expect(results[0].name).toBe("valid-pkg");
    expect(results[1].name).toBe("another-valid");
  });

  it("should set available to null for validation-only mode", () => {
    const results = processValidateOnly(["test-package"]);

    expect(results[0].available).toBeNull();
  });

  it("should return validation errors for names starting with period", () => {
    const results = processValidateOnly([".invalid"]);

    expect(results[0].valid).toBe(false);
    expect(results[0].validForNewPackages).toBe(false);
    expect(results[0].errors).toContain("name cannot start with a period");
  });

  it("should return validation errors for names starting with underscore", () => {
    const results = processValidateOnly(["_invalid"]);

    expect(results[0].valid).toBe(false);
    expect(results[0].errors).toContain("name cannot start with an underscore");
  });

  it("should return warnings for core module names", () => {
    const results = processValidateOnly(["http"]);

    expect(results[0].validForNewPackages).toBe(false);
    expect(results[0].warnings).toContain("http is a core module name");
  });

  it("should return warnings for uppercase names", () => {
    const results = processValidateOnly(["UPPERCASE"]);

    expect(results[0].validForNewPackages).toBe(false);
    expect(results[0].warnings).toContain(
      "name can no longer contain capital letters"
    );
  });

  it("should include suggestions when available", () => {
    const results = processValidateOnly(["UPPERCASE"]);

    expect(results[0].suggestions).toBeDefined();
    expect(results[0].suggestions).toContain("uppercase");
  });

  it("should handle scoped package names", () => {
    const results = processValidateOnly(["@scope/package"]);

    expect(results[0].name).toBe("@scope/package");
    expect(results[0].validForNewPackages).toBe(true);
  });

  it("should handle empty array input", () => {
    const results = processValidateOnly([]);

    expect(results).toHaveLength(0);
  });

  it("should preserve order of input names", () => {
    const names = ["first", "second", "third"];
    const results = processValidateOnly(names);

    expect(results[0].name).toBe("first");
    expect(results[1].name).toBe("second");
    expect(results[2].name).toBe("third");
  });
});

describe("determineExitCode", () => {
  describe("success scenarios (exit code 0)", () => {
    it("should return SUCCESS when all packages are available in check mode", () => {
      const results = [
        createCliResult({ available: true, name: "pkg1" }),
        createCliResult({ available: true, name: "pkg2" }),
      ];
      const flags = createFlags({ validate: false });

      const exitCode = determineExitCode(results, flags);

      expect(exitCode).toBe(EXIT_CODES.SUCCESS);
    });

    it("should return SUCCESS when all packages are valid in validate mode", () => {
      const results = [
        createCliResult({
          name: "pkg1",
          valid: true,
          validForNewPackages: true,
        }),
        createCliResult({
          name: "pkg2",
          valid: true,
          validForNewPackages: true,
        }),
      ];
      const flags = createFlags({ validate: true });

      const exitCode = determineExitCode(results, flags);

      expect(exitCode).toBe(EXIT_CODES.SUCCESS);
    });

    it("should return SUCCESS for single available package", () => {
      const results = [createCliResult({ available: true, name: "pkg" })];
      const flags = createFlags({ validate: false });

      const exitCode = determineExitCode(results, flags);

      expect(exitCode).toBe(EXIT_CODES.SUCCESS);
    });
  });

  describe("unavailable scenarios (exit code 1)", () => {
    it("should return UNAVAILABLE when any package is unavailable in check mode", () => {
      const results = [
        createCliResult({ available: true, name: "pkg1" }),
        createCliResult({ available: false, name: "pkg2" }),
      ];
      const flags = createFlags({ validate: false });

      const exitCode = determineExitCode(results, flags);

      expect(exitCode).toBe(EXIT_CODES.UNAVAILABLE);
    });

    it("should return UNAVAILABLE when all packages are unavailable in check mode", () => {
      const results = [
        createCliResult({ available: false, name: "pkg1" }),
        createCliResult({ available: false, name: "pkg2" }),
      ];
      const flags = createFlags({ validate: false });

      const exitCode = determineExitCode(results, flags);

      expect(exitCode).toBe(EXIT_CODES.UNAVAILABLE);
    });

    it("should return UNAVAILABLE when any package is invalid in validate mode", () => {
      const results = [
        createCliResult({
          name: "valid",
          valid: true,
          validForNewPackages: true,
        }),
        createCliResult({
          name: "invalid",
          valid: false,
          validForNewPackages: false,
        }),
      ];
      const flags = createFlags({ validate: true });

      const exitCode = determineExitCode(results, flags);

      expect(exitCode).toBe(EXIT_CODES.UNAVAILABLE);
    });

    it("should return UNAVAILABLE for old-only valid packages in validate mode", () => {
      const results = [
        createCliResult({
          name: "http",
          valid: true,
          validForNewPackages: false,
        }),
      ];
      const flags = createFlags({ validate: true });

      const exitCode = determineExitCode(results, flags);

      expect(exitCode).toBe(EXIT_CODES.UNAVAILABLE);
    });

    it("should return UNAVAILABLE when availability is null in check mode", () => {
      const results = [createCliResult({ available: null, name: "pkg" })];
      const flags = createFlags({ validate: false });

      const exitCode = determineExitCode(results, flags);

      expect(exitCode).toBe(EXIT_CODES.UNAVAILABLE);
    });
  });

  describe("error scenarios (exit code 2)", () => {
    it("should return ERROR when any result has an error", () => {
      const results = [
        createCliResult({ available: true, name: "pkg1" }),
        createCliResult({ error: "Network error", name: "pkg2" }),
      ];
      const flags = createFlags({ validate: false });

      const exitCode = determineExitCode(results, flags);

      expect(exitCode).toBe(EXIT_CODES.ERROR);
    });

    it("should return ERROR when all results have errors", () => {
      const results = [
        createCliResult({ error: "Error 1", name: "pkg1" }),
        createCliResult({ error: "Error 2", name: "pkg2" }),
      ];
      const flags = createFlags({ validate: false });

      const exitCode = determineExitCode(results, flags);

      expect(exitCode).toBe(EXIT_CODES.ERROR);
    });

    it("should prioritize ERROR over UNAVAILABLE", () => {
      const results = [
        createCliResult({ available: false, name: "unavailable" }),
        createCliResult({ error: "Network error", name: "errored" }),
      ];
      const flags = createFlags({ validate: false });

      const exitCode = determineExitCode(results, flags);

      expect(exitCode).toBe(EXIT_CODES.ERROR);
    });

    it("should return ERROR for validation mode with errors", () => {
      const results = [
        createCliResult({
          error: "Validation error",
          name: "pkg",
          valid: false,
          validForNewPackages: false,
        }),
      ];
      const flags = createFlags({ validate: true });

      const exitCode = determineExitCode(results, flags);

      expect(exitCode).toBe(EXIT_CODES.ERROR);
    });
  });

  describe("edge cases", () => {
    it("should handle empty results array as success in check mode", () => {
      const results: CliResult[] = [];
      const flags = createFlags({ validate: false });

      const exitCode = determineExitCode(results, flags);

      expect(exitCode).toBe(EXIT_CODES.SUCCESS);
    });

    it("should handle empty results array as success in validate mode", () => {
      const results: CliResult[] = [];
      const flags = createFlags({ validate: true });

      const exitCode = determineExitCode(results, flags);

      expect(exitCode).toBe(EXIT_CODES.SUCCESS);
    });

    it("should treat undefined error as no error", () => {
      const results = [
        createCliResult({ available: true, error: undefined, name: "pkg" }),
      ];
      const flags = createFlags({ validate: false });

      const exitCode = determineExitCode(results, flags);

      expect(exitCode).toBe(EXIT_CODES.SUCCESS);
    });
  });
});

describe("outputResults", () => {
  let originalConsoleLog: typeof console.log;
  let consoleLogs: string[];

  beforeEach(() => {
    consoleLogs = [];
    originalConsoleLog = console.log;
    console.log = mock((...args: unknown[]) => {
      consoleLogs.push(args.map(String).join(" "));
    });
  });

  afterEach(() => {
    console.log = originalConsoleLog;
  });

  describe("JSON output mode", () => {
    it("should output JSON when json flag is true", () => {
      const results = [createCliResult({ available: true, name: "pkg" })];
      const flags = createFlags({ json: true });

      outputResults(results, flags);

      expect(consoleLogs).toHaveLength(1);
      const parsed = JSON.parse(consoleLogs[0]);
      expect(parsed.name).toBe("pkg");
    });

    it("should output JSON array for multiple results", () => {
      const results = [
        createCliResult({ name: "pkg1" }),
        createCliResult({ name: "pkg2" }),
      ];
      const flags = createFlags({ json: true });

      outputResults(results, flags);

      const parsed = JSON.parse(consoleLogs[0]);
      expect(Array.isArray(parsed)).toBe(true);
      expect(parsed).toHaveLength(2);
    });
  });

  describe("quiet output mode", () => {
    it("should output only available names when quiet flag is true", () => {
      const results = [
        createCliResult({ available: true, name: "available-pkg" }),
        createCliResult({ available: false, name: "taken-pkg" }),
      ];
      const flags = createFlags({ quiet: true });

      outputResults(results, flags);

      expect(consoleLogs).toHaveLength(1);
      expect(consoleLogs[0]).toBe("available-pkg");
    });

    it("should output nothing when no packages are available", () => {
      const results = [createCliResult({ available: false, name: "taken" })];
      const flags = createFlags({ quiet: true });

      outputResults(results, flags);

      expect(consoleLogs).toHaveLength(0);
    });
  });

  describe("normal output mode", () => {
    it("should output formatted result for each package", () => {
      const results = [
        createCliResult({ available: true, name: "pkg1" }),
        createCliResult({ available: false, name: "pkg2" }),
      ];
      const flags = createFlags();

      outputResults(results, flags);

      expect(consoleLogs.length).toBeGreaterThanOrEqual(2);
      expect(consoleLogs.some((log) => log.includes("pkg1"))).toBe(true);
      expect(consoleLogs.some((log) => log.includes("pkg2"))).toBe(true);
    });

    it("should output summary for multiple results", () => {
      const results = [
        createCliResult({ available: true, name: "pkg1" }),
        createCliResult({ available: false, name: "pkg2" }),
      ];
      const flags = createFlags();

      outputResults(results, flags);

      expect(consoleLogs.some((log) => log.includes("Summary"))).toBe(true);
    });

    it("should not output summary for single result", () => {
      const results = [createCliResult({ available: true, name: "pkg" })];
      const flags = createFlags();

      outputResults(results, flags);

      expect(consoleLogs.some((log) => log.includes("Summary"))).toBe(false);
    });
  });

  describe("validate mode output", () => {
    it("should use validation formatting when validate flag is true", () => {
      const results = [
        createCliResult({
          name: "valid-pkg",
          valid: true,
          validForNewPackages: true,
        }),
      ];
      const flags = createFlags({ validate: true });

      outputResults(results, flags);

      expect(consoleLogs.some((log) => log.includes("valid-pkg"))).toBe(true);
      expect(
        consoleLogs.some((log) => log.includes("valid for new packages"))
      ).toBe(true);
    });

    it("should show validation summary for multiple validate results", () => {
      const results = [
        createCliResult({
          name: "valid",
          valid: true,
          validForNewPackages: true,
        }),
        createCliResult({
          name: "invalid",
          valid: false,
          validForNewPackages: false,
        }),
      ];
      const flags = createFlags({ validate: true });

      outputResults(results, flags);

      expect(consoleLogs.some((log) => log.includes("Summary"))).toBe(true);
      expect(consoleLogs.some((log) => log.includes("valid"))).toBe(true);
      expect(consoleLogs.some((log) => log.includes("invalid"))).toBe(true);
    });
  });
});

describe("processAvailability", () => {
  let manyMock: ReturnType<typeof spyOn>;

  beforeEach(() => {
    manyMock = spyOn(npname, "many");
  });

  afterEach(() => {
    manyMock.mockRestore();
  });

  it("should check availability for valid package names", async () => {
    manyMock.mockResolvedValue(
      new Map([
        ["valid-package", true],
        ["another-valid", false],
      ])
    );

    const flags = createFlags();
    const results = await processAvailability(
      ["valid-package", "another-valid"],
      flags
    );

    expect(results).toHaveLength(2);
    expect(results[0].name).toBe("valid-package");
    expect(results[0].available).toBe(true);
    expect(results[1].name).toBe("another-valid");
    expect(results[1].available).toBe(false);
    expect(manyMock).toHaveBeenCalledTimes(1);
  });

  it("should skip availability check for invalid names (mark as invalid without network call)", async () => {
    manyMock.mockResolvedValue(new Map([["valid-package", true]]));

    const flags = createFlags();
    const results = await processAvailability(
      ["valid-package", ".invalid-name"],
      flags
    );

    expect(results).toHaveLength(2);

    // Valid name should have been checked
    expect(results[0].name).toBe("valid-package");
    expect(results[0].available).toBe(true);
    expect(results[0].valid).toBe(true);

    // Invalid name should be marked as invalid without network call
    expect(results[1].name).toBe(".invalid-name");
    expect(results[1].available).toBeNull();
    expect(results[1].valid).toBe(false);
    expect(results[1].validForNewPackages).toBe(false);

    // npname.many should only be called with valid names
    expect(manyMock).toHaveBeenCalledWith(
      ["valid-package"],
      expect.any(Object)
    );
  });

  it("should handle network errors gracefully", async () => {
    manyMock.mockRejectedValue(new Error("Network timeout"));

    const flags = createFlags();
    const results = await processAvailability(["test-package"], flags);

    expect(results).toHaveLength(1);
    expect(results[0].name).toBe("test-package");
    expect(results[0].available).toBeNull();
    expect(results[0].error).toBe("Network timeout");
  });

  it("should respect concurrency flag", async () => {
    manyMock.mockResolvedValue(new Map([["test-pkg", true]]));

    const flags = createFlags({ concurrency: 10 });
    await processAvailability(["test-pkg"], flags);

    expect(manyMock).toHaveBeenCalledWith(
      ["test-pkg"],
      expect.objectContaining({ concurrency: 10 })
    );
  });

  it("should respect timeout flag", async () => {
    manyMock.mockResolvedValue(new Map([["test-pkg", true]]));

    const flags = createFlags({ timeout: 10_000 });
    await processAvailability(["test-pkg"], flags);

    expect(manyMock).toHaveBeenCalledWith(
      ["test-pkg"],
      expect.objectContaining({ timeout: 10_000 })
    );
  });

  it("should not show spinner in quiet mode", async () => {
    manyMock.mockResolvedValue(new Map([["test-pkg", true]]));

    const flags = createFlags({ quiet: true });
    const results = await processAvailability(["test-pkg"], flags);

    // Results should still be returned correctly even in quiet mode
    expect(results).toHaveLength(1);
    expect(results[0].available).toBe(true);
  });

  it("should not show spinner in json mode", async () => {
    manyMock.mockResolvedValue(new Map([["test-pkg", true]]));

    const flags = createFlags({ json: true });
    const results = await processAvailability(["test-pkg"], flags);

    // Results should still be returned correctly even in json mode
    expect(results).toHaveLength(1);
    expect(results[0].available).toBe(true);
  });

  it("should preserve input order in results", async () => {
    manyMock.mockResolvedValue(
      new Map([
        ["third-pkg", true],
        ["first-pkg", false],
        ["second-pkg", true],
      ])
    );

    const flags = createFlags();
    const results = await processAvailability(
      ["first-pkg", "second-pkg", "third-pkg"],
      flags
    );

    expect(results[0].name).toBe("first-pkg");
    expect(results[1].name).toBe("second-pkg");
    expect(results[2].name).toBe("third-pkg");
  });

  it("should handle mixed valid and invalid names while preserving order", async () => {
    manyMock.mockResolvedValue(
      new Map([
        ["valid-first", true],
        ["valid-third", false],
      ])
    );

    const flags = createFlags();
    const results = await processAvailability(
      ["valid-first", "_invalid", "valid-third"],
      flags
    );

    expect(results[0].name).toBe("valid-first");
    expect(results[0].available).toBe(true);

    expect(results[1].name).toBe("_invalid");
    expect(results[1].available).toBeNull();
    expect(results[1].validForNewPackages).toBe(false);

    expect(results[2].name).toBe("valid-third");
    expect(results[2].available).toBe(false);
  });

  it("should pass registry flag when provided", async () => {
    manyMock.mockResolvedValue(new Map([["test-pkg", true]]));

    const flags = createFlags({ registry: "https://custom-registry.com" });
    await processAvailability(["test-pkg"], flags);

    expect(manyMock).toHaveBeenCalledWith(
      ["test-pkg"],
      expect.objectContaining({ registryUrl: "https://custom-registry.com" })
    );
  });
});

describe("processFullCheck", () => {
  let checkMock: ReturnType<typeof spyOn>;

  beforeEach(() => {
    checkMock = spyOn(npname, "check");
  });

  afterEach(() => {
    checkMock.mockRestore();
  });

  it("should process names sequentially", async () => {
    const callOrder: string[] = [];

    checkMock.mockImplementation((name: string) => {
      callOrder.push(name);
      return Promise.resolve({
        available: true,
        name,
        validation: {
          errors: [],
          suggestions: undefined,
          valid: true,
          validForNewPackages: true,
          validForOldPackages: true,
          warnings: [],
        },
      });
    });

    const flags = createFlags({ check: true });
    await processFullCheck(["first", "second", "third"], flags);

    expect(callOrder).toEqual(["first", "second", "third"]);
  });

  it("should handle check errors for individual packages", async () => {
    checkMock
      .mockResolvedValueOnce({
        available: true,
        name: "working-pkg",
        validation: {
          errors: [],
          valid: true,
          validForNewPackages: true,
          validForOldPackages: true,
          warnings: [],
        },
      })
      .mockRejectedValueOnce(new Error("Check failed"));

    const flags = createFlags({ check: true });
    const results = await processFullCheck(
      ["working-pkg", "failing-pkg"],
      flags
    );

    expect(results).toHaveLength(2);
    expect(results[0].name).toBe("working-pkg");
    expect(results[0].available).toBe(true);
    expect(results[0].error).toBeUndefined();

    expect(results[1].name).toBe("failing-pkg");
    expect(results[1].available).toBeNull();
    expect(results[1].error).toBe("Check failed");
  });

  it("should include validation details in results", async () => {
    checkMock.mockResolvedValue({
      available: false,
      name: "test-package",
      validation: {
        errors: [],
        suggestions: ["test-pkg"],
        valid: true,
        validForNewPackages: true,
        validForOldPackages: true,
        warnings: ["some warning"],
      },
    });

    const flags = createFlags({ check: true });
    const results = await processFullCheck(["test-package"], flags);

    expect(results[0].valid).toBe(true);
    expect(results[0].validForNewPackages).toBe(true);
    expect(results[0].warnings).toEqual(["some warning"]);
    expect(results[0].suggestions).toEqual(["test-pkg"]);
  });

  it("should use registry flag when provided", async () => {
    checkMock.mockResolvedValue({
      available: true,
      name: "test-pkg",
      validation: {
        errors: [],
        valid: true,
        validForNewPackages: true,
        validForOldPackages: true,
        warnings: [],
      },
    });

    const flags = createFlags({
      check: true,
      registry: "https://custom-registry.com",
    });
    await processFullCheck(["test-pkg"], flags);

    expect(checkMock).toHaveBeenCalledWith(
      "test-pkg",
      expect.objectContaining({ registryUrl: "https://custom-registry.com" })
    );
  });

  it("should use timeout flag when provided", async () => {
    checkMock.mockResolvedValue({
      available: true,
      name: "test-pkg",
      validation: {
        errors: [],
        valid: true,
        validForNewPackages: true,
        validForOldPackages: true,
        warnings: [],
      },
    });

    const flags = createFlags({ check: true, timeout: 15_000 });
    await processFullCheck(["test-pkg"], flags);

    expect(checkMock).toHaveBeenCalledWith(
      "test-pkg",
      expect.objectContaining({ timeout: 15_000 })
    );
  });

  it("should not show spinner in quiet mode", async () => {
    checkMock.mockResolvedValue({
      available: true,
      name: "test-pkg",
      validation: {
        errors: [],
        valid: true,
        validForNewPackages: true,
        validForOldPackages: true,
        warnings: [],
      },
    });

    const flags = createFlags({ check: true, quiet: true });
    const results = await processFullCheck(["test-pkg"], flags);

    expect(results).toHaveLength(1);
    expect(results[0].available).toBe(true);
  });

  it("should not show spinner in json mode", async () => {
    checkMock.mockResolvedValue({
      available: true,
      name: "test-pkg",
      validation: {
        errors: [],
        valid: true,
        validForNewPackages: true,
        validForOldPackages: true,
        warnings: [],
      },
    });

    const flags = createFlags({ check: true, json: true });
    const results = await processFullCheck(["test-pkg"], flags);

    expect(results).toHaveLength(1);
    expect(results[0].available).toBe(true);
  });

  it("should handle error message from CheckResult", async () => {
    checkMock.mockResolvedValue({
      available: null,
      error: new Error("Invalid package name"),
      name: "test-pkg",
      validation: {
        errors: ["name is invalid"],
        valid: false,
        validForNewPackages: false,
        validForOldPackages: false,
        warnings: [],
      },
    });

    const flags = createFlags({ check: true });
    const results = await processFullCheck(["test-pkg"], flags);

    expect(results[0].available).toBeNull();
    expect(results[0].error).toBe("Invalid package name");
    expect(results[0].valid).toBe(false);
    expect(results[0].errors).toEqual(["name is invalid"]);
  });

  it("should handle non-Error thrown values", async () => {
    checkMock.mockRejectedValue("String error");

    const flags = createFlags({ check: true });
    const results = await processFullCheck(["test-pkg"], flags);

    expect(results[0].error).toBe("String error");
    expect(results[0].available).toBeNull();
  });

  it("should return empty array for empty input", async () => {
    const flags = createFlags({ check: true });
    const results = await processFullCheck([], flags);

    expect(results).toHaveLength(0);
    expect(checkMock).not.toHaveBeenCalled();
  });
});
