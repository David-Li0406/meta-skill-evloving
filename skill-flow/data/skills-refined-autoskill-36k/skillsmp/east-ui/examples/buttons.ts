/**
 * Buttons TypeDoc Examples
 *
 * This file contains compilable versions of all TypeDoc @example blocks
 * from the buttons module (Button, IconButton).
 *
 * Each example is compiled AND executed to verify correctness.
 *
 * Format: Each example has a comment indicating:
 *   - File path
 *   - Export property (e.g., Button.Root, IconButton.Root)
 */

import { East } from "@elaraai/east";
import { Button, IconButton, UIComponentType } from "../src/index.js";

// ============================================================================
// BUTTON
// ============================================================================

// File: src/buttons/button/index.ts
// Export: Button.Root (function-level example - validated via East.function)
const buttonRootExample = East.function([], UIComponentType, $ => {
    let counter = $.let(0)
    return Button.Root("Save", {
        variant: "solid",
        colorPalette: "blue",
        size: "md",
        onClick: (_$) => {
            // increment counter
            $.assign(counter, counter.add(1));
        }
    });
});
buttonRootExample.toIR().compile([])();

// ============================================================================
// ICON BUTTON
// ============================================================================

// File: src/buttons/icon-button/index.ts
// Export: IconButton.Root (basic example)
const iconButtonRootExample = East.function([], UIComponentType, $ => {
    return IconButton.Root("fas", "xmark");
});
iconButtonRootExample.toIR().compile([])();

// File: src/buttons/icon-button/index.ts
// Export: IconButton.Root (styled example)
const iconButtonStyledExample = East.function([], UIComponentType, $ => {
    let counter = $.let(0)
    return IconButton.Root("fas", "bars", {
        variant: "ghost",
        size: "lg",
        onClick: (_$) => {
            // increment counter
            $.assign(counter, counter.add(1));
        }
    });
});
iconButtonStyledExample.toIR().compile([])();

console.log("Buttons TypeDoc examples compiled and executed successfully!");
