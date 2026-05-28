#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

function detectRepositoryType(repoPath) {
  const packageJsonPath = path.join(repoPath, 'package.json');
  const requirementsPath = path.join(repoPath, 'requirements.txt');
  const goModPath = path.join(repoPath, 'go.mod');
  const cargoTomlPath = path.join(repoPath, 'Cargo.toml');
  
  if (fs.existsSync(packageJsonPath)) {
    const packageJson = JSON.parse(fs.readFileSync(packageJsonPath, 'utf8'));
    const deps = { ...packageJson.dependencies, ...packageJson.devDependencies };
    
    if (deps['react-native'] || deps['expo']) return 'mobile';
    if (deps['react'] || deps['vue'] || deps['@angular/core']) return 'frontend';
    if (deps['express'] || deps['fastify'] || deps['@nestjs/core']) return 'backend';
    if (packageJson.exports || packageJson.main) return 'shared';
  }
  
  if (fs.existsSync(requirementsPath)) return 'backend';
  if (fs.existsSync(goModPath)) return 'backend';
  if (fs.existsSync(cargoTomlPath)) return 'backend';
  
  if (fs.existsSync(path.join(repoPath, 'docker-compose.yml'))) return 'devops';
  if (fs.existsSync(path.join(repoPath, '.github', 'workflows'))) return 'devops';
  if (fs.existsSync(path.join(repoPath, 'terraform'))) return 'devops';
  
  return 'unknown';
}

function detectTechStack(repoPath) {
  const techStack = [];
  const packageJsonPath = path.join(repoPath, 'package.json');
  
  if (fs.existsSync(packageJsonPath)) {
    const packageJson = JSON.parse(fs.readFileSync(packageJsonPath, 'utf8'));
    const deps = { ...packageJson.dependencies, ...packageJson.devDependencies };
    
    if (deps['react']) techStack.push('react');
    if (deps['vue']) techStack.push('vue');
    if (deps['@angular/core']) techStack.push('angular');
    if (deps['typescript']) techStack.push('typescript');
    if (deps['express']) techStack.push('express');
    if (deps['fastify']) techStack.push('fastify');
    if (deps['@nestjs/core']) techStack.push('nestjs');
    if (deps['vite']) techStack.push('vite');
    if (deps['webpack']) techStack.push('webpack');
  }
  
  if (fs.existsSync(path.join(repoPath, 'requirements.txt'))) {
    techStack.push('python');
  }
  
  if (fs.existsSync(path.join(repoPath, 'go.mod'))) {
    techStack.push('go');
  }
  
  if (fs.existsSync(path.join(repoPath, 'Cargo.toml'))) {
    techStack.push('rust');
  }
  
  return techStack;
}

function detectCodeStyle(repoPath) {
  if (fs.existsSync(path.join(repoPath, '.eslintrc.json'))) {
    const eslintConfig = JSON.parse(fs.readFileSync(path.join(repoPath, '.eslintrc.json'), 'utf8'));
    if (eslintConfig.extends?.includes('airbnb')) return 'airbnb';
    if (eslintConfig.extends?.includes('google')) return 'google';
    if (eslintConfig.extends?.includes('standard')) return 'standard';
  }
  
  if (fs.existsSync(path.join(repoPath, '.prettierrc'))) return 'prettier';
  
  return 'standard';
}

function detectCommands(repoPath) {
  const packageJsonPath = path.join(repoPath, 'package.json');
  const commands = {};
  
  if (fs.existsSync(packageJsonPath)) {
    const packageJson = JSON.parse(fs.readFileSync(packageJsonPath, 'utf8'));
    const scripts = packageJson.scripts || {};
    
    if (scripts.dev || scripts.start) commands.dev = scripts.dev || scripts.start;
    if (scripts.build) commands.build = scripts.build;
    if (scripts.test) commands.test = scripts.test;
    if (scripts.lint) commands.lint = scripts.lint;
  }
  
  return commands;
}

function generateConfig(repoPath) {
  const repoName = path.basename(repoPath);
  const type = detectRepositoryType(repoPath);
  const techStack = detectTechStack(repoPath);
  const codeStyle = detectCodeStyle(repoPath);
  const commands = detectCommands(repoPath);
  
  const config = {
    repository: {
      name: repoName,
      type: type,
      description: `${repoName} repository`,
      tech_stack: techStack
    },
    development: {
      conventions: {
        code_style: codeStyle,
        naming: 'camelCase'
      },
      commands: commands
    },
    dependencies: {
      internal: [],
      external_critical: []
    },
    claude_preferences: {
      code_generation: {
        style: 'functional',
        testing: 'jest'
      },
      review_focus: ['performance', 'security']
    },
    metadata: {
      created: new Date().toISOString().split('T')[0],
      last_updated: new Date().toISOString().split('T')[0],
      version: '1.0.0',
      auto_generated: true
    }
  };
  
  return config;
}

function main() {
  const args = process.argv.slice(2);
  
  if (args.length === 0) {
    console.error('Usage: node auto-generate-config.js <repository-path>');
    process.exit(1);
  }
  
  const repoPath = path.resolve(args[0]);
  
  if (!fs.existsSync(repoPath)) {
    console.error(`Error: Repository path does not exist: ${repoPath}`);
    process.exit(1);
  }
  
  console.log(`Analyzing repository: ${repoPath}`);
  
  const config = generateConfig(repoPath);
  
  console.log('\nDetected configuration:');
  console.log(JSON.stringify(config, null, 2));
  
  const claudeDir = path.join(repoPath, '.claude');
  const configPath = path.join(claudeDir, 'config.json');
  
  if (!fs.existsSync(claudeDir)) {
    fs.mkdirSync(claudeDir, { recursive: true });
    console.log(`\nCreated directory: ${claudeDir}`);
  }
  
  if (fs.existsSync(configPath)) {
    console.log(`\nWarning: Configuration file already exists: ${configPath}`);
    console.log('Use --force to overwrite');
    
    if (!args.includes('--force')) {
      process.exit(0);
    }
  }
  
  fs.writeFileSync(configPath, JSON.stringify(config, null, 2));
  console.log(`\nConfiguration saved to: ${configPath}`);
  
  const contextPath = path.join(claudeDir, 'context.md');
  if (!fs.existsSync(contextPath)) {
    const contextTemplate = `# ${config.repository.name}

## Purpose

Brief description of what this repository does and why it exists.

## Architecture

### Tech Stack
${config.repository.tech_stack.map(tech => `- ${tech}`).join('\n')}

### Key Patterns
- Pattern 1: Description
- Pattern 2: Description

## Dependencies

### Internal Dependencies
- List internal workspace dependencies

### External Critical Dependencies
${config.repository.tech_stack.map(tech => `- ${tech}`).join('\n')}

## Development Guidelines

### Code Style
- Follow ${config.development.conventions.code_style} style guide

### Testing Strategy
- Unit tests: ${config.claude_preferences.code_generation.testing}
- Target coverage: 80%+

## Integration Points

### Consumes From
- List services/repos this depends on

### Provides To
- List services/repos that depend on this

## Known Issues & Technical Debt

- [ ] Issue 1: Description

## Recent Decisions

### [Date] - Decision Title
**Context**: Why this decision was needed
**Decision**: What was decided
**Consequences**: Impact on the codebase
`;
    
    fs.writeFileSync(contextPath, contextTemplate);
    console.log(`Context template saved to: ${contextPath}`);
  }
  
  console.log('\n✅ Configuration generated successfully!');
  console.log('\nNext steps:');
  console.log('1. Review and customize .claude/config.json');
  console.log('2. Fill out .claude/context.md with project details');
  console.log('3. Commit the configuration files');
}

main();
