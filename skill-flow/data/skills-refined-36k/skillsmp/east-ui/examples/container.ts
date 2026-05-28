/**
 * Container TypeDoc Examples
 *
 * This file contains compilable versions of all TypeDoc @example blocks
 * from the container module (Card).
 *
 * Each example is compiled AND executed to verify correctness.
 *
 * Format: Each example has a comment indicating:
 *   - File path
 *   - Export property (e.g., Card.Root)
 */

import { East } from "@elaraai/east";
import { Card, Text, Button, UIComponentType } from "../src/index.js";

// ============================================================================
// CARD
// ============================================================================

// File: src/container/card/index.ts
// Export: createCard (private function)
const cardRootExample = East.function([], UIComponentType, $ => {
    return Card.Root([
        Text.Root("Card content here"),
        Button.Root("Action"),
    ], {
        title: "Card Title",
        description: "A brief description",
        variant: "elevated",
    });
});
cardRootExample.toIR().compile([])();

// File: src/container/card/index.ts
// Export: Card.Root
const cardDotRootExample = East.function([], UIComponentType, $ => {
    return Card.Root([
        Text.Root("Card content here"),
        Button.Root("Action"),
    ], {
        title: "Card Title",
        description: "A brief description",
    });
});
cardDotRootExample.toIR().compile([])();

console.log("Container TypeDoc examples compiled and executed successfully!");
