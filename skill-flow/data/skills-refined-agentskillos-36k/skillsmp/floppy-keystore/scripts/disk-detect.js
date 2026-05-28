#!/usr/bin/env node
/**
 * Floppy Disk Detection and Password Resolution
 *
 * Reads the disk.name metadata from the inserted floppy and resolves
 * the correct password from environment variables.
 *
 * Usage:
 *   node disk-detect.js           # Show detected disk info
 *   node disk-detect.js --export  # Export for shell: eval $(node disk-detect.js --export)
 *   node disk-detect.js --json    # Output as JSON
 */

const fs = require('fs');
const path = require('path');

const MOUNT_POINT = process.env.FLOPPY_MOUNT || '/mnt/floppy';
const IDENTITY_DIR = path.join(MOUNT_POINT, '.keystore', 'identity');
const METADATA_FILE = path.join(IDENTITY_DIR, 'metadata.json');

function isMounted() {
  try {
    return fs.existsSync(MOUNT_POINT) && fs.readdirSync(MOUNT_POINT).length > 0;
  } catch {
    return false;
  }
}

function getDiskName() {
  if (!fs.existsSync(METADATA_FILE)) {
    return null;
  }
  try {
    const metadata = JSON.parse(fs.readFileSync(METADATA_FILE, 'utf8'));
    return metadata['disk.name'] || null;
  } catch {
    return null;
  }
}

function getDiskMetadata() {
  if (!fs.existsSync(METADATA_FILE)) {
    return {};
  }
  try {
    return JSON.parse(fs.readFileSync(METADATA_FILE, 'utf8'));
  } catch {
    return {};
  }
}

function getProfile() {
  const profileFile = path.join(IDENTITY_DIR, 'profile.json');
  if (!fs.existsSync(profileFile)) {
    return null;
  }
  try {
    return JSON.parse(fs.readFileSync(profileFile, 'utf8'));
  } catch {
    return null;
  }
}

function resolvePassword(diskName) {
  if (!diskName) return null;

  // Look for FLOPPY_<NAME>_PASSWORD in environment
  const envKey = `FLOPPY_${diskName.toUpperCase()}_PASSWORD`;
  return process.env[envKey] || null;
}

function main() {
  const args = process.argv.slice(2);
  const exportMode = args.includes('--export');
  const jsonMode = args.includes('--json');

  if (!isMounted()) {
    if (jsonMode) {
      console.log(JSON.stringify({ error: 'Floppy not mounted', mounted: false }));
    } else if (exportMode) {
      console.log('# Floppy not mounted');
      console.log('export FLOPPY_DETECTED=false');
    } else {
      console.log('❌ Floppy not mounted');
    }
    process.exit(1);
  }

  const diskName = getDiskName();
  const metadata = getDiskMetadata();
  const profile = getProfile();
  const password = resolvePassword(diskName);

  const result = {
    mounted: true,
    diskName: diskName,
    displayName: profile?.name || diskName || 'Unknown',
    network: metadata['disk.network'] || null,
    passwordFound: !!password,
    envVar: diskName ? `FLOPPY_${diskName.toUpperCase()}_PASSWORD` : null
  };

  if (jsonMode) {
    console.log(JSON.stringify(result, null, 2));
  } else if (exportMode) {
    console.log(`# Detected disk: ${result.displayName}`);
    console.log(`export FLOPPY_DETECTED=true`);
    console.log(`export FLOPPY_DISK_NAME="${diskName || ''}"`);
    console.log(`export FLOPPY_DISPLAY_NAME="${result.displayName}"`);
    if (password) {
      console.log(`export FLOPPY_KEYSTORE_PASSWORD="${password}"`);
    }
  } else {
    console.log('=== Detected Floppy Disk ===\n');
    console.log(`  Name:     ${result.displayName}`);
    console.log(`  ID:       ${diskName || '(not set)'}`);
    console.log(`  Network:  ${result.network || '(not set)'}`);
    console.log(`  Password: ${password ? '✅ Found in env' : '❌ Not found'}`);
    if (!password && diskName) {
      console.log(`\n  Set password in .env:`);
      console.log(`  ${result.envVar}=<password>`);
    }
  }
}

main();
