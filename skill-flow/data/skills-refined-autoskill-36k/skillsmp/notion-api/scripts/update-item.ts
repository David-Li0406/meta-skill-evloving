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
    page: { type: 'string', short: 'p' },
    property: { type: 'string' },
    value: { type: 'string', short: 'v' },
    type: { type: 'string', short: 't' }, // Override type detection
    title: { type: 'string' }, // Shortcut for updating title
    json: { type: 'boolean', default: false },
  },
});

if (!values.page || (!values.title && (!values.property || values.value === undefined))) {
  console.error(`Usage:
  update-item.ts --page <PAGE_ID|URL> --property <PROP_NAME> --value <VALUE> [--type <TYPE>]
  update-item.ts --page <PAGE_ID|URL> --title "New Title"

Property types (auto-detected or specify with --type):
  title, rich_text, number, select, multi_select, status, date, checkbox, url, email, phone_number, people

Examples:
  --property Status --value "Done"
  --property Priority --value "High" --type select
  --property "Due Date" --value "2025-01-20"
  --property Notes --value "Updated notes" --type rich_text
  --property Complete --value true --type checkbox
  --property Assign --value "John Smith"   # people: accepts name or UUID
`);
  process.exit(1);
}

const pageId = extractId(values.page);

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
    // First, get the page to understand property types
    const page = await notion.pages.retrieve({ page_id: pageId }) as any;

    const properties: any = {};

    if (values.title) {
      // Find the title property name
      const titlePropName = Object.entries(page.properties)
        .find(([_, p]: any) => p.type === 'title')?.[0] || 'Name';

      properties[titlePropName] = {
        title: [{ text: { content: values.title } }],
      };
    } else {
      const propName = values.property!;
      const propValue = values.value!;
      const existingProp = page.properties[propName];

      if (!existingProp && !values.type) {
        console.error(`Property "${propName}" not found. Available properties:`);
        for (const [name, prop] of Object.entries(page.properties) as any[]) {
          console.error(`  - ${name} (${prop.type})`);
        }
        process.exit(1);
      }

      const propType = values.type || existingProp?.type;
      properties[propName] = await buildPropertyValue(propType, propValue);
    }
    
    const updated = await notion.pages.update({
      page_id: pageId,
      properties,
    });
    
    if (values.json) {
      console.log(JSON.stringify(updated, null, 2));
    } else {
      console.log('✓ Updated successfully');
      console.log(`  Page ID: ${updated.id}`);
      if (values.title) {
        console.log(`  New title: ${values.title}`);
      } else {
        console.log(`  Property: ${values.property}`);
        console.log(`  New value: ${values.value}`);
      }
    }
    
  } catch (error: any) {
    console.error('Error:', JSON.stringify(error, null, 2));
    process.exit(1);
  }
}

async function buildPropertyValue(type: string, value: string): Promise<any> {
  switch (type) {
    case 'title':
      return { title: [{ text: { content: value } }] };

    case 'rich_text':
      return { rich_text: [{ text: { content: value } }] };

    case 'number':
      return { number: parseFloat(value) };

    case 'select':
      return { select: value ? { name: value } : null };

    case 'multi_select':
      return {
        multi_select: value.split(',').map(v => ({ name: v.trim() }))
      };

    case 'status':
      return { status: { name: value } };

    case 'date':
      // Supports: "2025-01-20" or "2025-01-20 to 2025-01-25"
      if (value.includes(' to ')) {
        const [start, end] = value.split(' to ').map(d => d.trim());
        return { date: { start, end } };
      }
      return { date: value ? { start: value } : null };

    case 'checkbox':
      return { checkbox: value === 'true' || value === '1' || value === 'yes' };

    case 'url':
      return { url: value || null };

    case 'email':
      return { email: value || null };

    case 'phone_number':
      return { phone_number: value || null };

    case 'people': {
      // Value can be comma-separated user IDs or names
      const parts = value.split(',').map(v => v.trim());
      const userIds: { id: string }[] = [];

      for (const part of parts) {
        if (isUuid(part)) {
          userIds.push({ id: part });
        } else {
          // Look up user by name
          const userId = await findUserByName(part);
          if (userId) {
            userIds.push({ id: userId });
          } else {
            console.error(`User not found: "${part}"`);
            process.exit(1);
          }
        }
      }
      return { people: userIds };
    }

    case 'relation':
      // Value should be comma-separated page IDs
      return {
        relation: value.split(',').map(id => ({ id: id.trim() }))
      };

    case 'files':
      // Value should be comma-separated URLs
      return {
        files: value.split(',').map(url => ({
          type: 'external',
          name: url.split('/').pop() || 'file',
          external: { url: url.trim() }
        }))
      };

    default:
      console.error(`Unsupported property type: ${type}`);
      console.error('Supported: title, rich_text, number, select, multi_select, status, date, checkbox, url, email, phone_number, people, relation, files');
      process.exit(1);
  }
}

main();
