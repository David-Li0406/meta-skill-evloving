# React Flow API Reference

Complete API reference for @xyflow/react v12. This document covers all props, types, and detailed options.

## Table of Contents

1. [ReactFlow Component Props](#reactflow-component-props)
2. [Node Types](#node-types)
3. [Edge Types](#edge-types)
4. [Handle Props](#handle-props)
5. [Change Types](#change-types)
6. [Connection Types](#connection-types)
7. [Viewport Types](#viewport-types)
8. [Position & Enums](#position--enums)

---

## ReactFlow Component Props

### Data Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `nodes` | `Node[]` | `[]` | Controlled nodes array |
| `edges` | `Edge[]` | `[]` | Controlled edges array |
| `defaultNodes` | `Node[]` | `[]` | Initial nodes (uncontrolled) |
| `defaultEdges` | `Edge[]` | `[]` | Initial edges (uncontrolled) |
| `nodeTypes` | `NodeTypes` | built-in types | Custom node component map |
| `edgeTypes` | `EdgeTypes` | built-in types | Custom edge component map |
| `defaultEdgeOptions` | `Partial<Edge>` | `{}` | Default options for new edges |

### Change Handlers

| Prop | Type | Description |
|------|------|-------------|
| `onNodesChange` | `(changes: NodeChange[]) => void` | Called when nodes change |
| `onEdgesChange` | `(changes: EdgeChange[]) => void` | Called when edges change |
| `onConnect` | `(connection: Connection) => void` | Called when connection made |
| `onConnectStart` | `(event, params: OnConnectStartParams) => void` | Connection drag started |
| `onConnectEnd` | `(event, connectionState) => void` | Connection drag ended |

### Node Event Handlers

| Prop | Type | Description |
|------|------|-------------|
| `onNodeClick` | `(event: ReactMouseEvent, node: Node) => void` | Node clicked |
| `onNodeDoubleClick` | `(event: ReactMouseEvent, node: Node) => void` | Node double-clicked |
| `onNodeDragStart` | `(event, node: Node, nodes: Node[]) => void` | Node drag started |
| `onNodeDrag` | `(event, node: Node, nodes: Node[]) => void` | Node being dragged |
| `onNodeDragStop` | `(event, node: Node, nodes: Node[]) => void` | Node drag ended |
| `onNodeMouseEnter` | `(event: ReactMouseEvent, node: Node) => void` | Mouse entered node |
| `onNodeMouseMove` | `(event: ReactMouseEvent, node: Node) => void` | Mouse moving over node |
| `onNodeMouseLeave` | `(event: ReactMouseEvent, node: Node) => void` | Mouse left node |
| `onNodeContextMenu` | `(event: ReactMouseEvent, node: Node) => void` | Node right-clicked |

### Edge Event Handlers

| Prop | Type | Description |
|------|------|-------------|
| `onEdgeClick` | `(event: ReactMouseEvent, edge: Edge) => void` | Edge clicked |
| `onEdgeDoubleClick` | `(event: ReactMouseEvent, edge: Edge) => void` | Edge double-clicked |
| `onEdgeMouseEnter` | `(event: ReactMouseEvent, edge: Edge) => void` | Mouse entered edge |
| `onEdgeMouseMove` | `(event: ReactMouseEvent, edge: Edge) => void` | Mouse moving over edge |
| `onEdgeMouseLeave` | `(event: ReactMouseEvent, edge: Edge) => void` | Mouse left edge |
| `onEdgeContextMenu` | `(event: ReactMouseEvent, edge: Edge) => void` | Edge right-clicked |
| `onReconnect` | `(oldEdge: Edge, newConnection: Connection) => void` | Edge reconnected |
| `onReconnectStart` | `(event, edge: Edge, handleType) => void` | Edge reconnect started |
| `onReconnectEnd` | `(event, edge: Edge, handleType, connectionState) => void` | Edge reconnect ended |

### Deletion Event Handlers

| Prop | Type | Description |
|------|------|-------------|
| `onNodesDelete` | `(nodes: Node[]) => void` | Nodes deleted |
| `onEdgesDelete` | `(edges: Edge[]) => void` | Edges deleted |
| `onDelete` | `({ nodes, edges }) => void` | Any elements deleted |
| `onBeforeDelete` | `async ({ nodes, edges }) => boolean \| { nodes?, edges? }` | Before deletion (return false to cancel) |

### Selection Event Handlers

| Prop | Type | Description |
|------|------|-------------|
| `onSelectionChange` | `({ nodes, edges }) => void` | Selection changed |
| `onSelectionDragStart` | `(event, nodes: Node[]) => void` | Selection drag started |
| `onSelectionDrag` | `(event, nodes: Node[]) => void` | Selection being dragged |
| `onSelectionDragStop` | `(event, nodes: Node[]) => void` | Selection drag ended |
| `onSelectionContextMenu` | `(event, nodes: Node[]) => void` | Selection right-clicked |

### Viewport Event Handlers

| Prop | Type | Description |
|------|------|-------------|
| `onMove` | `(event, viewport: Viewport) => void` | Viewport moving |
| `onMoveStart` | `(event, viewport: Viewport) => void` | Viewport move started |
| `onMoveEnd` | `(event, viewport: Viewport) => void` | Viewport move ended |
| `onViewportChange` | `(viewport: Viewport) => void` | Viewport changed |

### Pane Event Handlers

| Prop | Type | Description |
|------|------|-------------|
| `onPaneClick` | `(event: ReactMouseEvent) => void` | Pane clicked |
| `onPaneContextMenu` | `(event: ReactMouseEvent) => void` | Pane right-clicked |
| `onPaneMouseEnter` | `(event: ReactMouseEvent) => void` | Mouse entered pane |
| `onPaneMouseMove` | `(event: ReactMouseEvent) => void` | Mouse moving over pane |
| `onPaneMouseLeave` | `(event: ReactMouseEvent) => void` | Mouse left pane |
| `onPaneScroll` | `(event: WheelEvent) => void` | Pane scrolled |

### Initialization

| Prop | Type | Description |
|------|------|-------------|
| `onInit` | `(instance: ReactFlowInstance) => void` | React Flow initialized |
| `onError` | `(code: string, message: string) => void` | Error occurred |

### Viewport Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `fitView` | `boolean` | `false` | Fit view on mount |
| `fitViewOptions` | `FitViewOptions` | `{}` | Options for fitView |
| `minZoom` | `number` | `0.5` | Minimum zoom level |
| `maxZoom` | `number` | `2` | Maximum zoom level |
| `defaultViewport` | `Viewport` | `{ x: 0, y: 0, zoom: 1 }` | Initial viewport |
| `translateExtent` | `[[x1, y1], [x2, y2]]` | `[[-∞, -∞], [∞, ∞]]` | Pan boundaries |

### Interaction Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `nodesDraggable` | `boolean` | `true` | Nodes can be dragged |
| `nodesConnectable` | `boolean` | `true` | Nodes can be connected |
| `nodesFocusable` | `boolean` | `true` | Nodes can receive focus |
| `edgesFocusable` | `boolean` | `true` | Edges can receive focus |
| `edgesReconnectable` | `boolean` | `true` | Edges can be reconnected |
| `elementsSelectable` | `boolean` | `true` | Elements can be selected |
| `selectNodesOnDrag` | `boolean` | `true` | Select nodes on drag |
| `panOnDrag` | `boolean \| number[]` | `true` | Pan on drag (array = specific mouse buttons) |
| `panOnScroll` | `boolean` | `false` | Pan on scroll |
| `panOnScrollMode` | `PanOnScrollMode` | `Free` | Free \| Horizontal \| Vertical |
| `panOnScrollSpeed` | `number` | `0.5` | Pan speed on scroll |
| `zoomOnScroll` | `boolean` | `true` | Zoom on scroll |
| `zoomOnPinch` | `boolean` | `true` | Zoom on pinch |
| `zoomOnDoubleClick` | `boolean` | `true` | Zoom on double click |
| `preventScrolling` | `boolean` | `true` | Prevent page scroll when over flow |
| `selectionOnDrag` | `boolean` | `false` | Selection box on drag |
| `selectionMode` | `SelectionMode` | `Full` | Full \| Partial |
| `selectionKeyCode` | `KeyCode` | `'Shift'` | Key to enable selection mode |
| `multiSelectionKeyCode` | `KeyCode` | `'Meta'` | Key for multi-select |
| `deleteKeyCode` | `KeyCode` | `'Backspace'` | Key to delete selected |
| `zoomActivationKeyCode` | `KeyCode` | `'Meta'` | Key to enable zoom mode |
| `panActivationKeyCode` | `KeyCode` | `'Space'` | Key to enable pan mode |
| `disableKeyboardA11y` | `boolean` | `false` | Disable keyboard a11y |
| `nodeDragThreshold` | `number` | `1` | Pixels before drag starts |
| `autoPanOnConnect` | `boolean` | `true` | Auto-pan during connection |
| `autoPanOnNodeDrag` | `boolean` | `true` | Auto-pan during node drag |
| `autoPanSpeed` | `number` | `15` | Auto-pan speed |

### Connection Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `connectionMode` | `ConnectionMode` | `Strict` | Strict \| Loose |
| `connectionLineType` | `ConnectionLineType` | `Bezier` | Bezier \| Straight \| Step \| SmoothStep \| SimpleBezier |
| `connectionLineStyle` | `CSSProperties` | `{}` | Connection line CSS |
| `connectionLineComponent` | `ComponentType` | - | Custom connection line |
| `connectionLineWrapperStyles` | `CSSProperties` | `{}` | Wrapper CSS |
| `connectionRadius` | `number` | `20` | Snap radius for connections |
| `isValidConnection` | `(connection) => boolean` | - | Validate connections |

### Snapping Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `snapToGrid` | `boolean` | `false` | Snap nodes to grid |
| `snapGrid` | `[number, number]` | `[15, 15]` | Grid size [x, y] |

### Appearance Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `colorMode` | `'light' \| 'dark' \| 'system'` | `'light'` | Color mode |
| `elevateNodesOnSelect` | `boolean` | `true` | Bring selected nodes to front |
| `elevateEdgesOnSelect` | `boolean` | `false` | Bring selected edges to front |
| `nodeOrigin` | `[number, number]` | `[0, 0]` | Node anchor point |
| `nodeExtent` | `CoordinateExtent` | - | Global node drag bounds |
| `onlyRenderVisibleElements` | `boolean` | `false` | Only render visible |
| `className` | `string` | - | Container class |
| `style` | `CSSProperties` | - | Container styles |
| `id` | `string` | - | Container ID |
| `proOptions` | `ProOptions` | - | Pro feature options |

---

## Node Types

### Node<NodeData, NodeType>

```typescript
type Node<NodeData = Record<string, unknown>, NodeType = string> = {
  // Required
  id: string;
  position: XYPosition;
  data: NodeData;

  // Type & State
  type?: NodeType;
  selected?: boolean;
  hidden?: boolean;
  dragging?: boolean;

  // Permissions
  draggable?: boolean;
  selectable?: boolean;
  connectable?: boolean;
  deletable?: boolean;
  focusable?: boolean;

  // Hierarchy
  parentId?: string;
  extent?: 'parent' | CoordinateExtent;
  expandParent?: boolean;

  // Handles
  sourcePosition?: Position;
  targetPosition?: Position;

  // Dimensions
  width?: number;
  height?: number;
  measured?: { width?: number; height?: number };

  // Interaction
  dragHandle?: string;  // CSS selector

  // Appearance
  zIndex?: number;
  style?: CSSProperties;
  className?: string;

  // Accessibility
  ariaRole?: string;
  ariaLabel?: string;
  domAttributes?: HTMLAttributes<HTMLDivElement>;
};
```

### NodeProps<NodeType>

Props passed to custom node components:

```typescript
type NodeProps<NodeType extends Node = Node> = {
  id: string;
  data: NodeType['data'];
  type: NodeType['type'];

  // Position (flow coordinates)
  xPos: number;
  yPos: number;

  // Absolute position (includes parent offset)
  positionAbsoluteX: number;
  positionAbsoluteY: number;

  // State
  selected: boolean;
  isConnectable: boolean;
  dragging: boolean;
  draggable: boolean;
  selectable: boolean;
  deletable: boolean;

  // Dimensions
  width?: number;
  height?: number;

  // Z-index
  zIndex: number;

  // Parent
  parentId?: string;
};
```

### InternalNode

Extended node type used internally:

```typescript
type InternalNode<NodeType extends Node = Node> = NodeType & {
  measured: { width?: number; height?: number };
  internals: {
    positionAbsolute: XYPosition;
    z: number;
    userNode: NodeType;
    handleBounds?: NodeHandleBounds;
    isParent?: boolean;
  };
};
```

---

## Edge Types

### Edge<EdgeData, EdgeType>

```typescript
type Edge<EdgeData = Record<string, unknown>, EdgeType = string> = {
  // Required
  id: string;
  source: string;
  target: string;

  // Handles
  sourceHandle?: string | null;
  targetHandle?: string | null;

  // Type & State
  type?: EdgeType;
  selected?: boolean;
  hidden?: boolean;

  // Permissions
  deletable?: boolean;
  selectable?: boolean;
  focusable?: boolean;
  reconnectable?: boolean | 'source' | 'target';

  // Animation
  animated?: boolean;

  // Data
  data?: EdgeData;

  // Labels
  label?: ReactNode;
  labelStyle?: CSSProperties;
  labelShowBg?: boolean;
  labelBgStyle?: CSSProperties;
  labelBgPadding?: [number, number];
  labelBgBorderRadius?: number;

  // Markers
  markerStart?: EdgeMarkerType;
  markerEnd?: EdgeMarkerType;

  // Interaction
  interactionWidth?: number;

  // Appearance
  zIndex?: number;
  style?: CSSProperties;
  className?: string;

  // Accessibility
  ariaRole?: string;
  ariaLabel?: string;
  domAttributes?: SVGAttributes<SVGPathElement>;
};
```

### EdgeProps<EdgeType>

Props passed to custom edge components:

```typescript
type EdgeProps<EdgeType extends Edge = Edge> = {
  id: string;
  source: string;
  target: string;
  sourceHandleId?: string | null;
  targetHandleId?: string | null;

  // Node references
  sourceNode: InternalNode;
  targetNode: InternalNode;

  // Computed positions
  sourceX: number;
  sourceY: number;
  targetX: number;
  targetY: number;
  sourcePosition: Position;
  targetPosition: Position;

  // State
  selected: boolean;
  animated: boolean;

  // Data
  data?: EdgeType['data'];

  // Labels (inherited from Edge)
  label?: ReactNode;
  labelStyle?: CSSProperties;
  labelShowBg?: boolean;
  labelBgStyle?: CSSProperties;
  labelBgPadding?: [number, number];
  labelBgBorderRadius?: number;

  // Markers
  markerStart?: string;
  markerEnd?: string;

  // Appearance
  interactionWidth?: number;
  style?: CSSProperties;
};
```

### EdgeMarkerType

```typescript
type EdgeMarkerType = string | {
  type: MarkerType;  // 'arrow' | 'arrowclosed'
  color?: string;
  width?: number;
  height?: number;
  markerUnits?: string;
  orient?: string;
  strokeWidth?: number;
};
```

---

## Handle Props

```typescript
type HandleProps = {
  // Required
  type: 'source' | 'target';
  position: Position;

  // Identification
  id?: string;

  // State
  isConnectable?: boolean;
  isConnectableStart?: boolean;
  isConnectableEnd?: boolean;

  // Callbacks
  onConnect?: (connections: Connection[]) => void;

  // Appearance
  style?: CSSProperties;
  className?: string;
};
```

---

## Change Types

### NodeChange

```typescript
type NodeChange<NodeType extends Node = Node> =
  | NodeAddChange<NodeType>
  | NodeRemoveChange
  | NodeReplaceChange<NodeType>
  | NodeResetChange<NodeType>
  | NodePositionChange
  | NodeDimensionChange
  | NodeSelectionChange;

type NodePositionChange = {
  type: 'position';
  id: string;
  position?: XYPosition;
  positionAbsolute?: XYPosition;
  dragging?: boolean;
};

type NodeDimensionChange = {
  type: 'dimensions';
  id: string;
  dimensions?: Dimensions;
  resizing?: boolean;
};

type NodeSelectionChange = {
  type: 'select';
  id: string;
  selected: boolean;
};

type NodeRemoveChange = {
  type: 'remove';
  id: string;
};

type NodeAddChange<NodeType> = {
  type: 'add';
  item: NodeType;
  index?: number;
};

type NodeReplaceChange<NodeType> = {
  type: 'replace';
  id: string;
  item: NodeType;
};
```

### EdgeChange

```typescript
type EdgeChange<EdgeType extends Edge = Edge> =
  | EdgeAddChange<EdgeType>
  | EdgeRemoveChange
  | EdgeReplaceChange<EdgeType>
  | EdgeResetChange<EdgeType>
  | EdgeSelectionChange;

type EdgeSelectionChange = {
  type: 'select';
  id: string;
  selected: boolean;
};

type EdgeRemoveChange = {
  type: 'remove';
  id: string;
};

type EdgeAddChange<EdgeType> = {
  type: 'add';
  item: EdgeType;
  index?: number;
};

type EdgeReplaceChange<EdgeType> = {
  type: 'replace';
  id: string;
  item: EdgeType;
};
```

---

## Connection Types

### Connection

```typescript
type Connection = {
  source: string;
  target: string;
  sourceHandle: string | null;
  targetHandle: string | null;
};
```

### ConnectionState

```typescript
type ConnectionState = ConnectionInProgress | NoConnection;

type ConnectionInProgress = {
  inProgress: true;
  isValid: boolean | null;
  from: XYPosition;
  to: XYPosition;
  fromHandle: HandleType | null;
  toHandle: HandleType | null;
  fromPosition: Position;
  toPosition: Position;
  fromNode: InternalNode;
  toNode: InternalNode | null;
};

type NoConnection = {
  inProgress: false;
  isValid: null;
  from: null;
  to: null;
  fromHandle: null;
  toHandle: null;
  fromPosition: null;
  toPosition: null;
  fromNode: null;
  toNode: null;
};
```

### OnConnectStartParams

```typescript
type OnConnectStartParams = {
  nodeId: string | null;
  handleId: string | null;
  handleType: HandleType | null;
};
```

---

## Viewport Types

### Viewport

```typescript
type Viewport = {
  x: number;
  y: number;
  zoom: number;
};
```

### FitViewOptions

```typescript
type FitViewOptions<NodeType extends Node = Node> = {
  padding?: number | { top?: number | string; right?: number | string; bottom?: number | string; left?: number | string };
  includeHiddenNodes?: boolean;
  minZoom?: number;
  maxZoom?: number;
  duration?: number;
  nodes?: (NodeType | { id: string })[];
};
```

### SetCenterOptions

```typescript
type SetCenterOptions = {
  zoom?: number;
  duration?: number;
};
```

---

## Position & Enums

### Position

```typescript
enum Position {
  Top = 'top',
  Right = 'right',
  Bottom = 'bottom',
  Left = 'left',
}
```

### ConnectionMode

```typescript
enum ConnectionMode {
  Strict = 'strict',  // Only connect to valid handle types
  Loose = 'loose',    // Connect to any handle
}
```

### ConnectionLineType

```typescript
enum ConnectionLineType {
  Bezier = 'default',
  Straight = 'straight',
  Step = 'step',
  SmoothStep = 'smoothstep',
  SimpleBezier = 'simplebezier',
}
```

### SelectionMode

```typescript
enum SelectionMode {
  Full = 'full',      // Selection box must fully contain element
  Partial = 'partial', // Selection box only needs to touch element
}
```

### MarkerType

```typescript
enum MarkerType {
  Arrow = 'arrow',
  ArrowClosed = 'arrowclosed',
}
```

### BackgroundVariant

```typescript
enum BackgroundVariant {
  Dots = 'dots',
  Lines = 'lines',
  Cross = 'cross',
}
```

### PanOnScrollMode

```typescript
enum PanOnScrollMode {
  Free = 'free',
  Horizontal = 'horizontal',
  Vertical = 'vertical',
}
```

---

## XYPosition & Dimensions

```typescript
type XYPosition = {
  x: number;
  y: number;
};

type XYZPosition = XYPosition & {
  z: number;
};

type Dimensions = {
  width: number;
  height: number;
};

type Rect = XYPosition & Dimensions;

type Box = {
  x: number;
  y: number;
  x2: number;
  y2: number;
};

type CoordinateExtent = [[number, number], [number, number]];
```
