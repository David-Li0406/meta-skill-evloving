# NPM Workspace Setup Templates

This directory contains ready-to-use configuration templates for setting up npm workspaces.

## Template Files

| File                          | Description                      | Placeholders                                                                                 |
| ----------------------------- | -------------------------------- | -------------------------------------------------------------------------------------------- |
| `root-package.json`           | Root workspace package.json      | `{{SCOPE}}`, `{{REPO_NAME}}`, `{{DESCRIPTION}}`, `{{ORG}}`, `{{PACKAGE_1}}`, `{{PACKAGE_2}}`, `{{EXAMPLE_1}}` |
| `package-package.json`        | Workspace package package.json   | `{{SCOPE}}`, `{{PACKAGE_NAME}}`, `{{DESCRIPTION}}`                                           |
| `root-tsconfig.json`          | Root TypeScript configuration    | `{{SCOPE}}`                                                                                  |
| `package-tsconfig.json`       | Package TypeScript config (dev)  | None                                                                                         |
| `package-tsconfig.build.json` | Package TypeScript config (prod) | None                                                                                         |
| `npmrc`                       | Registry configuration           | `{{SCOPE}}`                                                                                  |
| `gitignore`                   | Git ignore patterns              | None                                                                                         |
| `editorconfig`                | Editor settings                  | None                                                                                         |
| `prettierrc.json`             | Prettier configuration           | None                                                                                         |

## Placeholder Reference

| Placeholder        | Description            | Example                        |
| ------------------ | ---------------------- | ------------------------------ |
| `{{SCOPE}}`        | npm organization scope | `your-scope`                   |
| `{{REPO_NAME}}`    | Repository name        | `example-repo`                 |
| `{{ORG}}`          | GitHub organization    | `StaytunedLLP`                 |
| `{{DESCRIPTION}}`  | Package description    | `A modular TypeScript library` |
| `{{PACKAGE_NAME}}` | Workspace package name | `utils`                        |
| `{{PACKAGE_1}}`    | First package path     | `core`                         |
| `{{PACKAGE_2}}`    | Second package path    | `server`                       |
| `{{EXAMPLE_1}}`    | Example package path   | `ecom/backend`                 |

## Usage

### Manual Usage

1. Copy template to target location
2. Replace all `{{PLACEHOLDER}}` values
3. Adjust configuration as needed

### Automated Setup

When using the npm-workspace-setup skill, templates are automatically populated based on your responses to the questionnaire.

## Directory Structure After Setup

```plaintext
repo/
├── package.json              ← root-package.json
├── tsconfig.json             ← root-tsconfig.json
├── .npmrc                    ← npmrc
├── .gitignore                ← gitignore
├── .editorconfig             ← editorconfig
├── .prettierrc.json          ← prettierrc.json
├── src/
│   └── packages/
│       └── {package}/
│           ├── package.json  ← package-package.json
│           ├── tsconfig.json ← package-tsconfig.json
│           └── tsconfig.build.json ← package-tsconfig.build.json
```

## Customization Notes

### Adding More Packages

1. Add path to `workspaces` array in root package.json
2. Add export entry in root package.json `exports`
3. Create package directory with all config files
4. Run `npm install` to create symlinks

### Cross-Package Dependencies

In the dependent package's package.json:

```json
{
  "dependencies": {
    "@{{SCOPE}}/other-package": "*"
  }
}
```

The `"*"` uses the workspace protocol - npm resolves to local package.

### Private vs Public Packages

- Set `"private": true` to prevent publishing
- Remove `"private"` to allow publishing to registry
- Configure `"publishConfig"` for registry settings
