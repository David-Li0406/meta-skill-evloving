#!/usr/bin/env node
/**
 * Store admin/deployer private key on floppy disk
 *
 * Usage:
 *   ADMIN_PRIVATE_KEY="0x..." FLOPPY_KEYSTORE_PASSWORD="password" node store-admin-key.js
 */

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const CONFIG = require('./config');

async function storeAdminKey() {
  console.log('='.repeat(50));
  console.log('Store Admin Private Key on Floppy');
  console.log('='.repeat(50));

  // Get private key from environment
  const privateKey = process.env.ADMIN_PRIVATE_KEY;
  if (!privateKey) {
    console.error('Error: ADMIN_PRIVATE_KEY environment variable not set');
    console.error('Usage: ADMIN_PRIVATE_KEY="0x..." FLOPPY_KEYSTORE_PASSWORD="..." node store-admin-key.js');
    process.exit(1);
  }

  // Validate private key format
  if (!privateKey.match(/^0x[a-fA-F0-9]{64}$/)) {
    console.error('Error: Invalid private key format (expected 0x + 64 hex chars)');
    process.exit(1);
  }

  // Get password
  const password = process.env.FLOPPY_KEYSTORE_PASSWORD;
  if (!password) {
    console.error('Error: FLOPPY_KEYSTORE_PASSWORD environment variable not set');
    process.exit(1);
  }

  if (password.length < 8) {
    console.error('Error: Password must be at least 8 characters');
    process.exit(1);
  }

  // Check floppy mount
  const keystoreDir = path.join(CONFIG.MOUNT_POINT, CONFIG.KEYSTORE_DIR);
  if (!fs.existsSync(CONFIG.MOUNT_POINT)) {
    console.error(`Error: Floppy not mounted at ${CONFIG.MOUNT_POINT}`);
    console.error('Run mount script first');
    process.exit(1);
  }

  // Create keystore directory if needed
  if (!fs.existsSync(keystoreDir)) {
    fs.mkdirSync(keystoreDir, { recursive: true, mode: 0o700 });
    console.log('Created keystore directory:', keystoreDir);
  }

  // Generate encryption parameters
  const salt = crypto.randomBytes(32);
  const iv = crypto.randomBytes(16);

  // Use lower scrypt params for admin key (still secure, faster)
  const SCRYPT_N = CONFIG.ADMIN_SCRYPT_N;
  const SCRYPT_R = CONFIG.SCRYPT_R;
  const SCRYPT_P = CONFIG.SCRYPT_P;
  const SCRYPT_DKLEN = CONFIG.SCRYPT_DKLEN;

  // Derive key using scrypt
  console.log('\nDeriving encryption key...');
  const derivedKey = crypto.scryptSync(
    password,
    salt,
    SCRYPT_DKLEN,
    {
      N: SCRYPT_N,
      r: SCRYPT_R,
      p: SCRYPT_P
    }
  );

  // Encrypt private key (remove 0x prefix for storage)
  const privateKeyBytes = Buffer.from(privateKey.slice(2), 'hex');
  const cipher = crypto.createCipheriv(CONFIG.CIPHER, derivedKey.slice(0, 16), iv);
  const encrypted = Buffer.concat([
    cipher.update(privateKeyBytes),
    cipher.final()
  ]);

  // Create MAC for integrity verification (HMAC-SHA256)
  const mac = crypto.createHmac('sha256', derivedKey.slice(16, 32))
    .update(encrypted)
    .digest();

  // Derive address from private key
  let address;
  try {
    const { ethers } = require('ethers');
    const wallet = new ethers.Wallet(privateKey);
    address = wallet.address;
  } catch (err) {
    console.warn('Warning: Could not derive address (ethers not available)');
    address = 'unknown';
  }

  // Build keystore JSON
  const keystore = {
    version: 1,
    type: 'admin-private-key',
    address: address,
    crypto: {
      cipher: CONFIG.CIPHER,
      ciphertext: encrypted.toString('hex'),
      cipherparams: {
        iv: iv.toString('hex')
      },
      kdf: 'scrypt',
      kdfparams: {
        n: SCRYPT_N,
        r: SCRYPT_R,
        p: SCRYPT_P,
        dklen: SCRYPT_DKLEN,
        salt: salt.toString('hex')
      },
      mac: mac.toString('hex')
    },
    meta: {
      createdAt: new Date().toISOString(),
      description: 'Admin/Deployer private key'
    }
  };

  // Write keystore file
  const keystorePath = path.join(keystoreDir, CONFIG.ADMIN_KEYSTORE_FILENAME);
  fs.writeFileSync(keystorePath, JSON.stringify(keystore, null, 2));
  fs.chmodSync(keystorePath, 0o600);

  // Sync to disk
  const { execSync } = require('child_process');
  execSync('sync');

  console.log('\nAdmin key stored successfully!');
  console.log('Address:', address);
  console.log('Keystore path:', keystorePath);
  console.log('\nThe private key is now encrypted on the floppy disk.');
  console.log('Remember to unmount the floppy when done.');
}

storeAdminKey().catch(err => {
  console.error('Error:', err.message);
  process.exit(1);
});
