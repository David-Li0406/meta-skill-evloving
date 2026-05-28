#!/usr/bin/env node

// Dependency Conflict Analyzer
// Checks package.json for compatibility issues

const fs = require('fs');
const path = require('path');

function analyzeDependencies(packageJsonPath) {
  const pkgJson = JSON.parse(fs.readFileSync(packageJsonPath, 'utf8'));
  const deps = { ...pkgJson.dependencies, ...pkgJson.devDependencies };
  const issues = [];
  
  // Check React ecosystem versions
  const reactVersion = deps['react'];
  const reactDomVersion = deps['react-dom'];
  const reactRouterVersion = deps['react-router-dom'];
  
  if (reactVersion && reactDomVersion) {
    const reactMajor = extractMajorVersion(reactVersion);
    const reactDomMajor = extractMajorVersion(reactDomVersion);
    
    if (reactMajor !== reactDomMajor) {
      issues.push({
        severity: 'error',
        package: 'react/react-dom',
        message: `Version mismatch: react@${reactVersion} but react-dom@${reactDomVersion}`,
        fix: 'Both packages must be on same major version',
        category: 'version-mismatch'
      });
    }
  }
  
  // Check React Router compatibility with React
  if (reactVersion && reactRouterVersion) {
    const reactMajor = extractMajorVersion(reactVersion);
    const routerMajor = extractMajorVersion(reactRouterVersion);
    
    if (routerMajor >= 6 && reactMajor < 18) {
      issues.push({
        severity: 'error',
        package: 'react-router-dom',
        message: `react-router-dom@${routerMajor} requires React 18+, but found React ${reactMajor}`,
        fix: 'Upgrade react and react-dom to ^18.0.0, or downgrade react-router-dom to ^5.3.0',
        category: 'peer-dependency'
      });
    }
  }
  
  // Check for caret vs exact versions (potential lock issues)
  const exactVersions = Object.entries(deps)
    .filter(([_, version]) => !version.match(/^[\^~]/))
    .map(([pkg]) => pkg);
  
  if (exactVersions.length > 3) {
    issues.push({
      severity: 'warning',
      package: exactVersions.join(', '),
      message: `${exactVersions.length} packages use exact versions (no ^ or ~)`,
      fix: 'Consider using ^ for minor version updates: "^1.2.3" allows 1.x.x updates',
      category: 'versioning-strategy'
    });
  }
  
  // Check for very old packages (security risk)
  const oldPackages = [];
  for (const [pkg, version] of Object.entries(deps)) {
    const major = extractMajorVersion(version);
    // Flag React < 17, Node packages with major version 0
    if ((pkg === 'react' && major < 17) || (major === 0 && !pkg.includes('eslint'))) {
      oldPackages.push(`${pkg}@${version}`);
    }
  }
  
  if (oldPackages.length > 0) {
    issues.push({
      severity: 'warning',
      package: oldPackages.join(', '),
      message: 'Old package versions detected (potential security/compatibility issues)',
      fix: 'Review changelogs and consider upgrading to latest stable versions',
      category: 'outdated'
    });
  }
  
  return {
    file: packageJsonPath,
    totalDependencies: Object.keys(deps).length,
    issues,
    summary: issues.length === 0 
      ? 'No obvious compatibility issues detected' 
      : `Found ${issues.length} potential issue(s)`
  };
}

function extractMajorVersion(versionString) {
  const match = versionString.match(/(\d+)\./);
  return match ? parseInt(match[1], 10) : 0;
}

// CLI usage
if (require.main === module) {
  const packageJsonPath = process.argv[2] || './package.json';
  
  if (!fs.existsSync(packageJsonPath)) {
    console.error(`Error: File not found: ${packageJsonPath}`);
    process.exit(1);
  }
  
  const result = analyzeDependencies(packageJsonPath);
  console.log(JSON.stringify(result, null, 2));
  
  // Exit with error code if critical issues found
  const hasErrors = result.issues.some(i => i.severity === 'error');
  process.exit(hasErrors ? 1 : 0);
}

module.exports = { analyzeDependencies };
