'use client';

import { Download, ArrowUpRight, ArrowDownLeft } from 'lucide-react';
import type { Transaction } from './mockData';

interface InvoiceRowProps {
    transaction: Transaction;
}

export function InvoiceRow({ transaction }: InvoiceRowProps) {
    const isIncome = transaction.type === 'INCOME';
    const amountClass = isIncome ? 'text-green-600' : 'text-slate-900';
    const amountPrefix = isIncome ? '+' : '';

    const STATUS_STYLES = {
        PAID: 'bg-green-50 text-green-700',
        PENDING: 'bg-orange-50 text-orange-700',
        REFUNDED: 'bg-slate-100 text-slate-600 line-through decoration-slate-400',
    };

    const STATUS_LABELS = {
        PAID: 'Payé',
        PENDING: 'En attente',
        REFUNDED: 'Remboursé',
    };

    return (
        <div className="flex items-center justify-between p-4 hover:bg-slate-50 transition-colors group">
            <div className="flex items-center gap-4">
                <div className={`
                    w-10 h-10 rounded-full flex items-center justify-center
                    ${isIncome ? 'bg-green-50' : 'bg-slate-100'}
                `}>
                    {isIncome ? (
                        <ArrowDownLeft className="w-5 h-5 text-green-600" />
                    ) : (
                        <ArrowUpRight className="w-5 h-5 text-slate-600" />
                    )}
                </div>

                <div>
                    <h3 className="text-sm font-medium text-slate-900 truncate max-w-[200px] sm:max-w-xs">
                        {transaction.description}
                    </h3>
                    <div className="flex items-center gap-2 mt-0.5">
                        <span className="text-xs text-slate-500">
                            {transaction.date.toLocaleDateString('fr-FR')}
                        </span>
                        <span className={`px-1.5 py-0.5 rounded text-[10px] font-medium ${STATUS_STYLES[transaction.status]}`}>
                            {STATUS_LABELS[transaction.status]}
                        </span>
                    </div>
                </div>
            </div>

            <div className="flex items-center gap-4">
                <span className={`font-semibold text-sm ${amountClass}`}>
                    {amountPrefix}{transaction.amount.toFixed(2)}€
                </span>

                {transaction.downloadUrl && (
                    <button
                        className="p-2 text-slate-400 hover:text-brand-600 hover:bg-brand-50 rounded-lg transition-colors opacity-0 group-hover:opacity-100"
                        title="Télécharger la facture"
                    >
                        <Download className="w-4 h-4" />
                    </button>
                )}
            </div>
        </div>
    );
}
