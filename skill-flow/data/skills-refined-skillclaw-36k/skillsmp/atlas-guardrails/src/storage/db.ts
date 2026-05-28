import Database from 'better-sqlite3';
import path from 'path';
import fs from 'fs';

export class AtlasDatabase {
  private db: Database.Database;

  constructor(storagePath: string) {
    const dir = path.dirname(storagePath);
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
    }
    this.db = new Database(storagePath);
    this.init();
  }

  private init() {
    this.db.exec(`
      CREATE TABLE IF NOT EXISTS files (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        path TEXT UNIQUE NOT NULL,
        language TEXT,
        hash TEXT,
        last_seen_commit TEXT
      );

      CREATE TABLE IF NOT EXISTS symbols (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        file_id INTEGER NOT NULL,
        kind TEXT NOT NULL, -- 'function', 'class', 'variable', 'export'
        name TEXT NOT NULL,
        signature TEXT,
        start_line INTEGER,
        end_line INTEGER,
        exported_bool INTEGER DEFAULT 0,
        FOREIGN KEY(file_id) REFERENCES files(id) ON DELETE CASCADE
      );

      CREATE TABLE IF NOT EXISTS refs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        from_symbol_id INTEGER,
        to_symbol_id INTEGER,
        file_id INTEGER NOT NULL,
        kind TEXT, -- 'call', 'import'
        line INTEGER,
        FOREIGN KEY(file_id) REFERENCES files(id) ON DELETE CASCADE
      );
      
      CREATE TABLE IF NOT EXISTS imports (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        file_id INTEGER NOT NULL,
        imported_path TEXT NOT NULL,
        resolved_file_id INTEGER,
        FOREIGN KEY(file_id) REFERENCES files(id) ON DELETE CASCADE
      );
    `);
  }

  getDb() {
    return this.db;
  }

  close() {
    this.db.close();
  }
}
