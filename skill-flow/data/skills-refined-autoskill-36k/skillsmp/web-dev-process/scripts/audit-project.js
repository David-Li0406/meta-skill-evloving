#!/usr/bin/env node

/**
 * audit-project.js - Audit complet d'un projet
 *
 * Ce script effectue un audit complet du projet en vérifiant :
 * - La conformité au process
 * - La qualité du code
 * - La sécurité des dépendances
 * - La documentation
 *
 * Usage:
 *   node audit-project.js [options]
 *
 * Options:
 *   --json       Sortie au format JSON
 *   --ci         Mode CI (exit codes stricts)
 *   --no-deps    Ignorer l'audit des dépendances
 *   --verbose    Mode verbeux (affiche les erreurs de debug)
 *
 * Environment Variables:
 *   AUDIT_DEBUG=1           Enable debug output (same as --verbose)
 *   AUDIT_MAX_DEPTH=<n>     Maximum directory search depth (default: 5)
 */

import { existsSync, readFileSync, readdirSync, statSync } from 'node:fs';
import { join } from 'node:path';
import { execSync, spawnSync } from 'node:child_process';

// =============================================================================
// Configuration
// =============================================================================

/** Parse command line arguments early for configuration */
const ARGS = process.argv.slice(2);

/** Maximum depth for recursive directory search to prevent infinite loops */
const MAX_SEARCH_DEPTH = parseInt(process.env.AUDIT_MAX_DEPTH, 10) || 5;

/** Enable debug mode via environment variable or --verbose flag */
const DEBUG = process.env.AUDIT_DEBUG === '1' || ARGS.includes('--verbose');

const AUDIT_CHECKS = {
  process: {
    name: 'Conformité Process',
    weight: 30,
    checks: [
      { id: 'readme', name: 'README.md présent', file: 'README.md', required: true },
      { id: 'contributing', name: 'CONTRIBUTING.md présent', file: 'CONTRIBUTING.md', required: false },
      { id: 'changelog', name: 'CHANGELOG.md présent', file: 'CHANGELOG.md', required: false },
      { id: 'license', name: 'LICENSE présent', file: 'LICENSE', required: false },
      { id: 'gitignore', name: '.gitignore présent', file: '.gitignore', required: true },
      { id: 'editorconfig', name: '.editorconfig présent', file: '.editorconfig', required: false },
      { id: 'pr-template', name: 'Template PR présent', file: '.github/PULL_REQUEST_TEMPLATE.md', required: false },
    ],
  },
  quality: {
    name: 'Qualité du Code',
    weight: 30,
    checks: [
      { id: 'eslint', name: 'ESLint configuré', files: ['eslint.config.js', '.eslintrc.js', '.eslintrc.json'] },
      { id: 'prettier', name: 'Prettier configuré', files: ['.prettierrc', '.prettierrc.json', 'prettier.config.js'] },
      { id: 'typescript', name: 'TypeScript configuré', files: ['tsconfig.json'] },
      { id: 'hooks', name: 'Git hooks configurés', files: ['lefthook.yml', '.husky/pre-commit'] },
      { id: 'commitlint', name: 'Commitlint configuré', files: ['commitlint.config.js', '.commitlintrc.json'] },
    ],
  },
  testing: {
    name: 'Tests',
    weight: 20,
    checks: [
      { id: 'test-config', name: 'Framework de test configuré', files: ['vitest.config.ts', 'jest.config.js', 'playwright.config.ts'] },
      { id: 'test-script', name: 'Script test dans package.json', script: 'test' },
      { id: 'test-files', name: 'Fichiers de test présents', pattern: '**/*.{test,spec}.{js,ts,jsx,tsx}' },
    ],
  },
  documentation: {
    name: 'Documentation',
    weight: 10,
    checks: [
      { id: 'readme-content', name: 'README non vide', minLines: 10, file: 'README.md' },
      { id: 'api-docs', name: 'Documentation API', files: ['docs/api.md', 'API.md', 'openapi.yaml', 'swagger.json'] },
      { id: 'adr', name: 'Architecture Decision Records', dir: 'docs/adr' },
    ],
  },
  security: {
    name: 'Sécurité',
    weight: 10,
    checks: [
      { id: 'no-secrets', name: 'Pas de secrets commités', patterns: ['.env', '*.pem', '*.key'] },
      { id: 'security-policy', name: 'SECURITY.md présent', file: 'SECURITY.md' },
      { id: 'dependabot', name: 'Dependabot configuré', file: '.github/dependabot.yml' },
    ],
  },
};

// =============================================================================
// Helpers
// =============================================================================

const colors = {
  reset: '\x1b[0m',
  red: '\x1b[31m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  cyan: '\x1b[36m',
  gray: '\x1b[90m',
};

function checkFileExists(path) {
  return existsSync(join(process.cwd(), path));
}

function checkAnyFileExists(files) {
  return files.some(f => checkFileExists(f));
}

function checkDirExists(path) {
  const fullPath = join(process.cwd(), path);
  return existsSync(fullPath) && statSync(fullPath).isDirectory();
}

function getFileLineCount(path) {
  try {
    const content = readFileSync(join(process.cwd(), path), 'utf-8');
    return content.split('\n').length;
  } catch {
    return 0;
  }
}

function checkPackageScript(scriptName) {
  const pkgPath = join(process.cwd(), 'package.json');

  if (!existsSync(pkgPath)) {
    if (DEBUG) {
      console.error('[DEBUG] package.json not found');
    }
    return false;
  }

  try {
    const content = readFileSync(pkgPath, 'utf-8');
    const pkg = JSON.parse(content);
    return !!pkg.scripts?.[scriptName];
  } catch (err) {
    if (DEBUG) {
      console.error(`[DEBUG] Error parsing package.json:`, err.message);
    }
    return false;
  }
}

function findTestFiles() {
  const testPatterns = ['.test.', '.spec.', '__tests__'];
  let found = false;

  function searchDir(dir, depth = 0) {
    if (depth > MAX_SEARCH_DEPTH || found) return;

    try {
      const entries = readdirSync(dir);
      for (const entry of entries) {
        if (['node_modules', '.git', 'dist', 'build'].includes(entry)) continue;

        const fullPath = join(dir, entry);
        const stat = statSync(fullPath);

        if (stat.isDirectory()) {
          if (entry === '__tests__') {
            found = true;
            return;
          }
          searchDir(fullPath, depth + 1);
        } else if (testPatterns.some(p => entry.includes(p))) {
          found = true;
          return;
        }
      }
    } catch (err) {
      if (DEBUG) {
        console.error(`[DEBUG] Error reading directory ${dir}:`, err.message);
      }
    }
  }

  searchDir(process.cwd());
  return found;
}

function runNpmAudit() {
  try {
    execSync('npm audit --json 2>/dev/null', { stdio: 'pipe' });
    return { vulnerabilities: 0 };
  } catch (err) {
    try {
      const result = JSON.parse(err.stdout?.toString() || '{}');
      return {
        vulnerabilities: result.metadata?.vulnerabilities?.total || 0,
        high: result.metadata?.vulnerabilities?.high || 0,
        critical: result.metadata?.vulnerabilities?.critical || 0,
      };
    } catch {
      return { vulnerabilities: -1 }; // Unable to audit
    }
  }
}

// =============================================================================
// Audit Runner
// =============================================================================

function runCheck(check) {
  if (check.file) {
    if (check.minLines) {
      const lines = getFileLineCount(check.file);
      return lines >= check.minLines;
    }
    return checkFileExists(check.file);
  }

  if (check.files) {
    return checkAnyFileExists(check.files);
  }

  if (check.dir) {
    return checkDirExists(check.dir);
  }

  if (check.script) {
    return checkPackageScript(check.script);
  }

  if (check.pattern) {
    return findTestFiles();
  }

  if (check.patterns) {
    // Check that none of the patterns are tracked in git
    // Use spawnSync with array arguments to prevent command injection
    return !check.patterns.some(pattern => {
      try {
        const result = spawnSync('git', ['ls-files', '--', pattern], {
          stdio: 'pipe',
          encoding: 'utf-8',
        });
        // Returns true if files are tracked (output is non-empty)
        return result.stdout && result.stdout.trim().length > 0;
      } catch {
        return false;
      }
    });
  }

  return false;
}

function runCategoryAudit(category) {
  const results = {
    name: category.name,
    weight: category.weight,
    checks: [],
    passed: 0,
    failed: 0,
    score: 0,
  };

  for (const check of category.checks) {
    const passed = runCheck(check);
    results.checks.push({
      id: check.id,
      name: check.name,
      passed,
      required: check.required ?? false,
    });

    if (passed) {
      results.passed++;
    } else {
      results.failed++;
    }
  }

  results.score = Math.round((results.passed / category.checks.length) * 100);
  return results;
}

// =============================================================================
// Output
// =============================================================================

function printResults(auditResults, depAudit) {
  console.log('\n' + '═'.repeat(60));
  console.log('  📊 RAPPORT D\'AUDIT DU PROJET');
  console.log('═'.repeat(60) + '\n');

  let totalScore = 0;
  let totalWeight = 0;

  for (const category of auditResults) {
    const statusIcon = category.score >= 80 ? '🟢' : category.score >= 50 ? '🟡' : '🔴';
    console.log(`${statusIcon} ${category.name} (${category.score}%)`);
    console.log('─'.repeat(40));

    for (const check of category.checks) {
      const icon = check.passed ? `${colors.green}✓${colors.reset}` : `${colors.red}✗${colors.reset}`;
      const required = check.required ? `${colors.gray}(requis)${colors.reset}` : '';
      console.log(`   ${icon} ${check.name} ${required}`);
    }

    console.log('');
    totalScore += category.score * category.weight;
    totalWeight += category.weight;
  }

  // Audit des dépendances
  if (depAudit) {
    console.log('🔒 Sécurité des Dépendances');
    console.log('─'.repeat(40));

    if (depAudit.vulnerabilities === -1) {
      console.log(`   ${colors.yellow}⚠${colors.reset} Impossible d'auditer les dépendances`);
    } else if (depAudit.vulnerabilities === 0) {
      console.log(`   ${colors.green}✓${colors.reset} Aucune vulnérabilité détectée`);
    } else {
      console.log(`   ${colors.red}✗${colors.reset} ${depAudit.vulnerabilities} vulnérabilité(s)`);
      if (depAudit.critical > 0) {
        console.log(`     ${colors.red}• ${depAudit.critical} critique(s)${colors.reset}`);
      }
      if (depAudit.high > 0) {
        console.log(`     ${colors.yellow}• ${depAudit.high} haute(s)${colors.reset}`);
      }
    }
    console.log('');
  }

  // Score global
  const globalScore = Math.round(totalScore / totalWeight);
  const scoreColor = globalScore >= 80 ? colors.green : globalScore >= 50 ? colors.yellow : colors.red;

  console.log('═'.repeat(60));
  console.log(`\n  Score Global: ${scoreColor}${globalScore}%${colors.reset}\n`);

  // Recommandations
  const failedChecks = auditResults
    .flatMap(c => c.checks)
    .filter(c => !c.passed && c.required);

  if (failedChecks.length > 0) {
    console.log('📋 Actions Requises:');
    for (const check of failedChecks) {
      console.log(`   • ${check.name}`);
    }
    console.log('');
  }

  // Grade
  let grade;
  if (globalScore >= 90) grade = 'A';
  else if (globalScore >= 80) grade = 'B';
  else if (globalScore >= 70) grade = 'C';
  else if (globalScore >= 60) grade = 'D';
  else grade = 'F';

  console.log(`  Grade: ${scoreColor}${grade}${colors.reset}\n`);
  console.log('═'.repeat(60) + '\n');

  return globalScore;
}

function printJson(auditResults, depAudit, globalScore) {
  console.log(JSON.stringify({
    score: globalScore,
    categories: auditResults,
    dependencies: depAudit,
    timestamp: new Date().toISOString(),
  }, null, 2));
}

// =============================================================================
// Main
// =============================================================================

function main() {
  const jsonOutput = ARGS.includes('--json');
  const ciMode = ARGS.includes('--ci');
  const skipDeps = ARGS.includes('--no-deps');

  // Exécuter l'audit par catégorie
  const auditResults = Object.values(AUDIT_CHECKS).map(runCategoryAudit);

  // Audit des dépendances
  const depAudit = skipDeps ? null : runNpmAudit();

  // Calculer le score global
  let totalScore = 0;
  let totalWeight = 0;
  for (const category of auditResults) {
    totalScore += category.score * category.weight;
    totalWeight += category.weight;
  }
  const globalScore = Math.round(totalScore / totalWeight);

  // Affichage
  if (jsonOutput) {
    printJson(auditResults, depAudit, globalScore);
  } else {
    printResults(auditResults, depAudit);
  }

  // Exit code
  if (ciMode) {
    // En mode CI, échouer si score < 70 ou vulnérabilités critiques
    if (globalScore < 70) {
      process.exit(1);
    }
    if (depAudit?.critical > 0) {
      process.exit(2);
    }
  }

  process.exit(0);
}

main();
