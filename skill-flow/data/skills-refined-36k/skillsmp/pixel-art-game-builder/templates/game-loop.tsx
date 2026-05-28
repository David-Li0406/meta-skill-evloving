/**
 * Game Loop Hook
 *
 * Provides a 100ms tick loop with delta time calculation.
 * Handles resource generation, energy regeneration, and play time tracking.
 *
 * Usage:
 *   function App() {
 *     useGameLoop();
 *     return <div>Game is running...</div>;
 *   }
 */

import { useEffect, useRef } from 'react';

// ============================================
// TYPES - Adapt these to your game
// ============================================

interface GameState {
  credits: number;
  energy: number;
  maxEnergy: number;
  playTimeSeconds: number;
}

interface GameActions {
  addCredits: (amount: number) => void;
  addEnergy: (amount: number) => void;
  tick: (deltaSeconds: number) => void;
}

// ============================================
// MOCK STORE - Replace with your actual store
// ============================================

// Example: import { useGameStore } from '../stores/gameStore';
const useGameStore = (): GameState & GameActions => {
  // Replace this with your actual Zustand store
  throw new Error('Replace useGameStore with your actual store import');
};

// ============================================
// SERVICES - Replace with your calculations
// ============================================

function calculateTotalIncome(state: GameState): number {
  // Replace with your income calculation
  // Example: sum of all owned items' income rates
  return 1.0; // 1 credit per second base
}

function calculateEnergyRegen(state: GameState): number {
  // Replace with your energy regen calculation
  // Example: base regen * upgrade multipliers
  return 0.1; // 0.1 energy per second base (1 per 10 seconds)
}

// ============================================
// HOOK
// ============================================

export function useGameLoop() {
  const lastTickRef = useRef(Date.now());

  // Get store values and actions
  const state = useGameStore();
  const { addCredits, addEnergy, tick } = state;

  useEffect(() => {
    const TICK_INTERVAL = 100; // 10 updates per second

    const interval = setInterval(() => {
      const now = Date.now();
      const deltaMs = now - lastTickRef.current;
      const deltaSeconds = deltaMs / 1000;

      // Update play time
      tick(deltaSeconds);

      // Calculate and add income
      const income = calculateTotalIncome(state);
      if (income > 0) {
        addCredits(income * deltaSeconds);
      }

      // Regenerate energy (cap at maxEnergy)
      if (state.energy < state.maxEnergy) {
        const energyRegen = calculateEnergyRegen(state);
        const newEnergy = Math.min(
          energyRegen * deltaSeconds,
          state.maxEnergy - state.energy
        );
        addEnergy(newEnergy);
      }

      lastTickRef.current = now;
    }, TICK_INTERVAL);

    return () => clearInterval(interval);
  }, [state, addCredits, addEnergy, tick]);
}

// ============================================
// VARIANT: With pause support
// ============================================

export function useGameLoopWithPause(isPaused: boolean) {
  const lastTickRef = useRef(Date.now());
  const state = useGameStore();
  const { addCredits, addEnergy, tick } = state;

  useEffect(() => {
    if (isPaused) {
      // Reset lastTick when resuming to avoid time jumps
      lastTickRef.current = Date.now();
      return;
    }

    const TICK_INTERVAL = 100;

    const interval = setInterval(() => {
      const now = Date.now();
      const deltaMs = now - lastTickRef.current;
      const deltaSeconds = deltaMs / 1000;

      tick(deltaSeconds);

      const income = calculateTotalIncome(state);
      if (income > 0) {
        addCredits(income * deltaSeconds);
      }

      if (state.energy < state.maxEnergy) {
        const energyRegen = calculateEnergyRegen(state);
        const newEnergy = Math.min(
          energyRegen * deltaSeconds,
          state.maxEnergy - state.energy
        );
        addEnergy(newEnergy);
      }

      lastTickRef.current = now;
    }, TICK_INTERVAL);

    return () => clearInterval(interval);
  }, [isPaused, state, addCredits, addEnergy, tick]);
}
