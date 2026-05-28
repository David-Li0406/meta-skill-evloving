'use client';

import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
    Clock,
    Calendar,
    Save,
    Plus,
    Trash2,
    Check,
    AlertCircle,
    Loader2,
    Info,
} from 'lucide-react';
import { Button, Badge } from '@/components/ui';
import { toast } from 'sonner';
import { cn } from '@/lib/utils';
import { useAuth } from '@/lib/useAuth';
import {
    getWeekSlots,
    buildSlotsFromWeeklyConfig,
    bulkUpsertAvailabilitySlots,
    type TimeSlot,
} from '@/lib/availability';

// =============================================================================
// TYPES
// =============================================================================

interface WorkingHours {
    dayOfWeek: number;
    startTime: string;
    endTime: string;
    isActive: boolean;
}

interface AvailabilityManagerProps {
    talentId?: string;
    profileId?: string;
    initialConfig?: WorkingHours[];
    onSave?: (config: WorkingHours[]) => Promise<void>;
    className?: string;
}

// =============================================================================
// CONSTANTS
// =============================================================================

const DAYS_FR = [
    { dayOfWeek: 1, label: 'Lundi', short: 'Lun' },
    { dayOfWeek: 2, label: 'Mardi', short: 'Mar' },
    { dayOfWeek: 3, label: 'Mercredi', short: 'Mer' },
    { dayOfWeek: 4, label: 'Jeudi', short: 'Jeu' },
    { dayOfWeek: 5, label: 'Vendredi', short: 'Ven' },
    { dayOfWeek: 6, label: 'Samedi', short: 'Sam' },
    { dayOfWeek: 0, label: 'Dimanche', short: 'Dim' },
];

const DEFAULT_CONFIG: WorkingHours[] = [
    { dayOfWeek: 1, startTime: '09:00', endTime: '18:00', isActive: true },
    { dayOfWeek: 2, startTime: '09:00', endTime: '18:00', isActive: true },
    { dayOfWeek: 3, startTime: '09:00', endTime: '18:00', isActive: true },
    { dayOfWeek: 4, startTime: '09:00', endTime: '18:00', isActive: true },
    { dayOfWeek: 5, startTime: '09:00', endTime: '18:00', isActive: true },
    { dayOfWeek: 6, startTime: '09:00', endTime: '13:00', isActive: false },
    { dayOfWeek: 0, startTime: '09:00', endTime: '13:00', isActive: false },
];

const TIME_OPTIONS = [
    '06:00', '07:00', '08:00', '09:00', '10:00', '11:00', '12:00',
    '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', '22:00',
];

const toTimeString = (value: string) => {
    const parsed = new Date(value);
    if (Number.isNaN(parsed.getTime())) return value.slice(0, 5);
    const hours = String(parsed.getHours()).padStart(2, '0');
    const minutes = String(parsed.getMinutes()).padStart(2, '0');
    return `${hours}:${minutes}`;
};

const buildConfigFromWeekSlots = (slotsByDate: Record<string, TimeSlot[]>) => {
    const base = DEFAULT_CONFIG.map((day) => ({ ...day, isActive: false }));
    const ranges: Record<number, { start: string; end: string }> = {};

    Object.values(slotsByDate || {}).forEach((slots) => {
        slots.forEach((slot) => {
            const start = toTimeString(slot.startTime);
            const end = toTimeString(slot.endTime);
            const dayOfWeek = new Date(slot.startTime).getDay();
            const existing = ranges[dayOfWeek];

            if (!existing) {
                ranges[dayOfWeek] = { start, end };
                return;
            }

            if (start < existing.start) existing.start = start;
            if (end > existing.end) existing.end = end;
        });
    });

    return base.map((day) => {
        const range = ranges[day.dayOfWeek];
        if (!range) return day;
        return {
            ...day,
            startTime: range.start,
            endTime: range.end,
            isActive: true,
        };
    });
};

// =============================================================================
// COMPONENT
// =============================================================================

export function AvailabilityManager({
    talentId,
    profileId,
    initialConfig,
    onSave,
    className,
}: AvailabilityManagerProps) {
    const { user } = useAuth();
    const resolvedTalentId = talentId || user?.id;
    const resolvedProfileId = profileId || user?.profile?.id;
    const [config, setConfig] = useState<WorkingHours[]>(initialConfig || DEFAULT_CONFIG);
    const [baselineConfig, setBaselineConfig] = useState<WorkingHours[]>(initialConfig || DEFAULT_CONFIG);
    const [isLoading, setIsLoading] = useState(false);
    const [isSaving, setIsSaving] = useState(false);
    const [hasChanges, setHasChanges] = useState(false);

    // Track changes
    useEffect(() => {
        const original = JSON.stringify(baselineConfig);
        const current = JSON.stringify(config);
        setHasChanges(original !== current);
    }, [config, baselineConfig]);

    useEffect(() => {
        if (!initialConfig) return;
        setConfig(initialConfig);
        setBaselineConfig(initialConfig);
    }, [initialConfig]);

    useEffect(() => {
        if (!resolvedTalentId || initialConfig) return;

        let cancelled = false;

        const loadWeek = async () => {
            setIsLoading(true);
            try {
                const week = await getWeekSlots(resolvedTalentId);
                if (cancelled) return;
                const nextConfig = buildConfigFromWeekSlots(week.slotsByDate);
                setConfig(nextConfig);
                setBaselineConfig(nextConfig);
            } catch (error) {
                console.error('Failed to load availability week:', error);
                toast.error('Impossible de charger vos disponibilités');
            } finally {
                if (!cancelled) {
                    setIsLoading(false);
                }
            }
        };

        loadWeek();

        return () => {
            cancelled = true;
        };
    }, [resolvedTalentId, initialConfig]);

    const toggleDay = (dayOfWeek: number) => {
        setConfig(prev => prev.map(day =>
            day.dayOfWeek === dayOfWeek
                ? { ...day, isActive: !day.isActive }
                : day
        ));
    };

    const updateTime = (dayOfWeek: number, field: 'startTime' | 'endTime', value: string) => {
        setConfig(prev => prev.map(day =>
            day.dayOfWeek === dayOfWeek
                ? { ...day, [field]: value }
                : day
        ));
    };

    const handleSave = async () => {
        setIsSaving(true);
        try {
            if (onSave) {
                await onSave(config);
            } else {
                if (!resolvedProfileId) {
                    throw new Error('Profil introuvable');
                }

                const slots = buildSlotsFromWeeklyConfig(config);
                await bulkUpsertAvailabilitySlots({
                    profileId: resolvedProfileId,
                    slots,
                    replaceExisting: true,
                });
            }

            toast.success('Disponibilités enregistrées !', {
                description: 'Vos horaires de travail ont été mis à jour.',
            });
            setBaselineConfig(config);
            setHasChanges(false);
        } catch (error) {
            toast.error('Erreur lors de la sauvegarde');
        } finally {
            setIsSaving(false);
        }
    };

    const copyToAll = (dayOfWeek: number) => {
        const sourceDay = config.find(d => d.dayOfWeek === dayOfWeek);
        if (!sourceDay) return;

        setConfig(prev => prev.map(day => ({
            ...day,
            startTime: sourceDay.startTime,
            endTime: sourceDay.endTime,
            isActive: day.dayOfWeek === 0 || day.dayOfWeek === 6 ? day.isActive : true,
        })));

        toast.success('Horaires copiés sur tous les jours actifs');
    };

    const applyPreset = (preset: 'weekdays' | 'fullweek' | 'mornings') => {
        switch (preset) {
            case 'weekdays':
                setConfig(prev => prev.map(day => ({
                    ...day,
                    startTime: '09:00',
                    endTime: '18:00',
                    isActive: day.dayOfWeek >= 1 && day.dayOfWeek <= 5,
                })));
                break;
            case 'fullweek':
                setConfig(prev => prev.map(day => ({
                    ...day,
                    startTime: '09:00',
                    endTime: '18:00',
                    isActive: true,
                })));
                break;
            case 'mornings':
                setConfig(prev => prev.map(day => ({
                    ...day,
                    startTime: '08:00',
                    endTime: '13:00',
                    isActive: day.dayOfWeek >= 1 && day.dayOfWeek <= 5,
                })));
                break;
        }
    };

    const totalHours = config
        .filter(d => d.isActive)
        .reduce((sum, day) => {
            const [startH] = day.startTime.split(':').map(Number);
            const [endH] = day.endTime.split(':').map(Number);
            return sum + Math.max(0, endH - startH);
        }, 0);

    const activeDays = config.filter(d => d.isActive).length;

    return (
        <div className={cn('bg-white rounded-2xl border border-slate-200 shadow-sm', className)}>
            {/* Header */}
            <div className="p-4 sm:p-6 border-b border-slate-100">
                <div className="flex items-center justify-between">
                    <div className="flex items-center gap-3">
                        <div className="w-10 h-10 rounded-xl bg-teal-100 flex items-center justify-center">
                            <Clock className="w-5 h-5 text-teal-600" />
                        </div>
                        <div>
                            <h3 className="font-semibold text-slate-900">Horaires de travail</h3>
                            <p className="text-sm text-slate-500">Définissez vos plages de disponibilité</p>
                        </div>
                    </div>
                    <div className="flex items-center gap-2">
                        {isLoading && (
                            <Badge variant="outline">Chargement...</Badge>
                        )}
                        <Badge variant="outline" className="hidden sm:flex">
                            {activeDays} jours · {totalHours}h/sem
                        </Badge>
                    </div>
                </div>
            </div>

            {/* Quick Presets */}
            <div className="px-4 sm:px-6 py-3 bg-slate-50 border-b border-slate-100">
                <div className="flex items-center gap-2 flex-wrap">
                    <span className="text-xs font-medium text-slate-500">Préréglages :</span>
                    <button
                        onClick={() => applyPreset('weekdays')}
                        className="px-3 py-1 text-xs font-medium bg-white border border-slate-200 rounded-full hover:border-teal-400 hover:bg-teal-50 transition-colors"
                    >
                        Lun-Ven (9h-18h)
                    </button>
                    <button
                        onClick={() => applyPreset('fullweek')}
                        className="px-3 py-1 text-xs font-medium bg-white border border-slate-200 rounded-full hover:border-teal-400 hover:bg-teal-50 transition-colors"
                    >
                        7j/7
                    </button>
                    <button
                        onClick={() => applyPreset('mornings')}
                        className="px-3 py-1 text-xs font-medium bg-white border border-slate-200 rounded-full hover:border-teal-400 hover:bg-teal-50 transition-colors"
                    >
                        Matinées
                    </button>
                </div>
            </div>

            {/* Days Grid */}
            <div className="p-4 sm:p-6 space-y-3">
                {DAYS_FR.map((dayInfo) => {
                    const dayConfig = config.find(d => d.dayOfWeek === dayInfo.dayOfWeek);
                    if (!dayConfig) return null;

                    const isWeekend = dayInfo.dayOfWeek === 0 || dayInfo.dayOfWeek === 6;

                    return (
                        <motion.div
                            key={dayInfo.dayOfWeek}
                            layout
                            className={cn(
                                'flex items-center gap-3 sm:gap-4 p-3 rounded-xl transition-all',
                                dayConfig.isActive
                                    ? 'bg-teal-50/50 border border-teal-200'
                                    : 'bg-slate-50 border border-slate-200 opacity-60'
                            )}
                        >
                            {/* Toggle + Day Name */}
                            <button
                                onClick={() => toggleDay(dayInfo.dayOfWeek)}
                                className={cn(
                                    'w-6 h-6 rounded-md flex items-center justify-center transition-colors flex-shrink-0',
                                    dayConfig.isActive
                                        ? 'bg-teal-500 text-white'
                                        : 'bg-slate-200 text-slate-400'
                                )}
                            >
                                {dayConfig.isActive && <Check className="w-4 h-4" />}
                            </button>

                            <div className={cn(
                                'w-20 font-medium',
                                dayConfig.isActive ? 'text-slate-900' : 'text-slate-400'
                            )}>
                                <span className="hidden sm:inline">{dayInfo.label}</span>
                                <span className="sm:hidden">{dayInfo.short}</span>
                                {isWeekend && (
                                    <span className="ml-1 text-[10px] text-slate-400">(WE)</span>
                                )}
                            </div>

                            {/* Time Inputs */}
                            <AnimatePresence mode="wait">
                                {dayConfig.isActive ? (
                                    <motion.div
                                        initial={{ opacity: 0, x: -10 }}
                                        animate={{ opacity: 1, x: 0 }}
                                        exit={{ opacity: 0, x: -10 }}
                                        className="flex-1 flex items-center gap-2 sm:gap-3"
                                    >
                                        <select
                                            value={dayConfig.startTime}
                                            onChange={(e) => updateTime(dayInfo.dayOfWeek, 'startTime', e.target.value)}
                                            className="flex-1 px-2 sm:px-3 py-1.5 text-sm border border-slate-200 rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-teal-500 bg-white"
                                        >
                                            {TIME_OPTIONS.map(time => (
                                                <option key={time} value={time}>{time}</option>
                                            ))}
                                        </select>
                                        <span className="text-slate-400 text-sm">→</span>
                                        <select
                                            value={dayConfig.endTime}
                                            onChange={(e) => updateTime(dayInfo.dayOfWeek, 'endTime', e.target.value)}
                                            className="flex-1 px-2 sm:px-3 py-1.5 text-sm border border-slate-200 rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-teal-500 bg-white"
                                        >
                                            {TIME_OPTIONS.map(time => (
                                                <option key={time} value={time}>{time}</option>
                                            ))}
                                        </select>
                                        <button
                                            onClick={() => copyToAll(dayInfo.dayOfWeek)}
                                            className="hidden sm:flex p-1.5 text-slate-400 hover:text-teal-600 hover:bg-teal-100 rounded transition-colors"
                                            title="Copier sur tous les jours"
                                        >
                                            <Calendar className="w-4 h-4" />
                                        </button>
                                    </motion.div>
                                ) : (
                                    <motion.div
                                        initial={{ opacity: 0 }}
                                        animate={{ opacity: 1 }}
                                        className="flex-1 text-sm text-slate-400"
                                    >
                                        Non disponible
                                    </motion.div>
                                )}
                            </AnimatePresence>
                        </motion.div>
                    );
                })}
            </div>

            {/* Info Note */}
            <div className="px-4 sm:px-6 pb-4">
                <div className="flex items-start gap-2 p-3 bg-amber-50 border border-amber-200 rounded-xl text-sm">
                    <Info className="w-4 h-4 text-amber-600 flex-shrink-0 mt-0.5" />
                    <p className="text-amber-800">
                        Ces horaires définissent quand vous êtes disponible pour les <strong>réservations 1-to-1</strong>.
                        Les missions SOS peuvent être acceptées séparément.
                    </p>
                </div>
            </div>

            {/* Footer Actions */}
            <div className="p-4 sm:p-6 border-t border-slate-100 bg-slate-50/50">
                <div className="flex items-center justify-between">
                    <p className="text-sm text-slate-500">
                        {hasChanges && (
                            <span className="text-amber-600 flex items-center gap-1">
                                <AlertCircle className="w-4 h-4" />
                                Modifications non sauvegardées
                            </span>
                        )}
                    </p>
                    <Button
                        onClick={handleSave}
                        disabled={!hasChanges || isSaving || isLoading}
                        className="bg-teal-600 hover:bg-teal-700 text-white disabled:opacity-50"
                    >
                        {isSaving ? (
                            <span className="flex items-center gap-2">
                                <Loader2 className="w-4 h-4 animate-spin" />
                                Enregistrement...
                            </span>
                        ) : (
                            <span className="flex items-center gap-2">
                                <Save className="w-4 h-4" />
                                Enregistrer
                            </span>
                        )}
                    </Button>
                </div>
            </div>
        </div>
    );
}

export default AvailabilityManager;
