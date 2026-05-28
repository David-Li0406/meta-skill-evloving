#!/usr/bin/env node

/**
 * init-project.js - Initialisation d'un projet selon le process
 *
 * Ce script configure un projet avec tous les standards du process
 * de développement web.
 *
 * Usage:
 *   node init-project.js [options]
 *
 * Options:
 *   --force      Écrase les fichiers existants
 *   --minimal    Installation minimale (essentiels uniquement)
 *   --skip-deps  Ne pas installer les dépendances
 */

import { existsSync, readFileSync, writeFileSync, mkdirSync, copyFileSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { execSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import * as readline from 'node:readline';

const __dirname = dirname(fileURLToPath(import.meta.url));
const SKILL_ROOT = join(__dirname, '..');

// =============================================================================
// Configuration
// =============================================================================

const CONFIGS_TO_COPY = [
  { src: 'configs/.prettierrc', dest: '.prettierrc' },
  { src: 'configs/.prettierignore', dest: '.prettierignore' },
  { src: 'configs/.editorconfig', dest: '.editorconfig' },
  { src: 'configs/eslint.config.js', dest: 'eslint.config.js' },
  { src: 'configs/commitlint.config.js', dest: 'commitlint.config.js' },
  { src: 'configs/lefthook.yml', dest: 'lefthook.yml' },
];

const TEMPLATES_TO_COPY = [
  { src: 'templates/CONTRIBUTING.md', dest: 'CONTRIBUTING.md' },
  { src: 'templates/CHANGELOG.md', dest: 'CHANGELOG.md' },
  { src: 'templates/PULL_REQUEST_TEMPLATE.md', dest: '.github/PULL_REQUEST_TEMPLATE.md' },
  { src: 'templates/ISSUE_TEMPLATE/bug_report.md', dest: '.github/ISSUE_TEMPLATE/bug_report.md' },
  { src: 'templates/ISSUE_TEMPLATE/feature_request.md', dest: '.github/ISSUE_TEMPLATE/feature_request.md' },
  { src: 'templates/ISSUE_TEMPLATE/task.md', dest: '.github/ISSUE_TEMPLATE/task.md' },
  { src: 'templates/ISSUE_TEMPLATE/config.yml', dest: '.github/ISSUE_TEMPLATE/config.yml' },
];

const DEV_DEPENDENCIES = [
  // Linting & Formatting
  'prettier',
  'eslint',
  '@eslint/js',
  'globals',
  // Commit linting
  '@commitlint/cli',
  '@commitlint/config-conventional',
  // Git hooks
  'lefthook',
];

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
};

function log(emoji, message) {
  console.log(`${emoji} ${message}`);
}

function success(message) {
  console.log(`${colors.green}✓${colors.reset} ${message}`);
}

function warn(message) {
  console.log(`${colors.yellow}⚠${colors.reset} ${message}`);
}

function error(message) {
  console.log(`${colors.red}✗${colors.reset} ${message}`);
}

function copyFile(src, dest, force = false) {
  const srcPath = join(SKILL_ROOT, src);
  const destPath = join(process.cwd(), dest);

  if (!existsSync(srcPath)) {
    warn(`Source non trouvée: ${src}`);
    return false;
  }

  if (existsSync(destPath) && !force) {
    warn(`Fichier existant ignoré: ${dest}`);
    return false;
  }

  // Créer le dossier parent si nécessaire
  const destDir = dirname(destPath);
  if (!existsSync(destDir)) {
    mkdirSync(destDir, { recursive: true });
  }

  copyFileSync(srcPath, destPath);
  success(`Copié: ${dest}`);
  return true;
}

function detectPackageManager() {
  if (existsSync(join(process.cwd(), 'pnpm-lock.yaml'))) return 'pnpm';
  if (existsSync(join(process.cwd(), 'yarn.lock'))) return 'yarn';
  if (existsSync(join(process.cwd(), 'bun.lockb'))) return 'bun';
  return 'npm';
}

function installDependencies(deps, pm) {
  const commands = {
    pnpm: `pnpm add -D ${deps.join(' ')}`,
    yarn: `yarn add -D ${deps.join(' ')}`,
    npm: `npm install -D ${deps.join(' ')}`,
    bun: `bun add -D ${deps.join(' ')}`,
  };

  log('📦', `Installation des dépendances avec ${pm}...`);

  try {
    execSync(commands[pm], { stdio: 'inherit', timeout: 300000 });
    success('Dépendances installées');
    return true;
  } catch (err) {
    error(`Échec de l'installation: ${err.message}`);
    console.log(`\nEssayez manuellement: ${commands[pm]}\n`);
    return false;
  }
}

function updatePackageJson() {
  const pkgPath = join(process.cwd(), 'package.json');

  if (!existsSync(pkgPath)) {
    warn('package.json non trouvé');
    return false;
  }

  const pkg = JSON.parse(readFileSync(pkgPath, 'utf-8'));

  // Ajouter les scripts manquants
  pkg.scripts = pkg.scripts || {};

  const scriptsToAdd = {
    lint: 'eslint .',
    'lint:fix': 'eslint . --fix',
    format: 'prettier --write .',
    'format:check': 'prettier --check .',
    prepare: 'lefthook install',
  };

  let added = 0;
  for (const [name, command] of Object.entries(scriptsToAdd)) {
    if (!pkg.scripts[name]) {
      pkg.scripts[name] = command;
      added++;
    }
  }

  if (added > 0) {
    writeFileSync(pkgPath, JSON.stringify(pkg, null, 2) + '\n');
    success(`${added} scripts ajoutés à package.json`);
  } else {
    log('ℹ️', 'Tous les scripts sont déjà présents');
  }

  return true;
}

function initGitHooks(pm) {
  log('🪝', 'Configuration des hooks Git...');

  try {
    const command = pm === 'npm' ? 'npx lefthook install' : `${pm} lefthook install`;
    execSync(command, { stdio: 'pipe' });
    success('Hooks Git configurés avec Lefthook');
    return true;
  } catch {
    warn('Impossible de configurer les hooks (lefthook non installé)');
    return false;
  }
}

// =============================================================================
// Main
// =============================================================================

async function main() {
  const args = process.argv.slice(2);
  const force = args.includes('--force');
  const minimal = args.includes('--minimal');
  const skipDeps = args.includes('--skip-deps');

  console.log('\n🚀 Initialisation du projet selon le process de développement\n');
  console.log(`📁 Dossier: ${process.cwd()}\n`);

  // Vérifier que c'est un projet npm
  if (!existsSync(join(process.cwd(), 'package.json'))) {
    error('package.json non trouvé. Initialisez d\'abord votre projet.');
    console.log('\n  npm init -y\n');
    process.exit(1);
  }

  // Détecter le package manager
  const pm = detectPackageManager();
  log('📦', `Package manager détecté: ${pm}`);

  // Étape 1: Copier les configurations
  console.log('\n📋 Copie des fichiers de configuration...\n');
  for (const file of CONFIGS_TO_COPY) {
    copyFile(file.src, file.dest, force);
  }

  // Étape 2: Copier les templates (sauf en mode minimal)
  if (!minimal) {
    console.log('\n📋 Copie des templates...\n');
    for (const file of TEMPLATES_TO_COPY) {
      copyFile(file.src, file.dest, force);
    }
  }

  // Étape 3: Mettre à jour package.json
  console.log('\n📝 Mise à jour de package.json...\n');
  updatePackageJson();

  // Étape 4: Installer les dépendances
  if (!skipDeps) {
    console.log('\n');
    installDependencies(DEV_DEPENDENCIES, pm);
  }

  // Étape 5: Configurer les hooks Git
  if (!skipDeps) {
    console.log('\n');
    initGitHooks(pm);
  }

  // Résumé
  console.log('\n' + '─'.repeat(50));
  console.log(`\n${colors.green}✅ Projet initialisé avec succès !${colors.reset}\n`);

  console.log('Prochaines étapes :');
  console.log('  1. Vérifiez les fichiers de configuration');
  console.log('  2. Adaptez eslint.config.js à votre stack');
  console.log('  3. Personnalisez les templates GitHub');
  console.log('  4. Lancez `node check-process.js` pour vérifier\n');
}

main().catch(console.error);
