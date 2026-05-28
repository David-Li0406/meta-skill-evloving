import { describe, expect, it } from "bun:test";

import npname, {
  checkAvailability,
  checkAvailabilityMany,
  DEFAULT_REGISTRY,
  getAuthToken,
  getRegistryUrl,
  InvalidNameError,
  parseName,
  parseNpmrc,
  validate,
  type AuthInfo,
  type CheckResult,
  type ParsedName,
  type ValidationResult,
} from "../src";

describe("npname default export", () => {
  it("should be a callable function", () => {
    expect(typeof npname).toBe("function");
  });

  it("should have all expected methods attached", () => {
    expect(typeof npname.many).toBe("function");
    // eslint-disable-next-line import/no-named-as-default-member
    expect(typeof npname.validate).toBe("function");
    expect(typeof npname.check).toBe("function");
    expect(typeof npname.parse).toBe("function");
    expect(typeof npname.registry).toBe("function");
    expect(typeof npname.auth).toBe("function");
  });
});

describe("validate() named export", () => {
  it("should return ValidationResult for valid package name", () => {
    const result = validate("my-package");

    expect(result).toHaveProperty("valid");
    expect(result).toHaveProperty("validForNewPackages");
    expect(result).toHaveProperty("validForOldPackages");
    expect(result).toHaveProperty("errors");
    expect(result).toHaveProperty("warnings");
    expect(Array.isArray(result.errors)).toBe(true);
    expect(Array.isArray(result.warnings)).toBe(true);
  });

  it("should return valid result for a good package name", () => {
    const result = validate("valid-package-name");

    expect(result.valid).toBe(true);
    expect(result.validForNewPackages).toBe(true);
    expect(result.errors).toHaveLength(0);
  });

  it("should return invalid result for empty string", () => {
    const result = validate("");

    expect(result.valid).toBe(false);
    expect(result.validForNewPackages).toBe(false);
    expect(result.errors.length).toBeGreaterThan(0);
  });

  it("should return invalid result for non-string input", () => {
    const result = validate(123);

    expect(result.valid).toBe(false);
    expect(result.validForNewPackages).toBe(false);
  });

  it("should return invalid result for name with uppercase letters", () => {
    const result = validate("MyPackage");

    expect(result.validForNewPackages).toBe(false);
  });

  it("should handle scoped package names", () => {
    const result = validate("@scope/package-name");

    expect(result).toHaveProperty("valid");
    expect(result).toHaveProperty("validForNewPackages");
  });

  it("should return invalid result for null input", () => {
    const result = validate(null);

    expect(result.valid).toBe(false);
    expect(result.errors.length).toBeGreaterThan(0);
  });

  it("should return invalid result for undefined input", () => {
    const result = validate();

    expect(result.valid).toBe(false);
  });
});

describe("parseName() named export", () => {
  it("should parse unscoped package name", () => {
    const result = parseName("my-package");

    expect(result).toHaveProperty("scope");
    expect(result).toHaveProperty("name");
    expect(result).toHaveProperty("full");
    expect(result).toHaveProperty("isScoped");

    expect(result.scope).toBeNull();
    expect(result.name).toBe("my-package");
    expect(result.full).toBe("my-package");
    expect(result.isScoped).toBe(false);
  });

  it("should parse scoped package name", () => {
    const result = parseName("@scope/name");

    expect(result.scope).toBe("scope");
    expect(result.name).toBe("name");
    expect(result.full).toBe("@scope/name");
    expect(result.isScoped).toBe(true);
  });

  it("should handle organization-style scopes", () => {
    const result = parseName("@myorg/my-package");

    expect(result.scope).toBe("myorg");
    expect(result.name).toBe("my-package");
    expect(result.isScoped).toBe(true);
  });
});

describe("getRegistryUrl() named export", () => {
  it("should return default registry when no scope provided", () => {
    const url = getRegistryUrl();

    expect(typeof url).toBe("string");
    expect(url).toContain("registry");
  });

  it("should return registry URL for scoped packages", () => {
    const url = getRegistryUrl("@myorg");

    expect(typeof url).toBe("string");
  });

  it("should handle scope without @ prefix", () => {
    const url = getRegistryUrl("myorg");

    expect(typeof url).toBe("string");
  });
});

describe("getAuthToken() named export", () => {
  it("should return undefined or AuthInfo for default registry", () => {
    const auth = getAuthToken("https://registry.npmjs.org/");

    // Auth can be undefined (no .npmrc) or an object (has .npmrc)
    expect([undefined, "object"]).toContain(typeof auth);
  });

  it("should handle DEFAULT_REGISTRY constant", () => {
    const auth = getAuthToken(DEFAULT_REGISTRY);

    // Result depends on user's .npmrc configuration - just check it doesn't throw
    expect(auth).toBeDefined();
  });
});

describe("npname() availability check", () => {
  it("should return a promise", () => {
    const result = npname("some-test-package");

    expect(result).toBeInstanceOf(Promise);
  });

  it("should resolve to a boolean", async () => {
    const result = await npname("xyzzy-test-pkg-12345-nonexistent");

    expect(typeof result).toBe("boolean");
  });
});

describe("npname.many()", () => {
  it("should return a promise", () => {
    const result = npname.many(["pkg1", "pkg2"]);

    expect(result).toBeInstanceOf(Promise);
  });

  it("should resolve to a Map", async () => {
    const result = await npname.many(["xyzzy-test-pkg-a", "xyzzy-test-pkg-b"]);

    expect(result).toBeInstanceOf(Map);
  });

  it("should have entries for each input name", async () => {
    const names = ["test-pkg-one", "test-pkg-two"];
    const result = await npname.many(names);

    for (const name of names) {
      expect(result.has(name)).toBe(true);
      expect(typeof result.get(name)).toBe("boolean");
    }
  });
});

describe("npname.check()", () => {
  it("should return a CheckResult for valid name", async () => {
    const result = await npname.check("valid-package-test");

    expect(result).toHaveProperty("name");
    expect(result).toHaveProperty("available");
    expect(result).toHaveProperty("validation");
    expect(result.name).toBe("valid-package-test");
  });

  it("should include validation in the result", async () => {
    const result = await npname.check("my-test-package");

    expect(result.validation).toHaveProperty("valid");
    expect(result.validation).toHaveProperty("validForNewPackages");
    expect(result.validation).toHaveProperty("errors");
    expect(result.validation).toHaveProperty("warnings");
  });

  it("should return error for invalid package name", async () => {
    const result = await npname.check("");

    expect(result.available).toBeNull();
    expect(result.error).toBeInstanceOf(InvalidNameError);
    expect(result.validation.validForNewPackages).toBe(false);
  });

  it("should return InvalidNameError with errors and warnings for invalid name", async () => {
    const result = await npname.check("INVALID-UPPERCASE");

    expect(result.error).toBeInstanceOf(InvalidNameError);
    const error = result.error as InstanceType<typeof InvalidNameError>;
    expect(error.errors).toBeDefined();
    expect(error.warnings).toBeDefined();
    expect(Array.isArray(error.errors)).toBe(true);
    expect(Array.isArray(error.warnings)).toBe(true);
  });
});

describe("Named exports", () => {
  it("should export validate function", () => {
    expect(typeof validate).toBe("function");
  });

  it("should export parseName function", () => {
    expect(typeof parseName).toBe("function");
  });

  it("should export checkAvailability function", () => {
    expect(typeof checkAvailability).toBe("function");
  });

  it("should export checkAvailabilityMany function", () => {
    expect(typeof checkAvailabilityMany).toBe("function");
  });

  it("should export getRegistryUrl function", () => {
    expect(typeof getRegistryUrl).toBe("function");
  });

  it("should export getAuthToken function", () => {
    expect(typeof getAuthToken).toBe("function");
  });

  it("should export parseNpmrc function", () => {
    expect(typeof parseNpmrc).toBe("function");
  });

  it("should export DEFAULT_REGISTRY constant", () => {
    expect(typeof DEFAULT_REGISTRY).toBe("string");
    expect(DEFAULT_REGISTRY).toContain("registry");
  });

  it("should export InvalidNameError class", () => {
    expect(typeof InvalidNameError).toBe("function");
    expect(new InvalidNameError("test", [], [])).toBeInstanceOf(Error);
  });
});

describe("InvalidNameError", () => {
  it("should be an Error subclass", () => {
    const error = new InvalidNameError(
      "test message",
      ["error1"],
      ["warning1"]
    );

    expect(error).toBeInstanceOf(Error);
    expect(error.message).toBe("test message");
  });

  it("should have name property set to InvalidNameError", () => {
    const error = new InvalidNameError("test", [], []);

    expect(error.name).toBe("InvalidNameError");
  });

  it("should store errors and warnings", () => {
    const errors = ["error1", "error2"];
    const warnings = ["warning1"];
    const error = new InvalidNameError("test", errors, warnings);

    expect(error.errors).toEqual(errors);
    expect(error.warnings).toEqual(warnings);
  });
});

describe("Type exports", () => {
  it("should allow typed usage of ValidationResult", () => {
    const result: ValidationResult = {
      errors: [],
      valid: true,
      validForNewPackages: true,
      validForOldPackages: true,
      warnings: [],
    };

    expect(result.valid).toBe(true);
  });

  it("should allow typed usage of CheckResult", () => {
    const result: CheckResult = {
      available: true,
      name: "test",
      validation: {
        errors: [],
        valid: true,
        validForNewPackages: true,
        validForOldPackages: true,
        warnings: [],
      },
    };

    expect(result.name).toBe("test");
  });

  it("should allow typed usage of ParsedName", () => {
    const parsed: ParsedName = {
      full: "@myorg/package",
      isOrganization: true,
      isScoped: true,
      name: "package",
      scope: "myorg",
    };

    expect(parsed.isScoped).toBe(true);
  });

  it("should allow typed usage of AuthInfo", () => {
    const auth: AuthInfo = {
      token: "abc123",
      type: "Bearer",
    };

    expect(auth.type).toBe("Bearer");
  });
});

describe("Integration scenarios", () => {
  it("should validate then check availability", async () => {
    const name = "my-test-package";

    const validation = validate(name);
    expect(validation.validForNewPackages).toBe(true);

    const available = await npname(name);
    expect(typeof available).toBe("boolean");
  });

  it("should parse and get registry for scoped package", () => {
    const name = "@myorg/my-package";
    const parsed = parseName(name);
    const registry = getRegistryUrl(`@${parsed.scope}`);

    expect(parsed.isScoped).toBe(true);
    expect(typeof registry).toBe("string");
  });

  it("should handle complete workflow with check()", async () => {
    const result = await npname.check("complete-workflow-test");

    expect(result.validation).toBeDefined();
    // available is either boolean (success) or null (error)
    expect([true, false, null]).toContain(result.available);
  });

  it("should batch check multiple packages", async () => {
    const names = ["batch-test-1", "batch-test-2", "batch-test-3"];
    const results = await npname.many(names);

    expect(results.size).toBe(names.length);
    for (const name of names) {
      expect(results.has(name)).toBe(true);
    }
  });
});

describe("Error handling", () => {
  it("should handle network errors gracefully in check()", async () => {
    const result = await npname.check("test-error-handling");

    expect(result).toHaveProperty("name");
    expect(result).toHaveProperty("validation");
  });
});
