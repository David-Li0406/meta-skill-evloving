/**
 * Disclosure TypeDoc Examples
 *
 * This file contains compilable versions of all TypeDoc @example blocks
 * from the disclosure module (Accordion, Carousel, Tabs).
 *
 * Each example is compiled AND executed to verify correctness.
 *
 * Format: Each example has a comment indicating:
 *   - File path
 *   - Export property (e.g., Accordion.Root, Accordion.Item, Carousel.Root, Tabs.Root)
 */

import { East } from "@elaraai/east";
import { Accordion, Box, Carousel, Tabs, Text, UIComponentType } from "../src/index.js";

// ============================================================================
// ACCORDION
// ============================================================================

// File: src/disclosure/accordion/index.ts
// Export: createAccordionItem (private function)
const accordionItemExample = East.function([], UIComponentType, $ => {
    return Accordion.Root([
        Accordion.Item("section-1", "Section 1", [
            Text.Root("Content for section 1"),
        ]),
        Accordion.Item("section-2", "Section 2", [
            Text.Root("Content for section 2"),
        ], { disabled: true }),
    ]);
});
accordionItemExample.toIR().compile([])();

// File: src/disclosure/accordion/index.ts
// Export: createAccordionRoot (private function)
const accordionRootExample = East.function([], UIComponentType, $ => {
    return Accordion.Root([
        Accordion.Item("q1", "What is East UI?", [
            Text.Root("East UI is a typed UI library."),
        ]),
        Accordion.Item("q2", "How do I install it?", [
            Text.Root("Run npm install @elaraai/east-ui"),
        ]),
    ], {
        multiple: true,
        variant: "enclosed",
    });
});
accordionRootExample.toIR().compile([])();

// File: src/disclosure/accordion/index.ts
// Export: Accordion.Root
const accordionDotRootExample = East.function([], UIComponentType, $ => {
    return Accordion.Root([
        Accordion.Item("section-1", "Section 1", [Text.Root("Content 1")]),
        Accordion.Item("section-2", "Section 2", [Text.Root("Content 2")]),
    ], {
        variant: "enclosed",
        collapsible: true,
    });
});
accordionDotRootExample.toIR().compile([])();

// File: src/disclosure/accordion/index.ts
// Export: Accordion.Item
const accordionDotItemExample = East.function([], UIComponentType, $ => {
    return Accordion.Root([
        Accordion.Item("faq-1", "What is East UI?", [
            Text.Root("East UI is a typed UI component library."),
        ]),
    ]);
});
accordionDotItemExample.toIR().compile([])();

// ============================================================================
// CAROUSEL
// ============================================================================

// File: src/disclosure/carousel/index.ts
// Export: createCarousel (private function)
const carouselRootExample = East.function([], UIComponentType, $ => {
    return Carousel.Root([
        Box.Root([Text.Root("Slide 1")]),
        Box.Root([Text.Root("Slide 2")]),
        Box.Root([Text.Root("Slide 3")]),
    ], {
        loop: true,
        showIndicators: true,
        showControls: true,
    });
});
carouselRootExample.toIR().compile([])();

// File: src/disclosure/carousel/index.ts
// Export: Carousel.Root
const carouselDotRootExample = East.function([], UIComponentType, $ => {
    return Carousel.Root([
        Box.Root([Text.Root("Slide 1")]),
        Box.Root([Text.Root("Slide 2")]),
    ], {
        showControls: true,
        showIndicators: true,
    });
});
carouselDotRootExample.toIR().compile([])();

// ============================================================================
// TABS
// ============================================================================

// File: src/disclosure/tabs/index.ts
// Export: createTabsItem (private function)
const tabsItemExample = East.function([], UIComponentType, $ => {
    return Tabs.Root([
        Tabs.Item("overview", "Overview", [Text.Root("Overview content")]),
        Tabs.Item("disabled", "Disabled Tab", [Text.Root("Disabled")], { disabled: true }),
    ]);
});
tabsItemExample.toIR().compile([])();

// File: src/disclosure/tabs/index.ts
// Export: createTabsRoot (private function)
const tabsRootExample = East.function([], UIComponentType, $ => {
    return Tabs.Root([
        Tabs.Item("overview", "Overview", [Text.Root("Overview content")]),
        Tabs.Item("settings", "Settings", [Text.Root("Settings content")]),
    ], {
        defaultValue: "overview",
        variant: "line",
    });
});
tabsRootExample.toIR().compile([])();

// File: src/disclosure/tabs/index.ts
// Export: Tabs.Root
const tabsDotRootExample = East.function([], UIComponentType, $ => {
    return Tabs.Root([
        Tabs.Item("tab1", "Overview", [Text.Root("Overview content")]),
        Tabs.Item("tab2", "Details", [Text.Root("Details content")]),
    ], {
        variant: "line",
        fitted: true,
    });
});
tabsDotRootExample.toIR().compile([])();

// File: src/disclosure/tabs/index.ts
// Export: Tabs.Item
const tabsDotItemExample = East.function([], UIComponentType, $ => {
    return Tabs.Root([
        Tabs.Item("overview", "Overview", [
            Text.Root("Overview content here"),
        ]),
        Tabs.Item("disabled", "Disabled Tab", [
            Text.Root("This tab is disabled"),
        ], {
            disabled: true,
        }),
    ], {
        defaultValue: "overview",
    });
});
tabsDotItemExample.toIR().compile([])();

// File: src/disclosure/tabs/index.ts
// Export: Tabs.Variant
const tabsVariantExample = East.function([], UIComponentType, $ => {
    return Tabs.Root([
        Tabs.Item("tab1", "Tab 1", [Text.Root("Content")]),
    ], {
        variant: Tabs.Variant("enclosed"),
    });
});
tabsVariantExample.toIR().compile([])();

console.log("Disclosure TypeDoc examples compiled and executed successfully!");
