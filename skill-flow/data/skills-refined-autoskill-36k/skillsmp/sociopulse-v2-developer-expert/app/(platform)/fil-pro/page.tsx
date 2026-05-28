'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';
import {
    User,
    Briefcase,
    MapPin,
    Star,
    TrendingUp,
    Users,
    Zap
} from 'lucide-react';
import { Badge } from '@/components/ui';
import { FeedItem, type FeedItemType } from '@/components/feed/FeedItem';
import { UserIdentityCard } from '@/components/feed/UserIdentityCard';
import { FeedSuggestions } from '@/components/feed/FeedSuggestions';

// Mock feed data
const mockFeedItems: FeedItemType[] = [
    {
        id: '1',
        type: 'mission',
        author: {
            name: 'EHPAD Les Mimosas',
            avatarUrl: null,
            role: 'Établissement',
        },
        mission: {
            title: 'Infirmier(ère) de Nuit',
            date: '14 Fév 2026, 20h - 06h',
            hourlyRate: 35,
            city: 'Lyon 3ème',
            urgency: 'HIGH',
        },
        createdAt: new Date('2026-01-20T10:00:00'),
    },
    {
        id: '2',
        type: 'social',
        author: {
            name: 'Marie Lambert',
            avatarUrl: null,
            role: 'Aide-soignante',
        },
        content: 'Très belle expérience cette semaine à l\'EHPAD Les Jardins ! Une équipe formidable et des résidents adorables. Merci @SocioPulse pour cette mission 🙏',
        imageUrl: null,
        likes: 24,
        comments: 5,
        createdAt: new Date('2026-01-19T15:30:00'),
    },
    {
        id: '3',
        type: 'mission',
        author: {
            name: 'IME Soleil Levant',
            avatarUrl: null,
            role: 'Établissement',
        },
        mission: {
            title: 'Éducateur Spécialisé - Vacances',
            date: '27 Jan - 31 Jan 2026',
            hourlyRate: 28,
            city: 'Villeurbanne',
            urgency: 'MEDIUM',
        },
        createdAt: new Date('2026-01-19T09:00:00'),
    },
    {
        id: '4',
        type: 'social',
        author: {
            name: 'Thomas Durand',
            avatarUrl: null,
            role: 'Éducateur spécialisé',
        },
        content: 'Nouvelle certification obtenue en accompagnement des personnes autistes ! Toujours en formation pour offrir le meilleur accompagnement possible. 📚✨',
        imageUrl: null,
        likes: 47,
        comments: 12,
        createdAt: new Date('2026-01-18T11:00:00'),
    },
];

const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
        opacity: 1,
        transition: { staggerChildren: 0.1 }
    }
};

const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: { opacity: 1, y: 0 }
};

export default function FilProPage() {
    const [feedItems] = useState(mockFeedItems);
    const isEmpty = feedItems.length === 0;

    return (
        <div className="min-h-screen bg-slate-50">
            <div className="mx-auto max-w-7xl px-4 py-6">
                {/* 3-Column Grid Layout */}
                <div className="grid grid-cols-1 gap-6 lg:grid-cols-12">
                    {/* Left Column - User Identity (Hidden on mobile) */}
                    <aside className="hidden lg:col-span-3 lg:block">
                        <div className="sticky top-20">
                            <UserIdentityCard />
                        </div>
                    </aside>

                    {/* Center Column - Feed */}
                    <main className="lg:col-span-6">
                        {isEmpty ? (
                            <EmptyState />
                        ) : (
                            <motion.div
                                variants={containerVariants}
                                initial="hidden"
                                animate="visible"
                                className="space-y-4"
                            >
                                {feedItems.map((item) => (
                                    <motion.div key={item.id} variants={itemVariants}>
                                        <FeedItem item={item} />
                                    </motion.div>
                                ))}
                            </motion.div>
                        )}
                    </main>

                    {/* Right Column - Suggestions (Hidden on mobile) */}
                    <aside className="hidden lg:col-span-3 lg:block">
                        <div className="sticky top-20">
                            <FeedSuggestions />
                        </div>
                    </aside>
                </div>
            </div>
        </div>
    );
}

function EmptyState() {
    return (
        <div className="flex flex-col items-center justify-center rounded-xl border border-dashed border-slate-200 bg-white p-12 text-center">
            <div className="flex h-16 w-16 items-center justify-center rounded-full bg-slate-100">
                <TrendingUp className="h-8 w-8 text-slate-400" />
            </div>
            <h3 className="mt-4 text-lg font-semibold text-slate-900">
                Aucune actualité pour le moment
            </h3>
            <p className="mt-2 max-w-sm text-sm text-slate-500">
                Suivez des talents et des établissements pour voir leurs publications ici.
            </p>
            <button className="mt-6 inline-flex items-center gap-2 rounded-full bg-teal-600 px-5 py-2.5 text-sm font-medium text-white transition-colors hover:bg-teal-700">
                <Users className="h-4 w-4" />
                Découvrir des talents
            </button>
        </div>
    );
}
