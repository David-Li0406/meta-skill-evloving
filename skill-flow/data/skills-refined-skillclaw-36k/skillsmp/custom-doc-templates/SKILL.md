---
name: custom-doc-templates
description: Enable coding agents to create custom Handlebars templates for documentation generation and use them to generate professional documentation. Use when users want to create specialized documentation types or customize existing templates. Integrates with the Context-Aware Documentation Generation feature (P023).
---

# Custom Documentation Templates Skill

This skill enables coding agents to create custom Handlebars templates for automated documentation generation and use them to generate professional, spec-traceable documentation for SEA-Forge™ projects.

## When to Offer This Skill

**Trigger conditions:**
- User mentions creating a custom template: "create a template", "new template", "custom doc template"
- User wants specialized documentation: "generate a deployment guide", "create an SLA doc", "write a runbook"
- User mentions customizing existing templates: "modify the README template", "update the architecture template"
- User asks about documentation capabilities: "what docs can you generate?", "how do I customize templates?"

**Initial offer:**
Explain that the agent can help create custom Handlebars templates for any documentation type and use them to generate documentation with context-aware analysis. The process involves:

1. **Template Design**: Define the structure, sections, and data requirements
2. **Template Creation**: Write the Handlebars template with Markdown helpers
3. **Testing**: Validate the template with sample data
4. **Generation**: Use the template to generate documentation for projects

Ask if they want to create a new template or use existing templates to generate documentation.

## Mode 1: Create Custom Template

### Step 1: Understand Requirements

Ask the user:
1. What type of documentation is this? (e.g., Deployment Guide, SLA, Runbook, Migration Guide)
2. Who's the target audience?
3. What sections should it include?
4. What data will be needed? (e.g., project context, specs, architecture, custom metadata)
5. Any specific formatting or style requirements?

### Step 2: Design Template Structure

Based on their answers, propose a template structure:

```markdown
Proposed structure for [TEMPLATE TYPE]:

## Sections
1. [Section 1 Name] - [Purpose]
2. [Section 2 Name] - [Purpose]
3. [Section 3 Name] - [Purpose]
...

## Data Requirements
- projectName
- description
- [custom fields...]

## Available Helpers
- {{codeBlock code lang}} - Markdown code blocks
- {{link text url}} - Markdown links
- {{table headers rows}} - Markdown tables
- {{mermaid diagram}} - Mermaid diagrams
- {{heading level text}} - Headings (h1-h6)
```

Ask if this structure works or if they want to adjust it.

### Step 3: Create Template File

Create the Handlebars template file in `libs/documentation/templates/[TEMPLATE_NAME].hbs`:

```handlebars
# {{projectName}} [Template Type]

## Overview
{{description}}

{{#if customSection1}}
## [Section 1]
{{customSection1}}
{{/if}}

... [rest of template]

## Specification Traceability
| Type | ID | Title |
| --- | --- | --- |
{{#each traceability}}
| {{type}} | {{link id url}} | {{title}} |
{{/each}}
```

**Key Guidelines:**
- Use Handlebars syntax: `{{variable}}`, `{{#if condition}}`, `{{#each array}}`
- Use available helpers for Markdown formatting
- Always include traceability section
- Use semantic HTML structure
- Make sections conditional when appropriate

### Step 4: Register Template in Code

Create/update the template registration service:

```typescript
// In libs/documentation/adapters/src/template-registry.ts
import { HandlebarsTemplateAdapter } from './handlebars-template.adapter';
import * as fs from 'fs/promises';
import * as path from 'path';

export class TemplateRegistry {
  private adapter: HandlebarsTemplateAdapter;

  constructor() {
    this.adapter = new HandlebarsTemplateAdapter();
  }

  async registerTemplate(templateId: string, templatePath: string): Promise<void> {
    const content = await fs.readFile(templatePath, 'utf-8');
    await this.adapter.registerFromContent(templateId, templateId.toUpperCase(), content);
  }

  async loadAllTemplates(): Promise<void> {
    const templatesDir = path.join(__dirname, '../../templates');
    const files = await fs.readdir(templatesDir);
    
    for (const file of files) {
      if (file.endsWith('.hbs')) {
        const templateId = file.replace('.hbs', '');
        await this.registerTemplate(templateId, path.join(templatesDir, file));
      }
    }
  }
}
```

### Step 5: Create Sample Data

Create a sample data file to test the template:

```typescript
// sample-data/[template-name].json
{
  "projectName": "Example Service",
  "description": "A sample microservice...",
  "customField1": "...",
  "traceability": [
    {
      "type": "ADR",
      "id": "ADR-024",
      "title": "Automated Documentation Generation",
      "url": "file:///path/to/adr/024.md"
    }
  ]
}
```

### Step 6: Test Template

Test the template rendering:

```typescript
import { TemplateRegistry } from './template-registry';
import * as fs from 'fs/promises';

const registry = new TemplateRegistry();
await registry.registerTemplate('[template-id]', './templates/[TEMPLATE_NAME].hbs');

const sampleData = JSON.parse(
  await fs.readFile('./sample-data/[template-name].json', 'utf-8')
);

const output = await registry.adapter.render('[template-id]', sampleData);
console.log(output);
```

Review the output with the user and iterate on the template as needed.

### Step 7: Document Template Usage

Create documentation for the template in `libs/documentation/templates/README.md`:

```markdown
## [Template Name]

**Purpose**: [Brief description]

**Audience**: [Target readers]

**Data Requirements**:
- `projectName` (string) - Name of the project
- `description` (string) - Project description
- [other fields...

]

**Usage**:
```bash
just doc-generate /path/to/project [template-id]
```

**Example Output**: See `sample-data/[template-name]-example.md`
```

## Mode 2: Generate Documentation from Templates

### Step 1: List Available Templates

Show user available templates:

```bash
# List built-in templates
ls libs/documentation/templates/

# Available templates:
# - README.hbs
# - ARCHITECTURE.hbs
# - API_REFERENCE.hbs
# - [custom templates...]
```

### Step 2: Analyze Project Context

```bash
# Enable AST analysis for code structure (optional)
export ENABLE_AST_ANALYSIS=true

# Analyze project context
just context-analyze /path/to/project
```

This extracts:
- Specifications (SDS, ADR, PRD)
- CALM architecture model
- Code structure (if enabled)
- Dependencies
- Technical stack

### Step 3: Prepare Template Data

Create a data preparation script or gather data manually:

```typescript
// prepare-doc-data.ts
import { SpecAnalyzerAdapter } from '@sea/context-adapters';
import { CalmAnalyzerAdapter } from '@sea/context-adapters';

async function prepareData(projectPath: string) {
  const specAnalyzer = new SpecAnalyzerAdapter();
  const calmAnalyzer = new CalmAnalyzerAdapter();

  const specs = await specAnalyzer.extractSpecs(projectPath);
  const architecture = await calmAnalyzer.extractArchitecture(projectPath);

  return {
    projectName: /* derive from package.json */,
    description: /* from README or specs */,
    features: /* from SDS files */,
    architecture: {
      nodes: architecture.nodes,
      relationships: architecture.relationships
    },
    traceability: specs.sdsList.map(sds => ({
      type: 'SDS',
      id: sds.id,
      title: sds.title,
      url: `file://${sds.path}`
    }))
  };
}
```

### Step 4: Generate Documentation

```bash
# Generate documentation using template
just doc-generate /path/to/project [template-type]

# Examples:
just doc-generate ./libs/my-service readme
just doc-generate ./libs/my-service architecture
just doc-generate ./libs/my-service deployment-guide
```

### Step 5: Validate Output

```bash
# Validate generated documentation
just doc-validate /path/to/project/docs/generated/[type].md
```

Validation checks:
- Required sections present (POL-DOC-002)
- Traceability links included (POL-DOC-003)
- Template conformance
- Markdown syntax validity

### Step 6: Iterate as Needed

If validation fails or output needs adjustment:
1. Review validation errors
2. Check template data
3. Update template or data as needed
4. Regenerate

## Advanced: Custom Handlebars Helpers

### Creating Custom Helpers

If built-in helpers aren't sufficient, create custom ones:

```typescript
// In HandlebarsTemplateAdapter
Handlebars.registerHelper('customHelper', (arg1: string, arg2: string) => {
  // Custom logic
  return new Handlebars.SafeString(result);
});
```

**Example: Status Badge Helper**

```typescript
Handlebars.registerHelper('statusBadge', (status: string) => {
  const badges = {
    'approved': '![Status: Approved](https://img.shields.io/badge/status-approved-green)',
    'draft': '![Status: Draft](https://img.shields.io/badge/status-draft-yellow)',
    'deprecated': '![Status: Deprecated](https://img.shields.io/badge/status-deprecated-red)'
  };
  return new Handlebars.SafeString(badges[status] || '');
});
```

**Usage in template:**
```handlebars
{{statusBadge status}}
```

## Best Practices

### Template Design

1. **Start Simple**: Begin with minimal sections, add complexity as needed
2. **Make Sections Conditional**: Use `{{#if}}` for optional sections
3. **Reuse Components**: Create partial templates for common sections
4. **Include Examples**: Show examples of expected output
5. **Document Data Shape**: Clearly specify what data is required

### Data Preparation

1. **Validate Inputs**: Check for required fields before rendering
2. **Provide Defaults**: Use sensible defaults for optional fields
3. **Transform Data**: Shape data to match template expectations
4. **Cache Context**: Reuse analyzed context for multiple templates

### Quality Assurance

1. **Test with Real Data**: Use actual project data, not just mocks
2. **Validate Output**: Run `just doc-validate` on generated docs
3. **Check Links**: Ensure traceability links are valid
4. **Review Manually**: Have humans review generated documentation

## Common Templates to Create

### Deployment Guide
- Prerequisites
- Configuration
- Deployment steps
- Rollback procedure
- Troubleshooting

### Runbook
- Service overview
- Common operations
- Monitoring and alerts
- Incident response
- Escalation procedures

### SLA Document
- Service description
- Availability targets
- Performance metrics
- Support levels
- Change management

### Migration Guide
- Current state
- Target state
- Migration steps
- Rollback plan
- Known risks

### API Changelog
- Version history
- Breaking changes
- New features
- Deprecations
- Migration notes

## Troubleshooting

### Template Not Rendering

**Symptom**: Template produces empty or malformed output

**Solutions**:
1. Check data matches template variables
2. Verify Handlebars syntax is correct
3. Test with minimal template first
4. Check for typos in variable names

### Missing Traceability Links

**Symptom**: Traceability section is empty

**Solutions**:
1. Ensure `traceability` array is in data
2. Check spec files have proper frontmatter
3. Run `just spec-guard` to validate specs
4. Verify file paths are absolute

### Handlebars Syntax Errors

**Symptom**: Template compilation fails

**Solutions**:
1. Balance all `{{#if}}` with `{{/if}}`
2. Balance all `{{#each}}` with `{{/each}}`
3. Escape literal braces: `\{{not_a_variable}}`
4. Check helper syntax matches registration

## Integration with P023

This skill leverages the Context-Aware Documentation Generation feature:

- **Universal Context Service (SDS-051)**: Provides context extraction
- **Documentation Orchestrator Service (SDS-036)**: Manages generation workflow
- **Template Engine**: Handlebars adapter with Markdown helpers
- **Feature Flags**: Control analysis depth

**Just Commands**:
- `just doc-generate <project> <type>`
- `just doc-validate <artifact>`
- `just context-analyze <project>`

## Example Session

```bash
# User: "I want to create a deployment guide template"

# Agent: [Creates template structure based on requirements]

# Agent: [Writes Handlebars template to libs/documentation/templates/deployment-guide.hbs]

# Agent: [Creates sample data file]

# Agent: [Tests template and shows output]

# User: "Looks good! Now generate one for my-service"

# Agent:
just context-analyze ./libs/my-service
just doc-generate ./libs/my-service deployment-guide

# Agent: [Shows generated deployment-guide.md]

# User: "Perfect!"
```

## Exit Criteria

Template creation is complete when:
- Template file exists in `libs/documentation/templates/`
- Template renders correctly with sample data
- Generated output validates successfully
- Documentation for the template is created

Generation is complete when:
- Documentation is generated at expected location
- Validation passes
- Output meets user requirements
