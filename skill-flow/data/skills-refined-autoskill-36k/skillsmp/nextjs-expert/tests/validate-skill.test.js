import { describe, it } from 'node:test';
import assert from 'node:assert';
import { SKILL_CONFIG } from './config.js';
import { resolvePath, fileExists, readFileContent, countTotalAgents } from './utils.js';

describe('Skill nextjs-expert', () => {

  describe('Fichiers racine', () => {
    for (const file of SKILL_CONFIG.requiredRootFiles) {
      it(`${file} existe`, async () => {
        const filePath = resolvePath(file);
        const exists = await fileExists(filePath);
        assert.strictEqual(exists, true, `${file} n'existe pas à la racine`);
      });
    }
  });

  describe('SKILL.md', () => {
    it('contient les informations du skill', async () => {
      const content = await readFileContent(resolvePath('SKILL.md'));

      assert.ok(content, 'SKILL.md est vide ou manquant');
      assert.ok(content.includes('# Next.js Expert'), 'Titre manquant');
      assert.ok(content.includes('## Domaines'), 'Section Domaines manquante');
    });

    it('liste tous les domaines', async () => {
      const content = await readFileContent(resolvePath('SKILL.md'));

      for (const domain of SKILL_CONFIG.domains) {
        assert.ok(
          content.includes(domain),
          `Domaine ${domain} non mentionné dans SKILL.md`
        );
      }
    });

    it('indique le bon nombre d\'agents', async () => {
      const content = await readFileContent(resolvePath('SKILL.md'));

      assert.ok(
        content.includes('35') || content.includes('35 agents'),
        `SKILL.md devrait mentionner ${SKILL_CONFIG.totalAgents} agents`
      );
    });
  });

  describe('orchestrator.md', () => {
    it('contient les informations de routage', async () => {
      const content = await readFileContent(resolvePath('orchestrator.md'));

      assert.ok(content, 'orchestrator.md est vide ou manquant');
      assert.ok(content.includes('# Next.js Expert'), 'Titre manquant');
      assert.ok(
        content.includes('Arbre de Décision') || content.includes('Domaines'),
        'Arbre de décision manquant'
      );
    });

    it('référence tous les domaines', async () => {
      const content = await readFileContent(resolvePath('orchestrator.md'));

      for (const domain of SKILL_CONFIG.domains) {
        assert.ok(
          content.includes(domain),
          `Domaine ${domain} non référencé dans orchestrator.md`
        );
      }
    });
  });

  describe('Comptage des agents', () => {
    it(`contient exactement ${SKILL_CONFIG.totalAgents} agents`, async () => {
      const basePath = resolvePath();
      const total = await countTotalAgents(basePath, SKILL_CONFIG.domains);

      assert.strictEqual(
        total,
        SKILL_CONFIG.totalAgents,
        `Nombre d'agents incorrect: ${total} au lieu de ${SKILL_CONFIG.totalAgents}`
      );
    });
  });
});
