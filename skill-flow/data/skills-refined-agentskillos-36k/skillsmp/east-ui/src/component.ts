/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

import {
    RecursiveType,
    VariantType,
    ArrayType,
    OptionType,
    StructType,
    StringType,
    IntegerType,
    FloatType,
    BooleanType,
    DictType,
    FunctionType,
    LiteralValueType,
} from "@elaraai/east";

// Typography
import { TextType } from "./typography/text/types.js";
import { CodeType } from "./typography/code/types.js";
import { HeadingType } from "./typography/heading/types.js";
import { LinkType } from "./typography/link/types.js";
import { HighlightType } from "./typography/highlight/types.js";
import { MarkType } from "./typography/mark/types.js";
import { ListType } from "./typography/list/types.js";
import { CodeBlockType } from "./typography/code-block/types.js";

// Layout
import { BoxStyleType } from "./layout/box/types.js";
import { FlexStyleType } from "./layout/flex/types.js";
import { StackStyleType } from "./layout/stack/types.js";
import { SeparatorStyleType } from "./layout/separator/types.js";
import { GridStyleType } from "./layout/grid/types.js";
import { SplitterStyleType } from "./layout/splitter/types.js";

// Buttons
import { ButtonType } from "./buttons/button/types.js";
import { IconButtonType } from "./buttons/icon-button/types.js";
import { CopyButtonType } from "./buttons/copy-button/types.js";

// Forms
import { StringInputType, IntegerInputType, FloatInputType, DateTimeInputType } from "./forms/input/types.js";
import { CheckboxType } from "./forms/checkbox/types.js";
import { FieldType } from "./forms/field/types.js";
import { SwitchType } from "./forms/switch/types.js";
import { SelectRootType } from "./forms/select/types.js";
import { SliderType } from "./forms/slider/types.js";
import { FileUploadType } from "./forms/file-upload/types.js";
import { TextareaType } from "./forms/textarea/types.js";
import { TagsInputRootType } from "./forms/tags-input/types.js";

// Feedback
import { ProgressType } from "./feedback/progress/types.js";
import { AlertType } from "./feedback/alert/types.js";

// Display
import { BadgeType } from "./display/badge/types.js";
import { TagType } from "./display/tag/types.js";
import { AvatarType } from "./display/avatar/types.js";
import { CardStyleType } from "./container/card/types.js";
import { StatType } from "./display/stat/types.js";
import { IconType } from "./display/icon/types.js";

// Collections
import { DataListRootType } from "./collections/data-list/index.js";
import { TableColumnType, TableStyleType } from "./collections/table/types.js";
import { GanttEventType, GanttStyleType } from "./collections/gantt/types.js";
import { PlannerStyleType, PlannerEventType, EventPopoverContextType } from "./collections/planner/types.js";
// import { TreeViewStyleType } from "./collections/tree-view/types.js";

// Charts
import { SparklineType } from "./charts/sparkline/types.js";
import { AreaChartType, AreaRangeChartType } from "./charts/area/types.js";
import { BarChartType } from "./charts/bar/types.js";
import { LineChartType } from "./charts/line/types.js";
import { ScatterChartType } from "./charts/scatter/types.js";
import { PieChartType } from "./charts/pie/types.js";
import { RadarChartType } from "./charts/radar/types.js";
import { BarListType } from "./charts/bar-list/types.js";
import { BarSegmentType } from "./charts/bar-segment/types.js";
import { ComposedChartType } from "./charts/composed/types.js";

// Disclosure
import { AccordionStyleType } from "./disclosure/accordion/types.js";
import { CarouselStyleType } from "./disclosure/carousel/types.js";
import { TabsStyleType } from "./disclosure/tabs/types.js";

// Overlays
import { PlacementType } from "./overlays/tooltip/types.js";
import { MenuItemType } from "./overlays/menu/types.js";
import { TreeViewStyleType } from "./collections/tree-view/types.js";
import { DialogStyleType } from "./overlays/dialog/types.js";
import { DrawerStyleType } from "./overlays/drawer/types.js";
import { PopoverStyleType } from "./overlays/popover/types.js";
import { HoverCardStyleType } from "./overlays/hover-card/types.js";
import { ActionBarItemType, ActionBarStyleType } from "./overlays/action-bar/types.js";
import { ToggleTipStyleType } from "./overlays/toggle-tip/types.js";

/**
 * Recursive type representing any UI component in East UI.
 *
 * @remarks
 * This is a discriminated union of all available UI components.
 * The recursive structure allows container components (Box, Stack, Card)
 * to have children that are also UIComponentType.
 *
 * The `node` parameter in the RecursiveType callback represents
 * UIComponentType itself, enabling recursive children definitions.
 *
 * As new components are added, they should be registered here:
 * - Leaf components: just add their type directly
 * - Container components: use `ArrayType(node)` for children
 *
 * @property Text - Text component for displaying styled text (leaf)
 * @property Button - Button component for interactive actions (leaf)
 * @property Box - Box component for general-purpose layout (container with children)
 * @property Stack - Stack component for flex-based layout (container with children)
 * @property Separator - Separator component for visual dividers (leaf)
 * @property Grid - Grid component for CSS grid layouts (container with items)
 * @property Splitter - Splitter component for resizable panel layouts (container with panels)
 * @property StringInput - String input component for text entry (leaf)
 * @property IntegerInput - Integer input component for whole numbers (leaf)
 * @property FloatInput - Float input component for decimal numbers (leaf)
 * @property DateTimeInput - DateTime input component for date/time entry (leaf)
 * @property Checkbox - Checkbox component for boolean input (leaf)
 * @property Switch - Switch component for toggle input (leaf)
 * @property Select - Select component for dropdown selection (leaf)
 * @property Slider - Slider component for numeric range selection (leaf)
 * @property Field - Field component for form control wrappers (container with control)
 * @property Progress - Progress component for showing completion (leaf)
 * @property Alert - Alert component for feedback messages (leaf)
 * @property Badge - Badge component for labels and counts (leaf)
 * @property Tag - Tag component for categorization (leaf)
 * @property Avatar - Avatar component for user images (leaf)
 * @property Card - Card component for content containers (container with body)
 * @property Stat - Stat component for metric display (leaf)
 * @property DataList - DataList component for label-value pairs (leaf)
 * @property Table - Table component for data display (leaf)
 * @property TreeView - TreeView component for hierarchical data (leaf)
 * @property Accordion - Accordion component for collapsible panels (container with content children)
 * @property Sparkline - Sparkline component for compact inline charts (leaf)
 */
export const UIComponentType = RecursiveType(node => VariantType({
    // Typography
    Text: TextType,
    Code: CodeType,
    Heading: HeadingType,
    Link: LinkType,
    Highlight: HighlightType,
    Mark: MarkType,
    List: ListType,
    CodeBlock: CodeBlockType,

    // Buttons
    Button: ButtonType,
    IconButton: IconButtonType,
    CopyButton: CopyButtonType,

    // Layout - Containers
    Box: StructType({
        children: ArrayType(node),
        style: OptionType(BoxStyleType),
    }),

    Flex: StructType({
        children: ArrayType(node),
        style: OptionType(FlexStyleType),
    }),

    Stack: StructType({
        children: ArrayType(node),
        style: OptionType(StackStyleType),
    }),

    Separator: SeparatorStyleType,

    Grid: StructType({
        items: ArrayType(StructType({
            content: node,
            colSpan: OptionType(StringType),
            rowSpan: OptionType(StringType),
            colStart: OptionType(StringType),
            colEnd: OptionType(StringType),
            rowStart: OptionType(StringType),
            rowEnd: OptionType(StringType),
        })),
        style: OptionType(GridStyleType),
    }),

    Splitter: StructType({
        panels: ArrayType(StructType({
            id: StringType,
            content: node,
            minSize: OptionType(FloatType),
            maxSize: OptionType(FloatType),
            collapsible: OptionType(BooleanType),
            defaultCollapsed: OptionType(BooleanType),
        })),
        defaultSize: ArrayType(FloatType),
        style: OptionType(SplitterStyleType),
    }),


    // Forms
    StringInput: StringInputType,
    IntegerInput: IntegerInputType,
    FloatInput: FloatInputType,
    DateTimeInput: DateTimeInputType,
    Checkbox: CheckboxType,
    Switch: SwitchType,
    Select: SelectRootType,
    Slider: SliderType,
    FileUpload: FileUploadType,
    Field: FieldType,
    Textarea: TextareaType,
    TagsInput: TagsInputRootType,

    // Feedback
    Progress: ProgressType,
    Alert: AlertType,

    // Display
    Badge: BadgeType,
    Tag: TagType,
    Avatar: AvatarType,
    Stat: StatType,
    Icon: IconType,

    // Container
    Card: StructType({
        header: OptionType(node),
        body: ArrayType(node),
        footer: OptionType(node),
        style: OptionType(CardStyleType),
    }),
    DataList: DataListRootType,

    // Charts
    Sparkline: SparklineType,
    AreaChart: AreaChartType,
    AreaRangeChart: AreaRangeChartType,
    BarChart: BarChartType,
    LineChart: LineChartType,
    ScatterChart: ScatterChartType,
    PieChart: PieChartType,
    RadarChart: RadarChartType,
    BarList: BarListType,
    BarSegment: BarSegmentType,
    ComposedChart: ComposedChartType,

    TreeView: StructType({
        nodes: ArrayType(RecursiveType(inner => VariantType({
            Item: StructType({
                value: StringType,
                label: StringType,
                indicator: OptionType(IconType),
            }),
            Branch: StructType({
                value: StringType,
                label: StringType,
                indicator: OptionType(IconType),
                children: ArrayType(inner),
                disabled: OptionType(BooleanType),
            }),
        }))),
        label: OptionType(StringType),
        defaultExpandedValue: OptionType(ArrayType(StringType)),
        defaultSelectedValue: OptionType(ArrayType(StringType)),
        style: OptionType(TreeViewStyleType),
    }),

    Table: StructType({
        rows: ArrayType(DictType(StringType, StructType({
            value: LiteralValueType,
            content: node,
        }))),
        columns: ArrayType(TableColumnType),
        style: OptionType(TableStyleType),
    }),

    Gantt: StructType({
        rows: ArrayType(StructType({
            cells: DictType(StringType, StructType({
                value: LiteralValueType,
                content: node,
            })),
            events: ArrayType(GanttEventType),
        })),
        columns: ArrayType(TableColumnType),
        style: OptionType(GanttStyleType),
    }),

    Planner: StructType({
        rows: ArrayType(StructType({
            cells: DictType(StringType, StructType({
                value: LiteralValueType,
                content: node,
            })),
            events: ArrayType(PlannerEventType),
        })),
        columns: ArrayType(TableColumnType),
        style: OptionType(PlannerStyleType),
        eventPopover: OptionType(FunctionType([EventPopoverContextType], node)),
    }),

    // Disclosure
    Accordion: StructType({
        items: ArrayType(StructType({
            value: StringType,
            trigger: StringType,
            content: ArrayType(node),
            disabled: OptionType(BooleanType),
        })),
        style: OptionType(AccordionStyleType),
    }),

    Carousel: StructType({
        items: ArrayType(node),
        index: OptionType(IntegerType),
        defaultIndex: OptionType(IntegerType),
        slidesPerView: OptionType(IntegerType),
        slidesPerMove: OptionType(IntegerType),
        loop: OptionType(BooleanType),
        autoplay: OptionType(BooleanType),
        allowMouseDrag: OptionType(BooleanType),
        showIndicators: OptionType(BooleanType),
        showControls: OptionType(BooleanType),
        style: OptionType(CarouselStyleType),
    }),

    Tabs: StructType({
        items: ArrayType(StructType({
            value: StringType,
            trigger: StringType,
            content: ArrayType(node),
            disabled: OptionType(BooleanType),
        })),
        value: OptionType(StringType),
        defaultValue: OptionType(StringType),
        style: OptionType(TabsStyleType),
    }),

    // Overlays
    Tooltip: StructType({
        trigger: node,
        content: StringType,
        placement: OptionType(PlacementType),
        hasArrow: OptionType(BooleanType),
    }),

    Menu: StructType({
        trigger: node,
        items: ArrayType(MenuItemType),
        placement: OptionType(PlacementType),
    }),

    Dialog: StructType({
        trigger: node,
        body: ArrayType(node),
        title: OptionType(StringType),
        description: OptionType(StringType),
        style: OptionType(DialogStyleType),
    }),

    Drawer: StructType({
        trigger: node,
        body: ArrayType(node),
        title: OptionType(StringType),
        description: OptionType(StringType),
        style: OptionType(DrawerStyleType),
    }),

    Popover: StructType({
        trigger: node,
        body: ArrayType(node),
        title: OptionType(StringType),
        description: OptionType(StringType),
        style: OptionType(PopoverStyleType),
    }),

    HoverCard: StructType({
        trigger: node,
        body: ArrayType(node),
        style: OptionType(HoverCardStyleType),
    }),

    ActionBar: StructType({
        items: ArrayType(ActionBarItemType),
        selectionCount: OptionType(IntegerType),
        selectionLabel: OptionType(StringType),
        style: OptionType(ActionBarStyleType),
    }),

    ToggleTip: StructType({
        trigger: node,
        content: StringType,
        style: OptionType(ToggleTipStyleType),
    }),

    // Reactive - for selective re-rendering
    ReactiveComponent: StructType({
        /** The render function to execute - returns UIComponentType */
        render: FunctionType([], node),
    }),
}));

/**
 * Type alias for UIComponentType.
 */
export type UIComponentType = typeof UIComponentType;
