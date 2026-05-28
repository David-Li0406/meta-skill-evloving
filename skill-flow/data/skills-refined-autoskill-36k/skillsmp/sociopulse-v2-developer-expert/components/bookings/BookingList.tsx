'use client';

import { BookingCard, type Booking } from './BookingCard';
import { CalendarX } from 'lucide-react';

// ===========================================
// TYPES
// ===========================================

export interface BookingListProps {
    bookings: Booking[];
    onCancel?: (id: string) => void;
    isLoading?: boolean;
}

// ===========================================
// COMPONENT
// ===========================================

export function BookingList({ bookings, onCancel, isLoading }: BookingListProps) {
    if (isLoading) {
        return (
            <div className="space-y-4">
                {[1, 2, 3].map((i) => (
                    <div key={i} className="h-40 bg-slate-100 rounded-2xl animate-pulse" />
                ))}
            </div>
        );
    }

    if (bookings.length === 0) {
        return (
            <div className="text-center py-12 bg-white rounded-2xl border border-slate-100 border-dashed">
                <div className="w-16 h-16 bg-slate-50 rounded-full flex items-center justify-center mx-auto mb-4">
                    <CalendarX className="w-8 h-8 text-slate-300" />
                </div>
                <h3 className="text-lg font-semibold text-slate-900 mb-1">
                    Aucune réservation
                </h3>
                <p className="text-sm text-slate-500">
                    Vous n'avez aucune mission prévue pour le moment.
                </p>
            </div>
        );
    }

    return (
        <div className="space-y-4">
            {bookings.map((booking) => (
                <BookingCard
                    key={booking.id}
                    booking={booking}
                    onCancel={onCancel}
                />
            ))}
        </div>
    );
}
