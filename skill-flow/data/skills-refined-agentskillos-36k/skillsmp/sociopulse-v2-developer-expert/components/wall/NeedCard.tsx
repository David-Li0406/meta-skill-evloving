'use client';

import type { MouseEvent } from 'react';
import { motion } from 'framer-motion';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { Clock, MapPin, AlertTriangle } from 'lucide-react';

export interface NeedCardProps {
    data: any;
    onClick?: () => void;
}

const urgencyConfig = {
    LOW: { label: 'Sous 1 semaine', color: 'bg-slate-100 text-slate-600' },
    MEDIUM: { label: 'Sous 48h', color: 'bg-amber-100 text-amber-700' },
    HIGH: { label: 'Sous 24h', color: 'bg-orange-100 text-orange-700' },
    CRITICAL: { label: 'Urgent', color: 'bg-red-100 text-red-700' },
};

const getInitials = (value?: string) => {
    if (!value) return 'LX';
    const parts = value.split(' ').filter(Boolean);
    if (parts.length === 0) return 'LX';
    return parts.map((part) => part[0]?.toUpperCase()).join('').slice(0, 2);
};

const formatRelativeTime = (value?: string | Date | null) => {
    if (!value) return '';
    const date = typeof value === 'string' ? new Date(value) : value;
    if (isNaN(date.getTime())) return '';

    const diffMs = Date.now() - date.getTime();
    const diffMinutes = Math.max(1, Math.round(diffMs / 60000));

    if (diffMinutes < 60) return `Il y a ${diffMinutes} min`;
    const diffHours = Math.round(diffMinutes / 60);
    if (diffHours < 24) return `Il y a ${diffHours}h`;
    const diffDays = Math.round(diffHours / 24);
    return `Il y a ${diffDays}j`;
};

export function NeedCard({
    data,
    onClick,
}: NeedCardProps) {
    const mission = data || {};
    const missionId = mission?.id;
    const establishment = mission?.client?.establishment?.name || mission?.establishment || mission?.authorName || 'Etablissement';
    const establishmentLogo = mission?.client?.establishment?.logoUrl || mission?.establishmentLogo;
    const city = mission?.city || mission?.client?.establishment?.city || '';
    const description = mission?.description || mission?.content || '';
    const urgencyLevel = (mission?.urgencyLevel || 'MEDIUM') as keyof typeof urgencyConfig;
    const hourlyRate = mission?.hourlyRate !== undefined && mission?.hourlyRate !== null ? Number(mission.hourlyRate) : null;
    const missionTitle = mission?.title || mission?.jobTitle || 'Mission';
    const missionType = mission?.jobTitle || missionTitle;
    const startDate = mission?.startDate || mission?.validUntil || mission?.createdAt;
    const isNightShift = Boolean(mission?.isNightShift);
    const postedLabel = formatRelativeTime(mission?.createdAt || startDate);
    const startDateLabel = postedLabel || (startDate ? new Date(startDate).toLocaleDateString('fr-FR', { day: 'numeric', month: 'short' }) : '');
    const rawTags = Array.isArray(mission?.tags)
        ? mission.tags
        : Array.isArray(mission?.requiredSkills)
            ? mission.requiredSkills
            : [];
    const tags: string[] = rawTags.filter((tag: unknown): tag is string => typeof tag === 'string' && tag.trim().length > 0);
    const detailHref = missionId ? `/need/${missionId}` : undefined;
    const urgency = urgencyConfig[urgencyLevel];
    const isUrgent = urgencyLevel === 'HIGH' || urgencyLevel === 'CRITICAL';
    const router = useRouter();

    const handleView = (event: MouseEvent<HTMLButtonElement>) => {
        event.stopPropagation();

        if (!missionId) return;
        router.push(`/dashboard/missions/${missionId}`);
    };

    const card = (
        <motion.article
            whileHover={{ y: -4, transition: { duration: 0.2 } }}
            whileTap={{ scale: 0.98 }}
            onClick={onClick}
            className={`
        group relative bg-white rounded-2xl p-5 cursor-pointer
        border-l-4 border-blue-500
        shadow-soft hover:shadow-soft-lg
        transition-shadow duration-300
      `}
        >
            {/* Urgent Badge */}
            {isUrgent && (
                <div className="absolute -top-2 -right-2 z-10">
                    <span className={`
            inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-xs font-semibold
            ${urgency.color} animate-pulse
          `}>
                        <AlertTriangle className="w-3 h-3" />
                        {urgency.label}
                    </span>
                </div>
            )}

            {/* Header */}
            <div className="flex items-start gap-3 mb-4">
                {/* Establishment Logo */}
                <div className="flex-shrink-0 w-12 h-12 rounded-xl bg-gradient-to-br from-blue-50 to-blue-100 flex items-center justify-center overflow-hidden">
                    {establishmentLogo ? (
                        <img src={establishmentLogo} alt={establishment} className="w-full h-full object-cover" />
                    ) : (
                        <span className="text-sm font-semibold text-blue-600">
                            {getInitials(establishment)}
                        </span>
                    )}
                </div>

                <div className="flex-1 min-w-0">
                    <h3 className="font-semibold text-slate-900 text-base leading-tight line-clamp-1 group-hover:text-blue-600 transition-colors">
                        {missionTitle}
                    </h3>
                    <p className="text-sm text-slate-500 mt-0.5">{establishment}</p>
                </div>
            </div>

            {/* Job Title Badge */}
            <div className="mb-3">
                <span className="inline-block px-3 py-1 rounded-xl bg-rose-50 text-rose-700 text-xs font-medium">
                    {missionType}
                </span>
            </div>

            {/* Description */}
            <p className="text-sm text-slate-600 leading-relaxed line-clamp-2 mb-4">
                {description}
            </p>

            {/* Meta Info */}
            <div className="flex flex-wrap items-center gap-3 text-xs text-slate-500">
                <span className="inline-flex items-center gap-1">
                    <MapPin className="w-3.5 h-3.5" />
                    {city}
                </span>
                <span className="inline-flex items-center gap-1">
                    <Clock className="w-3.5 h-3.5" />
                    {startDateLabel}
                    {isNightShift && ' - Nuit'}
                </span>
                {hourlyRate !== null && hourlyRate !== undefined && (
                    <span className="ml-auto font-semibold text-slate-900">
                        {hourlyRate} EUR/h
                    </span>
                )}
            </div>

            {/* Tags */}
            {tags.length > 0 && (
                <div className="flex flex-wrap gap-1.5 mt-3 pt-3 border-t border-slate-100">
                    {tags.slice(0, 3).map((tag, index) => (
                        <span
                            key={index}
                            className="px-2 py-0.5 rounded-md bg-slate-100 text-slate-600 text-xs"
                        >
                            {tag}
                        </span>
                    ))}
                    {tags.length > 3 && (
                        <span className="text-xs text-slate-400">+{tags.length - 3}</span>
                    )}
                </div>
            )}

            <div className="mt-4 flex items-center justify-end">
                <button
                    type="button"
                    onClick={handleView}
                    className="inline-flex items-center gap-2 px-4 py-2 rounded-xl bg-rose-500 text-white text-sm font-semibold hover:bg-rose-600 shadow-sm hover:shadow-md active:scale-95 transition-all"
                    aria-label={`Voir la mission ${missionTitle}`}
                >
                    Voir
                </button>
            </div>

            {/* Hover Effect Overlay */}
            <div className="absolute inset-0 rounded-2xl border-2 border-transparent group-hover:border-blue-200 transition-colors pointer-events-none" />
        </motion.article>
    );

    return detailHref ? (
        <Link href={detailHref} className="block h-full">
            {card}
        </Link>
    ) : (
        card
    );
}
