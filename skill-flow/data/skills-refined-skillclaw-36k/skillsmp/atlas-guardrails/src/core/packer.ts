import fs from 'fs';
import path from 'path';
import { AtlasDatabase } from '../storage/db';

interface PackOptions {
  task: string;
  budget: number; // in characters approx
  mode: 'bugfix' | 'feature' | 'refactor';
}

export class AtlasPacker {
  private db: AtlasDatabase;
  private rootPath: string;

  constructor(rootPath: string) {
    this.rootPath = path.resolve(rootPath);
    this.db = new AtlasDatabase(path.join(this.rootPath, '.atlas', 'symbols.sqlite'));
  }

  pack(options: PackOptions) {
    const rawKeywords = options.task
      .toLowerCase()
      .split(/\s+/)
      .filter((w) => w.length >= 3);
    const keywords = new Set<string>();
    for (const kw of rawKeywords) {
      keywords.add(kw);
      // If word is long, add prefix (e.g. authentication -> auth)
      if (kw.length >= 6) {
        keywords.add(kw.substring(0, 4));
      }
    }
    const keywordList = Array.from(keywords);
    const db = this.db.getDb();

    const filesToInclude = new Set<string>();
    const fileReasons = new Map<string, string>();
    let seeds: any[] = [];

    if (keywordList.length > 0) {
      // 1. Search Symbols
      const symPlaceholders = keywordList.map(() => 's.name LIKE ?').join(' OR ');
      const symArgs = keywordList.map((k) => `%${k}%`);
      seeds = db
        .prepare(
          `
            SELECT s.*, f.path as file_path 
            FROM symbols s 
            JOIN files f ON s.file_id = f.id 
            WHERE ${symPlaceholders} 
            LIMIT 30
        `,
        )
        .all(...symArgs);

      for (const seed of seeds) {
        if (!filesToInclude.has(seed.file_path)) {
          filesToInclude.add(seed.file_path);
          fileReasons.set(seed.file_path, `Matched keyword in symbol: ${seed.name}`);
        }
      }

      // 2. Search File Paths
      const pathPlaceholders = keywordList.map(() => 'path LIKE ?').join(' OR ');
      const pathArgs = keywordList.map((k) => `%${k}%`);
      const pathMatches = db
        .prepare(
          `
            SELECT path FROM files WHERE ${pathPlaceholders} LIMIT 20
        `,
        )
        .all(...pathArgs) as any[];

      for (const match of pathMatches) {
        if (!filesToInclude.has(match.path)) {
          filesToInclude.add(match.path);
          fileReasons.set(match.path, `Matched keyword in file path`);
        }
      }
    }

    // 3. Simple Graph expansion (Dependencies)
    // Find what these files import
    const initialFiles = Array.from(filesToInclude);
    for (const filePath of initialFiles) {
      const fileRec = db.prepare('SELECT id FROM files WHERE path = ?').get(filePath) as any;
      if (fileRec) {
        const imports = db
          .prepare('SELECT imported_path FROM imports WHERE file_id = ?')
          .all(fileRec.id) as any[];
        for (const imp of imports) {
          // Try to resolve import to a file (naive resolution)
          // In a real system, we'd have a resolver. Here we just look for suffix match or exact match if local
          if (imp.imported_path.startsWith('.')) {
            // heuristic resolution
            // This is tricky without real resolution, so we might skip or just try to find if it exists in DB
            // For MVP, let's just search the DB for the partial path
          }
        }
      }
    }

    // 4. Construct Pack
    const selectedFiles: any[] = [];
    let currentSize = 0;

    for (const file of filesToInclude) {
      const fullPath = path.join(this.rootPath, file);
      if (fs.existsSync(fullPath)) {
        const content = fs.readFileSync(fullPath, 'utf-8');
        if (currentSize + content.length > options.budget) {
          break;
        }
        selectedFiles.push({
          path: file,
          reason: fileReasons.get(file),
          content: content,
        });
        currentSize += content.length;
      }
    }

    const pack = {
      task: options.task,
      created_at: new Date().toISOString(),
      files: selectedFiles,
      symbols: seeds.map((s) => ({
        name: s.name,
        kind: s.kind,
        file: s.file_path,
        signature: s.signature,
      })),
      stats: {
        total_files: selectedFiles.length,
        total_symbols: seeds.length,
        total_chars: currentSize,
        budget: options.budget,
      },
    };

    fs.writeFileSync(path.join(this.rootPath, 'pack.json'), JSON.stringify(pack, null, 2));
    return pack;
  }

  close() {
    this.db.close();
  }
}
