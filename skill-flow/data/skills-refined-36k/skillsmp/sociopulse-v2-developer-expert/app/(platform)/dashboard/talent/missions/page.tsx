'use client';

import { useState } from 'react';
import {
    Siren,
    MapPin,
    Clock,
    Euro,
    Building2,
    Calendar,
    Filter,
    Search,
    ChevronRight,
    AlertTriangle,
    CheckCircle2,
    XCircle,
    Hourglass,
    Zap,
    Users,
} from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle, Button, Badge, Input } from '@/components/ui';
import { cn } from '@/lib/utils';

// =============================================================================
// TYPES
// =============================================================================

type MissionUrgency = 'CRITICAL' | 'HIGH' | 'MEDIUM' | 'LOW';
type MissionStatus = 'OPEN' | 'APPLIED' | 'ASSIGNED' | 'IN_PROGRESS' | 'COMPLETED';

interface SOSMission {
    id: string;
    title: string;
    establishment: {
        name: string;
        type: string;
        logoUrl?: string;
    };
    location: {
        city: string;
        postalCode: string;
        distance?: string;
    };
    schedule: {
        date: string;
        startTime: string;
        endTime: string;
    };
    compensation: {
        amount: number;
        unit: 'hour' | 'mission';
    };
    urgency: MissionUrgency;
    status: MissionStatus;
    description: string;
    requirements?: string[];
    applicationsCount: number;
}

// =============================================================================
// MOCK DATA
// =============================================================================

const mockMissions: SOSMission[] = [
    {
        id: '1',
        title: 'Renfort Aide-Soignant(e)',
        establishment: { name: 'EHPAD Les Tilleuls', type: 'EHPAD' },
        location: { city: 'Lyon', postalCode: '69003', distance: '3.2 km' },
        schedule: { date: '2026-01-21', startTime: '07:00', endTime: '15:00' },
        compensation: { amount: 180, unit: 'mission' },
        urgency: 'CRITICAL',
        status: 'OPEN',
        description: 'Renfort urgent suite absence. Équipe de 3 AS. Soins de nursing classiques.',
        requirements: ['DEAS', 'Expérience EHPAD'],
        applicationsCount: 2,
    },
    {
        id: '2',
        title: 'Éducateur Spécialisé - Week-end',
        establishment: { name: 'MECS Horizon', type: 'MECS' },
        location: { city: 'Villeurbanne', postalCode: '69100', distance: '5.1 km' },
        schedule: { date: '2026-01-25', startTime: '09:00', endTime: '21:00' },
        compensation: { amount: 220, unit: 'mission' },
        urgency: 'HIGH',
        status: 'OPEN',
        description: 'Accompagnement groupe 8-12 ans. Activités week-end.',
        requirements: ['DEES', 'Permis B'],
        applicationsCount: 5,
    },
    {
        id: '3',
        title: 'Moniteur Éducateur - Nuit',
        establishment: { name: 'Foyer Le Phare', type: 'Foyer' },
        location: { city: 'Bron', postalCode: '69500', distance: '8.4 km' },
        schedule: { date: '2026-01-22', startTime: '21:00', endTime: '07:00' },
        compensation: { amount: 25, unit: 'hour' },
        urgency: 'MEDIUM',
        status: 'APPLIED',
        description: 'Veille active foyer jeunes majeurs. 12 résidents.',
        applicationsCount: 3,
    },
];

const myActiveMissions: SOSMission[] = [
    {
        id: '4',
        title: 'Renfort AS - Confirmé',
        establishment: { name: 'SSIAD Rhône', type: 'SSIAD' },
        location: { city: 'Lyon', postalCode: '69007' },
        schedule: { date: '2026-01-23', startTime: '08:00', endTime: '16:00' },
        compensation: { amount: 200, unit: 'mission' },
        urgency: 'MEDIUM',
        status: 'ASSIGNED',
        description: 'Tournée domicile secteur Lyon 7ème.',
        applicationsCount: 0,
    },
];

// =============================================================================
// COMPONENTS
// =============================================================================

function UrgencyBadge({ urgency }: { urgency: MissionUrgency }) {
    const styles = {
        CRITICAL: 'bg-rose-100 text-rose-700 border-rose-200 animate-pulse',
        HIGH: 'bg-orange-100 text-orange-700 border-orange-200',
        MEDIUM: 'bg-amber-100 text-amber-700 border-amber-200',
        LOW: 'bg-slate-100 text-slate-600 border-slate-200',
    };

    const labels = {
        CRITICAL: '🚨 Immédiat',
        HIGH: '⚡ Sous 24h',
        MEDIUM: '📅 Sous 48h',
        LOW: '📆 Planifié',
    };

    return (
        <span className={cn('px-2 py-1 text-xs font-bold rounded-full border', styles[urgency])}>
            {labels[urgency]}
        </span>
    );
}

function StatusBadge({ status }: { status: MissionStatus }) {
    const config = {
        OPEN: { label: 'Ouverte', icon: Zap, className: 'bg-emerald-100 text-emerald-700' },
        APPLIED: { label: 'Candidature envoyée', icon: Hourglass, className: 'bg-blue-100 text-blue-700' },
        ASSIGNED: { label: 'Confirmée', icon: CheckCircle2, className: 'bg-teal-100 text-teal-700' },
        IN_PROGRESS: { label: 'En cours', icon: Clock, className: 'bg-indigo-100 text-indigo-700' },
        COMPLETED: { label: 'Terminée', icon: CheckCircle2, className: 'bg-slate-100 text-slate-600' },
    };

    const { label, icon: Icon, className } = config[status];

    return (
        <span className={cn('inline-flex items-center gap-1 px-2 py-1 text-xs font-semibold rounded-full', className)}>
            <Icon size={12} />
            {label}
        </span>
    );
}

function MissionCard({ mission, variant = 'available' }: { mission: SOSMission; variant?: 'available' | 'active' }) {
    const formatDate = (dateStr: string) => {
        const date = new Date(dateStr);
        return date.toLocaleDateString('fr-FR', { weekday: 'short', day: 'numeric', month: 'short' });
    };

    return (
        <Card className={cn(
            'border-2 transition-all duration-200 hover:shadow-lg',
            mission.urgency === 'CRITICAL' ? 'border-rose-300 bg-rose-50/30' :
            mission.urgency === 'HIGH' ? 'border-orange-200' : 'border-slate-200'
        )}>
            <CardContent className="p-5">
                {/* Header */}
                <div className="flex items-start justify-between mb-4">
                    <div className="flex items-start gap-3">
                        <div className="p-2 bg-slate-100 rounded-lg">
                            <Building2 size={20} className="text-slate-600" />
                        </div>
                        <div>
                            <h3 className="font-bold text-slate-900">{mission.title}</h3>
                            <p className="text-sm text-slate-500">{mission.establishment.name}</p>
                        </div>
                    </div>
                    <div className="flex flex-col items-end gap-2">
                        <UrgencyBadge urgency={mission.urgency} />
                        {variant === 'active' && <StatusBadge status={mission.status} />}
                    </div>
                </div>

                {/* Details Grid */}
                <div className="grid grid-cols-2 gap-3 mb-4">
                    <div className="flex items-center gap-2 text-sm text-slate-600">
                        <Calendar size={16} className="text-slate-400" />
                        <span>{formatDate(mission.schedule.date)}</span>
                    </div>
                    <div className="flex items-center gap-2 text-sm text-slate-600">
                        <Clock size={16} className="text-slate-400" />
                        <span>{mission.schedule.startTime} - {mission.schedule.endTime}</span>
                    </div>
                    <div className="flex items-center gap-2 text-sm text-slate-600">
                        <MapPin size={16} className="text-slate-400" />
                        <span>{mission.location.city} ({mission.location.postalCode})</span>
                    </div>
                    <div className="flex items-center gap-2 text-sm font-semibold text-emerald-600">
                        <Euro size={16} />
                        <span>{mission.compensation.amount}€ / {mission.compensation.unit === 'hour' ? 'h' : 'mission'}</span>
                    </div>
                </div>

                {/* Description */}
                <p className="text-sm text-slate-600 mb-4 line-clamp-2">{mission.description}</p>

                {/* Requirements */}
                {mission.requirements && mission.requirements.length > 0 && (
                    <div className="flex flex-wrap gap-2 mb-4">
                        {mission.requirements.map((req, i) => (
                            <span key={i} className="px-2 py-1 text-xs bg-slate-100 text-slate-600 rounded-md">
                                {req}
                            </span>
                        ))}
                    </div>
                )}

                {/* Actions */}
                <div className="flex items-center justify-between pt-4 border-t border-slate-100">
                    {variant === 'available' && (
                        <>
                            <div className="flex items-center gap-1 text-sm text-slate-500">
                                <Users size={14} />
                                <span>{mission.applicationsCount} candidature(s)</span>
                            </div>
                            {mission.status === 'OPEN' ? (
                                <Button className="bg-rose-600 hover:bg-rose-700 text-white">
                                    Postuler <ChevronRight size={16} />
                                </Button>
                            ) : (
                                <span className="text-sm text-blue-600 font-medium">Candidature en cours...</span>
                            )}
                        </>
                    )}
                    {variant === 'active' && (
                        <>
                            <Button variant="outline" className="text-slate-600">
                                Voir détails
                            </Button>
                            <Button className="bg-teal-600 hover:bg-teal-700 text-white">
                                Accéder au Mission Hub
                            </Button>
                        </>
                    )}
                </div>
            </CardContent>
        </Card>
    );
}

// =============================================================================
// PAGE
// =============================================================================

export default function TalentMissionsPage() {
    const [filter, setFilter] = useState<'all' | 'critical' | 'today'>('all');
    const [searchQuery, setSearchQuery] = useState('');

    const filteredMissions = mockMissions.filter((mission) => {
        if (filter === 'critical' && mission.urgency !== 'CRITICAL') return false;
        if (filter === 'today') {
            const today = new Date().toISOString().split('T')[0];
            if (mission.schedule.date !== today) return false;
        }
        if (searchQuery) {
            const query = searchQuery.toLowerCase();
            return (
                mission.title.toLowerCase().includes(query) ||
                mission.establishment.name.toLowerCase().includes(query) ||
                mission.location.city.toLowerCase().includes(query)
            );
        }
        return true;
    });

    return (
        <div className="space-y-6 max-w-6xl mx-auto">
            {/* Header */}
            <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
                <div>
                    <h1 className="text-2xl font-bold text-slate-900 flex items-center gap-2">
                        <Siren className="text-rose-500" />
                        Missions SOS
                    </h1>
                    <p className="text-slate-500 mt-1">Flux Chaud - Renforts urgents disponibles</p>
                </div>
                <div className="flex items-center gap-2 px-4 py-2 bg-rose-50 border border-rose-200 rounded-xl">
                    <AlertTriangle size={18} className="text-rose-500" />
                    <span className="text-sm font-medium text-rose-700">
                        {mockMissions.filter(m => m.urgency === 'CRITICAL').length} mission(s) critique(s)
                    </span>
                </div>
            </div>

            {/* Filters */}
            <Card className="border-slate-200">
                <CardContent className="p-4">
                    <div className="flex flex-col sm:flex-row gap-4">
                        <div className="relative flex-1">
                            <Search size={18} className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
                            <Input
                                placeholder="Rechercher par ville, établissement..."
                                value={searchQuery}
                                onChange={(e) => setSearchQuery(e.target.value)}
                                className="pl-10"
                            />
                        </div>
                        <div className="flex gap-2">
                            {[
                                { key: 'all', label: 'Toutes' },
                                { key: 'critical', label: '🚨 Critiques' },
                                { key: 'today', label: "Aujourd'hui" },
                            ].map((f) => (
                                <button
                                    key={f.key}
                                    onClick={() => setFilter(f.key as typeof filter)}
                                    className={cn(
                                        'px-4 py-2 text-sm font-medium rounded-lg transition-colors',
                                        filter === f.key
                                            ? 'bg-rose-100 text-rose-700'
                                            : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
                                    )}
                                >
                                    {f.label}
                                </button>
                            ))}
                        </div>
                    </div>
                </CardContent>
            </Card>

            {/* My Active Missions */}
            {myActiveMissions.length > 0 && (
                <div>
                    <h2 className="text-lg font-semibold text-slate-900 mb-4 flex items-center gap-2">
                        <CheckCircle2 className="text-teal-500" size={20} />
                        Mes missions confirmées
                    </h2>
                    <div className="grid grid-cols-1 gap-4">
                        {myActiveMissions.map((mission) => (
                            <MissionCard key={mission.id} mission={mission} variant="active" />
                        ))}
                    </div>
                </div>
            )}

            {/* Available Missions */}
            <div>
                <h2 className="text-lg font-semibold text-slate-900 mb-4 flex items-center gap-2">
                    <Zap className="text-amber-500" size={20} />
                    Missions disponibles ({filteredMissions.length})
                </h2>
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
                    {filteredMissions.map((mission) => (
                        <MissionCard key={mission.id} mission={mission} variant="available" />
                    ))}
                </div>
                {filteredMissions.length === 0 && (
                    <Card className="border-slate-200">
                        <CardContent className="p-12 text-center">
                            <Siren size={48} className="mx-auto text-slate-300 mb-4" />
                            <h3 className="text-lg font-semibold text-slate-700">Aucune mission trouvée</h3>
                            <p className="text-slate-500 mt-1">Ajustez vos filtres ou revenez plus tard</p>
                        </CardContent>
                    </Card>
                )}
            </div>
        </div>
    );
}
