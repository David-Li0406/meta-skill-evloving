# OpenSCAD Modification Patterns

Common patterns for modifying existing 3D models.

## Table of Contents
1. [Resizing](#resizing)
2. [Adding Features](#adding-features)
3. [Removing Material](#removing-material)
4. [Combining Objects](#combining-objects)
5. [Edge Treatments](#edge-treatments)
6. [Arrays and Patterns](#arrays-and-patterns)
7. [Parametric Techniques](#parametric-techniques)

---

## Resizing

### Scale uniformly
```scad
scale([1.5, 1.5, 1.5]) existing_object();  // 150% all axes
```

### Scale single axis
```scad
scale([1, 1, 2]) existing_object();        // Double height only
```

### Resize to exact dimensions
```scad
resize([50, 0, 0], auto=true) existing_object();  // 50mm wide, proportional
resize([50, 30, 20]) existing_object();           // Exact dimensions
```

### Stretch/compress
```scad
scale([2, 0.5, 1]) existing_object();      // Wide and flat
```

---

## Adding Features

### Add mounting holes pattern
```scad
module with_mounting_holes(hole_d=3, spacing=20) {
    difference() {
        children();
        for (x = [-1, 1], y = [-1, 1])
            translate([x*spacing/2, y*spacing/2, -1])
                cylinder(d=hole_d, h=100);
    }
}
with_mounting_holes() existing_object();
```

### Add boss/standoff
```scad
union() {
    existing_object();
    translate([x, y, z]) cylinder(d=10, h=5);
}
```

### Add flange/lip
```scad
union() {
    existing_object();
    translate([0, 0, height])
        linear_extrude(3) offset(r=5) projection() existing_object();
}
```

### Add text/label
```scad
union() {
    existing_object();
    translate([x, y, z])
        linear_extrude(1) text("LABEL", size=5);
}
// Or engraved:
difference() {
    existing_object();
    translate([x, y, z-0.5])
        linear_extrude(1) text("LABEL", size=5);
}
```

### Add reinforcement rib
```scad
union() {
    existing_object();
    translate([x, y, 0])
        linear_extrude(height) polygon([[0,0], [thick,0], [0,length]]);
}
```

---

## Removing Material

### Add single hole
```scad
difference() {
    existing_object();
    translate([x, y, z]) cylinder(d=hole_diameter, h=depth);
}
```

### Counterbore hole
```scad
difference() {
    existing_object();
    translate([x, y, -1]) {
        cylinder(d=3, h=50);           // Through hole
        cylinder(d=6, h=5);            // Counterbore
    }
}
```

### Countersink hole
```scad
difference() {
    existing_object();
    translate([x, y, z]) {
        cylinder(d=3, h=50);           // Shaft
        cylinder(d1=8, d2=3, h=3);     // Countersink
    }
}
```

### Create slot
```scad
difference() {
    existing_object();
    translate([x, y, z]) hull() {
        cylinder(d=slot_width, h=depth);
        translate([slot_length, 0, 0]) cylinder(d=slot_width, h=depth);
    }
}
```

### Hollow out (shell)
```scad
difference() {
    existing_object();
    translate([0, 0, wall])
        scale([(size-2*wall)/size, (size-2*wall)/size, 1])
            existing_object();
}
// Or with offset for complex shapes:
difference() {
    linear_extrude(h) shape();
    translate([0, 0, wall]) linear_extrude(h) offset(-wall) shape();
}
```

### Cut in half
```scad
intersection() {
    existing_object();
    translate([-500, -500, 0]) cube([1000, 1000, 1000]);  // Keep bottom half
}
```

### Remove section
```scad
difference() {
    existing_object();
    translate([x, y, z]) cube([cut_x, cut_y, cut_z]);
}
```

---

## Combining Objects

### Side by side
```scad
union() {
    existing_object();
    translate([offset, 0, 0]) other_object();
}
```

### Stacked
```scad
union() {
    existing_object();
    translate([0, 0, height1]) other_object();
}
```

### Overlapping join
```scad
union() {
    existing_object();
    translate([0, 0, height1 - overlap]) other_object();
}
```

### Boolean combine
```scad
intersection() {
    existing_object();
    other_object();    // Keep only where both exist
}
```

---

## Edge Treatments

### Round all edges (slow but universal)
```scad
minkowski() {
    // Shrink original to compensate for sphere
    resize([w-2*r, d-2*r, h-2*r]) existing_object();
    sphere(r=r);
}
```

### Round selected edges with hull
```scad
hull() {
    translate([r, r, r]) sphere(r);
    translate([w-r, r, r]) sphere(r);
    translate([r, d-r, r]) sphere(r);
    translate([w-r, d-r, r]) sphere(r);
    // ... top corners
}
```

### Chamfer edge
```scad
difference() {
    existing_object();
    translate([0, 0, height])
        rotate([45, 0, 0])
            cube([width+2, chamfer*2, chamfer*2], center=true);
}
```

### Fillet inside corner (2D then extrude)
```scad
linear_extrude(h) difference() {
    square([w, d]);
    translate([r, r]) difference() {
        square([r, r]);
        circle(r);
    }
}
```

---

## Arrays and Patterns

### Linear array
```scad
for (i = [0:count-1])
    translate([i * spacing, 0, 0]) existing_object();
```

### Grid array
```scad
for (x = [0:cols-1], y = [0:rows-1])
    translate([x * spacing_x, y * spacing_y, 0]) existing_object();
```

### Circular/radial array
```scad
for (i = [0:count-1])
    rotate([0, 0, i * 360/count])
        translate([radius, 0, 0]) existing_object();
```

### Along path
```scad
path = [[0,0], [10,5], [20,0], [30,10]];
for (i = [0:len(path)-1])
    translate([path[i][0], path[i][1], 0]) existing_object();
```

### Mirror copy
```scad
union() {
    existing_object();
    mirror([1, 0, 0]) existing_object();
}
```

---

## Parametric Techniques

### Make dimensions variable
```scad
// At top of file:
width = 50;
height = 30;
wall = 2;

// Replace hardcoded values:
cube([width, height, wall]);
```

### Conditional geometry
```scad
with_holes = true;
if (with_holes) {
    difference() {
        base();
        holes();
    }
} else {
    base();
}
```

### Calculated dimensions
```scad
outer_d = 20;
wall = 2;
inner_d = outer_d - 2*wall;

difference() {
    cylinder(d=outer_d, h=10);
    cylinder(d=inner_d, h=11);
}
```

### Module with parameters
```scad
module box(w, d, h, wall=2) {
    difference() {
        cube([w, d, h]);
        translate([wall, wall, wall])
            cube([w-2*wall, d-2*wall, h]);
    }
}
box(50, 30, 20);
box(100, 50, 40, wall=3);
```

---

## Quick Fixes

### Object not centered
```scad
translate([-w/2, -d/2, -h/2]) existing_object();
// Or wrap:
module centered() { translate([-w/2, -d/2, -h/2]) children(); }
```

### Wrong orientation
```scad
rotate([90, 0, 0]) existing_object();   // Lay flat
rotate([0, 90, 0]) existing_object();   // Rotate around Y
rotate([0, 0, 45]) existing_object();   // Rotate in XY plane
```

### Flip upside down
```scad
mirror([0, 0, 1]) translate([0, 0, -height]) existing_object();
```

### Move to origin
```scad
translate([-min_x, -min_y, -min_z]) existing_object();
```
