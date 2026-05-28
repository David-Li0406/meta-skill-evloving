# Component Library Installation Examples

**Last Updated**: January 6, 2026

> **Note**: See `SKILL.md` for implementation instructions and decision tree.

## Package.json Format

The component library uses npm alias format:
```json
{
  "dependencies": {
    "@royalaholddelhaize/pdl-spectrum-component-library-web": "npm:@RoyalAholdDelhaize/pdl-spectrum-component-library-web@^{latest_version}"
  }
}
```

**Manual installation**: `npm install @RoyalAholdDelhaize/pdl-spectrum-component-library-web`

---

## Example 1: Component Library Requested - Successfully Added

**Scenario**: User requests component library and latest version is fetched successfully

**Configuration**:
```json
{
  "include_component_library": "yes"
}
```

**Execution Flow**:
1. Package JSON Skill generates base package.json
2. Component Library Skill reads package.json
3. Fetches latest version from npm registry
4. Adds component library to dependencies
5. Writes updated package.json back to disk

**Console Output**:
```
## Example 2: Component Library Requested - Fetch Fails (Token Missing)

**Scenario**: User requests component library but fetching latest version fails (likely due to missing GitHub token)

**Configuration**:
```json
{
  "include_component_library": "yes"
}
```

**Execution Flow**:
1. Package JSON Skill generates base package.json
2. Component Library Skill reads package.json
3. Attempts to fetch latest version from npm registry → **FAILS**
4. Skips adding component library to dependencies
5. Informs user about missing token and setup instructions
6. Sets `include_component_library: no` to prevent npmrc generation
7. Project generation continues normally

**Console Output**:
```
⚠️  GitHub token is missing. Skipping component library installation.
📖 To install the component library later, configure a GitHub token:
   https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-npm-registry#authenticating-with-a-personal-access-token
```

**Result**: 
- Component library NOT added to package.json dependencies
- No project .npmrc generated (npmrc skill skipped)
- Project generation continues successfully
- Application still fully functional without component library

---

## Example 3: Component Library Not Requested

**Scenario**: User chooses not to include component library

**Configuration**:
```json
{
  "include_component_library": "no"
}
```

**Execution Flow**:
1. Package JSON Skill generates base package.json
2. Component Library Skill checks `include_component_library` flag → **NO**
3. Skill exits immediately without any modifications
4. No npmrc generated (npmrc skill skipped)
5. Project generation continues normally

**Console Output**:
```
⏭️  Skipping component library - not requested
```

**Result**: 
- Component library NOT added to package.json dependencies
- No project .npmrc generated
- Standard project structure without component library integration