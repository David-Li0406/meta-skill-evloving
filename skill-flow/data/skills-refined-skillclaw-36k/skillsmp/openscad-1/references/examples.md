# OpenSCAD Example Patterns

Practical patterns and examples for common 3D modeling tasks.

## Basic Structural Patterns

### Rounded Box
```openscad
module rounded_box(size, radius) {
    hull() {
        for (x = [radius, size.x - radius])
            for (y = [radius, size.y - radius])
                translate([x, y, 0])
                    cylinder(r=radius, h=size.z);
    }
}

rounded_box([30, 20, 10], 3);
```

### Box with Rounded Edges (All Sides)
```openscad
module rounded_cube(size, r) {
    minkowski() {
        cube([size.x - 2*r, size.y - 2*r, size.z - 2*r], center=true);
        sphere(r);
    }
}

rounded_cube([30, 20, 10], 2);
```

### Hollow Box
```openscad
module hollow_box(outer, wall) {
    difference() {
        cube(outer);
        translate([wall, wall, wall])
            cube([outer.x - 2*wall, outer.y - 2*wall, outer.z]);
    }
}

hollow_box([30, 20, 15], 2);
```

### Box with Lid
```openscad
module box_with_lid(size, wall, lid_height, gap=0.3) {
    // Box
    difference() {
        cube(size);
        translate([wall, wall, wall])
            cube([size.x - 2*wall, size.y - 2*wall, size.z]);
    }
    
    // Lid (offset for printing)
    translate([size.x + 5, 0, 0])
        difference() {
            cube([size.x, size.y, lid_height]);
            translate([wall + gap, wall + gap, -1])
                cube([size.x - 2*wall - 2*gap, 
                      size.y - 2*wall - 2*gap, 
                      lid_height - wall + 1]);
        }
}

box_with_lid([40, 30, 20], 2, 8);
```

## Mechanical Parts

### Screw Hole with Counterbore
```openscad
module counterbore_hole(depth, hole_d, cbore_d, cbore_depth) {
    union() {
        cylinder(h=depth, d=hole_d);
        cylinder(h=cbore_depth, d=cbore_d);
    }
}

difference() {
    cube([30, 30, 10], center=true);
    translate([0, 0, 5])
        rotate([180, 0, 0])
            counterbore_hole(12, 3.2, 6, 3);
}
```

### Bolt Pattern
```openscad
module bolt_pattern(count, radius, hole_d) {
    for (i = [0:count-1])
        rotate([0, 0, i * 360/count])
            translate([radius, 0, 0])
                children();
}

difference() {
    cylinder(h=5, r=25);
    bolt_pattern(6, 18, 4)
        cylinder(h=10, d=4, center=true);
}
```

### Thread (Simplified Helix)
```openscad
module thread(d, pitch, length, $fn=30) {
    cylinder(d=d - pitch, h=length);
    linear_extrude(height=length, twist=360 * length/pitch, convexity=10)
        translate([d/2 - pitch/2, 0])
            circle(d=pitch * 0.8, $fn=3);
}

thread(10, 1.5, 20);
```

### Gear (Simplified)
```openscad
module gear(teeth, pitch, thickness, hole_d) {
    pitch_radius = teeth * pitch / (2 * PI);
    outer_radius = pitch_radius + pitch/2;
    
    difference() {
        linear_extrude(height=thickness)
            difference() {
                circle(r=outer_radius, $fn=teeth*4);
                for (i = [0:teeth-1])
                    rotate([0, 0, i * 360/teeth])
                        translate([pitch_radius, 0])
                            circle(r=pitch/2, $fn=20);
            }
        cylinder(h=thickness+1, d=hole_d, center=true);
    }
}

gear(20, 3, 5, 6);
```

## Enclosures

### Electronics Enclosure
```openscad
module enclosure(inner_size, wall, corner_r, standoff_h=3, standoff_d=5, screw_d=2.5) {
    outer = [inner_size.x + 2*wall, inner_size.y + 2*wall, inner_size.z + wall];
    
    difference() {
        // Outer shell with rounded corners
        hull() {
            for (x = [corner_r, outer.x - corner_r])
                for (y = [corner_r, outer.y - corner_r])
                    translate([x, y, 0])
                        cylinder(r=corner_r, h=outer.z);
        }
        
        // Inner cavity
        translate([wall, wall, wall])
            cube(inner_size);
    }
    
    // Standoffs
    for (x = [wall + standoff_d/2, outer.x - wall - standoff_d/2])
        for (y = [wall + standoff_d/2, outer.y - wall - standoff_d/2])
            translate([x, y, wall])
                difference() {
                    cylinder(d=standoff_d, h=standoff_h);
                    cylinder(d=screw_d, h=standoff_h + 1);
                }
}

enclosure([60, 40, 25], 2, 3);
```

### Raspberry Pi Case
```openscad
// Raspberry Pi 4 dimensions
pi_size = [85, 56, 20];
wall = 2;
gap = 0.5;

module pi_case() {
    difference() {
        // Outer box
        rounded_box([pi_size.x + 2*wall + 2*gap, 
                     pi_size.y + 2*wall + 2*gap, 
                     pi_size.z + wall], 3);
        
        // Inner cavity
        translate([wall, wall, wall])
            cube([pi_size.x + 2*gap, pi_size.y + 2*gap, pi_size.z + 1]);
        
        // USB ports
        translate([pi_size.x + wall, wall + 8, wall + 3])
            cube([10, 40, 15]);
        
        // Ethernet
        translate([pi_size.x + wall, wall + 48, wall + 3])
            cube([10, 15, 15]);
        
        // SD card slot
        translate([-1, wall + 20, wall])
            cube([10, 15, 3]);
        
        // Ventilation
        for (i = [0:5])
            translate([20 + i*8, -1, wall + 5])
                cube([4, wall + 2, 10]);
    }
}

pi_case();
```

## Decorative Objects

### Vase
```openscad
module vase(height, base_r, top_r, wall) {
    difference() {
        rotate_extrude($fn=100)
            polygon([
                [0, 0],
                [base_r, 0],
                [base_r, 5],
                [top_r, height - 10],
                [top_r + 5, height],
                [0, height]
            ]);
        
        translate([0, 0, wall])
            rotate_extrude($fn=100)
                polygon([
                    [0, 0],
                    [base_r - wall, 0],
                    [base_r - wall, 5 - wall],
                    [top_r - wall, height - 10],
                    [top_r + 5 - wall, height],
                    [0, height]
                ]);
    }
}

vase(80, 20, 15, 2);
```

### Twisted Pillar
```openscad
module twisted_pillar(height, size, twist_deg, $fn=4) {
    linear_extrude(height=height, twist=twist_deg, slices=height*2)
        square(size, center=true);
}

twisted_pillar(50, 10, 180);
```

### Star
```openscad
module star(points, outer_r, inner_r, h) {
    linear_extrude(height=h)
        polygon([for (i = [0:points*2-1]) 
            let(r = i % 2 == 0 ? outer_r : inner_r,
                a = i * 180/points)
            [r * cos(a), r * sin(a)]
        ]);
}

star(5, 20, 8, 3);
```

## Practical Objects

### Phone Stand
```openscad
module phone_stand(width, angle=70) {
    back_height = 80;
    base_depth = 50;
    thickness = 4;
    lip = 8;
    
    // Base
    cube([width, base_depth, thickness]);
    
    // Back support
    translate([0, 0, 0])
        rotate([90 - angle, 0, 0])
            cube([width, back_height, thickness]);
    
    // Front lip
    translate([0, thickness * cos(90-angle), 0])
        cube([width, lip, thickness + 10]);
    
    // Side supports
    for (x = [0, width - thickness])
        translate([x, 0, 0])
            linear_extrude(height=thickness)
                polygon([
                    [0, 0],
                    [0, base_depth],
                    [thickness, base_depth],
                    [thickness, thickness * cos(90-angle) + lip],
                    [thickness, 0]
                ]);
}

phone_stand(70);
```

### Cable Clip
```openscad
module cable_clip(cable_d, wall=2, base_h=3) {
    outer_d = cable_d + 2*wall;
    gap = cable_d * 0.4;
    
    difference() {
        union() {
            // Base
            cylinder(h=base_h, d=outer_d + 4);
            // Ring
            translate([0, 0, base_h])
                cylinder(h=cable_d, d=outer_d);
        }
        // Cable hole
        translate([0, 0, base_h])
            cylinder(h=cable_d + 1, d=cable_d);
        // Entry gap
        translate([-gap/2, 0, base_h])
            cube([gap, outer_d, cable_d + 1]);
    }
}

cable_clip(6);
```

### Hook
```openscad
module hook(length=30, radius=8, thickness=4) {
    // Vertical part
    cube([thickness, thickness, length]);
    
    // Curved part
    translate([0, thickness, length])
        rotate([90, 0, 0])
            rotate_extrude(angle=180, $fn=50)
                translate([radius, 0])
                    circle(d=thickness);
    
    // Tip
    translate([2*radius, 0, length])
        rotate([-90, 0, 0])
            cylinder(h=thickness, d=thickness);
}

hook();
```

## Text and Labels

### Embossed Text
```openscad
module label(text_str, size, depth=1) {
    linear_extrude(height=depth)
        text(text_str, size=size, halign="center", valign="center");
}

difference() {
    cube([50, 20, 3], center=true);
    translate([0, 0, 3/2 - 0.5])
        label("LABEL", 8, 1);
}
```

### Raised Text
```openscad
union() {
    cube([50, 20, 2], center=true);
    translate([0, 0, 1])
        linear_extrude(height=1)
            text("TEXT", size=8, halign="center", valign="center");
}
```

### QR Code Placeholder
```openscad
module qr_placeholder(size, depth=1) {
    // Simplified QR-like pattern
    cell = size / 7;
    
    linear_extrude(height=depth)
        for (x = [0:6], y = [0:6])
            if ((x < 2 || x > 4 || y < 2 || y > 4) && 
                (rands(0, 1, 1, x*10+y)[0] > 0.5))
                translate([x * cell, y * cell])
                    square(cell * 0.9);
}
```

## Assembly Patterns

### Parametric Grid
```openscad
module grid(cols, rows, spacing) {
    for (x = [0:cols-1], y = [0:rows-1])
        translate([x * spacing, y * spacing, 0])
            children();
}

grid(3, 4, 15) cylinder(h=10, r=3);
```

### Circular Array
```openscad
module circular_array(count, radius) {
    for (i = [0:count-1])
        rotate([0, 0, i * 360/count])
            translate([radius, 0, 0])
                children();
}

circular_array(8, 20) cube([5, 5, 10], center=true);
```

### Mirror with Original
```openscad
module mirror_copy(v) {
    children();
    mirror(v) children();
}

mirror_copy([1, 0, 0])
    translate([10, 0, 0])
        sphere(5);
```
