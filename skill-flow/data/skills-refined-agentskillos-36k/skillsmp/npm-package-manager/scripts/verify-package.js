#!/usr/bin/env node

/**
 * Verify Package Script for LucidData
 *
 * Checks if a package exists on npm registry before installation.
 *
 * Usage:
 *   node verify-package.js <package-name> [version]
 *
 * Examples:
 *   node verify-package.js date-fns
 *   node verify-package.js @prisma/client 6.20.0
 *   node verify-package.js react 19.0.0
 */

const https = require('https');

// Parse command line arguments
const args = process.argv.slice(2);

if (args.length === 0) {
  console.error('❌ Error: Package name is required');
  console.log('');
  console.log('Usage: node verify-package.js <package-name> [version]');
  console.log('');
  console.log('Examples:');
  console.log('  node verify-package.js date-fns');
  console.log('  node verify-package.js @prisma/client 6.20.0');
  process.exit(1);
}

const packageName = args[0];
const requestedVersion = args[1] || null;

// Encode package name for URL (handles scoped packages like @prisma/client)
const encodedPackageName = encodeURIComponent(packageName);

// Construct npm registry URL
const registryUrl = `https://registry.npmjs.org/${encodedPackageName}`;

console.log(`🔍 Checking npm registry for: ${packageName}`);
if (requestedVersion) {
  console.log(`   Requested version: ${requestedVersion}`);
}
console.log('');

/**
 * Fetch package information from npm registry
 */
function fetchPackageInfo() {
  return new Promise((resolve, reject) => {
    https.get(registryUrl, { timeout: 10000 }, (res) => {
      let data = '';

      // Handle non-200 status codes
      if (res.statusCode === 404) {
        reject(new Error('Package not found'));
        return;
      }

      if (res.statusCode !== 200) {
        reject(new Error(`HTTP ${res.statusCode}: ${res.statusMessage}`));
        return;
      }

      // Collect data chunks
      res.on('data', (chunk) => {
        data += chunk;
      });

      // Parse response when complete
      res.on('end', () => {
        try {
          const packageInfo = JSON.parse(data);
          resolve(packageInfo);
        } catch (error) {
          reject(new Error('Failed to parse registry response'));
        }
      });
    })
    .on('error', (error) => {
      reject(error);
    })
    .on('timeout', () => {
      reject(new Error('Request timed out'));
    });
  });
}

/**
 * Main execution
 */
async function main() {
  try {
    const packageInfo = await fetchPackageInfo();

    // Extract key information
    const latestVersion = packageInfo['dist-tags']?.latest || 'unknown';
    const description = packageInfo.description || 'No description available';
    const license = packageInfo.license || 'Unknown license';
    const homepage = packageInfo.homepage || packageInfo.repository?.url || 'No homepage';
    const versions = Object.keys(packageInfo.versions || {});

    // Check if requested version exists
    let versionExists = true;
    if (requestedVersion) {
      versionExists = versions.includes(requestedVersion);
    }

    // Display results
    console.log('✅ Package found on npm registry');
    console.log('');
    console.log(`📦 Package: ${packageName}`);
    console.log(`📝 Description: ${description}`);
    console.log(`📄 License: ${license}`);
    console.log(`🔗 Homepage: ${homepage}`);
    console.log('');
    console.log(`📌 Latest version: ${latestVersion}`);
    console.log(`📊 Total versions: ${versions.length}`);

    if (requestedVersion) {
      console.log('');
      if (versionExists) {
        console.log(`✅ Version ${requestedVersion} exists`);
      } else {
        console.log(`❌ Version ${requestedVersion} NOT FOUND`);
        console.log('');
        console.log('Available versions (recent):');
        const recentVersions = versions.slice(-10).reverse();
        recentVersions.forEach((v) => console.log(`   - ${v}`));
        process.exit(1);
      }
    } else {
      console.log('');
      console.log('Recent versions:');
      const recentVersions = versions.slice(-10).reverse();
      recentVersions.forEach((v) => console.log(`   - ${v}`));
    }

    // Output JSON for programmatic use
    if (process.env.JSON_OUTPUT === 'true') {
      console.log('');
      console.log('JSON Output:');
      console.log(JSON.stringify({
        exists: true,
        packageName,
        latestVersion,
        requestedVersion,
        versionExists: requestedVersion ? versionExists : null,
        totalVersions: versions.length,
        description,
        license,
        homepage,
      }, null, 2));
    }

    process.exit(0);

  } catch (error) {
    console.error('❌ Error:', error.message);
    console.log('');

    if (error.message === 'Package not found') {
      console.log(`Package "${packageName}" does not exist on npm registry.`);
      console.log('');
      console.log('Suggestions:');
      console.log('  - Check spelling of package name');
      console.log('  - Verify the package is published to npm (not a private package)');
      console.log('  - Search npm: https://www.npmjs.com/search?q=' + encodeURIComponent(packageName));
    } else if (error.message.includes('timeout')) {
      console.log('Request to npm registry timed out.');
      console.log('');
      console.log('Suggestions:');
      console.log('  - Check your internet connection');
      console.log('  - Try again in a few moments');
      console.log('  - Verify npm registry is accessible: https://registry.npmjs.org/');
    } else {
      console.log('Failed to fetch package information from npm registry.');
      console.log('');
      console.log('Suggestions:');
      console.log('  - Check your internet connection');
      console.log('  - Verify npm registry is accessible');
      console.log('  - Try manually: npm view ' + packageName);
    }

    // Output JSON for programmatic use
    if (process.env.JSON_OUTPUT === 'true') {
      console.log('');
      console.log('JSON Output:');
      console.log(JSON.stringify({
        exists: false,
        packageName,
        error: error.message,
      }, null, 2));
    }

    process.exit(1);
  }
}

// Run main function
main();
