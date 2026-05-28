import fs from 'fs';
import path from 'path';
import crypto from 'crypto';
import { glob } from 'glob';
import ignore from 'ignore';
import { AtlasDatabase } from '../storage/db';
import { SimpleParser } from './parser';

export class AtlasIndexer {
  private db: AtlasDatabase;
  private rootPath: string;

  constructor(rootPath: string) {
    this.rootPath = path.resolve(rootPath);
    this.db = new AtlasDatabase(path.join(this.rootPath, '.atlas', 'symbols.sqlite'));
  }

  async index() {
    console.log('Starting indexing...');
    const ig = ignore();
    const gitignorePath = path.join(this.rootPath, '.gitignore');
    if (fs.existsSync(gitignorePath)) {
      ig.add(fs.readFileSync(gitignorePath).toString());
    }
    ig.add('.atlas/**');
    ig.add('.git/**');
    ig.add('node_modules/**');
    ig.add('.gitignore');
    ig.add('.trunk/**');

    const files = await glob('**/*', {
      cwd: this.rootPath,
      nodir: true,
      dot: true,
      ignore: ['node_modules/**', '.git/**', '.atlas/**'],
    });

    const filteredFiles = files.filter((f) => !ig.ignores(f));

    const db = this.db.getDb();
    
    let totalFiles = 0;
    let totalSymbols = 0;
    let totalImports = 0;

    // Prepare statements
    const insertFile = db.prepare('INSERT OR REPLACE INTO files (path, language, hash, last_seen_commit) VALUES (?, ?, ?, ?)');
    const insertSymbol = db.prepare('INSERT INTO symbols (file_id, kind, name, signature, start_line, end_line, exported_bool) VALUES (?, ?, ?, ?, ?, ?, ?)');
    const insertImport = db.prepare('INSERT INTO imports (file_id, imported_path) VALUES (?, ?)');
    const deleteSymbols = db.prepare('DELETE FROM symbols WHERE file_id = ?');
    const deleteImports = db.prepare('DELETE FROM imports WHERE file_id = ?');
    const getFile = db.prepare('SELECT id, hash FROM files WHERE path = ?');

    db.transaction(() => {
      for (const file of filteredFiles) {
        const fullPath = path.join(this.rootPath, file);

        try {
          if (!fs.existsSync(fullPath)) continue;
          const stat = fs.statSync(fullPath);
          if (!stat.isFile()) continue;

          totalFiles++;
          const content = fs.readFileSync(fullPath, 'utf-8');
          const hash = crypto.createHash('md5').update(content).digest('hex');
          
          const existing = getFile.get(file) as { id: number, hash: string } | undefined;

          if (existing && existing.hash === hash) {
            continue; // Unchanged
          }

          const parseResult = SimpleParser.parse(file, content);
          
          let fileId = existing ? existing.id : undefined;

          if (existing) {
               // Update file hash
               db.prepare('UPDATE files SET hash = ?, last_seen_commit = ? WHERE id = ?').run(hash, 'HEAD', existing.id);
               deleteSymbols.run(existing.id);
               deleteImports.run(existing.id);
          } else {
               const res = insertFile.run(file, parseResult.language, hash, 'HEAD');
               fileId = res.lastInsertRowid as number;
          }

          // Insert Symbols
          for (const sym of parseResult.symbols) {
              totalSymbols++;
              insertSymbol.run(fileId, sym.kind, sym.name, sym.signature, sym.start_line, sym.end_line, sym.exported ? 1 : 0);
          }

          // Insert Imports
          for (const imp of parseResult.imports) {
              totalImports++;
              insertImport.run(fileId, imp.path);
          }
        } catch (e) {
          process.stderr.write(`Skipping file ${file}: ${(e as Error).message}
`);
        }
      }
    })();

    this.generateManifests();
    console.log(`Indexing complete. Found ${totalSymbols} symbols across ${totalFiles} files.`);
  }

  private generateManifests() {
    const db = this.db.getDb();

    // Public API
    const exports = db
      .prepare(
        'SELECT f.path, s.name, s.signature FROM symbols s JOIN files f ON s.file_id = f.id WHERE s.exported_bool = 1',
      )
      .all();
    fs.writeFileSync(
      path.join(this.rootPath, '.atlas', 'public_api.json'),
      JSON.stringify(exports, null, 2),
    );

    // Repo Manifest
    const fileStats = db
      .prepare('SELECT language, COUNT(*) as count FROM files GROUP BY language')
      .all();
    fs.writeFileSync(
      path.join(this.rootPath, '.atlas', 'repo_manifest.json'),
      JSON.stringify(
        {
          generated_at: new Date().toISOString(),
          stats: fileStats,
        },
        null,
        2,
      ),
    );
  }

  close() {
    this.db.close();
  }
}
