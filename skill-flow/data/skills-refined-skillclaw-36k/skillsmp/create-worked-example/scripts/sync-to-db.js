// Sync HTML Slides to MongoDB
// Usage: node sync-to-db.js <slug>
// Automatically executes mongosh with DATABASE_URL from environment

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// Load environment variables from .env.local
const envPath = path.join(__dirname, '../../../../.env.local');
if (fs.existsSync(envPath)) {
  const envContent = fs.readFileSync(envPath, 'utf-8');
  envContent.split('\n').forEach(line => {
    const match = line.match(/^([^#=]+)=["']?(.+?)["']?$/);
    if (match && !process.env[match[1]]) {
      process.env[match[1]] = match[2];
    }
  });
}

// Get slug from command line arguments
const slug = process.argv[2];

if (!slug) {
  console.error('Error: Please provide a slug as argument');
  console.error('Usage: node sync-to-db.js <slug>');
  process.exit(1);
}

const presentationDir = path.join(__dirname, '../../../../src/app/presentations', slug);

// Check if directory exists
if (!fs.existsSync(presentationDir)) {
  console.error(`Error: Directory not found: ${presentationDir}`);
  process.exit(1);
}

// Read all HTML files
const slideFiles = fs.readdirSync(presentationDir)
  .filter(f => f.startsWith('slide-') && f.endsWith('.html'))
  .sort((a, b) => {
    const numA = parseInt(a.match(/slide-(\d+)/)[1]);
    const numB = parseInt(b.match(/slide-(\d+)/)[1]);
    return numA - numB;
  });

if (slideFiles.length === 0) {
  console.error('Error: No slide files found in directory');
  process.exit(1);
}

// Process each slide
const htmlSlides = slideFiles.map((file, index) => {
  const htmlContent = fs.readFileSync(path.join(presentationDir, file), 'utf-8');

  // Determine visual type based on content
  let visualType = 'html';
  const scripts = [];

  if (htmlContent.includes('p5-canvas') || htmlContent.includes('createCanvas') || htmlContent.includes('p5.js')) {
    visualType = 'p5';

    // Add P5.js CDN
    scripts.push({
      type: 'cdn',
      content: 'https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.7.0/p5.min.js'
    });

    // Extract inline P5 script if present
    const scriptMatch = htmlContent.match(/<script>([\s\S]*?)<\/script>/);
    if (scriptMatch) {
      scripts.push({
        type: 'inline',
        content: scriptMatch[1].trim()
      });
    }
  } else if (htmlContent.includes('d3.') || htmlContent.includes('d3.js')) {
    visualType = 'd3';

    // Add D3.js CDN
    scripts.push({
      type: 'cdn',
      content: 'https://d3js.org/d3.v7.min.js'
    });

    // Extract inline D3 script if present
    const scriptMatch = htmlContent.match(/<script>([\s\S]*?)<\/script>/);
    if (scriptMatch) {
      scripts.push({
        type: 'inline',
        content: scriptMatch[1].trim()
      });
    }
  }

  return {
    slideNumber: index + 1,
    htmlContent: htmlContent,
    visualType: visualType,
    scripts: scripts.length > 0 ? scripts : undefined
  };
});

// Read metadata file if it exists
let metadata = {};
const metadataPath = path.join(presentationDir, 'metadata.json');
if (fs.existsSync(metadataPath)) {
  metadata = JSON.parse(fs.readFileSync(metadataPath, 'utf-8'));
}

// Build the deck data object
const deckData = {
  title: metadata.title || `Presentation: ${slug}`,
  slug: slug,
  mathConcept: metadata.mathConcept || 'Unknown',
  mathStandard: metadata.mathStandard || '',
  gradeLevel: metadata.gradeLevel || 7,
  unitNumber: metadata.unitNumber,
  lessonNumber: metadata.lessonNumber,
  scopeAndSequenceId: metadata.scopeAndSequenceId,
  presentationType: 'html',
  htmlSlides: htmlSlides,
  learningGoals: metadata.learningGoals || [],
  generatedBy: 'ai',
  sourceImage: metadata.sourceImage || '',
  createdBy: 'system',
  isPublic: true,
  files: {
    pageComponent: `src/app/presentations/${slug}/`,
    dataFile: `src/app/presentations/${slug}/slide-*.html`
  },
  createdAt: new Date(),
  updatedAt: new Date()
};

// Generate MongoDB commands as a string
const mongoScript = `
// Sync HTML deck: ${slug}
// Generated: ${new Date().toISOString()}

// Switch to the correct database
use('ai-coaching-platform');

const deckData = ${JSON.stringify(deckData, null, 2)};

// Check if deck already exists
const existingDeck = db.workedexampledecks.findOne({ slug: deckData.slug });
if (existingDeck) {
  print('⚠️  Deck already exists. Deleting old version...');
  db.workedexampledecks.deleteOne({ slug: deckData.slug });
}

// Insert the deck
const result = db.workedexampledecks.insertOne(deckData);

if (result.acknowledged) {
  print('✅ HTML Deck saved successfully!');
  print('Deck ID: ' + result.insertedId);
  print('Slug: ' + deckData.slug);
  print('Total slides: ' + deckData.htmlSlides.length);
  print('📁 Local files: src/app/presentations/' + deckData.slug + '/');
  print('🔗 View at: /presentations/' + deckData.slug);
} else {
  print('❌ Error: Failed to insert deck');
  printjson(result);
}
`;

// Write to temp file and execute with mongosh
const tempFile = path.join('/tmp', `sync-${slug}-${Date.now()}.js`);
fs.writeFileSync(tempFile, mongoScript);

const databaseUrl = process.env.DATABASE_URL;
if (!databaseUrl) {
  console.error('Error: DATABASE_URL environment variable is not set');
  process.exit(1);
}

try {
  const output = execSync(`/usr/local/bin/mongosh "${databaseUrl}" --file "${tempFile}"`, {
    encoding: 'utf-8',
    stdio: ['pipe', 'pipe', 'pipe']
  });
  console.log(output);
} catch (error) {
  console.error('Error executing mongosh:', error.message);
  if (error.stdout) console.log(error.stdout);
  if (error.stderr) console.error(error.stderr);
  process.exit(1);
} finally {
  // Clean up temp file
  try {
    fs.unlinkSync(tempFile);
  } catch (e) {
    // Ignore cleanup errors
  }
}
