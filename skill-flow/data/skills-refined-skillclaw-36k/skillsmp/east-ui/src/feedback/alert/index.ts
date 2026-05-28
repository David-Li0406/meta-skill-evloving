/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

import {
    type ExprType,
    type SubtypeExprOrValue,
    East,
    StringType,
    variant,
} from "@elaraai/east";

import { UIComponentType } from "../../component.js";
import {
    AlertType,
    AlertStatusType,
    AlertStatus,
    AlertVariantType,
    AlertVariant,
    type AlertStyle,
    type AlertStatusLiteral,
} from "./types.js";

// Re-export types
export {
    AlertType,
    AlertStatusType,
    AlertStatus,
    AlertVariantType,
    AlertVariant,
    type AlertStyle,
    type AlertStatusLiteral,
    type AlertVariantLiteral,
} from "./types.js";

// ============================================================================
// Alert Function
// ============================================================================

/**
 * Creates an Alert component with status and optional styling.
 *
 * @param status - The alert status (info, warning, success, error)
 * @param style - Optional styling configuration
 * @returns An East expression representing the alert component
 *
 * @remarks
 * Alert is used to display feedback messages to users. Different status
 * types have appropriate color schemes (blue for info, yellow for warning,
 * green for success, red for error).
 *
 * @example
 * ```ts
 * import { East } from "@elaraai/east";
 * import { Alert, UIComponentType } from "@elaraai/east-ui";
 *
 * const example = East.function([], UIComponentType, $ => {
 *     return Alert.Root("warning", {
 *         title: "Warning",
 *         description: "Your session will expire in 5 minutes",
 *     });
 * });
 * ```
 */
function createAlert(
    status: SubtypeExprOrValue<AlertStatusType> | AlertStatusLiteral,
    style?: AlertStyle
): ExprType<UIComponentType> {
    const toStringOption = (val: SubtypeExprOrValue<StringType> | undefined) => {
        if (val === undefined) return variant("none", null);
        return variant("some", val);
    };

    const statusValue = typeof status === "string"
        ? East.value(variant(status, null), AlertStatusType)
        : status;

    const variantValue = style?.variant
        ? (typeof style.variant === "string"
            ? East.value(variant(style.variant, null), AlertVariantType)
            : style.variant)
        : undefined;

    return East.value(variant("Alert", {
        status: statusValue,
        title: toStringOption(style?.title),
        description: toStringOption(style?.description),
        variant: variantValue ? variant("some", variantValue) : variant("none", null),
    }), UIComponentType);
}

/**
 * Alert component for displaying feedback messages.
 *
 * @remarks
 * Use `Alert.Root(status, style)` to create an alert, or access `Alert.Types.Alert` for the East type.
 */
export const Alert = {
    /**
     * Creates an Alert component with status and optional styling.
     *
     * @param status - The alert status (info, warning, success, error) or AlertStatusType expression
     * @param style - Optional styling configuration
     * @returns An East expression representing the alert component
     *
     * @remarks
     * Alert is used to display feedback messages to users. Different status
     * types have appropriate color schemes (blue for info, yellow for warning,
     * green for success, red for error).
     *
     * @example
     * ```ts
     * import { East } from "@elaraai/east";
     * import { Alert, UIComponentType } from "@elaraai/east-ui";
     *
     * const example = East.function([], UIComponentType, $ => {
     *     return Alert.Root("warning", {
     *         title: "Warning",
     *         description: "Your session will expire in 5 minutes",
     *     });
     * });
     * ```
     */
    Root: createAlert,
    /**
     * Helper function to create alert status values.
     *
     * @param status - The status string ("info", "warning", "success", "error")
     * @returns An East expression representing the alert status
     */
    Status: AlertStatus,
    /**
     * Helper function to create alert variant values.
     *
     * @param v - The variant string ("solid", "subtle", "outline")
     * @returns An East expression representing the alert variant
     */
    Variant: AlertVariant,
    Types: {
        /**
         * Type for Alert component data.
         *
         * @remarks
         * Alert displays feedback messages to users, indicating status of
         * operations or important information.
         *
         * @property status - The status type (info, warning, success, error)
         * @property title - Optional alert title
         * @property description - Optional alert description
         * @property variant - Visual variant (solid, subtle, outline)
         */
        Alert: AlertType,
        /**
         * Status types for Alert component.
         *
         * @property info - Informational alert
         * @property warning - Warning alert
         * @property success - Success/confirmation alert
         * @property error - Error/danger alert
         */
        Status: AlertStatusType,
        /**
         * Variant types for Alert visual style.
         *
         * @property solid - Solid background alert
         * @property subtle - Subtle/light background alert
         * @property outline - Bordered alert
         */
        Variant: AlertVariantType,
    },
} as const;
