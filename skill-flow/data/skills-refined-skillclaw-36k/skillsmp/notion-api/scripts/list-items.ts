#!/usr/bin/env tsx
import { Client } from "@notionhq/client";
import { parseArgs } from "util";

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
    database: { type: "string", short: "d" },
    status: { type: "string", short: "s" },
    project: { type: "string", short: "p" },
    assign: { type: "string", short: "a" },
    limit: { type: "string", short: "l", default: "100" },
    json: { type: "boolean", default: false },
  },
});

if (!values.database) {
  console.error(
    'Usage: list-items.ts --database <DB_ID|URL> [--status "Done"] [--project "SOC 2"] [--limit 20]',
  );
  process.exit(1);
}

const databaseId = extractId(values.database);

// Cache for resolved relation titles
const relationCache = new Map<string, string>();

async function resolveRelationTitle(pageId: string): Promise<string> {
  if (relationCache.has(pageId)) return relationCache.get(pageId)!;
  try {
    const page = (await notion.pages.retrieve({ page_id: pageId })) as any;
    const title = getTitle(page.properties);
    relationCache.set(pageId, title);
    return title;
  } catch {
    return "(unknown)";
  }
}

async function findProjectIdByName(name: string): Promise<string | null> {
  // Search for a project page matching the name
  const response = await notion.search({
    query: name,
    filter: { property: "object", value: "page" },
    page_size: 10,
  });

  for (const page of response.results as any[]) {
    const title = getTitle(page.properties);
    if (title.toLowerCase() === name.toLowerCase()) {
      return page.id;
    }
  }
  return null;
}

async function main() {
  const filters: any[] = [];

  if (values.status) {
    filters.push({
      property: "Status",
      status: { equals: values.status },
    });
  }

  // Handle project filter - find project ID first if filtering by name
  let projectFilter: string | null = null;
  if (values.project) {
    const projectId = await findProjectIdByName(values.project);
    if (projectId) {
      filters.push({
        property: "Project",
        relation: { contains: projectId },
      });
    } else {
      // Fall back to client-side filtering
      projectFilter = values.project.toLowerCase();
    }
  }

  if (values.assign) {
    filters.push({
      property: "Assign",
      people: { contains: values.assign },
    });
  }

  const queryParams: any = {
    database_id: databaseId,
    page_size: Math.min(parseInt(values.limit || "100"), 100),
  };

  if (filters.length > 0) {
    queryParams.filter = filters.length === 1 ? filters[0] : { and: filters };
  }

  try {
    const response = await notion.databases.query(queryParams);

    if (values.json) {
      console.log(JSON.stringify(response.results, null, 2));
      return;
    }

    // Format output
    const pages = response.results as any[];
    const results: {
      title: string;
      id: string;
      status: string;
      assignee: string | null;
      project: string | null;
    }[] = [];

    for (const page of pages) {
      const props = page.properties;
      const title = getTitle(props);
      const status = getStatus(props);
      const assignee = getAssignee(props);
      const project = await getProjectAsync(props);

      // Client-side filter if project ID wasn't found
      if (
        projectFilter &&
        project &&
        !project.toLowerCase().includes(projectFilter)
      ) {
        continue;
      }

      results.push({ title, id: page.id, status, assignee, project });
    }

    console.log(`Found ${results.length} items:\n`);

    for (const item of results) {
      console.log(`• ${item.title}`);
      console.log(`  ID: ${item.id}`);
      console.log(`  Status: ${item.status}`);
      if (item.assignee) console.log(`  Assign: ${item.assignee}`);
      if (item.project) console.log(`  Project: ${item.project}`);
      console.log();
    }

    if (response.has_more) {
      console.log(`(More results available, use --limit to increase)`);
    }
  } catch (error: any) {
    console.error("Error:", JSON.stringify(error, null, 2));
    process.exit(1);
  }
}

function getTitle(props: any): string {
  for (const [key, val] of Object.entries(props) as any[]) {
    if (val.type === "title" && val.title?.[0]) {
      return val.title[0].plain_text;
    }
  }
  return "(Untitled)";
}

function getStatus(props: any): string {
  if (props.Status?.status?.name) return props.Status.status.name;
  if (props.Status?.select?.name) return props.Status.select.name;
  return "(No status)";
}

function getAssignee(props: any): string | null {
  if (props.Assign?.people?.[0]?.name) return props.Assign.people[0].name;
  return null;
}

function getProject(props: any): string | null {
  if (props.Project?.select?.name) return props.Project.select.name;
  if (props.Project?.rollup?.array?.[0]?.title?.[0]?.plain_text) {
    return props.Project.rollup.array[0].title[0].plain_text;
  }
  if (props.Project?.relation?.[0]) return "(relation)";
  return null;
}

async function getProjectAsync(props: any): Promise<string | null> {
  if (props.Project?.select?.name) return props.Project.select.name;
  if (props.Project?.rollup?.array?.[0]?.title?.[0]?.plain_text) {
    return props.Project.rollup.array[0].title[0].plain_text;
  }
  if (props.Project?.relation?.[0]?.id) {
    return resolveRelationTitle(props.Project.relation[0].id);
  }
  return null;
}

main();
