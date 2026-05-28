'use client';

import { motion } from 'framer-motion';
import { 
    Star, 
    Briefcase, 
    CheckCircle2, 
    Circle
} from 'lucide-react';

export interface TrustStats {
    /** Average rating (0-5) */
    averageRating: number;
    /** Total number of reviews */
    totalReviews: number;
    /** Total missions (completed for TALENT, posted for Client) */
    totalMissions: number;
    /** Reliability percentage (0-100) */
    reliabilityRate: number;
    /** Whether the user is currently available */
    isAvailable: boolean;
}

export interface StatsRowProps extends TrustStats {
    /** User role: determines labels */
    role: 'TALENT' | 'CLIENT' | 'ADMIN';
}

const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
        opacity: 1,
        transition: {
            staggerChildren: 0.1,
            delayChildren: 0.2,
        },
    },
};

const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: {
        opacity: 1,
        y: 0,
        transition: {
            type: 'spring' as const,
            stiffness: 100,
            damping: 15,
        },
    },
};

interface StatItemProps {
    icon: React.ReactNode;
    value: string | number;
    label: string;
    sublabel?: string;
    highlight?: boolean;
}

function StatItem({ icon, value, label, sublabel, highlight = false }: StatItemProps) {
    return (
        <motion.div
            variants={itemVariants}
            className={`
                flex flex-col items-center p-4 rounded-2xl
                ${highlight 
                    ? 'bg-gradient-to-br from-brand-50 to-indigo-50 border border-brand-100'
                    : 'bg-slate-50/80 hover:bg-slate-100/80'
                }
                transition-colors duration-200
            `}
        >
            {/* Icon */}
            <div className={`
                mb-2 p-2 rounded-xl
                ${highlight ? 'bg-brand-100 text-brand-600' : 'bg-white text-slate-500 shadow-sm'}
            `}>
                {icon}
            </div>

            {/* Value */}
            <span className={`
                text-xl sm:text-2xl font-bold
                ${highlight ? 'text-brand-600' : 'text-slate-900'}
            `}>
                {value}
            </span>

            {/* Label */}
            <span className="text-xs sm:text-sm font-medium text-slate-600 text-center">
                {label}
            </span>

            {/* Sublabel */}
            {sublabel && (
                <span className="text-[10px] sm:text-xs text-slate-400 mt-0.5">
                    {sublabel}
                </span>
            )}
        </motion.div>
    );
}

export function StatsRow({
    role,
    averageRating,
    totalReviews,
    totalMissions,
    reliabilityRate,
    isAvailable,
}: StatsRowProps) {
    // Role-specific labels
    const missionsLabel = role === 'TALENT' ? 'Missions' : 'Missions';
    const missionsSubLabel = role === 'TALENT' ? 'Réalisées' : 'Publiées';
    const reliabilityLabel = role === 'TALENT' ? 'Taux de présence' : 'Taux de réponse';
    const availabilityLabel = role === 'TALENT' ? 'Disponible' : 'Recrute';
    const unavailabilityLabel = role === 'TALENT' ? 'Indisponible' : 'Ne recrute pas';

    // Format rating
    const formattedRating = averageRating > 0 ? averageRating.toFixed(1) : '—';
    const ratingSubLabel = totalReviews > 0 ? `Sur ${totalReviews} avis` : 'Aucun avis';

    // Format reliability
    const formattedReliability = `${Math.round(reliabilityRate)}%`;

    return (
        <motion.div
            variants={containerVariants}
            initial="hidden"
            animate="visible"
            className="px-4 sm:px-6 py-6"
        >
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 sm:gap-4 max-w-3xl mx-auto">
                {/* Rating */}
                <StatItem
                    icon={<Star className="w-5 h-5 fill-amber-400 text-amber-400" />}
                    value={formattedRating}
                    label="Note moyenne"
                    sublabel={ratingSubLabel}
                    highlight={averageRating >= 4.5}
                />

                {/* Missions Count */}
                <StatItem
                    icon={<Briefcase className="w-5 h-5" />}
                    value={totalMissions}
                    label={missionsLabel}
                    sublabel={missionsSubLabel}
                />

                {/* Reliability Rate */}
                <StatItem
                    icon={<CheckCircle2 className="w-5 h-5" />}
                    value={formattedReliability}
                    label={reliabilityLabel}
                    highlight={reliabilityRate >= 95}
                />

                {/* Availability Status */}
                <motion.div
                    variants={itemVariants}
                    className={`
                        flex flex-col items-center justify-center p-4 rounded-2xl
                        ${isAvailable 
                            ? 'bg-gradient-to-br from-green-50 to-emerald-50 border border-green-200' 
                            : 'bg-slate-100 border border-slate-200'
                        }
                        transition-colors duration-200
                    `}
                >
                    {/* Animated Status Dot */}
                    <div className="relative mb-2">
                        {isAvailable ? (
                            <>
                                {/* Ping animation */}
                                <span className="absolute inset-0 w-4 h-4 rounded-full bg-green-400 animate-ping opacity-30" />
                                <span className="relative block w-4 h-4 rounded-full bg-green-500 shadow-sm" />
                            </>
                        ) : (
                            <Circle className="w-4 h-4 text-slate-400 fill-slate-300" />
                        )}
                    </div>

                    {/* Status Label */}
                    <span className={`
                        text-sm sm:text-base font-bold
                        ${isAvailable ? 'text-green-700' : 'text-slate-500'}
                    `}>
                        {isAvailable ? availabilityLabel : unavailabilityLabel}
                    </span>

                    {/* Status Hint */}
                    <span className={`
                        text-[10px] sm:text-xs mt-0.5
                        ${isAvailable ? 'text-green-600' : 'text-slate-400'}
                    `}>
                        {isAvailable 
                            ? (role === 'TALENT' ? 'Accepte les missions' : 'Recherche actifs')
                            : 'Statut actuel'
                        }
                    </span>
                </motion.div>
            </div>
        </motion.div>
    );
}

