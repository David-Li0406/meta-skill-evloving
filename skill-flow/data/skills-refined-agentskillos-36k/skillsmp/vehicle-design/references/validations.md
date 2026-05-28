# Vehicle Design - Validations

## Vehicle Proportion Check

### **Id**
proportion-verification
### **Severity**
critical
### **Type**
checklist
### **Description**
  Verify all fundamental proportions before proceeding to detail work.
  Bad proportions cannot be fixed with detail - they must be caught early.
  
### **When**
Before any surface detail work begins
### **Checklist**
  - Wheel diameter is correct for vehicle type (35-45% of body height for sports)
  - Wheelbase ratio matches archetype (55-65% of total length)
  - Ground clearance is intentional and appropriate
  - Cabin/glasshouse proportions feel balanced
  - Front and rear overhangs are intentional
  - Vehicle compared to real reference at same scale
  - Proportions reviewed from front, side, rear, and 3/4 views
### **Fix Action**
Revise basic volumes and proportions before proceeding
### **Approval Gate**


## Silhouette Readability Test

### **Id**
silhouette-test
### **Severity**
critical
### **Type**
checklist
### **Description**
  Verify the vehicle reads clearly at small sizes and distances.
  The silhouette should communicate vehicle type without any detail.
  
### **When**
After basic form is established
### **Checklist**
  - Vehicle type is identifiable at 100 pixel width
  - Silhouette is distinct from other vehicles in the project
  - Key features (spoiler, cab, turret) read in silhouette
  - Squint test passed - major masses are clear
  - Silhouette works from all major viewing angles
  - Day/night silhouette readability considered
### **Fix Action**
Strengthen silhouette by exaggerating key proportions and features
### **Approval Gate**


## Vehicle Stance Assessment

### **Id**
stance-evaluation
### **Severity**
high
### **Type**
checklist
### **Description**
  Verify the vehicle's stance communicates intended character.
  Stance is how the vehicle "sits" - its attitude and personality.
  
### **When**
After proportions are approved
### **Checklist**
  - Stance archetype is defined (aggressive, planted, nimble, heavy)
  - Wheel position creates intended character
  - Ride height matches vehicle purpose
  - Track width feels appropriate
  - Vehicle appears grounded, not floating
  - Suspension state looks loaded (not topped out)
  - Tire contact patch deformation considered
### **Fix Action**
Adjust wheel position, ride height, and rake to match intended character

## Wheel and Tire Design Verification

### **Id**
wheel-design-audit
### **Severity**
high
### **Type**
checklist
### **Description**
  Verify wheels are correctly sized, styled, and detailed.
  Wheels are 30-40% of what makes a vehicle design work.
  
### **When**
When wheel design is completed
### **Checklist**
  - Wheel diameter is correct for vehicle archetype
  - Tire sidewall ratio matches vehicle type (low for sports, high for off-road)
  - Spoke design matches vehicle character
  - Brake visibility appropriate for performance level
  - Wheel width proportional to body
  - Wheel offset creates correct stance (not too tucked or poked)
  - Tread pattern visible if close-up views expected
### **Fix Action**
Redesign wheels to match vehicle character and archetype

## Functional Element Verification

### **Id**
functional-aesthetic-check
### **Severity**
high
### **Type**
checklist
### **Description**
  Verify all surface details have functional justification.
  Every vent, intake, and panel line should have a reason to exist.
  
### **When**
After surface detailing
### **Checklist**
  - Every intake has implied airflow destination
  - Every vent has implied heat/exhaust source
  - Panel lines correspond to assembly, access, or style
  - Aerodynamic elements are placed logically
  - Can explain the purpose of each major surface feature
  - No arbitrary 'greeble' without function
  - Functional elements are appropriately sized
### **Fix Action**
Remove arbitrary details, add functional justification to retained elements

## Steering Geometry Verification

### **Id**
steering-clearance-check
### **Severity**
critical
### **Type**
checklist
### **Description**
  Verify wheel wells accommodate steering articulation.
  Front wheels must be able to turn to full lock without clipping.
  
### **When**
Before finalizing front end design
### **Checklist**
  - Maximum steering angle defined for vehicle type
  - Wheel position at full lock modeled/sketched
  - Wheel arch clears wheel at all steering angles
  - Inner fender clears wheel at full compression + lock
  - No tire-to-body contact at any combination
  - Clearance margin documented for modelers
### **Fix Action**
Adjust wheel arch shape to accommodate steering geometry
### **Applies To**
  - ground_vehicles
  - wheeled_military

## Scale Reference Inclusion

### **Id**
scale-reference-verification
### **Severity**
high
### **Type**
checklist
### **Description**
  Verify human scale reference is included in design documentation.
  Without scale reference, 3D modelers cannot size the vehicle correctly.
  
### **When**
Before concept approval
### **Checklist**
  - Human figure included in at least one concept view
  - Door/entry height indicates human access
  - Cockpit/cabin sized for intended occupants
  - Dimensions noted in meters or feet
  - Window proportions suggest human scale
  - Compared to known vehicles for reference
### **Fix Action**
Add human silhouettes and dimension callouts to concept

## Damage State Documentation

### **Id**
damage-state-planning
### **Severity**
medium
### **Type**
checklist
### **Description**
  Verify damage progression is planned from the initial design.
  Panel breaks, structure reveal, and destruction sequence defined.
  
### **When**
Before concept approval for action game vehicles
### **Checklist**
  - Panel break locations defined
  - Detachable vs deformable panels identified
  - Internal structure designed (visible when damaged)
  - At least 3 damage states sketched
  - Destruction sequence is logical (front-to-rear for crashes)
  - Silhouette remains recognizable when heavily damaged
  - Fire/explosion effect placement noted
### **Fix Action**
Add damage state concepts and panel break documentation
### **Applies To**
  - combat_vehicles
  - racing_vehicles
  - any_destructible

## Interior/Cockpit Design Verification

### **Id**
cockpit-interior-check
### **Severity**
medium
### **Type**
checklist
### **Description**
  Verify interior design matches exterior character and era.
  Interior technology level and style must be consistent.
  
### **When**
When interior concepts are completed
### **Checklist**
  - Technology level matches exterior era
  - Material quality matches exterior tier (economy vs luxury)
  - Instrument style matches vehicle purpose
  - Controls are appropriate for vehicle function
  - Driver/pilot visibility is adequate
  - Seating position makes sense for vehicle type
  - HUD integration zones defined (for game UI)
### **Fix Action**
Redesign interior to match exterior character and technology level
### **Applies To**
  - player_vehicles
  - cockpit_view_vehicles

## Customization Compatibility Check

### **Id**
customization-readiness
### **Severity**
medium
### **Type**
checklist
### **Description**
  Verify base design accommodates player customization.
  Body panels, mounting points, and wheel wells must support mods.
  
### **When**
Before approval for customizable vehicles
### **Checklist**
  - Body panels have livery-friendly surfaces
  - Spoiler/wing mounting points defined
  - Bumper/fascia can be swapped
  - Wheel wells have clearance for larger wheels
  - Widebody extension zones identified
  - Interior visible through windows (for interior mods)
  - Graphics zones documented for wrap designers
### **Fix Action**
Modify surfaces and add mounting zone documentation
### **Applies To**
  - racing_game_vehicles
  - customizable_vehicles

## Sci-Fi Propulsion Logic Verification

### **Id**
sci-fi-plausibility-check
### **Severity**
high
### **Type**
checklist
### **Description**
  Verify fictional vehicles have internal logic for propulsion and function.
  Even fantasy technology should have visible, logical placement.
  
### **When**
Designing spacecraft, hover vehicles, or mechs
### **Checklist**
  - Main propulsion is visible and logically placed
  - Maneuvering thrusters are in paired positions
  - Power source/fuel is implied (volume allocation)
  - Exhaust/emissions have outlet paths
  - Weapons have clear firing arcs without self-damage
  - Crew access is human-scaled and reachable
  - Designer can explain 'how it works'
### **Fix Action**
Add visible propulsion elements and rationalize layout
### **Applies To**
  - spacecraft
  - hover_vehicles
  - mechs
  - futuristic_vehicles

## Form Language Consistency Check

### **Id**
form-language-consistency
### **Severity**
medium
### **Type**
checklist
### **Description**
  Verify consistent visual vocabulary within vehicle and across fleet.
  Edge character, surface treatment, and graphic elements should match.
  
### **When**
Before fleet/faction vehicle approval
### **Checklist**
  - Edge character is consistent (all sharp, all soft, or documented mix)
  - Surface tension is consistent
  - Graphic elements repeat from manufacturer guide
  - Proportion ratios follow manufacturer rules
  - Vehicle is recognizable as part of faction/brand
  - Silhouette-tested alongside fleet siblings
### **Fix Action**
Revise elements that break form language rules
### **Applies To**
  - faction_vehicles
  - manufacturer_lineups