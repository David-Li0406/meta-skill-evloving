#!/usr/bin/env node

/**
 * ADF (Atlassian Document Format) Parser
 *
 * Converts Jira's ADF JSON format to plain text/markdown.
 *
 * Usage:
 *   echo "$ADF_JSON" | node parse-adf.js
 *   cat comment.json | jq '.body' | node parse-adf.js
 */

const fs = require('fs');

function parseADF(node, depth = 0) {
  if (!node) return '';

  // Text node - return the text
  if (node.text) return node.text;

  // No content array - return empty
  if (!node.content || !Array.isArray(node.content)) return '';

  // Parse all children
  const children = node.content.map(child => parseADF(child, depth + 1)).join('');

  // Format based on node type
  switch (node.type) {
    case 'paragraph':
      return children + '\n\n';
    case 'heading':
      const level = node.attrs?.level || 1;
      return '#'.repeat(level) + ' ' + children + '\n\n';
    case 'orderedList':
      return children + '\n';
    case 'bulletList':
      return children + '\n';
    case 'listItem':
      return '- ' + children.trim() + '\n';
    case 'codeBlock':
      const lang = node.attrs?.language || '';
      return '```' + lang + '\n' + children + '```\n\n';
    case 'hardBreak':
      return '\n';
    case 'rule':
      return '---\n\n';
    default:
      return children;
  }
}

// Read from stdin
const input = fs.readFileSync(0, 'utf-8').trim();

if (!input || input === 'null') {
  console.log('');
  process.exit(0);
}

try {
  const adf = JSON.parse(input);
  console.log(parseADF(adf).trim());
} catch (e) {
  // If parsing fails, assume it's already plain text
  console.log(input);
}
