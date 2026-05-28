'use client';

import type { CSSProperties, KeyboardEvent } from 'react';
import { useId, useMemo, useState } from 'react';
import { motion } from 'framer-motion';
import { Search } from 'lucide-react';
import { currentBrand, isMedical } from '@/lib/brand';

// ===========================================
// SMART SEARCH BAR - Brand-Aware
// Adapts placeholder and visuals to brand
// ===========================================

export type FloatingAvatar = {
    id: string;
    name?: string | null;
    avatarUrl?: string | null;
};

export interface SmartSearchBarProps {
    value: string;
    onChange: (value: string) => void;
    onSubmit?: () => void;
    placeholder?: string;
    avatars?: FloatingAvatar[];
}

// Dynamic placeholders based on brand
const PLACEHOLDERS = {
    SOCIAL: "Besoin d'un renfort pour demain ? Ou d'une visio Eduat'heure ?",
    MEDICAL: "Besoin d'un soignant en urgence ? IDE, AS, Kiné ?",
};

// Dynamic default avatars based on brand
const DEFAULT_AVATARS_SOCIAL: FloatingAvatar[] = [
    { id: 'lx-0', name: 'Les Extras', avatarUrl: null },
    { id: 'lx-1', name: 'Educateur', avatarUrl: null },
    { id: 'lx-2', name: 'Renfort', avatarUrl: null },
];

const DEFAULT_AVATARS_MEDICAL: FloatingAvatar[] = [
    { id: 'mp-0', name: 'MedicoPulse', avatarUrl: null },
    { id: 'mp-1', name: 'Infirmier', avatarUrl: null },
    { id: 'mp-2', name: 'Aide-Soignant', avatarUrl: null },
];

const ORBIT_POSITIONS: CSSProperties[] = [
    { top: '-22px', left: '10%' },
    { top: '10%', right: '-26px' },
    { bottom: '-28px', left: '18%' },
    { top: '52%', left: '-28px' },
    { bottom: '18%', right: '10%' },
    { top: '-28px', right: '18%' },
];

const getInitials = (name?: string | null) => {
    if (!name) return 'LX';
    const parts = name.split(' ').filter(Boolean);
    if (parts.length === 0) return 'LX';
    return parts.map((part) => part[0]?.toUpperCase()).join('').slice(0, 2);
};

export function SmartSearchBar({
    value,
    onChange,
    onSubmit,
    placeholder,
    avatars = [],
}: SmartSearchBarProps) {
    const inputId = useId();
    const [isFocused, setIsFocused] = useState(false);

    // Brand-aware placeholder
    const resolvedPlaceholder = placeholder ?? PLACEHOLDERS[currentBrand.mode];

    // Brand-aware glow color
    const glowGradient = isMedical()
        ? 'from-rose-500/35 via-red-500/30 to-rose-500/25'
        : 'from-indigo-500/35 via-teal-500/30 to-indigo-500/25';

    // Brand-aware ring colors for avatars
    const getRingColor = (index: number) => {
        if (isMedical()) {
            return index % 2 === 0 ? 'ring-rose-500/30' : 'ring-red-500/25';
        }
        return index % 2 === 0 ? 'ring-indigo-500/30' : 'ring-teal-500/25';
    };

    const floatingAvatars = useMemo(() => {
        const normalized = avatars
            .filter((avatar) => avatar && typeof avatar.id === 'string')
            .slice(0, ORBIT_POSITIONS.length);

        if (normalized.length > 0) {
            return normalized;
        }

        // Return brand-specific default avatars
        return isMedical() ? DEFAULT_AVATARS_MEDICAL : DEFAULT_AVATARS_SOCIAL;
    }, [avatars]);

    const handleKeyDown = (event: KeyboardEvent<HTMLInputElement>) => {
        if (event.key !== 'Enter') return;
        onSubmit?.();
    };

    return (
        <div className="relative">
            <div className="pointer-events-none absolute inset-0">
                {floatingAvatars.map((avatar, index) => {
                    const style = ORBIT_POSITIONS[index % ORBIT_POSITIONS.length];
                    const duration = 5.4 + index * 0.55;
                    const delay = index * 0.18;
                    const ringColor = getRingColor(index);

                    return (
                        <motion.div
                            key={avatar.id}
                            style={style}
                            className={`absolute h-12 w-12 rounded-full ring-1 ${ringColor} bg-white/70 backdrop-blur-md shadow-soft overflow-hidden`}
                            animate={{
                                y: [0, -10, 0],
                                rotate: [0, 2, -2, 0],
                            }}
                            transition={{
                                duration,
                                delay,
                                repeat: Infinity,
                                ease: 'easeInOut',
                            }}
                        >
                            {avatar.avatarUrl ? (
                                <img
                                    src={avatar.avatarUrl}
                                    alt={avatar.name || 'Avatar'}
                                    className="h-full w-full object-cover"
                                />
                            ) : (
                                <div className="h-full w-full grid place-items-center bg-gradient-to-br from-white/60 to-white/30">
                                    <span className="text-sm font-semibold text-slate-700">
                                        {getInitials(avatar.name)}
                                    </span>
                                </div>
                            )}
                        </motion.div>
                    );
                })}
            </div>

            <motion.div
                className="relative"
                animate={{ scale: isFocused ? 1.01 : 1 }}
                transition={{ type: 'spring' as const, stiffness: 240, damping: 18 }}
            >
                <motion.div
                    aria-hidden
                    className={`absolute -inset-2 rounded-[2rem] bg-gradient-to-r ${glowGradient} blur-2xl`}
                    animate={{ opacity: isFocused ? 1 : 0.35 }}
                    transition={{ duration: 0.35, ease: 'easeOut' }}
                />

                <div className="relative glass rounded-[2rem] border border-white/60 shadow-soft overflow-hidden">
                    <label htmlFor={inputId} className="sr-only">
                        Rechercher
                    </label>
                    <div className="relative">
                        <Search className="absolute left-6 top-1/2 -translate-y-1/2 h-6 w-6 text-slate-400" />
                        <input
                            id={inputId}
                            value={value}
                            onChange={(event) => onChange(event.target.value)}
                            onKeyDown={handleKeyDown}
                            onFocus={() => setIsFocused(true)}
                            onBlur={() => setIsFocused(false)}
                            placeholder={resolvedPlaceholder}
                            className="w-full bg-transparent pl-16 pr-6 py-5 text-lg sm:text-xl font-medium tracking-tight text-slate-900 placeholder:text-slate-400/90 outline-none"
                            aria-label="Rechercher une mission ou une visio"
                            autoComplete="off"
                        />
                    </div>
                </div>
            </motion.div>
        </div>
    );
}
