'use client';

import { useState, useMemo } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
    Calendar,
    ChevronLeft,
    ChevronRight,
    Video,
    AlertTriangle,
    Clock,
    MapPin,
    User,
    ExternalLink,
    List,
    Grid3X3,
} from 'lucide-react';
import { Button, Badge } from '@/components/ui';
import { cn } from '@/lib/utils';

// =============================================================================
// TYPES
// =============================================================================

type EventType = 'MISSION' | 'BOOKING' | 'AVAILABLE';

interface CalendarEvent {
    id: string;
    type: EventType;
    title: string;
    date: string; // YYYY-MM-DD
    startTime: string; // HH:MM
    endTime: string;
    status?: string;
    clientName?: string;
    location?: string;
    isUrgent?: boolean;
    liveKitRoom?: string;
    serviceName?: string;
}

interface UnifiedCalendarProps {
    events?: CalendarEvent[];
    onEventClick?: (event: CalendarEvent) => void;
    onJoinSession?: (event: CalendarEvent) => void;
    className?: string;
    userRole?: 'TALENT' | 'CLIENT' | 'ADMIN';
}

// =============================================================================
// MOCK DATA
// =============================================================================

const generateMockEvents = (): CalendarEvent[] => {
    const today = new Date();
    const events: CalendarEvent[] = [];

    // Add some missions (SOS Renfort)
    events.push({
        id: 'm1',
        type: 'MISSION',
        title: 'Aide-soignant(e) - EHPAD Les Mimosas',
        date: new Date(today.getTime() + 1 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
        startTime: '07:00',
        endTime: '15:00',
        status: 'CONFIRMED',
        location: 'Lyon 3ème',
        isUrgent: true,
    });

    events.push({
        id: 'm2',
        type: 'MISSION',
        title: 'Éducateur spécialisé - Foyer Jeunesse',
        date: new Date(today.getTime() + 3 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
        startTime: '09:00',
        endTime: '17:00',
        status: 'PENDING',
        location: 'Villeurbanne',
    });

    // Add some bookings (1-to-1 Coaching)
    events.push({
        id: 'b1',
        type: 'BOOKING',
        title: 'Coaching - Gestion du stress',
        date: new Date(today.getTime() + 2 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
        startTime: '14:00',
        endTime: '15:00',
        status: 'CONFIRMED',
        clientName: 'Sophie Martin',
        serviceName: 'Coaching individuel',
        liveKitRoom: 'room-abc123',
    });

    events.push({
        id: 'b2',
        type: 'BOOKING',
        title: 'Supervision - Analyse de pratique',
        date: new Date(today.getTime() + 4 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
        startTime: '10:00',
        endTime: '11:00',
        status: 'CONFIRMED',
        clientName: 'Pierre Durand',
        serviceName: 'Supervision',
        liveKitRoom: 'room-xyz789',
    });

    events.push({
        id: 'b3',
        type: 'BOOKING',
        title: 'Coaching carrière',
        date: today.toISOString().split('T')[0],
        startTime: '16:00',
        endTime: '17:00',
        status: 'CONFIRMED',
        clientName: 'Marie Lefebvre',
        liveKitRoom: 'room-today123',
    });

    return events;
};

// =============================================================================
// CONSTANTS
// =============================================================================

const DAYS_FR = ['Dim', 'Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam'];
const MONTHS_FR = [
    'Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin',
    'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre'
];

// =============================================================================
// HELPER FUNCTIONS
// =============================================================================

function getDaysInMonth(year: number, month: number): Date[] {
    const days: Date[] = [];
    const firstDay = new Date(year, month, 1);
    const lastDay = new Date(year, month + 1, 0);

    // Monday start
    const startPadding = firstDay.getDay() === 0 ? 6 : firstDay.getDay() - 1;
    for (let i = startPadding; i > 0; i--) {
        days.push(new Date(year, month, 1 - i));
    }

    for (let d = 1; d <= lastDay.getDate(); d++) {
        days.push(new Date(year, month, d));
    }

    const endPadding = 7 - (days.length % 7);
    if (endPadding < 7) {
        for (let i = 1; i <= endPadding; i++) {
            days.push(new Date(year, month + 1, i));
        }
    }

    return days;
}

function isSameDay(date1: Date, date2: Date): boolean {
    return (
        date1.getFullYear() === date2.getFullYear() &&
        date1.getMonth() === date2.getMonth() &&
        date1.getDate() === date2.getDate()
    );
}

function formatDateISO(date: Date): string {
    return date.toISOString().split('T')[0];
}

// =============================================================================
// SUB-COMPONENTS
// =============================================================================

function EventBadge({ event, compact = false }: { event: CalendarEvent; compact?: boolean }) {
    const config = {
        MISSION: {
            bg: event.isUrgent ? 'bg-rose-500' : 'bg-rose-100',
            text: event.isUrgent ? 'text-white' : 'text-rose-700',
            border: 'border-rose-200',
            dot: 'bg-rose-500',
            label: 'Mission',
        },
        BOOKING: {
            bg: 'bg-blue-100',
            text: 'text-blue-700',
            border: 'border-blue-200',
            dot: 'bg-blue-500',
            label: 'Coaching',
        },
        AVAILABLE: {
            bg: 'bg-emerald-100',
            text: 'text-emerald-700',
            border: 'border-emerald-200',
            dot: 'bg-emerald-500',
            label: 'Dispo',
        },
    };

    const style = config[event.type];

    if (compact) {
        return (
            <div className={cn(
                'w-2 h-2 rounded-full',
                style.dot
            )} title={event.title} />
        );
    }

    return (
        <div className={cn(
            'px-2 py-1 rounded text-xs font-medium truncate',
            style.bg,
            style.text
        )}>
            {event.startTime} - {event.title.substring(0, 20)}...
        </div>
    );
}

function EventCard({ event, onJoin }: { event: CalendarEvent; onJoin?: () => void }) {
    const isMission = event.type === 'MISSION';
    const isToday = event.date === formatDateISO(new Date());
    const canJoin = event.type === 'BOOKING' && event.liveKitRoom && isToday;

    return (
        <motion.div
            initial={{ opacity: 0, y: 5 }}
            animate={{ opacity: 1, y: 0 }}
            className={cn(
                'p-3 sm:p-4 rounded-xl border-2 transition-all',
                isMission
                    ? event.isUrgent
                        ? 'border-rose-300 bg-rose-50'
                        : 'border-rose-200 bg-rose-50/50'
                    : 'border-blue-200 bg-blue-50/50'
            )}
        >
            <div className="flex items-start justify-between gap-3">
                <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2 mb-1">
                        {isMission ? (
                            <Badge className={cn(
                                'text-xs',
                                event.isUrgent
                                    ? 'bg-rose-500 text-white'
                                    : 'bg-rose-100 text-rose-700'
                            )}>
                                {event.isUrgent && <AlertTriangle className="w-3 h-3 mr-1" />}
                                Mission SOS
                            </Badge>
                        ) : (
                            <Badge className="bg-blue-100 text-blue-700 text-xs">
                                <Video className="w-3 h-3 mr-1" />
                                Coaching
                            </Badge>
                        )}
                        {event.status === 'PENDING' && (
                            <Badge variant="outline" className="text-xs text-amber-600 border-amber-300">
                                En attente
                            </Badge>
                        )}
                    </div>

                    <h4 className="font-semibold text-slate-900 text-sm sm:text-base truncate">
                        {event.title}
                    </h4>

                    <div className="flex flex-wrap items-center gap-x-3 gap-y-1 mt-2 text-xs sm:text-sm text-slate-500">
                        <span className="flex items-center gap-1">
                            <Clock className="w-3.5 h-3.5" />
                            {event.startTime} - {event.endTime}
                        </span>
                        {event.location && (
                            <span className="flex items-center gap-1">
                                <MapPin className="w-3.5 h-3.5" />
                                {event.location}
                            </span>
                        )}
                        {event.clientName && (
                            <span className="flex items-center gap-1">
                                <User className="w-3.5 h-3.5" />
                                {event.clientName}
                            </span>
                        )}
                    </div>
                </div>

                {canJoin && (
                    <Button
                        onClick={onJoin}
                        size="sm"
                        className="bg-blue-600 hover:bg-blue-700 text-white flex-shrink-0"
                    >
                        <Video className="w-4 h-4 mr-1" />
                        <span className="hidden sm:inline">Rejoindre</span>
                    </Button>
                )}
            </div>
        </motion.div>
    );
}

function StatusLegend() {
    return (
        <div className="flex flex-wrap items-center gap-x-4 gap-y-2 text-xs sm:text-sm text-slate-600">
            <div className="flex items-center gap-1.5">
                <div className="w-3 h-3 rounded-full bg-rose-500" />
                <span>🔴 Mission SOS (Urgent)</span>
            </div>
            <div className="flex items-center gap-1.5">
                <div className="w-3 h-3 rounded-full bg-blue-500" />
                <span>🔵 Coaching 1-to-1</span>
            </div>
            <div className="flex items-center gap-1.5">
                <div className="w-3 h-3 rounded-full bg-emerald-500" />
                <span>⚪ Disponible</span>
            </div>
        </div>
    );
}

// =============================================================================
// MAIN COMPONENT
// =============================================================================

export function UnifiedCalendar({
    events = generateMockEvents(),
    onEventClick,
    onJoinSession,
    className,
    userRole = 'TALENT',
}: UnifiedCalendarProps) {
    const today = new Date();
    const [currentMonth, setCurrentMonth] = useState(today.getMonth());
    const [currentYear, setCurrentYear] = useState(today.getFullYear());
    const [selectedDate, setSelectedDate] = useState<Date>(today);
    const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid');

    const calendarDays = useMemo(() => {
        return getDaysInMonth(currentYear, currentMonth);
    }, [currentYear, currentMonth]);

    const eventsForDate = (date: Date): CalendarEvent[] => {
        const dateStr = formatDateISO(date);
        return events.filter(e => e.date === dateStr);
    };

    const selectedDateEvents = useMemo(() => {
        return eventsForDate(selectedDate);
    }, [selectedDate, events]);

    const upcomingEvents = useMemo(() => {
        const todayStr = formatDateISO(today);
        return events
            .filter(e => e.date >= todayStr)
            .sort((a, b) => {
                if (a.date !== b.date) return a.date.localeCompare(b.date);
                return a.startTime.localeCompare(b.startTime);
            })
            .slice(0, 5);
    }, [events]);

    const goToPrevMonth = () => {
        if (currentMonth === 0) {
            setCurrentMonth(11);
            setCurrentYear(currentYear - 1);
        } else {
            setCurrentMonth(currentMonth - 1);
        }
    };

    const goToNextMonth = () => {
        if (currentMonth === 11) {
            setCurrentMonth(0);
            setCurrentYear(currentYear + 1);
        } else {
            setCurrentMonth(currentMonth + 1);
        }
    };

    const handleJoinSession = (event: CalendarEvent) => {
        if (onJoinSession) {
            onJoinSession(event);
        } else {
            // Default: Navigate to live session
            window.location.href = `/live-session/${event.liveKitRoom}`;
        }
    };

    return (
        <div className={cn('space-y-4', className)}>
            {/* View Toggle (Mobile) */}
            <div className="flex items-center justify-between sm:hidden">
                <h2 className="font-semibold text-slate-900">Agenda</h2>
                <div className="flex bg-slate-100 rounded-lg p-1">
                    <button
                        onClick={() => setViewMode('grid')}
                        className={cn(
                            'p-2 rounded transition-colors',
                            viewMode === 'grid' ? 'bg-white shadow-sm' : 'text-slate-500'
                        )}
                    >
                        <Grid3X3 className="w-4 h-4" />
                    </button>
                    <button
                        onClick={() => setViewMode('list')}
                        className={cn(
                            'p-2 rounded transition-colors',
                            viewMode === 'list' ? 'bg-white shadow-sm' : 'text-slate-500'
                        )}
                    >
                        <List className="w-4 h-4" />
                    </button>
                </div>
            </div>

            {/* Calendar Grid View (Desktop Always, Mobile if grid mode) */}
            <div className={cn(
                'bg-white rounded-2xl border border-slate-200 shadow-sm',
                viewMode === 'list' && 'hidden sm:block'
            )}>
                {/* Navigation */}
                <div className="flex items-center justify-between p-4 border-b border-slate-100">
                    <button
                        onClick={goToPrevMonth}
                        className="p-2 hover:bg-slate-100 rounded-lg transition-colors"
                    >
                        <ChevronLeft className="w-5 h-5 text-slate-600" />
                    </button>
                    <h3 className="text-lg font-semibold text-slate-900">
                        {MONTHS_FR[currentMonth]} {currentYear}
                    </h3>
                    <button
                        onClick={goToNextMonth}
                        className="p-2 hover:bg-slate-100 rounded-lg transition-colors"
                    >
                        <ChevronRight className="w-5 h-5 text-slate-600" />
                    </button>
                </div>

                {/* Days Header */}
                <div className="grid grid-cols-7 border-b border-slate-100">
                    {['Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam', 'Dim'].map(day => (
                        <div key={day} className="py-2 text-center text-xs font-medium text-slate-500">
                            {day}
                        </div>
                    ))}
                </div>

                {/* Calendar Grid */}
                <div className="grid grid-cols-7">
                    {calendarDays.map((date, index) => {
                        const isCurrentMonth = date.getMonth() === currentMonth;
                        const isToday = isSameDay(date, today);
                        const isSelected = isSameDay(date, selectedDate);
                        const dayEvents = eventsForDate(date);
                        const hasMission = dayEvents.some(e => e.type === 'MISSION');
                        const hasBooking = dayEvents.some(e => e.type === 'BOOKING');
                        const hasUrgent = dayEvents.some(e => e.isUrgent);

                        return (
                            <button
                                key={index}
                                onClick={() => setSelectedDate(date)}
                                className={cn(
                                    'aspect-square p-1 border-b border-r border-slate-100 transition-colors relative',
                                    !isCurrentMonth && 'bg-slate-50',
                                    isSelected && 'bg-teal-50',
                                    isToday && !isSelected && 'bg-blue-50',
                                    'hover:bg-slate-100'
                                )}
                            >
                                <div className={cn(
                                    'w-6 h-6 mx-auto rounded-full flex items-center justify-center text-sm',
                                    isToday && 'bg-blue-600 text-white font-bold',
                                    isSelected && !isToday && 'bg-teal-600 text-white font-bold',
                                    !isCurrentMonth && 'text-slate-300'
                                )}>
                                    {date.getDate()}
                                </div>

                                {/* Event Indicators */}
                                {dayEvents.length > 0 && (
                                    <div className="flex justify-center gap-0.5 mt-1">
                                        {hasMission && (
                                            <div className={cn(
                                                'w-1.5 h-1.5 rounded-full',
                                                hasUrgent ? 'bg-rose-500' : 'bg-rose-400'
                                            )} />
                                        )}
                                        {hasBooking && (
                                            <div className="w-1.5 h-1.5 rounded-full bg-blue-500" />
                                        )}
                                    </div>
                                )}
                            </button>
                        );
                    })}
                </div>
            </div>

            {/* Selected Date Events */}
            <div className={cn(
                'bg-white rounded-2xl border border-slate-200 shadow-sm p-4',
                viewMode === 'list' && 'sm:block'
            )}>
                <div className="flex items-center justify-between mb-4">
                    <h3 className="font-semibold text-slate-900">
                        {selectedDate.toLocaleDateString('fr-FR', {
                            weekday: 'long',
                            day: 'numeric',
                            month: 'long',
                        })}
                    </h3>
                    <span className="text-sm text-slate-500">
                        {selectedDateEvents.length} événement(s)
                    </span>
                </div>

                <AnimatePresence mode="wait">
                    {selectedDateEvents.length === 0 ? (
                        <motion.div
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            className="py-8 text-center"
                        >
                            <Calendar className="w-10 h-10 text-slate-300 mx-auto mb-2" />
                            <p className="text-slate-500">Aucun événement ce jour</p>
                        </motion.div>
                    ) : (
                        <motion.div
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            className="space-y-3"
                        >
                            {selectedDateEvents.map(event => (
                                <EventCard
                                    key={event.id}
                                    event={event}
                                    onJoin={() => handleJoinSession(event)}
                                />
                            ))}
                        </motion.div>
                    )}
                </AnimatePresence>
            </div>

            {/* Mobile List View */}
            {viewMode === 'list' && (
                <div className="sm:hidden space-y-3">
                    <h3 className="font-semibold text-slate-900">Prochains événements</h3>
                    {upcomingEvents.map(event => (
                        <EventCard
                            key={event.id}
                            event={event}
                            onJoin={() => handleJoinSession(event)}
                        />
                    ))}
                </div>
            )}

            {/* Status Legend */}
            <StatusLegend />
        </div>
    );
}

export default UnifiedCalendar;
