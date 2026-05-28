'use client';

import { useState, useTransition } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
    Zap,
    Sun,
    Moon,
    AlertTriangle,
    Send,
    Loader2,
    CheckCircle2,
    Users
} from 'lucide-react';
import { useRouter } from 'next/navigation';
import { ToastContainer, useToasts } from '@/components/ui/Toast';
import { createReliefMission, type CreateReliefMissionInput } from '@/app/(platform)/services/matching.service';

const JOB_TITLES = [
    'Aide-soignant(e)',
    'Infirmier(ere)',
    'Educateur specialise',
    'Auxiliaire de vie',
    'Psychomotricien(ne)',
    'Ergotherapeute',
    'Agent de service',
    'Cuisinier(ere)',
];

interface FlashRequestFormProps {
    onMissionCreated?: (missionId: string, candidatesFound: number) => void;
}

export function FlashRequestForm({ onMissionCreated }: FlashRequestFormProps) {
    const [isPending, startTransition] = useTransition();
    const [isNightShift, setIsNightShift] = useState(false);
    const [jobTitle, setJobTitle] = useState('');
    const [hourlyRate, setHourlyRate] = useState(22);
    const [showSuccess, setShowSuccess] = useState(false);
    const [candidatesFound, setCandidatesFound] = useState(0);
    const router = useRouter();
    const { toasts, addToast, removeToast } = useToasts();

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();

        if (!jobTitle) return;

        startTransition(async () => {
            const input: CreateReliefMissionInput = {
                jobTitle,
                hourlyRate,
                isNightShift,
                urgencyLevel: 'CRITICAL',
                startDate: new Date().toISOString(),
                endDate: new Date(Date.now() + 4 * 60 * 60 * 1000).toISOString(),
                city: 'Lyon',
                postalCode: '69003',
                requiredSkills: [],
                requiredDiplomas: [],
            };

            try {
                const result = await createReliefMission(input);
                const missionId = result?.id || result?.missionId || '';
                const found =
                    result?.candidatesFound ??
                    result?.candidatesCount ??
                    (Array.isArray(result?.candidates) ? result.candidates.length : 0) ??
                    0;

                setShowSuccess(true);
                setCandidatesFound(found);
                onMissionCreated?.(missionId, found);
                addToast({ message: 'Recherche de candidats lancee', type: 'success' });
                router.refresh();

                setTimeout(() => {
                    setShowSuccess(false);
                    setJobTitle('');
                    setHourlyRate(22);
                    setIsNightShift(false);
                }, 3000);
            } catch (error) {
                console.error('createReliefMission error', error);
                addToast({ message: 'Erreur lors du lancement de la mission SOS', type: 'error' });
            }
        });
    };

    return (
        <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            className="relative overflow-hidden rounded-2xl bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 p-6 shadow-2xl"
        >
            <ToastContainer toasts={toasts} onRemove={removeToast} />
            {/* Background Pattern */}
            <div className="absolute inset-0 opacity-5">
                <div className="absolute inset-0" style={{
                    backgroundImage: `radial-gradient(circle at 2px 2px, white 1px, transparent 0)`,
                    backgroundSize: '32px 32px',
                }} />
            </div>

            {/* Urgency Indicator */}
            <div className="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-orange-500 via-red-500 to-orange-500" />

            <div className="relative z-10">
                {/* Header */}
                <div className="flex items-center gap-3 mb-6">
                    <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-orange-500 to-red-500 flex items-center justify-center shadow-lg shadow-orange-500/30">
                        <Zap className="w-6 h-6 text-white" />
                    </div>
                    <div>
                        <h2 className="text-xl font-bold text-white">Demande Flash</h2>
                        <p className="text-sm text-slate-400">Lancez une alerte en 10 secondes</p>
                    </div>
                </div>

                <form onSubmit={handleSubmit} className="space-y-5">
                    {/* Day/Night Switch */}
                    <div className="flex items-center justify-between p-4 rounded-xl bg-slate-800/50 border border-slate-700">
                        <span className="text-sm font-medium text-slate-300">Type de poste</span>
                        <button
                            type="button"
                            onClick={() => setIsNightShift(!isNightShift)}
                            className={`
                relative w-24 h-10 rounded-full transition-all duration-300
                ${isNightShift
                                    ? 'bg-indigo-600 shadow-lg shadow-indigo-500/30'
                                    : 'bg-amber-500 shadow-lg shadow-amber-500/30'
                                }
              `}
                        >
                            <motion.div
                                layout
                                className={`
                  absolute top-1 w-8 h-8 rounded-full bg-white shadow-md
                  flex items-center justify-center
                  ${isNightShift ? 'left-14' : 'left-1'}
                `}
                                transition={{ type: 'spring', stiffness: 500, damping: 30 }}
                            >
                                {isNightShift ? (
                                    <Moon className="w-4 h-4 text-indigo-600" />
                                ) : (
                                    <Sun className="w-4 h-4 text-amber-500" />
                                )}
                            </motion.div>
                            <span className={`
                absolute text-xs font-semibold
                ${isNightShift ? 'left-3 text-white' : 'right-3 text-white'}
              `}>
                                {isNightShift ? 'Nuit' : 'Jour'}
                            </span>
                        </button>
                    </div>

                    {/* Job Title Select */}
                    <div className="space-y-2">
                        <label className="text-sm font-medium text-slate-300">Poste recherche</label>
                        <select
                            value={jobTitle}
                            onChange={(e) => setJobTitle(e.target.value)}
                            required
                            className="w-full h-12 px-4 rounded-xl bg-slate-800/50 border border-slate-700 text-white text-sm
                focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent
                transition-all appearance-none cursor-pointer"
                        >
                            <option value="">Selectionner un poste...</option>
                            {JOB_TITLES.map((title) => (
                                <option key={title} value={title}>{title}</option>
                            ))}
                        </select>
                    </div>

                    {/* Hourly Rate Slider */}
                    <div className="space-y-3">
                        <div className="flex items-center justify-between">
                            <label className="text-sm font-medium text-slate-300">Tarif horaire</label>
                            <span className="text-2xl font-bold text-white">{hourlyRate} EUR<span className="text-sm font-normal text-slate-400">/h</span></span>
                        </div>
                        <input
                            type="range"
                            min="15"
                            max="45"
                            step="1"
                            value={hourlyRate}
                            onChange={(e) => setHourlyRate(parseInt(e.target.value))}
                            className="w-full h-2 rounded-full appearance-none cursor-pointer
                bg-gradient-to-r from-slate-700 via-orange-500 to-red-500
                [&::-webkit-slider-thumb]:appearance-none
                [&::-webkit-slider-thumb]:w-5
                [&::-webkit-slider-thumb]:h-5
                [&::-webkit-slider-thumb]:rounded-full
                [&::-webkit-slider-thumb]:bg-white
                [&::-webkit-slider-thumb]:shadow-lg
                [&::-webkit-slider-thumb]:cursor-pointer
                [&::-webkit-slider-thumb]:transition-transform
                [&::-webkit-slider-thumb]:hover:scale-110"
                        />
                        <div className="flex justify-between text-xs text-slate-500">
                            <span>15 EUR</span>
                            <span>30 EUR</span>
                            <span>45 EUR</span>
                        </div>
                    </div>

                    {/* Submit Button */}
                    <AnimatePresence mode="wait">
                        {showSuccess ? (
                            <motion.div
                                key="success"
                                initial={{ opacity: 0, scale: 0.9 }}
                                animate={{ opacity: 1, scale: 1 }}
                                exit={{ opacity: 0, scale: 0.9 }}
                                className="flex items-center justify-center gap-3 h-14 rounded-xl bg-green-500/20 border border-green-500/30"
                            >
                                <CheckCircle2 className="w-5 h-5 text-green-400" />
                                <span className="font-semibold text-green-400">
                                    Alerte lancee ! {candidatesFound} candidat(s) notifie(s)
                                </span>
                                <Users className="w-5 h-5 text-green-400" />
                            </motion.div>
                        ) : (
                            <motion.button
                                key="submit"
                                type="submit"
                                disabled={isPending || !jobTitle}
                                initial={{ opacity: 0, scale: 0.9 }}
                                animate={{ opacity: 1, scale: 1 }}
                                exit={{ opacity: 0, scale: 0.9 }}
                                whileHover={{ scale: 1.02 }}
                                whileTap={{ scale: 0.98 }}
                                className={`
                  relative w-full h-14 rounded-xl font-bold text-white text-lg
                  transition-all duration-300
                  ${isPending || !jobTitle
                                        ? 'bg-slate-700 cursor-not-allowed'
                                        : 'bg-gradient-to-r from-orange-500 to-red-500 shadow-lg shadow-orange-500/30 hover:shadow-orange-500/50'
                                    }
                `}
                            >
                                {isPending ? (
                                    <span className="flex items-center justify-center gap-2">
                                        <Loader2 className="w-5 h-5 animate-spin" />
                                        Recherche en cours...
                                    </span>
                                ) : (
                                    <span className="flex items-center justify-center gap-2">
                                        <AlertTriangle className="w-5 h-5" />
                                        Lancer l'alerte
                                        <Send className="w-5 h-5" />
                                    </span>
                                )}

                                {/* Pulse Effect */}
                                {!isPending && jobTitle && (
                                    <span className="absolute inset-0 rounded-xl animate-ping bg-orange-500/20" />
                                )}
                            </motion.button>
                        )}
                    </AnimatePresence>
                </form>
            </div>
        </motion.div>
    );
}
