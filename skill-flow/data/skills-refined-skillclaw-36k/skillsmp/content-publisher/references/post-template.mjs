#!/usr/bin/env node
/**
 * Content Publisher - Post Template Generator
 *
 * Creates posts in Notion Content Hub with proper structure and brand alignment.
 *
 * Usage:
 *   node .claude/skills/content-publisher/references/post-template.mjs \
 *     --title "Post Title" \
 *     --content "Post content..." \
 *     --accounts "LinkedIn (Company),LinkedIn (Personal)" \
 *     --type "LinkedIn Post"
 */

const NOTION_TOKEN = process.env.NOTION_TOKEN;
const DATABASE_ID = "7005d0d1-41d3-436c-9f86-526d275c2f10";

/**
 * Valid target accounts for multi-select
 */
const VALID_ACCOUNTS = [
  'LinkedIn (Company)',
  'LinkedIn (Personal)',
  'YouTube',
  'Google Business',
  'Bluesky',
  'Facebook',
  'Instagram',
  'Twitter'
];

/**
 * Valid communication types
 */
const VALID_TYPES = [
  'LinkedIn Post',
  'Story Update',
  'Newsletter',
  'Delight & Excitement',
  'Innovation Showcase',
  'Regular Check-in',
  'Justice Hub Connection',
  'Empathy Ledger Story'
];

/**
 * Create a post in Notion Content Hub
 */
async function createPost({ title, content, accounts = ['LinkedIn (Company)'], type = 'LinkedIn Post', scheduledDate = null }) {
  if (!NOTION_TOKEN) {
    throw new Error('NOTION_TOKEN environment variable required');
  }

  // Validate accounts
  const validAccounts = accounts.filter(a => VALID_ACCOUNTS.includes(a));
  if (validAccounts.length === 0) {
    throw new Error(`Invalid accounts. Valid options: ${VALID_ACCOUNTS.join(', ')}`);
  }

  // Validate type
  if (!VALID_TYPES.includes(type)) {
    console.warn(`Unknown type "${type}", using "LinkedIn Post"`);
    type = 'LinkedIn Post';
  }

  const properties = {
    "Content/Communication Name": {
      title: [{ text: { content: title } }]
    },
    "Key Message/Story": {
      rich_text: [{ text: { content: content } }]
    },
    "Communication Type": {
      select: { name: type }
    },
    "Status": {
      status: { name: "Story in Development" }
    },
    "Target Accounts": {
      multi_select: validAccounts.map(name => ({ name }))
    }
  };

  // Add scheduled date if provided
  if (scheduledDate) {
    properties["Sent date"] = {
      date: { start: scheduledDate }
    };
  }

  const response = await fetch("https://api.notion.com/v1/pages", {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${NOTION_TOKEN}`,
      "Content-Type": "application/json",
      "Notion-Version": "2025-09-03"
    },
    body: JSON.stringify({
      parent: { database_id: DATABASE_ID },
      properties
    })
  });

  if (!response.ok) {
    const error = await response.text();
    throw new Error(`Notion API Error: ${error}`);
  }

  return await response.json();
}

/**
 * Generate post from Ralph completion
 */
function generateRalphCompletionPost(feature) {
  const title = `Shipped: ${feature.title}`;

  const content = `We just shipped something new.

${feature.description}

What it does:
${feature.acceptance_criteria.map(c => `• ${c}`).join('\n')}

This is part of our ongoing work to build technology that serves community—not the other way around.

More coming soon.

#BuildingDifferently #TechForJustice #RegenerativeInnovation`;

  return { title, content, type: 'Innovation Showcase' };
}

/**
 * Generate post from sprint milestone
 */
function generateSprintPost(sprint) {
  const title = `Sprint ${sprint.number} Complete`;

  const content = `Another sprint in the books.

${sprint.completed} issues completed across ${sprint.projects.join(', ')}.

Highlights:
${sprint.highlights.map(h => `• ${h}`).join('\n')}

Velocity: ${sprint.velocity} points
Team: Still small, still scrappy, still building.

${sprint.nextFocus ? `Next: ${sprint.nextFocus}` : ''}

#AgileForGood #BuildingInPublic`;

  return { title, content, type: 'Story Update' };
}

/**
 * Generate post from ecosystem insight
 */
function generateInsightPost(insight) {
  const title = insight.headline;

  const content = `${insight.hook}

${insight.body}

${insight.callToAction || 'More on this soon.'}

${insight.hashtags?.map(h => `#${h.replace('#', '')}`).join(' ') || '#ACTEcosystem #RegenerativeInnovation'}`;

  return { title, content, type: insight.type || 'LinkedIn Post' };
}

// CLI interface
if (import.meta.url === `file://${process.argv[1]}`) {
  const args = process.argv.slice(2);
  const options = {};

  for (let i = 0; i < args.length; i += 2) {
    const key = args[i].replace('--', '');
    options[key] = args[i + 1];
  }

  if (!options.title || !options.content) {
    console.log('Usage: node post-template.mjs --title "Title" --content "Content" [--accounts "LinkedIn (Company)"] [--type "LinkedIn Post"]');
    process.exit(1);
  }

  const accounts = options.accounts ? options.accounts.split(',').map(a => a.trim()) : ['LinkedIn (Company)'];

  createPost({
    title: options.title,
    content: options.content,
    accounts,
    type: options.type || 'LinkedIn Post',
    scheduledDate: options.date || null
  })
    .then(result => {
      console.log('Post created:', result.url);
    })
    .catch(err => {
      console.error('Error:', err.message);
      process.exit(1);
    });
}

export { createPost, generateRalphCompletionPost, generateSprintPost, generateInsightPost, VALID_ACCOUNTS, VALID_TYPES };
