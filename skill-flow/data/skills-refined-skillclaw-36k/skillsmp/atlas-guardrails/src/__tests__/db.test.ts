import { AtlasDatabase } from '../storage/db';
import fs from 'fs';
import path from 'path';

describe('AtlasDatabase', () => {
  const dbPath = path.join(__dirname, 'test.sqlite');

  afterEach(() => {
    if (fs.existsSync(dbPath)) {
      fs.unlinkSync(dbPath);
    }
  });

  test('initializes schema', () => {
    const db = new AtlasDatabase(dbPath);
    const tables = db.getDb().prepare("SELECT name FROM sqlite_master WHERE type='table'").all();
    const tableNames = tables.map((t: any) => t.name);

    expect(tableNames).toContain('files');
    expect(tableNames).toContain('symbols');
    expect(tableNames).toContain('refs');
    expect(tableNames).toContain('imports');

    db.close();
  });
});
