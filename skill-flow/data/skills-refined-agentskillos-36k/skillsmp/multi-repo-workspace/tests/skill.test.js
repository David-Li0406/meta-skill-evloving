const fs = require('fs');
const path = require('path');

describe('Multi-Repo Workspace Skill', () => {
  describe('Configuration Files', () => {
    test('skill.md exists and is not empty', () => {
      const skillPath = path.join(__dirname, '..', 'skill.md');
      expect(fs.existsSync(skillPath)).toBe(true);
      const content = fs.readFileSync(skillPath, 'utf8');
      expect(content.length).toBeGreaterThan(0);
      expect(content).toContain('@workspace');
    });

    test('custom-instructions.md exists and is not empty', () => {
      const instructionsPath = path.join(__dirname, '..', 'custom-instructions.md');
      expect(fs.existsSync(instructionsPath)).toBe(true);
      const content = fs.readFileSync(instructionsPath, 'utf8');
      expect(content.length).toBeGreaterThan(0);
      expect(content).toContain('@workspace');
    });

    test('prompt.md exists and is not empty', () => {
      const promptPath = path.join(__dirname, '..', 'prompt.md');
      expect(fs.existsSync(promptPath)).toBe(true);
      const content = fs.readFileSync(promptPath, 'utf8');
      expect(content.length).toBeGreaterThan(0);
      expect(content).toContain('@workspace');
    });
  });

  describe('Templates', () => {
    test('config.json template exists and is valid JSON', () => {
      const templatePath = path.join(__dirname, '..', 'templates', '.claude', 'config.json');
      expect(fs.existsSync(templatePath)).toBe(true);
      const content = fs.readFileSync(templatePath, 'utf8');
      expect(() => JSON.parse(content)).not.toThrow();
      
      const config = JSON.parse(content);
      expect(config).toHaveProperty('repository');
      expect(config).toHaveProperty('development');
      expect(config).toHaveProperty('dependencies');
      expect(config).toHaveProperty('claude_preferences');
    });

    test('context.md template exists', () => {
      const templatePath = path.join(__dirname, '..', 'templates', '.claude', 'context.md');
      expect(fs.existsSync(templatePath)).toBe(true);
      const content = fs.readFileSync(templatePath, 'utf8');
      expect(content.length).toBeGreaterThan(0);
    });

    test('workspace config template exists and is valid JSON', () => {
      const templatePath = path.join(__dirname, '..', 'templates', '.workspace', 'config.json');
      expect(fs.existsSync(templatePath)).toBe(true);
      const content = fs.readFileSync(templatePath, 'utf8');
      expect(() => JSON.parse(content)).not.toThrow();
      
      const config = JSON.parse(content);
      expect(config).toHaveProperty('workspace');
      expect(config).toHaveProperty('repositories');
    });
  });

  describe('Examples', () => {
    test('monorepo example has valid configuration', () => {
      const configPath = path.join(__dirname, '..', 'examples', 'monorepo-example', '.workspace', 'config.json');
      expect(fs.existsSync(configPath)).toBe(true);
      const content = fs.readFileSync(configPath, 'utf8');
      expect(() => JSON.parse(content)).not.toThrow();
      
      const config = JSON.parse(content);
      expect(config.workspace.type).toBe('monorepo');
      expect(Array.isArray(config.repositories)).toBe(true);
      expect(config.repositories.length).toBeGreaterThan(0);
    });

    test('microservices example has valid configuration', () => {
      const configPath = path.join(__dirname, '..', 'examples', 'microservices-example', '.workspace', 'config.json');
      expect(fs.existsSync(configPath)).toBe(true);
      const content = fs.readFileSync(configPath, 'utf8');
      expect(() => JSON.parse(content)).not.toThrow();
      
      const config = JSON.parse(content);
      expect(config.workspace.type).toBe('microservices');
      expect(Array.isArray(config.repositories)).toBe(true);
      expect(config.repositories.length).toBeGreaterThan(0);
    });

    test('fullstack example has valid configuration', () => {
      const configPath = path.join(__dirname, '..', 'examples', 'fullstack-example', '.workspace', 'config.json');
      expect(fs.existsSync(configPath)).toBe(true);
      const content = fs.readFileSync(configPath, 'utf8');
      expect(() => JSON.parse(content)).not.toThrow();
      
      const config = JSON.parse(content);
      expect(config.workspace.type).toBe('fullstack');
      expect(Array.isArray(config.repositories)).toBe(true);
      expect(config.repositories.length).toBeGreaterThan(0);
    });
  });

  describe('Documentation', () => {
    test('setup-guide.md exists', () => {
      const guidePath = path.join(__dirname, '..', 'docs', 'setup-guide.md');
      expect(fs.existsSync(guidePath)).toBe(true);
      const content = fs.readFileSync(guidePath, 'utf8');
      expect(content).toContain('Setup Guide');
    });

    test('commands.md exists', () => {
      const commandsPath = path.join(__dirname, '..', 'docs', 'commands.md');
      expect(fs.existsSync(commandsPath)).toBe(true);
      const content = fs.readFileSync(commandsPath, 'utf8');
      expect(content).toContain('@workspace');
    });

    test('best-practices.md exists', () => {
      const practicesPath = path.join(__dirname, '..', 'docs', 'best-practices.md');
      expect(fs.existsSync(practicesPath)).toBe(true);
      const content = fs.readFileSync(practicesPath, 'utf8');
      expect(content).toContain('Best Practices');
    });
  });

  describe('Scripts', () => {
    test('auto-generate-config.js exists', () => {
      const scriptPath = path.join(__dirname, '..', 'scripts', 'auto-generate-config.js');
      expect(fs.existsSync(scriptPath)).toBe(true);
    });

    test('validate-workspace.js exists', () => {
      const scriptPath = path.join(__dirname, '..', 'scripts', 'validate-workspace.js');
      expect(fs.existsSync(scriptPath)).toBe(true);
    });
  });

  describe('Skill Commands', () => {
    test('skill.md contains all required commands', () => {
      const skillPath = path.join(__dirname, '..', 'skill.md');
      const content = fs.readFileSync(skillPath, 'utf8');
      
      expect(content).toContain('@workspace init');
      expect(content).toContain('@workspace add');
      expect(content).toContain('@workspace analyze');
      expect(content).toContain('@workspace focus');
      expect(content).toContain('@workspace task');
    });

    test('skill.md contains repository type detection', () => {
      const skillPath = path.join(__dirname, '..', 'skill.md');
      const content = fs.readFileSync(skillPath, 'utf8');
      
      expect(content).toContain('Frontend');
      expect(content).toContain('Backend');
      expect(content).toContain('Mobile');
      expect(content).toContain('DevOps');
      expect(content).toContain('Shared');
    });

    test('skill.md contains configuration structure', () => {
      const skillPath = path.join(__dirname, '..', 'skill.md');
      const content = fs.readFileSync(skillPath, 'utf8');
      
      expect(content).toContain('.claude/config.json');
      expect(content).toContain('.claude/context.md');
      expect(content).toContain('repository');
      expect(content).toContain('development');
      expect(content).toContain('dependencies');
      expect(content).toContain('claude_preferences');
    });
  });
});
