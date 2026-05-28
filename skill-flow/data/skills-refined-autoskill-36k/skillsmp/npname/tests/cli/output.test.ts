import { describe, expect, it } from "bun:test";

import {
  formatJson,
  formatQuiet,
  formatResult,
  formatSummary,
  formatValidation,
} from "../../src/cli/output";
import { type CliResult } from "../../src/cli/types";

const createCliResult = (overrides: Partial<CliResult> = {}): CliResult => ({
  available: null,
  errors: [],
  name: "test-package",
  valid: true,
  validForNewPackages: true,
  warnings: [],
  ...overrides,
});

describe("formatResult", () => {
  describe("available packages", () => {
    it("should format an available package with success symbol", () => {
      const result = createCliResult({
        available: true,
        name: "my-package",
      });

      const output = formatResult(result);

      expect(output).toContain("my-package");
      expect(output).toContain("available");
    });

    it("should include errors when present", () => {
      const result = createCliResult({
        available: true,
        errors: ["name is too long"],
        name: "my-package",
      });

      const output = formatResult(result);

      expect(output).toContain("name is too long");
    });

    it("should include warnings when present", () => {
      const result = createCliResult({
        available: true,
        name: "my-package",
        warnings: ["name contains capital letters"],
      });

      const output = formatResult(result);

      expect(output).toContain("name contains capital letters");
    });

    it("should include suggestions when present", () => {
      const result = createCliResult({
        available: true,
        name: "My-Package",
        suggestions: ["my-package"],
      });

      const output = formatResult(result);

      expect(output).toContain("my-package");
      expect(output).toContain("Suggestions");
    });
  });

  describe("unavailable packages", () => {
    it("should format an unavailable package with error symbol", () => {
      const result = createCliResult({
        available: false,
        name: "express",
      });

      const output = formatResult(result);

      expect(output).toContain("express");
      expect(output).toContain("unavailable");
    });
  });

  describe("invalid packages", () => {
    it("should format a package with error message", () => {
      const result = createCliResult({
        error: "Network error",
        name: "my-package",
      });

      const output = formatResult(result);

      expect(output).toContain("my-package");
      expect(output).toContain("Network error");
    });

    it("should show error line for packages with errors", () => {
      const result = createCliResult({
        error: "Invalid package name",
        name: "INVALID",
      });

      const output = formatResult(result);

      expect(output).toContain("INVALID");
      expect(output).toContain("Invalid package name");
    });
  });

  describe("edge cases", () => {
    it("should handle null availability as unknown", () => {
      const result = createCliResult({
        available: null,
        name: "unknown-pkg",
      });
      const output = formatResult(result);
      expect(output).toContain("unknown");
    });

    it("should format multiple errors and warnings together", () => {
      const result = createCliResult({
        available: true,
        errors: ["error1", "error2"],
        name: "pkg",
        warnings: ["warning1", "warning2"],
      });
      const output = formatResult(result);
      expect(output).toContain("error1");
      expect(output).toContain("error2");
      expect(output).toContain("warning1");
      expect(output).toContain("warning2");
    });

    it("should not show suggestions section for empty array", () => {
      const result = createCliResult({
        available: true,
        name: "pkg",
        suggestions: [],
      });
      const output = formatResult(result);
      expect(output).not.toContain("Suggestions");
    });
  });
});

describe("formatValidation", () => {
  describe("valid packages", () => {
    it("should format a valid package for new packages", () => {
      const result = createCliResult({
        name: "valid-package",
        valid: true,
        validForNewPackages: true,
      });

      const output = formatValidation(result);

      expect(output).toContain("valid-package");
      expect(output).toContain("valid for new packages");
    });
  });

  describe("old-only valid packages", () => {
    it("should format a package valid only for old packages", () => {
      const result = createCliResult({
        name: "UPPERCASE",
        valid: true,
        validForNewPackages: false,
        warnings: ["name can no longer contain capital letters"],
      });

      const output = formatValidation(result);

      expect(output).toContain("UPPERCASE");
      expect(output).toContain("valid for old packages only");
    });

    it("should include warnings for old-only valid packages", () => {
      const result = createCliResult({
        name: "http",
        valid: true,
        validForNewPackages: false,
        warnings: ["http is a core module name"],
      });

      const output = formatValidation(result);

      expect(output).toContain("http is a core module name");
    });
  });

  describe("invalid packages", () => {
    it("should format an invalid package", () => {
      const result = createCliResult({
        errors: ["name cannot start with a period"],
        name: ".invalid",
        valid: false,
        validForNewPackages: false,
      });

      const output = formatValidation(result);

      expect(output).toContain(".invalid");
      expect(output).toContain("invalid");
    });

    it("should include errors for invalid packages", () => {
      const result = createCliResult({
        errors: ["name cannot be empty"],
        name: "",
        valid: false,
        validForNewPackages: false,
      });

      const output = formatValidation(result);

      expect(output).toContain("name cannot be empty");
    });

    it("should format package with error property", () => {
      const result = createCliResult({
        error: "Validation failed",
        name: "test",
        valid: false,
        validForNewPackages: false,
      });

      const output = formatValidation(result);

      expect(output).toContain("test");
      expect(output).toContain("Validation failed");
    });
  });
});

describe("formatJson", () => {
  describe("single result", () => {
    it("should return valid JSON for a single result", () => {
      const result = createCliResult({
        available: true,
        name: "my-package",
      });

      const output = formatJson([result]);
      const parsed = JSON.parse(output);

      expect(parsed.name).toBe("my-package");
      expect(parsed.available).toBe(true);
    });

    it("should not wrap single result in array", () => {
      const result = createCliResult({ name: "single" });

      const output = formatJson([result]);
      const parsed = JSON.parse(output);

      expect(Array.isArray(parsed)).toBe(false);
      expect(parsed.name).toBe("single");
    });

    it("should include all result properties", () => {
      const result = createCliResult({
        available: false,
        errors: ["error1"],
        name: "test",
        suggestions: ["suggestion1"],
        valid: false,
        validForNewPackages: false,
        warnings: ["warning1"],
      });

      const output = formatJson([result]);
      const parsed = JSON.parse(output);

      expect(parsed.name).toBe("test");
      expect(parsed.available).toBe(false);
      expect(parsed.valid).toBe(false);
      expect(parsed.validForNewPackages).toBe(false);
      expect(parsed.errors).toEqual(["error1"]);
      expect(parsed.warnings).toEqual(["warning1"]);
      expect(parsed.suggestions).toEqual(["suggestion1"]);
    });
  });

  describe("multiple results", () => {
    it("should return valid JSON array for multiple results", () => {
      const results = [
        createCliResult({ available: true, name: "pkg1" }),
        createCliResult({ available: false, name: "pkg2" }),
      ];

      const output = formatJson(results);
      const parsed = JSON.parse(output);

      expect(Array.isArray(parsed)).toBe(true);
      expect(parsed).toHaveLength(2);
    });

    it("should preserve order of results", () => {
      const results = [
        createCliResult({ name: "first" }),
        createCliResult({ name: "second" }),
        createCliResult({ name: "third" }),
      ];

      const output = formatJson(results);
      const parsed = JSON.parse(output);

      expect(parsed[0].name).toBe("first");
      expect(parsed[1].name).toBe("second");
      expect(parsed[2].name).toBe("third");
    });

    it("should include all properties for each result", () => {
      const results = [
        createCliResult({
          available: true,
          name: "available-pkg",
          valid: true,
          validForNewPackages: true,
        }),
        createCliResult({
          available: false,
          errors: ["taken"],
          name: "taken-pkg",
          valid: true,
          validForNewPackages: true,
        }),
      ];

      const output = formatJson(results);
      const parsed = JSON.parse(output);

      expect(parsed[0].available).toBe(true);
      expect(parsed[1].available).toBe(false);
      expect(parsed[1].errors).toEqual(["taken"]);
    });
  });

  describe("edge cases", () => {
    it("should handle empty arrays", () => {
      const output = formatJson([]);
      const parsed = JSON.parse(output);

      expect(parsed).toEqual([]);
    });

    it("should format JSON with proper indentation", () => {
      const result = createCliResult({ name: "pkg" });
      const output = formatJson([result]);
      expect(output).toContain("  ");
      expect(output.split("\n").length).toBeGreaterThan(1);
    });

    it("should handle results with undefined suggestions", () => {
      const result = createCliResult({
        name: "no-suggestions",
        suggestions: undefined,
      });

      const output = formatJson([result]);
      const parsed = JSON.parse(output);

      expect(parsed.suggestions).toBeUndefined();
    });

    it("should handle results with error property", () => {
      const result = createCliResult({
        error: "Something went wrong",
        name: "errored",
      });

      const output = formatJson([result]);
      const parsed = JSON.parse(output);

      expect(parsed.error).toBe("Something went wrong");
    });
  });
});

describe("formatQuiet", () => {
  it("should return only available package names", () => {
    const results = [
      createCliResult({ available: true, name: "available-1" }),
      createCliResult({ available: false, name: "taken" }),
      createCliResult({ available: true, name: "available-2" }),
    ];

    const output = formatQuiet(results);

    expect(output).toContain("available-1");
    expect(output).toContain("available-2");
    expect(output).not.toContain("taken");
  });

  it("should return empty string when no packages are available", () => {
    const results = [
      createCliResult({ available: false, name: "taken-1" }),
      createCliResult({ available: false, name: "taken-2" }),
    ];

    const output = formatQuiet(results);

    expect(output).toBe("");
  });

  it("should return names separated by newlines", () => {
    const results = [
      createCliResult({ available: true, name: "pkg1" }),
      createCliResult({ available: true, name: "pkg2" }),
      createCliResult({ available: true, name: "pkg3" }),
    ];

    const output = formatQuiet(results);
    const lines = output.split("\n");

    expect(lines).toHaveLength(3);
    expect(lines[0]).toBe("pkg1");
    expect(lines[1]).toBe("pkg2");
    expect(lines[2]).toBe("pkg3");
  });

  it("should exclude packages with null availability", () => {
    const results = [
      createCliResult({ available: true, name: "available" }),
      createCliResult({ available: null, name: "unknown" }),
    ];

    const output = formatQuiet(results);

    expect(output).toBe("available");
  });

  it("should handle single available package", () => {
    const results = [createCliResult({ available: true, name: "only-one" })];

    const output = formatQuiet(results);

    expect(output).toBe("only-one");
  });

  it("should handle empty results array", () => {
    const output = formatQuiet([]);

    expect(output).toBe("");
  });
});

describe("formatSummary", () => {
  describe("edge cases", () => {
    it("should handle empty results array in check mode", () => {
      const output = formatSummary([], "check");
      expect(output).toContain("0");
    });
  });

  describe("check mode", () => {
    it("should show available and taken counts", () => {
      const results = [
        createCliResult({ available: true, name: "pkg1" }),
        createCliResult({ available: true, name: "pkg2" }),
        createCliResult({ available: false, name: "pkg3" }),
      ];

      const output = formatSummary(results, "check");

      expect(output).toContain("2 available");
      expect(output).toContain("1 taken");
    });

    it("should show errored count when there are errors", () => {
      const results = [
        createCliResult({ available: true, name: "pkg1" }),
        createCliResult({ error: "Network error", name: "pkg2" }),
      ];

      const output = formatSummary(results, "check");

      expect(output).toContain("1 available");
      expect(output).toContain("1 errored");
    });

    it("should not show errored when there are no errors", () => {
      const results = [
        createCliResult({ available: true, name: "pkg1" }),
        createCliResult({ available: false, name: "pkg2" }),
      ];

      const output = formatSummary(results, "check");

      expect(output).not.toContain("errored");
    });

    it("should show Summary header", () => {
      const results = [createCliResult({ available: true, name: "pkg" })];

      const output = formatSummary(results, "check");

      expect(output).toContain("Summary:");
    });

    it("should handle all available packages", () => {
      const results = [
        createCliResult({ available: true, name: "pkg1" }),
        createCliResult({ available: true, name: "pkg2" }),
      ];

      const output = formatSummary(results, "check");

      expect(output).toContain("2 available");
      expect(output).toContain("0 taken");
    });

    it("should handle all taken packages", () => {
      const results = [
        createCliResult({ available: false, name: "pkg1" }),
        createCliResult({ available: false, name: "pkg2" }),
      ];

      const output = formatSummary(results, "check");

      expect(output).toContain("0 available");
      expect(output).toContain("2 taken");
    });
  });

  describe("validate mode", () => {
    it("should show valid and invalid counts", () => {
      const results = [
        createCliResult({
          name: "valid-pkg",
          valid: true,
          validForNewPackages: true,
        }),
        createCliResult({
          name: "invalid-pkg",
          valid: false,
          validForNewPackages: false,
        }),
      ];

      const output = formatSummary(results, "validate");

      expect(output).toContain("1 valid");
      expect(output).toContain("1 invalid");
    });

    it("should show legacy only count when there are old-only valid packages", () => {
      const results = [
        createCliResult({
          name: "new-valid",
          valid: true,
          validForNewPackages: true,
        }),
        createCliResult({
          name: "old-only",
          valid: true,
          validForNewPackages: false,
        }),
      ];

      const output = formatSummary(results, "validate");

      expect(output).toContain("1 valid");
      expect(output).toContain("1 legacy only");
    });

    it("should not show legacy only when there are no old-only valid packages", () => {
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

      const output = formatSummary(results, "validate");

      expect(output).not.toContain("legacy only");
    });

    it("should show Summary header", () => {
      const results = [
        createCliResult({
          name: "pkg",
          valid: true,
          validForNewPackages: true,
        }),
      ];

      const output = formatSummary(results, "validate");

      expect(output).toContain("Summary:");
    });

    it("should handle all valid packages", () => {
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

      const output = formatSummary(results, "validate");

      expect(output).toContain("2 valid");
      expect(output).toContain("0 invalid");
    });

    it("should handle all invalid packages", () => {
      const results = [
        createCliResult({
          name: "pkg1",
          valid: false,
          validForNewPackages: false,
        }),
        createCliResult({
          name: "pkg2",
          valid: false,
          validForNewPackages: false,
        }),
      ];

      const output = formatSummary(results, "validate");

      expect(output).toContain("0 valid");
      expect(output).toContain("2 invalid");
    });

    it("should handle mixed valid, legacy-only, and invalid packages", () => {
      const results = [
        createCliResult({
          name: "new-valid",
          valid: true,
          validForNewPackages: true,
        }),
        createCliResult({
          name: "old-only-1",
          valid: true,
          validForNewPackages: false,
        }),
        createCliResult({
          name: "old-only-2",
          valid: true,
          validForNewPackages: false,
        }),
        createCliResult({
          name: "invalid",
          valid: false,
          validForNewPackages: false,
        }),
      ];

      const output = formatSummary(results, "validate");

      expect(output).toContain("1 valid");
      expect(output).toContain("2 legacy only");
      expect(output).toContain("1 invalid");
    });
  });
});
