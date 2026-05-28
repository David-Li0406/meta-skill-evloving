'use client';

import Link from 'next/link';
import {
    User,
    Briefcase,
    MapPin,
    Star,
    ChevronRight,
    Eye
} from 'lucide-react';

// Mock user data
const mockUser = {
    name: 'Jean Dupont',
    role: 'Directeur - EHPAD Les Jardins',
    avatarUrl: null,
    stats: {
        missionsPosted: 12,
        talentsHired: 8,
        rating: 4.8,
    },
};

export function UserIdentityCard() {
    return (
        <div className="overflow-hidden rounded-xl border border-slate-200 bg-white shadow-sm">
            {/* Cover / Gradient Header */}
            <div className="h-16 bg-gradient-to-r from-teal-500 to-cyan-500" />

            {/* Avatar & Name */}
            <div className="-mt-8 px-4 pb-4">
                <div className="flex h-16 w-16 items-center justify-center rounded-full border-4 border-white bg-slate-100 text-xl font-bold text-slate-600">
                    {mockUser.avatarUrl ? (
                        <img
                            src={mockUser.avatarUrl}
                            alt={mockUser.name}
                            className="h-full w-full rounded-full object-cover"
                        />
                    ) : (
                        mockUser.name.charAt(0)
                    )}
                </div>
                <h3 className="mt-2 font-semibold text-slate-900">{mockUser.name}</h3>
                <p className="text-sm text-slate-500">{mockUser.role}</p>
            </div>

            {/* Stats */}
            <div className="grid grid-cols-3 divide-x divide-slate-100 border-t border-slate-100">
                <StatItem label="Missions" value={mockUser.stats.missionsPosted} />
                <StatItem label="Recrutés" value={mockUser.stats.talentsHired} />
                <StatItem label="Note" value={mockUser.stats.rating} icon={<Star className="h-3 w-3 fill-amber-400 text-amber-400" />} />
            </div>

            {/* Quick Links */}
            <div className="border-t border-slate-100 p-3">
                <Link
                    href="/dashboard"
                    className="flex items-center justify-between rounded-lg px-3 py-2 text-sm text-slate-600 transition-colors hover:bg-slate-50"
                >
                    <span className="flex items-center gap-2">
                        <Eye className="h-4 w-4" />
                        Mon tableau de bord
                    </span>
                    <ChevronRight className="h-4 w-4 text-slate-400" />
                </Link>
                <Link
                    href="/dashboard/client"
                    className="flex items-center justify-between rounded-lg px-3 py-2 text-sm text-slate-600 transition-colors hover:bg-slate-50"
                >
                    <span className="flex items-center gap-2">
                        <Briefcase className="h-4 w-4" />
                        Mon Dashboard
                    </span>
                    <ChevronRight className="h-4 w-4 text-slate-400" />
                </Link>
            </div>
        </div>
    );
}

interface StatItemProps {
    label: string;
    value: number;
    icon?: React.ReactNode;
}

function StatItem({ label, value, icon }: StatItemProps) {
    return (
        <div className="px-3 py-3 text-center">
            <p className="flex items-center justify-center gap-1 text-lg font-bold text-slate-900">
                {value}
                {icon}
            </p>
            <p className="text-xs text-slate-500">{label}</p>
        </div>
    );
}
