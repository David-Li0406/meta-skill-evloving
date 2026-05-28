---
name: mobject-grouping
description: VGroup organization and dictionary mapping patterns from 3b1b
metadata:
  tags: vgroup, grouping, organization, dictionary, mobject
priority: critical
---

# Mobject Grouping Patterns

Patterns observed from 3Blue1Brown's video code for organizing visual elements.

## Core Requirement

**MUST** group related elements using VGroup and dictionary mappings for coordinated manipulation.

**MUST NOT** create loose, unorganized mobjects that are hard to animate together.

---

## Pattern 1: Dictionary Mapping

Map strings/identifiers to visual objects for easy reference.

```python
class NetworkScene(Scene):
    def construct(self):
        # MUST: Create dictionaries for element lookup
        self.node_to_circle = {}
        self.node_to_label = {}
        self.edge_to_line = {}

        # Create nodes with consistent mapping
        for name in ['A', 'B', 'C', 'D', 'E']:
            circle = Circle(radius=0.3, color=BLUE, fill_opacity=0.3)
            label = Text(name, font_size=24)
            label.move_to(circle.get_center())

            self.node_to_circle[name] = circle
            self.node_to_label[name] = label

        # Now you can easily animate by name
        self.play(
            self.node_to_circle['A'].animate.set_fill(GREEN, opacity=0.6),
            Indicate(self.node_to_label['A'])
        )
```

## Pattern 2: VGroup for Logical Units

Group elements that move/transform together.

```python
# MUST: Group related elements
class ArrayVisualization(Scene):
    def construct(self):
        # Each array element is a VGroup of box + label
        self.elements = []

        for i, val in enumerate([3, 7, 11, 15, 19]):
            box = Square(side_length=0.7, color=BLUE)
            label = Text(str(val), font_size=20)
            label.move_to(box.get_center())

            # Group box and label together
            element = VGroup(box, label)
            element.shift(RIGHT * i)
            self.elements.append(element)

        # All elements as one group
        self.array_group = VGroup(*self.elements)

        # Now the entire array can be manipulated as one unit
        self.play(FadeIn(self.array_group))
        self.play(self.array_group.animate.shift(LEFT * 2))
```

## Pattern 3: Nested VGroups

Create hierarchical structure for complex visuals.

```python
class NeuralNetworkScene(Scene):
    def construct(self):
        # Layer groups
        self.layers = []

        for layer_idx in range(3):
            neurons = VGroup()
            for neuron_idx in range(4):
                circle = Circle(radius=0.2, color=BLUE)
                circle.shift(UP * neuron_idx * 0.6)
                neurons.add(circle)

            neurons.shift(RIGHT * layer_idx * 2)
            self.layers.append(neurons)

        # All layers as network
        self.network = VGroup(*self.layers)

        # Animate entire network
        self.play(FadeIn(self.network))

        # Or animate single layer
        self.play(self.layers[1].animate.set_color(GREEN))
```

## Pattern 4: State Dictionary

Track element states for complex animations.

```python
class DijkstraScene(Scene):
    def construct(self):
        # State tracking
        self.node_states = {
            'A': {'distance': 0, 'visited': False},
            'B': {'distance': float('inf'), 'visited': False},
            'C': {'distance': float('inf'), 'visited': False},
        }

        # Visual elements
        self.dist_labels = {}

        for name in self.node_states:
            dist = self.node_states[name]['distance']
            label = Text(str(dist) if dist != float('inf') else '∞')
            self.dist_labels[name] = label

    def update_distance(self, node, new_dist):
        """Update both state and visual."""
        self.node_states[node]['distance'] = new_dist

        new_label = Text(str(new_dist), color=GREEN)
        new_label.move_to(self.dist_labels[node].get_center())

        self.play(Transform(self.dist_labels[node], new_label))
```

## Pattern 5: arrange() for Layout

Use VGroup's arrange methods for consistent spacing.

```python
# Horizontal arrangement
row = VGroup(*[Square() for _ in range(5)])
row.arrange(RIGHT, buff=0.2)

# Vertical arrangement
column = VGroup(*[Circle() for _ in range(4)])
column.arrange(DOWN, buff=0.3)

# Grid arrangement
grid = VGroup(*[
    VGroup(*[Square(side_length=0.5) for _ in range(4)]).arrange(RIGHT, buff=0.1)
    for _ in range(3)
]).arrange(DOWN, buff=0.1)

# With alignment
labels = VGroup(
    Text("First"),
    Text("Second item"),
    Text("Third")
).arrange(DOWN, aligned_edge=LEFT)
```

## Pattern 6: Subgroup Access

Access specific parts of complex groups.

```python
class TableScene(Scene):
    def construct(self):
        # Create table with rows and cells
        self.rows = []
        for i in range(5):
            cells = VGroup(*[
                Square(side_length=0.5).set_fill(WHITE, opacity=0.1)
                for _ in range(3)
            ]).arrange(RIGHT, buff=0)
            self.rows.append(cells)

        self.table = VGroup(*self.rows).arrange(DOWN, buff=0)

        # Access specific cell: row 2, column 1
        target_cell = self.rows[2][1]
        self.play(target_cell.animate.set_fill(YELLOW, opacity=0.5))
```

---

## Quick Reference

| Pattern | Use Case |
|---------|----------|
| `dict[name] = mobject` | Name-based lookup |
| `VGroup(a, b, c)` | Group related elements |
| `group.arrange(DIR, buff=0.2)` | Auto-layout |
| `group[index]` | Access by position |
| `nested_group[i][j]` | Access in hierarchy |

---

## Checklist

```
□ Related elements grouped with VGroup
□ Dictionary mapping for name-based access
□ Hierarchical grouping for complex structures
□ State tracking separate from visuals
□ Using arrange() for consistent layout
□ Subgroup access for targeted animations
```
