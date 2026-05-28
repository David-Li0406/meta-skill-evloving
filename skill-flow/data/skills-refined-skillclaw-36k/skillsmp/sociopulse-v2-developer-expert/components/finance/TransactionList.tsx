'use client';

import { InvoiceRow } from './InvoiceRow';
import type { Transaction } from './mockData';

interface TransactionListProps {
    transactions: Transaction[];
    title?: string;
}

export function TransactionList({ transactions, title = 'Historique' }: TransactionListProps) {
    return (
        <div className="card-surface overflow-hidden">
            <div className="px-6 py-4 border-b border-slate-100">
                <h3 className="font-semibold text-slate-900">{title}</h3>
            </div>
            <div className="divide-y divide-slate-100">
                {transactions.map((tx) => (
                    <InvoiceRow key={tx.id} transaction={tx} />
                ))}
            </div>
        </div>
    );
}
