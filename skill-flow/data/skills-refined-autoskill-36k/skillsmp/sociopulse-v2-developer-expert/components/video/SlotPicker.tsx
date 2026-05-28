'use client';

import { useState, useMemo } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
    ChevronLeft,
    ChevronRight,
    Clock,
    Video,
    Check,
    Calendar
} from 'lucide-react';

interface TimeSlot {
    time: string;
    available: boolean;
}

interface DaySlots {
    date: Date;
    slots: TimeSlot[];
}

interface SlotPickerProps {
    providerId: string;
    providerName: string;
    duration?: number; // in minutes
    price: number;
    onSlotSelect?: (date: Date, time: string) => void;
    onConfirm?: (date: Date, time: string) => void;
}

// Generate mock availability data
function generateMockSlots(startDate: Date, days: number): DaySlots[] {
    const result: DaySlots[] = [];
    const times = ['09:00', '10:00', '11:00', '14:00', '15:00', '16:00', '17:00'];

    for (let i = 0; i < days; i++) {
        const date = new Date(startDate);
        date.setDate(date.getDate() + i);

        // Skip weekends
        if (date.getDay() === 0 || date.getDay() === 6) {
            continue;
        }

        const slots = times.map(time => ({
            time,
            available: Math.random() > 0.3, // 70% chance of being available
        }));

        result.push({ date, slots });
    }

    return result;
}

const DAYS_FR = ['Dim', 'Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam'];
const MONTHS_FR = ['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre'];

export function SlotPicker({
    providerId,
    providerName,
    duration = 60,
    price,
    onSlotSelect,
    onConfirm
}: SlotPickerProps) {
    const [currentWeekStart, setCurrentWeekStart] = useState(() => {
        const today = new Date();
        today.setHours(0, 0, 0, 0);
        return today;
    });

    const [selectedDate, setSelectedDate] = useState<Date | null>(null);
    const [selectedTime, setSelectedTime] = useState<string | null>(null);

    const weekSlots = useMemo(() => {
        return generateMockSlots(currentWeekStart, 14);
    }, [currentWeekStart]);

    const currentWeekSlots = weekSlots.slice(0, 5);

    const navigateWeek = (direction: 'prev' | 'next') => {
        const newDate = new Date(currentWeekStart);
        newDate.setDate(newDate.getDate() + (direction === 'next' ? 7 : -7));

        // Don't go before today
        const today = new Date();
        today.setHours(0, 0, 0, 0);
        if (newDate < today) return;

        setCurrentWeekStart(newDate);
        setSelectedDate(null);
        setSelectedTime(null);
    };

    const handleSlotClick = (date: Date, time: string) => {
        setSelectedDate(date);
        setSelectedTime(time);
        onSlotSelect?.(date, time);
    };

    const handleConfirm = () => {
        if (selectedDate && selectedTime) {
            onConfirm?.(selectedDate, selectedTime);
        }
    };

    const formatDate = (date: Date) => {
        return `${date.getDate()} ${MONTHS_FR[date.getMonth()]}`;
    };

    const isToday = (date: Date) => {
        const today = new Date();
        return date.toDateString() === today.toDateString();
    };

    return (
        <div className="bg-white rounded-2xl shadow-soft overflow-hidden">
            {/* Header */}
            <div className="px-6 py-4 bg-gradient-to-r from-purple-600 to-indigo-600">
                <div className="flex items-center gap-3 text-white mb-2">
                    <Video className="w-5 h-5" />
                    <span className="font-semibold">Consultation Vidéo</span>
                </div>
                <div className="flex items-center justify-between text-white/90">
                    <div className="flex items-center gap-4 text-sm">
                        <span className="flex items-center gap-1">
                            <Clock className="w-4 h-4" />
                            Durée : {duration} min
                        </span>
                        <span className="font-bold text-lg">{price}€</span>
                    </div>
                </div>
            </div>

            {/* Calendar Navigation */}
            <div className="px-6 py-4 border-b border-slate-100">
                <div className="flex items-center justify-between">
                    <button
                        onClick={() => navigateWeek('prev')}
                        className="p-2 rounded-lg hover:bg-slate-100 text-slate-400 hover:text-slate-600 transition-colors disabled:opacity-50"
                        disabled={currentWeekStart <= new Date()}
                    >
                        <ChevronLeft className="w-5 h-5" />
                    </button>

                    <div className="flex items-center gap-2">
                        <Calendar className="w-4 h-4 text-slate-400" />
                        <span className="font-medium text-slate-900">
                            {MONTHS_FR[currentWeekStart.getMonth()]} {currentWeekStart.getFullYear()}
                        </span>
                    </div>

                    <button
                        onClick={() => navigateWeek('next')}
                        className="p-2 rounded-lg hover:bg-slate-100 text-slate-400 hover:text-slate-600 transition-colors"
                    >
                        <ChevronRight className="w-5 h-5" />
                    </button>
                </div>
            </div>

            {/* Days Grid */}
            <div className="px-6 py-4">
                <div className="grid grid-cols-5 gap-2 mb-4">
                    {currentWeekSlots.map((daySlot, index) => {
                        const isSelected = selectedDate?.toDateString() === daySlot.date.toDateString();
                        const hasAvailable = daySlot.slots.some(s => s.available);

                        return (
                            <button
                                key={index}
                                onClick={() => hasAvailable && setSelectedDate(daySlot.date)}
                                disabled={!hasAvailable}
                                className={`
                  py-3 px-2 rounded-xl text-center transition-all
                  ${isSelected
                                        ? 'bg-purple-600 text-white shadow-lg shadow-purple-500/30'
                                        : hasAvailable
                                            ? 'bg-slate-50 text-slate-900 hover:bg-purple-50 hover:text-purple-600'
                                            : 'bg-slate-50 text-slate-300 cursor-not-allowed'
                                    }
                `}
                            >
                                <div className="text-xs font-medium opacity-70">
                                    {DAYS_FR[daySlot.date.getDay()]}
                                </div>
                                <div className="text-lg font-bold">
                                    {daySlot.date.getDate()}
                                </div>
                                {isToday(daySlot.date) && (
                                    <div className="text-[10px] font-medium mt-0.5">
                                        Auj.
                                    </div>
                                )}
                            </button>
                        );
                    })}
                </div>

                {/* Time Slots */}
                <AnimatePresence mode="wait">
                    {selectedDate && (
                        <motion.div
                            key={selectedDate.toISOString()}
                            initial={{ opacity: 0, height: 0 }}
                            animate={{ opacity: 1, height: 'auto' }}
                            exit={{ opacity: 0, height: 0 }}
                            className="space-y-3"
                        >
                            <p className="text-sm text-slate-500">
                                Créneaux disponibles le {formatDate(selectedDate)}
                            </p>

                            <div className="grid grid-cols-3 sm:grid-cols-4 gap-2">
                                {currentWeekSlots
                                    .find(d => d.date.toDateString() === selectedDate.toDateString())
                                    ?.slots.filter(s => s.available)
                                    .map((slot) => {
                                        const isSelected = selectedTime === slot.time;

                                        return (
                                            <motion.button
                                                key={slot.time}
                                                whileHover={{ scale: 1.02 }}
                                                whileTap={{ scale: 0.98 }}
                                                onClick={() => handleSlotClick(selectedDate, slot.time)}
                                                className={`
                          py-2.5 px-3 rounded-lg text-sm font-medium transition-all
                          ${isSelected
                                                        ? 'bg-purple-600 text-white shadow-md shadow-purple-500/30'
                                                        : 'bg-slate-100 text-slate-700 hover:bg-purple-100 hover:text-purple-700'
                                                    }
                        `}
                                            >
                                                {slot.time}
                                            </motion.button>
                                        );
                                    })}
                            </div>
                        </motion.div>
                    )}
                </AnimatePresence>
            </div>

            {/* Selected Summary & CTA */}
            <AnimatePresence>
                {selectedDate && selectedTime && (
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0, y: 20 }}
                        className="px-6 py-4 bg-slate-50 border-t border-slate-100"
                    >
                        <div className="flex items-center justify-between mb-4">
                            <div>
                                <p className="text-sm text-slate-500">Votre rendez-vous</p>
                                <p className="font-semibold text-slate-900">
                                    {formatDate(selectedDate)} à {selectedTime}
                                </p>
                            </div>
                            <div className="text-right">
                                <p className="text-sm text-slate-500">Total</p>
                                <p className="text-xl font-bold text-slate-900">{price}€</p>
                            </div>
                        </div>

                        <motion.button
                            whileHover={{ scale: 1.02 }}
                            whileTap={{ scale: 0.98 }}
                            onClick={handleConfirm}
                            className="w-full py-3.5 rounded-xl bg-gradient-to-r from-purple-600 to-indigo-600 text-white font-semibold shadow-lg shadow-purple-500/30 flex items-center justify-center gap-2"
                        >
                            <Check className="w-5 h-5" />
                            Confirmer le rendez-vous
                        </motion.button>

                        <p className="text-xs text-slate-400 text-center mt-3">
                            Paiement sécurisé • Annulation gratuite jusqu'à 24h avant
                        </p>
                    </motion.div>
                )}
            </AnimatePresence>
        </div>
    );
}
