/**
 * Display TypeDoc Examples
 *
 * This file contains compilable versions of all TypeDoc @example blocks
 * from the display module (Avatar, Badge, Icon, Stat, Tag).
 *
 * Each example is compiled AND executed to verify correctness.
 *
 * Format: Each example has a comment indicating:
 *   - File path
 *   - Export property (e.g., Avatar.Root, Badge.Root, Icon.Root, Stat.Root, Tag.Root)
 */

import { East } from "@elaraai/east";
import { Avatar, Badge, Icon, Stat, Tag, UIComponentType } from "../src/index.js";

// ============================================================================
// AVATAR
// ============================================================================

// File: src/display/avatar/index.ts
// Export: createAvatar (private function)
const avatarExample = East.function([], UIComponentType, $ => {
    return Avatar.Root({
        name: "Jane Smith",
        colorPalette: "blue",
        size: "lg",
    });
});
avatarExample.toIR().compile([])();

// File: src/display/avatar/index.ts
// Export: Avatar.Root
const avatarRootExample = East.function([], UIComponentType, $ => {
    return Avatar.Root({
        name: "Jane Smith",
        colorPalette: "blue",
    });
});
avatarRootExample.toIR().compile([])();

// ============================================================================
// BADGE
// ============================================================================

// File: src/display/badge/index.ts
// Export: createBadge (private function)
const badgeExample = East.function([], UIComponentType, $ => {
    return Badge.Root("Active", {
        colorPalette: "green",
        variant: "solid",
    });
});
badgeExample.toIR().compile([])();

// File: src/display/badge/index.ts
// Export: Badge.Root
const badgeRootExample = East.function([], UIComponentType, $ => {
    return Badge.Root("Active", {
        colorPalette: "green",
        variant: "solid",
    });
});
badgeRootExample.toIR().compile([])();

// ============================================================================
// ICON
// ============================================================================

// File: src/display/icon/index.ts
// Export: createIcon (private function)
const iconExample = East.function([], UIComponentType, $ => {
    return Icon.Root("fas", "user");
});
iconExample.toIR().compile([])();

// File: src/display/icon/index.ts
// Export: Icon.Root (basic example)
const iconRootExample = East.function([], UIComponentType, $ => {
    return Icon.Root("fas", "user");
});
iconRootExample.toIR().compile([])();

// File: src/display/icon/index.ts
// Export: Icon.Root (styled example)
const iconStyledExample = East.function([], UIComponentType, $ => {
    return Icon.Root("fas", "heart", {
        color: "red.500",
        size: "xl",
    });
});
iconStyledExample.toIR().compile([])();

// ============================================================================
// STAT
// ============================================================================

// File: src/display/stat/index.ts
// Export: createStat (private function)
const statExample = East.function([], UIComponentType, $ => {
    return Stat.Root("Growth", "+23.36%", {
        helpText: "From last week",
        indicator: "up",
    });
});
statExample.toIR().compile([])();

// File: src/display/stat/index.ts
// Export: Stat.Root
const statRootExample = East.function([], UIComponentType, $ => {
    return Stat.Root("Growth", "+23.36%", {
        helpText: "From last week",
        indicator: "up",
    });
});
statRootExample.toIR().compile([])();

// File: src/display/stat/index.ts
// Export: Stat.Indicator
const statIndicatorExample = East.function([], UIComponentType, $ => {
    return Stat.Root("Revenue", "$45,231", {
        helpText: "+20.1%",
        indicator: Stat.Indicator("up"),
    });
});
statIndicatorExample.toIR().compile([])();

// File: src/display/stat/types.ts
// Export: StatIndicator
const statIndicatorTypesExample = East.function([], UIComponentType, $ => {
    return Stat.Root("Revenue", "$45,231", {
        helpText: "+20.1%",
        indicator: Stat.Indicator("up"),
    });
});
statIndicatorTypesExample.toIR().compile([])();

// ============================================================================
// TAG
// ============================================================================

// File: src/display/tag/index.ts
// Export: createTag (private function)
const tagExample = East.function([], UIComponentType, $ => {
    return Tag.Root("Featured", {
        colorPalette: "blue",
        variant: "solid",
    });
});
tagExample.toIR().compile([])();

// File: src/display/tag/index.ts
// Export: Tag.Root
const tagRootExample = East.function([], UIComponentType, $ => {
    return Tag.Root("Featured", {
        colorPalette: "blue",
        variant: "solid",
    });
});
tagRootExample.toIR().compile([])();

console.log("Display TypeDoc examples compiled and executed successfully!");
