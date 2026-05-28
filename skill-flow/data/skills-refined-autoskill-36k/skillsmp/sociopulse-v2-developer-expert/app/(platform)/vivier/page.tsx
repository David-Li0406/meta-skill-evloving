'use client';

import { useState } from 'react';
import Link from 'next/link';
import { Search, MapPin, Star, Filter, Upload } from 'lucide-react';
import { TalentImportModal } from '@/components/vivier/TalentImportModal';
import { useAuth } from '@/lib/useAuth';

// Mock Data for Talent Pool
const MOCK_TALENTS = [
    {
        id: '1',
        name: 'Marie Dupont',
        role: 'Éducatrice Spécialisée',
        city: 'Lyon 3e',
        rating: 4.8,
        reviews: 24,
        avatar: null,
        tags: ['Autisme', 'EHPAD'],
        isAvailable: true
    },
    {
        id: '2',
        name: 'Thomas Martin',
        role: 'Coach Sportif Adapté',
        city: 'Toulouse',
        rating: 4.9,
        reviews: 47,
        avatar: null,
        tags: ['Sport', 'Handicap'],
        isAvailable: true
    },
    {
        id: '3',
        name: 'Sophie Laurent',
        role: 'Musicothérapeute',
        city: 'Paris 15e',
        rating: 4.7,
        reviews: 12,
        avatar: null,
        tags: ['Musique', 'Art-thérapie'],
        isAvailable: false
    },
    {
        id: '4',
        name: 'Lucas Bernard',
        role: 'Aide-Soignant',
        city: 'Marseille',
        rating: 4.5,
        reviews: 8,
        avatar: null,
        tags: ['Nuite', 'Gériatrie'],
        isAvailable: true
    }
];

export default function VivierPage() {
    const [search, setSearch] = useState('');
    const [isImportModalOpen, setIsImportModalOpen] = useState(false);
    const { user } = useAuth(); // Assuming useAuth gives us the current user/establisment

    // Fallback ID if not found (in a real app, strict auth logic prevents this)
    const establishmentId = user?.establishment?.id || "demo-establishment-id";

    const filteredTalents = MOCK_TALENTS.filter(t =>
        t.name.toLowerCase().includes(search.toLowerCase()) ||
        t.role.toLowerCase().includes(search.toLowerCase()) ||
        t.city.toLowerCase().includes(search.toLowerCase())
    );

    return (
        <div className="min-h-screen bg-slate-50 pb-20">
            <TalentImportModal
                isOpen={isImportModalOpen}
                onClose={() => setIsImportModalOpen(false)}
                establishmentId={establishmentId}
            />

            {/* Header */}
            <div className="bg-white border-b border-slate-100 sticky top-0 z-30">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
                    <div className="flex items-center justify-between">
                        <div className="flex items-center gap-4">
                            <Link href="/" className="p-2 -ml-2 rounded-xl hover:bg-slate-50 text-slate-500">
                                ← Retour
                            </Link>
                            <h1 className="text-xl font-bold text-slate-900">Mon Vivier</h1>
                        </div>
                        <button
                            onClick={() => setIsImportModalOpen(true)}
                            className="flex items-center gap-2 px-4 py-2 bg-brand-600 hover:bg-brand-700 text-white rounded-xl font-medium transition-colors shadow-sm shadow-brand-200"
                        >
                            <Upload className="w-4 h-4" />
                            <span className="hidden sm:inline">Importer</span>
                        </button>
                    </div>


                    {/* Search Bar */}
                    <div className="mt-4 relative">
                        <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
                        <input
                            type="text"
                            placeholder="Rechercher par nom, rôle ou ville..."
                            value={search}
                            onChange={(e) => setSearch(e.target.value)}
                            className="w-full pl-10 pr-4 py-3 rounded-xl bg-slate-100 border-none focus:ring-2 focus:ring-brand-500 transition-shadow"
                        />
                        <button className="absolute right-3 top-1/2 -translate-y-1/2 p-1.5 rounded-lg hover:bg-white/50 text-slate-500">
                            <Filter className="w-5 h-5" />
                        </button>
                    </div>
                </div>
            </div>

            {/* List */}
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                    {filteredTalents.map((talent) => (
                        <Link
                            key={talent.id}
                            href={`/profile/${talent.id}`}
                            className="group block bg-white rounded-2xl p-4 border border-slate-100 shadow-sm hover:shadow-md transition-all active:scale-[0.98]"
                        >
                            <div className="flex items-start gap-4">
                                <div className="w-16 h-16 rounded-full bg-gradient-to-br from-brand-100 to-brand-50 flex items-center justify-center flex-shrink-0">
                                    <span className="text-xl font-bold text-brand-600">
                                        {talent.name.charAt(0)}
                                    </span>
                                </div>
                                <div className="flex-1 min-w-0">
                                    <h3 className="font-semibold text-slate-900 group-hover:text-brand-600 transition-colors">
                                        {talent.name}
                                    </h3>
                                    <p className="text-sm text-brand-600 font-medium mb-1">{talent.role}</p>
                                    <div className="flex items-center gap-2 text-xs text-slate-500 mb-2">
                                        <span className="flex items-center gap-1">
                                            <MapPin className="w-3 h-3" />
                                            {talent.city}
                                        </span>
                                        <span className="flex items-center gap-1">
                                            <Star className="w-3 h-3 text-amber-400 fill-amber-400" />
                                            {talent.rating} ({talent.reviews})
                                        </span>
                                    </div>
                                    <div className="flex flex-wrap gap-1">
                                        {talent.tags.map(tag => (
                                            <span key={tag} className="px-2 py-0.5 rounded-md bg-slate-50 text-slate-600 text-[10px] font-medium border border-slate-100">
                                                {tag}
                                            </span>
                                        ))}
                                    </div>
                                </div>
                            </div>
                        </Link>
                    ))}
                </div>

                {filteredTalents.length === 0 && (
                    <div className="text-center py-12">
                        <p className="text-slate-500">Aucun talent trouvé pour "{search}"</p>
                    </div>
                )}
            </div>
        </div>
    );
}
