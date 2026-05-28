'use client';

import Link from 'next/link';
import {
    Heart,
    MessageCircle,
    Share2,
    Bookmark,
    MapPin,
    Clock,
    Zap,
    ChevronRight,
    Building2
} from 'lucide-react';
import { Badge } from '@/components/ui';

export interface FeedItemType {
    id: string;
    type: 'social' | 'mission';
    author: {
        name: string;
        avatarUrl: string | null;
        role: string;
    };
    content?: string;
    imageUrl?: string | null;
    likes?: number;
    comments?: number;
    mission?: {
        title: string;
        date: string;
        hourlyRate: number;
        city: string;
        urgency: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
    };
    createdAt: Date;
}

interface FeedItemProps {
    item: FeedItemType;
}

export function FeedItem({ item }: FeedItemProps) {
    if (item.type === 'mission') {
        return <MissionCard item={item} />;
    }
    return <SocialPost item={item} />;
}

// ============================================================================
// SOCIAL POST COMPONENT
// ============================================================================
function SocialPost({ item }: FeedItemProps) {
    const timeAgo = getTimeAgo(item.createdAt);

    return (
        <article className="rounded-xl border border-slate-200 bg-white shadow-sm">
            {/* Header */}
            <div className="flex items-center gap-3 p-4">
                <div className="flex h-12 w-12 items-center justify-center rounded-full bg-slate-100 text-sm font-semibold text-slate-600">
                    {item.author.avatarUrl ? (
                        <img
                            src={item.author.avatarUrl}
                            alt={item.author.name}
                            className="h-full w-full rounded-full object-cover"
                        />
                    ) : (
                        item.author.name.charAt(0)
                    )}
                </div>
                <div className="flex-1">
                    <p className="font-semibold text-slate-900">{item.author.name}</p>
                    <p className="text-sm text-slate-500">{item.author.role} · {timeAgo}</p>
                </div>
            </div>

            {/* Content */}
            <div className="px-4 pb-3">
                <p className="text-slate-800 leading-relaxed">{item.content}</p>
            </div>

            {/* Image (if any) */}
            {item.imageUrl && (
                <div className="border-t border-slate-100">
                    <img
                        src={item.imageUrl}
                        alt="Post image"
                        className="w-full object-cover"
                    />
                </div>
            )}

            {/* Footer - Interactions */}
            <div className="flex items-center justify-between border-t border-slate-100 px-4 py-3">
                <div className="flex items-center gap-6">
                    <button className="flex items-center gap-2 text-sm text-slate-500 transition-colors hover:text-rose-500">
                        <Heart className="h-5 w-5" />
                        <span>{item.likes || 0}</span>
                    </button>
                    <button className="flex items-center gap-2 text-sm text-slate-500 transition-colors hover:text-teal-500">
                        <MessageCircle className="h-5 w-5" />
                        <span>{item.comments || 0}</span>
                    </button>
                    <button className="flex items-center gap-2 text-sm text-slate-500 transition-colors hover:text-blue-500">
                        <Share2 className="h-5 w-5" />
                    </button>
                </div>
                <button className="text-slate-400 transition-colors hover:text-slate-600">
                    <Bookmark className="h-5 w-5" />
                </button>
            </div>
        </article>
    );
}

// ============================================================================
// MISSION CARD COMPONENT
// ============================================================================
function MissionCard({ item }: FeedItemProps) {
    const timeAgo = getTimeAgo(item.createdAt);
    const mission = item.mission!;

    const urgencyConfig = {
        CRITICAL: { label: 'Urgent', className: 'bg-rose-100 text-rose-700 border-rose-200' },
        HIGH: { label: 'Prioritaire', className: 'bg-amber-100 text-amber-700 border-amber-200' },
        MEDIUM: { label: 'Normal', className: 'bg-slate-100 text-slate-700 border-slate-200' },
        LOW: { label: 'Flexible', className: 'bg-slate-100 text-slate-600 border-slate-200' },
    };

    const config = urgencyConfig[mission.urgency];

    return (
        <article className="overflow-hidden rounded-xl border border-slate-200 bg-white shadow-sm">
            {/* Urgency indicator bar */}
            {mission.urgency === 'CRITICAL' && (
                <div className="flex items-center gap-2 bg-rose-50 px-4 py-2 border-b border-rose-100">
                    <Zap className="h-4 w-4 text-rose-600" />
                    <span className="text-sm font-medium text-rose-700">Mission urgente</span>
                </div>
            )}

            {/* Header */}
            <div className="flex items-center gap-3 p-4">
                <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-teal-50 text-teal-600">
                    <Building2 className="h-6 w-6" />
                </div>
                <div className="flex-1">
                    <p className="font-semibold text-slate-900">{item.author.name}</p>
                    <p className="text-sm text-slate-500">recrute · {timeAgo}</p>
                </div>
                <Badge variant={mission.urgency === 'CRITICAL' ? 'destructive' : mission.urgency === 'HIGH' ? 'warning' : 'secondary'} size="sm">
                    {config.label}
                </Badge>
            </div>

            {/* Mission Details */}
            <div className="border-t border-slate-100 px-4 py-4">
                <h3 className="text-lg font-semibold text-slate-900">{mission.title}</h3>
                <div className="mt-2 flex flex-wrap items-center gap-4 text-sm text-slate-500">
                    <span className="flex items-center gap-1">
                        <Clock className="h-4 w-4" />
                        {mission.date}
                    </span>
                    <span className="flex items-center gap-1">
                        <MapPin className="h-4 w-4" />
                        {mission.city}
                    </span>
                </div>
                <p className="mt-3 text-2xl font-bold text-teal-600">
                    {mission.hourlyRate}€<span className="text-sm font-normal text-slate-500">/h</span>
                </p>
            </div>

            {/* Actions */}
            <div className="flex items-center justify-between border-t border-slate-100 px-4 py-3">
                <button className="text-sm font-medium text-slate-500 transition-colors hover:text-slate-700">
                    Voir l'établissement
                </button>
                <Link
                    href={`/sos`}
                    className="inline-flex items-center gap-2 rounded-full bg-teal-600 px-5 py-2 text-sm font-medium text-white transition-colors hover:bg-teal-700"
                >
                    Postuler
                    <ChevronRight className="h-4 w-4" />
                </Link>
            </div>
        </article>
    );
}

// ============================================================================
// HELPER FUNCTIONS
// ============================================================================
function getTimeAgo(date: Date): string {
    const now = new Date();
    const diffMs = now.getTime() - date.getTime();
    const diffMins = Math.floor(diffMs / (1000 * 60));
    const diffHours = Math.floor(diffMs / (1000 * 60 * 60));
    const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));

    if (diffMins < 60) return `il y a ${diffMins}m`;
    if (diffHours < 24) return `il y a ${diffHours}h`;
    if (diffDays < 7) return `il y a ${diffDays}j`;
    return date.toLocaleDateString('fr-FR', { day: 'numeric', month: 'short' });
}
