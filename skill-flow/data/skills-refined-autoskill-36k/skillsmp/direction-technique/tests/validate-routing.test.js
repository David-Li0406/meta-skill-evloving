#!/usr/bin/env node
/**
 * Test: Validate Routing Logic
 *
 * Validates that:
 * - All agents referenced in routing rules exist
 * - All orchestrators have valid routing tables
 * - Agent references in SKILL.md point to existing files
 *
 * @module tests/validate-routing
 */

const path = require('path');
const {
  safeReadFile,
  fileExists,
  directoryExists,
  findMarkdownFiles,
  TestReporter
} = require('./utils');
const { SKILL_ROOT, DOMAINS, EXPECTED_AGENTS_PER_DOMAIN } = require('./config');

const reporter = new TestReporter('validate-routing');
reporter.header('Validating Routing Logic');

// Build a map of all existing agents
const existingAgents = new Set();

for (const domain of DOMAINS) {
  const domainDir = path.join(SKILL_ROOT, 'agents', domain);
  if (directoryExists(domainDir)) {
    const files = findMarkdownFiles(domainDir);
    for (const file of files) {
      const agentName = path.basename(file, '.md');
      existingAgents.add(`${domain}/${agentName}`);
      existingAgents.add(agentName);
    }
  }
}

reporter.info(`Found ${existingAgents.size} agent references`);

// 1. Validate SKILL.md routing references
reporter.section('SKILL.md Agent References');
const skillMdPath = path.join(SKILL_ROOT, 'SKILL.md');
const { content: skillContent, error: skillError } = safeReadFile(skillMdPath);

if (skillError) {
  reporter.fail(`Cannot read SKILL.md: ${skillError}`, { path: skillMdPath });
} else if (skillContent) {
  const agentRefPattern = /`([a-z0-9-]+\/[a-z0-9-]+)`|`([a-z0-9-]+)`/g;
  const references = new Set();
  let match;

  while ((match = agentRefPattern.exec(skillContent)) !== null) {
    const ref = match[1] || match[2];
    if (ref && !ref.includes(' ') && ref.length > 2) {
      references.add(ref);
    }
  }

  let validRefs = 0;
  let invalidRefs = [];

  for (const ref of references) {
    if (ref.includes('/')) {
      const [domain, agent] = ref.split('/');
      if (DOMAINS.includes(domain)) {
        const agentPath = path.join(SKILL_ROOT, 'agents', domain, `${agent}.md`);
        if (fileExists(agentPath)) {
          validRefs++;
        } else {
          invalidRefs.push(ref);
        }
      }
    }
  }

  if (invalidRefs.length === 0) {
    reporter.pass('All domain/agent references valid', { validRefs });
  } else {
    reporter.fail(`Invalid references: ${invalidRefs.slice(0, 5).join(', ')}`, {
      invalid: invalidRefs
    });
  }
}

// 2. Validate orchestrator routing tables
reporter.section('Orchestrator Routing Tables');

for (const domain of DOMAINS) {
  const orchestratorPath = path.join(SKILL_ROOT, 'agents', domain, 'orchestrator.md');

  if (!fileExists(orchestratorPath)) {
    reporter.warn(`${domain}/orchestrator.md not found`);
    continue;
  }

  const { content, error } = safeReadFile(orchestratorPath);
  if (error) {
    reporter.fail(`${domain}/orchestrator.md: ${error}`, { domain, path: orchestratorPath });
    continue;
  }
  if (!content) continue;

  // Only check routing tables BEFORE the disambiguation or coordination sections
  // These sections reference other domains, not local agents
  const disambiguationIndex = content.indexOf('## Désambiguïsation');
  const coordinationIndex = content.indexOf('## Coordination');

  let endIndex = content.length;
  if (disambiguationIndex > 0) endIndex = Math.min(endIndex, disambiguationIndex);
  if (coordinationIndex > 0) endIndex = Math.min(endIndex, coordinationIndex);

  const routingContent = content.substring(0, endIndex);

  const tablePattern = /\|\s*`([a-z0-9-]+)`\s*\|/g;
  const referencedAgents = new Set();
  let tableMatch;

  while ((tableMatch = tablePattern.exec(routingContent)) !== null) {
    const agentName = tableMatch[1];
    if (agentName !== 'orchestrator') {
      referencedAgents.add(agentName);
    }
  }

  let missingAgents = [];

  for (const agentName of referencedAgents) {
    const agentPath = path.join(SKILL_ROOT, 'agents', domain, `${agentName}.md`);
    if (!fileExists(agentPath)) {
      missingAgents.push(agentName);
    }
  }

  if (missingAgents.length === 0) {
    reporter.pass(`${domain}/orchestrator.md - all references valid`, { domain });
  } else {
    reporter.fail(`${domain}/orchestrator.md - missing agents: ${missingAgents.join(', ')}`, {
      domain,
      missing: missingAgents
    });
  }
}

// 3. Validate cross-domain references
reporter.section('Cross-Domain References');

let crossDomainIssues = [];

for (const domain of DOMAINS) {
  const domainDir = path.join(SKILL_ROOT, 'agents', domain);
  if (!directoryExists(domainDir)) continue;

  const files = findMarkdownFiles(domainDir);

  for (const file of files) {
    const { content, error } = safeReadFile(file);
    if (error) {
      reporter.warn(`Cannot read ${path.relative(SKILL_ROOT, file)}: ${error}`);
      continue;
    }
    if (!content) continue;

    const crossRefPattern = /([a-z0-9-]+)\/([a-z0-9-]+)(?:\.md)?/g;
    let crossMatch;

    while ((crossMatch = crossRefPattern.exec(content)) !== null) {
      const [, refDomain, refAgent] = crossMatch;

      if (DOMAINS.includes(refDomain) && refDomain !== domain) {
        const targetPath = path.join(SKILL_ROOT, 'agents', refDomain, `${refAgent}.md`);
        if (!fileExists(targetPath) && refAgent !== 'orchestrator') {
          const expectedInDomain = EXPECTED_AGENTS_PER_DOMAIN[refDomain] || [];
          if (expectedInDomain.includes(refAgent)) {
            crossDomainIssues.push({
              from: path.relative(SKILL_ROOT, file),
              to: `${refDomain}/${refAgent}`
            });
          }
        }
      }
    }
  }
}

if (crossDomainIssues.length === 0) {
  reporter.pass('All cross-domain references valid');
} else {
  reporter.warn(`${crossDomainIssues.length} potential broken cross-references`);
}

reporter.summarize();
