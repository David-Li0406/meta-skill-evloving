---
name: ts-morph-refactoring
description: TypeScript refactoring using ts-morph in pnpm monorepos. Use when renaming variables, functions, classes, or types across packages; updating imports; moving files; or performing codemod operations. Triggers on requests involving TypeScript AST manipulation, bulk code changes, or cross-package refactoring.
---

# ts-morph Refactoring in pnpm Monorepos

## Setup

```typescript
import { Project } from "ts-morph";

const project = new Project({
  tsConfigFilePath: "./tsconfig.json", // Root tsconfig with project references
});

// For monorepo: add all package tsconfigs
project.addSourceFilesFromTsConfig("./packages/*/tsconfig.json");
```

## Rename Variable/Function

```typescript
const sourceFile = project.getSourceFileOrThrow("src/utils.ts");

// Find and rename
const fn = sourceFile.getFunctionOrThrow("oldName");
fn.rename("newName"); // Updates all references across project

// For exports - also updates import statements
const exportedFn = sourceFile.getExportedDeclarations().get("oldExport")?.[0];
exportedFn?.asKind(SyntaxKind.FunctionDeclaration)?.rename("newExport");

project.saveSync();
```

## Rename Across Packages

```typescript
// Find declaration in any package
const declaration = project.getSourceFiles()
  .flatMap(sf => sf.getExportedDeclarations().get("targetName") ?? [])
  .find(d => d.getSourceFile().getFilePath().includes("packages/shared"));

declaration?.asKind(SyntaxKind.FunctionDeclaration)?.rename("newTargetName");
// All imports in all packages update automatically

project.saveSync();
```

## Update Import Paths

```typescript
// Change import path across all files
project.getSourceFiles().forEach(sourceFile => {
  sourceFile.getImportDeclarations().forEach(imp => {
    const moduleSpec = imp.getModuleSpecifierValue();
    if (moduleSpec === "@old/package") {
      imp.setModuleSpecifier("@new/package");
    }
    // Relative path updates
    if (moduleSpec.startsWith("../old-folder/")) {
      imp.setModuleSpecifier(moduleSpec.replace("../old-folder/", "../new-folder/"));
    }
  });
});

project.saveSync();
```

## Add/Remove Named Imports

```typescript
sourceFile.getImportDeclarations().forEach(imp => {
  if (imp.getModuleSpecifierValue() === "@company/utils") {
    // Add named import
    imp.addNamedImport("newUtil");
    
    // Remove named import
    imp.getNamedImports()
      .find(n => n.getName() === "deprecatedUtil")
      ?.remove();
    
    // Rename named import
    imp.getNamedImports()
      .find(n => n.getName() === "oldUtil")
      ?.setName("renamedUtil");
  }
});
```

## Move Export Between Packages

```typescript
// Get source declaration
const srcFile = project.getSourceFileOrThrow("packages/old/src/helper.ts");
const fn = srcFile.getFunctionOrThrow("helperFn");
const fnText = fn.getFullText();

// Add to destination
const destFile = project.getSourceFileOrThrow("packages/new/src/helper.ts");
destFile.addStatements(fnText);

// Update all imports
project.getSourceFiles().forEach(sf => {
  sf.getImportDeclarations()
    .filter(i => i.getModuleSpecifierValue() === "@company/old")
    .forEach(imp => {
      const namedImport = imp.getNamedImports().find(n => n.getName() === "helperFn");
      if (namedImport) {
        namedImport.remove();
        if (imp.getNamedImports().length === 0) imp.remove();
        
        // Add new import if not exists
        const existingNew = sf.getImportDeclaration("@company/new");
        if (existingNew) {
          existingNew.addNamedImport("helperFn");
        } else {
          sf.addImportDeclaration({
            moduleSpecifier: "@company/new",
            namedImports: ["helperFn"]
          });
        }
      }
    });
});

// Remove from source after updating imports
fn.remove();
project.saveSync();
```

## Common Patterns

### Find All References
```typescript
const refs = declaration.findReferencesAsNodes();
refs.forEach(ref => console.log(ref.getSourceFile().getFilePath(), ref.getStartLineNumber()));
```

### Batch Rename Pattern
```typescript
const renames = [["oldA", "newA"], ["oldB", "newB"]];
renames.forEach(([old, new_]) => {
  project.getSourceFiles().forEach(sf => {
    sf.getExportedDeclarations().get(old)?.[0]
      ?.asKind(SyntaxKind.FunctionDeclaration)?.rename(new_);
  });
});
project.saveSync();
```

### Dry Run
```typescript
// Preview changes without saving
project.getSourceFiles().forEach(sf => {
  if (sf.wasSaved() === false) {
    console.log(`Would modify: ${sf.getFilePath()}`);
    console.log(sf.getFullText());
  }
});
```

## Notes

- Always use `project.saveSync()` after refactoring
- `rename()` handles cross-file references automatically
- For pnpm workspaces: ensure root tsconfig has `references` to all packages
- Use `SyntaxKind` enum for type narrowing: `import { SyntaxKind } from "ts-morph"`
