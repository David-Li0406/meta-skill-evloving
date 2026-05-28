# OpenSCAD Syntax Reference

## Table of Contents
1. [3D Primitives](#3d-primitives)
2. [2D Primitives](#2d-primitives)
3. [Transformations](#transformations)
4. [Boolean Operations](#boolean-operations)
5. [Extrusions](#extrusions)
6. [Modules and Functions](#modules-and-functions)
7. [Control Flow](#control-flow)
8. [Special Variables](#special-variables)

## 3D Primitives

```scad
cube(size);                              // Single value = cube
cube([x, y, z]);                         // Vector = rectangular prism
cube(size, center=true);                 // Centered at origin

sphere(r=radius);                        // By radius
sphere(d=diameter);                      // By diameter

cylinder(h=height, r=radius);            // Uniform radius
cylinder(h=height, r1=bottom, r2=top);   // Cone/tapered
cylinder(h=height, d=diameter);          // By diameter
cylinder(h=height, d1=bottom, d2=top);   // Tapered by diameter
cylinder(h, r, center=true);             // Centered on Z

polyhedron(points=[[x,y,z],...], faces=[[0,1,2],...]);
```

## 2D Primitives

```scad
circle(r=radius);
circle(d=diameter);

square(size);                            // Square
square([x, y]);                          // Rectangle
square(size, center=true);               // Centered

polygon(points=[[x,y],...]);             // Simple polygon
polygon(points=[[x,y],...], paths=[[0,1,2,...]]);  // With holes

text("string", size=10, font="Liberation Sans");
```

## Transformations

```scad
translate([x, y, z]) object;

rotate([x_deg, y_deg, z_deg]) object;    // Euler angles
rotate(a=angle, v=[x,y,z]) object;       // Axis-angle

scale([x, y, z]) object;

mirror([x, y, z]) object;                // Mirror across plane normal to vector

resize([x, y, z]) object;                // Resize to exact dimensions
resize([x, y, z], auto=true) object;     // Auto-scale undefined axes

color("red") object;                     // Named color
color([r, g, b]) object;                 // RGB 0-1
color([r, g, b, a]) object;              // RGBA

multmatrix(m) object;                    // 4x4 transformation matrix

hull() { objects; }                      // Convex hull of children

minkowski() { base; tool; }              // Minkowski sum (rounds edges)
```

## Boolean Operations

```scad
union() {
    object1;
    object2;
}

difference() {
    base_object;      // Keep this
    subtract1;        // Remove these
    subtract2;
}

intersection() {
    object1;
    object2;          // Keep only overlapping volume
}
```

## Extrusions

```scad
linear_extrude(height=h) 2d_shape;
linear_extrude(height=h, center=true) 2d_shape;
linear_extrude(height=h, twist=degrees) 2d_shape;
linear_extrude(height=h, scale=factor) 2d_shape;    // Taper
linear_extrude(height=h, scale=[x,y]) 2d_shape;     // Non-uniform taper
linear_extrude(height=h, slices=n) 2d_shape;        // Resolution

rotate_extrude(angle=360) 2d_shape;     // 2D shape must be on positive X
rotate_extrude(angle=90, $fn=100) 2d_shape;

offset(r=radius) 2d_shape;              // Rounded expand/contract
offset(delta=distance) 2d_shape;        // Sharp corners
offset(delta=d, chamfer=true) 2d_shape; // Chamfered corners

projection(cut=false) 3d_object;        // Project to XY plane
projection(cut=true) 3d_object;         // Slice at Z=0
```

## Modules and Functions

```scad
// Module (creates geometry)
module name(param1, param2=default) {
    // geometry
    children();  // Pass through child objects
}
name(value1, value2);

// Function (returns value)
function name(x, y) = x + y;
result = name(1, 2);

// Include vs Use
include <file.scad>   // Execute all code
use <file.scad>       // Import modules/functions only

// Import external files
import("model.stl");
import("drawing.svg");
import("drawing.dxf");
```

## Control Flow

```scad
// For loop
for (i = [0:10]) translate([i*5, 0, 0]) cube(1);
for (i = [0:2:10]) cube(i);              // Step by 2
for (p = [[0,0], [10,0], [5,10]]) translate(p) sphere(1);

// If statement
if (condition) {
    object1;
} else {
    object2;
}

// Ternary
size = (large) ? 10 : 5;

// Intersection for loop (creates intersections)
intersection_for(i = [0:2]) rotate([0, 0, i*60]) cube(10);

// Let (local variables)
let (x = 10, y = x * 2) cube([x, y, 5]);
```

## Special Variables

```scad
$fn = 100;           // Number of fragments (circle resolution)
$fa = 12;            // Minimum angle per fragment
$fs = 2;             // Minimum fragment size

$t                   // Animation time 0-1
$vpr                 // Viewport rotation
$vpt                 // Viewport translation
$vpd                 // Viewport distance
$vpf                 // Viewport FOV

$children            // Number of child objects
$preview             // true in preview, false in render
```

## Mathematical Functions

```scad
// Trigonometry (degrees)
sin(deg), cos(deg), tan(deg)
asin(x), acos(x), atan(x), atan2(y, x)

// Other math
abs(x), sign(x), floor(x), ceil(x), round(x)
sqrt(x), pow(base, exp), exp(x), ln(x), log(x)
min(a, b, ...), max(a, b, ...)

// Vector operations
norm(v)              // Length of vector
cross(v1, v2)        // Cross product
len(list)            // Length of list/string

// List operations
concat(list1, list2)
lookup(key, [[k,v],...])
```

## Common Patterns

```scad
// Centered hole in plate
difference() {
    cube([20, 20, 5], center=true);
    cylinder(h=6, d=8, center=true);
}

// Rounded cube (minkowski with sphere)
minkowski() {
    cube([10, 10, 10]);
    sphere(r=2);
}

// Hollow box
difference() {
    cube([20, 20, 20]);
    translate([2, 2, 2]) cube([16, 16, 20]);
}

// Fillet edge (hull two cylinders)
hull() {
    translate([0, 0, 0]) cylinder(r=5, h=1);
    translate([20, 0, 0]) cylinder(r=5, h=1);
}
```
