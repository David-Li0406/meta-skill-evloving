// =============================================================================
// CLIENT DASHBOARD - Type Definitions
// =============================================================================

export type MissionStatus = 'OPEN' | 'ASSIGNED' | 'IN_PROGRESS' | 'COMPLETED' | 'CANCELLED';
export type ContractStatus = 'PENDING' | 'SIGNED' | 'IN_PROGRESS' | 'COMPLETED' | 'CANCELLED';
export type InvoiceStatus = 'PENDING' | 'PAID' | 'OVERDUE' | 'REFUNDED';
export type BookingStatus = 'PENDING' | 'CONFIRMED' | 'COMPLETED' | 'CANCELLED';

export interface Mission {
    id: string;
    title: string;
    status: MissionStatus;
    talentId?: string;
    talentName?: string;
    startDate: Date;
    endDate: Date;
    hourlyRate: number;
    city: string;
    urgencyLevel: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
    createdAt: Date;
}

export interface Contract {
    id: string;
    reference: string;
    status: ContractStatus;
    missionId?: string;
    talentName: string;
    totalAmount: number;
    signedAt?: Date;
    createdAt: Date;
}

export interface Invoice {
    id: string;
    reference: string;
    amount: number;
    status: InvoiceStatus;
    dueDate: Date;
    paidAt?: Date;
    createdAt: Date;
}

export interface Booking {
    id: string;
    serviceName: string;
    providerName: string;
    status: BookingStatus;
    scheduledAt: Date;
    duration: number;
    price: number;
}

export interface Establishment {
    id: string;
    name: string;
    siret?: string;
    organizationType?: 'PUBLIC' | 'PRIVATE' | 'ASSOCIATION';
    chorusProCode?: string;
    address: string;
    city: string;
    postalCode: string;
    creditLimit: number;
    currentOutstanding: number;
}

export interface TalentPoolMember {
    id: string;
    profileId: string;
    firstName: string;
    lastName: string;
    avatarUrl?: string;
    specialty: string;
    rating: number;
    tags: string[];
}

export interface DashboardStats {
    activeMissions: number;
    pendingBookings: number;
    unsignedContracts: number;
    walletBalance: number;
    teamSize: number;
}
