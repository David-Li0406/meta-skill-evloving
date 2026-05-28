/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

import {
    type ExprType,
    type SubtypeExprOrValue,
    East,
    OptionType,
    StructType,
    ArrayType,
    StringType,
    BooleanType,
    RecursiveType,
    variant,
    VariantType,
} from "@elaraai/east";

import type { IconName, IconPrefix } from "@fortawesome/fontawesome-common-types";

import {
    TreeViewVariantType,
    TreeViewSizeType,
    TreeViewSelectionModeType,
    TreeViewStyleType,
    type TreeViewStyle,
} from "./types.js";
import { UIComponentType } from "../../component.js";
import {
    IconType,
    IconSizeType,
    IconVariantType,
    IconStyleType,
    type IconStyle,
} from "../../display/icon/types.js";
import { ColorSchemeType } from "../../style.js";

// Re-export style types
export {
    TreeViewVariantType,
    TreeViewSizeType,
    TreeViewSelectionModeType,
    TreeViewStyleType,
    type TreeViewStyle,
} from "./types.js";

// ============================================================================
// TreeNode Type (Recursive)
// ============================================================================

/**
 * Recursive type for tree nodes.
 *
 * @remarks
 * Each node has a value (unique identifier), label (display text),
 * optional indicator icon, and children.
 *
 * @property value - Unique identifier for the node
 * @property label - Display text for the node
 * @property indicator - Optional icon to display before the label
 * @property children - Array of child nodes
 */
export const TreeNodeType = RecursiveType(self => VariantType({
    Item: StructType({
        value: StringType,
        label: StringType,
        indicator: OptionType(IconType),
    }),
    Branch: StructType({
        value: StringType,
        label: StringType,
        indicator: OptionType(IconType),
        children: ArrayType(self),
        disabled: OptionType(BooleanType)
    })
}));

/**
 * Type representing the tree node structure.
 */
export type TreeNodeType = typeof TreeNodeType;

// ============================================================================
// TreeNode Variant Types
// ============================================================================

/**
 * East StructType for a leaf tree node (Item).
 *
 * @remarks
 * Items are leaf nodes in the tree hierarchy that cannot have children.
 * Use {@link TreeView.Item} factory function to create Item nodes.
 *
 * @property value - Unique identifier for the node
 * @property label - Display text for the node
 * @property indicator - Optional icon to display before the label
 */
export const TreeItemNodeType = StructType({
    value: StringType,
    label: StringType,
    indicator: OptionType(IconType),
});

/**
 * Type alias for TreeItemNodeType.
 */
export type TreeItemNodeType = typeof TreeItemNodeType;

/**
 * East StructType for a branch tree node (Branch).
 *
 * @remarks
 * Branches are expandable nodes that can contain child nodes (Items or other Branches).
 * Use {@link TreeView.Branch} factory function to create Branch nodes.
 *
 * @property value - Unique identifier for the node
 * @property label - Display text for the node
 * @property indicator - Optional icon to display before the label
 * @property children - Array of child nodes (Items or Branches)
 * @property disabled - Whether the branch is disabled
 */
export const TreeBranchNodeType = StructType({
    value: StringType,
    label: StringType,
    indicator: OptionType(IconType),
    children: ArrayType(TreeNodeType),
    disabled: OptionType(BooleanType),
});

/**
 * Type alias for TreeBranchNodeType.
 */
export type TreeBranchNodeType = typeof TreeBranchNodeType;

// ============================================================================
// TreeView Root Type
// ============================================================================

/**
 * East type for the complete tree view structure.
 *
 * @remarks
 * Contains the tree nodes, optional label, and styling configuration.
 *
 * @property nodes - Array of root-level tree nodes
 * @property label - Optional label for the tree view
 * @property defaultExpandedValue - Initially expanded node values
 * @property defaultSelectedValue - Initially selected node values
 * @property style - Optional styling configuration
 */
export const TreeViewRootType = StructType({
    nodes: ArrayType(TreeNodeType),
    label: OptionType(StringType),
    defaultExpandedValue: OptionType(ArrayType(StringType)),
    defaultSelectedValue: OptionType(ArrayType(StringType)),
    style: OptionType(TreeViewStyleType),
});

/**
 * Type representing the tree view root structure.
 */
export type TreeViewRootType = typeof TreeViewRootType;

// ============================================================================
// TreeNode Input Interface
// ============================================================================

/**
 * TypeScript interface for creating tree nodes.
 *
 * @remarks
 * Provides a convenient way to create tree node structures.
 *
 * @property value - Unique identifier for the node
 * @property label - Display text for the node
 * @property indicator - Optional icon to display before the label
 * @property children - Optional array of child nodes
 */
export interface TreeNodeInput {
    value: SubtypeExprOrValue<typeof StringType>;
    label: SubtypeExprOrValue<typeof StringType>;
    indicator?: SubtypeExprOrValue<typeof IconType>;
    children?: TreeNodeInput[];
}

// ============================================================================
// TreeNode Factory
// ============================================================================

/**
 * Indicator icon configuration for tree nodes.
 * Extends IconStyle so styling properties are at the top level.
 */
export interface TreeNodeIndicator extends IconStyle {
    /** Font Awesome icon prefix (e.g., "fas", "far", "fab") */
    prefix: IconPrefix;
    /** Font Awesome icon name (e.g., "folder", "file", "file-code") */
    name: IconName;
}

/**
 * Helper to build indicator option value.
 */
function buildIndicatorValue(indicator?: TreeNodeIndicator) {
    if (!indicator) return variant("none", null);

    return variant("some", East.value({
        prefix: indicator.prefix,
        name: indicator.name,
        style: (indicator.size || indicator.variant || indicator.color || indicator.colorPalette)
            ? variant("some", East.value({
                size: indicator.size
                    ? variant("some", typeof indicator.size === "string"
                        ? East.value(variant(indicator.size, null), IconSizeType)
                        : indicator.size)
                    : variant("none", null),
                variant: indicator.variant
                    ? variant("some", typeof indicator.variant === "string"
                        ? East.value(variant(indicator.variant, null), IconVariantType)
                        : indicator.variant)
                    : variant("none", null),
                color: indicator.color ? variant("some", indicator.color) : variant("none", null),
                colorPalette: indicator.colorPalette
                    ? variant("some", typeof indicator.colorPalette === "string"
                        ? East.value(variant(indicator.colorPalette, null), ColorSchemeType)
                        : indicator.colorPalette)
                    : variant("none", null),
            }, IconStyleType))
            : variant("none", null),
    }, IconType));
}

/**
 * Creates a leaf tree node (Item) with no children.
 *
 * @param value - Unique identifier for the node
 * @param label - Display text for the node
 * @param indicator - Optional indicator icon with prefix, name, and styling
 * @returns An East expression representing the tree item
 *
 * @example
 * ```ts
 * import { East } from "@elaraai/east";
 * import { TreeView, UIComponentType } from "@elaraai/east-ui";
 *
 * const example = East.function([], UIComponentType, $ => {
 *     return TreeView.Root([
 *         TreeView.Item("readme", "README.md", { prefix: "far", name: "file" }),
 *         TreeView.Item("index", "index.ts", { prefix: "fas", name: "file-code", color: "blue.500" }),
 *     ]);
 * });
 * ```
 */
function TreeItem(
    value: SubtypeExprOrValue<typeof StringType>,
    label: SubtypeExprOrValue<typeof StringType>,
    indicator?: TreeNodeIndicator
): ExprType<TreeNodeType> {
    return East.value(variant("Item", {
        value: value,
        label: label,
        indicator: buildIndicatorValue(indicator),
    }), TreeNodeType);
}

/**
 * Creates a branch tree node that can contain children.
 *
 * @param value - Unique identifier for the node
 * @param label - Display text for the node
 * @param children - Array of child nodes
 * @param indicator - Optional indicator icon with prefix, name, and styling
 * @param disabled - Whether the branch is disabled
 * @returns An East expression representing the tree branch
 *
 * @example
 * ```ts
 * import { East } from "@elaraai/east";
 * import { TreeView, UIComponentType } from "@elaraai/east-ui";
 *
 * const example = East.function([], UIComponentType, $ => {
 *     return TreeView.Root([
 *         TreeView.Branch("src", "src", [
 *             TreeView.Branch("components", "components", [
 *                 TreeView.Item("button", "Button.tsx"),
 *             ]),
 *             TreeView.Item("index", "index.ts"),
 *         ], { prefix: "fas", name: "folder", color: "yellow.500" }),
 *     ]);
 * });
 * ```
 */
function TreeBranch(
    value: SubtypeExprOrValue<typeof StringType>,
    label: SubtypeExprOrValue<typeof StringType>,
    children: SubtypeExprOrValue<ArrayType<TreeNodeType>>,
    indicator?: TreeNodeIndicator,
    disabled?: SubtypeExprOrValue<typeof BooleanType>
): ExprType<TreeNodeType> {
    return East.value(variant("Branch", {
        value: value,
        label: label,
        indicator: buildIndicatorValue(indicator),
        children: children,
        disabled: disabled !== undefined ? variant("some", disabled) : variant("none", null),
    }), TreeNodeType);
}

// ============================================================================
// TreeView Root Factory
// ============================================================================

/**
 * Creates a TreeView component with nodes and styling.
 *
 * @param nodes - Array of root-level tree nodes (Item or Branch)
 * @param style - Optional styling and configuration
 * @returns An East expression representing the tree view
 *
 * @example
 * ```ts
 * import { East } from "@elaraai/east";
 * import { TreeView, UIComponentType } from "@elaraai/east-ui";
 *
 * const example = East.function([], UIComponentType, $ => {
 *     return TreeView.Root([
 *         TreeView.Branch("src", "src", [
 *             TreeView.Item("index", "index.ts"),
 *             TreeView.Item("utils", "utils.ts"),
 *         ]),
 *         TreeView.Item("package", "package.json"),
 *     ], {
 *         variant: "subtle",
 *         size: "sm",
 *     });
 * });
 * ```
 */
function TreeViewRoot(
    nodes: SubtypeExprOrValue<ArrayType<TreeNodeType>>,
    style?: TreeViewStyle
): ExprType<UIComponentType> {
    const nodes_expr = East.value(nodes, ArrayType(TreeNodeType));
    const sizeValue = style?.size
        ? (typeof style.size === "string"
            ? East.value(variant(style.size, null), TreeViewSizeType)
            : style.size)
        : undefined;

    const variantValue = style?.variant
        ? (typeof style.variant === "string"
            ? East.value(variant(style.variant, null), TreeViewVariantType)
            : style.variant)
        : undefined;

    const selectionModeValue = style?.selectionMode
        ? (typeof style.selectionMode === "string"
            ? East.value(variant(style.selectionMode, null), TreeViewSelectionModeType)
            : style.selectionMode)
        : undefined;

    const toBoolOption = (value: SubtypeExprOrValue<typeof BooleanType> | undefined) => {
        if (value === undefined) return variant("none", null);
        return variant("some", value);
    };

    const toArrayOption = (value: SubtypeExprOrValue<ArrayType<typeof StringType>> | undefined) => {
        if (value === undefined) return variant("none", null);
        return variant("some", value);
    };

    const hasStyle = style && (
        style.size !== undefined ||
        style.variant !== undefined ||
        style.selectionMode !== undefined ||
        style.animateContent !== undefined ||
        style.onExpandedChange !== undefined ||
        style.onSelectionChange !== undefined ||
        style.onFocusChange !== undefined
    );

    return East.value(variant("TreeView", {
        nodes: nodes_expr,
        label: style?.label ? variant("some", style.label) : variant("none", null),
        defaultExpandedValue: toArrayOption(style?.defaultExpandedValue),
        defaultSelectedValue: toArrayOption(style?.defaultSelectedValue),
        style: hasStyle ? variant("some", East.value({
            size: sizeValue ? variant("some", sizeValue) : variant("none", null),
            variant: variantValue ? variant("some", variantValue) : variant("none", null),
            selectionMode: selectionModeValue ? variant("some", selectionModeValue) : variant("none", null),
            animateContent: toBoolOption(style?.animateContent),
            onExpandedChange: style?.onExpandedChange ? variant("some", style.onExpandedChange) : variant("none", null),
            onSelectionChange: style?.onSelectionChange ? variant("some", style.onSelectionChange) : variant("none", null),
            onFocusChange: style?.onFocusChange ? variant("some", style.onFocusChange) : variant("none", null),
        }, TreeViewStyleType)) : variant("none", null),
    }), UIComponentType);
}

// ============================================================================
// TreeView Namespace Export
// ============================================================================

/**
 * TreeView compound component for hierarchical data display.
 *
 * @remarks
 * TreeView displays hierarchical data structures in an expandable tree format.
 * Use TreeView.Item for leaf nodes and TreeView.Branch for expandable nodes.
 */
export const TreeView = {
    /**
     * Creates a TreeView component with nodes and styling.
     *
     * @param nodes - Array of root-level tree nodes (Item or Branch)
     * @param style - Optional styling and configuration
     * @returns An East expression representing the tree view
     *
     * @remarks
     * TreeView displays hierarchical data structures in an expandable tree format.
     * Use TreeView.Item for leaf nodes and TreeView.Branch for expandable nodes.
     *
     * @example
     * ```ts
     * import { East } from "@elaraai/east";
     * import { TreeView, UIComponentType } from "@elaraai/east-ui";
     *
     * const example = East.function([], UIComponentType, $ => {
     *     return TreeView.Root([
     *         TreeView.Branch("src", "src", [
     *             TreeView.Item("index", "index.ts"),
     *             TreeView.Item("utils", "utils.ts"),
     *         ]),
     *         TreeView.Item("package", "package.json"),
     *     ], {
     *         variant: "subtle",
     *         size: "sm",
     *     });
     * });
     * ```
     */
    Root: TreeViewRoot,
    /**
     * Creates a leaf tree node (Item) with no children.
     *
     * @param value - Unique identifier for the node
     * @param label - Display text for the node
     * @param indicator - Optional indicator icon with prefix, name, and styling
     * @returns An East expression representing the tree item
     *
     * @remarks
     * Items are leaf nodes in the tree hierarchy that cannot have children.
     * Use within TreeView.Root or as children of TreeView.Branch.
     *
     * @example
     * ```ts
     * import { East } from "@elaraai/east";
     * import { TreeView, UIComponentType } from "@elaraai/east-ui";
     *
     * const example = East.function([], UIComponentType, $ => {
     *     return TreeView.Root([
     *         TreeView.Item("readme", "README.md", { prefix: "far", name: "file" }),
     *         TreeView.Item("index", "index.ts", { prefix: "fas", name: "file-code", color: "blue.500" }),
     *     ]);
     * });
     * ```
     */
    Item: TreeItem,
    /**
     * Creates a branch tree node that can contain children.
     *
     * @param value - Unique identifier for the node
     * @param label - Display text for the node
     * @param children - Array of child nodes
     * @param indicator - Optional indicator icon with prefix, name, and styling
     * @param disabled - Whether the branch is disabled
     * @returns An East expression representing the tree branch
     *
     * @remarks
     * Branches are expandable nodes that can contain child nodes (Items or other Branches).
     * Use within TreeView.Root or as children of other TreeView.Branch nodes.
     *
     * @example
     * ```ts
     * import { East } from "@elaraai/east";
     * import { TreeView, UIComponentType } from "@elaraai/east-ui";
     *
     * const example = East.function([], UIComponentType, $ => {
     *     return TreeView.Root([
     *         TreeView.Branch("src", "src", [
     *             TreeView.Branch("components", "components", [
     *                 TreeView.Item("button", "Button.tsx"),
     *             ]),
     *             TreeView.Item("index", "index.ts"),
     *         ], { prefix: "fas", name: "folder", color: "yellow.500" }),
     *     ]);
     * });
     * ```
     */
    Branch: TreeBranch,
    Types: {
        /**
         * East type for the complete tree view structure.
         *
         * @remarks
         * Contains the tree nodes, optional label, and styling configuration.
         *
         * @property nodes - Array of root-level tree nodes
         * @property label - Optional label for the tree view
         * @property defaultExpandedValue - Initially expanded node values
         * @property defaultSelectedValue - Initially selected node values
         * @property style - Optional styling configuration
         */
        Root: TreeViewRootType,
        /**
         * Recursive type for tree nodes.
         *
         * @remarks
         * Each node has a value (unique identifier), label (display text),
         * optional indicator icon, and children.
         *
         * @property value - Unique identifier for the node
         * @property label - Display text for the node
         * @property indicator - Optional icon to display before the label
         * @property children - Array of child nodes
         */
        Node: TreeNodeType,
        /**
         * East StructType for a leaf tree node (Item).
         *
         * @remarks
         * Items are leaf nodes in the tree hierarchy that cannot have children.
         * Use {@link TreeView.Item} factory function to create Item nodes.
         *
         * @property value - Unique identifier for the node
         * @property label - Display text for the node
         * @property indicator - Optional icon to display before the label
         */
        ItemNode: TreeItemNodeType,
        /**
         * East StructType for a branch tree node (Branch).
         *
         * @remarks
         * Branches are expandable nodes that can contain child nodes (Items or other Branches).
         * Use {@link TreeView.Branch} factory function to create Branch nodes.
         *
         * @property value - Unique identifier for the node
         * @property label - Display text for the node
         * @property indicator - Optional icon to display before the label
         * @property children - Array of child nodes (Items or Branches)
         * @property disabled - Whether the branch is disabled
         */
        BranchNode: TreeBranchNodeType,
        /**
         * Style type for the tree view root component.
         *
         * @remarks
         * All properties are optional and wrapped in {@link OptionType}.
         *
         * @property size - Tree view size (xs, sm, md)
         * @property variant - Visual variant (subtle or solid)
         * @property selectionMode - Selection behavior (single or multiple)
         * @property animateContent - Whether to animate expand/collapse
         */
        Style: TreeViewStyleType,
        /**
         * TreeView variant type for visual styling.
         *
         * @remarks
         * Create instances using string literals or the variant function.
         *
         * @property subtle - Subtle background on hover/selection
         * @property solid - Solid background on hover/selection
         */
        Variant: TreeViewVariantType,
        /**
         * TreeView size type for controlling node sizing.
         *
         * @remarks
         * TreeView uses its own size type (xs, sm, md) rather than the shared SizeType.
         *
         * @property xs - Extra small size
         * @property sm - Small size
         * @property md - Medium size (default)
         */
        Size: TreeViewSizeType,
        /**
         * TreeView selection mode type.
         *
         * @property single - Only one node can be selected at a time
         * @property multiple - Multiple nodes can be selected
         */
        SelectionMode: TreeViewSelectionModeType,
    },
} as const;
