# Video Directing - Validations

## Shot List Coverage Check

### **Id**
shot-list-completeness
### **Description**
Validates that shot list includes essential coverage types
### **Check Type**
content
### **Severity**
warning
### **Pattern**
  Shot list should include:
  - Establishing/wide shots
  - Master shots for each scene
  - Singles/close-ups on key subjects
  - Reaction shots
  - Insert/detail shots
  - Entry and exit coverage
  
### **Fix**
  Add missing coverage types to shot list:
  □ WIDE: Establishing shot showing full location
  □ MASTER: Full scene coverage in continuous shot
  □ SINGLES: Individual character shots
  □ CU: Close-ups for emotional beats
  □ INSERTS: Detail shots (hands, objects)
  □ REACTIONS: Cutaway faces for editing flexibility
  

## Emotional Intent Declaration

### **Id**
emotional-intent-defined
### **Description**
Each scene should have clearly defined emotional intent
### **Check Type**
content
### **Severity**
warning
### **Pattern**
  Scene/sequence descriptions should include:
  - What emotion the audience should feel
  - What the character wants in the scene
  - The emotional arc (where it starts/ends)
  
### **Fix**
  Add emotional context to scene planning:
  "SCENE: [description]
  EMOTION: Audience should feel [specific emotion]
  CHARACTER WANT: [character] wants to [specific goal]
  ARC: Starts [emotion A], ends [emotion B]"
  

## Eyeline Direction Check

### **Id**
eyeline-specification
### **Description**
Dialogue scenes should specify eyeline directions
### **Check Type**
content
### **Severity**
warning
### **Pattern**
  Dialogue coverage should specify:
  - Character A eyeline direction (left/right, up/down)
  - Character B eyeline direction (opposite of A)
  - Any POV shots match character heights
  
### **Fix**
  For each character in dialogue:
  - A looks: screen-[direction] at [height]
  - B looks: screen-[opposite direction] at [height]
  Example: "A looks screen-right, eye level. B looks screen-left, slight up."
  

## Lighting Specification Check

### **Id**
lighting-consistency-spec
### **Description**
Multi-shot sequences should specify consistent lighting
### **Check Type**
content
### **Severity**
error
### **Pattern**
  For AI generation prompts in a sequence:
  - Light direction (key light from left/right/above)
  - Color temperature (warm/cool/neutral, or Kelvin)
  - Time of day (dawn, golden hour, midday, dusk, night)
  - Lighting style reference (cinematographer name or film)
  
### **Fix**
  Add to every prompt in a sequence:
  "[shot description], key light from [direction],
  [color temperature] lighting, [time of day],
  [reference cinematographer/film] style"
  

## Camera Movement Motivation Check

### **Id**
camera-movement-motivation
### **Description**
Moving camera shots should have stated purpose
### **Check Type**
content
### **Severity**
info
### **Pattern**
  Camera movement specifications should include:
  - What type of move (track, dolly, crane, steadicam, handheld)
  - Why this movement (reveal, follow, intensify, disorient)
  - What it expresses about the scene/character
  
### **Fix**
  For each moving shot:
  "MOVE: [type] - [direction]
  PURPOSE: To [reveal/follow/intensify/express]
  EXPRESSES: [what this communicates emotionally]"
  

## AI Prompt Cinematography Elements

### **Id**
ai-prompt-cinematography
### **Description**
AI video prompts should include cinematographic specifications
### **Check Type**
content
### **Severity**
warning
### **Pattern**
  AI video prompts should specify:
  - Lens/focal length feel (wide, normal, telephoto)
  - Shot size (extreme CU, CU, MCU, MS, MLS, LS, ELS)
  - Camera angle (eye level, low angle, high angle, Dutch)
  - Film stock/format reference (35mm, IMAX, anamorphic)
  
### **Fix**
  AI Prompt Template:
  "[Shot size] of [subject] [action],
  [lens feel e.g., 85mm portrait, 24mm wide],
  [angle e.g., low angle looking up],
  shot on [format e.g., 35mm anamorphic, ARRI Alexa],
  [lighting], cinematic, shallow depth of field"
  

## Sequence Rhythm Planning

### **Id**
sequence-rhythm-plan
### **Description**
Sequences should have defined pacing rhythm
### **Check Type**
content
### **Severity**
info
### **Pattern**
  Action/montage sequences should specify:
  - Overall tempo (frenetic, measured, building, declining)
  - Shot length pattern (long-short alternation, accelerating cuts)
  - Music/beat alignment points
  
### **Fix**
  Add rhythm plan to sequences:
  "RHYTHM: [overall tempo]
  PATTERN: [e.g., 4s-2s-1s-1s accelerating to climax]
  BEATS: Music hits at [moments], cut on [beats]
  BREATHERS: Pause at [moments] to let emotion land"
  

## Edit Flexibility Coverage

### **Id**
coverage-for-edit
### **Description**
Coverage plan should include edit flexibility shots
### **Check Type**
content
### **Severity**
warning
### **Pattern**
  Coverage should include "escape" shots:
  - Neutral angles for any cut point
  - Reaction shots without dialogue
  - Insert cutaways
  - Environmental/atmosphere shots
  
### **Fix**
  Add to every scene's shot list:
  "EDIT FLEXIBILITY:
  □ Neutral wide (can cut to from any shot)
  □ Listening reactions (no dialogue, just face)
  □ Hands/objects (cover any moment)
  □ Environment (buy time, establish rhythm)"
  

## Performance Direction Specificity

### **Id**
actor-direction-specificity
### **Description**
Performer direction should be specific and playable
### **Check Type**
content
### **Severity**
info
### **Pattern**
  Direction should avoid:
  - Vague emotions ("be sad", "look happy")
  - Result-oriented direction ("be more compelling")
  Direction should include:
  - Playable actions ("try to make them laugh")
  - Specific intentions ("hide that you know")
  
### **Fix**
  Convert vague direction to specific:
  VAGUE: "Look nervous"
  SPECIFIC: "You know something's wrong but you're trying not to let them see it. Every time they look at you, look away casually."
  
  VAGUE: "Be angry"
  SPECIFIC: "You're not showing the anger—you're controlling it. The calmer you seem, the more dangerous you are."
  

## Story-First Spectacle Check

### **Id**
story-serves-spectacle
### **Description**
Spectacle/effect shots should serve story purpose
### **Check Type**
content
### **Severity**
warning
### **Pattern**
  Visual spectacle moments should be justified by:
  - Emotional story purpose
  - Character revelation
  - Narrative payoff
  Not just: "It would look cool"
  
### **Fix**
  For each major visual moment, document:
  "SPECTACLE: [description]
  STORY PURPOSE: This reveals/advances [what]
  EMOTIONAL GOAL: Audience should feel [emotion]
  EARNED BY: Setup in [previous scene/moment]"
  

## Audio Integration Planning

### **Id**
audio-integration-plan
### **Description**
Visual plans should include audio considerations
### **Check Type**
content
### **Severity**
warning
### **Pattern**
  Scene planning should include:
  - Music placement (where it starts/stops/shifts)
  - Sound design notes (ambient, effects, silence)
  - Dialogue priority (clean recording needs)
  
### **Fix**
  Add audio layer to scene planning:
  "AUDIO:
  - Music: [starts at/ends at/shifts at]
  - Ambient: [environmental sound]
  - Effects: [specific sound design needs]
  - Silence: [deliberate quiet moments]
  - Dialogue: [recording priority areas]"
  

## Axis/Line Awareness Check

### **Id**
180-rule-awareness
### **Description**
Coverage plans should identify and maintain spatial axis
### **Check Type**
content
### **Severity**
error
### **Pattern**
  Dialogue/action scenes should specify:
  - The line (axis between subjects)
  - Which side camera stays on
  - Any planned line crosses (with technique)
  
### **Fix**
  Add to dialogue scene planning:
  "AXIS: Line between [A] and [B]
  CAMERA SIDE: All coverage from [left/right] side
  LINE CROSS: [None / At [moment] via [technique]]
  
  If crossing: Use neutral shot, dolly through, or character movement to justify"
  