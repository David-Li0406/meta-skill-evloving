'use client';

import { useState } from 'react';
import {
    Calendar,
    Clock,
    Settings,
    LayoutGrid,
    ChevronLeft,
    ChevronRight,
    Check,
    X,
    Repeat,
    Copy,
    Sun,
    Moon,
    Coffee,
    AlertCircle,
    Plus,
} from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle, Button, Badge } from '@/components/ui';
import { AvailabilityManager, UnifiedCalendar } from '@/components/planning';
import { cn } from '@/lib/utils';

// =============================================================================
// TYPES
// =============================================================================

type SlotType = 'AVAILABLE' | 'BOOKED' | 'BLOCKED';

interface TimeSlot {
    id: string;
    date: string;
    startTime: string;
    endTime: string;
    type: SlotType;
    serviceId?: string;
    serviceName?: string;
    isRecurring?: boolean;
}

interface DaySchedule {
    date: string;
    dayName: string;
    dayNumber: number;
    isToday: boolean;
    slots: TimeSlot[];
}

// =============================================================================
// MOCK DATA
// =============================================================================

const generateWeekDays = (): DaySchedule[] => {
    const days: DaySchedule[] = [];
    const today = new Date();
    const dayNames = ['Dim', 'Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam'];

    for (let i = 0; i < 7; i++) {
        const date = new Date(today);
        date.setDate(today.getDate() + i);
        const dateStr = date.toISOString().split('T')[0];

        const slots: TimeSlot[] = [];

        // Add some mock slots
        if (i === 0) {
            slots.push({ id: '1', date: dateStr, startTime: '09:00', endTime: '12:00', type: 'AVAILABLE' });
            slots.push({ id: '2', date: dateStr, startTime: '14:00', endTime: '17:00', type: 'BOOKED', serviceId: 's1', serviceName: 'Coaching Carrière' });
        } else if (i === 1) {
            slots.push({ id: '3', date: dateStr, startTime: '08:00', endTime: '16:00', type: 'AVAILABLE', isRecurring: true });
        } else if (i === 2) {
            slots.push({ id: '4', date: dateStr, startTime: '10:00', endTime: '12:00', type: 'BOOKED', serviceId: 's2', serviceName: 'Atelier Stress' });
            slots.push({ id: '5', date: dateStr, startTime: '14:00', endTime: '18:00', type: 'AVAILABLE' });
        } else if (i === 4) {
            slots.push({ id: '6', date: dateStr, startTime: '09:00', endTime: '18:00', type: 'BLOCKED' });
        } else if (i === 5) {
            slots.push({ id: '7', date: dateStr, startTime: '09:00', endTime: '13:00', type: 'AVAILABLE', isRecurring: true });
        }

        days.push({
            date: dateStr,
            dayName: dayNames[date.getDay()],
            dayNumber: date.getDate(),
            isToday: i === 0,
            slots,
        });
    }

    return days;
};

const quickSlots = [
    { label: 'Matin', icon: Sun, start: '08:00', end: '12:00' },
    { label: 'Après-midi', icon: Coffee, start: '14:00', end: '18:00' },
    { label: 'Journée', icon: Clock, start: '08:00', end: '18:00' },
    { label: 'Soirée', icon: Moon, start: '18:00', end: '21:00' },
];

// =============================================================================
// COMPONENTS
// =============================================================================

function SlotTypeBadge({ type }: { type: SlotType }) {
    const config = {
        AVAILABLE: { label: 'Disponible', className: 'bg-emerald-100 text-emerald-700' },
        BOOKED: { label: 'Réservé', className: 'bg-blue-100 text-blue-700' },
        BLOCKED: { label: 'Bloqué', className: 'bg-slate-100 text-slate-600' },
    };

    const { label, className } = config[type];

    return (
        <span className={cn('px-2 py-0.5 text-xs font-semibold rounded-full', className)}>
            {label}
        </span>
    );
}

function TimeSlotCard({ slot, onEdit, onDelete }: { slot: TimeSlot; onEdit?: () => void; onDelete?: () => void }) {
    const typeStyles = {
        AVAILABLE: 'border-emerald-200 bg-emerald-50/50 hover:border-emerald-300',
        BOOKED: 'border-blue-200 bg-blue-50/50',
        BLOCKED: 'border-slate-200 bg-slate-50/50 opacity-60',
    };

    return (
        <div className={cn(
            'p-3 rounded-xl border-2 transition-all',
            typeStyles[slot.type]
        )}>
            <div className="flex items-start justify-between">
                <div>
                    <div className="flex items-center gap-2">
                        <Clock size={14} className="text-slate-400" />
                        <span className="font-semibold text-slate-900 text-sm">
                            {slot.startTime} - {slot.endTime}
                        </span>
                        {slot.isRecurring && (
                            <span title="Récurrent">
                                <Repeat size={12} className="text-indigo-500" />
                            </span>
                        )}
                    </div>
                    {slot.serviceName && (
                        <p className="text-xs text-blue-600 mt-1 font-medium">{slot.serviceName}</p>
                    )}
                </div>
                <div className="flex items-center gap-1">
                    <SlotTypeBadge type={slot.type} />
                    {slot.type === 'AVAILABLE' && (
                        <button
                            onClick={onDelete}
                            className="p-1 hover:bg-rose-100 rounded text-slate-400 hover:text-rose-500 transition-colors"
                        >
                            <X size={14} />
                        </button>
                    )}
                </div>
            </div>
        </div>
    );
}

function DayColumn({ day, onAddSlot }: { day: DaySchedule; onAddSlot: (date: string) => void }) {
    return (
        <div className={cn(
            'flex-1 min-w-[140px] rounded-xl p-3 transition-colors',
            day.isToday ? 'bg-primary-50 ring-2 ring-primary-200' : 'bg-slate-50'
        )}>
            {/* Day Header */}
            <div className="text-center mb-3">
                <p className={cn(
                    'text-xs font-semibold uppercase',
                    day.isToday ? 'text-primary-600' : 'text-slate-500'
                )}>
                    {day.dayName}
                </p>
                <p className={cn(
                    'text-2xl font-bold',
                    day.isToday ? 'text-primary-700' : 'text-slate-900'
                )}>
                    {day.dayNumber}
                </p>
                {day.isToday && (
                    <span className="inline-block px-2 py-0.5 text-[10px] font-bold bg-primary-600 text-white rounded-full mt-1">
                        Aujourd'hui
                    </span>
                )}
            </div>

            {/* Slots */}
            <div className="space-y-2">
                {day.slots.length === 0 ? (
                    <div className="py-6 text-center">
                        <p className="text-xs text-slate-400 mb-2">Aucun créneau</p>
                        <button
                            onClick={() => onAddSlot(day.date)}
                            className="p-2 bg-white border border-dashed border-slate-300 rounded-lg hover:border-teal-400 hover:bg-teal-50 transition-colors group"
                        >
                            <Plus size={16} className="text-slate-400 group-hover:text-teal-500" />
                        </button>
                    </div>
                ) : (
                    <>
                        {day.slots.map((slot) => (
                            <TimeSlotCard key={slot.id} slot={slot} />
                        ))}
                        <button
                            onClick={() => onAddSlot(day.date)}
                            className="w-full py-2 border border-dashed border-slate-300 rounded-lg text-slate-400 hover:border-teal-400 hover:text-teal-500 hover:bg-teal-50 transition-colors flex items-center justify-center gap-1 text-xs"
                        >
                            <Plus size={12} /> Ajouter
                        </button>
                    </>
                )}
            </div>
        </div>
    );
}

function AddSlotModal({ date, onClose, onAdd }: { date: string; onClose: () => void; onAdd: (slot: Partial<TimeSlot>) => void }) {
    const [startTime, setStartTime] = useState('09:00');
    const [endTime, setEndTime] = useState('17:00');
    const [isRecurring, setIsRecurring] = useState(false);

    const handleQuickSlot = (start: string, end: string) => {
        setStartTime(start);
        setEndTime(end);
    };

    return (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
            <Card className="w-full max-w-md">
                <CardHeader className="pb-3">
                    <div className="flex items-center justify-between">
                        <CardTitle className="text-lg">Ajouter un créneau</CardTitle>
                        <button onClick={onClose} className="p-1 hover:bg-slate-100 rounded">
                            <X size={18} />
                        </button>
                    </div>
                    <p className="text-sm text-slate-500">{new Date(date).toLocaleDateString('fr-FR', { weekday: 'long', day: 'numeric', month: 'long' })}</p>
                </CardHeader>
                <CardContent className="space-y-4">
                    {/* Quick Slots */}
                    <div>
                        <p className="text-xs font-semibold text-slate-500 mb-2 uppercase">Raccourcis</p>
                        <div className="grid grid-cols-4 gap-2">
                            {quickSlots.map((qs) => (
                                <button
                                    key={qs.label}
                                    onClick={() => handleQuickSlot(qs.start, qs.end)}
                                    className="p-2 bg-slate-100 hover:bg-teal-100 rounded-lg transition-colors text-center"
                                >
                                    <qs.icon size={16} className="mx-auto text-slate-600 mb-1" />
                                    <span className="text-xs font-medium text-slate-700">{qs.label}</span>
                                </button>
                            ))}
                        </div>
                    </div>

                    {/* Time Inputs */}
                    <div className="grid grid-cols-2 gap-4">
                        <div>
                            <label className="text-xs font-semibold text-slate-500 mb-1 block">Début</label>
                            <input
                                type="time"
                                value={startTime}
                                onChange={(e) => setStartTime(e.target.value)}
                                className="w-full px-3 py-2 border border-slate-200 rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-teal-500"
                            />
                        </div>
                        <div>
                            <label className="text-xs font-semibold text-slate-500 mb-1 block">Fin</label>
                            <input
                                type="time"
                                value={endTime}
                                onChange={(e) => setEndTime(e.target.value)}
                                className="w-full px-3 py-2 border border-slate-200 rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-teal-500"
                            />
                        </div>
                    </div>

                    {/* Recurring Toggle */}
                    <div className="flex items-center justify-between p-3 bg-slate-50 rounded-xl">
                        <div className="flex items-center gap-2">
                            <Repeat size={16} className="text-indigo-500" />
                            <span className="text-sm font-medium text-slate-700">Répéter chaque semaine</span>
                        </div>
                        <button
                            onClick={() => setIsRecurring(!isRecurring)}
                            className={cn(
                                'w-10 h-5 rounded-full transition-colors relative',
                                isRecurring ? 'bg-indigo-500' : 'bg-slate-300'
                            )}
                        >
                            <span className={cn(
                                'absolute top-0.5 w-4 h-4 bg-white rounded-full transition-all',
                                isRecurring ? 'left-5' : 'left-0.5'
                            )} />
                        </button>
                    </div>

                    {/* Actions */}
                    <div className="flex gap-3 pt-2">
                        <Button variant="outline" className="flex-1" onClick={onClose}>
                            Annuler
                        </Button>
                        <Button
                            className="flex-1 bg-teal-600 hover:bg-teal-700 text-white"
                            onClick={() => {
                                onAdd({ date, startTime, endTime, type: 'AVAILABLE', isRecurring });
                                onClose();
                            }}
                        >
                            <Check size={16} className="mr-1" /> Ajouter
                        </Button>
                    </div>
                </CardContent>
            </Card>
        </div>
    );
}

// =============================================================================
// PAGE
// =============================================================================

type TabView = 'calendar' | 'availability' | 'slots';

export default function TalentPlanningPage() {
    const [activeTab, setActiveTab] = useState<TabView>('calendar');
    const [weekDays, setWeekDays] = useState<DaySchedule[]>(generateWeekDays());
    const [selectedDate, setSelectedDate] = useState<string | null>(null);
    const [weekOffset, setWeekOffset] = useState(0);

    const stats = {
        availableSlots: weekDays.reduce((sum, d) => sum + d.slots.filter(s => s.type === 'AVAILABLE').length, 0),
        bookedSlots: weekDays.reduce((sum, d) => sum + d.slots.filter(s => s.type === 'BOOKED').length, 0),
        totalHours: weekDays.reduce((sum, d) => {
            return sum + d.slots.filter(s => s.type === 'AVAILABLE').reduce((h, slot) => {
                const [startH] = slot.startTime.split(':').map(Number);
                const [endH] = slot.endTime.split(':').map(Number);
                return h + (endH - startH);
            }, 0);
        }, 0),
    };

    const handleAddSlot = (slot: Partial<TimeSlot>) => {
        // In real app, this would call an API
        console.log('Adding slot:', slot);
    };

    return (
        <div className="space-y-6 max-w-7xl mx-auto">
            {/* Header */}
            <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
                <div>
                    <h1 className="text-2xl font-bold text-slate-900 flex items-center gap-2">
                        <Calendar className="text-primary-500" />
                        Mon Planning
                    </h1>
                    <p className="text-slate-500 mt-1">Gérez vos missions et séances de coaching</p>
                </div>
            </div>

            {/* Tab Navigation */}
            <div className="flex gap-1 p-1 bg-slate-100 rounded-xl w-fit">
                <button
                    onClick={() => setActiveTab('calendar')}
                    className={cn(
                        'px-4 py-2 rounded-lg text-sm font-medium transition-all flex items-center gap-2',
                        activeTab === 'calendar'
                            ? 'bg-white shadow-sm text-slate-900'
                            : 'text-slate-500 hover:text-slate-700'
                    )}
                >
                    <LayoutGrid size={16} />
                    Agenda
                </button>
                <button
                    onClick={() => setActiveTab('availability')}
                    className={cn(
                        'px-4 py-2 rounded-lg text-sm font-medium transition-all flex items-center gap-2',
                        activeTab === 'availability'
                            ? 'bg-white shadow-sm text-slate-900'
                            : 'text-slate-500 hover:text-slate-700'
                    )}
                >
                    <Settings size={16} />
                    Horaires de travail
                </button>
                <button
                    onClick={() => setActiveTab('slots')}
                    className={cn(
                        'px-4 py-2 rounded-lg text-sm font-medium transition-all flex items-center gap-2',
                        activeTab === 'slots'
                            ? 'bg-white shadow-sm text-slate-900'
                            : 'text-slate-500 hover:text-slate-700'
                    )}
                >
                    <Clock size={16} />
                    Créneaux
                </button>
            </div>

            {/* TAB: Calendar View (Unified) */}
            {activeTab === 'calendar' && (
                <UnifiedCalendar
                    onJoinSession={(event) => {
                        if (event.liveKitRoom) {
                            window.location.href = `/live-session/${event.liveKitRoom}`;
                        }
                    }}
                />
            )}

            {/* TAB: Availability Settings */}
            {activeTab === 'availability' && (
                <AvailabilityManager />
            )}

            {/* TAB: Slot Management (Original View) */}
            {activeTab === 'slots' && (
                <>
                    {/* Stats */}
                    <div className="grid grid-cols-3 gap-4">
                <Card className="border-emerald-200 bg-emerald-50/50">
                    <CardContent className="p-4 flex items-center gap-3">
                        <div className="p-2 bg-emerald-100 rounded-lg">
                            <Check size={18} className="text-emerald-600" />
                        </div>
                        <div>
                            <p className="text-2xl font-bold text-emerald-700">{stats.availableSlots}</p>
                            <p className="text-xs text-emerald-600">Créneaux disponibles</p>
                        </div>
                    </CardContent>
                </Card>
                <Card className="border-blue-200 bg-blue-50/50">
                    <CardContent className="p-4 flex items-center gap-3">
                        <div className="p-2 bg-blue-100 rounded-lg">
                            <Calendar size={18} className="text-blue-600" />
                        </div>
                        <div>
                            <p className="text-2xl font-bold text-blue-700">{stats.bookedSlots}</p>
                            <p className="text-xs text-blue-600">Réservations</p>
                        </div>
                    </CardContent>
                </Card>
                <Card className="border-slate-200">
                    <CardContent className="p-4 flex items-center gap-3">
                        <div className="p-2 bg-slate-100 rounded-lg">
                            <Clock size={18} className="text-slate-600" />
                        </div>
                        <div>
                            <p className="text-2xl font-bold text-slate-700">{stats.totalHours}h</p>
                            <p className="text-xs text-slate-500">Disponibles cette semaine</p>
                        </div>
                    </CardContent>
                </Card>
            </div>

            {/* Week Navigation */}
            <Card className="border-slate-200">
                <CardContent className="p-4">
                    <div className="flex items-center justify-between mb-4">
                        <button
                            onClick={() => setWeekOffset(weekOffset - 1)}
                            className="p-2 hover:bg-slate-100 rounded-lg transition-colors"
                        >
                            <ChevronLeft size={20} />
                        </button>
                        <div className="text-center">
                            <h2 className="font-semibold text-slate-900">
                                Semaine du {weekDays[0]?.dayNumber} au {weekDays[6]?.dayNumber}
                            </h2>
                            <p className="text-sm text-slate-500">Janvier 2026</p>
                        </div>
                        <button
                            onClick={() => setWeekOffset(weekOffset + 1)}
                            className="p-2 hover:bg-slate-100 rounded-lg transition-colors"
                            aria-label="Semaine suivante"
                        >
                            <ChevronRight size={20} />
                        </button>
                    </div>

                    {/* Week Grid */}
                    <div className="flex gap-3 overflow-x-auto pb-2">
                        {weekDays.map((day) => (
                            <DayColumn
                                key={day.date}
                                day={day}
                                onAddSlot={(date) => setSelectedDate(date)}
                            />
                        ))}
                    </div>
                </CardContent>
            </Card>

            {/* Legend */}
            <div className="flex items-center gap-6 text-sm text-slate-600">
                <div className="flex items-center gap-2">
                    <div className="w-3 h-3 bg-emerald-400 rounded-full" />
                    <span>Disponible</span>
                </div>
                <div className="flex items-center gap-2">
                    <div className="w-3 h-3 bg-blue-400 rounded-full" />
                    <span>Réservé</span>
                </div>
                <div className="flex items-center gap-2">
                    <div className="w-3 h-3 bg-slate-300 rounded-full" />
                    <span>Bloqué</span>
                </div>
                <div className="flex items-center gap-2">
                    <Repeat size={14} className="text-indigo-500" />
                    <span>Récurrent</span>
                </div>
            </div>

            {/* Info Box */}
            <Card className="border-amber-200 bg-amber-50/50">
                <CardContent className="p-4 flex items-start gap-3">
                    <AlertCircle size={20} className="text-amber-600 flex-shrink-0 mt-0.5" />
                    <div>
                        <h3 className="font-semibold text-amber-800">Note importante</h3>
                        <p className="text-sm text-amber-700 mt-1">
                            Ces créneaux concernent uniquement vos <strong>Services Marketplace</strong> (Ateliers & Coaching).
                            Votre disponibilité pour les <strong>Missions SOS</strong> est gérée via le toggle "Renfort Immédiat" dans l'en-tête.
                        </p>
                    </div>
                </CardContent>
            </Card>

            {/* Add Slot Modal */}
            {selectedDate && (
                <AddSlotModal
                    date={selectedDate}
                    onClose={() => setSelectedDate(null)}
                    onAdd={handleAddSlot}
                />
            )}
                </>
            )}
        </div>
    );
}
