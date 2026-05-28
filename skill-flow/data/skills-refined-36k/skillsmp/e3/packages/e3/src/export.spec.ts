/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

import { describe, it, before, after } from 'node:test';
import * as assert from 'node:assert';
import * as fs from 'node:fs';
import * as os from 'node:os';
import * as path from 'node:path';
import yazl from 'yazl';
import yauzl from 'yauzl';
import { StringType, decodeBeast2For } from '@elaraai/east';
import { PackageObjectType } from '@elaraai/e3-types';
import { addObject, export_ } from './export.js';
import { package_ } from './package.js';
import { input } from './input.js';

describe('addObject', () => {
  it('returns correct SHA256 hash for empty buffer', () => {
    const zipfile = new yazl.ZipFile();
    const data = Buffer.from('');
    const hash = addObject(zipfile, data);
    // SHA256 of empty string
    assert.strictEqual(hash, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855');
  });

  it('returns correct SHA256 hash for known input', () => {
    const zipfile = new yazl.ZipFile();
    const data = Buffer.from('hello');
    const hash = addObject(zipfile, data);
    // SHA256 of "hello"
    assert.strictEqual(hash, '2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824');
  });

  it('adds object at correct path in zip', () => {
    const zipfile = new yazl.ZipFile();
    const data = Buffer.from('hello');
    const hash = addObject(zipfile, data);

    // Verify the path format: objects/xx/yyyy...beast2
    const expectedPath = `objects/${hash.slice(0, 2)}/${hash.slice(2)}.beast2`;
    assert.strictEqual(expectedPath, 'objects/2c/f24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824.beast2');
  });

  it('returns consistent hash for same input', () => {
    const zipfile1 = new yazl.ZipFile();
    const zipfile2 = new yazl.ZipFile();
    const data = Buffer.from('test data');

    const hash1 = addObject(zipfile1, data);
    const hash2 = addObject(zipfile2, data);

    assert.strictEqual(hash1, hash2);
  });

  it('returns different hash for different input', () => {
    const zipfile = new yazl.ZipFile();
    const data1 = Buffer.from('hello');
    const data2 = Buffer.from('world');

    const hash1 = addObject(zipfile, data1);
    const hash2 = addObject(zipfile, data2);

    assert.notStrictEqual(hash1, hash2);
  });
});

/**
 * Helper to read a zip file and return entries as a map of path -> buffer
 */
async function readZip(zipPath: string): Promise<Map<string, Buffer>> {
  return new Promise((resolve, reject) => {
    yauzl.open(zipPath, { lazyEntries: true }, (err, zipfile) => {
      if (err) return reject(err);
      if (!zipfile) return reject(new Error('No zipfile'));

      const entries = new Map<string, Buffer>();
      zipfile.readEntry();

      zipfile.on('entry', (entry) => {
        if (/\/$/.test(entry.fileName)) {
          // Directory entry, skip
          zipfile.readEntry();
        } else {
          zipfile.openReadStream(entry, (err, readStream) => {
            if (err) return reject(err);
            if (!readStream) return reject(new Error('No read stream'));

            const chunks: Buffer[] = [];
            readStream.on('data', (chunk) => chunks.push(chunk));
            readStream.on('end', () => {
              entries.set(entry.fileName, Buffer.concat(chunks));
              zipfile.readEntry();
            });
          });
        }
      });

      zipfile.on('end', () => resolve(entries));
      zipfile.on('error', reject);
    });
  });
}

describe('export_', () => {
  let tempDir: string;

  before(async () => {
    tempDir = await fs.promises.mkdtemp(path.join(os.tmpdir(), 'e3-export-test-'));
  });

  after(async () => {
    await fs.promises.rm(tempDir, { recursive: true });
  });

  it('exports empty package', async () => {
    const pkg = package_('empty-pkg', '1.0.0') as any;
    const zipPath = path.join(tempDir, 'empty.zip');

    await export_(pkg, zipPath);

    // Verify zip exists
    const stat = await fs.promises.stat(zipPath);
    assert.ok(stat.isFile());

    // Read zip contents
    const entries = await readZip(zipPath);

    // Should have package ref
    assert.ok(entries.has('packages/empty-pkg/1.0.0'));

    // Package ref should contain a hash
    const refContent = entries.get('packages/empty-pkg/1.0.0')!.toString().trim();
    assert.match(refContent, /^[a-f0-9]{64}$/);

    // Should have at least the package object and root tree
    const objectEntries = Array.from(entries.keys()).filter(k => k.startsWith('objects/'));
    assert.ok(objectEntries.length >= 2, `Expected at least 2 objects, got ${objectEntries.length}`);

    // Decode and verify package object
    const packageObjectPath = `objects/${refContent.slice(0, 2)}/${refContent.slice(2)}.beast2`;
    assert.ok(entries.has(packageObjectPath), `Missing package object at ${packageObjectPath}`);

    const packageObjectData = entries.get(packageObjectPath)!;
    const decoder = decodeBeast2For(PackageObjectType);
    const packageObject = decoder(packageObjectData);

    // Empty package should have no tasks
    assert.strictEqual(packageObject.tasks.size, 0);

    // Structure should be an empty struct
    assert.strictEqual(packageObject.data.structure.type, 'struct');
    assert.strictEqual(packageObject.data.structure.value.size, 0);
  });

  it('exports package with input dataset', async () => {
    const myInput = input('greeting', StringType, 'hello');
    const pkg = package_('input-pkg', '1.0.0', myInput);
    const zipPath = path.join(tempDir, 'input.zip');

    await export_(pkg, zipPath);

    // Read zip contents
    const entries = await readZip(zipPath);

    // Get package object
    const refContent = entries.get('packages/input-pkg/1.0.0')!.toString().trim();
    const packageObjectPath = `objects/${refContent.slice(0, 2)}/${refContent.slice(2)}.beast2`;
    const packageObjectData = entries.get(packageObjectPath)!;
    const decoder = decodeBeast2For(PackageObjectType);
    const packageObject = decoder(packageObjectData);

    // Should have no tasks (input only)
    assert.strictEqual(packageObject.tasks.size, 0);

    // Structure should have inputs.greeting as a value
    assert.strictEqual(packageObject.data.structure.type, 'struct');
    const inputs = packageObject.data.structure.value.get('inputs');
    assert.ok(inputs, 'Missing inputs in structure');
    assert.strictEqual(inputs.type, 'struct');
    const greeting = inputs.value.get('greeting');
    assert.ok(greeting, 'Missing greeting in inputs structure');
    assert.strictEqual(greeting.type, 'value');
    // The value should be a String type
    assert.strictEqual(greeting.value.type, 'String');
  });

  it('produces identical output for same package', async () => {
    const myInput = input('name', StringType, 'world');
    const pkg = package_('deterministic', '1.0.0', myInput);

    const zipPath1 = path.join(tempDir, 'deterministic1.zip');
    const zipPath2 = path.join(tempDir, 'deterministic2.zip');

    await export_(pkg, zipPath1);
    await export_(pkg, zipPath2);

    // Read both zips
    const entries1 = await readZip(zipPath1);
    const entries2 = await readZip(zipPath2);

    // Should have same entries
    assert.deepStrictEqual(
      Array.from(entries1.keys()).sort(),
      Array.from(entries2.keys()).sort()
    );

    // Each entry should have identical content
    for (const [path, data1] of entries1) {
      const data2 = entries2.get(path)!;
      assert.ok(data1.equals(data2), `Content mismatch at ${path}`);
    }
  });
});
