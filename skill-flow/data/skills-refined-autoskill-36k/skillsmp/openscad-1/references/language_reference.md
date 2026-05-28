# OpenSCAD Language Reference

Complete syntax reference for OpenSCAD primitives, transformations, and operations.

## Data Types

### Numbers
```openscad
x = 42;           // integer
y = 3.14159;      // float
z = 2.99e8;       // scientific notation
PI                // built-in constant (3.14159...)
```

### Booleans
```openscad
flag = true;
other = false;
// Falsy values: false, 0, "", [], undef
```

### Strings
```openscad
name = "Hello";
escaped = "Line1\nLine2";  // \n newline, \t tab, \\ backslash
unicode = "\u03C0";        // π character
```

### Vectors
```openscad
point = [1, 2, 3];
point.x;  // 1 (same as point[0])
point.y;  // 2 (same as point[1])  
point.z;  // 3 (same as point[2])
len(point);  // 3
nested = [[1,2], [3,4]];
```

### Ranges
```openscad
r1 = [0:10];      // 0,1,2,...,10
r2 = [0:2:10];    // 0,2,4,6,8,10
r3 = [10:-1:0];   // 10,9,8,...,0
```

## 3D Primitives

### cube
```openscad
cube(size);                    // cube with equal sides
cube([width, depth, height]);  // rectangular box
cube([10, 20, 5], center=true);
```

### sphere
```openscad
sphere(r=10);      // by radius
sphere(d=20);      // by diameter
sphere(r=10, $fn=100);  // high resolution
```

### cylinder
```openscad
cylinder(h=20, r=5);              // cylinder
cylinder(h=20, r1=10, r2=5);      // cone (tapered)
cylinder(h=20, d=10, center=true);
cylinder(h=20, d1=20, d2=10);     // cone by diameter
```

### polyhedron
```openscad
// Define points and faces (clockwise winding from outside)
polyhedron(
    points = [
        [0,0,0], [10,0,0], [10,10,0], [0,10,0],  // bottom
        [0,0,10], [10,0,10], [10,10,10], [0,10,10]  // top
    ],
    faces = [
        [0,1,2,3],    // bottom
        [4,5,1,0],    // front
        [7,6,5,4],    // top
        [5,6,2,1],    // right
        [6,7,3,2],    // back
        [7,4,0,3]     // left
    ]
);
```

## 2D Primitives

### square
```openscad
square(10);              // 10x10 square
square([20, 10]);        // rectangle
square([20, 10], center=true);
```

### circle
```openscad
circle(r=5);
circle(d=10);
circle(r=5, $fn=6);  // hexagon
circle(r=5, $fn=3);  // triangle
```

### polygon
```openscad
// Simple polygon
polygon(points=[[0,0], [10,0], [5,10]]);

// Polygon with holes
polygon(
    points=[[0,0], [20,0], [20,20], [0,20],  // outer (0-3)
            [5,5], [15,5], [10,15]],          // hole (4-6)
    paths=[[0,1,2,3], [4,5,6]]
);
```

### text
```openscad
text("Hello", size=10);
text("World", size=8, font="Liberation Sans:style=Bold");
text("Centered", halign="center", valign="center");
// halign: "left", "center", "right"
// valign: "top", "center", "baseline", "bottom"
```

## Transformations

### translate
```openscad
translate([x, y, z]) child();
translate([10, 0, 0]) cube(5);
```

### rotate
```openscad
rotate([x_deg, y_deg, z_deg]) child();
rotate([0, 0, 45]) square(10);
rotate(a=45, v=[1,1,0]) cube(5);  // around arbitrary axis
```

### scale
```openscad
scale([x, y, z]) child();
scale([2, 1, 0.5]) sphere(5);
scale(2) cube(5);  // uniform scale
```

### resize
```openscad
resize([30, 20, 10]) sphere(1);  // resize to exact dimensions
resize([30, 0, 0], auto=true) cube(10);  // auto-scale proportionally
```

### mirror
```openscad
mirror([1, 0, 0]) child();  // mirror across YZ plane
mirror([0, 1, 0]) child();  // mirror across XZ plane
mirror([0, 0, 1]) child();  // mirror across XY plane
mirror([1, 1, 0]) child();  // mirror across diagonal plane
```

### multmatrix
```openscad
// 4x4 transformation matrix
multmatrix([
    [1, 0, 0, tx],   // x scale, xy shear, xz shear, x translate
    [0, 1, 0, ty],   // yx shear, y scale, yz shear, y translate
    [0, 0, 1, tz],   // zx shear, zy shear, z scale, z translate
    [0, 0, 0, 1]
]) child();
```

### color
```openscad
color("red") cube(5);
color("DeepSkyBlue") sphere(3);
color([1, 0.5, 0]) cube(5);      // RGB 0-1
color([1, 0, 0, 0.5]) sphere(3); // RGBA with transparency
color("#FF5500") cube(5);        // hex color
```

### offset (2D only)
```openscad
offset(r=5) square(10);      // round corners (outward)
offset(r=-2) square(10);     // round corners (inward)
offset(delta=3) square(10);  // sharp corners
offset(delta=3, chamfer=true) square(10);  // chamfered corners
```

### hull
```openscad
// Convex hull of children
hull() {
    translate([0, 0, 0]) cylinder(r=5, h=1);
    translate([20, 0, 0]) cylinder(r=5, h=1);
}
```

### minkowski
```openscad
// Minkowski sum - rounds edges
minkowski() {
    cube([10, 10, 2]);
    sphere(r=1);  // rounds all edges with r=1
}
```

## Boolean Operations

### union
```openscad
union() {
    cube(10);
    translate([5, 5, 5]) sphere(8);
}
// Note: objects without explicit boolean are implicitly unioned
```

### difference
```openscad
difference() {
    cube(10);                          // base shape
    translate([5, 5, -1]) cylinder(h=12, r=3);  // subtracted
    translate([2, 2, 5]) sphere(2);    // also subtracted
}
```

### intersection
```openscad
intersection() {
    cube(10, center=true);
    sphere(7);
}
```

## Extrusion

### linear_extrude
```openscad
linear_extrude(height=10) circle(5);
linear_extrude(height=20, twist=90) square(10, center=true);
linear_extrude(height=10, scale=2) circle(5);  // flared
linear_extrude(height=10, scale=[2, 0.5]) square(5);  // asymmetric
linear_extrude(height=20, twist=360, slices=100, $fn=50) 
    translate([10, 0]) circle(3);
```

### rotate_extrude
```openscad
// Shape must be on positive X side of Y axis
rotate_extrude($fn=100) 
    translate([10, 0]) circle(3);  // torus

rotate_extrude(angle=180) 
    translate([10, 0]) square([3, 5]);  // half ring

// Profile for a vase
rotate_extrude($fn=100) 
    polygon([[5,0], [8,0], [10,20], [8,30], [6,30], [8,20], [6,5], [5,5]]);
```

## Modules and Functions

### Modules
```openscad
module box_with_hole(size, hole_d) {
    difference() {
        cube(size, center=true);
        cylinder(h=size+1, d=hole_d, center=true);
    }
}

box_with_hole(20, 8);
box_with_hole(size=30, hole_d=10);
```

### Modules with Children
```openscad
module rounded(r=2) {
    minkowski() {
        children();
        sphere(r);
    }
}

rounded(r=1) cube(10);
```

### children()
```openscad
module distribute(spacing=10) {
    for (i = [0:$children-1])
        translate([i * spacing, 0, 0])
            children(i);
}

distribute(15) {
    cube(5);
    sphere(3);
    cylinder(h=10, r=2);
}
```

### Functions
```openscad
function add(a, b) = a + b;
function area(r) = PI * r * r;
function factorial(n) = n <= 1 ? 1 : n * factorial(n-1);

echo(add(3, 4));      // 7
echo(area(5));        // 78.5398
echo(factorial(5));   // 120
```

## Control Flow

### for loops
```openscad
// Range iteration
for (i = [0:5]) 
    translate([i*10, 0, 0]) cube(5);

// With step
for (i = [0:2:10])
    translate([i, 0, 0]) sphere(1);

// List iteration  
for (pos = [[0,0], [10,10], [20,0]])
    translate(pos) cylinder(h=5, r=2);

// Multiple iterators
for (x = [0:2], y = [0:2])
    translate([x*10, y*10, 0]) cube(5);
```

### if/else
```openscad
module shape(type) {
    if (type == "cube")
        cube(10);
    else if (type == "sphere")
        sphere(5);
    else
        cylinder(h=10, r=5);
}
```

### Conditional expression
```openscad
size = large ? 20 : 10;
shape = round ? sphere(5) : cube(10);
```

### let
```openscad
let(a = 5, b = a * 2)
    cube([a, b, a+b]);
```

## Math Functions

```openscad
// Trigonometry (degrees)
sin(45)   cos(45)   tan(45)
asin(x)   acos(x)   atan(x)   atan2(y, x)

// Rounding
floor(3.7)   // 3
ceil(3.2)    // 4
round(3.5)   // 4

// Other
abs(-5)      // 5
sign(-5)     // -1
sqrt(16)     // 4
pow(2, 8)    // 256
exp(1)       // 2.71828
ln(10)       // 2.30259
log(100)     // 2

// Min/Max
min(1, 5, 3)   // 1
max(1, 5, 3)   // 5

// Vector math
norm([3, 4])        // 5 (length)
cross([1,0,0], [0,1,0])  // [0, 0, 1]

// Random
rands(0, 10, 5)     // 5 random numbers 0-10
rands(0, 10, 5, 42) // seeded random
```

## String Functions

```openscad
str("Value: ", 42)        // "Value: 42"
len("hello")              // 5
chr(65)                   // "A"
ord("A")                  // 65
search("l", "hello")      // [2] (first occurrence)
```

## List Comprehensions

```openscad
// Generate list
squares = [for (i = [1:5]) i*i];  // [1, 4, 9, 16, 25]

// With condition
evens = [for (i = [1:10]) if (i % 2 == 0) i];  // [2, 4, 6, 8, 10]

// Nested
coords = [for (x = [0:2], y = [0:2]) [x, y]];

// Flatten
flat = [for (row = [[1,2], [3,4]]) each row];  // [1, 2, 3, 4]
```

## Import/Export

### import
```openscad
import("model.stl");
import("drawing.dxf");
import("shape.svg");

// With layer (DXF)
import("drawing.dxf", layer="outline");
```

### surface
```openscad
surface(file="heightmap.png", center=true);
surface(file="data.dat", center=true, convexity=5);
```

## Debugging

### Modifier Characters
```openscad
*cube(10);   // disable (comment out)
!sphere(5);  // show only this
#cube(10);   // highlight/debug
%cylinder(h=10, r=5);  // transparent/background
```

### echo
```openscad
echo("Debug:", variable);
echo(str("Area = ", PI * r * r));
```

### assert
```openscad
assert(r > 0, "Radius must be positive");
```

## Special Variables

```openscad
$fn = 50;     // number of facets (fragments) in full circle
$fa = 12;     // minimum angle per fragment
$fs = 2;      // minimum fragment size in mm

$preview      // true in F5 preview, false in F6 render
$t            // animation time 0-1

$vpr          // viewport rotation [x, y, z]
$vpt          // viewport translation [x, y, z]
$vpd          // viewport distance

$children     // number of child objects in module
$parent_modules  // depth of module nesting
```

## File Organization

### include vs use
```openscad
include <library.scad>  // imports everything (modules, functions, geometry)
use <library.scad>      // imports only modules and functions
```
