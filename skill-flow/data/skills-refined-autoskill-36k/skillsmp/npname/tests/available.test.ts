import { describe, expect, it } from "bun:test";

import { checkAvailability, checkAvailabilityMany } from "../src/available";
import { InvalidNameError } from "../src/types";

describe("checkAvailability", () => {
  describe("available packages", () => {
    it("should return true for an available package name", async () => {
      const result = await checkAvailability(
        "this-package-definitely-does-not-exist-xyz123abc"
      );
      expect(result).toBe(true);
    });

    it("should return true for available scoped package (404 on public registry)", async () => {
      const result = await checkAvailability("@nonexistent-scope-xyz/pkg-test");
      // Public npm registry returns 404 for non-existent scoped packages
      expect(result).toBe(true);
    });
  });

  describe("taken packages", () => {
    it("should return false for a taken package (chalk)", async () => {
      const result = await checkAvailability("chalk");
      expect(result).toBe(false);
    });

    it("should return false for a taken package (lodash)", async () => {
      const result = await checkAvailability("lodash");
      expect(result).toBe(false);
    });

    it("should return false for taken scoped package", async () => {
      const result = await checkAvailability("@types/node");
      expect(result).toBe(false);
    });
  });

  describe("scoped packages", () => {
    it("should handle scoped package names correctly", async () => {
      const result = await checkAvailability("@types/node");
      expect(typeof result).toBe("boolean");
    });

    it("should URL-encode scoped package names", async () => {
      const result = await checkAvailability("@babel/core");
      expect(result).toBe(false);
    });
  });

  describe("organization checks", () => {
    it("should return boolean or null for organization availability check", async () => {
      const result = await checkAvailability("@vercel");
      // Returns false (taken), true (available), or null (auth required)
      expect([true, false, null]).toContain(result);
    });

    it("should throw InvalidNameError for organization name with trailing slash", async () => {
      await expect(checkAvailability("@vercel/")).rejects.toThrow(
        InvalidNameError
      );
    });

    it("should return true for non-existent organization", async () => {
      const result = await checkAvailability(
        "@this-org-definitely-does-not-exist-xyz123"
      );
      // npmjs.com returns 404 for non-existent orgs
      expect(result).toBe(true);
    });
  });

  describe("invalid names", () => {
    it("should throw InvalidNameError for empty name", async () => {
      await expect(checkAvailability("")).rejects.toThrow();
    });

    it("should throw InvalidNameError for name starting with period", async () => {
      await expect(checkAvailability(".invalid")).rejects.toThrow(
        InvalidNameError
      );
    });

    it("should throw InvalidNameError for name starting with hyphen", async () => {
      await expect(checkAvailability("-invalid")).rejects.toThrow(
        InvalidNameError
      );
    });

    it("should throw InvalidNameError for name starting with underscore", async () => {
      await expect(checkAvailability("_invalid")).rejects.toThrow(
        InvalidNameError
      );
    });

    it("should throw InvalidNameError for name with spaces", async () => {
      await expect(checkAvailability(" invalid ")).rejects.toThrow(
        InvalidNameError
      );
    });

    it("should throw InvalidNameError for node_modules", async () => {
      await expect(checkAvailability("node_modules")).rejects.toThrow(
        InvalidNameError
      );
    });

    it("should reject non-string input (number)", async () => {
      // @ts-expect-error - Testing invalid input
      await expect(checkAvailability(123)).rejects.toThrow(
        "Package name required"
      );
    });

    it("should reject null input", async () => {
      // @ts-expect-error - Testing invalid input
      await expect(checkAvailability(null)).rejects.toThrow(
        "Package name required"
      );
    });

    it("should throw InvalidNameError for core module names", async () => {
      await expect(checkAvailability("fs")).rejects.toThrow(InvalidNameError);
    });

    it("should throw InvalidNameError for special characters", async () => {
      await expect(checkAvailability("test~package")).rejects.toThrow(
        InvalidNameError
      );
    });

    it("should include errors and warnings in InvalidNameError", async () => {
      try {
        await checkAvailability(".invalid");
        expect.unreachable("Should have thrown");
      } catch (error) {
        expect(error).toBeInstanceOf(InvalidNameError);
        const invalidError = error as InvalidNameError;
        expect(invalidError.errors.length).toBeGreaterThan(0);
      }
    });
  });

  describe("options", () => {
    it("should accept custom registry URL", async () => {
      const result = await checkAvailability("chalk", {
        registryUrl: "https://registry.npmjs.org/",
      });
      expect(result).toBe(false);
    });

    it("should work with registry URL without trailing slash", async () => {
      const result = await checkAvailability("chalk", {
        registryUrl: "https://registry.npmjs.org",
      });
      expect(result).toBe(false);
    });

    it("should return same result with or without trailing slash", async () => {
      const withSlash = await checkAvailability("chalk", {
        registryUrl: "https://registry.npmjs.org/",
      });
      const withoutSlash = await checkAvailability("chalk", {
        registryUrl: "https://registry.npmjs.org",
      });
      expect(withSlash).toBe(withoutSlash);
    });

    it("should respect timeout option", async () => {
      await expect(
        checkAvailability("chalk", { timeout: 1 })
      ).rejects.toThrow();
    });

    it("should work with timeout of 5000ms", async () => {
      const result = await checkAvailability("chalk", { timeout: 5000 });
      expect(result).toBe(false);
    });
  });
});

describe("checkAvailabilityMany", () => {
  describe("batch checking", () => {
    it("should check multiple packages and return a Map", async () => {
      const names = ["chalk", "lodash", "nonexistent-pkg-xyz123abc"];
      const results = await checkAvailabilityMany(names);

      expect(results).toBeInstanceOf(Map);
      expect(results.size).toBe(3);
      expect(results.get("chalk")).toBe(false);
      expect(results.get("lodash")).toBe(false);
      expect(results.get("nonexistent-pkg-xyz123abc")).toBe(true);
    });

    it("should handle empty array", async () => {
      const results = await checkAvailabilityMany([]);
      expect(results).toBeInstanceOf(Map);
      expect(results.size).toBe(0);
    });

    it("should handle single item array", async () => {
      const results = await checkAvailabilityMany(["chalk"]);
      expect(results.size).toBe(1);
      expect(results.get("chalk")).toBe(false);
    });
  });

  describe("concurrency", () => {
    it("should respect concurrency option", async () => {
      const names = ["chalk", "lodash", "express", "react"];
      const results = await checkAvailabilityMany(names, { concurrency: 2 });

      expect(results.size).toBe(4);
    });

    it("should use default concurrency of 4", async () => {
      const names = ["chalk", "lodash"];
      const results = await checkAvailabilityMany(names);

      expect(results.size).toBe(2);
    });

    it("should handle concurrency of 1", async () => {
      const names = ["chalk", "lodash"];
      const results = await checkAvailabilityMany(names, { concurrency: 1 });
      expect(results.size).toBe(2);
    });
  });

  describe("error handling", () => {
    it("should throw TypeError for non-array input", async () => {
      await expect(
        // @ts-expect-error - Testing invalid input
        checkAvailabilityMany("chalk")
      ).rejects.toThrow(TypeError);
    });

    it("should throw AggregateError when checks fail", async () => {
      const names = [".invalid", "-invalid"];

      await expect(checkAvailabilityMany(names)).rejects.toThrow(
        AggregateError
      );
    });

    it("should throw TypeError for null input", async () => {
      // @ts-expect-error - Testing invalid input
      await expect(checkAvailabilityMany(null)).rejects.toThrow(TypeError);
    });

    it("should include all errors in AggregateError", async () => {
      const names = [".invalid", "-invalid", "_invalid"];

      try {
        await checkAvailabilityMany(names);
        expect.unreachable("Should have thrown");
      } catch (error) {
        expect(error).toBeInstanceOf(AggregateError);
        const aggregateError = error as AggregateError;
        expect(aggregateError.errors.length).toBe(3);
      }
    });

    it("should throw AggregateError for mixed batch with valid and invalid names", async () => {
      const names = [
        "chalk",
        ".invalid",
        "nonexistent-pkg-xyz123abc",
        "-also-invalid",
      ];

      try {
        await checkAvailabilityMany(names);
        expect.unreachable("Should have thrown");
      } catch (error) {
        expect(error).toBeInstanceOf(AggregateError);
        const aggregateError = error as AggregateError;
        expect(aggregateError.errors.length).toBe(2);
        for (const err of aggregateError.errors) {
          expect(err).toBeInstanceOf(InvalidNameError);
        }
      }
    });
  });

  describe("options passthrough", () => {
    it("should pass registryUrl to individual checks", async () => {
      const results = await checkAvailabilityMany(["chalk"], {
        registryUrl: "https://registry.npmjs.org/",
      });
      expect(results.get("chalk")).toBe(false);
    });

    it("should pass timeout to individual checks", async () => {
      const results = await checkAvailabilityMany(["chalk"], {
        timeout: 10_000,
      });
      expect(results.get("chalk")).toBe(false);
    });
  });
});
