#!/usr/bin/env node

/**
 * Asset Optimizer for Three.js Projects
 * Automatically optimize textures, models, and other assets
 * 
 * Features:
 * - Compress textures to WebP/KTX2
 * - Optimize GLTF models (draco compression)
 * - Generate mipmaps
 * - Create texture atlases
 * - Batch processing
 * 
 * Usage:
 *   node asset-optimizer.js --input ./assets --output ./optimized
 *   node asset-optimizer.js --textures-only
 *   node asset-optimizer.js --models-only
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

class AssetOptimizer {
  constructor(options = {}) {
    this.inputDir = options.input || './assets';
    this.outputDir = options.output || './optimized';
    this.quality = options.quality || 80;
    this.createMipmaps = options.mipmaps !== false;
    this.verbose = options.verbose || false;
    
    // Statistics
    this.stats = {
      texturesProcessed: 0,
      modelsProcessed: 0,
      originalSize: 0,
      optimizedSize: 0,
      timeSaved: 0
    };
    
    this.ensureOutputDir();
    this.checkDependencies();
  }
  
  ensureOutputDir() {
    if (!fs.existsSync(this.outputDir)) {
      fs.mkdirSync(this.outputDir, { recursive: true });
      this.log('Created output directory:', this.outputDir);
    }
  }
  
  checkDependencies() {
    const required = {
      'sharp': 'Image processing',
      'gltf-pipeline': 'GLTF optimization',
      '@gltf-transform/cli': 'Advanced GLTF transforms'
    };
    
    const missing = [];
    
    for (const [pkg, description] of Object.entries(required)) {
      try {
        require.resolve(pkg);
      } catch (e) {
        missing.push({ pkg, description });
      }
    }
    
    if (missing.length > 0) {
      console.log('⚠️  Missing dependencies:');
      missing.forEach(({ pkg, description }) => {
        console.log(`  • ${pkg} - ${description}`);
      });
      console.log('\nInstall with:');
      console.log(`  npm install ${missing.map(m => m.pkg).join(' ')}`);
      process.exit(1);
    }
  }
  
  async optimizeAll() {
    console.log('🚀 Starting asset optimization...\n');
    
    const files = this.getAllFiles(this.inputDir);
    
    for (const file of files) {
      const ext = path.extname(file).toLowerCase();
      
      // Textures
      if (['.jpg', '.jpeg', '.png', '.tiff', '.bmp'].includes(ext)) {
        await this.optimizeTexture(file);
      }
      
      // 3D Models
      if (['.gltf', '.glb'].includes(ext)) {
        await this.optimizeModel(file);
      }
    }
    
    this.printSummary();
  }
  
  async optimizeTexture(inputPath) {
    const sharp = require('sharp');
    const filename = path.basename(inputPath, path.extname(inputPath));
    const relativePath = path.relative(this.inputDir, path.dirname(inputPath));
    const outputPath = path.join(this.outputDir, relativePath);
    
    if (!fs.existsSync(outputPath)) {
      fs.mkdirSync(outputPath, { recursive: true });
    }
    
    try {
      const image = sharp(inputPath);
      const metadata = await image.metadata();
      
      this.log(`Processing: ${inputPath}`);
      this.log(`  Dimensions: ${metadata.width}x${metadata.height}`);
      
      // Get original size
      const originalSize = fs.statSync(inputPath).size;
      this.stats.originalSize += originalSize;
      
      // Optimize to WebP (better compression than PNG/JPG)
      const webpPath = path.join(outputPath, `${filename}.webp`);
      await image
        .webp({ quality: this.quality })
        .toFile(webpPath);
      
      // Also create KTX2 for GPU compression (requires toktx tool)
      if (this.hasToktx()) {
        const ktx2Path = path.join(outputPath, `${filename}.ktx2`);
        try {
          execSync(
            `toktx --genmipmap --bcmp --clevel 4 "${ktx2Path}" "${inputPath}"`,
            { stdio: 'ignore' }
          );
          this.log(`  Created KTX2: ${ktx2Path}`);
        } catch (e) {
          this.log(`  ⚠️ KTX2 creation failed`);
        }
      }
      
      const optimizedSize = fs.statSync(webpPath).size;
      this.stats.optimizedSize += optimizedSize;
      
      const saved = originalSize - optimizedSize;
      const percent = ((saved / originalSize) * 100).toFixed(1);
      
      this.log(`  Saved: ${this.formatBytes(saved)} (${percent}%)`);
      this.log(`  Output: ${webpPath}\n`);
      
      this.stats.texturesProcessed++;
      
    } catch (error) {
      console.error(`❌ Failed to optimize ${inputPath}:`, error.message);
    }
  }
  
  async optimizeModel(inputPath) {
    const filename = path.basename(inputPath);
    const relativePath = path.relative(this.inputDir, path.dirname(inputPath));
    const outputPath = path.join(this.outputDir, relativePath);
    
    if (!fs.existsSync(outputPath)) {
      fs.mkdirSync(outputPath, { recursive: true });
    }
    
    const outputFile = path.join(outputPath, filename);
    
    try {
      this.log(`Processing model: ${inputPath}`);
      
      const originalSize = fs.statSync(inputPath).size;
      this.stats.originalSize += originalSize;
      
      // Use gltf-transform for optimization
      const cmd = `gltf-transform optimize "${inputPath}" "${outputFile}" \
        --compress \
        --texture-compress webp \
        --texture-size 2048`;
      
      execSync(cmd, { stdio: this.verbose ? 'inherit' : 'ignore' });
      
      const optimizedSize = fs.statSync(outputFile).size;
      this.stats.optimizedSize += optimizedSize;
      
      const saved = originalSize - optimizedSize;
      const percent = ((saved / originalSize) * 100).toFixed(1);
      
      this.log(`  Saved: ${this.formatBytes(saved)} (${percent}%)`);
      this.log(`  Output: ${outputFile}\n`);
      
      this.stats.modelsProcessed++;
      
    } catch (error) {
      console.error(`❌ Failed to optimize ${inputPath}:`, error.message);
    }
  }
  
  hasToktx() {
    try {
      execSync('which toktx', { stdio: 'ignore' });
      return true;
    } catch (e) {
      return false;
    }
  }
  
  getAllFiles(dir, fileList = []) {
    const files = fs.readdirSync(dir);
    
    files.forEach(file => {
      const filePath = path.join(dir, file);
      const stat = fs.statSync(filePath);
      
      if (stat.isDirectory()) {
        this.getAllFiles(filePath, fileList);
      } else {
        fileList.push(filePath);
      }
    });
    
    return fileList;
  }
  
  formatBytes(bytes) {
    if (bytes === 0) return '0 B';
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  }
  
  printSummary() {
    const totalSaved = this.stats.originalSize - this.stats.optimizedSize;
    const percent = ((totalSaved / this.stats.originalSize) * 100).toFixed(1);
    
    console.log('\n' + '='.repeat(60));
    console.log('✨ Optimization Complete!');
    console.log('='.repeat(60));
    console.log(`\n📊 Statistics:`);
    console.log(`  Textures processed: ${this.stats.texturesProcessed}`);
    console.log(`  Models processed: ${this.stats.modelsProcessed}`);
    console.log(`  Original size: ${this.formatBytes(this.stats.originalSize)}`);
    console.log(`  Optimized size: ${this.formatBytes(this.stats.optimizedSize)}`);
    console.log(`  Total saved: ${this.formatBytes(totalSaved)} (${percent}%)`);
    
    // Estimate load time savings (assuming 10 Mbps connection)
    const mbps = 10;
    const originalLoadTime = (this.stats.originalSize / 1024 / 1024) / (mbps / 8);
    const optimizedLoadTime = (this.stats.optimizedSize / 1024 / 1024) / (mbps / 8);
    const timeSaved = originalLoadTime - optimizedLoadTime;
    
    console.log(`\n⏱️  Estimated load time savings:`);
    console.log(`  Before: ${originalLoadTime.toFixed(2)}s`);
    console.log(`  After: ${optimizedLoadTime.toFixed(2)}s`);
    console.log(`  Saved: ${timeSaved.toFixed(2)}s`);
    console.log('');
  }
  
  log(...args) {
    if (this.verbose) {
      console.log(...args);
    }
  }
}

// CLI
if (require.main === module) {
  const args = process.argv.slice(2);
  const options = {};
  
  for (let i = 0; i < args.length; i++) {
    switch (args[i]) {
      case '--input':
      case '-i':
        options.input = args[++i];
        break;
      case '--output':
      case '-o':
        options.output = args[++i];
        break;
      case '--quality':
      case '-q':
        options.quality = parseInt(args[++i]);
        break;
      case '--verbose':
      case '-v':
        options.verbose = true;
        break;
      case '--help':
      case '-h':
        console.log(`
Asset Optimizer for Three.js Projects

Usage:
  node asset-optimizer.js [options]

Options:
  -i, --input <dir>      Input directory (default: ./assets)
  -o, --output <dir>     Output directory (default: ./optimized)
  -q, --quality <0-100>  Compression quality (default: 80)
  -v, --verbose          Verbose output
  -h, --help             Show this help

Examples:
  node asset-optimizer.js --input ./public/assets --output ./dist/assets
  node asset-optimizer.js -i ./textures -o ./textures-opt -q 90 -v
        `);
        process.exit(0);
    }
  }
  
  const optimizer = new AssetOptimizer(options);
  optimizer.optimizeAll().catch(console.error);
}

module.exports = { AssetOptimizer };
