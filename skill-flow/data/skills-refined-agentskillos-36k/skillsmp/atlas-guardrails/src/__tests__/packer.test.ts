import { AtlasPacker } from '../core/packer';
import { AtlasIndexer } from '../core/indexer';
import fs from 'fs';
import path from 'path';

describe('AtlasPacker', () => {
  const testDir = path.join(__dirname, 'temp_packer_test');

  beforeEach(async () => {
    if (fs.existsSync(testDir)) {
      try {
        fs.rmSync(testDir, { recursive: true, force: true });
      } catch {
        /* ignore */
      }
    }

    fs.mkdirSync(testDir);

    // Setup repo
    fs.writeFileSync(path.join(testDir, 'utils.ts'), 'export function helper() { return "help"; }');
    fs.writeFileSync(
      path.join(testDir, 'main.ts'),
      'import { helper } from "./utils";\nexport class Main { run() { helper(); } }',
    );

    // Index it
    const indexer = new AtlasIndexer(testDir);
    await indexer.index();
    indexer.close();
  });

  afterEach(() => {
    if (fs.existsSync(testDir)) {
      try {
        fs.rmSync(testDir, { recursive: true, force: true });
      } catch {
        /* ignore */
      }
    }
  });

  test('packs relevant files based on keyword', () => {
    const packer = new AtlasPacker(testDir);
    const pack = packer.pack({ task: 'fix Main class', budget: 1000, mode: 'bugfix' });
    packer.close();

    expect(pack.files).toHaveLength(1); // Should find main.ts (class Main matched)
    expect(pack.files[0].path).toBe('main.ts');
  });

  test('respects budget', () => {
    const packer = new AtlasPacker(testDir);
    // Budget is small
    const pack = packer.pack({ task: 'fix Main', budget: 10, mode: 'bugfix' });
    packer.close();
    expect(pack.files).toHaveLength(0);
  });
});
