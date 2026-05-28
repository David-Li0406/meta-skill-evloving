#!/usr/bin/env tsx
import { Client } from '@notionhq/client';
import { parseArgs } from 'util';

const notion = new Client({ auth: process.env.NOTION_API_KEY });

function extractId(input: string): string {
  if (input.includes('notion.so')) {
    const url = new URL(input);
    const pParam = url.searchParams.get('p');
    if (pParam) return pParam.replace(/-/g, '');
    const match = url.pathname.match(/([a-f0-9]{32})$/i)
      || url.pathname.match(/([a-f0-9-]{36})$/i)
      || url.pathname.match(/-([a-f0-9]{32})(?:\?|$)/i);
    if (match) return match[1].replace(/-/g, '');
  }
  return input.replace(/-/g, '');
}

const { values } = parseArgs({
  options: {
    database: { type: 'string', short: 'd' },
    title: { type: 'string', short: 't' },
    due: { type: 'string' },
    status: { type: 'string', short: 's' },
    assign: { type: 'string', short: 'a' },
    json: { type: 'boolean', default: false },
  },
});

if (!values.database || !values.title) {
  console.error(`Usage: append-task.ts --database <DB_ID|URL> --title <text> [--due <date>] [--status <status>]

Add a task with title and optional due date.

Options:
  --database, -d  Database ID or URL (required)
  --title, -t     Task title (required)
  --due           Due date (YYYY-MM-DD or "YYYY-MM-DD to YYYY-MM-DD")
  --status, -s    Status value
  --assign, -a    Assignee name or UUID
  --json          Output full response as JSON

Examples:
  append-task.ts -d abc123 -t "Review PR" --due 2025-01-15
  append-task.ts -d abc123 -t "Sprint planning" --due "2025-01-20 to 2025-01-21" -s "Not Started"
`);
  process.exit(1);
}

const databaseId = extractId(values.database);

// Cache for user lookups
const userCache = new Map<string, string>();

async function findUserByName(name: string): Promise<string | null> {
  const lowerName = name.toLowerCase();
  if (userCache.has(lowerName)) return userCache.get(lowerName)!;

  let cursor: string | undefined;
  do {
    const response = await notion.users.list({ start_cursor: cursor, page_size: 100 });
    for (const user of response.results as any[]) {
      const userName = user.name?.toLowerCase() || '';
      userCache.set(userName, user.id);
      if (userName === lowerName || userName.includes(lowerName)) {
        return user.id;
      }
    }
    cursor = response.has_more ? response.next_cursor! : undefined;
  } while (cursor);

  return null;
}

function isUuid(value: string): boolean {
  return /^[a-f0-9-]{32,36}$/i.test(value.replace(/-/g, ''));
}

async function main() {
  try {
    const db = await notion.databases.retrieve({ database_id: databaseId });
    const schema = db.properties as any;

    const titleProp = Object.entries(schema)
      .find(([_, p]: any) => p.type === 'title')?.[0] || 'Name';

    const properties: any = {
      [titleProp]: {
        title: [{ text: { content: values.title } }],
      },
    };

    // Find and set due date property
    if (values.due) {
      const datePropName = Object.entries(schema)
        .find(([name, p]: any) => p.type === 'date' &&
          (name.toLowerCase().includes('due') || name.toLowerCase().includes('date'))
        )?.[0];

      if (datePropName) {
        if (values.due.includes(' to ')) {
          const [start, end] = values.due.split(' to ').map(d => d.trim());
          properties[datePropName] = { date: { start, end } };
        } else {
          properties[datePropName] = { date: { start: values.due } };
        }
      } else {
        console.error('Warning: No date property found in database');
      }
    }

    if (values.status && schema.Status) {
      if (schema.Status.type === 'status') {
        properties.Status = { status: { name: values.status } };
      } else if (schema.Status.type === 'select') {
        properties.Status = { select: { name: values.status } };
      }
    }

    if (values.assign && schema.Assign) {
      let userId: string;
      if (isUuid(values.assign)) {
        userId = values.assign;
      } else {
        const foundId = await findUserByName(values.assign);
        if (!foundId) {
          console.error(`User not found: "${values.assign}"`);
          process.exit(1);
        }
        userId = foundId;
      }
      properties.Assign = { people: [{ id: userId }] };
    }

    const page = await notion.pages.create({
      parent: { database_id: databaseId },
      properties,
    });

    if (values.json) {
      console.log(JSON.stringify(page, null, 2));
    } else {
      console.log('✓ Task created');
      console.log(`  ID: ${page.id}`);
      console.log(`  Title: ${values.title}`);
      if (values.due) console.log(`  Due: ${values.due}`);
      console.log(`  URL: ${(page as any).url}`);
    }
  } catch (error: any) {
    console.error('Error:', JSON.stringify(error, null, 2));
    process.exit(1);
  }
}

main();
