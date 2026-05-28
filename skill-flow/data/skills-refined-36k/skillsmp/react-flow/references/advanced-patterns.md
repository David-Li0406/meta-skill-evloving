# Advanced React Flow Patterns

This document covers advanced usage patterns for React Flow including middleware, layouting, subflows, custom connection lines, and more.

## Table of Contents

1. [Change Middleware](#change-middleware)
2. [Auto-Layout with Dagre/ELK](#auto-layout)
3. [Computed/Derived Positions](#computed-positions)
4. [Floating Edges](#floating-edges)
5. [Custom Connection Lines](#custom-connection-lines)
6. [Click-to-Connect](#click-to-connect)
7. [Undo/Redo](#undoredo)
8. [Save/Restore Flow](#saverestore-flow)
9. [Multiple Flows](#multiple-flows)
10. [Server-Side Rendering](#server-side-rendering)
11. [Testing](#testing)

---

## Change Middleware

Intercept and modify node/edge changes before they're applied. Useful for validation, constraints, or side effects.

```tsx
import { experimental_useOnNodesChangeMiddleware } from '@xyflow/react';

function Flow() {
  // Prevent nodes from being dragged outside canvas bounds
  experimental_useOnNodesChangeMiddleware((changes) => {
    return changes.map((change) => {
      if (change.type === 'position' && change.position) {
        return {
          ...change,
          position: {
            x: Math.max(0, Math.min(1000, change.position.x)),
            y: Math.max(0, Math.min(1000, change.position.y)),
          },
        };
      }
      return change;
    });
  });

  return <ReactFlow ... />;
}
```

### Prevent Specific Deletions

```tsx
experimental_useOnNodesChangeMiddleware((changes) => {
  return changes.filter((change) => {
    // Prevent deleting nodes of type 'locked'
    if (change.type === 'remove') {
      const node = getNode(change.id);
      return node?.type !== 'locked';
    }
    return true;
  });
});
```

---

## Auto-Layout

Use layout algorithms (Dagre, ELK, D3) to automatically position nodes.

### With Dagre

```bash
npm install @dagrejs/dagre
```

```tsx
import Dagre from '@dagrejs/dagre';

const getLayoutedElements = (nodes: Node[], edges: Edge[], direction = 'TB') => {
  const g = new Dagre.graphlib.Graph().setDefaultEdgeLabel(() => ({}));
  g.setGraph({ rankdir: direction });

  edges.forEach((edge) => g.setEdge(edge.source, edge.target));
  nodes.forEach((node) =>
    g.setNode(node.id, {
      ...node,
      width: node.measured?.width ?? 150,
      height: node.measured?.height ?? 50,
    })
  );

  Dagre.layout(g);

  return {
    nodes: nodes.map((node) => {
      const position = g.node(node.id);
      const x = position.x - (node.measured?.width ?? 150) / 2;
      const y = position.y - (node.measured?.height ?? 50) / 2;
      return { ...node, position: { x, y } };
    }),
    edges,
  };
};

function Flow() {
  const { fitView } = useReactFlow();
  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);

  const onLayout = useCallback(
    (direction: string) => {
      const layouted = getLayoutedElements(nodes, edges, direction);
      setNodes([...layouted.nodes]);
      setEdges([...layouted.edges]);
      window.requestAnimationFrame(() => fitView());
    },
    [nodes, edges]
  );

  return (
    <ReactFlow nodes={nodes} edges={edges} onNodesChange={onNodesChange} onEdgesChange={onEdgesChange}>
      <Panel position="top-right">
        <button onClick={() => onLayout('TB')}>Vertical Layout</button>
        <button onClick={() => onLayout('LR')}>Horizontal Layout</button>
      </Panel>
    </ReactFlow>
  );
}
```

### Layout on Node Add

```tsx
const onConnect = useCallback(
  (connection: Connection) => {
    setEdges((eds) => addEdge(connection, eds));
    // Re-layout after new connection
    requestAnimationFrame(() => onLayout('TB'));
  },
  [onLayout]
);
```

---

## Computed Positions

Dynamically compute node positions based on data or other nodes.

### Radial Layout

```tsx
const computeRadialPositions = (nodes: Node[], centerX: number, centerY: number, radius: number) => {
  const angleStep = (2 * Math.PI) / nodes.length;

  return nodes.map((node, index) => ({
    ...node,
    position: {
      x: centerX + radius * Math.cos(angleStep * index),
      y: centerY + radius * Math.sin(angleStep * index),
    },
  }));
};
```

### Timeline Layout

```tsx
const computeTimelinePositions = (nodes: Node[], startX: number, startY: number, gap: number) => {
  return nodes
    .sort((a, b) => a.data.timestamp - b.data.timestamp)
    .map((node, index) => ({
      ...node,
      position: { x: startX + index * gap, y: startY },
    }));
};
```

---

## Floating Edges

Edges that connect to the nearest point on node boundaries rather than fixed handles.

```tsx
import { getBezierPath, Position, InternalNode } from '@xyflow/react';

// Find nearest point on node boundary to target
function getNodeIntersection(intersectionNode: InternalNode, targetNode: InternalNode) {
  const w = intersectionNode.measured?.width ?? 0;
  const h = intersectionNode.measured?.height ?? 0;
  const { positionAbsolute: targetPos } = targetNode.internals;
  const { positionAbsolute: intersectionPos } = intersectionNode.internals;

  const targetCenter = {
    x: targetPos.x + (targetNode.measured?.width ?? 0) / 2,
    y: targetPos.y + (targetNode.measured?.height ?? 0) / 2,
  };

  const intersectionCenter = {
    x: intersectionPos.x + w / 2,
    y: intersectionPos.y + h / 2,
  };

  // Calculate angle to target
  const dx = targetCenter.x - intersectionCenter.x;
  const dy = targetCenter.y - intersectionCenter.y;

  // Find intersection with rectangle boundary
  const absX = Math.abs(dx);
  const absY = Math.abs(dy);
  const ratio = absX / absY;
  const halfW = w / 2;
  const halfH = h / 2;

  let x, y;
  if (ratio > halfW / halfH) {
    // Intersects with left or right edge
    x = dx > 0 ? halfW : -halfW;
    y = (x / dx) * dy;
  } else {
    // Intersects with top or bottom edge
    y = dy > 0 ? halfH : -halfH;
    x = (y / dy) * dx;
  }

  return {
    x: intersectionCenter.x + x,
    y: intersectionCenter.y + y,
  };
}

function getEdgePosition(node: InternalNode, intersectionPoint: { x: number; y: number }) {
  const { positionAbsolute } = node.internals;
  const nx = positionAbsolute.x + (node.measured?.width ?? 0) / 2;
  const ny = positionAbsolute.y + (node.measured?.height ?? 0) / 2;
  const dx = intersectionPoint.x - nx;
  const dy = intersectionPoint.y - ny;

  if (Math.abs(dx) > Math.abs(dy)) {
    return dx > 0 ? Position.Right : Position.Left;
  }
  return dy > 0 ? Position.Bottom : Position.Top;
}

function FloatingEdge({ id, source, target, markerEnd, style }: EdgeProps) {
  const sourceNode = useInternalNode(source);
  const targetNode = useInternalNode(target);

  if (!sourceNode || !targetNode) return null;

  const sourceIntersection = getNodeIntersection(sourceNode, targetNode);
  const targetIntersection = getNodeIntersection(targetNode, sourceNode);

  const sourcePos = getEdgePosition(sourceNode, sourceIntersection);
  const targetPos = getEdgePosition(targetNode, targetIntersection);

  const [edgePath] = getBezierPath({
    sourceX: sourceIntersection.x,
    sourceY: sourceIntersection.y,
    sourcePosition: sourcePos,
    targetX: targetIntersection.x,
    targetY: targetIntersection.y,
    targetPosition: targetPos,
  });

  return <BaseEdge id={id} path={edgePath} markerEnd={markerEnd} style={style} />;
}

const edgeTypes = { floating: FloatingEdge };
```

---

## Custom Connection Lines

Custom visual feedback while dragging to create connections.

```tsx
import { ConnectionLineComponentProps, getBezierPath } from '@xyflow/react';

function CustomConnectionLine({
  fromX,
  fromY,
  toX,
  toY,
  fromPosition,
  toPosition,
  connectionLineStyle,
}: ConnectionLineComponentProps) {
  const [edgePath] = getBezierPath({
    sourceX: fromX,
    sourceY: fromY,
    sourcePosition: fromPosition,
    targetX: toX,
    targetY: toY,
    targetPosition: toPosition,
  });

  return (
    <g>
      <path
        d={edgePath}
        fill="none"
        stroke="#222"
        strokeWidth={2}
        strokeDasharray="5,5"
        style={connectionLineStyle}
      />
      <circle cx={toX} cy={toY} r={6} fill="#222" />
    </g>
  );
}

<ReactFlow connectionLineComponent={CustomConnectionLine} ... />
```

---

## Click-to-Connect

Alternative to drag-and-drop connections.

```tsx
function Flow() {
  const [connectingNodeId, setConnectingNodeId] = useState<string | null>(null);
  const { addEdges } = useReactFlow();

  const onNodeClick = useCallback(
    (event: React.MouseEvent, node: Node) => {
      if (connectingNodeId && connectingNodeId !== node.id) {
        // Complete connection
        addEdges({
          id: `${connectingNodeId}-${node.id}`,
          source: connectingNodeId,
          target: node.id,
        });
        setConnectingNodeId(null);
      } else if (!connectingNodeId) {
        // Start connection
        setConnectingNodeId(node.id);
      }
    },
    [connectingNodeId, addEdges]
  );

  const onPaneClick = useCallback(() => {
    setConnectingNodeId(null);
  }, []);

  return (
    <ReactFlow
      onNodeClick={onNodeClick}
      onPaneClick={onPaneClick}
      ...
    />
  );
}
```

---

## Undo/Redo

Implement history management for flow state.

```tsx
import { useCallback, useRef } from 'react';

const MAX_HISTORY = 100;

function useUndoRedo() {
  const { getNodes, getEdges, setNodes, setEdges } = useReactFlow();

  const historyRef = useRef<{ nodes: Node[]; edges: Edge[] }[]>([]);
  const historyIndexRef = useRef(-1);

  const takeSnapshot = useCallback(() => {
    const nodes = getNodes();
    const edges = getEdges();

    // Remove any future history if we're not at the end
    historyRef.current = historyRef.current.slice(0, historyIndexRef.current + 1);

    // Add new snapshot
    historyRef.current.push({
      nodes: nodes.map((n) => ({ ...n })),
      edges: edges.map((e) => ({ ...e })),
    });

    // Limit history size
    if (historyRef.current.length > MAX_HISTORY) {
      historyRef.current.shift();
    } else {
      historyIndexRef.current++;
    }
  }, [getNodes, getEdges]);

  const undo = useCallback(() => {
    if (historyIndexRef.current <= 0) return;

    historyIndexRef.current--;
    const { nodes, edges } = historyRef.current[historyIndexRef.current];
    setNodes(nodes);
    setEdges(edges);
  }, [setNodes, setEdges]);

  const redo = useCallback(() => {
    if (historyIndexRef.current >= historyRef.current.length - 1) return;

    historyIndexRef.current++;
    const { nodes, edges } = historyRef.current[historyIndexRef.current];
    setNodes(nodes);
    setEdges(edges);
  }, [setNodes, setEdges]);

  const canUndo = historyIndexRef.current > 0;
  const canRedo = historyIndexRef.current < historyRef.current.length - 1;

  return { takeSnapshot, undo, redo, canUndo, canRedo };
}
```

### With Keyboard Shortcuts

```tsx
function Flow() {
  const { undo, redo } = useUndoRedo();

  useKeyPress('Meta+z', undo);
  useKeyPress('Meta+Shift+z', redo);

  return <ReactFlow ... />;
}
```

---

## Save/Restore Flow

Persist and restore flow state.

### Local Storage

```tsx
const STORAGE_KEY = 'my-flow';

function Flow() {
  const { toObject, setNodes, setEdges, setViewport } = useReactFlow();
  const [nodes, , onNodesChange] = useNodesState([]);
  const [edges, , onEdgesChange] = useEdgesState([]);

  // Save
  const onSave = useCallback(() => {
    const flow = toObject();
    localStorage.setItem(STORAGE_KEY, JSON.stringify(flow));
  }, [toObject]);

  // Restore
  const onRestore = useCallback(() => {
    const stored = localStorage.getItem(STORAGE_KEY);
    if (stored) {
      const flow = JSON.parse(stored);
      setNodes(flow.nodes || []);
      setEdges(flow.edges || []);
      setViewport(flow.viewport || { x: 0, y: 0, zoom: 1 });
    }
  }, [setNodes, setEdges, setViewport]);

  // Load on mount
  useEffect(() => {
    onRestore();
  }, []);

  return (
    <ReactFlow
      nodes={nodes}
      edges={edges}
      onNodesChange={onNodesChange}
      onEdgesChange={onEdgesChange}
    >
      <Panel position="top-right">
        <button onClick={onSave}>Save</button>
        <button onClick={onRestore}>Restore</button>
      </Panel>
    </ReactFlow>
  );
}
```

### Server Persistence

```tsx
const saveFlow = async (flow: { nodes: Node[]; edges: Edge[]; viewport: Viewport }) => {
  await fetch('/api/flows/my-flow', {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(flow),
  });
};

const loadFlow = async () => {
  const response = await fetch('/api/flows/my-flow');
  return response.json();
};
```

---

## Multiple Flows

Render multiple independent flows on the same page.

```tsx
function App() {
  return (
    <div style={{ display: 'flex' }}>
      <div style={{ width: '50%', height: '100vh' }}>
        <ReactFlowProvider>
          <Flow1 />
        </ReactFlowProvider>
      </div>
      <div style={{ width: '50%', height: '100vh' }}>
        <ReactFlowProvider>
          <Flow2 />
        </ReactFlowProvider>
      </div>
    </div>
  );
}
```

Each flow needs its own `ReactFlowProvider` context.

---

## Server-Side Rendering

React Flow requires browser APIs. Handle SSR with dynamic imports or checks.

### Next.js

```tsx
import dynamic from 'next/dynamic';

const Flow = dynamic(() => import('./Flow'), {
  ssr: false,
  loading: () => <div>Loading...</div>,
});

export default function Page() {
  return <Flow />;
}
```

### Check for Browser

```tsx
function Flow() {
  const [isClient, setIsClient] = useState(false);

  useEffect(() => {
    setIsClient(true);
  }, []);

  if (!isClient) {
    return <div>Loading...</div>;
  }

  return <ReactFlow ... />;
}
```

---

## Testing

### React Testing Library

```tsx
import { render, screen, fireEvent } from '@testing-library/react';
import { ReactFlowProvider } from '@xyflow/react';

function renderWithProvider(component: React.ReactElement) {
  return render(
    <ReactFlowProvider>
      {component}
    </ReactFlowProvider>
  );
}

test('renders nodes', () => {
  const nodes = [{ id: '1', position: { x: 0, y: 0 }, data: { label: 'Test Node' } }];

  renderWithProvider(<Flow initialNodes={nodes} />);

  expect(screen.getByText('Test Node')).toBeInTheDocument();
});
```

### Cypress

```tsx
// cypress/e2e/flow.cy.ts
describe('Flow', () => {
  beforeEach(() => {
    cy.visit('/');
  });

  it('can add a node', () => {
    cy.get('.react-flow__pane').dblclick();
    cy.get('.react-flow__node').should('have.length', 2);
  });

  it('can drag a node', () => {
    cy.get('.react-flow__node').first()
      .trigger('mousedown', { which: 1 })
      .trigger('mousemove', { clientX: 300, clientY: 300 })
      .trigger('mouseup');
  });

  it('can connect nodes', () => {
    cy.get('[data-handleid="source-1"]')
      .trigger('mousedown', { which: 1 })
      .trigger('mousemove', { clientX: 400, clientY: 200 });
    cy.get('[data-handleid="target-2"]')
      .trigger('mouseup');

    cy.get('.react-flow__edge').should('have.length', 1);
  });
});
```

---

## ReactFlowProvider Props

When using multiple flows or needing initial state in the provider:

```tsx
<ReactFlowProvider
  initialNodes={nodes}
  initialEdges={edges}
>
  <Flow />
</ReactFlowProvider>
```

This is an alternative to passing `defaultNodes`/`defaultEdges` to `<ReactFlow>` and allows the provider to manage initial state.

---

## Node Internals Update

When handle positions change dynamically (e.g., after a node resize or content change), notify React Flow:

```tsx
const updateNodeInternals = useUpdateNodeInternals();

// After changing handles
updateNodeInternals('node-1');

// Update multiple nodes
updateNodeInternals(['node-1', 'node-2']);
```

This recalculates handle bounds for edge connections.

---

## Edge Label Renderer

Render complex React components as edge labels without SVG limitations:

```tsx
import { EdgeLabelRenderer, getBezierPath } from '@xyflow/react';

function CustomEdge({ id, sourceX, sourceY, targetX, targetY, sourcePosition, targetPosition }: EdgeProps) {
  const [edgePath, labelX, labelY] = getBezierPath({
    sourceX, sourceY, sourcePosition,
    targetX, targetY, targetPosition,
  });

  return (
    <>
      <BaseEdge id={id} path={edgePath} />
      <EdgeLabelRenderer>
        <div
          style={{
            position: 'absolute',
            transform: `translate(-50%, -50%) translate(${labelX}px, ${labelY}px)`,
            pointerEvents: 'all',
          }}
          className="nodrag nopan"
        >
          <button onClick={() => console.log('Clicked!')}>
            Delete
          </button>
        </div>
      </EdgeLabelRenderer>
    </>
  );
}
```

`EdgeLabelRenderer` creates a portal that renders HTML outside the SVG, allowing full React components.
