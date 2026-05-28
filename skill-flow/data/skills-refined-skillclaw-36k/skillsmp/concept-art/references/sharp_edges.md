# Concept Art - Sharp Edges

## Jumping to Detail Too Early

### **Id**
premature-detail
### **Severity**
critical
### **Description**
  The #1 killer of good concept art. Artists spend 20 hours rendering a single
  idea that gets rejected in review. Feng Zhu calls this "polishing a turd."
  
  Detail is seductive - it feels like progress. But detail before design approval
  is wasted effort and limits creative exploration.
  
### **Symptoms**
  - First thumbnail is also final concept
  - Can't show alternatives because 'this one took so long'
  - Art director says 'this is beautiful but not what we need'
  - Rendering before silhouette is approved
### **Prevention**
  - Enforce thumbnail phase - no exceptions
  - Get written approval before Stage 3 (tight sketch)
  - Time-box exploration: if you can't do 20 thumbs in 2 hours, you're too detailed
  - Squint test: does it read at postage-stamp size?
### **Recovery**
  Stop immediately. Crop or trace the best elements into new thumbnails.
  The rendered work isn't wasted if you extract learnings. Show art director
  the piece as exploration, then present proper alternatives.
  

## Designing What Can't Be Built

### **Id**
unbuildable-concepts
### **Severity**
critical
### **Description**
  Beautiful paintings that cause production nightmares. The concept looks amazing
  but requires impossible geometry, breaks the game engine, or would take
  6 months to model something that appears for 2 seconds.
  
  Common in junior artists who haven't worked with 3D teams.
  
### **Symptoms**
  - 3D artist says 'how do I even build this?'
  - Floating elements with no structural logic
  - Intersecting geometry that can't exist
  - Materials that don't exist in the engine
  - Polycounts would crash the game
### **Prevention**
  - Include scale reference in EVERY concept
  - Sketch construction logic, not just appearance
  - Know your engine's material capabilities
  - Talk to 3D before finalizing (15-min check-in)
  - Ask: 'How would this be modeled?'
  - Include orthographics for anything approved
### **Recovery**
  Work with 3D artist to identify specific problems.
  Create revision concepts that solve structural issues
  while maintaining the visual intent. Document learnings.
  

## Colors That Die in Engine

### **Id**
engine-lighting-mismatch
### **Severity**
high
### **Description**
  Concept art painted in Photoshop rarely survives game engine lighting.
  That perfect painted sunset becomes a muddy mess under dynamic lighting.
  Emissive materials blow out. Highly saturated colors clash with PBR.
  
### **Symptoms**
  - In-engine screenshot looks nothing like concept
  - Environment artists constantly asking for 'the real colors'
  - Colors looked great in paint but terrible in Unity/Unreal
  - Subsurface scattering materials rendered flat
### **Prevention**
  - Paint in sRGB but understand linear color space
  - Test key colors in engine early
  - Work with lighting artists on color scripts
  - Provide base color AND lit color references
  - Include notes on expected lighting conditions
  - Create daylight AND dramatic lighting versions
### **Recovery**
  Create an engine-accurate version alongside painted version.
  Establish a color correction LUT between paint and engine.
  Adjust expectations with art director on what's achievable.
  

## Copying Reference Without Comprehension

### **Id**
reference-without-understanding
### **Severity**
high
### **Description**
  Using reference as a crutch rather than research. The artist copies surface
  details without understanding why they exist. Results look derivative,
  lack internal logic, and fall apart under scrutiny.
  
  Scott Robertson emphasizes understanding form before stylizing it.
  
### **Symptoms**
  - Can't explain why design elements exist
  - Mix of incompatible style languages
  - Falls apart when asked for alternate angle
  - Looks like collage of unrelated sources
  - Can't iterate without returning to reference
### **Prevention**
  - Ask 'WHY does this exist?' for every reference element
  - Understand function before copying form
  - Draw from imagination first, then refine with reference
  - Study underlying structure (anatomy, engineering, nature)
  - Synthesize 5+ references into something new
### **Recovery**
  Step back and study fundamentals. Draw the subject from multiple
  angles without reference. Understand the engineering/biology/physics.
  Then return to reference with informed eyes.
  

## Ignoring Silhouette Readability

### **Id**
no-silhouette-thinking
### **Severity**
high
### **Description**
  Designs that rely on internal detail to read. When reduced to silhouette
  (as they will be in-game, at distance, in motion), they become generic blobs.
  Critical for characters and props.
  
### **Symptoms**
  - All characters look same in silhouette
  - Can't identify character at 50% zoom
  - Relies on color to differentiate
  - Details invisible at game camera distance
### **Prevention**
  - Fill silhouette test BEFORE any detail
  - Design for thumbnail readability
  - Asymmetry creates interesting silhouettes
  - Test at intended in-game scale
  - Unique silhouette per character class
### **Recovery**
  Identify the silhouette's unique features.
  Exaggerate distinguishing elements.
  Remove details that don't contribute to silhouette.
  

## Concepting Without Production Awareness

### **Id**
scope-blindness
### **Severity**
high
### **Description**
  Creating concepts without understanding production constraints.
  The background character has more detail than the protagonist.
  The one-off prop gets hero treatment. Wastes production resources.
  
### **Symptoms**
  - Every asset gets same level of detail
  - Background elements more detailed than foreground
  - No tiering of asset importance
  - Producer asks 'why did this take so long?'
### **Prevention**
  - Know the asset tier: hero, secondary, tertiary
  - Match concept fidelity to production priority
  - Ask: how long will players see this?
  - Thumbnails for background, full render for hero
  - Communicate tier expectations with AD
### **Recovery**
  Create an asset tier document. Retroactively categorize concepts.
  Adjust expectations and potentially simplify over-detailed
  low-priority assets before they hit production.
  

## Presenting One Precious Idea

### **Id**
single-solution-syndrome
### **Severity**
medium
### **Description**
  Artist falls in love with one solution and presents only that.
  When rejected, they have nothing to show. Creates ego attachment
  and makes feedback feel personal.
  
### **Symptoms**
  - Only one concept in review
  - Defensive when receiving feedback
  - Argues for rejected design
  - Slow to pivot to alternatives
### **Prevention**
  - ALWAYS present 3-5 options minimum
  - Include one safe option you don't love
  - Include one wild option you don't expect to win
  - Present without advocacy - let work speak
  - Prepare for ANY option to win
### **Recovery**
  Develop emotional detachment from work.
  Generate alternatives rapidly after rejection.
  Reframe feedback as information, not judgment.
  

## Over-Reliance on Photo Reference

### **Id**
photobash-dependency
### **Severity**
medium
### **Description**
  Using photobashing as the entire process rather than a tool.
  Work looks like collage. Can't paint without photos. Falls apart
  when unique designs are needed.
  
### **Symptoms**
  - Every concept requires specific photo reference
  - Struggles with stylized or fantastical subjects
  - Seams visible between photo elements
  - Can't draw subject from alternate angle
### **Prevention**
  - Balance: 50% painted, 50% photo in exploration
  - Final should be 70%+ painted
  - Practice fundamentals without reference daily
  - Use photobash for speed, not as crutch
  - Transform all photos significantly
### **Recovery**
  Set aside dedicated practice time for fundamentals.
  Challenge yourself with subjects that have no photo reference.
  Gradually reduce photo percentage in work.
  

## Rendering Without Design

### **Id**
lost-in-rendering
### **Severity**
medium
### **Description**
  Spending hours on rendering technique while design is weak.
  The shiny surface hides empty content. Common when learning
  new software or techniques.
  
### **Symptoms**
  - Impressive technique, boring design
  - All concepts look technically similar
  - Focuses on materials over silhouette
  - Can talk about brushes but not design choices
### **Prevention**
  - Design approval before rendering begins
  - Value sketch must work before color
  - Ask: 'Is this a good design or just good painting?'
  - Separate design phase from rendering phase
### **Recovery**
  Return to thumbnails. Practice design without rendering.
  Study graphic designers and their shape thinking.
  Render only what has already been approved.
  

## Impossible Lighting Logic

### **Id**
inconsistent-lighting
### **Severity**
medium
### **Description**
  Multiple light sources that contradict each other. Shadows going
  different directions. Looks painted rather than lit.
  Destroys believability.
  
### **Symptoms**
  - Shadows point in multiple directions
  - Highlights inconsistent with shadows
  - Can't identify light source location
  - Different elements lit from different angles
### **Prevention**
  - Establish key light direction FIRST
  - Use simple 3D sphere to test lighting
  - Draw through forms to understand shadow shapes
  - Study James Gurney's 'Color and Light'
### **Recovery**
  Identify your intended key light. Repaint all shadows
  consistently from that direction. Add fill and bounce
  logically. Use grayscale layer to check values.
  

## Empty Environments Without Narrative

### **Id**
no-story-in-environment
### **Severity**
medium
### **Description**
  Environments that are technically correct but emotionally empty.
  No signs of life, history, or story. Just architecture.
  Sparth emphasizes that every environment tells a story.
  
### **Symptoms**
  - Environments feel like 3D renders, not lived spaces
  - No wear, weathering, or history
  - Can't answer 'who lives here?'
  - Prop placement is arbitrary
### **Prevention**
  - Write a one-paragraph story for every environment
  - Add signs of inhabitants (past or present)
  - Include environmental storytelling beats
  - Weather and wear appropriate to history
  - Every prop should have a reason
### **Recovery**
  Write the space's history. Identify 3 story beats.
  Add specific details that reveal character.
  Include one unexpected element that raises questions.
  

## No Scale Reference in Deliverables

### **Id**
ignoring-scale
### **Severity**
low
### **Description**
  Concepts without human scale reference cause constant questions
  in production. "How big is this?" becomes a recurring Slack message.
  
### **Symptoms**
  - 3D artists asking about scale
  - Assets built at wrong size
  - Environments feel wrong when populated
  - Props don't fit hands/spaces
### **Prevention**
  - Human silhouette in EVERY environment concept
  - Hand reference in EVERY prop concept
  - Include measurement callouts
  - Standard reference objects (door, chair, car)
### **Recovery**
  Add scale reference retroactively.
  Establish scale standards document.
  Create template with built-in scale figures.
  

## Drifting From Established Style Guide

### **Id**
style-guide-drift
### **Severity**
low
### **Description**
  Later concepts don't match the visual language established early
  in the project. Creates inconsistency across the game.
  
### **Symptoms**
  - New concepts feel from different game
  - Art director catches style violations in review
  - Different concept artists have different interpretations
  - Props from different artists don't match
### **Prevention**
  - Reference visual bible before every concept
  - Regular style alignment meetings
  - Create style test: does this fit next to X?
  - Update bible when style evolves (with approval)
### **Recovery**
  Review all recent concepts against bible.
  Identify and document drift. Either revise
  concepts or update bible (with AD approval).
  