'use client';

import { motion } from 'framer-motion';
import {
    Wallet,
    ArrowDownLeft,
    ArrowUpRight,
    Download,
    CreditCard,
    TrendingUp,
    Receipt,
    ChevronRight,
    Calendar
} from 'lucide-react';
import { Badge } from '@/components/ui';
import {
    mockInvoices,
    mockTransactions,
    mockDashboardStats,
    formatCurrency,
    formatDate
} from '@/components/dashboard/client/mock-data';

const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
        opacity: 1,
        transition: { staggerChildren: 0.1 }
    }
};

const itemVariants = {
    hidden: { opacity: 0, y: 10 },
    visible: { opacity: 1, y: 0 }
};

export default function ClientFinancePage() {
    const balance = mockDashboardStats.walletBalance;
    const monthlyCredits = mockTransactions
        .filter(t => t.type === 'CREDIT')
        .reduce((sum, t) => sum + t.amount, 0);
    const monthlyDebits = mockTransactions
        .filter(t => t.type === 'DEBIT')
        .reduce((sum, t) => sum + t.amount, 0);

    return (
        <motion.div
            variants={containerVariants}
            initial="hidden"
            animate="visible"
            className="p-6 space-y-6"
        >
            {/* Header */}
            <motion.div variants={itemVariants}>
                <h1 className="text-2xl font-bold text-slate-900">Finance</h1>
                <p className="text-slate-500">
                    Portefeuille, factures et historique des transactions
                </p>
            </motion.div>

            {/* Wallet Card - Credit Card Style */}
            <motion.div variants={itemVariants}>
                <div className="relative overflow-hidden rounded-2xl bg-gradient-to-br from-teal-500 via-teal-600 to-cyan-600 p-6 text-white shadow-xl">
                    {/* Background pattern */}
                    <div className="absolute inset-0 opacity-10">
                        <div className="absolute right-0 top-0 h-64 w-64 -translate-y-1/2 translate-x-1/2 rounded-full bg-white" />
                        <div className="absolute bottom-0 left-0 h-48 w-48 -translate-x-1/2 translate-y-1/2 rounded-full bg-white" />
                    </div>

                    <div className="relative">
                        {/* Card Header */}
                        <div className="flex items-center justify-between">
                            <div className="flex items-center gap-2">
                                <Wallet className="h-6 w-6" />
                                <span className="text-sm font-medium text-teal-100">Portefeuille SocioPulse</span>
                            </div>
                            <CreditCard className="h-8 w-8 text-teal-200/50" />
                        </div>

                        {/* Balance */}
                        <div className="mt-6">
                            <p className="text-sm text-teal-100">Solde disponible</p>
                            <p className="text-4xl font-bold tracking-tight">
                                {formatCurrency(balance)}
                            </p>
                        </div>

                        {/* Card Footer */}
                        <div className="mt-6 flex items-center justify-between">
                            <div className="flex gap-6">
                                <div>
                                    <p className="text-xs text-teal-200">Ce mois</p>
                                    <p className="text-sm font-medium">+{formatCurrency(monthlyCredits)}</p>
                                </div>
                                <div>
                                    <p className="text-xs text-teal-200">Dépensé</p>
                                    <p className="text-sm font-medium">-{formatCurrency(monthlyDebits)}</p>
                                </div>
                            </div>
                            <button className="inline-flex items-center gap-2 rounded-full bg-white/20 px-4 py-2 text-sm font-medium backdrop-blur-sm transition-colors hover:bg-white/30">
                                <CreditCard className="h-4 w-4" />
                                Recharger
                            </button>
                        </div>
                    </div>
                </div>
            </motion.div>

            {/* Quick Stats */}
            <motion.div variants={itemVariants} className="grid grid-cols-1 gap-4 sm:grid-cols-2">
                <div className="flex items-center gap-4 rounded-xl border border-slate-200 bg-white p-4 shadow-sm">
                    <div className="rounded-lg bg-emerald-50 p-3 text-emerald-600">
                        <ArrowDownLeft className="h-6 w-6" />
                    </div>
                    <div>
                        <p className="text-sm text-slate-500">Crédits ce mois</p>
                        <p className="text-2xl font-bold text-emerald-600">
                            +{formatCurrency(monthlyCredits)}
                        </p>
                    </div>
                </div>
                <div className="flex items-center gap-4 rounded-xl border border-slate-200 bg-white p-4 shadow-sm">
                    <div className="rounded-lg bg-rose-50 p-3 text-rose-600">
                        <ArrowUpRight className="h-6 w-6" />
                    </div>
                    <div>
                        <p className="text-sm text-slate-500">Débits ce mois</p>
                        <p className="text-2xl font-bold text-rose-600">
                            -{formatCurrency(monthlyDebits)}
                        </p>
                    </div>
                </div>
            </motion.div>

            {/* Main Content Grid */}
            <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
                {/* Transaction History */}
                <motion.div
                    variants={itemVariants}
                    className="rounded-xl border border-slate-200 bg-white shadow-sm"
                >
                    <div className="flex items-center justify-between border-b border-slate-200 px-6 py-4">
                        <h2 className="text-lg font-semibold text-slate-900">Transactions récentes</h2>
                        <button className="text-sm font-medium text-teal-600 hover:text-teal-700">
                            Voir tout
                        </button>
                    </div>
                    <div className="divide-y divide-slate-100">
                        {mockTransactions.map((transaction) => (
                            <TransactionRow key={transaction.id} transaction={transaction} />
                        ))}
                    </div>
                </motion.div>

                {/* Invoices */}
                <motion.div
                    variants={itemVariants}
                    className="rounded-xl border border-slate-200 bg-white shadow-sm"
                >
                    <div className="flex items-center justify-between border-b border-slate-200 px-6 py-4">
                        <h2 className="text-lg font-semibold text-slate-900">Factures</h2>
                        <button className="inline-flex items-center gap-2 text-sm font-medium text-teal-600 hover:text-teal-700">
                            <Download className="h-4 w-4" />
                            Exporter
                        </button>
                    </div>
                    <div className="divide-y divide-slate-100">
                        {mockInvoices.map((invoice) => (
                            <InvoiceRow key={invoice.id} invoice={invoice} />
                        ))}
                    </div>
                </motion.div>
            </div>

            {/* Quick Actions */}
            <motion.div variants={itemVariants} className="grid grid-cols-1 gap-4 md:grid-cols-3">
                <QuickAction
                    title="Historique complet"
                    description="Toutes vos transactions"
                    icon={TrendingUp}
                />
                <QuickAction
                    title="Télécharger relevé"
                    description="Export PDF mensuel"
                    icon={Receipt}
                />
                <QuickAction
                    title="Planifier un paiement"
                    description="Programmez un virement"
                    icon={Calendar}
                />
            </motion.div>
        </motion.div>
    );
}

// Sub-components

interface TransactionRowProps {
    transaction: {
        id: string;
        type: 'CREDIT' | 'DEBIT';
        description: string;
        amount: number;
        date: Date;
        reference?: string;
    };
}

function TransactionRow({ transaction }: TransactionRowProps) {
    const isCredit = transaction.type === 'CREDIT';

    return (
        <div className="flex items-center justify-between px-6 py-4">
            <div className="flex items-center gap-3">
                <div className={`rounded-lg p-2 ${isCredit ? 'bg-emerald-50 text-emerald-600' : 'bg-rose-50 text-rose-600'}`}>
                    {isCredit ? (
                        <ArrowDownLeft className="h-4 w-4" />
                    ) : (
                        <ArrowUpRight className="h-4 w-4" />
                    )}
                </div>
                <div>
                    <p className="font-medium text-slate-900">{transaction.description}</p>
                    <p className="text-sm text-slate-500">{formatDate(transaction.date)}</p>
                </div>
            </div>
            <p className={`font-semibold ${isCredit ? 'text-emerald-600' : 'text-rose-600'}`}>
                {isCredit ? '+' : '-'}{formatCurrency(transaction.amount)}
            </p>
        </div>
    );
}

interface InvoiceRowProps {
    invoice: {
        id: string;
        reference: string;
        amount: number;
        status: string;
        dueDate: Date;
        createdAt: Date;
    };
}

function InvoiceRow({ invoice }: InvoiceRowProps) {
    const statusConfig: Record<string, { label: string; variant: 'success' | 'warning' | 'destructive' }> = {
        PAID: { label: 'Payée', variant: 'success' },
        PENDING: { label: 'En attente', variant: 'warning' },
        OVERDUE: { label: 'En retard', variant: 'destructive' },
    };

    const config = statusConfig[invoice.status] || statusConfig.PENDING;

    return (
        <div className="flex items-center justify-between px-6 py-4">
            <div className="flex items-center gap-3">
                <div className="rounded-lg bg-slate-100 p-2 text-slate-600">
                    <Receipt className="h-4 w-4" />
                </div>
                <div>
                    <p className="font-medium text-slate-900">{invoice.reference}</p>
                    <p className="text-sm text-slate-500">{formatDate(invoice.createdAt)}</p>
                </div>
            </div>
            <div className="flex items-center gap-3">
                <div className="text-right">
                    <p className="font-semibold text-slate-900">{formatCurrency(invoice.amount)}</p>
                    <Badge variant={config.variant} size="sm">{config.label}</Badge>
                </div>
                <button
                    className="rounded-lg p-2 text-slate-400 transition-colors hover:bg-slate-100 hover:text-slate-600"
                    aria-label={`Télécharger la facture ${invoice.reference}`}
                >
                    <Download className="h-4 w-4" />
                </button>
            </div>
        </div>
    );
}

interface QuickActionProps {
    title: string;
    description: string;
    icon: React.ElementType;
}

function QuickAction({ title, description, icon: Icon }: QuickActionProps) {
    return (
        <button className="group flex items-center justify-between rounded-xl border border-slate-200 bg-white p-4 text-left shadow-sm transition-all hover:border-slate-300 hover:shadow-md">
            <div className="flex items-center gap-3">
                <div className="rounded-lg bg-slate-100 p-2 text-slate-600">
                    <Icon className="h-5 w-5" />
                </div>
                <div>
                    <p className="font-medium text-slate-900">{title}</p>
                    <p className="text-sm text-slate-500">{description}</p>
                </div>
            </div>
            <ChevronRight className="h-5 w-5 text-slate-400 transition-transform group-hover:translate-x-0.5" />
        </button>
    );
}
