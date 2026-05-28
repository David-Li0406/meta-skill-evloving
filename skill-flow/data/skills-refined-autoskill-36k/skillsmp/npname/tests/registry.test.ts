import { afterEach, beforeEach, describe, expect, it } from "bun:test";

import {
  DEFAULT_REGISTRY,
  expandEnvVars,
  getAuthToken,
  getRegistryUrl,
  parseNpmrc,
} from "../src/registry";

describe("registry", () => {
  describe("parseNpmrc", () => {
    it("should parse key=value pairs", () => {
      const content = `
registry=https://registry.example.com/
@scope:registry=https://scope.example.com/
`;
      const result = parseNpmrc(content);
      expect(result.registry).toBe("https://registry.example.com/");
      expect(result["@scope:registry"]).toBe("https://scope.example.com/");
    });

    it("should handle comments with #", () => {
      const content = `
# This is a comment
registry=https://registry.example.com/
# Another comment
`;
      const result = parseNpmrc(content);
      expect(result.registry).toBe("https://registry.example.com/");
      expect(Object.keys(result)).toHaveLength(1);
    });

    it("should handle comments with ;", () => {
      const content = `
; This is a semicolon comment
registry=https://registry.example.com/
; Another comment
`;
      const result = parseNpmrc(content);
      expect(result.registry).toBe("https://registry.example.com/");
      expect(Object.keys(result)).toHaveLength(1);
    });

    it("should handle empty lines", () => {
      const content = `

registry=https://registry.example.com/

@scope:registry=https://scope.example.com/

`;
      const result = parseNpmrc(content);
      expect(Object.keys(result)).toHaveLength(2);
    });

    it("should trim whitespace", () => {
      const content = `  registry  =  https://registry.example.com/  `;
      const result = parseNpmrc(content);
      expect(result.registry).toBe("https://registry.example.com/");
    });

    it("should handle auth tokens", () => {
      const content = `
//registry.example.com/:_authToken=my-secret-token
//registry.example.com/:username=myuser
//registry.example.com/:_password=bXlwYXNz
`;
      const result = parseNpmrc(content);
      expect(result["//registry.example.com/:_authToken"]).toBe(
        "my-secret-token"
      );
      expect(result["//registry.example.com/:username"]).toBe("myuser");
      expect(result["//registry.example.com/:_password"]).toBe("bXlwYXNz");
    });

    it("should handle legacy _auth token", () => {
      const content = `_auth=dXNlcm5hbWU6cGFzc3dvcmQ=`;
      const result = parseNpmrc(content);
      expect(result._auth).toBe("dXNlcm5hbWU6cGFzc3dvcmQ=");
    });

    it("should handle values containing equals signs", () => {
      const content = `//registry.example.com/:_authToken=abc=def==`;
      const result = parseNpmrc(content);
      expect(result["//registry.example.com/:_authToken"]).toBe("abc=def==");
    });

    it("should parse registry URL with port", () => {
      const content = `//localhost:8770/:_authToken=token123`;
      const result = parseNpmrc(content);
      expect(result["//localhost:8770/:_authToken"]).toBe("token123");
    });

    it("should parse both bearer and basic auth for same registry", () => {
      const content = `
//registry.example.com/:_authToken=bearer-token
//registry.example.com/:username=myuser
//registry.example.com/:_password=bXlwYXNzd29yZA==
`;
      const result = parseNpmrc(content);
      expect(result["//registry.example.com/:_authToken"]).toBe("bearer-token");
      expect(result["//registry.example.com/:username"]).toBe("myuser");
      expect(result["//registry.example.com/:_password"]).toBe(
        "bXlwYXNzd29yZA=="
      );
    });

    it("should parse Azure DevOps style nested registry paths", () => {
      const content = `//contoso.pkgs.visualstudio.com/_packaging/MyFeed/npm/registry/:_authToken=azure-token`;
      const result = parseNpmrc(content);
      expect(
        result[
          "//contoso.pkgs.visualstudio.com/_packaging/MyFeed/npm/registry/:_authToken"
        ]
      ).toBe("azure-token");
    });

    it("should parse legacy _auth with base64 username:password", () => {
      // base64 of "username:password" is "dXNlcm5hbWU6cGFzc3dvcmQ="
      const content = `_auth=dXNlcm5hbWU6cGFzc3dvcmQ=`;
      const result = parseNpmrc(content);
      expect(result._auth).toBe("dXNlcm5hbWU6cGFzc3dvcmQ=");
      // Verify decoding works
      const decoded = Buffer.from(result._auth, "base64").toString("utf8");
      expect(decoded).toBe("username:password");
    });

    it("should parse scoped registry URL", () => {
      const content = `@myco:registry=https://custom.registry.com/`;
      const result = parseNpmrc(content);
      expect(result["@myco:registry"]).toBe("https://custom.registry.com/");
    });
  });

  describe("expandEnvVars", () => {
    const originalEnv = process.env;

    beforeEach(() => {
      process.env = { ...originalEnv };
      process.env.TEST_VAR = "test-value";
      process.env.ANOTHER_VAR = "another-value";
      process.env.NPM_TOKEN = "secret-token";
    });

    afterEach(() => {
      process.env = originalEnv;
    });

    it("should expand braces pattern", () => {
      // eslint-disable-next-line no-template-curly-in-string
      const input = "${TEST_VAR}";
      const result = expandEnvVars(input);
      expect(result).toBe("test-value");
    });

    it("should expand dollar pattern", () => {
      const result = expandEnvVars("$TEST_VAR");
      expect(result).toBe("test-value");
    });

    it("should expand multiple variables", () => {
      // eslint-disable-next-line no-template-curly-in-string
      const input = "${TEST_VAR}-$ANOTHER_VAR";
      const result = expandEnvVars(input);
      expect(result).toBe("test-value-another-value");
    });

    it("should return empty string for undefined variables", () => {
      // eslint-disable-next-line no-template-curly-in-string
      const input = "${UNDEFINED_VAR}";
      const result = expandEnvVars(input);
      expect(result).toBe("");
    });

    it("should handle mixed content", () => {
      // eslint-disable-next-line no-template-curly-in-string
      const input = "prefix-${NPM_TOKEN}-suffix";
      const result = expandEnvVars(input);
      expect(result).toBe("prefix-secret-token-suffix");
    });

    it("should not expand when no env vars", () => {
      const result = expandEnvVars("plain-text");
      expect(result).toBe("plain-text");
    });

    it("should expand env var with braces in authToken context", () => {
      // eslint-disable-next-line no-template-curly-in-string
      const input = "${NPM_TOKEN}";
      const result = expandEnvVars(input);
      expect(result).toBe("secret-token");
    });

    it("should expand env var without braces in authToken context", () => {
      const input = "$NPM_TOKEN";
      const result = expandEnvVars(input);
      expect(result).toBe("secret-token");
    });
  });

  describe("getRegistryUrl", () => {
    const originalEnv = process.env;

    beforeEach(() => {
      process.env = { ...originalEnv };
      delete process.env.npm_config_registry;
      delete process.env.NPM_CONFIG_REGISTRY;
    });

    afterEach(() => {
      process.env = originalEnv;
    });

    it("should return default registry when no config", () => {
      const result = getRegistryUrl();
      expect(result).toBe(DEFAULT_REGISTRY);
    });

    it("should return lowercase env var over uppercase", () => {
      process.env.npm_config_registry = "https://lowercase.example.com";
      process.env.NPM_CONFIG_REGISTRY = "https://uppercase.example.com";
      const result = getRegistryUrl();
      expect(result).toBe("https://lowercase.example.com/");
    });

    it("should return uppercase env var when lowercase not set", () => {
      process.env.NPM_CONFIG_REGISTRY = "https://uppercase.example.com";
      const result = getRegistryUrl();
      expect(result).toBe("https://uppercase.example.com/");
    });

    it("should normalize URL to have trailing slash", () => {
      process.env.npm_config_registry = "https://registry.example.com";
      const result = getRegistryUrl();
      expect(result).toBe("https://registry.example.com/");
    });

    it("should not double-add trailing slash", () => {
      process.env.npm_config_registry = "https://registry.example.com/";
      const result = getRegistryUrl();
      expect(result).toBe("https://registry.example.com/");
    });

    it("should normalize URL without trailing slash", () => {
      process.env.npm_config_registry = "https://no-trailing-slash.example.com";
      const result = getRegistryUrl();
      expect(result).toBe("https://no-trailing-slash.example.com/");
      expect(result).not.toBe("https://no-trailing-slash.example.com//");
    });

    it("should not create double trailing slash when URL already has one", () => {
      process.env.npm_config_registry =
        "https://already-has-trailing-slash.example.com/";
      const result = getRegistryUrl();
      expect(result).toBe("https://already-has-trailing-slash.example.com/");
      expect(result.endsWith("//")).toBe(false);
    });
  });

  describe("getAuthToken", () => {
    it("should not throw for valid registry URL", () => {
      // The test verifies the function executes without throwing
      // Result depends on system .npmrc configuration
      expect(() => getAuthToken("https://registry.npmjs.org/")).not.toThrow();
    });

    it("should return correct type", () => {
      const result = getAuthToken("https://registry.npmjs.org/");
      // Result is either undefined or an object with token and type
      const resultType = typeof result;
      expect(["undefined", "object"]).toContain(resultType);
    });

    it("should handle registry URL with port", () => {
      // This test verifies the function doesn't throw for port-specific URLs
      expect(() => getAuthToken("http://localhost:8770/")).not.toThrow();
    });
  });

  describe("parseNpmrc with environment variable expansion", () => {
    const originalEnv = process.env;

    beforeEach(() => {
      process.env = { ...originalEnv };
      process.env.NPM_TOKEN = "env-token-value";
    });

    afterEach(() => {
      process.env = originalEnv;
    });

    it("should expand env var with braces syntax in _authToken value", () => {
      // eslint-disable-next-line no-template-curly-in-string
      const content = `//registry.example.com/:_authToken=\${NPM_TOKEN}`;
      const result = parseNpmrc(content);
      expect(result["//registry.example.com/:_authToken"]).toBe(
        "env-token-value"
      );
    });

    it("should expand $NPM_TOKEN (without braces) in _authToken value", () => {
      const content = `//registry.example.com/:_authToken=$NPM_TOKEN`;
      const result = parseNpmrc(content);
      expect(result["//registry.example.com/:_authToken"]).toBe(
        "env-token-value"
      );
    });

    it("should handle undefined environment variable in _authToken", () => {
      // eslint-disable-next-line no-template-curly-in-string
      const content = `//registry.example.com/:_authToken=\${UNDEFINED_TOKEN}`;
      const result = parseNpmrc(content);
      expect(result["//registry.example.com/:_authToken"]).toBe("");
    });
  });

  describe("DEFAULT_REGISTRY", () => {
    it("should be the npm registry", () => {
      expect(DEFAULT_REGISTRY).toBe("https://registry.npmjs.org/");
    });
  });
});
