/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Licensed under BSL 1.1. See LICENSE for details.
 */

import { NullType, ArrayType, StringType, decodeBeast2, none, toEastTypeValue, isVariant, type EastTypeValue } from '@elaraai/east';
import type { TreePath } from '@elaraai/e3-types';
import {
  workspaceListTree,
  workspaceGetDatasetHash,
  workspaceSetDataset,
  workspaceGetTree,
  type TreeNode,
} from '@elaraai/e3-core';
import type { StorageBackend } from '@elaraai/e3-core';
import { sendSuccess, sendError } from '../beast2.js';
import { errorToVariant } from '../errors.js';
import { DatasetListItemType, type DatasetListItem } from '../types.js';

/**
 * List dataset fields at the given path.
 */
export async function listDatasets(
  storage: StorageBackend,
  repoPath: string,
  workspace: string,
  treePath: TreePath
): Promise<Response> {
  try {
    const fields = await workspaceListTree(storage, repoPath, workspace, treePath);
    return sendSuccess(ArrayType(StringType), fields);
  } catch (err) {
    return sendError(ArrayType(StringType), errorToVariant(err));
  }
}

/**
 * Get dataset value as raw BEAST2 bytes.
 */
export async function getDataset(
  storage: StorageBackend,
  repoPath: string,
  workspace: string,
  treePath: TreePath
): Promise<Response> {
  try {
    if (treePath.length === 0) {
      return sendError(NullType, errorToVariant(new Error('Path required for get')));
    }

    const { refType, hash } = await workspaceGetDatasetHash(storage, repoPath, workspace, treePath);

    if (refType === 'unassigned') {
      return sendError(NullType, errorToVariant(new Error('Dataset is unassigned (pending task output)')));
    }

    if (refType === 'null' || !hash) {
      return sendError(NullType, errorToVariant(new Error('Dataset is null')));
    }

    // Return raw BEAST2 bytes directly from object store
    const data = await storage.objects.read(repoPath, hash);
    return new Response(data, {
      status: 200,
      headers: { 'Content-Type': 'application/beast2' },
    });
  } catch (err) {
    return sendError(NullType, errorToVariant(err));
  }
}

/**
 * Set dataset value from raw BEAST2 bytes.
 */
export async function setDataset(
  storage: StorageBackend,
  repoPath: string,
  workspace: string,
  treePath: TreePath,
  body: Uint8Array
): Promise<Response> {
  try {
    if (treePath.length === 0) {
      return sendError(NullType, errorToVariant(new Error('Path required for set')));
    }

    // Body is raw BEAST2 - decode to get type and value
    const { type, value } = decodeBeast2(body);

    await workspaceSetDataset(storage, repoPath, workspace, treePath, value, type);
    return sendSuccess(NullType, null);
  } catch (err) {
    return sendError(NullType, errorToVariant(err));
  }
}

/**
 * Flatten a tree of nodes into a list of dataset items.
 */
function flattenTree(
  nodes: TreeNode[],
  pathPrefix: string,
  result: DatasetListItem[]
): void {
  for (const node of nodes) {
    const path = pathPrefix ? `${pathPrefix}.${node.name}` : `.${node.name}`;

    if (node.kind === 'dataset') {
      // Leaf node - add to result
      const datasetType = node.datasetType;
      if (datasetType) {
        // Convert EastType to EastTypeValue if needed
        const typeValue: EastTypeValue = isVariant(datasetType)
          ? datasetType as EastTypeValue
          : toEastTypeValue(datasetType);

        result.push({
          path,
          type: typeValue,
          hash: none, // TODO: get hash from tree walk
          size: none, // TODO: get size if needed
        });
      }
    } else if (node.kind === 'tree') {
      // Branch node - recurse
      flattenTree(node.children, path, result);
    }
  }
}

/**
 * List datasets recursively (flat list with paths).
 */
export async function listDatasetsRecursive(
  storage: StorageBackend,
  repoPath: string,
  workspace: string,
  treePath: TreePath
): Promise<Response> {
  try {
    // Get tree with types included
    const nodes = await workspaceGetTree(storage, repoPath, workspace, treePath, {
      includeTypes: true,
    });

    // Build path prefix from treePath
    const pathPrefix = treePath.map(seg => seg.value).join('.');

    // Flatten to list
    const result: DatasetListItem[] = [];
    flattenTree(nodes, pathPrefix ? `.${pathPrefix}` : '', result);

    return sendSuccess(ArrayType(DatasetListItemType), result);
  } catch (err) {
    return sendError(ArrayType(DatasetListItemType), errorToVariant(err));
  }
}
