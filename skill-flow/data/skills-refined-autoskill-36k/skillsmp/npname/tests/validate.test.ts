import { describe, expect, it } from "bun:test";

import {
  isOrganization,
  isScoped,
  isUrlSafe,
  parseName,
  validate,
} from "../src/validate";

describe("validate - valid traditional package names", () => {
  it("should accept valid hyphenated name", () => {
    const result = validate("validate-npm-package-name");
    expect(result.validForNewPackages).toBe(true);
    expect(result.validForOldPackages).toBe(true);
    expect(result.errors).toEqual([]);
    expect(result.warnings).toEqual([]);
  });

  it("should accept simple package name", () => {
    const result = validate("some-package");
    expect(result.validForNewPackages).toBe(true);
    expect(result.validForOldPackages).toBe(true);
  });

  it("should accept domain-like name", () => {
    const result = validate("example.com");
    expect(result.validForNewPackages).toBe(true);
    expect(result.validForOldPackages).toBe(true);
  });

  it("should accept underscore in middle", () => {
    const result = validate("under_score");
    expect(result.validForNewPackages).toBe(true);
    expect(result.validForOldPackages).toBe(true);
  });

  it("should accept period.js style name", () => {
    const result = validate("period.js");
    expect(result.validForNewPackages).toBe(true);
    expect(result.validForOldPackages).toBe(true);
  });

  it("should accept numeric prefix", () => {
    const result = validate("123numeric");
    expect(result.validForNewPackages).toBe(true);
    expect(result.validForOldPackages).toBe(true);
  });
});

describe("validate - scoped package names", () => {
  it("should accept basic scoped package", () => {
    const result = validate("@npm/thingy");
    expect(result.validForNewPackages).toBe(true);
    expect(result.validForOldPackages).toBe(true);
  });

  it("should warn about special characters in scoped package", () => {
    const result = validate("@npm-zors/money!time.js");
    expect(result.validForNewPackages).toBe(false);
    expect(result.validForOldPackages).toBe(true);
    expect(result.warnings).toContain(
      'name can no longer contain special characters ("~\'!()*")'
    );
  });

  it("should allow node_modules as package name in scope", () => {
    const result = validate("@user/node_modules");
    expect(result.validForNewPackages).toBe(true);
    expect(result.validForOldPackages).toBe(true);
  });

  it("should allow package starting with hyphen in scope", () => {
    const result = validate("@user/-package");
    expect(result.validForNewPackages).toBe(true);
    expect(result.validForOldPackages).toBe(true);
  });

  it("should allow package starting with underscore in scope", () => {
    const result = validate("@user/_package");
    expect(result.validForNewPackages).toBe(true);
    expect(result.validForOldPackages).toBe(true);
  });

  it("should allow core module name in scope", () => {
    const result = validate("@user/http");
    expect(result.validForNewPackages).toBe(true);
    expect(result.validForOldPackages).toBe(true);
  });
});

describe("validate - invalid names (type errors)", () => {
  it("should reject null", () => {
    const result = validate(null);
    expect(result.validForNewPackages).toBe(false);
    expect(result.validForOldPackages).toBe(false);
    expect(result.errors).toContain("name cannot be null");
  });

  it("should reject undefined", () => {
    const result = validate();
    expect(result.validForNewPackages).toBe(false);
    expect(result.validForOldPackages).toBe(false);
    expect(result.errors).toContain("name cannot be undefined");
  });

  it("should reject number", () => {
    const result = validate(42);
    expect(result.validForNewPackages).toBe(false);
    expect(result.validForOldPackages).toBe(false);
    expect(result.errors).toContain("name must be a string");
  });
});

describe("validate - invalid names (format)", () => {
  it("should reject empty string", () => {
    const result = validate("");
    expect(result.validForNewPackages).toBe(false);
    expect(result.validForOldPackages).toBe(false);
    expect(result.errors).toContain("name length must be greater than zero");
  });

  it("should reject name starting with period", () => {
    const result = validate(".start-with-period");
    expect(result.validForNewPackages).toBe(false);
    expect(result.validForOldPackages).toBe(false);
    expect(result.errors).toContain("name cannot start with a period");
  });

  it("should reject name starting with underscore", () => {
    const result = validate("_start-with-underscore");
    expect(result.validForNewPackages).toBe(false);
    expect(result.validForOldPackages).toBe(false);
    expect(result.errors).toContain("name cannot start with an underscore");
  });

  it("should reject name starting with hyphen", () => {
    const result = validate("-start-with-hyphen");
    expect(result.validForNewPackages).toBe(false);
    expect(result.validForOldPackages).toBe(false);
    expect(result.errors).toContain("name cannot start with a hyphen");
  });

  it("should reject name with leading space", () => {
    const result = validate(" leading-space");
    expect(result.validForNewPackages).toBe(false);
    expect(result.validForOldPackages).toBe(false);
    expect(result.errors).toContain(
      "name cannot contain leading or trailing spaces"
    );
  });

  it("should reject name with trailing space", () => {
    const result = validate("trailing-space ");
    expect(result.validForNewPackages).toBe(false);
    expect(result.validForOldPackages).toBe(false);
    expect(result.errors).toContain(
      "name cannot contain leading or trailing spaces"
    );
  });
});

describe("validate - invalid names (URL unsafe)", () => {
  it("should reject name with colons", () => {
    const result = validate("contain:colons");
    expect(result.validForNewPackages).toBe(false);
    expect(result.validForOldPackages).toBe(false);
    expect(result.errors).toContain(
      "name can only contain URL-friendly characters"
    );
  });

  it("should reject name with multiple slashes", () => {
    const result = validate("s/l/a/s/h/e/s");
    expect(result.validForNewPackages).toBe(false);
    expect(result.validForOldPackages).toBe(false);
    expect(result.errors).toContain(
      "name can only contain URL-friendly characters"
    );
  });
});

describe("validate - invalid names (blocked)", () => {
  it("should reject node_modules", () => {
    const result = validate("node_modules");
    expect(result.validForNewPackages).toBe(false);
    expect(result.validForOldPackages).toBe(false);
    expect(result.errors).toContain("node_modules is not a valid package name");
  });

  it("should reject favicon.ico", () => {
    const result = validate("favicon.ico");
    expect(result.validForNewPackages).toBe(false);
    expect(result.validForOldPackages).toBe(false);
    expect(result.errors).toContain("favicon.ico is not a valid package name");
  });
});

describe("validate - scoped package edge cases", () => {
  it("should reject scoped package starting with period", () => {
    const result = validate("@npm/.");
    expect(result.validForNewPackages).toBe(false);
    expect(result.validForOldPackages).toBe(false);
    expect(result.errors).toContain("name cannot start with a period");
  });

  it("should reject scoped package with .. name", () => {
    const result = validate("@npm/..");
    expect(result.validForNewPackages).toBe(false);
    expect(result.validForOldPackages).toBe(false);
    expect(result.errors).toContain("name cannot start with a period");
  });

  it("should reject scoped package with .package name", () => {
    const result = validate("@npm/.package");
    expect(result.validForNewPackages).toBe(false);
    expect(result.validForOldPackages).toBe(false);
    expect(result.errors).toContain("name cannot start with a period");
  });
});

describe("validate - warnings", () => {
  it("should warn about http module name", () => {
    const result = validate("http");
    expect(result.validForNewPackages).toBe(false);
    expect(result.validForOldPackages).toBe(true);
    expect(result.warnings).toContain("http is a core module name");
  });

  it("should warn about names longer than 214 characters", () => {
    const longName =
      "ifyouwanttogetthesumoftwonumberswherethosetwonumbersarechosenbyfindingthelargestoftwooutofthreenumbersandsquaringthemwhichismultiplyingthembyitselfthenyoushouldinputthreenumbersintothisfunctionanditwilldothatforyou-";
    const result = validate(longName);
    expect(result.validForNewPackages).toBe(false);
    expect(result.validForOldPackages).toBe(true);
    expect(result.warnings).toContain(
      "name can no longer contain more than 214 characters"
    );
  });

  it("should accept 214 character name", () => {
    const maxName =
      "ifyouwanttogetthesumoftwonumberswherethosetwonumbersarechosenbyfindingthelargestoftwooutofthreenumbersandsquaringthemwhichismultiplyingthembyitselfthenyoushouldinputthreenumbersintothisfunctionanditwilldothatforyou";
    const result = validate(maxName);
    expect(result.validForNewPackages).toBe(true);
    expect(result.validForOldPackages).toBe(true);
  });

  it("should warn about capital letters", () => {
    const result = validate("CAPITAL-LETTERS");
    expect(result.validForNewPackages).toBe(false);
    expect(result.validForOldPackages).toBe(true);
    expect(result.warnings).toContain(
      "name can no longer contain capital letters"
    );
  });

  it("should warn about exclamation mark", () => {
    const result = validate("crazy!");
    expect(result.validForNewPackages).toBe(false);
    expect(result.validForOldPackages).toBe(true);
    expect(result.warnings).toContain(
      'name can no longer contain special characters ("~\'!()*")'
    );
  });
});

describe("validate - suggestions", () => {
  it("should suggest lowercase version for uppercase names", () => {
    const result = validate("CAPITAL-LETTERS");
    expect(result.suggestions).toBeDefined();
    expect(result.suggestions).toContain("capital-letters");
  });

  it("should suggest URL-safe version for unsafe names", () => {
    const result = validate("has spaces");
    expect(result.suggestions).toBeDefined();
    expect(result.suggestions?.length).toBeGreaterThan(0);
  });
});

describe("validate - valid property", () => {
  it("should set valid to true when no errors and no warnings", () => {
    const result = validate("valid-package");
    expect(result.valid).toBe(true);
  });

  it("should set valid to false when there are warnings", () => {
    const result = validate("http");
    expect(result.valid).toBe(false);
    expect(result.validForOldPackages).toBe(true);
  });

  it("should set valid to false when there are errors", () => {
    const result = validate("");
    expect(result.valid).toBe(false);
  });
});

describe("parseName", () => {
  it("should parse unscoped package name", () => {
    const result = parseName("my-package");
    expect(result.scope).toBe(null);
    expect(result.name).toBe("my-package");
    expect(result.full).toBe("my-package");
    expect(result.isScoped).toBe(false);
  });

  it("should parse scoped package name", () => {
    const result = parseName("@scope/package");
    expect(result.scope).toBe("scope");
    expect(result.name).toBe("package");
    expect(result.full).toBe("@scope/package");
    expect(result.isScoped).toBe(true);
  });

  it("should parse scoped package with hyphenated scope", () => {
    const result = parseName("@my-org/my-package");
    expect(result.scope).toBe("my-org");
    expect(result.name).toBe("my-package");
    expect(result.full).toBe("@my-org/my-package");
    expect(result.isScoped).toBe(true);
  });
});

describe("isUrlSafe", () => {
  it("should return true for simple alphanumeric strings", () => {
    expect(isUrlSafe("mypackage")).toBe(true);
    expect(isUrlSafe("my-package")).toBe(true);
    expect(isUrlSafe("my_package")).toBe(true);
    expect(isUrlSafe("my.package")).toBe(true);
  });

  it("should return false for strings with spaces", () => {
    expect(isUrlSafe("my package")).toBe(false);
    expect(isUrlSafe(" leading")).toBe(false);
    expect(isUrlSafe("trailing ")).toBe(false);
  });

  it("should return false for strings with special characters", () => {
    expect(isUrlSafe("package@scope")).toBe(false);
    expect(isUrlSafe("package/name")).toBe(false);
    expect(isUrlSafe("package:name")).toBe(false);
  });
});

describe("node builtins validation", () => {
  it.each([
    "assert",
    "buffer",
    "child_process",
    "crypto",
    "dns",
    "events",
    "fs",
    "http",
    "https",
    "net",
    "os",
    "path",
    "process",
    "stream",
    "url",
    "util",
    "zlib",
  ])("should warn that %s is a core module name", (builtin) => {
    const result = validate(builtin);
    expect(result.validForNewPackages).toBe(false);
    expect(result.validForOldPackages).toBe(true);
    expect(result.warnings).toContain(`${builtin} is a core module name`);
  });
});

describe("validate - additional special characters", () => {
  it("should warn about tilde character", () => {
    const result = validate("~tilde");
    expect(result.validForNewPackages).toBe(false);
    expect(result.validForOldPackages).toBe(true);
    expect(result.warnings).toContain(
      'name can no longer contain special characters ("~\'!()*")'
    );
  });

  it("should warn about apostrophe", () => {
    const result = validate("it's");
    expect(result.validForNewPackages).toBe(false);
    expect(result.validForOldPackages).toBe(true);
    expect(result.warnings).toContain(
      'name can no longer contain special characters ("~\'!()*")'
    );
  });

  it("should warn about parentheses", () => {
    const result = validate("func()");
    expect(result.validForNewPackages).toBe(false);
    expect(result.validForOldPackages).toBe(true);
    expect(result.warnings).toContain(
      'name can no longer contain special characters ("~\'!()*")'
    );
  });

  it("should warn about asterisk", () => {
    const result = validate("star*");
    expect(result.validForNewPackages).toBe(false);
    expect(result.validForOldPackages).toBe(true);
    expect(result.warnings).toContain(
      'name can no longer contain special characters ("~\'!()*")'
    );
  });

  it("should warn about mixed special characters", () => {
    const result = validate("~'!()*");
    expect(result.validForNewPackages).toBe(false);
    expect(result.validForOldPackages).toBe(true);
    expect(result.warnings).toContain(
      'name can no longer contain special characters ("~\'!()*")'
    );
  });
});

describe("validate - double hyphen start", () => {
  it("should reject name starting with double hyphen", () => {
    const result = validate("--double-hyphen");
    expect(result.validForNewPackages).toBe(false);
    expect(result.validForOldPackages).toBe(false);
    expect(result.errors).toContain("name cannot start with a hyphen");
  });
});

describe("validate - scoped package format edge cases", () => {
  it("should reject empty scope", () => {
    const result = validate("@/empty-scope");
    expect(result.validForNewPackages).toBe(false);
    expect(result.validForOldPackages).toBe(false);
    expect(result.errors).toContain(
      "name can only contain URL-friendly characters"
    );
  });

  it("should reject double @ symbol", () => {
    const result = validate("@@double-at");
    expect(result.validForNewPackages).toBe(false);
    expect(result.validForOldPackages).toBe(false);
    expect(result.errors).toContain(
      "name can only contain URL-friendly characters"
    );
  });

  it("should reject @ not at start", () => {
    const result = validate("foo@bar");
    expect(result.validForNewPackages).toBe(false);
    expect(result.validForOldPackages).toBe(false);
    expect(result.errors).toContain(
      "name can only contain URL-friendly characters"
    );
  });

  it("should reject extra @ in scoped package", () => {
    const result = validate("@foo@bar");
    expect(result.validForNewPackages).toBe(false);
    expect(result.validForOldPackages).toBe(false);
    expect(result.errors).toContain(
      "name can only contain URL-friendly characters"
    );
  });

  it("should reject scope without slash", () => {
    const result = validate("@foo");
    expect(result.validForNewPackages).toBe(false);
    expect(result.validForOldPackages).toBe(false);
    expect(result.errors).toContain(
      "name can only contain URL-friendly characters"
    );
  });

  it("should reject extra trailing slash", () => {
    const result = validate("@foo/bar/");
    expect(result.validForNewPackages).toBe(false);
    expect(result.validForOldPackages).toBe(false);
    expect(result.errors).toContain(
      "name can only contain URL-friendly characters"
    );
  });
});

describe("validate - additional type checks", () => {
  it("should reject boolean true", () => {
    const result = validate(true);
    expect(result.validForNewPackages).toBe(false);
    expect(result.validForOldPackages).toBe(false);
    expect(result.errors).toContain("name must be a string");
  });

  it("should reject boolean false", () => {
    const result = validate(false);
    expect(result.validForNewPackages).toBe(false);
    expect(result.validForOldPackages).toBe(false);
    expect(result.errors).toContain("name must be a string");
  });

  it("should reject array input", () => {
    const result = validate([]);
    expect(result.validForNewPackages).toBe(false);
    expect(result.validForOldPackages).toBe(false);
    expect(result.errors).toContain("name must be a string");
  });

  it("should reject object input", () => {
    const result = validate({});
    expect(result.validForNewPackages).toBe(false);
    expect(result.validForOldPackages).toBe(false);
    expect(result.errors).toContain("name must be a string");
  });
});

describe("isScoped helper", () => {
  it("should return true for scoped package", () => {
    expect(isScoped("@scope/pkg")).toBe(true);
  });

  it("should return false for unscoped package", () => {
    expect(isScoped("pkg")).toBe(false);
  });
});

describe("isOrganization helper", () => {
  it("should return true for organization without trailing slash", () => {
    expect(isOrganization("@org")).toBe(true);
  });

  it("should return false for organization with trailing slash", () => {
    expect(isOrganization("@org/")).toBe(false);
  });

  it("should return false for scoped package", () => {
    expect(isOrganization("@org/pkg")).toBe(false);
  });

  it("should return false for unscoped package", () => {
    expect(isOrganization("pkg")).toBe(false);
  });
});

describe("validate - unicode and international characters", () => {
  it("should reject unicode characters", () => {
    const result = validate("café");
    expect(result.validForNewPackages).toBe(false);
  });

  it("should reject emoji", () => {
    const result = validate("pkg-😀");
    expect(result.validForNewPackages).toBe(false);
  });
});

describe("validate - whitespace variations", () => {
  it("should reject tabs in name", () => {
    const result = validate("pkg\tname");
    expect(result.validForNewPackages).toBe(false);
  });

  it("should reject newlines in name", () => {
    const result = validate("pkg\nname");
    expect(result.validForNewPackages).toBe(false);
  });
});

describe("validate - blocked names case insensitivity", () => {
  it("should reject NODE_MODULES uppercase", () => {
    const result = validate("NODE_MODULES");
    expect(result.errors).toContain("node_modules is not a valid package name");
  });

  it("should reject FAVICON.ICO uppercase", () => {
    const result = validate("FAVICON.ICO");
    expect(result.errors).toContain("favicon.ico is not a valid package name");
  });
});

describe("validate - multiple errors/warnings accumulation", () => {
  it("should accumulate multiple warnings", () => {
    const result = validate("HTTP!");
    expect(result.warnings.length).toBeGreaterThan(1);
  });
});

describe("parseName - edge cases", () => {
  it("should handle empty string in parseName", () => {
    const result = parseName("");
    expect(result.name).toBe("");
    expect(result.isScoped).toBe(false);
  });
});
