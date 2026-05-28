import { AtlasIndexer } from '../core/indexer';
import fs from 'fs';
import path from 'path';
import { AtlasDatabase } from '../storage/db';

describe('AtlasIndexer', () => {
  const testDir = path.join(__dirname, 'temp_indexer_test');

  beforeEach(() => {
    if (fs.existsSync(testDir)) {
      try {
        fs.rmSync(testDir, { recursive: true, force: true });
      } catch {
        /* ignore */
      }
    }

    fs.mkdirSync(testDir);

    fs.mkdirSync(path.join(testDir, 'src'));
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

  test('indexes a typescript file correctly', async () => {
    const fileContent = `
      export const myVar = 123;
      export function testFunc() {}
    `;
    fs.writeFileSync(path.join(testDir, 'src/test.ts'), fileContent);

    const indexer = new AtlasIndexer(testDir);
    await indexer.index();
    indexer.close();

    const db = new AtlasDatabase(path.join(testDir, '.atlas/symbols.sqlite'));
    const files = db.getDb().prepare('SELECT * FROM files').all() as any[];
    const symbols = db.getDb().prepare('SELECT * FROM symbols').all() as any[];
    db.close();

    expect(files).toHaveLength(1);
    expect(files[0].path).toBe(path.join('src', 'test.ts'));
    expect(files[0].language).toBe('typescript');

    expect(symbols).toHaveLength(4); // 2 exports + 2 specific kinds
    expect(symbols.some((s: any) => s.name === 'myVar')).toBe(true);
    expect(symbols.some((s: any) => s.name === 'testFunc')).toBe(true);
  });

  test('respects gitignore', async () => {
    fs.writeFileSync(path.join(testDir, '.gitignore'), 'ignored.ts');
    fs.writeFileSync(path.join(testDir, 'ignored.ts'), 'export const ignoreMe = 1;');
    fs.writeFileSync(path.join(testDir, 'included.ts'), 'export const includeMe = 1;');

    const indexer = new AtlasIndexer(testDir);
    await indexer.index();
    indexer.close();

    const db = new AtlasDatabase(path.join(testDir, '.atlas/symbols.sqlite'));
    const files = db.getDb().prepare('SELECT * FROM files').all() as any[];
    db.close();

    expect(files).toHaveLength(1);
    expect(files[0].path).toBe('included.ts');
  });

  test('generates manifests', async () => {
    fs.writeFileSync(path.join(testDir, 'src/test.ts'), 'export const foo = 1;');
    const indexer = new AtlasIndexer(testDir);
    await indexer.index();
    indexer.close();

    const manifestPath = path.join(testDir, '.atlas/repo_manifest.json');
    const apiPath = path.join(testDir, '.atlas/public_api.json');

    expect(fs.existsSync(manifestPath)).toBe(true);
    expect(fs.existsSync(apiPath)).toBe(true);

    const api = JSON.parse(fs.readFileSync(apiPath, 'utf-8'));
    expect(api).toHaveLength(2); // Export + Const
    expect(api[0].path).toBe(path.join('src', 'test.ts'));
  });
});
