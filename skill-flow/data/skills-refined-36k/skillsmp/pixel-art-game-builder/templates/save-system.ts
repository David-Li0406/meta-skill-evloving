/**
 * Save System Template
 *
 * Zustand store with persist middleware, immer for immutable updates,
 * and migration support for save version upgrades.
 *
 * Usage:
 *   import { useGameStore } from './stores/gameStore';
 *
 *   function Component() {
 *     const { credits, addCredits } = useGameStore();
 *     return <button onClick={() => addCredits(10)}>+10</button>;
 *   }
 */

import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';
import { immer } from 'zustand/middleware/immer';

// ============================================
// TYPES
// ============================================

interface GameState {
  // Resources
  credits: number;
  energy: number;
  maxEnergy: number;

  // Collections
  ownedItemIds: string[];

  // Progression
  purchasedUpgrades: Record<string, number>; // upgradeId → level

  // Meta
  playTimeSeconds: number;
  totalCreditsEarned: number;
  lastSaveTimestamp: string;
  saveVersion: number;
}

interface GameActions {
  // Resources
  addCredits: (amount: number) => void;
  spendCredits: (amount: number) => boolean;
  addEnergy: (amount: number) => void;
  spendEnergy: (amount: number) => boolean;

  // Collections
  addItem: (itemId: string) => void;

  // Progression
  purchaseUpgrade: (upgradeId: string) => void;

  // Game loop
  tick: (deltaSeconds: number) => void;

  // Save management
  resetGame: () => void;
}

// ============================================
// INITIAL STATE
// ============================================

const INITIAL_STATE: GameState = {
  credits: 0,
  energy: 100,
  maxEnergy: 100,
  ownedItemIds: [],
  purchasedUpgrades: {},
  playTimeSeconds: 0,
  totalCreditsEarned: 0,
  lastSaveTimestamp: new Date().toISOString(),
  saveVersion: 1,
};

// ============================================
// CURRENT SAVE VERSION
// ============================================

const CURRENT_SAVE_VERSION = 1;

// ============================================
// MIGRATION FUNCTION
// ============================================

function migrateSave(persistedState: unknown, version: number): GameState {
  let state = persistedState as GameState;

  // Migration from version 0 (no version) to version 1
  if (version === 0) {
    state = {
      ...INITIAL_STATE,
      ...state,
      saveVersion: 1,
    };
  }

  // Future migrations:
  // if (version === 1) {
  //   state = { ...state, newField: defaultValue, saveVersion: 2 };
  // }

  return state;
}

// ============================================
// STORE
// ============================================

export const useGameStore = create<GameState & GameActions>()(
  persist(
    immer((set, get) => ({
      ...INITIAL_STATE,

      // =====================================
      // RESOURCE ACTIONS
      // =====================================

      addCredits: (amount) => set((state) => {
        state.credits += amount;
        state.totalCreditsEarned += amount;
        state.lastSaveTimestamp = new Date().toISOString();
      }),

      spendCredits: (amount) => {
        const state = get();
        if (state.credits < amount) return false;

        set((s) => {
          s.credits -= amount;
          s.lastSaveTimestamp = new Date().toISOString();
        });
        return true;
      },

      addEnergy: (amount) => set((state) => {
        state.energy = Math.min(state.energy + amount, state.maxEnergy);
      }),

      spendEnergy: (amount) => {
        const state = get();
        if (state.energy < amount) return false;

        set((s) => {
          s.energy -= amount;
        });
        return true;
      },

      // =====================================
      // COLLECTION ACTIONS
      // =====================================

      addItem: (itemId) => set((state) => {
        if (!state.ownedItemIds.includes(itemId)) {
          state.ownedItemIds.push(itemId);
          state.lastSaveTimestamp = new Date().toISOString();
        }
      }),

      // =====================================
      // PROGRESSION ACTIONS
      // =====================================

      purchaseUpgrade: (upgradeId) => set((state) => {
        const currentLevel = state.purchasedUpgrades[upgradeId] || 0;
        state.purchasedUpgrades[upgradeId] = currentLevel + 1;
        state.lastSaveTimestamp = new Date().toISOString();
      }),

      // =====================================
      // GAME LOOP
      // =====================================

      tick: (deltaSeconds) => set((state) => {
        state.playTimeSeconds += deltaSeconds;
      }),

      // =====================================
      // SAVE MANAGEMENT
      // =====================================

      resetGame: () => set(() => ({
        ...INITIAL_STATE,
        lastSaveTimestamp: new Date().toISOString(),
      })),
    })),
    {
      name: 'idle-game-save', // localStorage key
      version: CURRENT_SAVE_VERSION,
      storage: createJSONStorage(() => localStorage),
      migrate: migrateSave,

      // Optional: only persist certain fields
      // partialize: (state) => ({
      //   credits: state.credits,
      //   ownedItemIds: state.ownedItemIds,
      //   // ... other fields to persist
      // }),
    }
  )
);

// ============================================
// SELECTORS (Optional optimization)
// ============================================

export const selectCredits = (state: GameState & GameActions) => state.credits;
export const selectEnergy = (state: GameState & GameActions) => state.energy;
export const selectOwnedItems = (state: GameState & GameActions) => state.ownedItemIds;

// Usage with selector:
// const credits = useGameStore(selectCredits);

// ============================================
// OFFLINE EARNINGS CALCULATOR
// ============================================

export function calculateOfflineEarnings(
  incomePerSecond: number,
  lastSaveTimestamp: string,
  maxOfflineHours: number = 8
): number {
  const lastSave = new Date(lastSaveTimestamp).getTime();
  const now = Date.now();
  const offlineMs = now - lastSave;
  const offlineSeconds = offlineMs / 1000;

  const maxOfflineSeconds = maxOfflineHours * 3600;
  const cappedSeconds = Math.min(offlineSeconds, maxOfflineSeconds);

  return incomePerSecond * cappedSeconds;
}
