#!/usr/bin/env node

/**
 * check-process.js - Vérification de conformité au process
 *
 * Ce script vérifie qu'un projet respecte les standards du process
 * de développement web.
 *
 * Usage:
 *   node check-process.js [options]
 *
 * Options:
 *   --fix     Tente de corriger les problèmes automatiquement
 *   --strict  Mode strict (échoue sur les warnings)
 *   --quiet   Affiche uniquement les erreurs
 */

import { existsSync, readFileSync } from 'node:fs';
import { join } from 'node:path';
import { execSync } from 'node:child_process';

// =============================================================================
// Configuration
// =============================================================================

const REQUIRED_FILES = [
  { path: 'README.md', description: 'Documentation principale' },
  { path: 'package.json', description: 'Manifest du projet' },
  { path: '.gitignore', description: 'Fichiers ignorés par Git' },
];

const RECOMMENDED_FILES = [
  { path: '.prettierrc', description: 'Configuration Prettier' },
  { path: '.editorconfig', description: 'Configuration EditorConfig' },
  { path: 'eslint.config.js', description: 'Configuration ESLint', alternatives: ['.eslintrc.js', '.eslintrc.json', '.eslintrc.cjs'] },
  { path: 'tsconfig.json', description: 'Configuration TypeScript' },
  { path: 'CHANGELOG.md', description: 'Historique des versions' },
  { path: 'CONTRIBUTING.md', description: 'Guide de contribution' },
  { path: '.github/PULL_REQUEST_TEMPLATE.md', description: 'Template PR' },
];

const PACKAGE_JSON_CHECKS = [
  { field: 'name', required: true },
  { field: 'version', required: true },
  { field: 'description', required: false },
  { field: 'license', required: false },
  { field: 'scripts.lint', required: false, description: 'Script de linting' },
  { field: 'scripts.test', required: false, description: 'Script de tests' },
  { field: 'scripts.build', required: false, description: 'Script de build' },
];

/** Protected branch names that indicate main development branches */
const PROTECTED_BRANCHES = ['main', 'master', 'develop'];

// =============================================================================
// Helpers
// =============================================================================

const colors = {
  reset: '\x1b[0m',
  red: '\x1b[31m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  gray: '\x1b[90m',
};

const icons = {
  pass: `${colors.green}✓${colors.reset}`,
  fail: `${colors.red}✗${colors.reset}`,
  warn: `${colors.yellow}⚠${colors.reset}`,
  info: `${colors.blue}ℹ${colors.reset}`,
};

function log(icon, message, detail = '') {
  const detailStr = detail ? ` ${colors.gray}(${detail})${colors.reset}` : '';
  console.log(`  ${icon} ${message}${detailStr}`);
}

function getNestedValue(obj, path) {
  return path.split('.').reduce((acc, part) => acc?.[part], obj);
}

// =============================================================================
// Checks
// =============================================================================

function checkFiles(files, required = true) {
  const results = { passed: 0, failed: 0, warnings: 0 };

  for (const file of files) {
    const paths = [file.path, ...(file.alternatives || [])];
    const exists = paths.some(p => existsSync(join(process.cwd(), p)));

    if (exists) {
      log(icons.pass, file.description, file.path);
      results.passed++;
    } else if (required) {
      log(icons.fail, file.description, `${file.path} manquant`);
      results.failed++;
    } else {
      log(icons.warn, file.description, `${file.path} recommandé`);
      results.warnings++;
    }
  }

  return results;
}

function checkPackageJson() {
  const results = { passed: 0, failed: 0, warnings: 0 };
  const pkgPath = join(process.cwd(), 'package.json');

  if (!existsSync(pkgPath)) {
    log(icons.fail, 'package.json non trouvé');
    return { passed: 0, failed: 1, warnings: 0 };
  }

  const pkg = JSON.parse(readFileSync(pkgPath, 'utf-8'));

  for (const check of PACKAGE_JSON_CHECKS) {
    const value = getNestedValue(pkg, check.field);
    const description = check.description || check.field;

    if (value) {
      log(icons.pass, description, check.field);
      results.passed++;
    } else if (check.required) {
      log(icons.fail, description, `${check.field} manquant`);
      results.failed++;
    } else {
      log(icons.warn, description, `${check.field} recommandé`);
      results.warnings++;
    }
  }

  return results;
}

function checkGitHooks() {
  const results = { passed: 0, failed: 0, warnings: 0 };
  const hookManagers = [
    { path: 'lefthook.yml', name: 'Lefthook' },
    { path: '.husky', name: 'Husky' },
    { path: '.git/hooks/pre-commit', name: 'Git hooks natifs' },
  ];

  const hasHooks = hookManagers.some(h => existsSync(join(process.cwd(), h.path)));

  if (hasHooks) {
    const found = hookManagers.find(h => existsSync(join(process.cwd(), h.path)));
    log(icons.pass, 'Git hooks configurés', found.name);
    results.passed++;
  } else {
    log(icons.warn, 'Aucun gestionnaire de hooks Git détecté');
    results.warnings++;
  }

  return results;
}

function checkGitStatus() {
  const results = { passed: 0, failed: 0, warnings: 0 };

  try {
    // Vérifier si c'est un repo Git
    execSync('git rev-parse --git-dir', { stdio: 'pipe' });
    log(icons.pass, 'Repository Git initialisé');
    results.passed++;

    // Vérifier la branche principale
    const branch = execSync('git branch --show-current', { stdio: 'pipe' }).toString().trim();
    if (PROTECTED_BRANCHES.includes(branch)) {
      log(icons.info, `Branche actuelle: ${branch}`);
    }

    // Vérifier si remote configuré
    try {
      execSync('git remote get-url origin', { stdio: 'pipe' });
      log(icons.pass, 'Remote origin configuré');
      results.passed++;
    } catch {
      log(icons.warn, 'Aucun remote origin configuré');
      results.warnings++;
    }
  } catch {
    log(icons.warn, 'Pas un repository Git');
    results.warnings++;
  }

  return results;
}

// =============================================================================
// Main
// =============================================================================

function main() {
  const args = process.argv.slice(2);
  const strict = args.includes('--strict');
  const quiet = args.includes('--quiet');

  console.log('\n🔍 Vérification du process de développement\n');
  console.log(`📁 Dossier: ${process.cwd()}\n`);

  let totalPassed = 0;
  let totalFailed = 0;
  let totalWarnings = 0;

  // Section 1: Fichiers requis
  console.log('📋 Fichiers requis');
  const requiredResults = checkFiles(REQUIRED_FILES, true);
  totalPassed += requiredResults.passed;
  totalFailed += requiredResults.failed;

  // Section 2: Fichiers recommandés
  if (!quiet) {
    console.log('\n📋 Fichiers recommandés');
    const recommendedResults = checkFiles(RECOMMENDED_FILES, false);
    totalPassed += recommendedResults.passed;
    totalWarnings += recommendedResults.warnings;
  }

  // Section 3: package.json
  console.log('\n📦 Configuration package.json');
  const pkgResults = checkPackageJson();
  totalPassed += pkgResults.passed;
  totalFailed += pkgResults.failed;
  totalWarnings += pkgResults.warnings;

  // Section 4: Git hooks
  if (!quiet) {
    console.log('\n🪝 Git hooks');
    const hookResults = checkGitHooks();
    totalPassed += hookResults.passed;
    totalWarnings += hookResults.warnings;
  }

  // Section 5: Git status
  console.log('\n📊 Git repository');
  const gitResults = checkGitStatus();
  totalPassed += gitResults.passed;
  totalWarnings += gitResults.warnings;

  // Résumé
  console.log('\n' + '─'.repeat(50));
  console.log('\n📊 Résumé:');
  console.log(`   ${icons.pass} ${totalPassed} vérifications passées`);
  if (totalWarnings > 0) {
    console.log(`   ${icons.warn} ${totalWarnings} avertissements`);
  }
  if (totalFailed > 0) {
    console.log(`   ${icons.fail} ${totalFailed} erreurs`);
  }

  // Exit code
  if (totalFailed > 0) {
    console.log(`\n${colors.red}❌ Le projet ne respecte pas le process${colors.reset}\n`);
    process.exit(1);
  } else if (strict && totalWarnings > 0) {
    console.log(`\n${colors.yellow}⚠️  Mode strict: des améliorations sont recommandées${colors.reset}\n`);
    process.exit(1);
  } else {
    console.log(`\n${colors.green}✅ Le projet respecte le process${colors.reset}\n`);
    process.exit(0);
  }
}

main();
