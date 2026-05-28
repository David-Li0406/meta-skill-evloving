/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

/**
 * Workspace state type definitions.
 *
 * A workspace is a mutable working copy of a package. The state tracks:
 * - Which package was deployed (immutable reference via hash)
 * - When the deployment occurred
 * - Current root data tree hash
 * - When the root was last updated
 *
 * State file location: workspaces/<name>/state.beast2
 * No state file = workspace exists but not yet deployed.
 */

import { StructType, StringType, DateTimeType, ValueTypeOf } from '@elaraai/east';

/**
 * Workspace state stored in workspaces/<name>/state.beast2
 *
 * Contains both deployment info and current data root in a single
 * atomic unit to ensure consistency.
 *
 * Future audit trail support:
 * When we implement full audit trail, this state will move to the object
 * store (content-addressed) with a ref file pointing to current state hash.
 * Additional fields for the Merkle chain:
 *
 *   previousStateHash: NullableType(StringType),  // null for initial deploy
 *   message: StringType,  // "deployed package X", "user Y wrote to dataset Z"
 *
 * This gives a complete history of workspace changes, similar to git commits.
 */
export const WorkspaceStateType = StructType({
  /** Name of the deployed package */
  packageName: StringType,
  /** Version of the deployed package */
  packageVersion: StringType,
  /** Hash of the package object at deploy time (immutable reference) */
  packageHash: StringType,
  /** UTC datetime when the package was deployed */
  deployedAt: DateTimeType,
  /** Current root data tree hash */
  rootHash: StringType,
  /** UTC datetime when root was last updated */
  rootUpdatedAt: DateTimeType,
});

export type WorkspaceState = ValueTypeOf<typeof WorkspaceStateType>;
