# Implementation Patterns

## Complete Container Component

```tsx
import { useSortable } from '@dnd-kit/sortable';
import { useDroppable } from '@dnd-kit/core';
import { useDndContext } from '@dnd-kit/core';
import { CSS } from '@dnd-kit/utilities';

interface Container {
  id: string;
  title: string;
  items: Item[];
}

interface Item {
  id: string;
  content: string;
}

const SortableDroppableContainer = ({ container }: { container: Container }) => {
  // Sortable functionality for container reordering
  const {
    attributes,
    listeners,
    setNodeRef: setSortableRef,
    transform,
    transition,
    isDragging,
  } = useSortable({ id: container.id });

  // Droppable functionality for receiving items
  const { setNodeRef: setDroppableRef, isOver } = useDroppable({
    id: container.id,
  });

  // Get current drag context
  const { active } = useDndContext();

  // Determine what type of element is being dragged
  const isItem = active?.id?.toString().startsWith('item-');
  const isContainer = active?.id?.toString().startsWith('container-');

  // Apply appropriate ref based on drag state
  const setNodeRef = isItem ? setDroppableRef : setSortableRef;

  // Apply transform only when this container is being dragged
  const style = {
    transform: CSS.Transform.toString(transform),
    transition,
    opacity: isDragging ? 0.5 : 1,
    backgroundColor: isOver && isItem ? '#e0e0e0' : 'white',
  };

  return (
    <div ref={setNodeRef} style={style}>
      {/* Drag handle - only active when dragging containers */}
      <div 
        {...(isContainer ? attributes : {})} 
        {...(isContainer ? listeners : {})}
        style={{ cursor: isContainer ? 'grab' : 'default', padding: '8px' }}
      >
        ☰ {container.title}
      </div>
      
      {/* Container content */}
      <div>
        {container.items.map(item => (
          <SortableItem key={item.id} item={item} />
        ))}
      </div>
    </div>
  );
};
```

## Sortable Item Component

```tsx
import { useSortable } from '@dnd-kit/sortable';
import { CSS } from '@dnd-kit/utilities';

const SortableItem = ({ item }: { item: Item }) => {
  const {
    attributes,
    listeners,
    setNodeRef,
    transform,
    transition,
    isDragging,
  } = useSortable({ id: item.id });

  const style = {
    transform: CSS.Transform.toString(transform),
    transition,
    opacity: isDragging ? 0.5 : 1,
    padding: '8px',
    margin: '4px',
    backgroundColor: '#f5f5f5',
    cursor: 'grab',
  };

  return (
    <div ref={setNodeRef} style={style} {...attributes} {...listeners}>
      {item.content}
    </div>
  );
};
```

## DndContext Setup

```tsx
import {
  DndContext,
  DragEndEvent,
  DragOverlay,
  closestCenter,
  PointerSensor,
  useSensor,
  useSensors,
} from '@dnd-kit/core';
import {
  SortableContext,
  arrayMove,
  verticalListSortingStrategy,
} from '@dnd-kit/sortable';

const App = () => {
  const [containers, setContainers] = useState<Container[]>([
    { id: 'container-1', title: 'Container 1', items: [] },
    { id: 'container-2', title: 'Container 2', items: [] },
  ]);

  const sensors = useSensors(
    useSensor(PointerSensor, {
      activationConstraint: {
        distance: 8,
      },
    })
  );

  const handleDragEnd = (event: DragEndEvent) => {
    const { active, over } = event;
    
    if (!over) return;

    const activeId = active.id.toString();
    const overId = over.id.toString();

    // Handle container reordering
    if (activeId.startsWith('container-') && overId.startsWith('container-')) {
      setContainers(prev => {
        const oldIndex = prev.findIndex(c => c.id === activeId);
        const newIndex = prev.findIndex(c => c.id === overId);
        return arrayMove(prev, oldIndex, newIndex);
      });
    }

    // Handle item dropping into container
    if (activeId.startsWith('item-') && overId.startsWith('container-')) {
      // Implementation in state-management.md
    }
  };

  return (
    <DndContext
      sensors={sensors}
      collisionDetection={closestCenter}
      onDragEnd={handleDragEnd}
    >
      <SortableContext
        items={containers.map(c => c.id)}
        strategy={verticalListSortingStrategy}
      >
        {containers.map(container => (
          <SortableDroppableContainer 
            key={container.id} 
            container={container} 
          />
        ))}
      </SortableContext>
      <DragOverlay>
        {/* Optional: Render dragging preview */}
      </DragOverlay>
    </DndContext>
  );
};
```

## Conditional Logic Pattern Summary

The pattern relies on three key decisions:

1. **Which ref to use**: `isItem ? setDroppableRef : setSortableRef`
2. **Which attributes to apply**: `isContainer ? attributes : {}`
3. **Which listeners to apply**: `isContainer ? listeners : {}`

This ensures clean separation of concerns and predictable behavior.
