/**
 * Progression Formulas
 *
 * Pure functions for calculating costs, rewards, and scaling.
 * No dependencies - can be used anywhere.
 *
 * Usage:
 *   import { calculateUpgradeCost, formatNumber } from './progression';
 *
 *   const cost = calculateUpgradeCost(100, 1.5, 5); // 759
 *   const display = formatNumber(1234567); // "1.23M"
 */

// ============================================
// COST FORMULAS
// ============================================

/**
 * Exponential cost scaling (most common for idle games)
 *
 * Formula: baseCost × multiplier^currentLevel
 *
 * @param baseCost - Starting cost at level 0
 * @param multiplier - Growth rate (1.5 = 50% increase per level)
 * @param currentLevel - Current upgrade level
 * @returns Cost for next level
 *
 * @example
 * // Upgrade costs: 100, 150, 225, 337, 506...
 * calculateUpgradeCost(100, 1.5, 0) // 100
 * calculateUpgradeCost(100, 1.5, 3) // 337
 */
export function calculateUpgradeCost(
  baseCost: number,
  multiplier: number,
  currentLevel: number
): number {
  return Math.floor(baseCost * Math.pow(multiplier, currentLevel));
}

/**
 * Linear cost scaling (gentle progression)
 *
 * Formula: baseCost + (increment × currentLevel)
 *
 * @example
 * // Costs: 100, 150, 200, 250...
 * calculateLinearCost(100, 50, 2) // 200
 */
export function calculateLinearCost(
  baseCost: number,
  increment: number,
  currentLevel: number
): number {
  return Math.floor(baseCost + increment * currentLevel);
}

/**
 * Polynomial cost scaling (accelerating growth)
 *
 * Formula: baseCost × (currentLevel + 1)^exponent
 *
 * @example
 * // With exponent 2: 100, 400, 900, 1600...
 * calculatePolynomialCost(100, 2, 3) // 1600
 */
export function calculatePolynomialCost(
  baseCost: number,
  exponent: number,
  currentLevel: number
): number {
  return Math.floor(baseCost * Math.pow(currentLevel + 1, exponent));
}

/**
 * Cost to buy multiple levels at once
 *
 * @param baseCost - Starting cost
 * @param multiplier - Growth rate
 * @param currentLevel - Current level
 * @param levelsToBuy - How many levels to purchase
 * @returns Total cost for all levels
 */
export function calculateBulkUpgradeCost(
  baseCost: number,
  multiplier: number,
  currentLevel: number,
  levelsToBuy: number
): number {
  let totalCost = 0;
  for (let i = 0; i < levelsToBuy; i++) {
    totalCost += calculateUpgradeCost(baseCost, multiplier, currentLevel + i);
  }
  return totalCost;
}

/**
 * Max levels affordable with given budget
 *
 * @returns Number of levels that can be purchased
 */
export function calculateMaxAffordableLevels(
  baseCost: number,
  multiplier: number,
  currentLevel: number,
  budget: number
): number {
  let levels = 0;
  let totalCost = 0;

  while (true) {
    const nextCost = calculateUpgradeCost(baseCost, multiplier, currentLevel + levels);
    if (totalCost + nextCost > budget) break;
    totalCost += nextCost;
    levels++;
  }

  return levels;
}

// ============================================
// REWARD FORMULAS
// ============================================

/**
 * Diminishing returns formula
 *
 * Good for bonuses that shouldn't scale infinitely.
 * Approaches maxValue asymptotically.
 *
 * @param baseValue - Starting value
 * @param level - Current level
 * @param diminishRate - How quickly returns diminish (higher = faster)
 * @returns Bonus value
 *
 * @example
 * // Income bonus: +10%, +18%, +24%, +28%... (approaches 50%)
 * calculateDiminishingReturns(0.1, 0.5, level)
 */
export function calculateDiminishingReturns(
  baseValue: number,
  maxValue: number,
  level: number,
  diminishRate: number = 0.5
): number {
  return maxValue * (1 - Math.exp(-diminishRate * level * (baseValue / maxValue)));
}

/**
 * Soft cap formula
 *
 * Full effect up to threshold, then reduced effect after.
 *
 * @example
 * // 100% effect up to level 10, then 50% effect
 * applySoftCap(2, 10, 15, 0.5) // 2 + (5 * 0.5) = 4.5
 */
export function applySoftCap(
  valuePerLevel: number,
  softCapLevel: number,
  currentLevel: number,
  postCapMultiplier: number = 0.5
): number {
  if (currentLevel <= softCapLevel) {
    return valuePerLevel * currentLevel;
  }

  const preCap = valuePerLevel * softCapLevel;
  const postCap = valuePerLevel * (currentLevel - softCapLevel) * postCapMultiplier;
  return preCap + postCap;
}

// ============================================
// PRESTIGE FORMULAS
// ============================================

/**
 * Calculate prestige currency earned
 *
 * Common formula: sqrt(totalEarned / threshold)
 *
 * @param totalEarned - Total credits earned this run
 * @param threshold - Credits needed for 1 prestige point
 * @returns Prestige points to award
 *
 * @example
 * calculatePrestigePoints(1000000, 10000) // 10
 */
export function calculatePrestigePoints(
  totalEarned: number,
  threshold: number
): number {
  if (totalEarned < threshold) return 0;
  return Math.floor(Math.sqrt(totalEarned / threshold));
}

/**
 * Prestige multiplier from prestige points
 *
 * @example
 * calculatePrestigeMultiplier(10, 0.1) // 2.0 (100% bonus)
 */
export function calculatePrestigeMultiplier(
  prestigePoints: number,
  bonusPerPoint: number = 0.1
): number {
  return 1 + prestigePoints * bonusPerPoint;
}

// ============================================
// RARITY WEIGHTS
// ============================================

/**
 * Weighted random selection
 *
 * @param items - Array of items
 * @param weights - Array of weights (same length as items)
 * @returns Selected item
 *
 * @example
 * const rarities = ['common', 'uncommon', 'rare', 'epic'];
 * const weights = [60, 25, 12, 3];
 * weightedRandom(rarities, weights) // Mostly 'common'
 */
export function weightedRandom<T>(items: T[], weights: number[]): T {
  const totalWeight = weights.reduce((sum, w) => sum + w, 0);
  let random = Math.random() * totalWeight;

  for (let i = 0; i < items.length; i++) {
    random -= weights[i];
    if (random <= 0) return items[i];
  }

  return items[items.length - 1];
}

// ============================================
// NUMBER FORMATTING
// ============================================

const SUFFIXES = ['', 'K', 'M', 'B', 'T', 'Qa', 'Qi', 'Sx', 'Sp', 'Oc', 'No', 'Dc'];

/**
 * Format large numbers with suffixes
 *
 * @example
 * formatNumber(1234) // "1.23K"
 * formatNumber(1234567) // "1.23M"
 * formatNumber(42) // "42"
 */
export function formatNumber(num: number, decimals: number = 2): string {
  if (num < 1000) {
    return num % 1 === 0 ? num.toString() : num.toFixed(decimals);
  }

  const tier = Math.floor(Math.log10(Math.abs(num)) / 3);
  const suffix = SUFFIXES[Math.min(tier, SUFFIXES.length - 1)];
  const scale = Math.pow(10, tier * 3);
  const scaled = num / scale;

  return scaled.toFixed(decimals) + suffix;
}

/**
 * Format time duration
 *
 * @example
 * formatDuration(3661) // "1h 1m 1s"
 * formatDuration(90) // "1m 30s"
 */
export function formatDuration(seconds: number): string {
  const hours = Math.floor(seconds / 3600);
  const minutes = Math.floor((seconds % 3600) / 60);
  const secs = Math.floor(seconds % 60);

  const parts: string[] = [];
  if (hours > 0) parts.push(`${hours}h`);
  if (minutes > 0) parts.push(`${minutes}m`);
  if (secs > 0 || parts.length === 0) parts.push(`${secs}s`);

  return parts.join(' ');
}
