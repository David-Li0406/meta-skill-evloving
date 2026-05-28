import { describe, it } from 'node:test';
import assert from 'node:assert';
import { SKILL_CONFIG } from './config.js';
import { resolvePath, fileExists, listFiles } from './utils.js';

describe('Domaines nextjs-expert', () => {

  describe('Existence des domaines', () => {
    for (const domain of SKILL_CONFIG.domains) {
      it(`Le domaine ${domain}/ existe`, async () => {
        const domainPath = resolvePath(domain);
        const exists = await fileExists(domainPath);
        assert.strictEqual(exists, true, `Le domaine ${domain}/ n'existe pas`);
      });
    }
  });

  describe('Agents par domaine', () => {
    for (const [domain, agents] of Object.entries(SKILL_CONFIG.expectedAgents)) {
      describe(`Domaine ${domain}/`, () => {
        for (const agent of agents) {
          it(`L'agent ${agent}.md existe`, async () => {
            const agentPath = resolvePath(domain, `${agent}.md`);
            const exists = await fileExists(agentPath);
            assert.strictEqual(exists, true, `L'agent ${domain}/${agent}.md n'existe pas`);
          });
        }

        it(`Contient exactement ${agents.length} agents`, async () => {
          const domainPath = resolvePath(domain);
          const files = await listFiles(domainPath);
          const mdFiles = files.filter(f => f.endsWith('.md'));
          assert.strictEqual(
            mdFiles.length,
            agents.length,
            `${domain}/ contient ${mdFiles.length} agents au lieu de ${agents.length}`
          );
        });
      });
    }
  });

  describe('Orchestrateurs', () => {
    for (const domain of SKILL_CONFIG.domains) {
      it(`${domain}/orchestrator.md existe`, async () => {
        const orchestratorPath = resolvePath(domain, 'orchestrator.md');
        const exists = await fileExists(orchestratorPath);
        assert.strictEqual(exists, true, `${domain}/orchestrator.md manquant`);
      });
    }
  });
});
