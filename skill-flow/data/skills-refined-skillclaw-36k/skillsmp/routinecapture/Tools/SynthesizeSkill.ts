#!/usr/bin/env bun
/**
 * SynthesizeSkill.ts - Generate a personal skill from extracted workflow data
 *
 * Creates the skill directory structure with SKILL.md and Workflows/Execute.md
 * based on extracted workflow data from ExtractWorkflow.ts
 *
 * CLI Usage:
 *   bun SynthesizeSkill.ts --name "_MyRoutine" --workflow '<json>'
 *   bun SynthesizeSkill.ts --name "_MyRoutine" --workflow-file extracted.json
 *   bun SynthesizeSkill.ts --name "_MyRoutine" --triggers "trigger1, trigger2"
 *
 * Module Usage:
 *   import { synthesizeSkill } from './SynthesizeSkill'
 */

import { mkdirSync, writeFileSync, existsSync } from 'fs';
import { join } from 'path';
import { homedir } from 'os';

// ============================================================================
// Types
// ============================================================================

export interface SynthesizeInput {
  name: string;  // Must start with _ for personal skills
  workflow: {
    originalRequest: string;
    steps: {
      index: number;
      description: string;
      tool: string;
      inputs: Record<string, any>;
      capability: 'browser' | 'code' | 'file' | 'api' | 'mixed';
      isCorrection: boolean;
    }[];
    parameters: {
      name: string;
      value: string;
      type: 'path' | 'url' | 'text' | 'number';
      isRequired: boolean;
      suggestedDefault: string | null;
    }[];
    suggestedTriggers: string[];
    metadata: {
      sessionId: string;
      extractedAt: string;
    };
  };
  additionalTriggers?: string[];
}

export interface SynthesizeResult {
  skillPath: string;
  skillMdPath: string;
  workflowPath: string;
  success: boolean;
  error?: string;
}

// ============================================================================
// Constants
// ============================================================================

const HOME = homedir();
const SKILLS_DIR = join(HOME, '.claude', 'skills');

// ============================================================================
// Skill Generation
// ============================================================================

/**
 * Generate and write a personal skill from workflow data
 */
export function synthesizeSkill(input: SynthesizeInput): SynthesizeResult {
  const { name, workflow, additionalTriggers = [] } = input;

  // Validate name starts with underscore
  if (!name.startsWith('_')) {
    return {
      skillPath: '',
      skillMdPath: '',
      workflowPath: '',
      success: false,
      error: 'Personal skill names must start with underscore (_)',
    };
  }

  // Create skill directory path
  const skillPath = join(SKILLS_DIR, name);
  const workflowsPath = join(skillPath, 'Workflows');
  const skillMdPath = join(skillPath, 'SKILL.md');
  const executeWorkflowPath = join(workflowsPath, 'Execute.md');

  try {
    // Create directories
    mkdirSync(workflowsPath, { recursive: true });

    // Generate SKILL.md content
    const skillMdContent = generateSkillMd(name, workflow, additionalTriggers);
    writeFileSync(skillMdPath, skillMdContent);

    // Generate Workflows/Execute.md content
    const executeContent = generateExecuteWorkflow(name, workflow);
    writeFileSync(executeWorkflowPath, executeContent);

    return {
      skillPath,
      skillMdPath,
      workflowPath: executeWorkflowPath,
      success: true,
    };
  } catch (error) {
    return {
      skillPath,
      skillMdPath,
      workflowPath: executeWorkflowPath,
      success: false,
      error: error instanceof Error ? error.message : 'Unknown error',
    };
  }
}

/**
 * Generate SKILL.md content
 */
function generateSkillMd(
  name: string,
  workflow: SynthesizeInput['workflow'],
  additionalTriggers: string[]
): string {
  const triggers = [...workflow.suggestedTriggers, ...additionalTriggers];
  const triggerString = triggers.join(', ');

  // Generate description (max ~100 chars before USE WHEN)
  const shortDesc = workflow.originalRequest.length > 80
    ? workflow.originalRequest.slice(0, 77) + '...'
    : workflow.originalRequest;

  // Determine required capabilities
  const capabilities = new Set(workflow.steps.map(s => s.capability));
  const capabilityNote = capabilities.size > 1
    ? `Requires: ${[...capabilities].join(', ')}`
    : '';

  // Build parameters table
  let paramsTable = '';
  if (workflow.parameters.length > 0) {
    paramsTable = `## Parameters

| Parameter | Default | Required | Description |
|-----------|---------|----------|-------------|
${workflow.parameters.map(p => {
  const defaultVal = p.suggestedDefault || '-';
  const req = p.isRequired ? 'Yes' : 'No';
  return `| \`${p.name}\` | ${defaultVal} | ${req} | ${p.type} value |`;
}).join('\n')}
`;
  }

  const content = `---
name: ${name}
description: ${shortDesc}. USE WHEN ${triggerString}.
---

# ${name}

Personal routine captured ${new Date().toISOString().split('T')[0]}.

${capabilityNote}

${paramsTable}
## Workflow Routing

| Workflow | Trigger | File |
|----------|---------|------|
| **Execute** | Run this routine | \`Workflows/Execute.md\` |

## Examples

**Example 1: Basic invocation**
\`\`\`
User: "${triggers[0] || 'run routine'}"
→ Invokes Execute workflow
→ Follows captured steps
\`\`\`

## Origin

- **Session**: ${workflow.metadata.sessionId || 'unknown'}
- **Captured**: ${workflow.metadata.extractedAt || new Date().toISOString()}
- **Original request**: "${workflow.originalRequest.slice(0, 100)}"
`;

  return content.trim() + '\n';
}

/**
 * Generate Workflows/Execute.md content
 */
function generateExecuteWorkflow(
  name: string,
  workflow: SynthesizeInput['workflow']
): string {
  // Build parameters section
  let paramsSection = '';
  if (workflow.parameters.length > 0) {
    paramsSection = `## Parameters

${workflow.parameters.map(p => {
  const req = p.isRequired ? '(required)' : `(default: ${p.suggestedDefault || 'none'})`;
  return `- \`${p.name}\` ${req}: ${p.type} value`;
}).join('\n')}
`;
  }

  // Build steps section - group by capability when useful
  const stepsByCapability = new Map<string, typeof workflow.steps>();
  for (const step of workflow.steps) {
    const cap = step.capability;
    if (!stepsByCapability.has(cap)) {
      stepsByCapability.set(cap, []);
    }
    stepsByCapability.get(cap)!.push(step);
  }

  // Generate step content
  let stepsContent = '';
  let stepNum = 1;

  for (const step of workflow.steps) {
    // Skip correction steps - use the corrected version
    if (step.isCorrection) continue;

    const capBadge = getCapabilityBadge(step.capability);

    stepsContent += `### Step ${stepNum}: ${step.description}
${capBadge}

`;

    // Add specific guidance based on tool
    if (step.tool === 'Read') {
      stepsContent += `Read the file to understand its contents.\n\n`;
    } else if (step.tool === 'Write') {
      stepsContent += `Create/overwrite the file with generated content.\n\n`;
    } else if (step.tool === 'Edit') {
      stepsContent += `Modify the existing file.\n\n`;
    } else if (step.tool === 'Bash') {
      const cmd = step.inputs.command?.slice(0, 80) || 'command';
      stepsContent += `\`\`\`bash\n${cmd}\n\`\`\`\n\n`;
    } else if (step.tool.includes('navigate')) {
      stepsContent += `Navigate browser to the target URL.\n\n`;
    } else if (step.tool.includes('read_page')) {
      stepsContent += `Read and analyze the page content.\n\n`;
    } else if (step.tool.includes('form_input')) {
      stepsContent += `Fill in the form field.\n\n`;
    } else if (step.tool.includes('computer')) {
      stepsContent += `Perform browser interaction: ${step.inputs.action || 'action'}\n\n`;
    }

    stepNum++;
  }

  const content = `# Execute ${name}

Captured workflow for: "${workflow.originalRequest.slice(0, 100)}"

${paramsSection}
## Steps

${stepsContent}
## Notes

- This routine was automatically captured from a conversation
- Steps marked with capabilities indicate required tools (browser, file, code)
- Parameters can be overridden when invoking this routine
`;

  return content.trim() + '\n';
}

/**
 * Get capability badge for step display
 */
function getCapabilityBadge(capability: string): string {
  const badges: Record<string, string> = {
    browser: '🌐 **Browser**',
    file: '📁 **File**',
    code: '💻 **Code**',
    api: '🔗 **API**',
    mixed: '🔄 **Mixed**',
  };
  return badges[capability] || '';
}

// ============================================================================
// CLI
// ============================================================================

if (import.meta.main) {
  const args = process.argv.slice(2);

  // Parse arguments
  let name = '';
  let workflowJson = '';
  let workflowFile = '';
  let additionalTriggers: string[] = [];

  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--name' && args[i + 1]) {
      name = args[++i];
    } else if (args[i] === '--workflow' && args[i + 1]) {
      workflowJson = args[++i];
    } else if (args[i] === '--workflow-file' && args[i + 1]) {
      workflowFile = args[++i];
    } else if (args[i] === '--triggers' && args[i + 1]) {
      additionalTriggers = args[++i].split(',').map(t => t.trim());
    }
  }

  if (!name) {
    console.log(`Usage: bun SynthesizeSkill.ts --name "_MyRoutine" --workflow '<json>'
       bun SynthesizeSkill.ts --name "_MyRoutine" --workflow-file extracted.json

Options:
  --name <name>           Skill name (must start with _)
  --workflow <json>       Workflow data as JSON string
  --workflow-file <path>  Path to workflow JSON file
  --triggers <list>       Additional trigger phrases (comma-separated)
`);
    process.exit(1);
  }

  // Load workflow data
  let workflow: SynthesizeInput['workflow'];

  if (workflowFile) {
    try {
      const content = Bun.file(workflowFile);
      workflow = JSON.parse(await content.text());
    } catch (error) {
      console.error('Error reading workflow file:', error);
      process.exit(1);
    }
  } else if (workflowJson) {
    try {
      workflow = JSON.parse(workflowJson);
    } catch (error) {
      console.error('Error parsing workflow JSON:', error);
      process.exit(1);
    }
  } else {
    console.error('Must provide --workflow or --workflow-file');
    process.exit(1);
  }

  // Synthesize the skill
  const result = synthesizeSkill({
    name,
    workflow,
    additionalTriggers,
  });

  if (result.success) {
    console.log(`✅ Skill created successfully!`);
    console.log(`   Skill path: ${result.skillPath}`);
    console.log(`   SKILL.md: ${result.skillMdPath}`);
    console.log(`   Workflow: ${result.workflowPath}`);
  } else {
    console.error(`❌ Failed to create skill: ${result.error}`);
    process.exit(1);
  }
}
