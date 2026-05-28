import { describe, it } from 'node:test';
import assert from 'node:assert';
import { SKILL_CONFIG } from './config.js';
import { resolvePath, readFileContent, extractFrontmatter } from './utils.js';

describe('Agents nextjs-expert', () => {

  describe('Frontmatter YAML', () => {
    for (const [domain, agents] of Object.entries(SKILL_CONFIG.expectedAgents)) {
      for (const agent of agents) {
        it(`${domain}/${agent}.md a un frontmatter valide`, async () => {
          const agentPath = resolvePath(domain, `${agent}.md`);
          const content = await readFileContent(agentPath);

          assert.ok(content, `Impossible de lire ${domain}/${agent}.md`);
          assert.ok(
            content.startsWith('---'),
            `${domain}/${agent}.md n'a pas de frontmatter YAML`
          );

          const frontmatter = extractFrontmatter(content);
          assert.ok(frontmatter, `Frontmatter invalide dans ${domain}/${agent}.md`);
          assert.ok(frontmatter.name, `Champ 'name' manquant dans ${domain}/${agent}.md`);
          assert.ok(frontmatter.description, `Champ 'description' manquant dans ${domain}/${agent}.md`);
        });
      }
    }
  });

  describe('Structure des agents', () => {
    for (const [domain, agents] of Object.entries(SKILL_CONFIG.expectedAgents)) {
      for (const agent of agents) {
        it(`${domain}/${agent}.md a la structure attendue`, async () => {
          const agentPath = resolvePath(domain, `${agent}.md`);
          const content = await readFileContent(agentPath);

          assert.ok(content, `Impossible de lire ${domain}/${agent}.md`);

          // Vérifier les sections clés
          assert.ok(
            content.includes('# '),
            `${domain}/${agent}.md n'a pas de titre H1`
          );

          // Les orchestrateurs ont une structure spécifique
          if (agent === 'orchestrator') {
            assert.ok(
              content.includes('Agents Disponibles') || content.includes('Arbre de Décision'),
              `${domain}/${agent}.md n'a pas de section de décision`
            );
          } else {
            // Les agents doivent avoir ces sections
            assert.ok(
              content.includes('## Ta Responsabilité Unique') ||
              content.includes('## Responsabilité'),
              `${domain}/${agent}.md n'a pas de section responsabilité`
            );
          }
        });
      }
    }
  });

  describe('Références croisées', () => {
    for (const [domain, agents] of Object.entries(SKILL_CONFIG.expectedAgents)) {
      for (const agent of agents) {
        if (agent !== 'orchestrator') {
          it(`${domain}/${agent}.md a une section Escalades`, async () => {
            const agentPath = resolvePath(domain, `${agent}.md`);
            const content = await readFileContent(agentPath);

            assert.ok(content, `Impossible de lire ${domain}/${agent}.md`);
            assert.ok(
              content.includes('## Escalades') || content.includes('Escalades'),
              `${domain}/${agent}.md n'a pas de section Escalades`
            );
          });
        }
      }
    }
  });
});
