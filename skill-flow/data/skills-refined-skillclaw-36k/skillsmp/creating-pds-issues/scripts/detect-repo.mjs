#!/usr/bin/env node
/**
 * detect-repo.mjs
 *
 * Detects if the current directory is a NASA-PDS repository.
 * Returns the repository name if detected, or null if not.
 *
 * Usage:
 *   node scripts/detect-repo.mjs
 *
 * Output (JSON):
 *   {"detected": true, "repo": "pds-registry", "org": "NASA-PDS"}
 *   {"detected": false}
 */

import { execSync } from 'child_process';

function detectRepo() {
  try {
    // Try to get remote URL, preferring origin first, then upstream
    let remoteUrl;
    let remoteName;

    try {
      remoteUrl = execSync('git remote get-url origin 2>/dev/null', {
        encoding: 'utf8',
        stdio: ['pipe', 'pipe', 'ignore']
      }).trim();
      remoteName = 'origin';
    } catch {
      // Fall back to upstream if origin doesn't exist
      try {
        remoteUrl = execSync('git remote get-url upstream 2>/dev/null', {
          encoding: 'utf8',
          stdio: ['pipe', 'pipe', 'ignore']
        }).trim();
        remoteName = 'upstream';
      } catch {
        return {
          detected: false,
          reason: 'No origin or upstream remote configured'
        };
      }
    }

    // Parse the URL to extract org and repo
    // Handles both HTTPS and SSH formats:
    // - https://github.com/NASA-PDS/pds-registry.git
    // - git@github.com:NASA-PDS/pds-registry.git

    let match;

    // Try HTTPS format
    match = remoteUrl.match(/github\.com[/:]([\w-]+)\/([\w-]+?)(?:\.git)?$/);

    if (match) {
      const [, org, repo] = match;

      // Check if it's a NASA-PDS repository
      if (org === 'NASA-PDS') {
        return {
          detected: true,
          repo: repo,
          org: org,
          url: remoteUrl,
          remote: remoteName
        };
      } else {
        // If origin is not NASA-PDS, check if upstream is available
        if (remoteName === 'origin') {
          try {
            const upstreamUrl = execSync('git remote get-url upstream 2>/dev/null', {
              encoding: 'utf8',
              stdio: ['pipe', 'pipe', 'ignore']
            }).trim();

            const upstreamMatch = upstreamUrl.match(/github\.com[/:]([\w-]+)\/([\w-]+?)(?:\.git)?$/);
            if (upstreamMatch && upstreamMatch[1] === 'NASA-PDS') {
              return {
                detected: true,
                repo: upstreamMatch[2],
                org: 'NASA-PDS',
                url: upstreamUrl,
                remote: 'upstream',
                note: 'Detected from upstream (origin is a fork)'
              };
            }
          } catch {
            // No upstream available
          }
        }

        return {
          detected: false,
          reason: `Repository is from ${org}, not NASA-PDS`
        };
      }
    }

    return {
      detected: false,
      reason: 'Could not parse GitHub URL from remote'
    };
  } catch (error) {
    return {
      detected: false,
      reason: 'Not in a git repository'
    };
  }
}

// Run detection and output JSON
const result = detectRepo();
console.log(JSON.stringify(result, null, 2));
