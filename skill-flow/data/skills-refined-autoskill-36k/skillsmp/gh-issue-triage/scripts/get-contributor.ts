#!/usr/bin/env bun

/**
 * Fetch GitHub contributor profile including Twitter handle
 * 
 * Usage:
 *   bun run get-contributor.ts <login> [issue-number]
 *   bun run get-contributor.ts bcheung 42
 * 
 * Outputs:
 *   1. Contributor profile details
 *   2. Ready-to-paste changeset credit line (name + Twitter link)
 *   3. Ready-to-paste semantic-memory_store command
 * 
 * Returns JSON with:
 *   - login (GitHub username)
 *   - name (display name)
 *   - twitter_username (if set in profile)
 *   - blog (website URL)
 *   - bio (profile description)
 *   - avatar_url
 *   - html_url (GitHub profile)
 */

import { z } from "zod";

const GitHubUserSchema = z.object({
  login: z.string(),
  name: z.string().nullable(),
  twitter_username: z.string().nullable(),
  blog: z.string().nullable(),
  bio: z.string().nullable(),
  avatar_url: z.string(),
  html_url: z.string(),
  public_repos: z.number().optional(),
  followers: z.number().optional(),
});

type GitHubUser = z.infer<typeof GitHubUserSchema>;

async function getContributor(login: string): Promise<GitHubUser> {
  // Use gh CLI to fetch user profile
  const result = await Bun.$`gh api users/${login}`.json();
  
  // Validate response
  const user = GitHubUserSchema.parse(result);
  
  return user;
}

function formatOutput(user: GitHubUser): string {
  const parts = [
    `Login: ${user.login}`,
    user.name ? `Name: ${user.name}` : null,
    user.twitter_username ? `Twitter: @${user.twitter_username}` : "Twitter: N/A",
    user.blog ? `Blog: ${user.blog}` : null,
    user.bio ? `Bio: ${user.bio}` : null,
    `Profile: ${user.html_url}`,
  ].filter(Boolean);
  
  return parts.join("\n");
}

function formatForChangeset(user: GitHubUser, issueNumber?: number): string {
  // PREFERRED: Full name + Twitter (best for engagement)
  if (user.name && user.twitter_username) {
    const issue = issueNumber ? `reporting #${issueNumber}` : 'the report';
    return `Thanks to ${user.name} ([@${user.twitter_username}](https://x.com/${user.twitter_username})) for ${issue}!`;
  }
  
  // Twitter only (no name available)
  if (user.twitter_username) {
    const issue = issueNumber ? `reporting #${issueNumber}` : 'the report';
    return `Thanks to [@${user.twitter_username}](https://x.com/${user.twitter_username}) for ${issue}!`;
  }
  
  // Name only (no Twitter)
  if (user.name) {
    const issue = issueNumber ? `reporting #${issueNumber}` : 'the report';
    return `Thanks to ${user.name} (@${user.login} on GitHub) for ${issue}!`;
  }
  
  // Fallback: GitHub username only
  const issue = issueNumber ? `reporting #${issueNumber}` : 'the report';
  return `Thanks to @${user.login} for ${issue}!`;
}

function formatSemanticMemoryStore(user: GitHubUser, issueNumber?: number): string {
  const twitterPart = user.twitter_username ? ` (@${user.twitter_username} on Twitter)` : '';
  const issuePart = issueNumber ? `. Filed issue #${issueNumber}` : '';
  const bioPart = user.bio ? `. Bio: '${user.bio}'` : '';
  
  const tags = ['contributor', user.login, issueNumber ? `issue-${issueNumber}` : null]
    .filter(Boolean)
    .join(',');
  
  return `semantic-memory_store(
  information: "Contributor @${user.login}: ${user.name || user.login}${twitterPart}${issuePart}${bioPart}",
  tags: "${tags}"
)`;
}

// CLI
if (import.meta.main) {
  const args = Bun.argv.slice(2);
  const [login, issueNumberArg] = args.filter(arg => !arg.startsWith('--'));
  const issueNumber = issueNumberArg ? parseInt(issueNumberArg, 10) : undefined;
  
  if (!login) {
    console.error("Usage: bun run get-contributor.ts <login> [issue-number]");
    console.error("Example: bun run get-contributor.ts bcheung 42");
    console.error("\nOptions:");
    console.error("  --json    Include JSON output");
    process.exit(1);
  }
  
  try {
    const user = await getContributor(login);
    
    console.log("\n📝 Contributor Profile\n");
    console.log(formatOutput(user));
    console.log("\n✨ Changeset Credit (copy/paste)\n");
    console.log(formatForChangeset(user, issueNumber));
    console.log("\n🧠 Semantic Memory Store (copy/paste)\n");
    console.log(formatSemanticMemoryStore(user, issueNumber));
    console.log();
    
    // Also output JSON for programmatic use
    if (Bun.argv.includes("--json")) {
      console.log("\n📦 JSON Output\n");
      console.log(JSON.stringify(user, null, 2));
    }
  } catch (error) {
    if (error instanceof Error) {
      console.error(`❌ Error: ${error.message}`);
    }
    process.exit(1);
  }
}

export { getContributor, formatForChangeset, formatSemanticMemoryStore, type GitHubUser };
