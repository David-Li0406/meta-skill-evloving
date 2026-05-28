'use client';

import { useState, useEffect, useMemo, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
    ChevronLeft,
    ChevronRight,
    Calendar,
    Clock,
    Euro,
    CheckCircle2,
    Loader2,
    AlertCircle,
    User,
} from 'lucide-react';
import { Button } from '@/components/ui';
import { toast } from 'sonner';
import { cn } from '@/lib/utils';
import { getAvailableSlots, type TimeSlot } from '@/lib/availability';
import { AddToCalendar } from './AddToCalendar';
import type { CalendarEvent } from '@/lib/calendar';

// =============================================================================
// TYPES
// =============================================================================

interface BookingCalendarProps {
    talentId: string;
    talentName: string;
    serviceName: string;
    servicePrice: number;
    serviceDuration: number; // in minutes
    onBookingComplete?: (booking: BookingData) => void;
    availableDays?: number[]; // 0-6, Sunday-Saturday (for highlighting)
    className?: string;
}

interface BookingData {
    talentId: string;
    date: string;
    startTime: string;
    endTime: string;
    price: number;
}

// =============================================================================
// DATE UTILITIES
// =============================================================================

const DAYS_FR = ['Dim', 'Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam'];
const MONTHS_FR = [
    'Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin',
    'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre'
];
const DAYS_FULL_FR = ['Dimanche', 'Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi'];

function formatDateISO(date: Date): string {
    return date.toISOString().split('T')[0];
}

function formatTimeDisplay(isoString: string): string {
    const date = new Date(isoString);
    return date.toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' });
}

function formatDateDisplay(date: Date): string {
    const dayName = DAYS_FULL_FR[date.getDay()];
    const day = date.getDate();
    const month = MONTHS_FR[date.getMonth()];
    return `${dayName} ${day} ${month}`;
}

function isSameDay(date1: Date, date2: Date): boolean {
    return (
        date1.getFullYear() === date2.getFullYear() &&
        date1.getMonth() === date2.getMonth() &&
        date1.getDate() === date2.getDate()
    );
}

function isPastDate(date: Date): boolean {
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    const checkDate = new Date(date);
    checkDate.setHours(0, 0, 0, 0);
    return checkDate < today;
}

function getDaysInMonth(year: number, month: number): Date[] {
    const days: Date[] = [];
    const firstDay = new Date(year, month, 1);
    const lastDay = new Date(year, month + 1, 0);

    // Add empty slots for days before the first day of month
    const startPadding = firstDay.getDay() === 0 ? 6 : firstDay.getDay() - 1; // Monday start
    for (let i = startPadding; i > 0; i--) {
        const prevDate = new Date(year, month, 1 - i);
        days.push(prevDate);
    }

    // Add all days in the month
    for (let d = 1; d <= lastDay.getDate(); d++) {
        days.push(new Date(year, month, d));
    }

    // Add empty slots for days after the last day of month
    const endPadding = 7 - (days.length % 7);
    if (endPadding < 7) {
        for (let i = 1; i <= endPadding; i++) {
            days.push(new Date(year, month + 1, i));
        }
    }

    return days;
}

// =============================================================================
// COMPONENT
// =============================================================================

export function BookingCalendar({
    talentId,
    talentName,
    serviceName,
    servicePrice,
    serviceDuration,
    onBookingComplete,
    availableDays = [1, 2, 3, 4, 5], // Default: Mon-Fri
    className,
}: BookingCalendarProps) {
    const today = new Date();
    const [currentMonth, setCurrentMonth] = useState(today.getMonth());
    const [currentYear, setCurrentYear] = useState(today.getFullYear());
    const [selectedDate, setSelectedDate] = useState<Date | null>(null);
    const [selectedSlot, setSelectedSlot] = useState<TimeSlot | null>(null);
    const [slots, setSlots] = useState<TimeSlot[]>([]);
    const [isLoadingSlots, setIsLoadingSlots] = useState(false);
    const [isBooking, setIsBooking] = useState(false);
    const [slotsError, setSlotsError] = useState<string | null>(null);
    const [bookingConfirmed, setBookingConfirmed] = useState(false);

    // Get days for current month view
    const calendarDays = useMemo(() => {
        return getDaysInMonth(currentYear, currentMonth);
    }, [currentYear, currentMonth]);

    // Navigate months
    const goToPrevMonth = () => {
        if (currentMonth === 0) {
            setCurrentMonth(11);
            setCurrentYear(currentYear - 1);
        } else {
            setCurrentMonth(currentMonth - 1);
        }
        setSelectedDate(null);
        setSelectedSlot(null);
    };

    const goToNextMonth = () => {
        if (currentMonth === 11) {
            setCurrentMonth(0);
            setCurrentYear(currentYear + 1);
        } else {
            setCurrentMonth(currentMonth + 1);
        }
        setSelectedDate(null);
        setSelectedSlot(null);
    };

    // Fetch slots when date is selected
    const fetchSlots = useCallback(async (date: Date) => {
        setIsLoadingSlots(true);
        setSlotsError(null);
        setSlots([]);
        setSelectedSlot(null);

        try {
            const dateStr = formatDateISO(date);
            const response = await getAvailableSlots(talentId, dateStr, serviceDuration);
            const availableSlots = response.slots.filter(slot => slot.available);
            setSlots(availableSlots);
        } catch (error) {
            console.error('Error fetching slots:', error);
            setSlotsError('Impossible de charger les créneaux');
            // Mock data for development
            setSlots([
                { startTime: new Date(date.setHours(9, 0)).toISOString(), endTime: new Date(date.setHours(10, 0)).toISOString(), available: true },
                { startTime: new Date(date.setHours(10, 0)).toISOString(), endTime: new Date(date.setHours(11, 0)).toISOString(), available: true },
                { startTime: new Date(date.setHours(14, 0)).toISOString(), endTime: new Date(date.setHours(15, 0)).toISOString(), available: true },
                { startTime: new Date(date.setHours(15, 0)).toISOString(), endTime: new Date(date.setHours(16, 0)).toISOString(), available: true },
                { startTime: new Date(date.setHours(16, 0)).toISOString(), endTime: new Date(date.setHours(17, 0)).toISOString(), available: true },
            ]);
            setSlotsError(null); // Clear error since we have mock data
        } finally {
            setIsLoadingSlots(false);
        }
    }, [talentId, serviceDuration]);

    // Handle date selection
    const handleDateSelect = (date: Date) => {
        if (isPastDate(date)) return;
        setSelectedDate(date);
        fetchSlots(date);
    };

    // Handle booking confirmation
    const handleConfirmBooking = async () => {
        if (!selectedDate || !selectedSlot) return;

        setIsBooking(true);

        try {
            // TODO: Real API call to create booking
            await new Promise(resolve => setTimeout(resolve, 1500));

            const booking: BookingData = {
                talentId,
                date: formatDateISO(selectedDate),
                startTime: selectedSlot.startTime,
                endTime: selectedSlot.endTime,
                price: servicePrice,
            };

            toast.success('Réservation confirmée !', {
                description: `Votre séance avec ${talentName} est confirmée.`,
            });

            // Show success state with AddToCalendar option
            setBookingConfirmed(true);
            onBookingComplete?.(booking);
        } catch (error) {
            toast.error('Erreur lors de la réservation');
        } finally {
            setIsBooking(false);
        }
    };

    // Helper to create CalendarEvent from booking
    const getCalendarEventFromBooking = (): CalendarEvent | null => {
        if (!selectedDate || !selectedSlot) return null;
        
        return {
            title: `${serviceName} avec ${talentName}`,
            description: `Séance de ${serviceDuration} minutes\nPrix: ${servicePrice}€\n\nMerci pour votre réservation sur SocioPulse !`,
            location: 'Visio-conférence', // Can be updated based on service type
            startDate: new Date(selectedSlot.startTime),
            endDate: new Date(selectedSlot.endTime),
            organizer: talentName,
        };
    };

    // Check if day has availability (simplified check using availableDays)
    const dayHasAvailability = (date: Date): boolean => {
        // Monday = 1, Sunday = 0 (JS getDay()), but we use Monday = 1, Sunday = 7 style
        const dayOfWeek = date.getDay();
        return availableDays.includes(dayOfWeek);
    };

    return (
        <div className={cn('bg-white rounded-2xl border border-slate-200 shadow-lg overflow-hidden', className)}>
            {/* Header */}
            <div className="p-4 sm:p-6 border-b border-slate-100 bg-gradient-to-r from-teal-50 to-white">
                <div className="flex items-center gap-3">
                    <div className="w-10 h-10 rounded-xl bg-teal-100 flex items-center justify-center">
                        <Calendar className="w-5 h-5 text-teal-600" />
                    </div>
                    <div>
                        <h3 className="font-semibold text-slate-900">Réserver une séance</h3>
                        <p className="text-sm text-slate-500">Choisissez une date et un créneau</p>
                    </div>
                </div>
            </div>

            <div className="p-4 sm:p-6">
                {/* Calendar Navigation */}
                <div className="flex items-center justify-between mb-4">
                    <button
                        onClick={goToPrevMonth}
                        className="p-2 hover:bg-slate-100 rounded-lg transition-colors"
                        aria-label="Mois précédent"
                    >
                        <ChevronLeft className="w-5 h-5 text-slate-600" />
                    </button>
                    <h4 className="text-lg font-semibold text-slate-900">
                        {MONTHS_FR[currentMonth]} {currentYear}
                    </h4>
                    <button
                        onClick={goToNextMonth}
                        className="p-2 hover:bg-slate-100 rounded-lg transition-colors"
                        aria-label="Mois suivant"
                    >
                        <ChevronRight className="w-5 h-5 text-slate-600" />
                    </button>
                </div>

                {/* Calendar Grid */}
                <div className="mb-6">
                    {/* Day Headers (Monday first) */}
                    <div className="grid grid-cols-7 gap-1 mb-2">
                        {['Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam', 'Dim'].map((day) => (
                            <div
                                key={day}
                                className="text-center text-xs font-medium text-slate-500 py-2"
                            >
                                {day}
                            </div>
                        ))}
                    </div>

                    {/* Day Cells */}
                    <div className="grid grid-cols-7 gap-1">
                        {calendarDays.map((date, index) => {
                            const isCurrentMonth = date.getMonth() === currentMonth;
                            const isPast = isPastDate(date);
                            const isToday = isSameDay(date, today);
                            const isSelected = selectedDate && isSameDay(date, selectedDate);
                            const hasAvailability = dayHasAvailability(date) && !isPast;

                            return (
                                <button
                                    key={index}
                                    onClick={() => handleDateSelect(date)}
                                    disabled={isPast || !isCurrentMonth}
                                    className={cn(
                                        'aspect-square flex items-center justify-center text-sm rounded-lg transition-all relative',
                                        !isCurrentMonth && 'text-slate-300 cursor-default',
                                        isCurrentMonth && !isPast && 'hover:bg-slate-100 cursor-pointer',
                                        isPast && isCurrentMonth && 'text-slate-300 cursor-not-allowed',
                                        isToday && 'font-bold',
                                        isSelected && 'bg-teal-500 text-white hover:bg-teal-600',
                                        !isSelected && hasAvailability && isCurrentMonth && 'bg-teal-50 text-teal-700 font-medium',
                                    )}
                                >
                                    {date.getDate()}
                                    {hasAvailability && isCurrentMonth && !isSelected && (
                                        <span className="absolute bottom-1 left-1/2 -translate-x-1/2 w-1 h-1 bg-teal-500 rounded-full" />
                                    )}
                                </button>
                            );
                        })}
                    </div>
                </div>

                {/* Time Slots Section */}
                <AnimatePresence mode="wait">
                    {selectedDate && (
                        <motion.div
                            initial={{ opacity: 0, y: 10 }}
                            animate={{ opacity: 1, y: 0 }}
                            exit={{ opacity: 0, y: -10 }}
                            transition={{ duration: 0.2 }}
                            className="border-t border-slate-100 pt-6"
                        >
                            <div className="flex items-center gap-2 mb-4">
                                <Clock className="w-4 h-4 text-slate-500" />
                                <h4 className="font-medium text-slate-700">
                                    Créneaux disponibles le {formatDateDisplay(selectedDate)}
                                </h4>
                            </div>

                            {isLoadingSlots ? (
                                <div className="flex items-center justify-center py-8">
                                    <Loader2 className="w-6 h-6 text-teal-500 animate-spin" />
                                    <span className="ml-2 text-slate-500">Chargement des créneaux...</span>
                                </div>
                            ) : slotsError ? (
                                <div className="flex items-center justify-center py-8 text-rose-500">
                                    <AlertCircle className="w-5 h-5 mr-2" />
                                    {slotsError}
                                </div>
                            ) : slots.length === 0 ? (
                                <div className="text-center py-8 px-4 bg-slate-50 rounded-xl">
                                    <Calendar className="w-10 h-10 text-slate-300 mx-auto mb-3" />
                                    <p className="text-slate-500 font-medium">
                                        Aucun créneau disponible ce jour-là
                                    </p>
                                    <p className="text-sm text-slate-400 mt-1">
                                        Essayez une autre date
                                    </p>
                                </div>
                            ) : (
                                <div className="grid grid-cols-3 sm:grid-cols-4 gap-2">
                                    {slots.map((slot, index) => {
                                        const isSlotSelected = selectedSlot?.startTime === slot.startTime;
                                        return (
                                            <motion.button
                                                key={index}
                                                initial={{ opacity: 0, scale: 0.9 }}
                                                animate={{ opacity: 1, scale: 1 }}
                                                transition={{ delay: index * 0.05 }}
                                                onClick={() => setSelectedSlot(slot)}
                                                className={cn(
                                                    'py-3 px-4 rounded-xl text-sm font-medium transition-all border-2',
                                                    isSlotSelected
                                                        ? 'bg-teal-500 text-white border-teal-500 shadow-lg shadow-teal-500/25'
                                                        : 'bg-white text-slate-700 border-slate-200 hover:border-teal-400 hover:bg-teal-50'
                                                )}
                                            >
                                                {formatTimeDisplay(slot.startTime)}
                                            </motion.button>
                                        );
                                    })}
                                </div>
                            )}
                        </motion.div>
                    )}
                </AnimatePresence>
            </div>

            {/* Confirmation Summary */}
            <AnimatePresence>
                {selectedDate && selectedSlot && (
                    <motion.div
                        initial={{ opacity: 0, height: 0 }}
                        animate={{ opacity: 1, height: 'auto' }}
                        exit={{ opacity: 0, height: 0 }}
                        transition={{ duration: 0.3 }}
                        className="border-t border-slate-200 bg-gradient-to-r from-slate-50 to-teal-50/50 p-4 sm:p-6"
                    >
                        {bookingConfirmed ? (
                            /* Success State with Add to Calendar */
                            <div className="space-y-4">
                                <div className="flex items-center gap-3 p-4 bg-green-50 rounded-xl border border-green-200">
                                    <div className="w-10 h-10 rounded-full bg-green-100 flex items-center justify-center">
                                        <CheckCircle2 className="w-5 h-5 text-green-600" />
                                    </div>
                                    <div>
                                        <h4 className="font-semibold text-green-800">
                                            Réservation confirmée ! 🎉
                                        </h4>
                                        <p className="text-sm text-green-600">
                                            {formatDateDisplay(selectedDate)} à {formatTimeDisplay(selectedSlot.startTime)}
                                        </p>
                                    </div>
                                </div>

                                {/* Add to Calendar Button */}
                                {getCalendarEventFromBooking() && (
                                    <div className="flex flex-col items-center gap-3">
                                        <p className="text-sm text-slate-600">
                                            N'oubliez pas d'ajouter ce rendez-vous à votre agenda !
                                        </p>
                                        <AddToCalendar
                                            event={getCalendarEventFromBooking()!}
                                            variant="dropdown"
                                            size="md"
                                        />
                                    </div>
                                )}

                                {/* Navigate to Dashboard */}
                                <Button
                                    onClick={() => window.location.href = '/dashboard/client/bookings'}
                                    variant="outline"
                                    className="w-full"
                                >
                                    Voir mes réservations
                                </Button>
                            </div>
                        ) : (
                            /* Pre-confirmation State */
                            <div className="space-y-4">
                                {/* Summary */}
                                <div className="flex items-start gap-4">
                                    <div className="w-12 h-12 rounded-full bg-teal-100 flex items-center justify-center flex-shrink-0">
                                        <User className="w-6 h-6 text-teal-600" />
                                    </div>
                                    <div className="flex-1 min-w-0">
                                        <h4 className="font-semibold text-slate-900 truncate">
                                            {serviceName}
                                        </h4>
                                        <p className="text-sm text-slate-600">
                                            avec {talentName}
                                        </p>
                                        <div className="flex items-center gap-2 mt-2 text-sm">
                                            <Calendar className="w-4 h-4 text-teal-600" />
                                            <span className="text-slate-700 font-medium">
                                                {formatDateDisplay(selectedDate)} à {formatTimeDisplay(selectedSlot.startTime)}
                                            </span>
                                        </div>
                                        <div className="flex items-center gap-2 mt-1 text-sm">
                                            <Clock className="w-4 h-4 text-teal-600" />
                                            <span className="text-slate-500">
                                                Durée: {serviceDuration} min
                                            </span>
                                        </div>
                                    </div>
                                    <div className="text-right">
                                        <p className="text-2xl font-bold text-teal-600">
                                            {servicePrice}€
                                        </p>
                                        <p className="text-xs text-slate-500">TTC</p>
                                    </div>
                                </div>

                                {/* Confirm Button */}
                                <Button
                                    onClick={handleConfirmBooking}
                                    disabled={isBooking}
                                    className="w-full h-12 bg-teal-600 hover:bg-teal-700 text-white font-semibold rounded-xl shadow-lg shadow-teal-600/25 transition-all disabled:opacity-50"
                                >
                                    {isBooking ? (
                                        <span className="flex items-center gap-2">
                                            <Loader2 className="w-5 h-5 animate-spin" />
                                            Confirmation en cours...
                                        </span>
                                    ) : (
                                        <span className="flex items-center gap-2">
                                            <CheckCircle2 className="w-5 h-5" />
                                            Confirmer la réservation
                                        </span>
                                    )}
                                </Button>

                                {/* Info */}
                                <p className="text-xs text-center text-slate-500">
                                    En confirmant, vous acceptez les conditions générales de vente
                                </p>
                            </div>
                        )}
                    </motion.div>
                )}
            </AnimatePresence>
        </div>
    );
}

export default BookingCalendar;
