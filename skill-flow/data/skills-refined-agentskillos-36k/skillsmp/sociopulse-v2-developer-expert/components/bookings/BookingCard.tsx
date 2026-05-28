'use client';

import { motion } from 'framer-motion';
import {
    Calendar,
    Clock,
    MapPin,
    MoreVertical,
    MessageCircle,
    User,
} from 'lucide-react';
import Link from 'next/link';
import { StatusBadge, type BookingStatus } from './StatusBadge';
import { AddToCalendar } from './AddToCalendar';
import type { CalendarEvent } from '@/lib/calendar';

// ===========================================
// TYPES
// ===========================================

export interface Booking {
    id: string;
    title: string;
    partnerName: string;
    partnerAvatar?: string;
    date: Date;
    time: string;
    duration: string;
    location: string;
    price: number;
    status: BookingStatus;
}

export interface BookingCardProps {
    booking: Booking;
    onCancel?: (id: string) => void;
}

// ===========================================
// COMPONENT
// ===========================================

export function BookingCard({ booking, onCancel }: BookingCardProps) {
    return (
        <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            whileHover={{ y: -2 }}
            className="card-surface p-0 overflow-hidden group transition-all duration-300 hover:shadow-lg"
        >
            <div className="p-5 flex flex-col sm:flex-row gap-4">
                {/* Date Box */}
                <div className="flex-shrink-0 flex sm:flex-col items-center justify-center sm:justify-start gap-2 sm:gap-0 w-full sm:w-16 bg-slate-50 rounded-xl sm:p-2 border border-slate-100">
                    <span className="text-xs font-semibold text-slate-500 uppercase">
                        {booking.date.toLocaleDateString('fr-FR', { month: 'short' })}
                    </span>
                    <span className="text-2xl font-bold text-slate-900">
                        {booking.date.getDate()}
                    </span>
                </div>

                {/* Content */}
                <div className="flex-1 min-w-0">
                    <div className="flex items-start justify-between gap-2">
                        <div>
                            <h3 className="font-semibold text-slate-900 truncate">
                                {booking.title}
                            </h3>
                            <div className="flex items-center gap-2 mt-1">
                                <StatusBadge status={booking.status} />
                                <span className="text-sm font-medium text-slate-900">
                                    {booking.price}€
                                </span>
                            </div>
                        </div>

                        <button className="p-1 rounded-lg hover:bg-slate-100 text-slate-400 opacity-0 group-hover:opacity-100 transition-opacity">
                            <MoreVertical className="w-5 h-5" />
                        </button>
                    </div>

                    <div className="mt-4 grid grid-cols-1 sm:grid-cols-2 gap-2 text-sm text-slate-600">
                        <div className="flex items-center gap-2">
                            <Clock className="w-4 h-4 text-slate-400" />
                            {booking.time} ({booking.duration})
                        </div>
                        <div className="flex items-center gap-2">
                            <MapPin className="w-4 h-4 text-slate-400" />
                            {booking.location}
                        </div>
                    </div>

                    <div className="mt-4 flex items-center justify-between pt-4 border-t border-slate-50">
                        <div className="flex items-center gap-2">
                            <div className="w-6 h-6 rounded-full bg-gradient-to-br from-brand-100 to-brand-50 flex items-center justify-center overflow-hidden">
                                {booking.partnerAvatar ? (
                                    <img src={booking.partnerAvatar} alt={booking.partnerName} className="w-full h-full object-cover" />
                                ) : (
                                    <User className="w-3 h-3 text-brand-600" />
                                )}
                            </div>
                            <span className="text-sm font-medium text-slate-700">
                                {booking.partnerName}
                            </span>
                        </div>

                        <div className="flex items-center gap-2">
                            {/* Add to Calendar Button */}
                            <AddToCalendar
                                event={bookingToCalendarEvent(booking)}
                                variant="icon"
                                size="sm"
                            />
                            <Link
                                href={`/messages/conv-${booking.id}`} // Mock link
                                className="p-2 rounded-lg text-slate-400 hover:text-brand-600 hover:bg-brand-50 transition-colors"
                            >
                                <MessageCircle className="w-5 h-5" />
                            </Link>
                            {booking.status === 'PENDING' && onCancel && (
                                <button
                                    onClick={() => onCancel(booking.id)}
                                    className="text-xs font-semibold text-red-500 hover:text-red-600 px-3 py-1.5 rounded-lg hover:bg-red-50 transition-colors"
                                >
                                    Annuler
                                </button>
                            )}
                        </div>
                    </div>
                </div>
            </div>
        </motion.div>
    );
}

// ===========================================
// HELPER: Convert Booking to CalendarEvent
// ===========================================

function bookingToCalendarEvent(booking: Booking): CalendarEvent {
    // Parse time string (e.g., "14h00" or "14:00")
    const timeParts = booking.time.replace('h', ':').split(':');
    const hours = parseInt(timeParts[0], 10);
    const minutes = parseInt(timeParts[1] || '0', 10);

    // Parse duration string (e.g., "2h" or "1h30")
    const durationMatch = booking.duration.match(/(\d+)h(\d+)?/);
    const durationHours = durationMatch ? parseInt(durationMatch[1], 10) : 1;
    const durationMinutes = durationMatch && durationMatch[2] ? parseInt(durationMatch[2], 10) : 0;

    // Create start date
    const startDate = new Date(booking.date);
    startDate.setHours(hours, minutes, 0, 0);

    // Create end date
    const endDate = new Date(startDate);
    endDate.setHours(
        startDate.getHours() + durationHours,
        startDate.getMinutes() + durationMinutes
    );

    return {
        title: booking.title,
        description: `Réservation avec ${booking.partnerName}\n\nStatut: ${booking.status}\nPrix: ${booking.price}€`,
        location: booking.location,
        startDate,
        endDate,
        organizer: booking.partnerName,
    };
}