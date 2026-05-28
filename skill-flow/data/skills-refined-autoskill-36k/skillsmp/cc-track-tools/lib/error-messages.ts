// ABOUTME: Error message templates for plugin installation and dependency issues
// ABOUTME: Provides clear, actionable error messages to guide users through common setup problems

/**
 * Error message when both npm and plugin versions are detected
 */
export function getNpmPluginConflictMessage(): string {
  return `
⚠️ npm/plugin conflict detected

You have both the npm package and plugin versions of cc-track installed.
This will cause conflicts. Please uninstall the npm version first.

To uninstall the npm version:
\`\`\`bash
npm uninstall -g cc-track
\`\`\`

After uninstalling, restart Claude Code and try again.
`.trim();
}

/**
 * Error message when plugin dependencies are missing
 */
export function getMissingDependenciesMessage(pluginRoot: string): string {
  return `
⚠️ Plugin dependencies not installed

cc-track plugin dependencies are not installed. You need to run \`bun install\` in the plugin directory.

To install dependencies:
\`\`\`bash
cd ${pluginRoot}
bun install
\`\`\`

After installing, try your command again.
`.trim();
}

/**
 * Error message when Bun runtime is not installed
 */
export function getBunNotInstalledMessage(): string {
  return `
⚠️ Bun runtime not found

cc-track plugin requires Bun runtime to execute TypeScript directly.

To install Bun:
\`\`\`bash
curl -fsSL https://bun.sh/install | bash
\`\`\`

Or visit https://bun.sh for installation instructions.

After installing Bun, restart your terminal and try again.
`.trim();
}

/**
 * Error message when plugin root is not set
 */
export function getPluginRootNotSetMessage(): string {
  return `
⚠️ Plugin root not found

The \${CLAUDE_PLUGIN_ROOT} environment variable is not set.
This usually means cc-track is not running as a Claude Code plugin.

Make sure you:
1. Installed cc-track as a Claude Code plugin (not via npm)
2. Are running commands through Claude Code (not directly from terminal)

If you need to install the plugin, see the README for installation instructions.
`.trim();
}
