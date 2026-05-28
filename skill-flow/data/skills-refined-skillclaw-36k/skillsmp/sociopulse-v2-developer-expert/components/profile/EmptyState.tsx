'use client';

import { motion } from 'framer-motion';
import {
    Sprout,
    Handshake,
    Sparkles,
    Star,
    Briefcase,
    MessageCircle
} from 'lucide-react';

export type EmptyStateType = 'missions' | 'reviews' | 'profile';

export interface EmptyStateProps {
    type: EmptyStateType;
    /** User's first name for personalization */
    userName?: string;
    /** Whether this is the user's own profile */
    isOwnProfile?: boolean;
    /** Custom message override */
    customMessage?: string;
    /** Action button callback */
    onAction?: () => void;
    /** Action button label */
    actionLabel?: string;
}

const emptyStateConfig: Record<EmptyStateType, {
    icon: typeof Sprout;
    title: string;
    titleOwn: string;
    description: string;
    descriptionOwn: string;
}> = {
    missions: {
        icon: Sprout,
        title: 'Ce profil est nouveau sur Sociopulse !',
        titleOwn: 'Votre parcours commence ici',
        description: 'Soyez le premier à collaborer avec eux.',
        descriptionOwn: 'Complétez votre première mission pour construire votre réputation.',
    },
    reviews: {
        icon: Handshake,
        title: 'Pas encore d\'avis',
        titleOwn: 'Aucun avis pour le moment',
        description: 'Soyez le premier à partager votre expérience avec ce profil.',
        descriptionOwn: 'Les avis apparaîtront ici après vos premières collaborations.',
    },
    profile: {
        icon: Sparkles,
        title: 'Profil en cours de création',
        titleOwn: 'Complétez votre profil',
        description: 'Ce membre n\'a pas encore complété son profil.',
        descriptionOwn: 'Ajoutez vos compétences et expériences pour attirer plus de missions.',
    },
};

const containerVariants = {
    hidden: { opacity: 0, scale: 0.95 },
    visible: {
        opacity: 1,
        scale: 1,
        transition: {
            type: 'spring' as const,
            stiffness: 100,
            damping: 15,
        },
    },
};

export function EmptyState({
    type,
    userName,
    isOwnProfile = false,
    customMessage,
    onAction,
    actionLabel,
}: EmptyStateProps) {
    const config = emptyStateConfig[type];
    const Icon = config.icon;

    const title = customMessage ? customMessage : (isOwnProfile ? config.titleOwn : config.title);
    const description = isOwnProfile ? config.descriptionOwn : config.description;

    return (
        <motion.div
            variants={containerVariants}
            initial="hidden"
            animate="visible"
            className="py-12 px-6 flex flex-col items-center text-center border-2 border-dashed border-slate-200 rounded-xl bg-slate-50/50"
        >
            {/* Animated Icon Container */}
            <motion.div
                initial={{ y: 10, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                transition={{ delay: 0.1 }}
                className="relative inline-flex mb-6"
            >
                {/* Icon Circle - White background with shadow */}
                <div className="relative bg-white rounded-full p-4 shadow-sm">
                    <Icon className="w-16 h-16 text-slate-300" />
                </div>

                {/* Decorative Sparkles */}
                <motion.div
                    animate={{
                        rotate: [0, 10, -10, 0],
                        scale: [1, 1.1, 1],
                    }}
                    transition={{
                        duration: 3,
                        repeat: Infinity,
                        repeatType: 'reverse'
                    }}
                    className="absolute -top-1 -right-1"
                >
                    <Sparkles className="w-5 h-5 text-amber-400" />
                </motion.div>
            </motion.div>

            {/* Title */}
            <motion.h3
                initial={{ y: 10, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                transition={{ delay: 0.2 }}
                className="text-lg font-semibold text-slate-800"
            >
                {userName && !isOwnProfile ? title.replace('Ce profil', userName) : title}
            </motion.h3>

            {/* Description */}
            <motion.p
                initial={{ y: 10, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                transition={{ delay: 0.3 }}
                className="text-sm text-slate-500 max-w-xs mt-2"
            >
                {description}
            </motion.p>

            {/* Action Button - Pill style */}
            {onAction && actionLabel && (
                <motion.button
                    initial={{ y: 10, opacity: 0 }}
                    animate={{ y: 0, opacity: 1 }}
                    transition={{ delay: 0.4 }}
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.98 }}
                    onClick={onAction}
                    className="mt-6 inline-flex items-center gap-2 px-5 py-2.5 rounded-full bg-brand-600 text-white font-medium text-sm hover:bg-brand-700 transition-all duration-200 shadow-lg shadow-brand-600/25 border border-transparent hover:border-brand-500"
                >
                    {type === 'missions' && <Briefcase className="w-4 h-4" />}
                    {type === 'reviews' && <Star className="w-4 h-4" />}
                    {type === 'profile' && <MessageCircle className="w-4 h-4" />}
                    {actionLabel}
                </motion.button>
            )}

            {/* Encouragement badge for new profiles */}
            {type === 'missions' && !isOwnProfile && (
                <motion.div
                    initial={{ y: 10, opacity: 0 }}
                    animate={{ y: 0, opacity: 1 }}
                    transition={{ delay: 0.5 }}
                    className="mt-6 inline-flex items-center gap-2 px-4 py-2 rounded-full bg-white border border-slate-200 shadow-sm"
                >
                    <Sprout className="w-4 h-4 text-green-500" />
                    <span className="text-xs font-medium text-slate-600">
                        Nouveau membre • Inscrit récemment
                    </span>
                </motion.div>
            )}
        </motion.div>
    );
}
