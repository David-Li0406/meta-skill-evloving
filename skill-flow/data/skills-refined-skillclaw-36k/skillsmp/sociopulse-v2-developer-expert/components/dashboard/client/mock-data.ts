// =============================================================================
// CLIENT DASHBOARD - Centralized Mock Data
// =============================================================================

import type {
    Contract,
    Mission,
    Invoice,
    Establishment,
    Booking,
    TalentPoolMember,
    DashboardStats
} from '@/app/(platform)/dashboard/client/types';

// -----------------------------------------------------------------------------
// CONTRACTS & QUOTES
// -----------------------------------------------------------------------------
export const mockContracts: (Contract & { documentType: 'CONTRACT' | 'QUOTE' })[] = [
    {
        id: 'ctr-001',
        reference: 'CTR-2026-042',
        documentType: 'CONTRACT',
        status: 'PENDING',
        missionId: 'mis-001',
        talentName: 'Marie Lambert',
        totalAmount: 45000, // in cents
        createdAt: new Date('2026-01-18'),
    },
    {
        id: 'ctr-002',
        reference: 'CTR-2026-041',
        documentType: 'CONTRACT',
        status: 'PENDING',
        missionId: 'mis-002',
        talentName: 'Thomas Durand',
        totalAmount: 68000,
        createdAt: new Date('2026-01-17'),
    },
    {
        id: 'ctr-003',
        reference: 'CTR-2026-040',
        documentType: 'CONTRACT',
        status: 'SIGNED',
        missionId: 'mis-003',
        talentName: 'Sophie Martin',
        totalAmount: 32000,
        signedAt: new Date('2026-01-15'),
        createdAt: new Date('2026-01-14'),
    },
    {
        id: 'qte-001',
        reference: 'DEV-2026-015',
        documentType: 'QUOTE',
        status: 'PENDING',
        talentName: 'Claire Dubois',
        totalAmount: 150000,
        createdAt: new Date('2026-01-19'),
    },
];

// -----------------------------------------------------------------------------
// MISSIONS
// -----------------------------------------------------------------------------
export const mockMissions: Mission[] = [
    {
        id: 'mis-001',
        title: 'Renfort weekend EHPAD - Nuit',
        status: 'OPEN',
        startDate: new Date('2026-01-25T20:00:00'),
        endDate: new Date('2026-01-26T06:00:00'),
        hourlyRate: 25,
        city: 'Lyon 3ème',
        urgencyLevel: 'CRITICAL',
        createdAt: new Date('2026-01-18'),
    },
    {
        id: 'mis-002',
        title: 'Éducateur spécialisé - Vacances scolaires',
        status: 'ASSIGNED',
        talentId: 'tal-002',
        talentName: 'Thomas Durand',
        startDate: new Date('2026-01-27T08:00:00'),
        endDate: new Date('2026-01-31T18:00:00'),
        hourlyRate: 28,
        city: 'Villeurbanne',
        urgencyLevel: 'MEDIUM',
        createdAt: new Date('2026-01-15'),
    },
    {
        id: 'mis-003',
        title: 'Art-thérapie Groupe Séniors',
        status: 'COMPLETED',
        talentId: 'tal-003',
        talentName: 'Sophie Martin',
        startDate: new Date('2026-01-10T14:00:00'),
        endDate: new Date('2026-01-10T17:00:00'),
        hourlyRate: 45,
        city: 'Lyon 6ème',
        urgencyLevel: 'LOW',
        createdAt: new Date('2026-01-05'),
    },
    {
        id: 'mis-004',
        title: 'AMP Accompagnement sortie',
        status: 'COMPLETED',
        talentId: 'tal-001',
        talentName: 'Marie Lambert',
        startDate: new Date('2026-01-08T09:00:00'),
        endDate: new Date('2026-01-08T18:00:00'),
        hourlyRate: 22,
        city: 'Lyon',
        urgencyLevel: 'LOW',
        createdAt: new Date('2026-01-02'),
    },
];

// -----------------------------------------------------------------------------
// INVOICES & TRANSACTIONS
// -----------------------------------------------------------------------------
export const mockInvoices: Invoice[] = [
    {
        id: 'inv-001',
        reference: 'FAC-2026-015',
        amount: 45000,
        status: 'PAID',
        dueDate: new Date('2026-01-25'),
        paidAt: new Date('2026-01-18'),
        createdAt: new Date('2026-01-10'),
    },
    {
        id: 'inv-002',
        reference: 'FAC-2026-014',
        amount: 68000,
        status: 'PENDING',
        dueDate: new Date('2026-01-30'),
        createdAt: new Date('2026-01-12'),
    },
    {
        id: 'inv-003',
        reference: 'FAC-2026-013',
        amount: 32000,
        status: 'PAID',
        dueDate: new Date('2026-01-20'),
        paidAt: new Date('2026-01-15'),
        createdAt: new Date('2026-01-05'),
    },
];

export interface Transaction {
    id: string;
    type: 'CREDIT' | 'DEBIT';
    description: string;
    amount: number; // in cents
    date: Date;
    reference?: string;
}

export const mockTransactions: Transaction[] = [
    {
        id: 'txn-001',
        type: 'CREDIT',
        description: 'Rechargement Wallet',
        amount: 200000,
        date: new Date('2026-01-15'),
        reference: 'TOP-2026-001',
    },
    {
        id: 'txn-002',
        type: 'DEBIT',
        description: 'Mission #3 - Sophie Martin',
        amount: 32000,
        date: new Date('2026-01-16'),
        reference: 'FAC-2026-013',
    },
    {
        id: 'txn-003',
        type: 'DEBIT',
        description: 'Mission #4 - Marie Lambert',
        amount: 19800,
        date: new Date('2026-01-18'),
        reference: 'FAC-2026-014',
    },
    {
        id: 'txn-004',
        type: 'CREDIT',
        description: 'Rechargement Wallet',
        amount: 100000,
        date: new Date('2026-01-20'),
        reference: 'TOP-2026-002',
    },
];

// -----------------------------------------------------------------------------
// ESTABLISHMENT (with missing Chorus Pro for testing)
// -----------------------------------------------------------------------------
export const mockEstablishment: Establishment = {
    id: 'est-001',
    name: 'EHPAD Les Jardins de Bellecour',
    siret: '12345678900012',
    organizationType: 'PUBLIC',
    chorusProCode: '', // Empty to test the warning state
    address: '15 Rue des Fleurs',
    city: 'Lyon',
    postalCode: '69003',
    creditLimit: 500000, // 5000€
    currentOutstanding: 68000, // 680€
};

// -----------------------------------------------------------------------------
// TALENT POOL
// -----------------------------------------------------------------------------
export const mockTalentPool: TalentPoolMember[] = [
    {
        id: 'tpm-001',
        profileId: 'tal-001',
        firstName: 'Marie',
        lastName: 'Lambert',
        specialty: 'Aide-soignante',
        rating: 4.9,
        tags: ['Nuit', 'Weekend', 'EHPAD'],
    },
    {
        id: 'tpm-002',
        profileId: 'tal-002',
        firstName: 'Thomas',
        lastName: 'Durand',
        specialty: 'Éducateur spécialisé',
        rating: 4.7,
        tags: ['Autisme', 'Adolescents'],
    },
    {
        id: 'tpm-003',
        profileId: 'tal-003',
        firstName: 'Sophie',
        lastName: 'Martin',
        specialty: 'Art-thérapeute',
        rating: 5.0,
        tags: ['Séniors', 'Ateliers', 'Créatif'],
    },
    {
        id: 'tpm-004',
        profileId: 'tal-004',
        firstName: 'Pierre',
        lastName: 'Dubois',
        specialty: 'AMP',
        rating: 4.6,
        tags: ['EHPAD', 'Jour'],
    },
];

// -----------------------------------------------------------------------------
// DASHBOARD STATS
// -----------------------------------------------------------------------------
export const mockDashboardStats: DashboardStats = {
    activeMissions: mockMissions.filter(m => m.status === 'OPEN' || m.status === 'ASSIGNED').length,
    pendingBookings: 2,
    unsignedContracts: mockContracts.filter(c => c.status === 'PENDING').length,
    walletBalance: 125000, // 1250€
    teamSize: mockTalentPool.length,
};

// -----------------------------------------------------------------------------
// HELPER FUNCTIONS
// -----------------------------------------------------------------------------
export function formatCurrency(cents: number): string {
    return new Intl.NumberFormat('fr-FR', {
        style: 'currency',
        currency: 'EUR',
    }).format(cents / 100);
}

export function formatDate(date: Date): string {
    return new Intl.DateTimeFormat('fr-FR', {
        day: 'numeric',
        month: 'short',
        year: 'numeric',
    }).format(date);
}

export function formatDateTime(date: Date): string {
    return new Intl.DateTimeFormat('fr-FR', {
        day: 'numeric',
        month: 'short',
        hour: '2-digit',
        minute: '2-digit',
    }).format(date);
}
