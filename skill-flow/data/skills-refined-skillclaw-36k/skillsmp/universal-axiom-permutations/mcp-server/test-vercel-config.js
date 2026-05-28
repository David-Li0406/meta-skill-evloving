#!/usr/bin/env node
/**
 * Test script to verify Vercel deployment configuration
 *
 * This validates:
 * - vercel.json configuration is valid
 * - API endpoint builds correctly
 * - No security vulnerabilities
 */

import { readFile } from 'fs/promises';
import { execSync } from 'child_process';

console.log('🧪 Testing Vercel Deployment Configuration\n');

// Test 1: Validate vercel.json
console.log('✓ Test 1: Validating vercel.json...');
try {
  const vercelConfig = JSON.parse(await readFile('./vercel.json', 'utf-8'));

  if (!vercelConfig.functions) {
    throw new Error('Missing functions configuration');
  }

  if (!vercelConfig.functions['api/**/*.ts']) {
    throw new Error('Missing API function configuration');
  }

  const runtime = vercelConfig.functions['api/**/*.ts'].runtime;
  if (!runtime.startsWith('@vercel/node@5')) {
    throw new Error(`Outdated runtime version: ${runtime}. Expected @vercel/node@5.x`);
  }

  console.log('  ✅ vercel.json is valid');
  console.log(`  ✅ Runtime: ${runtime}`);
} catch (error) {
  console.error('  ❌ Error:', error.message);
  process.exit(1);
}

// Test 2: Check package.json
console.log('\n✓ Test 2: Validating package.json...');
try {
  const pkg = JSON.parse(await readFile('./package.json', 'utf-8'));

  if (!pkg.optionalDependencies?.['@vercel/node']?.startsWith('^5')) {
    throw new Error('@vercel/node version should be ^5.x');
  }

  if (!pkg.optionalDependencies?.vercel?.startsWith('^50')) {
    throw new Error('vercel version should be ^50.x');
  }

  if (!pkg.overrides) {
    throw new Error('Missing overrides for security patches');
  }

  console.log('  ✅ Dependencies are up to date');
  console.log(`  ✅ @vercel/node: ${pkg.optionalDependencies['@vercel/node']}`);
  console.log(`  ✅ vercel: ${pkg.optionalDependencies.vercel}`);
  console.log('  ✅ Security overrides configured');
} catch (error) {
  console.error('  ❌ Error:', error.message);
  process.exit(1);
}

// Test 3: Check for vulnerabilities
console.log('\n✓ Test 3: Checking for security vulnerabilities...');
try {
  execSync('npm audit --audit-level=moderate', { stdio: 'pipe' });
  console.log('  ✅ No vulnerabilities found');
} catch (error) {
  console.error('  ❌ Vulnerabilities detected!');
  console.error(error.stdout?.toString() || error.message);
  process.exit(1);
}

// Test 4: Verify Vercel build compiles
console.log('\n✓ Test 4: Testing Vercel build...');
try {
  execSync('npm run build:vercel', { stdio: 'pipe' });
  console.log('  ✅ Vercel build successful');
} catch (error) {
  console.error('  ❌ Build failed');
  console.error(error.stdout?.toString() || error.message);
  process.exit(1);
}

// Test 5: Check build outputs exist
console.log('\n✓ Test 5: Verifying build outputs...');
try {
  const { statSync } = await import('fs');

  if (!statSync('dist/api/mcp.js').isFile()) {
    throw new Error('dist/api/mcp.js not found');
  }

  if (!statSync('build/mcp-server/index.js').isFile()) {
    throw new Error('build/mcp-server/index.js not found');
  }

  console.log('  ✅ dist/api/mcp.js exists');
  console.log('  ✅ build/mcp-server/index.js exists');
} catch (error) {
  console.error('  ❌ Error:', error.message);
  process.exit(1);
}

console.log('\n✅ All tests passed! Vercel deployment is ready.');
console.log('\nNext steps:');
console.log('  1. Deploy to preview: npm run deploy');
console.log('  2. Deploy to production: npm run deploy:prod');
