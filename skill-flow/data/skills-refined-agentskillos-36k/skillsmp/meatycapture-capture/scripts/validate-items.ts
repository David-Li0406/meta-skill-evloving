#!/usr/bin/env bun
/**
 * Validate MeatyCapture items without loading full skill content.
 * Execute-vs-load pattern: run this script directly instead of loading workflow docs.
 *
 * Usage: bun run validate-items.ts '{"items": [...]}'
 */

import { z } from 'zod';

const ItemSchema = z.object({
  title: z.string().min(5, 'Title must be at least 5 characters'),
  type: z.enum(['bug', 'enhancement', 'idea', 'debt', 'documentation']),
  domain: z.enum(['core', 'ui', 'api', 'cli', 'docs', 'infrastructure', 'testing']),
  priority: z.enum(['critical', 'high', 'medium', 'low']).optional().default('medium'),
  status: z.enum(['triage', 'accepted', 'in-progress', 'done', 'wont-fix']).optional().default('triage'),
  tags: z.array(z.string()).optional().default([]),
  notes: z.string().optional(),
});

const InputSchema = z.object({
  project: z.string().optional(),
  items: z.array(ItemSchema).min(1, 'At least one item required'),
});

async function main() {
  const input = process.argv[2];

  if (!input) {
    console.error('Usage: bun run validate-items.ts \'{"items": [...]}\'');
    process.exit(1);
  }

  try {
    const parsed = JSON.parse(input);
    const result = InputSchema.safeParse(parsed);

    if (!result.success) {
      console.error('Validation errors:');
      result.error.issues.forEach(issue => {
        console.error(`  - ${issue.path.join('.')}: ${issue.message}`);
      });
      process.exit(1);
    }

    console.log(JSON.stringify({ valid: true, items: result.data.items.length }));
  } catch (e) {
    console.error(`Invalid JSON: ${(e as Error).message}`);
    process.exit(1);
  }
}

main();
