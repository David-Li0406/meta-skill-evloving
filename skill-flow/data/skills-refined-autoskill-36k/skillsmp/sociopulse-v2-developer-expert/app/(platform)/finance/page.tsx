'use client';

import { useState } from 'react';
import { ChevronLeft, FileText, Wallet } from 'lucide-react';
import Link from 'next/link';
import {
    WalletCard,
    TransactionList,
    MOCK_WALLET_STATS,
    MOCK_TRANSACTIONS
} from '@/components/finance';

export default function FinancePage() {
    const [isClientMode, setIsClientMode] = useState(false);

    // Filter transactions based on active mode
    // In a real app, this would be fetched from API based on user role
    const filteredTransactions = isClientMode
        ? MOCK_TRANSACTIONS.filter(t => t.type === 'EXPENSE')
        : MOCK_TRANSACTIONS.filter(t => t.type === 'INCOME');

    return (
        <div className="min-h-screen bg-slate-50">
            {/* Header */}
            <header className="bg-white border-b border-slate-100 sticky top-0 z-30">
                <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
                    <div className="flex items-center gap-4">
                        <Link href="/" className="p-2 -ml-2 hover:bg-slate-50 rounded-lg transition-colors">
                            <ChevronLeft className="w-5 h-5 text-slate-600" />
                        </Link>
                        <h1 className="text-lg font-bold text-slate-900">Ma Finance</h1>
                    </div>

                    {/* Role Toggle for Demo */}
                    <button
                        onClick={() => setIsClientMode(!isClientMode)}
                        className="text-xs font-semibold px-3 py-1 bg-slate-100 hover:bg-slate-200 rounded-full text-slate-600 transition-colors"
                    >
                        Vue: {isClientMode ? 'CLIENT' : 'FREELANCE'}
                    </button>
                </div>
            </header>

            <main className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">

                {/* Dashboard Header */}
                {isClientMode ? (
                    // CLIENT VIEW
                    <div className="card-surface p-6 bg-slate-900 text-white">
                        <div className="flex items-start justify-between">
                            <div>
                                <h2 className="text-slate-400 text-sm font-medium mb-1">Dépenses (Décembre)</h2>
                                <div className="text-3xl font-bold tracking-tight">
                                    1 240,00 €
                                </div>
                            </div>
                            <div className="p-3 bg-white/10 rounded-xl backdrop-blur-md">
                                <FileText className="w-6 h-6 text-slate-300" />
                            </div>
                        </div>
                        <div className="mt-4 pt-4 border-t border-white/10 flex gap-4 text-sm">
                            <span className="text-slate-400">Total factures: 12</span>
                            <span className="text-slate-400">En attente: 0</span>
                        </div>
                    </div>
                ) : (
                    // FREELANCE VIEW
                    <WalletCard
                        stats={MOCK_WALLET_STATS}
                        onWithdraw={() => alert('Demande de virement envoyée !')}
                    />
                )}

                {/* History List */}
                <TransactionList
                    title={isClientMode ? 'Mes Factures' : 'Historique des Revenus'}
                    transactions={filteredTransactions}
                />

            </main>
        </div>
    );
}
