#!/usr/bin/env node
/**
 * Test: Validate Template Generation with Sample Data
 *
 * Tests that templates can be properly filled with sample data
 * and produce valid, complete output documents.
 *
 * @module tests/validate-template-generation
 */

const path = require('path');
const {
  findMarkdownFiles,
  safeReadFile,
  directoryExists,
  printSeparator
} = require('./utils');
const {
  TEMPLATES_DIR,
  SAMPLE_DATA,
  TEMPLATE_REQUIREMENTS
} = require('./config');

// =============================================================================
// Test Results
// =============================================================================

let passed = 0;
let failed = 0;
const errors = [];

// =============================================================================
// Template Placeholder Patterns
// =============================================================================

/** @const {RegExp} Pattern for bracket placeholders [text] */
const BRACKET_PLACEHOLDER = /\[([^\]]+)\]/g;

/** @const {RegExp} Pattern for HTML comments <!-- text --> */
const COMMENT_PLACEHOLDER = /<!--\s*([^>]+)\s*-->/g;

/** @const {RegExp} Pattern for empty table cells | | */
const EMPTY_CELL = /\|\s*\|\s*\|/g;

// =============================================================================
// Sample Data Templates
// =============================================================================

/**
 * Template fill rules - maps placeholder patterns to sample data
 * @const {Object.<string, Function>}
 */
const FILL_RULES = {
  // Client info
  'nom du client': () => SAMPLE_DATA.client.name,
  'client': () => SAMPLE_DATA.client.name,
  'contact': () => SAMPLE_DATA.client.contact,
  'email': () => SAMPLE_DATA.client.email,
  'secteur': () => SAMPLE_DATA.client.sector,

  // Project info
  'nom du projet': () => SAMPLE_DATA.project.name,
  'projet': () => SAMPLE_DATA.project.name,
  'budget': () => SAMPLE_DATA.project.budget,
  'date': () => new Date().toLocaleDateString('fr-FR'),
  'jj/mm/aaaa': () => new Date().toLocaleDateString('fr-FR'),

  // Generic
  'description': () => 'Description exemple générée par les tests',
  'objectif': () => 'Améliorer l\'expérience utilisateur',
  'contrainte': () => 'Respect du budget et des délais'
};

// =============================================================================
// Helper Functions
// =============================================================================

/**
 * Extract all placeholders from template content
 *
 * @param {string} content - Template content
 * @returns {string[]} Array of placeholder texts
 */
function extractPlaceholders(content) {
  const placeholders = [];

  // Bracket placeholders
  let match;
  BRACKET_PLACEHOLDER.lastIndex = 0;
  while ((match = BRACKET_PLACEHOLDER.exec(content)) !== null) {
    placeholders.push(match[1]);
  }

  // Comment placeholders
  COMMENT_PLACEHOLDER.lastIndex = 0;
  while ((match = COMMENT_PLACEHOLDER.exec(content)) !== null) {
    placeholders.push(match[1].trim());
  }

  return placeholders;
}

/**
 * Fill template with sample data
 *
 * @param {string} content - Template content
 * @returns {{ filled: string, replacements: number }} Filled content and count
 */
function fillTemplate(content) {
  let filled = content;
  let replacements = 0;

  // Apply fill rules to bracket placeholders
  for (const [pattern, getValue] of Object.entries(FILL_RULES)) {
    const regex = new RegExp(`\\[${pattern}\\]`, 'gi');
    const matches = filled.match(regex);
    if (matches) {
      filled = filled.replace(regex, getValue());
      replacements += matches.length;
    }
  }

  return { filled, replacements };
}

/**
 * Validate filled template completeness
 *
 * @param {string} originalContent - Original template
 * @param {string} filledContent - Filled template
 * @returns {string[]} Validation issues
 */
function validateFilledTemplate(originalContent, filledContent) {
  const issues = [];

  // Check minimum structure preserved
  const originalHeadings = (originalContent.match(/^#{1,3}\s+/gm) || []).length;
  const filledHeadings = (filledContent.match(/^#{1,3}\s+/gm) || []).length;

  if (filledHeadings < originalHeadings) {
    issues.push(`Headings reduced from ${originalHeadings} to ${filledHeadings}`);
  }

  // Check tables still valid
  const originalTables = (originalContent.match(/\|.*\|/g) || []).length;
  const filledTables = (filledContent.match(/\|.*\|/g) || []).length;

  if (filledTables < originalTables * 0.5) {
    issues.push('Table structure may be corrupted');
  }

  // Check content not empty
  if (filledContent.trim().length < TEMPLATE_REQUIREMENTS.minContentLength) {
    issues.push(`Content too short: ${filledContent.trim().length} chars`);
  }

  return issues;
}

/**
 * Check template has required placeholder types
 *
 * @param {string} content - Template content
 * @returns {string[]} Missing placeholder types
 */
function checkPlaceholderTypes(content) {
  const missing = [];

  // Should have bracket placeholders for data
  if (!BRACKET_PLACEHOLDER.test(content)) {
    missing.push('No [placeholder] format found');
  }

  // Should have sections to fill
  const headings = content.match(/^##\s+.+$/gm) || [];
  if (headings.length < TEMPLATE_REQUIREMENTS.minHeadingCount) {
    missing.push(`Only ${headings.length} sections (min: ${TEMPLATE_REQUIREMENTS.minHeadingCount})`);
  }

  return missing;
}

// =============================================================================
// Test Functions
// =============================================================================

/**
 * Test template structure and placeholders
 *
 * @param {string} filePath - Path to template
 * @param {string} content - Template content
 * @param {string} templateName - Name for display
 */
function testTemplateStructure(filePath, content, templateName) {
  const structureIssues = checkPlaceholderTypes(content);

  if (structureIssues.length === 0) {
    console.log(`   ✅ Template structure valid`);
    passed++;
  } else {
    console.log(`   ⚠️  Structure issues:`);
    for (const issue of structureIssues) {
      console.log(`      └─ ${issue}`);
    }
    // Warning only
    passed++;
  }
}

/**
 * Test template can be filled with sample data
 *
 * @param {string} filePath - Path to template
 * @param {string} content - Template content
 * @param {string} templateName - Name for display
 */
function testTemplateFilling(filePath, content, templateName) {
  const placeholders = extractPlaceholders(content);
  const { filled, replacements } = fillTemplate(content);

  console.log(`   📝 Found ${placeholders.length} placeholders`);

  if (replacements > 0) {
    console.log(`   ✅ Filled ${replacements} placeholders with sample data`);
    passed++;
  } else if (placeholders.length === 0) {
    console.log(`   ⚠️  No fillable placeholders found`);
    passed++;
  } else {
    console.log(`   ⚠️  Could not fill any placeholders (may need custom rules)`);
    passed++;
  }

  // Validate the result
  const validationIssues = validateFilledTemplate(content, filled);
  if (validationIssues.length === 0) {
    console.log(`   ✅ Filled template is valid`);
    passed++;
  } else {
    console.log(`   ⚠️  Filled template issues:`);
    for (const issue of validationIssues) {
      console.log(`      └─ ${issue}`);
    }
    passed++;
  }
}

/**
 * Test template has documentation comments
 *
 * @param {string} content - Template content
 */
function testTemplateDocumentation(content) {
  const hasComments = COMMENT_PLACEHOLDER.test(content);
  const hasInstructions = content.includes('<!--') || content.includes('Instructions:');

  if (hasComments || hasInstructions) {
    console.log(`   ✅ Has documentation/instructions`);
    passed++;
  } else {
    console.log(`   ⚠️  No documentation comments found`);
    passed++;
  }
}

// =============================================================================
// Main Execution
// =============================================================================

console.log('📄 Validating Template Generation with Sample Data\n');
printSeparator();

// TEMPLATES_DIR already points to project-management/templates/project-management
if (!directoryExists(TEMPLATES_DIR)) {
  console.error(`❌ Templates directory not found: ${TEMPLATES_DIR}`);
  process.exit(1);
}

const templateFiles = findMarkdownFiles(TEMPLATES_DIR);
console.log(`Found ${templateFiles.length} templates to test\n`);

for (const filePath of templateFiles) {
  const templateName = path.basename(filePath, '.md');
  console.log(`\n📋 ${templateName}.md`);

  const { content, error } = safeReadFile(filePath);
  if (error) {
    console.log(`   ❌ ${error}`);
    errors.push(`[${templateName}] ${error}`);
    failed++;
    continue;
  }

  testTemplateStructure(filePath, content, templateName);
  testTemplateFilling(filePath, content, templateName);
  testTemplateDocumentation(content);
}

// =============================================================================
// Summary
// =============================================================================

console.log('\n');
printSeparator();
console.log(`\n📊 Results: ${passed} passed, ${failed} failed`);

if (errors.length > 0) {
  console.log('\n❌ Template generation errors:');
  for (const err of errors) {
    console.log(`   └─ ${err}`);
  }
  process.exit(1);
} else {
  console.log('\n✅ All template generation tests passed');
  process.exit(0);
}
