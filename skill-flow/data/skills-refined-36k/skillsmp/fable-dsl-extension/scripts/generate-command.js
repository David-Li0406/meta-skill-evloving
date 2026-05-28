#!/usr/bin/env node

/**
 * DSL Command Generator
 * Generates boilerplate code for new FableDSL commands
 */

const fs = require('fs');
const path = require('path');

function generateCommand({ name, category, properties = [] }) {
  const pascalName = name.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase()).replace(/\s+/g, '');
  const camelName = name.replace(/_([a-z])/g, (_, letter) => letter.toUpperCase());

  console.log(`Generating DSL command: ${name}`);
  console.log(`Category: ${category}`);
  console.log(`Properties:`, properties);

  // Generate TypeScript interface
  const typeDefinition = generateTypeDefinition(name, pascalName, properties);
  console.log('\n📝 Generated Type Definition:');
  console.log(typeDefinition);

  // Generate parser rule
  const parserRule = generateParserRule(name, camelName, properties);
  console.log('\n🔍 Generated Parser Rule:');
  console.log(parserRule);

  // Generate runtime component
  const runtimeComponent = generateRuntimeComponent(name, pascalName, category, properties);
  console.log('\n⚙️ Generated Runtime Component:');
  console.log(runtimeComponent);

  // Generate test template
  const testTemplate = generateTestTemplate(name, pascalName, properties);
  console.log('\n🧪 Generated Test Template:');
  console.log(testTemplate);

  return {
    typeDefinition,
    parserRule,
    runtimeComponent,
    testTemplate
  };
}

function generateTypeDefinition(name, pascalName, properties) {
  const propDefinitions = properties.map(prop => {
    const [propName, propType, defaultValue] = prop.split(':');
    // Make optional only if it has a default value
    const optional = defaultValue !== undefined ? '?' : '';
    return `  ${propName}${optional}: ${propType};`;
  }).join('\n');

  return `export interface ${pascalName}Command {
  type: '${name}';
${propDefinitions}
}`;
}

function generateParserRule(name, camelName, properties) {
  const pascalName = name.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase()).replace(/\s+/g, '');
  const paramPattern = properties.length > 0
    ? properties.map(prop => {
        const [propName] = prop.split(':')[0];
        return `${propName}:${propName}`;
      }).join(' ')
    : '';

  return `${pascalName}Command
  = "${name}" ${paramPattern} properties:Properties? {
    return {
      type: "${name}",
      ${paramPattern ? `...parseParams(${paramPattern}),` : ''}
      ...properties?.parse() || {}
    };
  }`;
}

function generateRuntimeComponent(name, pascalName, category, properties) {
  const componentName = `Fable${pascalName}`;

  return `'use client'

import { memo } from 'react';

export interface ${componentName}Props {
  ${properties.map(prop => {
    const [propName, propType, defaultValue] = prop.split(':');
    const optional = defaultValue ? '?' : '';
    return `${propName}${optional}: ${propType};`;
  }).join('\n  ')}
}

export const ${componentName} = memo(function ${componentName}({
  ${properties.map(prop => {
    const [propName] = prop.split(':');
    return propName;
  }).join(', ')}
}: ${componentName}Props) {
  // TODO: Implement ${name} ${category} logic
  console.log('${name} command executed:', { ${properties.map(prop => {
    const [propName] = prop.split(':');
    return propName;
  }).join(', ')} });

  return null; // Placeholder - implement actual rendering
});`;
}

function generateTestTemplate(name, pascalName, properties) {
  const dslParams = properties.length > 0 ? ' ' + properties.map(prop => {
    const [propName, propType, defaultValue] = prop.split(':');
    return `${propName} ${defaultValue || 'value'}`;
  }).join(' ') : '';

  const astExpectations = properties.map(prop => {
    const [propName, propType, defaultValue] = prop.split(':');
    return `${propName}: ${defaultValue ? `'${defaultValue}'` : `'value'`}`;
  }).join(',\n      ');

  const commandProps = properties.map(prop => {
    const [propName, propType, defaultValue] = prop.split(':');
    return `${propName}: ${defaultValue ? `'${defaultValue}'` : `'test'`}`;
  }).join(',\n      ');

  return `import { ${pascalName}Command } from '../src/types';

describe('${pascalName}Command', () => {
  test('parses ${name} command correctly', () => {
    const dsl = '${name}${dslParams}';

    const ast = parseDSL(dsl);

    expect(ast).toMatchObject({
      type: '${name}',
      ${astExpectations}
    });
  });

  test('executes ${name} command in runtime', () => {
    const command: ${pascalName}Command = {
      type: '${name}',
      ${commandProps}
    };

    // TODO: Implement runtime execution test
    expect(command.type).toBe('${name}');
  });
});`;
}

// CLI interface
function main() {
  const args = process.argv.slice(2);

  if (args.length < 2) {
    console.log('Usage: node generate-command.js <command-name> <category> [properties...]');
    console.log('');
    console.log('Examples:');
    console.log('  node generate-command.js bounce animations duration:number:500 intensity:string:medium');
    console.log('  node generate-command.js fade_in animations duration:number:1000');
    console.log('  node generate-command.js button ui text:string position:array');
    process.exit(1);
  }

  const [commandName, category, ...properties] = args;

  const result = generateCommand({
    name: commandName,
    category,
    properties
  });

  console.log('\n✅ DSL Command generation complete!');
  console.log('Copy the generated code into the appropriate files:');
  console.log('1. Type definitions → packages/parser/src/types.d.ts');
  console.log('2. Parser rules → packages/parser/src/grammar/fable.ohm-bundle.d.ts');
  console.log('3. Runtime component → packages/runtime/src/components/');
  console.log('4. Tests → packages/*/tests/');
}

if (require.main === module) {
  main();
}

module.exports = { generateCommand };