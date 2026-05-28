'use client';

// ===========================================
// TYPES
// ===========================================

export type BookingStatus = 'PENDING' | 'CONFIRMED' | 'PAID' | 'COMPLETED' | 'CANCELLED';

export interface StatusBadgeProps {
    status: BookingStatus;
}

// ===========================================
// CONFIGURATION
// ===========================================

const STATUS_CONFIG: Record<BookingStatus, { label: string; bg: string; text: string; dot: string }> = {
    PENDING: {
        label: 'En attente',
        bg: 'bg-orange-50',
        text: 'text-orange-700',
        dot: 'bg-orange-500',
    },
    CONFIRMED: {
        label: 'Confirmé',
        bg: 'bg-green-50',
        text: 'text-green-700',
        dot: 'bg-green-500',
    },
    PAID: {
        label: 'Payé',
        bg: 'bg-emerald-50',
        text: 'text-emerald-700',
        dot: 'bg-emerald-500',
    },
    COMPLETED: {
        label: 'Terminé',
        bg: 'bg-slate-100',
        text: 'text-slate-600',
        dot: 'bg-slate-500',
    },
    CANCELLED: {
        label: 'Annulé',
        bg: 'bg-red-50',
        text: 'text-red-700',
        dot: 'bg-red-500',
    },
};

// ===========================================
// COMPONENT
// ===========================================

export function StatusBadge({ status }: StatusBadgeProps) {
    const config = STATUS_CONFIG[status];

    return (
        <span className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold ${config.bg} ${config.text}`}>
            <span className={`w-1.5 h-1.5 rounded-full ${config.dot}`} />
            {config.label}
        </span>
    );
}
