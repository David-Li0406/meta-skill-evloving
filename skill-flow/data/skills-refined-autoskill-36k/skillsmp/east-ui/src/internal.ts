/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

/**
 * Internal exports for east-ui-react and other internal consumers.
 *
 * @remarks
 * This module exports all types and utilities, including those not part
 * of the public API but needed by internal packages like east-ui-react.
 *
 * @internal
 * @packageDocumentation
 */

// Re-export public API
export * from "./index.js";

// Typography
export * from "./typography/index.js";

// Layout
export * from "./layout/index.js";
export * from "./layout/box/types.js";
export * from "./layout/stack/types.js";
export * from "./layout/grid/types.js";
export * from "./layout/separator/types.js";
export * from "./layout/splitter/types.js";

// Buttons
export * from "./buttons/index.js";
export * from "./buttons/button/types.js";

// Forms
export * from "./forms/index.js";
export * from "./forms/input/types.js";
export * from "./forms/checkbox/types.js";
export * from "./forms/switch/types.js";
export * from "./forms/select/types.js";
export * from "./forms/slider/types.js";
export * from "./forms/field/types.js";
export * from "./forms/file-upload/types.js";
export * from "./forms/textarea/types.js";
export * from "./forms/tags-input/types.js";

// Feedback
export * from "./feedback/index.js";
export * from "./feedback/alert/types.js";
export * from "./feedback/progress/types.js";

// Display
export * from "./display/index.js";
export * from "./display/avatar/types.js";
export * from "./display/badge/types.js";
export * from "./display/stat/types.js";
export * from "./display/tag/types.js";

// Container
export * from "./container/index.js";
export * from "./container/card/types.js";

// Collections
export * from "./collections/index.js";
export * from "./collections/data-list/types.js";
export * from "./collections/table/types.js";
export * from "./collections/tree-view/types.js";

// Charts
export * from "./charts/index.js";
export * from "./charts/types.js";
export * from "./charts/sparkline/types.js";
export * from "./charts/area/types.js";
export * from "./charts/bar/types.js";
export * from "./charts/line/types.js";
export * from "./charts/scatter/types.js";
export * from "./charts/pie/types.js";
export * from "./charts/radar/types.js";
export * from "./charts/bar-list/types.js";
export * from "./charts/bar-segment/types.js";

// Disclosure
export * from "./disclosure/index.js";
export * from "./disclosure/accordion/types.js";
export * from "./disclosure/carousel/types.js";

// Overlays
export * from "./overlays/index.js";
export * from "./overlays/tooltip/types.js";
export * from "./overlays/menu/types.js";
