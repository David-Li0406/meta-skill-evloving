#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

class WorkspaceValidator {
  constructor(workspacePath) {
    this.workspacePath = workspacePath;
    this.errors = [];
    this.warnings = [];
    this.info = [];
  }

  validate() {
    console.log('🔍 Validating workspace...\n');
    
    this.validateWorkspaceConfig();
    this.validateRepositories();
    this.validateDependencies();
    
    this.printResults();
    
    return this.errors.length === 0;
  }

  validateWorkspaceConfig() {
    const configPath = path.join(this.workspacePath, '.workspace', 'config.json');
    
    if (!fs.existsSync(configPath)) {
      this.warnings.push('No workspace configuration found (.workspace/config.json)');
      return;
    }
    
    try {
      const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
      
      if (!config.workspace) {
        this.errors.push('Workspace config missing "workspace" section');
      }
      
      if (!config.repositories || !Array.isArray(config.repositories)) {
        this.errors.push('Workspace config missing "repositories" array');
      }
      
      this.info.push(`Found workspace: ${config.workspace?.name || 'unnamed'}`);
      this.info.push(`Repositories defined: ${config.repositories?.length || 0}`);
      
    } catch (error) {
      this.errors.push(`Invalid workspace config JSON: ${error.message}`);
    }
  }

  validateRepositories() {
    const configPath = path.join(this.workspacePath, '.workspace', 'config.json');
    
    if (!fs.existsSync(configPath)) {
      return;
    }
    
    const workspaceConfig = JSON.parse(fs.readFileSync(configPath, 'utf8'));
    const repos = workspaceConfig.repositories || [];
    
    repos.forEach(repo => {
      this.validateRepository(repo);
    });
  }

  validateRepository(repoConfig) {
    const repoPath = path.join(this.workspacePath, repoConfig.path);
    
    if (!fs.existsSync(repoPath)) {
      this.errors.push(`Repository path does not exist: ${repoConfig.path}`);
      return;
    }
    
    const claudeConfigPath = path.join(repoPath, '.claude', 'config.json');
    const claudeContextPath = path.join(repoPath, '.claude', 'context.md');
    
    if (!fs.existsSync(claudeConfigPath)) {
      this.warnings.push(`Missing .claude/config.json in ${repoConfig.name}`);
    } else {
      this.validateRepoConfig(repoConfig.name, claudeConfigPath);
    }
    
    if (!fs.existsSync(claudeContextPath)) {
      this.warnings.push(`Missing .claude/context.md in ${repoConfig.name}`);
    }
    
    this.info.push(`✓ Repository found: ${repoConfig.name} (${repoConfig.type})`);
  }

  validateRepoConfig(repoName, configPath) {
    try {
      const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
      
      if (!config.repository) {
        this.errors.push(`${repoName}: Missing "repository" section`);
      }
      
      if (!config.repository?.type) {
        this.warnings.push(`${repoName}: Missing repository type`);
      }
      
      if (!config.repository?.tech_stack || config.repository.tech_stack.length === 0) {
        this.warnings.push(`${repoName}: Missing tech stack`);
      }
      
      if (!config.development) {
        this.warnings.push(`${repoName}: Missing "development" section`);
      }
      
      if (!config.claude_preferences) {
        this.warnings.push(`${repoName}: Missing "claude_preferences" section`);
      }
      
    } catch (error) {
      this.errors.push(`${repoName}: Invalid config JSON - ${error.message}`);
    }
  }

  validateDependencies() {
    const configPath = path.join(this.workspacePath, '.workspace', 'config.json');
    
    if (!fs.existsSync(configPath)) {
      return;
    }
    
    const workspaceConfig = JSON.parse(fs.readFileSync(configPath, 'utf8'));
    const repos = workspaceConfig.repositories || [];
    const repoNames = new Set(repos.map(r => r.name));
    
    repos.forEach(repo => {
      const repoPath = path.join(this.workspacePath, repo.path);
      const claudeConfigPath = path.join(repoPath, '.claude', 'config.json');
      
      if (!fs.existsSync(claudeConfigPath)) {
        return;
      }
      
      const config = JSON.parse(fs.readFileSync(claudeConfigPath, 'utf8'));
      const internalDeps = config.dependencies?.internal || [];
      
      internalDeps.forEach(dep => {
        const depName = dep.replace('@workspace/', '');
        if (!repoNames.has(depName)) {
          this.warnings.push(`${repo.name}: References unknown internal dependency "${dep}"`);
        }
      });
    });
  }

  printResults() {
    console.log('\n' + '='.repeat(60));
    console.log('VALIDATION RESULTS');
    console.log('='.repeat(60) + '\n');
    
    if (this.info.length > 0) {
      console.log('ℹ️  INFO:');
      this.info.forEach(msg => console.log(`   ${msg}`));
      console.log('');
    }
    
    if (this.warnings.length > 0) {
      console.log('⚠️  WARNINGS:');
      this.warnings.forEach(msg => console.log(`   ${msg}`));
      console.log('');
    }
    
    if (this.errors.length > 0) {
      console.log('❌ ERRORS:');
      this.errors.forEach(msg => console.log(`   ${msg}`));
      console.log('');
    }
    
    console.log('='.repeat(60));
    
    if (this.errors.length === 0 && this.warnings.length === 0) {
      console.log('✅ Workspace validation passed!');
    } else if (this.errors.length === 0) {
      console.log('⚠️  Workspace validation passed with warnings');
    } else {
      console.log('❌ Workspace validation failed');
    }
    
    console.log('='.repeat(60) + '\n');
    
    console.log('Summary:');
    console.log(`  Errors: ${this.errors.length}`);
    console.log(`  Warnings: ${this.warnings.length}`);
    console.log(`  Info: ${this.info.length}`);
    console.log('');
  }
}

function main() {
  const args = process.argv.slice(2);
  const workspacePath = args[0] || process.cwd();
  
  if (!fs.existsSync(workspacePath)) {
    console.error(`Error: Workspace path does not exist: ${workspacePath}`);
    process.exit(1);
  }
  
  const validator = new WorkspaceValidator(workspacePath);
  const isValid = validator.validate();
  
  process.exit(isValid ? 0 : 1);
}

main();
