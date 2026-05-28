#!/usr/bin/env node

/**
 * Publish a markdown post to Ghost CMS
 * Usage: node publish-post.js <path-to-markdown-file>
 */

const fs = require('fs');
const path = require('path');
const matter = require('gray-matter');
const GhostAdminAPI = require('@tryghost/admin-api');

// Load environment variables from .env file
const dotenvPath = path.join(__dirname, '../../../.env');
require('dotenv').config({ path: dotenvPath });

// Configuration
const GHOST_SITE_URL = process.env.GHOST_SITE_URL;
const GHOST_ADMIN_API_KEY = process.env.GHOST_ADMIN_API_KEY;
const GHOST_API_VERSION = process.env.GHOST_API_VERSION || 'v6.0';

if (!GHOST_SITE_URL || !GHOST_ADMIN_API_KEY) {
  console.error('Error: Missing Ghost API credentials');
  console.error('Please set GHOST_SITE_URL and GHOST_ADMIN_API_KEY in .env file');
  process.exit(1);
}

// Initialize Ghost API
const api = new GhostAdminAPI({
  url: GHOST_SITE_URL,
  key: GHOST_ADMIN_API_KEY,
  version: GHOST_API_VERSION
});

/**
 * Convert markdown content to HTML (Ghost will convert to lexical)
 */
function convertMarkdownToHTML(markdown) {
  // For now, we'll pass markdown as-is and let Ghost handle conversion
  // Ghost's markdown parser will convert it properly
  return markdown;
}

/**
 * Add GitHub footer if github_folder is present
 */
function addGitHubFooter(html, githubFolder) {
  if (!githubFolder) return html;

  const repoUrl = `https://github.com/houfu/blog-alt-counsel/tree/main/posts/${githubFolder}`;
  const footer = `

---

## View on GitHub

This post is open source. View the source files, discussion notes, and revision history on GitHub.

[View on GitHub](${repoUrl})`;

  return html + footer;
}

/**
 * Publish post to Ghost
 */
async function publishPost(filePath) {
  try {
    // Read the markdown file
    const fileContent = fs.readFileSync(filePath, 'utf-8');

    // Parse frontmatter
    const { data: frontmatter, content } = matter(fileContent);

    console.log('📝 Parsing post:', frontmatter.title || 'Untitled');
    console.log('   Slug:', frontmatter.slug || '(auto-generated)');
    console.log('   Tags:', frontmatter.tags?.join(', ') || '(none)');
    console.log('   Status:', frontmatter.status || 'draft');
    console.log('   Featured:', frontmatter.featured || false);

    // Add GitHub footer if github_folder is present
    let htmlContent = convertMarkdownToHTML(content);
    if (frontmatter.github_folder) {
      console.log('   GitHub folder:', frontmatter.github_folder);
      htmlContent = addGitHubFooter(htmlContent, frontmatter.github_folder);
    }

    // Prepare post data
    const postData = {
      title: frontmatter.title || 'Untitled Post',
      html: htmlContent,
      status: frontmatter.status || 'draft',
      visibility: frontmatter.visibility || 'public',
      featured: frontmatter.featured || false
    };

    // Add optional fields
    if (frontmatter.slug) {
      postData.slug = frontmatter.slug;
    }

    if (frontmatter.custom_excerpt) {
      postData.custom_excerpt = frontmatter.custom_excerpt;
    }

    if (frontmatter.tags && Array.isArray(frontmatter.tags)) {
      postData.tags = frontmatter.tags.map(tag => ({ name: tag }));
    }

    if (frontmatter.published_at) {
      postData.published_at = frontmatter.published_at;
    }

    console.log('\n🚀 Publishing to Ghost...');

    // Create post using ?source=html to let Ghost convert HTML/markdown to lexical
    // Note: The @tryghost/admin-api expects just the post object, not wrapped in posts array
    const post = await api.posts.add(postData, { source: 'html' });

    console.log('\n✅ Post published successfully!');
    console.log('   Post ID:', post.id);
    console.log('   URL:', post.url);
    console.log('   Status:', post.status);
    console.log('   Admin URL:', `${GHOST_SITE_URL}/ghost/#/editor/post/${post.id}`);

    // Return post data for further processing
    return post;

  } catch (error) {
    console.error('\n❌ Error publishing post:', error.message);
    if (error.context) {
      console.error('   Context:', error.context);
    }
    if (error.errors) {
      console.error('   Errors:', JSON.stringify(error.errors, null, 2));
    }
    if (error.response?.body) {
      console.error('   Response body:', JSON.stringify(error.response.body, null, 2));
    }
    // Log full error for debugging
    console.error('\n   Full error:', JSON.stringify(error, null, 2));
    throw error;
  }
}

// Main execution
if (require.main === module) {
  const args = process.argv.slice(2);

  if (args.length === 0) {
    console.error('Usage: node publish-post.js <path-to-markdown-file>');
    process.exit(1);
  }

  const filePath = path.resolve(args[0]);

  if (!fs.existsSync(filePath)) {
    console.error(`Error: File not found: ${filePath}`);
    process.exit(1);
  }

  publishPost(filePath)
    .then(() => process.exit(0))
    .catch(() => process.exit(1));
}

module.exports = { publishPost };
