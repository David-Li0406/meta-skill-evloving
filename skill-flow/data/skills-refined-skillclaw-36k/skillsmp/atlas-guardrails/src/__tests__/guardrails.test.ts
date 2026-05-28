import { AtlasGuardrails } from '../core/guardrails';
import { AtlasIndexer } from '../core/indexer';
import fs from 'fs';
import path from 'path';

describe('AtlasGuardrails', () => {
  const testDir = path.join(__dirname, 'temp_guard_test');

  beforeEach(async () => {
    if (fs.existsSync(testDir)) {
      try {
        fs.rmSync(testDir, { recursive: true, force: true });
      } catch {
        /* ignore */
      }
    }

    fs.mkdirSync(testDir);

    fs.mkdirSync(path.join(testDir, '.atlas'));
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

  test('finds duplicates (intent search)', async () => {
    fs.writeFileSync(path.join(testDir, 'foo.ts'), 'export class MyComponent {}');
    const indexer = new AtlasIndexer(testDir);
    await indexer.index();
    indexer.close();

    const guard = new AtlasGuardrails(testDir);
    const results = guard.findDuplicates('MyComponent');
    guard.close();

    expect(results).toHaveLength(2); // Export + Class
    expect(results[0].name).toBe('MyComponent');
  });

  test('finds duplicates fallback', async () => {
    // Create actual duplicates
    fs.writeFileSync(path.join(testDir, 'dup1.ts'), 'function duplicate() {}');
    fs.writeFileSync(path.join(testDir, 'dup2.ts'), 'function duplicate() {}');

    const indexer = new AtlasIndexer(testDir);
    await indexer.index();
    indexer.close();

    const guard = new AtlasGuardrails(testDir);
    const results = guard.findDuplicates(''); // No intent
    guard.close();

    expect(results.length).toBeGreaterThan(0);
    const dup = results.find((r: any) => r.name === 'duplicate');
    expect(dup).toBeDefined();
    expect(dup.count).toBe(2);
  });

  test('checks drift', async () => {
    // Mock approved API
    const approved = [{ path: 'foo.ts', name: 'Bar', signature: 'export class Bar' }];
    fs.writeFileSync(path.join(testDir, 'approved_api.json'), JSON.stringify(approved));

    // Mock current API (different)
    fs.writeFileSync(path.join(testDir, '.atlas/public_api.json'), JSON.stringify([]));

    const guard = new AtlasGuardrails(testDir);
    const result = await guard.checkDrift();
    guard.close();

    expect(result.status).toBe('fail');
  });
});
