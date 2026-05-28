---
name: react-flow
description: |
  Build interactive node-based diagrams, flowcharts, and graph editors with React Flow (@xyflow/react v12).
  Use when: (1) Creating node-based UIs like workflow editors, state machines, or mind maps, (2) Building
  diagram editors with drag-and-drop, (3) Implementing custom nodes and edges, (4) Working with connections
  between nodes, (5) Managing viewport/zoom controls, (6) Handling node/edge events, or (7) Any graph
  visualization in React. Triggers: "react flow", "xyflow", "node diagram", "flowchart editor", "workflow
  builder", "graph editor", "node-based UI", "canvas diagram", "draggable nodes", "edge connections".
---

# React Flow (@xyflow/react v12)

React Flow is a library for building node-based UIs with React.

## Installation

```bash
npm install @xyflow/react
```

Import styles in your app entry point:
```tsx
import '@xyflow/react/dist/style.css';
```

## Quick Start

```tsx
import { ReactFlow, Background, Controls, MiniMap } from '@xyflow/react';
import '@xyflow/react/dist/style.css';

const nodes = [
  { id: '1', position: { x: 0, y: 0 }, data: { label: 'Node 1' } },
  { id: '2', position: { x: 200, y: 100 }, data: { label: 'Node 2' } },
];
const edges = [{ id: 'e1-2', source: '1', target: '2' }];

function Flow() {
  return (
    <div style={{ width: '100%', height: '500px' }}>
      <ReactFlow defaultNodes={nodes} defaultEdges={edges} fitView>
        <Background />
        <Controls />
        <MiniMap />
      </ReactFlow>
    </div>
  );
}
```

## Core Concepts

### Controlled vs Uncontrolled Mode

**Uncontrolled** (internal state):
```tsx
<ReactFlow defaultNodes={nodes} defaultEdges={edges} />
```

**Controlled** (external state):
```tsx
const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);

<ReactFlow
  nodes={nodes}
  edges={edges}
  onNodesChange={onNodesChange}
  onEdgesChange={onEdgesChange}
  onConnect={(conn) => setEdges((eds) => addEdge(conn, eds))}
/>
```

### Node Structure

```tsx
type Node = {
  id: string;                    // Required
  position: { x: number; y: number }; // Required
  data: Record<string, unknown>; // Required
  type?: string;                 // 'input' | 'output' | 'default' | 'group' | custom
  parentId?: string;             // For nested nodes
  extent?: 'parent';             // Constrain to parent bounds
  selected?: boolean;
  hidden?: boolean;
  draggable?: boolean;
  connectable?: boolean;
  style?: CSSProperties;
};
```

### Edge Structure

```tsx
type Edge = {
  id: string;           // Required
  source: string;       // Required: source node ID
  target: string;       // Required: target node ID
  sourceHandle?: string;
  targetHandle?: string;
  type?: string;        // 'default' | 'straight' | 'step' | 'smoothstep'
  animated?: boolean;
  label?: ReactNode;
  markerEnd?: 'arrow' | 'arrowclosed';
  data?: Record<string, unknown>;
};
```

## Custom Nodes

```tsx
import { Handle, Position, NodeProps } from '@xyflow/react';

function CustomNode({ data, isConnectable }: NodeProps) {
  return (
    <div className="custom-node">
      <Handle type="target" position={Position.Left} isConnectable={isConnectable} />
      <div>{data.label}</div>
      <Handle type="source" position={Position.Right} isConnectable={isConnectable} />
    </div>
  );
}

// Register (define outside component to avoid re-renders)
const nodeTypes = { custom: CustomNode };
<ReactFlow nodeTypes={nodeTypes} ... />
```

### Handle Props

```tsx
<Handle
  type="source" | "target"
  position={Position.Top | Position.Right | Position.Bottom | Position.Left}
  id="optional-id"  // Required when multiple handles of same type
  isConnectable={true}
/>
```

Add `nodrag` class to elements that shouldn't trigger dragging:
```tsx
<input className="nodrag" type="text" />
```

## Custom Edges

```tsx
import { BaseEdge, EdgeProps, getBezierPath } from '@xyflow/react';

function CustomEdge({ id, sourceX, sourceY, targetX, targetY, sourcePosition, targetPosition }: EdgeProps) {
  const [edgePath] = getBezierPath({ sourceX, sourceY, sourcePosition, targetX, targetY, targetPosition });
  return <BaseEdge id={id} path={edgePath} />;
}

const edgeTypes = { custom: CustomEdge };
```

Edge path utilities: `getBezierPath`, `getStraightPath`, `getSmoothStepPath`, `getSimpleBezierPath`

## Key Hooks

### useReactFlow

```tsx
const {
  getNodes, getNode, setNodes, addNodes, updateNode, updateNodeData,
  getEdges, getEdge, setEdges, addEdges, deleteElements,
  fitView, zoomIn, zoomOut, setViewport, getViewport,
  screenToFlowPosition, flowToScreenPosition, toObject,
} = useReactFlow();

// Add node at drop position
const pos = screenToFlowPosition({ x: event.clientX, y: event.clientY });
addNodes({ id: 'new', position: pos, data: { label: 'New' } });

// Update node data
updateNodeData('node-1', { label: 'Updated' });
updateNodeData('node-1', (n) => ({ count: n.data.count + 1 }));

// Serialize
const flowState = toObject(); // { nodes, edges, viewport }
```

### useNodesState / useEdgesState

```tsx
const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);
```

### useStore / useStoreApi

Direct Zustand store access:
```tsx
const nodeCount = useStore((state) => state.nodes.length);
const store = useStoreApi();
const currentNodes = store.getState().nodes;
```

### Other Hooks

- `useOnSelectionChange({ onChange: ({ nodes, edges }) => {} })` - selection changes
- `useOnViewportChange({ onStart, onChange, onEnd })` - viewport changes
- `useNodeId()` - get node ID inside custom node
- `useConnection()` - get current connection being dragged
- `useNodeConnections({ nodeId, type })` - get connections for a node

## Components

```tsx
<Background variant={BackgroundVariant.Dots} gap={20} />
<Controls showZoom showFitView position="bottom-left" />
<MiniMap nodeColor={(n) => n.type === 'input' ? 'green' : 'red'} pannable zoomable />
<Panel position="top-right"><button>Save</button></Panel>
```

### NodeToolbar & NodeResizer

```tsx
function CustomNode({ data }) {
  return (
    <>
      <NodeToolbar position={Position.Top}>
        <button>Edit</button>
      </NodeToolbar>
      <NodeResizer minWidth={100} minHeight={50} />
      <div>{data.label}</div>
    </>
  );
}
```

## Common Props

```tsx
<ReactFlow
  nodes={nodes} edges={edges}
  nodeTypes={nodeTypes} edgeTypes={edgeTypes}

  // Events
  onNodesChange={onNodesChange}
  onEdgesChange={onEdgesChange}
  onConnect={(conn) => {}}
  onNodeClick={(e, node) => {}}
  isValidConnection={(conn) => boolean}

  // Viewport
  fitView
  fitViewOptions={{ padding: 0.2 }}
  minZoom={0.1} maxZoom={4}

  // Interaction
  nodesDraggable nodesConnectable
  panOnDrag zoomOnScroll
  snapToGrid snapGrid={[15, 15]}

  // Appearance
  colorMode="light" // 'light' | 'dark' | 'system'
  defaultEdgeOptions={{ animated: true }}
/>
```

## Drag and Drop

```tsx
function Flow() {
  const { screenToFlowPosition, addNodes } = useReactFlow();

  const onDragOver = (e: DragEvent) => {
    e.preventDefault();
    e.dataTransfer.dropEffect = 'move';
  };

  const onDrop = (e: DragEvent) => {
    e.preventDefault();
    const type = e.dataTransfer.getData('application/reactflow');
    const position = screenToFlowPosition({ x: e.clientX, y: e.clientY });
    addNodes({ id: `${Date.now()}`, type, position, data: { label: type } });
  };

  return <ReactFlow onDragOver={onDragOver} onDrop={onDrop}>...</ReactFlow>;
}
```

## Connection Validation

```tsx
const isValidConnection = (connection: Connection) => {
  if (connection.source === connection.target) return false; // no self-connections
  return sourceNode?.data.outputType === targetNode?.data.inputType;
};
<ReactFlow isValidConnection={isValidConnection} />
```

## Nested Nodes (Groups)

```tsx
const nodes = [
  { id: 'group', type: 'group', position: { x: 0, y: 0 }, style: { width: 400, height: 300 }, data: {} },
  { id: 'child', parentId: 'group', extent: 'parent', position: { x: 50, y: 50 }, data: { label: 'Child' } },
];
```

## TypeScript

```tsx
type MyNodeData = { label: string; value: number };
type MyNode = Node<MyNodeData, 'myType'>;

const { getNodes, updateNodeData } = useReactFlow<MyNode, MyEdge>();
```

## Performance Tips

1. **Memoize nodeTypes/edgeTypes** - define outside component
2. **Use useStore with selectors** - avoid full state subscriptions
3. **Memo custom components** - wrap with React.memo
4. **Large graphs** - set `onlyRenderVisibleElements={true}`

## Utilities

```tsx
import { addEdge, applyNodeChanges, applyEdgeChanges, getConnectedEdges, getIncomers, getOutgoers } from '@xyflow/react';
```

## Further Reading

- **API Reference**: See [references/api-reference.md](references/api-reference.md) for all props, types, and detailed options
- **Advanced Patterns**: See [references/advanced-patterns.md](references/advanced-patterns.md) for middleware, auto-layout, undo/redo, floating edges, and more
