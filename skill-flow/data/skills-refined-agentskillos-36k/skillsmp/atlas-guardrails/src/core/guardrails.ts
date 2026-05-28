import path from 'path';
import { AtlasDatabase } from '../storage/db';
import fs from 'fs';

export class AtlasGuardrails {
  private db: AtlasDatabase;
  private rootPath: string;

  constructor(rootPath: string) {
    this.rootPath = path.resolve(rootPath);
    this.db = new AtlasDatabase(path.join(this.rootPath, '.atlas', 'symbols.sqlite'));
  }

  findDuplicates(intent: string) {
    const db = this.db.getDb();

    let candidates: any[] = [];
    if (intent) {
      // Split intent into keywords for broader search
      const rawKeywords = intent
        .toLowerCase()
        .split(/\s+/)
        .filter((k) => k.length > 2);
      const keywords = new Set<string>();
      for (const kw of rawKeywords) {
        keywords.add(kw);
        if (kw.length >= 6) {
          keywords.add(kw.substring(0, 4));
        }
      }
      const keywordList = Array.from(keywords);

      if (keywordList.length > 0) {
        const placeholders = keywordList.map(() => 's.name LIKE ?').join(' OR ');
        const params = keywordList.map((k) => `%${k}%`);
        candidates = db
          .prepare(
            `
                SELECT s.name, s.kind, f.path, s.signature
                FROM symbols s
                JOIN files f ON s.file_id = f.id
                WHERE ${placeholders}
                LIMIT 20
            `,
          )
          .all(...params);
      } else {
        // fallback to original behavior if no keywords
        candidates = db
          .prepare(
            `
                SELECT s.name, s.kind, f.path, s.signature
                FROM symbols s
                JOIN files f ON s.file_id = f.id
                WHERE s.name LIKE ?
                LIMIT 20
            `,
          )
          .all(`%${intent}%`);
      }
    } else {
      // Fallback: Find actual duplicates (exact name matches in different files)
      candidates = db
        .prepare(
          `
            SELECT name, kind, COUNT(*) as count, GROUP_CONCAT(f.path) as files 
            FROM symbols s 
            JOIN files f ON s.file_id = f.id 
            GROUP BY name, kind 
            HAVING count > 1
        `,
        )
        .all();
    }

    return candidates;
  }

  async checkDrift() {
    // 1. Check Index Staleness
    // We compare the hash of current files vs DB files
    // A full check is expensive, so we might just check if any file modification time > index time
    // But since we want to be robust, let's just check a few random files or the manifest timestamp.

    // Better: Check if .atlas/repo_manifest.json mtime is older than git HEAD commit time?
    // Or just re-hash a sample.

    // For MVP: Check if file count in DB matches glob count roughly, or just pass if 'atlas index' was run recently.
    // Let's implement a 'stale' check by iterating files and checking hashes again? No, too slow.

    // Let's check public API drift.
    // Load old public_api.json
    const oldApiFile = path.join(this.rootPath, '.atlas', 'public_api.json');
    if (!fs.existsSync(oldApiFile)) {
      return { status: 'fail', reason: 'No public API manifest found. Run atlas index.' };
    }

    // This is a simplified check. A real one would diff the generated API vs the stored one.
    // Here we assume 'atlas index' has NOT been run yet if we are checking for drift relative to committed code?
    // Actually, 'atlas check' usually runs *after* indexing in CI.
    // If we assume index is up to date, drift check is "Did the API change vs the 'approved' API?"

    // Let's assume there is an 'approved_api.json' committed in the repo.
    const approvedApiFile = path.join(this.rootPath, 'approved_api.json');
    if (fs.existsSync(approvedApiFile)) {
      const approved = fs.readFileSync(approvedApiFile, 'utf-8');
      const current = fs.readFileSync(oldApiFile, 'utf-8');
      if (approved !== current) {
        return { status: 'fail', reason: 'Public API has drifted from approved_api.json' };
      }
    }

    return { status: 'pass' };
  }

  close() {
    this.db.close();
  }
}
