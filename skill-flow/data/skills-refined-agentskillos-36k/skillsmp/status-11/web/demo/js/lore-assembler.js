/**
 * LORE Context Assembler
 * 
 * Extracts player state, current scene, and recent choices from the Ink runtime
 * into a structured LORE (Living Observed Runtime Experience) context object.
 * 
 * @module lore-assembler
 * @see docs/dev/m2-design/lore-model.md
 */
(function() {
"use strict";

/**
 * Maximum number of recent choices to track
 * @const {number}
 */
const MAX_CHOICE_HISTORY = 5;

/**
 * Variables to extract from the Ink story state
 * These correspond to the demo.ink story variables
 * @const {string[]}
 */
const TRACKED_VARIABLES = [
  'campfire_log',
  'pocket_compass',
  'courage',
  'caution',
  'met_stranger',
  'found_artifact',
  'wolves_spotted'
];

/**
 * Choice history maintained across the session
 * @type {Array<{text: string, timestamp: number}>}
 */
let choiceHistory = [];

/**
 * Current knot/scene being tracked
 * @type {string|null}
 */
let currentKnot = null;

/**
 * Extracts variables from the Ink story's variablesState
 * 
 * @param {Object} story - The inkjs Story instance
 * @returns {Object} Key-value pairs of tracked variables
 */
function extractVariables(story) {
  const variables = {};
  
  if (!story || !story.variablesState) {
    return variables;
  }
  
  for (const varName of TRACKED_VARIABLES) {
    try {
      const value = story.variablesState[varName];
      if (value !== undefined) {
        variables[varName] = value;
      }
    } catch (e) {
      // Variable doesn't exist in this story, skip
      console.debug(`[lore-assembler] Variable ${varName} not found in story`);
    }
  }
  
  return variables;
}

/**
 * Attempts to determine the current knot/scene from story state
 * 
 * @param {Object} story - The inkjs Story instance
 * @returns {string} Current knot name or 'unknown'
 */
function getCurrentKnot(story) {
  if (!story || !story.state) {
    return 'unknown';
  }
  
  try {
    // Try to get current path from story state
    const currentPath = story.state.currentPathString;
    if (currentPath) {
      // Extract knot name from path (first segment before '.')
      const knotMatch = currentPath.match(/^([^.]+)/);
      if (knotMatch) {
        currentKnot = knotMatch[1];
        return currentKnot;
      }
    }
  } catch (e) {
    console.debug('[lore-assembler] Could not extract current knot', e);
  }
  
  return currentKnot || 'unknown';
}

/**
 * Records a player choice in the history
 * 
 * @param {string} choiceText - The text of the choice made
 */
function recordChoice(choiceText) {
  choiceHistory.push({
    text: choiceText,
    timestamp: Date.now()
  });
  
  // Maintain max history size
  if (choiceHistory.length > MAX_CHOICE_HISTORY) {
    choiceHistory.shift();
  }
}

/**
 * Gets the recent choice history
 * 
 * @returns {Array<{text: string, timestamp: number}>} Recent choices
 */
function getChoiceHistory() {
  return [...choiceHistory];
}

/**
 * Clears the choice history (e.g., on story restart)
 */
function clearHistory() {
  choiceHistory = [];
  currentKnot = null;
}

/**
 * Determines the narrative context type based on current scene
 * Used to help the prompt engine select the appropriate template
 * 
 * @param {string} knot - Current knot name
 * @param {Object} variables - Story variables
 * @returns {string} Context type: 'dialogue', 'exploration', 'tension', or 'discovery'
 */
function determineContextType(knot, variables) {
  // Dialogue scenes
  const dialogueKnots = [
    'stranger_dialogue', 'escorted_return', 'philosophical_moment',
    'shared_mystery', 'wolves_warning'
  ];
  if (dialogueKnots.includes(knot)) {
    return 'dialogue';
  }
  
  // Tension scenes
  const tensionKnots = ['tense_return', 'wolves_warning', 'descent_choice'];
  if (tensionKnots.includes(knot) || variables.wolves_spotted) {
    return 'tension';
  }
  
  // Discovery scenes
  const discoveryKnots = [
    'watchtower', 'tower_interior', 'tower_exterior', 
    'artifact_mystery', 'smoke_pattern', 'beacon_platform'
  ];
  if (discoveryKnots.includes(knot)) {
    return 'discovery';
  }
  
  // Default to exploration for forest/navigation scenes
  return 'exploration';
}

/**
 * Assembles the complete LORE context from current story state
 * 
 * @param {Object} story - The inkjs Story instance
 * @returns {Object} LORE context object conforming to partial LORE schema
 */
function assembleLORE(story) {
  const variables = extractVariables(story);
  const knot = getCurrentKnot(story);
  const contextType = determineContextType(knot, variables);
  
  // Build player state section
  const playerState = {
    variables: variables,
    courage: variables.courage || 0,
    caution: variables.caution || 0,
    inventory: []
  };
  
  // Build inventory from boolean flags
  if (variables.campfire_log) {
    playerState.inventory.push('flint and tinder');
  }
  if (variables.pocket_compass) {
    playerState.inventory.push('pocket compass');
  }
  if (variables.found_artifact) {
    playerState.inventory.push('mysterious artifact');
  }
  
  // Build game state section
  const gameState = {
    current_scene: knot,
    context_type: contextType,
    wolves_spotted: variables.wolves_spotted || false,
    met_stranger: variables.met_stranger || false
  };
  
  // Build narrative context section
  const narrativeContext = {
    recent_choices: choiceHistory.map(c => c.text),
    choice_count: choiceHistory.length,
    story_themes: ['discovery', 'survival', 'companionship'],
    tone: variables.wolves_spotted ? 'tense' : 'mysterious'
  };
  
  // Compute simple context hash for reproducibility tracking
  const contextString = JSON.stringify({
    knot,
    variables,
    choiceCount: choiceHistory.length
  });
  const contextHash = simpleHash(contextString);
  
  return {
    player_state: playerState,
    game_state: gameState,
    narrative_context: narrativeContext,
    context_hash: contextHash,
    capture_timestamp: new Date().toISOString()
  };
}

/**
 * Simple hash function for context tracking
 * Not cryptographic, just for identification
 * 
 * @param {string} str - String to hash
 * @returns {string} Hex hash string
 */
function simpleHash(str) {
  let hash = 0;
  for (let i = 0; i < str.length; i++) {
    const char = str.charCodeAt(i);
    hash = ((hash << 5) - hash) + char;
    hash = hash & hash; // Convert to 32-bit integer
  }
  // Convert to positive hex string, pad to 8 chars
  const hexHash = (hash >>> 0).toString(16).padStart(8, '0');
  return hexHash;
}

/**
 * Gets valid return path targets for the current story position
 * Based on docs/dev/m2-design/demo-return-targets.md
 * 
 * @param {string} currentKnot - Current knot name
 * @returns {string[]} Array of valid return path knot names
 */
function getValidReturnPaths(currentKnot) {
  // Tier 1: Primary return points (always valid)
  const tier1 = [
    'return_with_supplies',
    'return_empty',
    'campfire',
    'pines'
  ];
  
  // Tier 2: Secondary return points
  const tier2 = [
    'watchtower',
    'tower_interior',
    'beacon_platform',
    'tense_return',
    'underbrush'
  ];
  
  // Endings should never be return paths
  const endings = [
    'rescue_end', 'waiting_end', 'quiet_end', 'lost_end',
    'tower_gathering_end', 'urgent_return_end', 'revelation_end'
  ];
  
  // Don't return to current knot or endings
  const validPaths = [...tier1, ...tier2].filter(
    knot => knot !== currentKnot && !endings.includes(knot)
  );
  
  return validPaths;
}

// Export for use in other modules
const LoreAssembler = {
  assembleLORE,
  recordChoice,
  getChoiceHistory,
  clearHistory,
  extractVariables,
  getCurrentKnot,
  determineContextType,
  getValidReturnPaths,
  TRACKED_VARIABLES,
  MAX_CHOICE_HISTORY
};

// CommonJS export for testing
if (typeof module !== 'undefined' && module.exports) {
  module.exports = LoreAssembler;
}

// Browser global export
if (typeof window !== 'undefined') {
  window.LoreAssembler = LoreAssembler;
}

})();
