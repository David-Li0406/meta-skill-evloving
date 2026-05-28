import { readFile, access } from 'node:fs/promises';
import { join } from 'node:path';

interface VerificationConfig {
  outDir: string;
  checks: {
    file: string;
    contains: string[];
  }[];
}

async function verify() {
  const args = process.argv.slice(2);
  const configPath = args[0] || 'ssg.verify.json';
  
  try {
    const configRaw = await readFile(configPath, 'utf-8');
    const config: VerificationConfig = JSON.parse(configRaw);
    
    for (const check of config.checks) {
      const filePath = join(config.outDir, check.file);
      
      try {
        await access(filePath);
      } catch {
        throw new Error(`Missing file: ${filePath}`);
      }
      
      const content = await readFile(filePath, 'utf-8');
      for (const expected of check.contains) {
        if (!content.includes(expected)) {
          throw new Error(`File ${filePath} does not contain expected string: "${expected}"`);
        }
      }
      console.log(`✅ Verified: ${check.file}`);
    }
    
    console.log('✨ All verifications passed!');
  } catch (error) {
    console.error('❌ Verification Failed:', error);
    process.exit(1);
  }
}

verify();
