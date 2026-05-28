'use client';

import { useState } from 'react';
import { Plus, Calendar as CalendarIcon, Video, Users, List, Grid, ExternalLink } from 'lucide-react';
import { UnifiedCalendar } from '@/components/planning';

type ViewMode = 'cards' | 'calendar';
type TabType = 'workshops' | 'coaching' | 'history';

export default function ClientBookingsPage() {
    const [activeTab, setActiveTab] = useState<TabType>('workshops');
    const [viewMode, setViewMode] = useState<ViewMode>('cards');

    return (
        <div className="p-6 space-y-6">
            <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
                <div>
                    <h1 className="text-2xl font-bold text-slate-900">
                        Réservations
                    </h1>
                    <p className="text-slate-600">
                        Gérez vos ateliers et séances de coaching vidéo réservés.
                    </p>
                </div>
                <div className="flex items-center gap-3">
                    {/* View Toggle */}
                    <div className="flex items-center bg-slate-100 rounded-lg p-1">
                        <button
                            onClick={() => setViewMode('cards')}
                            className={`p-2 rounded-md transition-colors ${
                                viewMode === 'cards'
                                    ? 'bg-white shadow-sm text-slate-900'
                                    : 'text-slate-500 hover:text-slate-700'
                            }`}
                            aria-label="Vue en cartes"
                        >
                            <Grid className="h-4 w-4" />
                        </button>
                        <button
                            onClick={() => setViewMode('calendar')}
                            className={`p-2 rounded-md transition-colors ${
                                viewMode === 'calendar'
                                    ? 'bg-white shadow-sm text-slate-900'
                                    : 'text-slate-500 hover:text-slate-700'
                            }`}
                            aria-label="Vue calendrier"
                        >
                            <CalendarIcon className="h-4 w-4" />
                        </button>
                    </div>
                    <button className="inline-flex items-center gap-2 rounded-lg bg-emerald-600 px-4 py-2 text-sm font-medium text-white hover:bg-emerald-700">
                        <Plus className="h-4 w-4" />
                        Nouvelle Réservation
                    </button>
                </div>
            </div>

            {/* Tabs */}
            <div className="flex gap-4 border-b border-slate-200">
                <TabButton 
                    label="Ateliers" 
                    icon={Users} 
                    active={activeTab === 'workshops'}
                    onClick={() => setActiveTab('workshops')}
                />
                <TabButton 
                    label="Coaching Vidéo" 
                    icon={Video}
                    active={activeTab === 'coaching'}
                    onClick={() => setActiveTab('coaching')}
                />
                <TabButton 
                    label="Historique" 
                    icon={CalendarIcon}
                    active={activeTab === 'history'}
                    onClick={() => setActiveTab('history')}
                />
            </div>

            {/* Calendar View */}
            {viewMode === 'calendar' ? (
                <div className="bg-white rounded-xl border border-slate-200 p-4">
                    <UnifiedCalendar userRole="CLIENT" />
                </div>
            ) : (
                /* Card View */
                <div className="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3">
                    {activeTab === 'workshops' && (
                        <>
                            <BookingCard
                                title="Art-thérapie Séniors"
                                provider="Sophie Martin"
                                date="Ven 24 Jan, 14h00"
                                duration="2h"
                                status="CONFIRMED"
                                type="workshop"
                            />
                            <BookingCard
                                title="Musicothérapie"
                                provider="Claire Dubois"
                                date="Mar 28 Jan, 15h00"
                                duration="3h"
                                status="CONFIRMED"
                                type="workshop"
                            />
                        </>
                    )}
                    {activeTab === 'coaching' && (
                        <>
                            <BookingCard
                                title="Coaching Gestion de crise"
                                provider="Dr. Pierre Duval"
                                date="Lun 27 Jan, 10h00"
                                duration="1h"
                                status="PENDING"
                                type="video"
                            />
                            <BookingCard
                                title="Supervision d&apos;équipe"
                                provider="Marie Laurent"
                                date="Mer 29 Jan, 14h30"
                                duration="1h30"
                                status="CONFIRMED"
                                type="video"
                                showJoin
                            />
                        </>
                    )}
                    {activeTab === 'history' && (
                        <div className="col-span-full text-center py-12 text-slate-500">
                            <CalendarIcon className="h-12 w-12 mx-auto mb-4 opacity-50" />
                            <p>Aucune réservation passée</p>
                        </div>
                    )}
                </div>
            )}
        </div>
    );
}

interface TabButtonProps {
    label: string;
    icon: React.ElementType;
    active?: boolean;
    onClick?: () => void;
}

function TabButton({ label, icon: Icon, active, onClick }: TabButtonProps) {
    return (
        <button
            onClick={onClick}
            className={`flex items-center gap-2 border-b-2 px-4 py-3 text-sm font-medium transition-colors ${active
                    ? 'border-emerald-600 text-emerald-600'
                    : 'border-transparent text-slate-500 hover:text-slate-700'
                }`}
        >
            <Icon className="h-4 w-4" />
            {label}
        </button>
    );
}

interface BookingCardProps {
    title: string;
    provider: string;
    date: string;
    duration: string;
    status: string;
    type: 'workshop' | 'video';
    showJoin?: boolean;
}

function BookingCard({ title, provider, date, duration, status, type, showJoin }: BookingCardProps) {
    const statusColors: Record<string, string> = {
        PENDING: 'bg-yellow-100 text-yellow-700',
        CONFIRMED: 'bg-green-100 text-green-700',
        COMPLETED: 'bg-slate-100 text-slate-700',
        CANCELLED: 'bg-red-100 text-red-700',
    };

    const statusLabels: Record<string, string> = {
        PENDING: 'En attente',
        CONFIRMED: 'Confirmé',
        COMPLETED: 'Terminé',
        CANCELLED: 'Annulé',
    };

    return (
        <div className="rounded-lg border border-slate-200 bg-white p-4">
            <div className="flex items-start justify-between">
                <div className="flex items-center gap-2">
                    {type === 'video' ? (
                        <Video className="h-5 w-5 text-blue-500" />
                    ) : (
                        <Users className="h-5 w-5 text-emerald-500" />
                    )}
                    <span className={`rounded-full px-2 py-0.5 text-xs font-medium ${statusColors[status]}`}>
                        {statusLabels[status]}
                    </span>
                </div>
            </div>
            <h3 className="mt-3 font-semibold text-slate-900">{title}</h3>
            <p className="text-sm text-slate-500">par {provider}</p>
            <div className="mt-3 flex items-center gap-4 text-sm text-slate-600">
                <span className="flex items-center gap-1">
                    <CalendarIcon className="h-4 w-4" />
                    {date}
                </span>
                <span>{duration}</span>
            </div>
            
            {/* Join Button for Video Sessions */}
            {showJoin && type === 'video' && status === 'CONFIRMED' && (
                <button 
                    className="mt-4 w-full inline-flex items-center justify-center gap-2 rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700 transition-colors"
                    onClick={() => {
                        // Navigate to LiveKit room
                        window.location.href = '/live-session/booking-123';
                    }}
                >
                    <Video className="h-4 w-4" />
                    Rejoindre la session
                    <ExternalLink className="h-3 w-3" />
                </button>
            )}
        </div>
    );
}