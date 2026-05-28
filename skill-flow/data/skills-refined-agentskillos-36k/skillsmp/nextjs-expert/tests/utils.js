import { readdir, readFile, stat } from 'fs/promises';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

/**
 * Résout un chemin relatif à la racine du skill
 */
export function resolveRootPath(...segments) {
  return join(__dirname, '..', ...segments);
}

/**
 * Résout un chemin relatif au skill
 * - Fichiers racine (SKILL.md, etc.) → racine du skill
 * - Domaines/agents → dossier agents/
 */
export function resolvePath(...segments) {
  // Si pas de segments, retourne le dossier agents
  if (segments.length === 0) {
    return join(__dirname, '..', 'agents');
  }
  // Si le premier segment est un fichier racine connu, ne pas ajouter agents/
  const rootFiles = ['SKILL.md', 'orchestrator.md', 'package.json', 'CHANGELOG.md', 'README.md'];
  if (rootFiles.includes(segments[0])) {
    return join(__dirname, '..', ...segments);
  }
  return join(__dirname, '..', 'agents', ...segments);
}

/**
 * Vérifie si un fichier existe
 */
export async function fileExists(path) {
  try {
    await stat(path);
    return true;
  } catch {
    return false;
  }
}

/**
 * Lit le contenu d'un fichier
 */
export async function readFileContent(path) {
  try {
    return await readFile(path, 'utf-8');
  } catch {
    return null;
  }
}

/**
 * Liste les fichiers d'un répertoire
 */
export async function listFiles(dir) {
  try {
    return await readdir(dir);
  } catch {
    return [];
  }
}

/**
 * Extrait le frontmatter YAML d'un fichier markdown
 */
export function extractFrontmatter(content) {
  const match = content.match(/^---\n([\s\S]*?)\n---/);
  if (!match) return null;

  const yaml = match[1];
  const result = {};

  yaml.split('\n').forEach(line => {
    const [key, ...valueParts] = line.split(':');
    if (key && valueParts.length) {
      result[key.trim()] = valueParts.join(':').trim();
    }
  });

  return result;
}

/**
 * Compte le nombre total d'agents dans tous les domaines
 * @param {string} basePath - Chemin vers le dossier agents/
 * @param {string[]} domains - Liste des domaines
 */
export async function countTotalAgents(basePath, domains) {
  let total = 0;

  for (const domain of domains) {
    // basePath est déjà le dossier agents/, donc on ajoute juste le domaine
    const domainPath = join(basePath, domain);
    const files = await listFiles(domainPath);
    total += files.filter(f => f.endsWith('.md')).length;
  }

  return total;
}
