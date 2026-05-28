'use client';

import { useState } from 'react';
import Link from 'next/link';
import {
    Package,
    Plus,
    Video,
    Users,
    Calendar,
    Euro,
    Star,
    Edit2,
    Trash2,
    Eye,
    EyeOff,
    MoreVertical,
    Clock,
    MapPin,
    ChevronRight,
    Sparkles,
    BookOpen,
} from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle, Button, Badge, Input } from '@/components/ui';
import { cn } from '@/lib/utils';

// =============================================================================
// TYPES
// =============================================================================

type ServiceType = 'WORKSHOP' | 'COACHING_VIDEO';
type ServiceStatus = 'ACTIVE' | 'DRAFT' | 'PAUSED';

interface TalentService {
    id: string;
    title: string;
    type: ServiceType;
    status: ServiceStatus;
    description: string;
    price: number;
    duration: number; // minutes
    category: string;
    bookingsCount: number;
    rating?: number;
    reviewsCount?: number;
    imageUrl?: string;
    isOnline: boolean;
    location?: string;
    maxParticipants?: number;
}

// =============================================================================
// MOCK DATA
// =============================================================================

const mockServices: TalentService[] = [
    {
        id: '1',
        title: 'Atelier Gestion du Stress',
        type: 'WORKSHOP',
        status: 'ACTIVE',
        description: 'Techniques de relaxation et gestion émotionnelle pour équipes médico-sociales.',
        price: 350,
        duration: 120,
        category: 'Bien-être',
        bookingsCount: 12,
        rating: 4.9,
        reviewsCount: 8,
        isOnline: false,
        location: 'Lyon et alentours',
        maxParticipants: 15,
    },
    {
        id: '2',
        title: 'Coaching Orientation Carrière',
        type: 'COACHING_VIDEO',
        status: 'ACTIVE',
        description: 'Accompagnement individuel pour professionnels du social en reconversion.',
        price: 75,
        duration: 60,
        category: 'Développement Pro',
        bookingsCount: 24,
        rating: 4.8,
        reviewsCount: 18,
        isOnline: true,
    },
    {
        id: '3',
        title: 'Formation Communication Non-Violente',
        type: 'WORKSHOP',
        status: 'DRAFT',
        description: 'Initiation à la CNV pour améliorer les relations en équipe.',
        price: 450,
        duration: 180,
        category: 'Formation',
        bookingsCount: 0,
        isOnline: false,
        location: 'Rhône-Alpes',
        maxParticipants: 12,
    },
    {
        id: '4',
        title: 'Supervision Pratique Éducative',
        type: 'COACHING_VIDEO',
        status: 'PAUSED',
        description: 'Analyse de pratique en visio pour éducateurs spécialisés.',
        price: 60,
        duration: 45,
        category: 'Supervision',
        bookingsCount: 6,
        rating: 4.7,
        reviewsCount: 4,
        isOnline: true,
    },
];

// =============================================================================
// COMPONENTS
// =============================================================================

function ServiceTypeBadge({ type }: { type: ServiceType }) {
    const config = {
        WORKSHOP: { label: 'Atelier', icon: Users, className: 'bg-indigo-100 text-indigo-700' },
        COACHING_VIDEO: { label: 'Coaching Vidéo', icon: Video, className: 'bg-teal-100 text-teal-700' },
    };

    const { label, icon: Icon, className } = config[type];

    return (
        <span className={cn('inline-flex items-center gap-1.5 px-2.5 py-1 text-xs font-semibold rounded-full', className)}>
            <Icon size={12} />
            {label}
        </span>
    );
}

function ServiceStatusBadge({ status }: { status: ServiceStatus }) {
    const config = {
        ACTIVE: { label: 'Actif', icon: Eye, className: 'bg-emerald-100 text-emerald-700' },
        DRAFT: { label: 'Brouillon', icon: Edit2, className: 'bg-amber-100 text-amber-700' },
        PAUSED: { label: 'Pausé', icon: EyeOff, className: 'bg-slate-100 text-slate-600' },
    };

    const { label, icon: Icon, className } = config[status];

    return (
        <span className={cn('inline-flex items-center gap-1 px-2 py-0.5 text-xs font-medium rounded-md', className)}>
            <Icon size={10} />
            {label}
        </span>
    );
}

function ServiceCard({ service }: { service: TalentService }) {
    const [menuOpen, setMenuOpen] = useState(false);

    return (
        <Card className={cn(
            'border-2 transition-all duration-200 hover:shadow-lg relative overflow-hidden',
            service.status === 'ACTIVE' ? 'border-slate-200' :
            service.status === 'DRAFT' ? 'border-amber-200 bg-amber-50/20' :
            'border-slate-200 opacity-75'
        )}>
            {/* Decorative Top Border */}
            <div className={cn(
                'h-1 w-full',
                service.type === 'WORKSHOP' ? 'bg-gradient-to-r from-indigo-500 to-purple-500' :
                'bg-gradient-to-r from-teal-500 to-emerald-500'
            )} />

            <CardContent className="p-5">
                {/* Header */}
                <div className="flex items-start justify-between mb-3">
                    <div className="flex items-start gap-3">
                        <div className={cn(
                            'p-2.5 rounded-xl',
                            service.type === 'WORKSHOP' ? 'bg-indigo-100' : 'bg-teal-100'
                        )}>
                            {service.type === 'WORKSHOP' ? (
                                <Users size={20} className="text-indigo-600" />
                            ) : (
                                <Video size={20} className="text-teal-600" />
                            )}
                        </div>
                        <div>
                            <h3 className="font-bold text-slate-900 line-clamp-1">{service.title}</h3>
                            <div className="flex items-center gap-2 mt-1">
                                <ServiceTypeBadge type={service.type} />
                                <ServiceStatusBadge status={service.status} />
                            </div>
                        </div>
                    </div>
                    <div className="relative">
                        <button
                            onClick={() => setMenuOpen(!menuOpen)}
                            className="p-1.5 rounded-lg hover:bg-slate-100 text-slate-400"
                        >
                            <MoreVertical size={18} />
                        </button>
                        {menuOpen && (
                            <div className="absolute right-0 top-8 w-40 bg-white border border-slate-200 rounded-xl shadow-lg z-10 py-1">
                                <button className="w-full px-4 py-2 text-left text-sm hover:bg-slate-50 flex items-center gap-2">
                                    <Edit2 size={14} /> Modifier
                                </button>
                                <button className="w-full px-4 py-2 text-left text-sm hover:bg-slate-50 flex items-center gap-2">
                                    {service.status === 'PAUSED' ? <Eye size={14} /> : <EyeOff size={14} />}
                                    {service.status === 'PAUSED' ? 'Réactiver' : 'Mettre en pause'}
                                </button>
                                <button className="w-full px-4 py-2 text-left text-sm hover:bg-rose-50 text-rose-600 flex items-center gap-2">
                                    <Trash2 size={14} /> Supprimer
                                </button>
                            </div>
                        )}
                    </div>
                </div>

                {/* Description */}
                <p className="text-sm text-slate-600 mb-4 line-clamp-2">{service.description}</p>

                {/* Meta Info */}
                <div className="grid grid-cols-2 gap-2 mb-4">
                    <div className="flex items-center gap-2 text-sm text-slate-600">
                        <Euro size={14} className="text-slate-400" />
                        <span className="font-semibold text-emerald-600">{service.price}€</span>
                    </div>
                    <div className="flex items-center gap-2 text-sm text-slate-600">
                        <Clock size={14} className="text-slate-400" />
                        <span>{service.duration} min</span>
                    </div>
                    {service.isOnline ? (
                        <div className="flex items-center gap-2 text-sm text-slate-600">
                            <Video size={14} className="text-teal-500" />
                            <span>En ligne</span>
                        </div>
                    ) : (
                        <div className="flex items-center gap-2 text-sm text-slate-600">
                            <MapPin size={14} className="text-slate-400" />
                            <span className="truncate">{service.location}</span>
                        </div>
                    )}
                    {service.maxParticipants && (
                        <div className="flex items-center gap-2 text-sm text-slate-600">
                            <Users size={14} className="text-slate-400" />
                            <span>Max {service.maxParticipants} pers.</span>
                        </div>
                    )}
                </div>

                {/* Stats */}
                <div className="flex items-center justify-between pt-4 border-t border-slate-100">
                    <div className="flex items-center gap-4">
                        <div className="flex items-center gap-1 text-sm text-slate-600">
                            <Calendar size={14} className="text-slate-400" />
                            <span>{service.bookingsCount} réservation(s)</span>
                        </div>
                        {service.rating && (
                            <div className="flex items-center gap-1 text-sm">
                                <Star size={14} className="text-amber-400 fill-amber-400" />
                                <span className="font-semibold text-slate-700">{service.rating}</span>
                                <span className="text-slate-400">({service.reviewsCount})</span>
                            </div>
                        )}
                    </div>
                    <Badge className="bg-slate-100 text-slate-600">{service.category}</Badge>
                </div>
            </CardContent>
        </Card>
    );
}

function CreateServiceCard() {
    return (
        <Card className="border-2 border-dashed border-slate-300 hover:border-teal-400 transition-colors cursor-pointer group">
            <CardContent className="p-8 flex flex-col items-center justify-center text-center min-h-[280px]">
                <div className="p-4 bg-teal-100 rounded-2xl mb-4 group-hover:bg-teal-200 transition-colors">
                    <Plus size={28} className="text-teal-600" />
                </div>
                <h3 className="font-bold text-slate-900 mb-2">Créer un nouveau service</h3>
                <p className="text-sm text-slate-500 mb-4">Atelier ou Coaching Vidéo</p>
                <div className="flex gap-2">
                    <Button variant="outline" size="sm" className="gap-1">
                        <Users size={14} /> Atelier
                    </Button>
                    <Button variant="outline" size="sm" className="gap-1">
                        <Video size={14} /> Coaching
                    </Button>
                </div>
            </CardContent>
        </Card>
    );
}

// =============================================================================
// PAGE
// =============================================================================

export default function TalentServicesPage() {
    const [filter, setFilter] = useState<'all' | 'workshop' | 'coaching'>('all');
    const [statusFilter, setStatusFilter] = useState<'all' | 'active' | 'draft' | 'paused'>('all');

    const filteredServices = mockServices.filter((service) => {
        if (filter === 'workshop' && service.type !== 'WORKSHOP') return false;
        if (filter === 'coaching' && service.type !== 'COACHING_VIDEO') return false;
        if (statusFilter === 'active' && service.status !== 'ACTIVE') return false;
        if (statusFilter === 'draft' && service.status !== 'DRAFT') return false;
        if (statusFilter === 'paused' && service.status !== 'PAUSED') return false;
        return true;
    });

    const stats = {
        total: mockServices.length,
        active: mockServices.filter(s => s.status === 'ACTIVE').length,
        totalBookings: mockServices.reduce((sum, s) => sum + s.bookingsCount, 0),
        avgRating: (mockServices.filter(s => s.rating).reduce((sum, s) => sum + (s.rating || 0), 0) / mockServices.filter(s => s.rating).length).toFixed(1),
    };

    return (
        <div className="space-y-6 max-w-6xl mx-auto">
            {/* Header */}
            <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
                <div>
                    <h1 className="text-2xl font-bold text-slate-900 flex items-center gap-2">
                        <Package className="text-teal-500" />
                        Mes Services
                    </h1>
                    <p className="text-slate-500 mt-1">Flux Froid - Votre catalogue Marketplace</p>
                </div>
                <Button className="bg-teal-600 hover:bg-teal-700 text-white gap-2">
                    <Plus size={18} />
                    Nouveau Service
                </Button>
            </div>

            {/* Stats Cards */}
            <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
                <Card className="border-slate-200">
                    <CardContent className="p-4 flex items-center gap-3">
                        <div className="p-2 bg-teal-100 rounded-lg">
                            <Package size={18} className="text-teal-600" />
                        </div>
                        <div>
                            <p className="text-2xl font-bold text-slate-900">{stats.total}</p>
                            <p className="text-xs text-slate-500">Services créés</p>
                        </div>
                    </CardContent>
                </Card>
                <Card className="border-slate-200">
                    <CardContent className="p-4 flex items-center gap-3">
                        <div className="p-2 bg-emerald-100 rounded-lg">
                            <Eye size={18} className="text-emerald-600" />
                        </div>
                        <div>
                            <p className="text-2xl font-bold text-slate-900">{stats.active}</p>
                            <p className="text-xs text-slate-500">Actifs</p>
                        </div>
                    </CardContent>
                </Card>
                <Card className="border-slate-200">
                    <CardContent className="p-4 flex items-center gap-3">
                        <div className="p-2 bg-indigo-100 rounded-lg">
                            <Calendar size={18} className="text-indigo-600" />
                        </div>
                        <div>
                            <p className="text-2xl font-bold text-slate-900">{stats.totalBookings}</p>
                            <p className="text-xs text-slate-500">Réservations totales</p>
                        </div>
                    </CardContent>
                </Card>
                <Card className="border-slate-200">
                    <CardContent className="p-4 flex items-center gap-3">
                        <div className="p-2 bg-amber-100 rounded-lg">
                            <Star size={18} className="text-amber-600" />
                        </div>
                        <div>
                            <p className="text-2xl font-bold text-slate-900">{stats.avgRating}</p>
                            <p className="text-xs text-slate-500">Note moyenne</p>
                        </div>
                    </CardContent>
                </Card>
            </div>

            {/* Filters */}
            <Card className="border-slate-200">
                <CardContent className="p-4">
                    <div className="flex flex-col sm:flex-row gap-4 justify-between">
                        <div className="flex gap-2">
                            {[
                                { key: 'all', label: 'Tous', icon: Package },
                                { key: 'workshop', label: 'Ateliers', icon: Users },
                                { key: 'coaching', label: 'Coaching', icon: Video },
                            ].map((f) => (
                                <button
                                    key={f.key}
                                    onClick={() => setFilter(f.key as typeof filter)}
                                    className={cn(
                                        'px-4 py-2 text-sm font-medium rounded-lg transition-colors flex items-center gap-2',
                                        filter === f.key
                                            ? 'bg-teal-100 text-teal-700'
                                            : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
                                    )}
                                >
                                    <f.icon size={14} />
                                    {f.label}
                                </button>
                            ))}
                        </div>
                        <div className="flex gap-2">
                            {[
                                { key: 'all', label: 'Tous statuts' },
                                { key: 'active', label: 'Actifs' },
                                { key: 'draft', label: 'Brouillons' },
                                { key: 'paused', label: 'Pausés' },
                            ].map((f) => (
                                <button
                                    key={f.key}
                                    onClick={() => setStatusFilter(f.key as typeof statusFilter)}
                                    className={cn(
                                        'px-3 py-1.5 text-xs font-medium rounded-md transition-colors',
                                        statusFilter === f.key
                                            ? 'bg-slate-800 text-white'
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

            {/* Services Grid */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
                <CreateServiceCard />
                {filteredServices.map((service) => (
                    <ServiceCard key={service.id} service={service} />
                ))}
            </div>

            {filteredServices.length === 0 && (
                <Card className="border-slate-200">
                    <CardContent className="p-12 text-center">
                        <BookOpen size={48} className="mx-auto text-slate-300 mb-4" />
                        <h3 className="text-lg font-semibold text-slate-700">Aucun service trouvé</h3>
                        <p className="text-slate-500 mt-1">Créez votre premier service pour commencer</p>
                    </CardContent>
                </Card>
            )}
        </div>
    );
}
