'use client';

import { ArrowUpRight, Wallet } from 'lucide-react';
import type { WalletStats } from './mockData';

interface WalletCardProps {
    stats: WalletStats;
    onWithdraw: () => void;
}

export function WalletCard({ stats, onWithdraw }: WalletCardProps) {
    return (
        <div className="card-surface p-6 bg-gradient-to-br from-slate-900 to-slate-800 text-white">
            <div className="flex items-start justify-between mb-8">
                <div>
                    <h2 className="text-slate-400 text-sm font-medium mb-1">Solde disponible</h2>
                    <div className="text-4xl font-bold tracking-tight">
                        {stats.balance.toFixed(2)}€
                    </div>
                </div>
                <div className="p-3 bg-white/10 rounded-xl backdrop-blur-md">
                    <Wallet className="w-6 h-6 text-brand-400" />
                </div>
            </div>

            <div className="flex items-center gap-4">
                <button
                    onClick={onWithdraw}
                    className="flex-1 bg-brand-600 hover:bg-brand-700 text-white font-semibold py-2.5 rounded-lg transition-colors flex items-center justify-center gap-2"
                >
                    Demander un virement
                    <ArrowUpRight className="w-4 h-4" />
                </button>
            </div>

            <div className="mt-6 pt-6 border-t border-white/10 grid grid-cols-2 gap-4">
                <div>
                    <div className="text-slate-400 text-xs mb-1">En attente</div>
                    <div className="text-lg font-semibold text-orange-400">
                        {stats.pending.toFixed(2)}€
                    </div>
                </div>
                <div>
                    <div className="text-slate-400 text-xs mb-1">Gagné en Déc.</div>
                    <div className="text-lg font-semibold text-green-400">
                        +{stats.lastMonth.toFixed(2)}€
                    </div>
                </div>
            </div>
        </div>
    );
}
