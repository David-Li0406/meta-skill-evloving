#!/usr/bin/env node

// Docker Build Analyzer
// Checks Dockerfile for common issues

const fs = require('fs');
const path = require('path');

function analyzeDockerfile(dockerfilePath) {
  const content = fs.readFileSync(dockerfilePath, 'utf8');
  const lines = content.split('\n');
  const issues = [];
  
  let foundCopyPackageJson = false;
  let foundRunNpmInstall = false;
  let copyBeforeRun = false;
  let foundWorkdir = false;
  
  lines.forEach((line, idx) => {
    const trimmed = line.trim();
    
    // Check for WORKDIR
    if (trimmed.match(/^WORKDIR/i)) {
      foundWorkdir = true;
    }
    
    // Check COPY package.json comes before RUN npm install
    if (trimmed.match(/^COPY.*package\.json/i)) {
      foundCopyPackageJson = true;
      if (!foundRunNpmInstall) copyBeforeRun = true;
    }
    
    if (trimmed.match(/^RUN.*(npm install|npm ci)/i)) {
      foundRunNpmInstall = true;
      if (!copyBeforeRun && foundCopyPackageJson) {
        issues.push({
          line: idx + 1,
          severity: 'error',
          message: 'RUN npm install before COPY package.json - will fail with ENOENT',
          fix: 'Move COPY package*.json ./ before RUN npm install'
        });
      }
    }
    
    // Check for missing WORKDIR
    if ((trimmed.match(/^COPY/i) || trimmed.match(/^RUN/i)) && !foundWorkdir) {
      if (!issues.some(i => i.message.includes('WORKDIR'))) {
        issues.push({
          line: idx + 1,
          severity: 'warning',
          message: 'No WORKDIR set - COPY/RUN paths may be ambiguous',
          fix: 'Add WORKDIR /app before COPY commands'
        });
      }
    }
    
    // Check for COPY . . before npm install (slow rebuilds)
    if (trimmed.match(/^COPY\s+\.\s+\./i) && !foundRunNpmInstall) {
      issues.push({
        line: idx + 1,
        severity: 'warning',
        message: 'COPY . . before dependencies - breaks layer caching',
        fix: 'Copy package*.json first, RUN npm install, then COPY . .'
      });
    }
    
    // Check for npm install instead of npm ci
    if (trimmed.match(/^RUN.*npm install(?!\s|$)/i) && !trimmed.includes('npm ci')) {
      issues.push({
        line: idx + 1,
        severity: 'info',
        message: 'Using "npm install" instead of "npm ci"',
        fix: 'Use "npm ci" for faster, reproducible installs in Docker'
      });
    }
  });
  
  // Check if package.json is copied at all before npm commands
  if (foundRunNpmInstall && !foundCopyPackageJson) {
    issues.push({
      line: 0,
      severity: 'error',
      message: 'RUN npm install/ci without COPY package.json',
      fix: 'Add COPY package*.json ./ before RUN npm ci'
    });
  }
  
  return {
    file: dockerfilePath,
    issues,
    summary: issues.length === 0 
      ? 'No common issues detected' 
      : `Found ${issues.length} potential issue(s)`
  };
}

// CLI usage
if (require.main === module) {
  const dockerfilePath = process.argv[2] || './Dockerfile';
  
  if (!fs.existsSync(dockerfilePath)) {
    console.error(`Error: File not found: ${dockerfilePath}`);
    process.exit(1);
  }
  
  const result = analyzeDockerfile(dockerfilePath);
  console.log(JSON.stringify(result, null, 2));
  
  // Exit with error code if critical issues found
  const hasErrors = result.issues.some(i => i.severity === 'error');
  process.exit(hasErrors ? 1 : 0);
}

module.exports = { analyzeDockerfile };
