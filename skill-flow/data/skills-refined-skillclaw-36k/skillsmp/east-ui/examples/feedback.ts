/**
 * Feedback TypeDoc Examples
 *
 * This file contains compilable versions of all TypeDoc @example blocks
 * from the feedback module (Alert, Progress).
 *
 * Each example is compiled AND executed to verify correctness.
 *
 * Format: Each example has a comment indicating:
 *   - File path
 *   - Export property (e.g., Alert.Root, Progress.Root)
 */

import { East } from "@elaraai/east";
import { Alert, Progress, UIComponentType } from "../src/index.js";

// ============================================================================
// ALERT
// ============================================================================

// File: src/feedback/alert/index.ts
// Export: createAlert (private function)
const alertExample = East.function([], UIComponentType, $ => {
    return Alert.Root("warning", {
        title: "Warning",
        description: "Your session will expire in 5 minutes",
    });
});
alertExample.toIR().compile([])();

// File: src/feedback/alert/index.ts
// Export: Alert.Root
const alertRootExample = East.function([], UIComponentType, $ => {
    return Alert.Root("warning", {
        title: "Warning",
        description: "Your session will expire in 5 minutes",
    });
});
alertRootExample.toIR().compile([])();

// File: src/feedback/alert/types.ts
// Export: AlertStatus
const alertStatusExample = East.function([], UIComponentType, $ => {
    return Alert.Root(Alert.Status("success"), {
        title: "Saved!",
    });
});
alertStatusExample.toIR().compile([])();

// File: src/feedback/alert/types.ts
// Export: AlertVariant
const alertVariantExample = East.function([], UIComponentType, $ => {
    return Alert.Root("info", {
        title: "Info",
        variant: Alert.Variant("subtle"),
    });
});
alertVariantExample.toIR().compile([])();

// ============================================================================
// PROGRESS
// ============================================================================

// File: src/feedback/progress/index.ts
// Export: createProgress (private function)
const progressExample = East.function([], UIComponentType, $ => {
    return Progress.Root(60.0, {
        colorPalette: "green",
        size: "md",
        striped: true,
    });
});
progressExample.toIR().compile([])();

// File: src/feedback/progress/index.ts
// Export: Progress.Root
const progressRootExample = East.function([], UIComponentType, $ => {
    return Progress.Root(60.0, {
        colorPalette: "green",
        size: "md",
        striped: true,
    });
});
progressRootExample.toIR().compile([])();

// File: src/feedback/progress/types.ts
// Export: ProgressVariant
const progressVariantExample = East.function([], UIComponentType, $ => {
    return Progress.Root(50.0, {
        variant: Progress.Variant("subtle"),
    });
});
progressVariantExample.toIR().compile([])();

console.log("Feedback TypeDoc examples compiled and executed successfully!");
