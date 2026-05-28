'use client';

import { motion } from 'framer-motion';
import {
    BadgeCheck,
    Camera,
    MapPin,
    Calendar,
    Edit3
} from 'lucide-react';

export interface ProfileHeaderProps {
    /** User's first name */
    firstName: string;
    /** User's last name */
    lastName: string;
    /** Avatar URL */
    avatarUrl?: string | null;
    /** Cover image URL (optional) */
    coverUrl?: string | null;
    /** Professional headline/title */
    headline?: string | null;
    /** User's city */
    city?: string | null;
    /** Member since date */
    memberSince?: Date | string;
    /** Whether the user is verified */
    isVerified?: boolean;
    /** User role: TALENT (freelance) or CLIENT (establishment) */
    role: 'TALENT' | 'CLIENT' | 'ADMIN';
    /** Whether this is the current user's own profile */
    isOwnProfile?: boolean;
    /** Callback when edit cover is clicked */
    onEditCover?: () => void;
    /** Callback when edit avatar is clicked */
    onEditAvatar?: () => void;
}

export function ProfileHeader({
    firstName,
    lastName,
    avatarUrl,
    coverUrl,
    headline,
    city,
    memberSince,
    isVerified = false,
    role,
    isOwnProfile = false,
    onEditCover,
    onEditAvatar,
}: ProfileHeaderProps) {
    const fullName = `${firstName || ''} ${lastName || ''}`;
    const initials = `${(firstName || '').charAt(0)}${(lastName || '').charAt(0)}`.toUpperCase();

    const formattedDate = memberSince
        ? new Date(memberSince).toLocaleDateString('fr-FR', {
            month: 'long',
            year: 'numeric'
        })
        : null;

    const roleLabel = role === 'TALENT' ? 'Professionnel' : role === 'CLIENT' ? 'Établissement' : 'Admin';

    return (
        <div className="relative">
            {/* Cover Image / Gradient Background */}
            <div className="relative h-36 md:h-48 overflow-hidden rounded-t-3xl">
                {coverUrl ? (
                    <img
                        src={coverUrl}
                        alt="Couverture"
                        className="w-full h-full object-cover"
                    />
                ) : (
                    <div className="w-full h-full bg-gradient-to-r from-brand-50 via-slate-50 to-indigo-100" />
                )}

                {/* Gradient overlay for better text readability */}
                <div className="absolute inset-0 bg-gradient-to-t from-white/60 via-transparent to-transparent" />

                {/* Edit Cover Button (own profile only) */}
                {isOwnProfile && (
                    <motion.button
                        whileHover={{ scale: 1.05 }}
                        whileTap={{ scale: 0.95 }}
                        onClick={onEditCover}
                        className="absolute top-4 right-4 btn-secondary !px-3 !py-2 bg-white/80 backdrop-blur-sm shadow-soft"
                    >
                        <Camera className="w-4 h-4" />
                        <span className="hidden sm:inline">Modifier</span>
                    </motion.button>
                )}
            </div>

            {/* Profile Content Area */}
            <div className="relative px-6 pb-6">
                {/* Avatar - Overlapping cover and content */}
                <div className="relative -mt-16 mb-4 flex items-end gap-4">
                    {/* Avatar Container */}
                    <div className="relative flex-shrink-0">
                        <motion.div
                            initial={{ scale: 0.8, opacity: 0 }}
                            animate={{ scale: 1, opacity: 1 }}
                            transition={{ type: 'spring', stiffness: 200, damping: 20 }}
                            className="relative"
                        >
                            {/* Avatar Circle */}
                            <div className="w-32 h-32 rounded-full border-4 border-white shadow-lg overflow-hidden bg-gradient-to-br from-brand-100 to-brand-200">
                                {avatarUrl ? (
                                    <img
                                        src={avatarUrl}
                                        alt={fullName}
                                        className="w-full h-full object-cover"
                                    />
                                ) : (
                                    <div className="w-full h-full flex items-center justify-center">
                                        <span className="text-3xl font-bold text-brand-600">
                                            {initials}
                                        </span>
                                    </div>
                                )}
                            </div>

                            {/* Edit Avatar Button (own profile only) */}
                            {isOwnProfile && (
                                <motion.button
                                    whileHover={{ scale: 1.1 }}
                                    whileTap={{ scale: 0.9 }}
                                    onClick={onEditAvatar}
                                    className="absolute bottom-1 right-1 w-9 h-9 rounded-full bg-brand-600 text-white flex items-center justify-center shadow-lg hover:bg-brand-700 transition-colors"
                                >
                                    <Camera className="w-4 h-4" />
                                </motion.button>
                            )}
                        </motion.div>
                    </div>

                    {/* Role Badge (Mobile) */}
                    <div className="sm:hidden mb-2">
                        <span className="inline-flex px-3 py-1 rounded-full bg-brand-100 text-brand-700 text-xs font-semibold">
                            {roleLabel}
                        </span>
                    </div>
                </div>

                {/* Name, Verification, and Details */}
                <div className="space-y-3">
                    {/* Name Row with Verification */}
                    <div className="flex flex-wrap items-center gap-2">
                        <h1 className="text-2xl sm:text-3xl font-bold text-slate-900">
                            {fullName}
                        </h1>

                        {/* Verification Badge */}
                        {isVerified && (
                            <motion.div
                                initial={{ scale: 0, rotate: -180 }}
                                animate={{ scale: 1, rotate: 0 }}
                                transition={{ type: 'spring', delay: 0.2 }}
                                className="flex items-center gap-1 px-2 py-0.5 rounded-full bg-blue-50"
                            >
                                <BadgeCheck className="w-5 h-5 text-blue-500" />
                                <span className="text-xs font-medium text-blue-700 hidden sm:inline">
                                    Vérifié
                                </span>
                            </motion.div>
                        )}

                        {/* Role Badge (Desktop) */}
                        <span className="hidden sm:inline-flex px-3 py-1 rounded-full bg-brand-100 text-brand-700 text-xs font-semibold">
                            {roleLabel}
                        </span>

                        {/* Edit Profile Button (own profile, desktop) */}
                        {isOwnProfile && (
                            <motion.button
                                whileHover={{ scale: 1.02 }}
                                whileTap={{ scale: 0.98 }}
                                className="ml-auto hidden sm:flex btn-secondary"
                            >
                                <Edit3 className="w-4 h-4" />
                                Modifier le profil
                            </motion.button>
                        )}
                    </div>

                    {/* Headline / Title */}
                    {headline && (
                        <p className="text-slate-600 text-base sm:text-lg leading-relaxed max-w-2xl">
                            {headline}
                        </p>
                    )}

                    {/* Meta Info (Location, Member Since) */}
                    <div className="flex flex-wrap items-center gap-4 text-sm text-slate-500">
                        {city && (
                            <span className="inline-flex items-center gap-1.5">
                                <MapPin className="w-4 h-4 text-slate-400" />
                                {city}
                            </span>
                        )}
                        {formattedDate && (
                            <span className="inline-flex items-center gap-1.5">
                                <Calendar className="w-4 h-4 text-slate-400" />
                                Membre depuis {formattedDate}
                            </span>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
}

