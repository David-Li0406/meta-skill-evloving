# Level Design - Validations

## Level Metrics Document Exists

### **Id**
blockout-metrics-defined
### **Severity**
critical
### **Type**
checklist
### **Items**
  - Character height documented
  - Jump height and distance documented
  - Walk and run speeds documented
  - Corridor minimum widths defined
  - Door dimensions defined
  - Comfortable vs challenging jump gaps defined
  - Combat engagement ranges defined
### **Message**
Level metrics must be documented before blocking out. Derive all values from character controller.
### **Fix Action**
Create a metrics document from character controller values before any blockout work.
### **Applies To**
  - level-design
  - blockout

## Blockout Playtested Before Art Pass

### **Id**
blockout-before-art
### **Severity**
critical
### **Type**
checklist
### **Items**
  - Level playable with placeholder art
  - Minimum 3 external playtests completed
  - Core gameplay loop validated
  - Major layout issues addressed
  - Combat encounters timed and tuned
  - Pacing reviewed and adjusted
  - Geometry locked for art pass
### **Message**
Never begin art pass before blockout is proven fun through playtesting.
### **Fix Action**
Complete blockout iteration with playtests before any final art investment.
### **Applies To**
  - level-design
  - production

## Critical Path Clearly Readable

### **Id**
golden-path-clarity
### **Severity**
critical
### **Type**
checklist
### **Items**
  - Main path distinguishable from optional paths
  - Next objective visible or clearly signposted
  - Lighting guides toward objectives
  - No required backtracking through cleared areas
  - Fresh playtesters find path within 30 seconds of entering new area
### **Message**
Players should never be lost on the critical path. Test with fresh eyes.
### **Fix Action**
Apply breadcrumbing techniques: lighting, composition, environmental hints.
### **Applies To**
  - level-design
  - player-flow

## Navigation Landmarks Present

### **Id**
orientation-landmarks
### **Severity**
high
### **Type**
checklist
### **Items**
  - Global landmark visible from 70%+ of map (for open/hub areas)
  - Each area has distinctive visual identity
  - Local landmarks provide sub-area orientation
  - Players can describe their location verbally
  - No identical-looking corridors or rooms
### **Message**
Players must always know where they are and how to get where they're going.
### **Fix Action**
Add distinctive landmarks, color coding, or architectural variation.
### **Applies To**
  - level-design
  - open-world
  - hub-areas

## All Dead Ends Have Purpose

### **Id**
dead-end-rewards
### **Severity**
warning
### **Type**
checklist
### **Items**
  - Every non-main path leads to a reward, lore, or vista
  - Dead ends are short (sub-30 seconds to traverse)
  - Player can recognize dead end before full commitment
  - Optional paths clearly read as optional
### **Message**
Dead ends without rewards punish exploration and erode player trust.
### **Fix Action**
Add pickup, lore item, vista, or shortcut unlock. Or remove the path entirely.
### **Applies To**
  - level-design
  - exploration

## Intensity Variation in Level

### **Id**
push-pull-rhythm
### **Severity**
high
### **Type**
checklist
### **Items**
  - Level has identifiable high-intensity sections
  - Level has breathing room between intense moments
  - No more than 2 combat encounters back-to-back without breather
  - Safe spaces exist for resource management
  - Pacing graph shows variation, not flat line
### **Message**
Unrelenting intensity causes fatigue. Constant calm causes boredom.
### **Fix Action**
Add breathing rooms after intense sequences. Vary encounter density.
### **Applies To**
  - level-design
  - pacing

## Level Has Clear Structure

### **Id**
three-beat-structure
### **Severity**
warning
### **Type**
checklist
### **Items**
  - Setup phase introduces space and rules
  - Confrontation phase escalates challenge
  - Resolution phase provides climax and payoff
  - Each phase has distinct feel
  - Transitions between phases are clear
### **Message**
Well-structured levels are more memorable and satisfying.
### **Fix Action**
Map level to three-beat structure. Identify and strengthen phase transitions.
### **Applies To**
  - level-design
  - linear
  - mission

## Combat Arenas Properly Designed

### **Id**
combat-arena-design
### **Severity**
high
### **Type**
checklist
### **Items**
  - Cover elements distributed throughout arena
  - No invincible camping positions
  - Entry gives player overview before engagement
  - Exit clearly different from entry
  - Arena size matches enemy count and type
  - Vertical elements if ranged combat expected
  - Post-combat reward present (loot, vista, story)
### **Message**
Combat arenas need intentional design for tactical depth and flow.
### **Fix Action**
Review arena against cover, flow, and sight line requirements.
### **Applies To**
  - level-design
  - combat
  - arena

## Combat Encounters Properly Escalated

### **Id**
encounter-escalation
### **Severity**
warning
### **Type**
checklist
### **Items**
  - First encounter in level is easiest
  - New enemies introduced in controlled setting first
  - Enemy combinations build on player knowledge
  - No difficulty cliffs without warning
  - Final encounter is climax, not afterthought
### **Message**
Encounter design should teach then test, building throughout level.
### **Fix Action**
Map encounter difficulty curve. Ensure steady escalation with new elements isolated first.
### **Applies To**
  - level-design
  - combat
  - encounter-design

## Spawn Points Are Safe

### **Id**
multiplayer-spawn-safety
### **Severity**
critical
### **Type**
checklist
### **Items**
  - No enemy sightlines to spawn points
  - Each spawn has 3+ exit routes
  - Immediate cover available at spawn
  - No spawn point within grenade range of common positions
  - Spawn camping tested and mitigated
### **Message**
Spawn deaths destroy the multiplayer experience. Design spawns to be safe.
### **Fix Action**
Block sightlines to spawns. Add cover and multiple exits. Test with skilled players.
### **Applies To**
  - level-design
  - multiplayer
  - spawn-design

## Multiplayer Map Fairly Balanced

### **Id**
multiplayer-map-balance
### **Severity**
critical
### **Type**
checklist
### **Items**
  - Both teams have equal access to power positions
  - Objective routes balanced in distance and cover
  - Power weapons/pickups equidistant from spawns
  - High ground positions contestable from multiple angles
  - No side has inherent advantage
  - Map tested with team swaps showing similar results
### **Message**
Unfair maps aren't fun for either team.
### **Fix Action**
Audit distances, sightlines, and advantages for each team. Playtest with team swaps.
### **Applies To**
  - level-design
  - multiplayer
  - competitive

## Map Locations Are Communicable

### **Id**
multiplayer-callout-clarity
### **Severity**
warning
### **Type**
checklist
### **Items**
  - Each area has distinctive visual identity
  - Areas can be given clear, memorable names
  - No two areas look identical
  - Compass directions work (clear north/south/east/west)
  - Callouts tested with new players
### **Message**
Team communication requires unique, identifiable locations.
### **Fix Action**
Add visual distinction to similar areas. Test callout clarity with new players.
### **Applies To**
  - level-design
  - multiplayer
  - team-based

## New Mechanics Properly Introduced

### **Id**
mechanic-introduction
### **Severity**
high
### **Type**
checklist
### **Items**
  - New mechanic introduced in isolation
  - First use has low/no failure penalty
  - Player can observe solution before attempting
  - Complexity added after base mechanic understood
  - No tutorial text unless absolutely necessary
### **Message**
Teach through design, not text. Safe spaces to learn before stakes.
### **Fix Action**
Apply Nintendo teaching method: safe introduction, guided challenge, twist, mastery test.
### **Applies To**
  - level-design
  - tutorial
  - onboarding

## No Soft Lock Conditions

### **Id**
no-softlocks
### **Severity**
critical
### **Type**
checklist
### **Items**
  - Every one-way transition audited
  - Required items obtainable after any one-way
  - Pits have escape routes or quick death
  - Consumable soft locks impossible
  - Sequence breaks don't break story
### **Message**
Soft locks waste player time and break trust. Never ship one.
### **Fix Action**
Audit every one-way transition. Add escape routes or move required items.
### **Applies To**
  - level-design
  - progression
  - qa

## Jump Gaps Match Controller Metrics

### **Id**
jump-gap-consistency
### **Severity**
critical
### **Type**
checklist
### **Items**
  - All gaps tested against documented jump distance
  - Comfortable gaps at 80% of max jump
  - Challenging gaps at 95% of max jump
  - No gaps exceed 100% of max jump on critical path
  - Coyote time and jump buffer accounted for
  - All gaps tested at lowest supported framerate
### **Message**
Jumps that don't match controller feel unfair and frustrating.
### **Fix Action**
Measure all gaps against character controller. Adjust geometry to match metrics.
### **Applies To**
  - level-design
  - platforming
  - metrics

## Combat Corridors Wide Enough

### **Id**
corridor-combat-width
### **Severity**
high
### **Type**
checklist
### **Items**
  - Combat corridors at minimum 4x character width
  - Dodge/roll space available in combat zones
  - Cover positions accessible without getting stuck
  - Multiple players can pass (if multiplayer)
  - AI can navigate without clustering
### **Message**
Narrow combat spaces feel cramped and frustrating.
### **Fix Action**
Widen combat areas to at least 4x character width. Test with combat playthrough.
### **Applies To**
  - level-design
  - combat
  - metrics

## Visual Hierarchy Guides Player

### **Id**
visual-path-hierarchy
### **Severity**
warning
### **Type**
checklist
### **Items**
  - Critical paths are brightest or most saturated
  - Interactive elements have consistent visual language
  - Doors readable as doors
  - Composition leads eye to objectives
  - Blur test: direction clear when screenshot blurred
### **Message**
Players should know where to go without UI markers.
### **Fix Action**
Apply lighting, color, and composition to guide attention.
### **Applies To**
  - level-design
  - polish
  - art-pass

## Level Within Performance Budget

### **Id**
performance-budget
### **Severity**
critical
### **Type**
checklist
### **Items**
  - Draw calls within target
  - Poly count within budget
  - Occlusion culling functioning
  - LODs implemented for distant objects
  - Lightmaps within memory budget
  - Tested on minimum spec hardware
### **Message**
Beautiful levels that don't run are useless.
### **Fix Action**
Profile and optimize. Cut detail in non-focal areas.
### **Applies To**
  - level-design
  - optimization
  - production

## Content Density Balanced

### **Id**
open-world-density
### **Severity**
warning
### **Type**
checklist
### **Items**
  - Points of interest distributed evenly
  - No large empty zones without purpose
  - High-traffic routes have most content
  - Optional areas less dense but rewarding
  - Map icons not overwhelming
  - Discovery balanced with marking
### **Message**
Open worlds need intentional content distribution.
### **Fix Action**
Map content density. Fill dead zones or make emptiness intentional.
### **Applies To**
  - level-design
  - open-world

## Fast Travel System Supports Exploration

### **Id**
open-world-fast-travel
### **Severity**
warning
### **Type**
checklist
### **Items**
  - Fast travel points discovered through play
  - Manual exploration still rewarded
  - Fast travel doesn't skip critical content
  - Fast travel available after initial exploration
  - Destination preview shows what's there
### **Message**
Fast travel should enhance exploration, not replace it.
### **Fix Action**
Gate fast travel behind discovery. Ensure content between points is worth walking.
### **Applies To**
  - level-design
  - open-world
  - traversal