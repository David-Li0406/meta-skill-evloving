/**
 * Prompt Engine
 * 
 * Constructs prompts for the AI Writer using system prompt + context injection + task pattern.
 * Supports dialogue and exploration templates based on narrative context.
 * 
 * @module prompt-engine
 * @see docs/dev/m2-design/writer-prompts.md
 */
(function() {
"use strict";

/**
 * System prompt providing role, constraints, and output format
 * @const {string}
 */
const SYSTEM_PROMPT = `You are a creative narrative writer for a fantasy RPG. Your role is to generate story branches—short narrative sequences that branch from the main story, then return coherently to the scripted path.

## Your Constraints
- Generate dialogue and narrative that feels native to the game world
- Respect established character voices and personality traits
- Maintain thematic consistency with the current story arc
- Ensure the branch can logically return to the scripted content
- Do NOT introduce contradictions with established lore
- Do NOT violate player character's established alignment/values
- Do NOT introduce game-breaking mechanics or power spikes
- Keep content family-friendly and appropriate

## Output Format
Return a valid JSON object with exactly this structure:
{
  "choice_text": "Brief text for the choice button (5-15 words)",
  "content": {
    "branch_type": "narrative_delta",
    "text": "The narrative content to display (2-4 paragraphs)",
    "return_path": "knot_name"
  },
  "metadata": {
    "confidence_score": 0.0 to 1.0,
    "thematic_fit": 0.0 to 1.0
  }
}

Important: 
- The "return_path" must be one of the valid return knots provided
- Keep "text" content concise (100-200 words max)
- The "choice_text" should be enticing but not misleading`;

/**
 * Template for dialogue-focused branches
 * Used when branching around NPC interactions
 */
const DIALOGUE_TEMPLATE = `## Character Context
**Wanderer**: A traveler seeking to signal companions on the ridge
**Traits**: {courage_trait}, {caution_trait}
**Recent Inventory**: {inventory}

## Situation
**Location**: {scene_name}
**Current Mood**: {tone}
**What Just Happened**: {recent_context}

## Narrative Context
**Themes**: discovery, survival, companionship
**Key Established Facts**:
- The wanderer is trying to signal companions using smoke/fire
- A stranger in the forest may have useful information
- Wolves have been spotted in the area
{additional_context}

## Task
Generate a dialogue branch where the wanderer has a meaningful interaction.
The branch should:
- Explore the current situation through conversation or observation
- Provide atmosphere and character development
- Resolve within 30-60 seconds of reading
- Return to one of these knots: {valid_return_paths}

## Style Requirements
- Dialogue tone: Sincere, atmospheric
- Keep it brief but evocative
- Violence: AVOIDED`;

/**
 * Template for exploration/discovery branches
 * Used when branching around environmental discoveries
 */
const EXPLORATION_TEMPLATE = `## Player Context
**Character**: A wanderer exploring the forest ridge
**Traits**: {courage_trait}, {caution_trait}
**Current Items**: {inventory}

## Location Context
**Current Location**: {scene_name}
**Environment**: Forest ridge with pines, mist, and distant watchtower
**Mood**: {tone}

## What Triggered This Branch
**Current Situation**: {recent_context}
**Possible Discoveries**: hidden paths, old artifacts, natural phenomena

## Narrative Requirements
**Themes**: discovery, survival, mystery
**Established World Facts**:
- The forest holds secrets and old paths
- Rangers and travelers use smoke signals
- An abandoned watchtower stands to the east
{additional_context}

## Task
Generate an exploration branch where the wanderer discovers something interesting.
The branch should:
- Reward player curiosity and exploration
- Reveal something atmospheric or mysterious
- Resolve within 30-60 seconds of reading
- Return to one of these knots: {valid_return_paths}

## Style Requirements
- Tone: Mysterious, evocative
- Pacing: Moderate
- Keep descriptions vivid but concise`;

/**
 * Formats a courage/caution trait description
 * 
 * @param {number} courage - Courage score
 * @param {number} caution - Caution score
 * @returns {{courage_trait: string, caution_trait: string}} Trait descriptions
 */
function formatTraits(courage, caution) {
  let courage_trait = 'balanced';
  let caution_trait = 'balanced';
  
  if (courage > caution + 1) {
    courage_trait = 'bold and adventurous';
    caution_trait = 'sometimes reckless';
  } else if (caution > courage + 1) {
    courage_trait = 'careful and methodical';
    caution_trait = 'cautious to a fault';
  } else if (courage > 2) {
    courage_trait = 'courageous';
  } else if (caution > 2) {
    caution_trait = 'prudent';
  }
  
  return { courage_trait, caution_trait };
}

/**
 * Formats inventory items into a readable list
 * 
 * @param {string[]} items - Array of inventory items
 * @returns {string} Formatted inventory string
 */
function formatInventory(items) {
  if (!items || items.length === 0) {
    return 'nothing notable';
  }
  return items.join(', ');
}

/**
 * Formats recent choices into context string
 * 
 * @param {string[]} choices - Array of recent choice texts
 * @returns {string} Formatted context string
 */
function formatRecentContext(choices) {
  if (!choices || choices.length === 0) {
    return 'The wanderer has just arrived at this location.';
  }
  
  const lastChoice = choices[choices.length - 1];
  if (choices.length === 1) {
    return `The wanderer chose to: "${lastChoice}"`;
  }
  
  return `Recent actions: ${choices.slice(-3).map(c => `"${c}"`).join(', ')}`;
}

/**
 * Generates additional context based on story state
 * 
 * @param {Object} lore - LORE context object
 * @returns {string} Additional context bullet points
 */
function generateAdditionalContext(lore) {
  const lines = [];
  const variables = lore.player_state?.variables || {};
  
  if (lore.game_state?.wolves_spotted) {
    lines.push('- Wolves have been spotted nearby—tension is high');
  }
  
  if (lore.game_state?.met_stranger) {
    lines.push('- The wanderer has met a helpful stranger in the forest');
  }
  
  if (variables.found_artifact) {
    lines.push('- A mysterious artifact has been discovered');
  }
  
  if (variables.campfire_log) {
    lines.push('- The wanderer has fire-making supplies');
  }
  
  return lines.join('\n');
}

/**
 * Scene name mapping for better prompt context
 */
const SCENE_NAMES = {
  'start': 'the camp on the ridge',
  'pines': 'deep in the pine forest',
  'trail': 'a faint forest trail',
  'campfire': 'by the campfire',
  'stranger_dialogue': 'meeting a stranger on the trail',
  'wolves_warning': 'hearing about wolves',
  'watchtower': 'at the old watchtower',
  'tower_interior': 'inside the watchtower',
  'tower_exterior': 'circling the watchtower',
  'beacon_platform': 'on the beacon platform',
  'artifact_mystery': 'examining a strange artifact',
  'underbrush': 'in the dense underbrush',
  'smoke_pattern': 'watching strange smoke patterns',
  'tense_return': 'hurrying back through the forest',
  'escorted_return': 'walking with the stranger',
  'return_with_supplies': 'returning to camp with supplies',
  'return_empty': 'returning to camp empty-handed'
};

/**
 * Gets a human-readable scene name
 * 
 * @param {string} knot - Knot/scene identifier
 * @returns {string} Human-readable scene name
 */
function getSceneName(knot) {
  return SCENE_NAMES[knot] || `at ${knot.replace(/_/g, ' ')}`;
}

/**
 * Builds a prompt for the AI Writer
 * 
 * @param {Object} lore - LORE context object from LoreAssembler
 * @param {string} templateType - 'dialogue' or 'exploration'
 * @param {string[]} validReturnPaths - Array of valid return path knot names
 * @returns {{systemPrompt: string, userPrompt: string}} The complete prompt
 */
function buildPrompt(lore, templateType, validReturnPaths) {
  // Select template based on type
  const template = templateType === 'dialogue' ? DIALOGUE_TEMPLATE : EXPLORATION_TEMPLATE;
  
  // Extract values from LORE
  const traits = formatTraits(
    lore.player_state.courage || 0,
    lore.player_state.caution || 0
  );
  
  // Build substitution values
  const substitutions = {
    courage_trait: traits.courage_trait,
    caution_trait: traits.caution_trait,
    inventory: formatInventory(lore.player_state.inventory),
    scene_name: getSceneName(lore.game_state.current_scene),
    tone: lore.narrative_context.tone || 'mysterious',
    recent_context: formatRecentContext(lore.narrative_context.recent_choices),
    additional_context: generateAdditionalContext(lore),
    valid_return_paths: validReturnPaths.join(', ')
  };
  
  // Apply substitutions to template
  let userPrompt = template;
  for (const [key, value] of Object.entries(substitutions)) {
    userPrompt = userPrompt.replace(new RegExp(`\\{${key}\\}`, 'g'), value);
  }
  
  return {
    systemPrompt: SYSTEM_PROMPT,
    userPrompt: userPrompt
  };
}

/**
 * Automatically selects the best template type based on LORE context
 * 
 * @param {Object} lore - LORE context object
 * @returns {string} 'dialogue' or 'exploration'
 */
function selectTemplateType(lore) {
  const contextType = lore.game_state.context_type;
  
  // Dialogue for dialogue/tension scenes
  if (contextType === 'dialogue' || contextType === 'tension') {
    return 'dialogue';
  }
  
  // Exploration for discovery/exploration scenes
  return 'exploration';
}

/**
 * Convenience function to build a prompt automatically based on context
 * 
 * @param {Object} lore - LORE context object from LoreAssembler
 * @param {string[]} validReturnPaths - Array of valid return path knot names
 * @returns {{systemPrompt: string, userPrompt: string, templateType: string}} Complete prompt with metadata
 */
function buildAutoPrompt(lore, validReturnPaths) {
  const templateType = selectTemplateType(lore);
  const { systemPrompt, userPrompt } = buildPrompt(lore, templateType, validReturnPaths);
  
  return {
    systemPrompt,
    userPrompt,
    templateType
  };
}

// Export for use in other modules
const PromptEngine = {
  buildPrompt,
  buildAutoPrompt,
  selectTemplateType,
  SYSTEM_PROMPT,
  DIALOGUE_TEMPLATE,
  EXPLORATION_TEMPLATE,
  getSceneName,
  formatTraits,
  formatInventory,
  formatRecentContext,
  generateAdditionalContext
};

// CommonJS export for testing
if (typeof module !== 'undefined' && module.exports) {
  module.exports = PromptEngine;
}

// Browser global export
if (typeof window !== 'undefined') {
  window.PromptEngine = PromptEngine;
}

})();
