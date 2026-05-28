# Parsing Cookbook

Recipes for extracting data from AoC inputs.

---

## Extract All Integers

**Problem**: Numbers scattered in text like `"pos=<3,-5>, vel=<-2,1>"`.

**Solution**:
```python
import re
nums = [int(x) for x in re.findall(r'-?\d+', line)]
# [3, -5, -2, 1]
```

**Tip**: `-?` handles negative numbers. Works on most AoC inputs.

---

## Parse Character Grid

**Problem**: Grid of characters, need 2D access.

**Solution** (dense):
```python
lines = input.strip().split('\n')
grid = [list(line) for line in lines]
value = grid[row][col]
```

**Solution** (sparse/dict):
```python
grid = {}
for row, line in enumerate(lines):
    for col, char in enumerate(line):
        if char != '.':
            grid[(row, col)] = char

value = grid.get((row, col), '.')
```

**Tip**: Use sparse for infinite grids or when most cells are empty.

---

## Parse Blank-Line Groups

**Problem**: Input has sections separated by blank lines.

**Solution**:
```python
groups = input.strip().split('\n\n')
for group in groups:
    items = group.split('\n')
```

**Tip**: Common for "first section = rules, second section = data".

---

## Parse Key-Value Pairs

**Problem**: Lines like `"name: value"` or `"key=value"`.

**Solution**:
```python
data = {}
for line in lines:
    key, value = line.split(': ')  # or '='
    data[key] = value
```

**Tip**: May need to cast value to int or further parse.

---

## Parse Instructions/Opcodes

**Problem**: Lines like `"mov R1 42"` or `"jnz x -3"`.

**Solution**:
```python
for line in lines:
    parts = line.split()
    op, args = parts[0], parts[1:]

    match op:
        case 'mov': ...
        case 'jnz': ...
```

**Tip**: Use regex for complex formats: `re.match(r'(\w+) (\w+) (-?\d+)', line)`

---

## Cardinal Directions

**Problem**: Need to move in 4 directions on a grid.

**Solution**:
```python
UP, DOWN = (-1, 0), (1, 0)
LEFT, RIGHT = (0, -1), (0, 1)
DIRS4 = [UP, DOWN, LEFT, RIGHT]

# Move:
new_row, new_col = row + dr, col + dc
```

**Tip**: `(row, col)` with row increasing downward matches visual grid layout.

---

## 8-Directional Movement

**Problem**: Need diagonals too.

**Solution**:
```python
DIRS8 = [(dr, dc)
         for dr in [-1, 0, 1]
         for dc in [-1, 0, 1]
         if (dr, dc) != (0, 0)]
```

---

## Direction from Characters

**Problem**: Input uses `^v<>` or `UDLR` for directions.

**Solution**:
```python
DIR_MAP = {
    'U': (-1, 0), '^': (-1, 0),
    'D': (1, 0),  'v': (1, 0),
    'L': (0, -1), '<': (0, -1),
    'R': (0, 1),  '>': (0, 1),
}
dr, dc = DIR_MAP[char]
```

---

## Rotation

**Problem**: Turn left/right on a grid.

**Solution** (tuples):
```python
# 90° clockwise:     (row, col) → (col, -row)
# 90° counter-clock: (row, col) → (-col, row)
# 180°:              (row, col) → (-row, -col)
```

**Solution** (complex numbers):
```python
pos = col + row * 1j
turn_right = pos * -1j
turn_left = pos * 1j
```

**Tip**: Complex numbers make rotation trivial.

---

## Hex Grid

**Problem**: Hex grid with directions like `ne`, `sw`.

**Solution** (cube coordinates, x + y + z = 0):
```python
HEX_DIRS = {
    'e':  (1, -1, 0),  'w':  (-1, 1, 0),
    'ne': (1, 0, -1),  'sw': (-1, 0, 1),
    'nw': (0, 1, -1),  'se': (0, -1, 1),
}

def hex_move(pos, direction):
    dx, dy, dz = HEX_DIRS[direction]
    return (pos[0]+dx, pos[1]+dy, pos[2]+dz)

def hex_distance(a, b):
    return (abs(a[0]-b[0]) + abs(a[1]-b[1]) + abs(a[2]-b[2])) // 2
```

---

## Bounds Checking

**Problem**: Need to check if position is valid.

**Solution**:
```python
def in_bounds(row, col, grid):
    return 0 <= row < len(grid) and 0 <= col < len(grid[0])

def neighbors(row, col, grid):
    for dr, dc in DIRS4:
        nr, nc = row + dr, col + dc
        if in_bounds(nr, nc, grid):
            yield nr, nc
```

**Tip**: For sparse grids, use `grid.get((r,c), default)` instead.

---

## Wrapping (Toroidal Grid)

**Problem**: Grid wraps around edges.

**Solution**:
```python
row = row % height
col = col % width
```

---

## Padding with Sentinels

**Problem**: Avoid bounds checking by padding edges.

**Solution**:
```python
padded = [['#'] * (width + 2)]
for line in lines:
    padded.append(['#'] + list(line) + ['#'])
padded.append(['#'] * (width + 2))
```

**Tip**: Choose sentinel that won't appear in real data.
