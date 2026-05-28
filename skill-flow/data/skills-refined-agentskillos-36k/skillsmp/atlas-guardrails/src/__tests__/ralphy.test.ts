import { RalphyIntegration } from '../core/ralphy';
import fs from 'fs';
import path from 'path';

describe('RalphyIntegration', () => {
  const testDir = path.join(__dirname, 'temp_ralphy_test');

  beforeEach(() => {
    if (fs.existsSync(testDir)) {
      try {
        fs.rmSync(testDir, { recursive: true, force: true });
      } catch {
        /* ignore */
      }
    }

    fs.mkdirSync(testDir);
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

  test('generates config file', () => {
    RalphyIntegration.init(testDir);
    const configPath = path.join(testDir, '.ralphy/config.yaml');
    expect(fs.existsSync(configPath)).toBe(true);
    const content = fs.readFileSync(configPath, 'utf-8');
    expect(content).toContain('project:');
  });

  test('does not overwrite existing config', () => {
    fs.mkdirSync(path.join(testDir, '.ralphy'));
    const configPath = path.join(testDir, '.ralphy/config.yaml');
    fs.writeFileSync(configPath, 'original content');

    RalphyIntegration.init(testDir);
    const content = fs.readFileSync(configPath, 'utf-8');
    expect(content).toBe('original content');
  });
});
