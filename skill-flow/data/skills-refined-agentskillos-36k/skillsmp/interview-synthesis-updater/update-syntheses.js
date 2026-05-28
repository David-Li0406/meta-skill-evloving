#!/usr/bin/env node

import fs from 'fs';
import path from 'path';
import yaml from 'js-yaml';
import { glob } from 'glob';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

/**
 * Parse command line arguments
 */
function parseArgs() {
  const args = process.argv.slice(2);
  const params = {
    analysisFile: null,
    baseDir: process.cwd()
  };

  args.forEach(arg => {
    const [key, value] = arg.split('=');
    const cleanKey = key.replace('--', '');

    if (cleanKey === 'file') {
      params.analysisFile = value?.replace(/^["']|["']$/g, '');
    } else if (cleanKey === 'base-dir') {
      params.baseDir = value?.replace(/^["']|["']$/g, '');
    }
  });

  return params;
}

/**
 * Extract YAML frontmatter and content from markdown file
 */
function parseMarkdownFile(filePath) {
  const content = fs.readFileSync(filePath, 'utf8');

  // Check for YAML frontmatter
  const frontmatterRegex = /^---\n([\s\S]*?)\n---\n([\s\S]*)$/;
  const match = content.match(frontmatterRegex);

  if (!match) {
    return { frontmatter: {}, content: content };
  }

  const frontmatter = yaml.load(match[1]);
  const body = match[2];

  return { frontmatter, content: body };
}

/**
 * Extract key quotes from interview analysis
 */
function extractKeyQuotes(content) {
  const quotes = [];
  const quotesSection = content.match(/## Key Quotes\n\n([\s\S]*?)\n\n##/);

  if (!quotesSection) return quotes;

  const quoteBlocks = quotesSection[1].split('\n\n> "');

  for (const block of quoteBlocks) {
    if (!block.trim()) continue;

    const quoteMatch = block.match(/^"?([^"]+)"\s*\n>\s*\n> — (.+)$/m);
    if (quoteMatch) {
      quotes.push({
        text: quoteMatch[1].trim(),
        attribution: quoteMatch[2].trim()
      });
    }
  }

  return quotes;
}

/**
 * Convert string to filename (lowercase, hyphenated)
 */
function toFilename(str) {
  return str
    .toLowerCase()
    .replace(/[\/\s]+/g, '-')
    .replace(/[^a-z0-9-]/g, '')
    .replace(/-+/g, '-');
}

/**
 * Update or create synthesis document
 */
function updateSynthesis(synthesisPath, templatePath, updates) {
  let content;

  if (fs.existsSync(synthesisPath)) {
    // Update existing synthesis
    content = fs.readFileSync(synthesisPath, 'utf8');

    // Add quotes to Representative Quotes section
    if (updates.quotes && updates.quotes.length > 0) {
      const quotesSection = content.match(/(## Representative Quotes\n\n)([\s\S]*?)(\n\n##)/);
      if (quotesSection) {
        const existingQuotes = quotesSection[2];
        const newQuotes = updates.quotes.map(q =>
          `> "${q.text}"\n>\n> — ${q.attribution}`
        ).join('\n\n');

        content = content.replace(
          quotesSection[0],
          `${quotesSection[1]}${existingQuotes}\n\n${newQuotes}${quotesSection[3]}`
        );
      }
    }

    // Add to source interviews list
    if (updates.sourceInterview) {
      const sourcesSection = content.match(/(## Source Interviews\n\n)([\s\S]*?)$/);
      if (sourcesSection) {
        const existingSources = sourcesSection[2];
        // Check if already exists
        if (!existingSources.includes(updates.sourceInterview)) {
          content = content.replace(
            sourcesSection[0],
            `${sourcesSection[1]}${existingSources}${updates.sourceInterview}\n`
          );
        }
      }
    }

    // Update Last Updated date
    const today = new Date().toISOString().split('T')[0];
    content = content.replace(
      /\*\*Last Updated\*\*: \d{4}-\d{2}-\d{2}/,
      `**Last Updated**: ${today}`
    );

    // Update frequency count if provided
    if (updates.incrementFrequency) {
      const freqMatch = content.match(/This theme appears in (\d+) interviews?/);
      if (freqMatch) {
        const newCount = parseInt(freqMatch[1]) + 1;
        content = content.replace(
          freqMatch[0],
          `This theme appears in ${newCount} interview${newCount === 1 ? '' : 's'}`
        );
      }
    }

  } else {
    // Create new synthesis from template
    const template = fs.readFileSync(templatePath, 'utf8');
    content = template;

    // Replace placeholders
    if (updates.title) {
      content = content.replace(/# \[Theme\/Product\/Persona Name\]/g, `# ${updates.title}`);
    }

    if (updates.description) {
      content = content.replace(
        /Brief description of this theme\/product\/persona and why it matters\./,
        updates.description
      );
    }

    // Add initial quote
    if (updates.quotes && updates.quotes.length > 0) {
      const quote = updates.quotes[0];
      content = content.replace(
        /> "Example quote from an interview that exemplifies this theme\/pain point\/pattern\."\n>\n> — Attribution/,
        `> "${quote.text}"\n>\n> — ${quote.attribution}`
      );
    }

    // Add source interview
    if (updates.sourceInterview) {
      content = content.replace(
        /- \[YYYY-MM-DD Interview Title\]\(\.\.\/interview-analysis\/filename\.md\)/,
        updates.sourceInterview
      );
    }

    // Set initial frequency
    content = content.replace(
      /This theme appears in X interviews?/,
      'This theme appears in 1 interview'
    );

    // Set Last Updated
    const today = new Date().toISOString().split('T')[0];
    content = content.replace(
      /\*\*Last Updated\*\*: YYYY-MM-DD/,
      `**Last Updated**: ${today}`
    );
  }

  // Write the file
  fs.writeFileSync(synthesisPath, content, 'utf8');
}

/**
 * Update index.md
 */
function updateIndex(indexPath, interviewData, baseDir) {
  let content = fs.readFileSync(indexPath, 'utf8');

  // Count total interviews
  const analysisDir = path.join(baseDir, 'interview-analysis');
  const totalInterviews = fs.readdirSync(analysisDir).filter(f => f.endsWith('.md')).length;

  // Count total syntheses
  const synthesisDir = path.join(baseDir, 'syntheses');
  const themeCount = fs.readdirSync(path.join(synthesisDir, 'by-theme')).filter(f => f.endsWith('.md') && !f.startsWith('_')).length;
  const productCount = fs.readdirSync(path.join(synthesisDir, 'by-product')).filter(f => f.endsWith('.md') && !f.startsWith('_')).length;
  const personaCount = fs.readdirSync(path.join(synthesisDir, 'by-persona')).filter(f => f.endsWith('.md') && !f.startsWith('_')).length;

  // Update quick stats
  content = content.replace(
    /\*\*Total Interviews\*\*: \d+/,
    `**Total Interviews**: ${totalInterviews}`
  );

  // Update synthesis counts
  content = content.replace(
    /- Themes: \d+/,
    `- Themes: ${themeCount}`
  );
  content = content.replace(
    /- Products: \d+/,
    `- Products: ${productCount}`
  );
  content = content.replace(
    /- Personas: \d+/,
    `- Personas: ${personaCount}`
  );

  // Add to Recent Interviews section (keep top 10)
  const recentSection = content.match(/(## Recent Interviews\n\n)([\s\S]*?)(\n\n##)/);
  if (recentSection) {
    const recentEntry = `- **${interviewData.date}**: ${interviewData.name} - ${interviewData.brief}\n`;
    const existingRecent = recentSection[2].split('\n').filter(l => l.trim());
    const updatedRecent = [recentEntry.trim(), ...existingRecent].slice(0, 10).join('\n');

    content = content.replace(
      recentSection[0],
      `${recentSection[1]}${updatedRecent}\n${recentSection[3]}`
    );
  }

  // Add to All Interviews table
  const tableSection = content.match(/(## All Interviews by Date\n\n\| Date[\s\S]*?\n\|[-|\s]+\|[\s\S]*?)(\n\n##|\n\n$)/);
  if (tableSection) {
    const tableRow = `| ${interviewData.date} | ${interviewData.name} | ${interviewData.company} | ${interviewData.role} | ${interviewData.topics} | [Link](interview-analysis/${interviewData.filename}) |\n`;

    // Insert after header rows
    const headerEnd = tableSection[1].indexOf('\n|---');
    const afterHeader = tableSection[1].indexOf('\n', headerEnd + 1) + 1;

    content = content.replace(
      tableSection[1],
      tableSection[1].slice(0, afterHeader) + tableRow + tableSection[1].slice(afterHeader)
    );
  }

  fs.writeFileSync(indexPath, content, 'utf8');
}

/**
 * Main execution
 */
async function main() {
  const params = parseArgs();

  // Validate inputs
  if (!params.analysisFile) {
    console.error(JSON.stringify({
      success: false,
      error: 'Missing required parameter: --file'
    }, null, 2));
    process.exit(1);
  }

  if (!fs.existsSync(params.analysisFile)) {
    console.error(JSON.stringify({
      success: false,
      error: `Analysis file not found: ${params.analysisFile}`
    }, null, 2));
    process.exit(1);
  }

  try {
    // Parse interview analysis
    const { frontmatter, content } = parseMarkdownFile(params.analysisFile);

    // Validate frontmatter
    const required = ['date', 'customer_first', 'company', 'role', 'call_type'];
    const missing = required.filter(field => !frontmatter[field]);
    if (missing.length > 0) {
      console.error(JSON.stringify({
        success: false,
        error: `Missing required frontmatter fields: ${missing.join(', ')}`
      }, null, 2));
      process.exit(1);
    }

    // Extract data
    const quotes = extractKeyQuotes(content);
    const themes = frontmatter.themes || [];
    const products = frontmatter.hubspot_products || [];
    const persona = frontmatter.role;

    const customerName = frontmatter.customer_last
      ? `${frontmatter.customer_first} ${frontmatter.customer_last}`
      : frontmatter.customer_first;

    const filename = path.basename(params.analysisFile);
    const sourceLink = `- [${frontmatter.date} ${customerName}, ${frontmatter.company}](../interview-analysis/${filename})`;

    // Paths
    const synthesisDir = path.join(params.baseDir, 'syntheses');
    const templatePath = path.join(synthesisDir, '_SYNTHESIS_TEMPLATE.md');
    const indexPath = path.join(params.baseDir, 'index.md');

    if (!fs.existsSync(templatePath)) {
      console.error(JSON.stringify({
        success: false,
        error: `Template not found: ${templatePath}`
      }, null, 2));
      process.exit(1);
    }

    const report = {
      updated: { theme: [], product: [], persona: [] },
      created: []
    };

    // Update by-theme syntheses
    for (const theme of themes) {
      const themeFile = toFilename(theme) + '.md';
      const themePath = path.join(synthesisDir, 'by-theme', themeFile);
      const exists = fs.existsSync(themePath);

      updateSynthesis(themePath, templatePath, {
        title: theme,
        description: `Insights and patterns related to ${theme}.`,
        quotes: quotes.slice(0, 3), // Add first 3 quotes
        sourceInterview: sourceLink,
        incrementFrequency: exists
      });

      if (exists) {
        report.updated.theme.push(themeFile);
      } else {
        report.created.push(`syntheses/by-theme/${themeFile}`);
      }
    }

    // Update by-product syntheses
    for (const product of products) {
      const productFile = toFilename(product) + '.md';
      const productPath = path.join(synthesisDir, 'by-product', productFile);
      const exists = fs.existsSync(productPath);

      updateSynthesis(productPath, templatePath, {
        title: product,
        description: `Customer feedback and pain points related to ${product}.`,
        quotes: quotes.slice(0, 3),
        sourceInterview: sourceLink,
        incrementFrequency: exists
      });

      if (exists) {
        report.updated.product.push(productFile);
      } else {
        report.created.push(`syntheses/by-product/${productFile}`);
      }
    }

    // Update by-persona synthesis
    const personaFile = toFilename(persona) + 's.md'; // Pluralize
    const personaPath = path.join(synthesisDir, 'by-persona', personaFile);
    const personaExists = fs.existsSync(personaPath);

    updateSynthesis(personaPath, templatePath, {
      title: persona + 's',
      description: `Insights from interviews with ${persona}s.`,
      quotes: quotes.slice(0, 5),
      sourceInterview: sourceLink,
      incrementFrequency: personaExists
    });

    if (personaExists) {
      report.updated.persona.push(personaFile);
    } else {
      report.created.push(`syntheses/by-persona/${personaFile}`);
    }

    // Update index.md
    const summaryMatch = content.match(/## Call Summary\n\n(.*?)\n\n/s);
    const briefSummary = summaryMatch ? summaryMatch[1].split('\n')[0] : '';

    updateIndex(indexPath, {
      date: frontmatter.date,
      name: customerName,
      company: frontmatter.company,
      role: frontmatter.role,
      topics: themes.join(', '),
      filename: filename,
      brief: briefSummary
    }, params.baseDir);

    // Count total interviews
    const analysisDir = path.join(params.baseDir, 'interview-analysis');
    const totalInterviews = fs.readdirSync(analysisDir).filter(f => f.endsWith('.md')).length;

    // Output report
    console.log(JSON.stringify({
      success: true,
      report: report,
      stats: {
        totalInterviews: totalInterviews,
        totalSyntheses: report.updated.theme.length + report.updated.product.length + report.updated.persona.length + report.created.length
      }
    }, null, 2));

  } catch (error) {
    console.error(JSON.stringify({
      success: false,
      error: error.message,
      stack: error.stack
    }, null, 2));
    process.exit(1);
  }
}

main();
