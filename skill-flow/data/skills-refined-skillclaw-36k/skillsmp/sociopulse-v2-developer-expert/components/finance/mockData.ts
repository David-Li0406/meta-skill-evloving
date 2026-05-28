export type TransactionStatus = 'PAID' | 'PENDING' | 'REFUNDED';
export type TransactionType = 'INCOME' | 'EXPENSE';

export interface Transaction {
    id: string;
    description: string;
    amount: number;
    date: Date;
    status: TransactionStatus;
    type: TransactionType;
    downloadUrl?: string; // Mock PDF link
}

export interface WalletStats {
    balance: number;
    pending: number;
    lastMonth: number;
}

export const MOCK_WALLET_STATS: WalletStats = {
    balance: 1250.00,
    pending: 340.00,
    lastMonth: 890.00,
};

export const MOCK_TRANSACTIONS: Transaction[] = [
    {
        id: 'tx-1',
        description: 'Mission Garde de nuit - EHPAD Les Oliviers',
        amount: 220.00,
        date: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000), // 2 days ago
        status: 'PAID',
        type: 'INCOME',
        downloadUrl: '#',
    },
    {
        id: 'tx-2',
        description: 'Remplacement Infirmier - Clinique St Joseph',
        amount: 180.00,
        date: new Date(Date.now() - 5 * 24 * 60 * 60 * 1000),
        status: 'PENDING',
        type: 'INCOME',
    },
    {
        id: 'tx-3',
        description: 'Abonnement Premium (Mensuel)',
        amount: -29.00,
        date: new Date(Date.now() - 15 * 24 * 60 * 60 * 1000),
        status: 'PAID',
        type: 'EXPENSE',
        downloadUrl: '#',
    },
    {
        id: 'tx-4',
        description: 'Formation Premiers Secours',
        amount: -150.00,
        date: new Date(Date.now() - 20 * 24 * 60 * 60 * 1000),
        status: 'REFUNDED',
        type: 'EXPENSE',
        downloadUrl: '#',
    },
];
