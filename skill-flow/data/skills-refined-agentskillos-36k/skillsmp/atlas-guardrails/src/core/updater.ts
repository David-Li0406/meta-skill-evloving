import https from 'https';
import { execSync } from 'child_process';
import fs from 'fs';
import path from 'path';

const PACKAGE_NAME = 'atlas-guardrails';
const UPDATE_CHECK_INTERVAL = 24 * 60 * 60 * 1000; // 24 hours

export class AtlasUpdater {
  private static getCachePath(): string {
    const home = process.env.HOME || process.env.USERPROFILE || '.';
    const dir = path.join(home, '.atlas');
    if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
    return path.join(dir, 'last_update_check.json');
  }

  static async getLatestVersion(): Promise<string | null> {
    return new Promise((resolve) => {
      https
        .get(`https://registry.npmjs.org/${PACKAGE_NAME}/latest`, (res) => {
          let data = '';
          res.on('data', (chunk) => (data += chunk));
          res.on('end', () => {
            try {
              const json = JSON.parse(data);
              resolve(json.version);
            } catch {
              resolve(null);
            }
          });
        })
        .on('error', () => resolve(null));
    });
  }

  static shouldCheck(): boolean {
    const cachePath = this.getCachePath();
    if (!fs.existsSync(cachePath)) return true;
    try {
      const stats = fs.statSync(cachePath);
      return Date.now() - stats.mtimeMs > UPDATE_CHECK_INTERVAL;
    } catch {
      return true;
    }
  }

  static async checkForUpdates(currentVersion: string, silent = false) {
    if (silent && !this.shouldCheck()) return;

    const latest = await this.getLatestVersion();
    if (!latest) return;

    // Update timestamp
    fs.writeFileSync(this.getCachePath(), JSON.stringify({ lastCheck: Date.now() }));

    if (latest !== currentVersion) {
      if (silent) {
        process.stderr.write(
          `\n\x1b[33m[Atlas] A new version is available: ${latest} (Current: ${currentVersion})\x1b[0m\n`,
        );
        process.stderr.write(`\x1b[33mRun 'atlas update' to upgrade.\x1b[0m\n\n`);
      } else {
        console.log(`Updating Atlas from ${currentVersion} to ${latest}...`);
        this.performUpdate();
      }
    } else if (!silent) {
      console.log(`Atlas is already up to date (${currentVersion}).`);
    }
  }

  static performUpdate() {
    try {
      console.log('Running: npm install -g atlas-guardrails');
      execSync('npm install -g atlas-guardrails', { stdio: 'inherit' });
      console.log('\x1b[32mSuccessfully updated Atlas Guardrails!\x1b[0m');
    } catch (e) {
      console.error(
        '\x1b[31mUpdate failed. Please run "npm install -g atlas-guardrails" manually.\x1b[0m',
      );
      console.error((e as Error).message);
    }
  }
}
