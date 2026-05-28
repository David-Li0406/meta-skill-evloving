/**
 * Minimal Idle Game - Complete Single-File Example
 *
 * A working idle game demonstrating:
 * - Game loop with delta time (100ms tick)
 * - Zustand state management with persist
 * - Exponential upgrade costs
 * - Resource generation (passive income)
 * - Auto-save to localStorage
 *
 * To run:
 * 1. npm create vite@latest my-game -- --template react-ts
 * 2. npm install zustand
 * 3. Replace App.tsx with this file
 * 4. npm run dev
 */

import { useEffect, useState } from 'react';
import { create } from 'zustand';
import { persist } from 'zustand/middleware';

// ============================================
// TYPES
// ============================================

interface Upgrade {
  id: string;
  name: string;
  description: string;
  baseCost: number;
  costMultiplier: number;
  incomePerLevel: number;
}

interface GameState {
  credits: number;
  upgrades: Record<string, number>;
  lastTick: number;
  addCredits: (amount: number) => void;
  spendCredits: (amount: number) => boolean;
  purchaseUpgrade: (upgradeId: string) => void;
  setLastTick: (time: number) => void;
  resetGame: () => void;
}

// ============================================
// GAME DATA
// ============================================

const UPGRADES: Upgrade[] = [
  {
    id: 'clicker',
    name: 'Better Clicker',
    description: '+0.5 credits per click',
    baseCost: 10,
    costMultiplier: 1.5,
    incomePerLevel: 0, // Only affects clicking
  },
  {
    id: 'passive',
    name: 'Passive Income',
    description: '+1 credit per second',
    baseCost: 50,
    costMultiplier: 1.8,
    incomePerLevel: 1,
  },
  {
    id: 'multiplier',
    name: 'Income Multiplier',
    description: '+25% total income',
    baseCost: 500,
    costMultiplier: 2.5,
    incomePerLevel: 0, // Multiplier effect
  },
];

// ============================================
// STORE
// ============================================

const useGameStore = create<GameState>()(
  persist(
    (set, get) => ({
      credits: 0,
      upgrades: {},
      lastTick: Date.now(),

      addCredits: (amount) => set((state) => ({
        credits: state.credits + amount,
      })),

      spendCredits: (amount) => {
        const state = get();
        if (state.credits < amount) return false;
        set({ credits: state.credits - amount });
        return true;
      },

      purchaseUpgrade: (upgradeId) => set((state) => ({
        upgrades: {
          ...state.upgrades,
          [upgradeId]: (state.upgrades[upgradeId] || 0) + 1,
        },
      })),

      setLastTick: (time) => set({ lastTick: time }),

      resetGame: () => set({
        credits: 0,
        upgrades: {},
        lastTick: Date.now(),
      }),
    }),
    { name: 'idle-game-save' }
  )
);

// ============================================
// CALCULATIONS
// ============================================

function calculateUpgradeCost(upgrade: Upgrade, currentLevel: number): number {
  return Math.floor(upgrade.baseCost * Math.pow(upgrade.costMultiplier, currentLevel));
}

function calculateIncomePerSecond(upgrades: Record<string, number>): number {
  const passiveLevel = upgrades['passive'] || 0;
  const multiplierLevel = upgrades['multiplier'] || 0;

  const baseIncome = passiveLevel * 1; // 1 per level
  const multiplier = 1 + (multiplierLevel * 0.25); // +25% per level

  return baseIncome * multiplier;
}

function calculateClickValue(upgrades: Record<string, number>): number {
  const clickerLevel = upgrades['clicker'] || 0;
  return 1 + (clickerLevel * 0.5); // Base 1 + 0.5 per level
}

function formatNumber(num: number): string {
  if (num < 1000) return num.toFixed(num % 1 === 0 ? 0 : 1);
  if (num < 1000000) return (num / 1000).toFixed(1) + 'K';
  if (num < 1000000000) return (num / 1000000).toFixed(1) + 'M';
  return (num / 1000000000).toFixed(1) + 'B';
}

// ============================================
// COMPONENTS
// ============================================

function ResourceDisplay() {
  const { credits, upgrades } = useGameStore();
  const incomePerSecond = calculateIncomePerSecond(upgrades);

  return (
    <div style={{ padding: '20px', background: '#1a1a2e', marginBottom: '20px' }}>
      <h2 style={{ color: '#ffd93d', margin: 0 }}>
        {formatNumber(credits)} Credits
      </h2>
      <p style={{ color: '#39ff14', margin: '4px 0 0 0', fontSize: '14px' }}>
        +{formatNumber(incomePerSecond)}/sec
      </p>
    </div>
  );
}

function ClickButton() {
  const { addCredits, upgrades } = useGameStore();
  const clickValue = calculateClickValue(upgrades);

  return (
    <button
      onClick={() => addCredits(clickValue)}
      style={{
        width: '100%',
        padding: '20px',
        fontSize: '18px',
        background: '#00fff5',
        color: '#0a0a0f',
        border: 'none',
        borderRadius: '8px',
        marginBottom: '20px',
      }}
    >
      Click! (+{formatNumber(clickValue)})
    </button>
  );
}

function UpgradeButton({ upgrade }: { upgrade: Upgrade }) {
  const { credits, upgrades, spendCredits, purchaseUpgrade } = useGameStore();
  const currentLevel = upgrades[upgrade.id] || 0;
  const cost = calculateUpgradeCost(upgrade, currentLevel);
  const canAfford = credits >= cost;

  const handlePurchase = () => {
    if (spendCredits(cost)) {
      purchaseUpgrade(upgrade.id);
    }
  };

  return (
    <div style={{
      padding: '12px',
      background: '#1a1a2e',
      borderRadius: '8px',
      marginBottom: '8px',
      border: canAfford ? '1px solid #00fff5' : '1px solid #2d2d44',
    }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>
          <strong>{upgrade.name}</strong>
          <span style={{ color: '#a0a0a0', marginLeft: '8px' }}>Lv.{currentLevel}</span>
          <p style={{ color: '#a0a0a0', fontSize: '12px', margin: '4px 0 0 0' }}>
            {upgrade.description}
          </p>
        </div>
        <button
          onClick={handlePurchase}
          disabled={!canAfford}
          style={{
            background: canAfford ? '#00fff5' : '#2d2d44',
            color: canAfford ? '#0a0a0f' : '#a0a0a0',
            border: 'none',
            padding: '8px 16px',
            borderRadius: '4px',
          }}
        >
          {formatNumber(cost)}
        </button>
      </div>
    </div>
  );
}

function ResetButton() {
  const { resetGame } = useGameStore();
  const [confirm, setConfirm] = useState(false);

  if (confirm) {
    return (
      <div style={{ marginTop: '20px' }}>
        <p style={{ color: '#ff4757', marginBottom: '8px' }}>Reset all progress?</p>
        <button onClick={() => { resetGame(); setConfirm(false); }}
          style={{ background: '#ff4757', color: 'white', marginRight: '8px' }}>
          Yes, Reset
        </button>
        <button onClick={() => setConfirm(false)}>Cancel</button>
      </div>
    );
  }

  return (
    <button
      onClick={() => setConfirm(true)}
      style={{ marginTop: '20px', background: 'transparent', color: '#a0a0a0' }}
    >
      Reset Game
    </button>
  );
}

// ============================================
// MAIN APP
// ============================================

export default function App() {
  const { addCredits, upgrades, lastTick, setLastTick } = useGameStore();

  // Game loop - 100ms tick
  useEffect(() => {
    const interval = setInterval(() => {
      const now = Date.now();
      const deltaSeconds = (now - lastTick) / 1000;

      const income = calculateIncomePerSecond(upgrades);
      if (income > 0) {
        addCredits(income * deltaSeconds);
      }

      setLastTick(now);
    }, 100);

    return () => clearInterval(interval);
  }, [upgrades, lastTick, addCredits, setLastTick]);

  return (
    <div style={{ maxWidth: '400px', margin: '0 auto', padding: '20px' }}>
      <h1 style={{ textAlign: 'center', marginBottom: '20px' }}>Minimal Idle Game</h1>

      <ResourceDisplay />
      <ClickButton />

      <h3 style={{ marginBottom: '12px' }}>Upgrades</h3>
      {UPGRADES.map((upgrade) => (
        <UpgradeButton key={upgrade.id} upgrade={upgrade} />
      ))}

      <ResetButton />

      <p style={{ textAlign: 'center', color: '#a0a0a0', marginTop: '20px', fontSize: '12px' }}>
        Auto-saves to localStorage
      </p>
    </div>
  );
}
