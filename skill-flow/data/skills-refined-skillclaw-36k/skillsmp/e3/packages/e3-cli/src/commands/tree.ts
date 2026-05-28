/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Licensed under BSL 1.1. See LICENSE for details.
 */

/**
 * e3 tree command - Show full tree structure of a workspace
 *
 * Usage:
 *   e3 tree . dev                 # Full tree for workspace
 *   e3 tree . dev.tasks           # Tree from subtree
 *   e3 tree . dev --depth 2       # Limit depth
 *   e3 tree . dev --types         # Show dataset types
 */

import { workspaceGetTree, type TreeNode, LocalStorage } from '@elaraai/e3-core';
import { printFor, EastTypeType } from '@elaraai/east';
import { datasetListRecursive as datasetListRecursiveRemote, type DatasetListItem } from '@elaraai/e3-api-client';
import { parseRepoLocation, parseDatasetPath, formatError, exitError } from '../utils.js';

// Printer for type values (decoded types are EastTypeValue, not EastType)
const printTypeValue = printFor(EastTypeType);

interface TreeOptions {
  depth?: string;
  types?: boolean;
}

/**
 * Render tree nodes with box-drawing characters.
 */
function renderTree(nodes: TreeNode[], prefix: string = '', showTypes: boolean = false): string[] {
  const lines: string[] = [];

  for (let i = 0; i < nodes.length; i++) {
    const node = nodes[i]!;
    const isLast = i === nodes.length - 1;
    const connector = isLast ? '└── ' : '├── ';
    const childPrefix = isLast ? '    ' : '│   ';

    // Format node name with optional type
    let nodeName = node.name;
    if (showTypes && node.kind === 'dataset' && node.datasetType) {
      try {
        nodeName += ` (${printTypeValue(node.datasetType)})`;
      } catch {
        nodeName += ' (?)';
      }
    }

    lines.push(prefix + connector + nodeName);

    // Recurse into children (only tree nodes have children)
    if (node.kind === 'tree' && node.children.length > 0) {
      const childLines = renderTree(node.children, prefix + childPrefix, showTypes);
      lines.push(...childLines);
    }
  }

  return lines;
}

/**
 * Build tree structure from flat dataset list.
 */
interface FlatTreeNode {
  name: string;
  type?: string;
  children: Map<string, FlatTreeNode>;
  isDataset: boolean;
}

function buildTreeFromFlat(items: DatasetListItem[], showTypes: boolean): FlatTreeNode {
  const root: FlatTreeNode = { name: '', children: new Map(), isDataset: false };

  for (const item of items) {
    // Path is like ".inputs.a.x" - split into segments
    const segments = item.path.split('.').filter(s => s !== '');
    let current = root;

    for (let i = 0; i < segments.length; i++) {
      const segment = segments[i]!;
      const isLast = i === segments.length - 1;

      if (!current.children.has(segment)) {
        current.children.set(segment, {
          name: segment,
          children: new Map(),
          isDataset: false,
        });
      }

      const node = current.children.get(segment)!;
      if (isLast) {
        node.isDataset = true;
        if (showTypes) {
          try {
            node.type = printTypeValue(item.type);
          } catch {
            node.type = '?';
          }
        }
      }
      current = node;
    }
  }

  return root;
}

/**
 * Render flat tree structure with box-drawing characters.
 */
function renderFlatTree(node: FlatTreeNode, prefix: string = '', showTypes: boolean = false): string[] {
  const lines: string[] = [];
  const children = Array.from(node.children.values());

  for (let i = 0; i < children.length; i++) {
    const child = children[i]!;
    const isLast = i === children.length - 1;
    const connector = isLast ? '└── ' : '├── ';
    const childPrefix = isLast ? '    ' : '│   ';

    let nodeName = child.name;
    if (showTypes && child.isDataset && child.type) {
      nodeName += ` (${child.type})`;
    }

    lines.push(prefix + connector + nodeName);

    // Recurse into children
    if (child.children.size > 0) {
      const childLines = renderFlatTree(child, prefix + childPrefix, showTypes);
      lines.push(...childLines);
    }
  }

  return lines;
}

/**
 * Show full tree structure of a workspace.
 */
export async function treeCommand(
  repoArg: string,
  pathSpec: string,
  options: TreeOptions
): Promise<void> {
  try {
    const location = await parseRepoLocation(repoArg);
    const { ws, path } = parseDatasetPath(pathSpec);

    const maxDepth = options.depth !== undefined ? parseInt(options.depth, 10) : undefined;
    const includeTypes = options.types ?? false;

    if (location.type === 'local') {
      const storage = new LocalStorage();

      const nodes = await workspaceGetTree(storage, location.path, ws, path, {
        maxDepth,
        includeTypes,
      });

      if (nodes.length === 0) {
        console.log('(empty)');
        return;
      }

      // Print root path
      console.log(pathSpec);

      // Render and print tree
      const lines = renderTree(nodes, '', includeTypes);
      for (const line of lines) {
        console.log(line);
      }
    } else {
      // Remote: use flat list and build tree
      const items = await datasetListRecursiveRemote(
        location.baseUrl,
        location.repo,
        ws,
        path,
        { token: location.token }
      );

      if (items.length === 0) {
        console.log('(empty)');
        return;
      }

      // Print root path
      console.log(pathSpec);

      // Build tree from flat list and render
      const tree = buildTreeFromFlat(items, includeTypes);

      // Apply depth limit if specified
      const lines = renderFlatTree(tree, '', includeTypes);

      // Apply depth filter if needed
      if (maxDepth !== undefined) {
        const filteredLines: string[] = [];
        for (const line of lines) {
          // Count depth by counting connector patterns
          const depth = (line.match(/[├└]/g) || []).length;
          if (depth <= maxDepth) {
            filteredLines.push(line);
          }
        }
        for (const line of filteredLines) {
          console.log(line);
        }
      } else {
        for (const line of lines) {
          console.log(line);
        }
      }
    }
  } catch (err) {
    exitError(formatError(err));
  }
}
