'use client';

import type { MouseEvent } from 'react';
import { motion } from 'framer-motion';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { MapPin, Euro, Zap, Clock, Building2, ArrowRight, Moon, Calendar } from 'lucide-react';

// ===========================================
// MISSION LIST CARD - Compact Design
// Layout: Liste verticale (une carte sous l'autre)
// Vibe: Professionnel, Clinique, Urgent
// NO IMAGES - Focus on data: Logo, Title, Tags, CTA
// ===========================================

export interface MissionListCardProps {
    data: any;
    onClick?: () => void;
}

const urgencyConfig = {
    LOW: { label: 'Sous 1 semaine', color: 'bg-slate-100 text-slate-600', urgent: false, dot: 'bg-slate-400', border: 'border-l-slate-400', tagBg: 'bg-slate-100 text-slate-700' },
    MEDIUM: { label: 'Sous 48h', color: 'bg-amber-100 text-amber-700', urgent: false, dot: 'bg-amber-500', border: 'border-l-amber-500', tagBg: 'bg-amber-50 text-amber-700' },
    HIGH: { label: 'Sous 24h', color: 'bg-rose-100 text-rose-700', urgent: true, dot: 'bg-rose-500', border: 'border-l-rose-500', tagBg: 'bg-rose-50 text-rose-700' },
    CRITICAL: { label: 'URGENT !', color: 'bg-rose-500 text-white', urgent: true, dot: 'bg-white', border: 'border-l-rose-600', tagBg: 'bg-rose-500 text-white' },
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

const formatDate = (value?: string | Date | null) => {
    if (!value) return '';
    const date = typeof value === 'string' ? new Date(value) : value;
    if (isNaN(date.getTime())) return '';
    return date.toLocaleDateString('fr-FR', { weekday: 'short', day: 'numeric', month: 'short' });
};

const getInitials = (value?: string) => {
    if (!value) return 'ET';
    const parts = value.split(' ').filter(Boolean);
    if (parts.length === 0) return 'ET';
    return parts.map((part) => part[0]?.toUpperCase()).join('').slice(0, 2);
};

export function MissionListCard({ data, onClick }: MissionListCardProps) {
    const mission = data || {};
    const missionId = mission?.id;
    const establishment = mission?.client?.establishment?.name || mission?.establishment || mission?.authorName || 'Établissement';
    const establishmentLogo = mission?.client?.establishment?.logoUrl || mission?.establishmentLogo;
    const city = mission?.city || mission?.client?.establishment?.city || 'Non précisé';
    const urgencyLevel = (mission?.urgencyLevel || 'MEDIUM') as keyof typeof urgencyConfig;
    const hourlyRate = mission?.hourlyRate !== undefined && mission?.hourlyRate !== null ? Number(mission.hourlyRate) : null;
    const totalPrice = mission?.totalPrice !== undefined ? Number(mission.totalPrice) : null;
    const missionTitle = mission?.title || mission?.jobTitle || 'Mission de renfort';
    const jobType = mission?.jobTitle || mission?.missionType || '';
    const startDate = mission?.startDate;
    const isNightShift = Boolean(mission?.isNightShift);
    const postedLabel = formatRelativeTime(mission?.createdAt);
    const detailHref = missionId ? `/need/${missionId}` : undefined;
    const urgency = urgencyConfig[urgencyLevel];
    const isUrgent = urgency.urgent;
    const router = useRouter();

    const priceDisplay = hourlyRate !== null
        ? `${hourlyRate}€/h`
        : totalPrice !== null
            ? `${totalPrice}€`
            : 'À définir';

    const handleViewMission = (event: MouseEvent<HTMLButtonElement>) => {
        event.stopPropagation();
        event.preventDefault();
        if (!missionId) return;
        router.push(`/need/${missionId}`);
    };

    const card = (
        <motion.article
            whileHover={{ x: 4, transition: { duration: 0.15 } }}
            onClick={onClick}
            className={`
                group relative bg-white rounded-xl overflow-hidden cursor-pointer
                border-l-4 ${urgency.border} border border-slate-100
                shadow-sm hover:shadow-md
                transition-all duration-200
            `}
            itemScope
            itemType="https://schema.org/JobPosting"
        >
            <div className="flex items-stretch">
                {/* LEFT: Logo/Initials */}
                <div className="flex-shrink-0 w-20 flex items-center justify-center bg-slate-50 border-r border-slate-100">
                    <div className="w-12 h-12 rounded-xl bg-white border border-slate-200 flex items-center justify-center overflow-hidden shadow-sm">
                        {establishmentLogo ? (
                            <img src={establishmentLogo} alt={establishment} className="w-full h-full object-cover" loading="lazy" />
                        ) : (
                            <span className="text-sm font-bold text-slate-400">{getInitials(establishment)}</span>
                        )}
                    </div>
                </div>

                {/* CENTER: Content */}
                <div className="flex-1 min-w-0 px-4 py-4">
                    {/* Establishment + Time */}
                    <div className="flex items-center gap-2 text-xs text-slate-500 mb-1">
                        <Building2 className="w-3 h-3 flex-shrink-0" />
                        <span className="truncate font-medium" itemProp="hiringOrganization">{establishment}</span>
                        <span className="text-slate-300">•</span>
                        <Clock className="w-3 h-3 flex-shrink-0" />
                        <span>{postedLabel || 'Récemment'}</span>
                    </div>

                    {/* Title */}
                    <h3
                        className="text-base font-bold text-slate-900 leading-tight line-clamp-1 group-hover:text-rose-600 transition-colors"
                        itemProp="title"
                    >
                        {missionTitle}
                    </h3>

                    {/* Job Type if different */}
                    {jobType && jobType !== missionTitle && (
                        <p className="text-sm text-slate-600 mt-0.5 flex items-center gap-1">
                            {jobType}
                            {isNightShift && (
                                <span className="inline-flex items-center gap-0.5 text-xs bg-indigo-50 text-indigo-600 px-1.5 py-0.5 rounded">
                                    <Moon className="w-3 h-3" />Nuit
                                </span>
                            )}
                        </p>
                    )}

                    {/* Tags Row */}
                    <div className="flex flex-wrap items-center gap-2 mt-2">
                        {/* Urgency Tag */}
                        <span className={`inline-flex items-center gap-1 px-2.5 py-1 rounded-lg text-xs font-bold ${urgency.tagBg}`}>
                            {isUrgent && <Zap className="w-3 h-3" />}
                            <span className={`w-1.5 h-1.5 rounded-full ${urgency.dot} ${isUrgent ? 'animate-pulse' : ''}`} />
                            {urgency.label}
                        </span>

                        {/* Location Tag */}
                        <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-lg bg-slate-100 text-xs font-medium text-slate-700">
                            <MapPin className="w-3 h-3" />
                            <span itemProp="jobLocation">{city}</span>
                        </span>

                        {/* Salary Tag */}
                        <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-lg bg-emerald-50 text-xs font-bold text-emerald-700">
                            <Euro className="w-3 h-3" />
                            <span itemProp="baseSalary">{priceDisplay}</span>
                        </span>

                        {/* Date Tag */}
                        {startDate && (
                            <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-lg bg-slate-100 text-xs font-medium text-slate-700">
                                <Calendar className="w-3 h-3" />
                                {formatDate(startDate)}
                            </span>
                        )}
                    </div>
                </div>

                {/* RIGHT: CTA Button */}
                <div className="flex-shrink-0 flex items-center px-4 border-l border-slate-100">
                    <button
                        type="button"
                        onClick={handleViewMission}
                        className="inline-flex items-center gap-2 px-4 py-2.5 rounded-xl bg-rose-500 hover:bg-rose-600 text-white text-sm font-semibold shadow-sm hover:shadow active:scale-[0.97] transition-all whitespace-nowrap"
                    >
                        Voir la mission
                        <ArrowRight className="w-4 h-4" />
                    </button>
                </div>
            </div>
        </motion.article>
    );

    return detailHref ? <Link href={detailHref} className="block">{card}</Link> : card;
}
