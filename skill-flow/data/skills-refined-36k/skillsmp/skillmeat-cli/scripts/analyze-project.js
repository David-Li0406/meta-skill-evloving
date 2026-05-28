#!/usr/bin/env node
/**
 * Project Analysis Script for SkillMeat CLI Skill
 *
 * Analyzes a project directory to recommend relevant artifacts.
 *
 * Usage:
 *   node analyze-project.js [project-path]
 *   node analyze-project.js .
 *
 * Output: JSON with project type, indicators found, and recommendations
 */

import { readFile, readdir, stat } from 'fs/promises';
import { join, basename } from 'path';

// Artifact recommendations by project indicator
const RECOMMENDATIONS = {
  react: {
    artifacts: ['frontend-design', 'webapp-testing'],
    description: 'React project detected',
  },
  nextjs: {
    artifacts: ['frontend-design', 'webapp-testing'],
    description: 'Next.js project detected',
  },
  python: {
    artifacts: [],
    description: 'Python project detected',
  },
  fastapi: {
    artifacts: ['openapi-expert'],
    description: 'FastAPI project detected',
  },
  typescript: {
    artifacts: [],
    description: 'TypeScript project detected',
  },
  documentation: {
    artifacts: ['pdf', 'docx', 'xlsx'],
    description: 'Documentation needs detected',
  },
};

// File indicators for project types
const INDICATORS = {
  'package.json': ['react', 'nextjs', 'typescript'],
  'pyproject.toml': ['python'],
  'requirements.txt': ['python'],
  'next.config.js': ['nextjs'],
  'next.config.ts': ['nextjs'],
  'next.config.mjs': ['nextjs'],
  'tsconfig.json': ['typescript'],
  'fastapi': ['fastapi'],
  '.claude': ['claude-code'],
};

async function fileExists(path) {
  try {
    await stat(path);
    return true;
  } catch {
    return false;
  }
}

async function detectProjectTypes(projectPath) {
  const detected = new Set();
  const indicators = [];

  // Check for indicator files
  for (const [file, types] of Object.entries(INDICATORS)) {
    const filePath = join(projectPath, file);
    if (await fileExists(filePath)) {
      indicators.push(file);
      types.forEach(t => detected.add(t));
    }
  }

  // Check package.json for specific dependencies
  const packageJsonPath = join(projectPath, 'package.json');
  if (await fileExists(packageJsonPath)) {
    try {
      const content = await readFile(packageJsonPath, 'utf-8');
      const pkg = JSON.parse(content);
      const deps = {
        ...pkg.dependencies,
        ...pkg.devDependencies,
      };

      if (deps.react || deps['react-dom']) {
        detected.add('react');
      }
      if (deps.next) {
        detected.add('nextjs');
      }
      if (deps.typescript) {
        detected.add('typescript');
      }
    } catch {
      // Ignore parse errors
    }
  }

  // Check pyproject.toml for FastAPI
  const pyprojectPath = join(projectPath, 'pyproject.toml');
  if (await fileExists(pyprojectPath)) {
    try {
      const content = await readFile(pyprojectPath, 'utf-8');
      if (content.includes('fastapi')) {
        detected.add('fastapi');
      }
    } catch {
      // Ignore read errors
    }
  }

  return {
    types: Array.from(detected),
    indicators,
  };
}

async function getDeployedArtifacts(projectPath) {
  const skillsPath = join(projectPath, '.claude', 'skills');
  const deployed = [];

  try {
    const entries = await readdir(skillsPath, { withFileTypes: true });
    for (const entry of entries) {
      if (entry.isDirectory()) {
        deployed.push(entry.name);
      }
    }
  } catch {
    // .claude/skills doesn't exist
  }

  return deployed;
}

async function analyzeProject(projectPath) {
  const { types, indicators } = await detectProjectTypes(projectPath);
  const deployed = await getDeployedArtifacts(projectPath);

  // Collect recommendations
  const recommendations = [];
  const seen = new Set(deployed);

  for (const type of types) {
    const rec = RECOMMENDATIONS[type];
    if (rec) {
      for (const artifact of rec.artifacts) {
        if (!seen.has(artifact)) {
          recommendations.push({
            artifact,
            reason: rec.description,
          });
          seen.add(artifact);
        }
      }
    }
  }

  return {
    projectPath,
    projectTypes: types,
    indicators,
    deployed,
    recommendations,
    summary: recommendations.length > 0
      ? `Found ${recommendations.length} artifact(s) that could help with this project`
      : 'No additional artifacts recommended',
  };
}

// Main execution
const projectPath = process.argv[2] || '.';

analyzeProject(projectPath)
  .then(result => {
    console.log(JSON.stringify(result, null, 2));
  })
  .catch(error => {
    console.error(JSON.stringify({
      error: error.message,
      projectPath,
    }));
    process.exit(1);
  });
