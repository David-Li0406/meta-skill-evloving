import Link from 'next/link';
import { notFound } from 'next/navigation';
import { getApiBaseWithVersion } from '@/lib/config';

type MissionDetail = {
    id: string;
    title: string;
    description?: string | null;
    jobTitle?: string | null;
    urgencyLevel?: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
    startDate?: string | Date | null;
    endDate?: string | Date | null;
    hourlyRate?: number | null;
    isNightShift?: boolean | null;
    city?: string | null;
    client?: {
        establishment?: {
            name?: string | null;
            logoUrl?: string | null;
            city?: string | null;
        } | null;
    } | null;
    requiredSkills?: string[] | null;
};

const API_BASE = getApiBaseWithVersion();

async function fetchMission(id: string): Promise<MissionDetail | null> {
    const res = await fetch(`${API_BASE}/matching/missions/${id}`, { cache: 'no-store' });

    if (res.status === 404) {
        return null;
    }

    if (!res.ok) {
        throw new Error(`Failed to load mission ${id}`);
    }

    return res.json();
}

const formatDate = (value?: string | Date | null) => {
    if (!value) return 'Date à définir';
    const date = typeof value === 'string' ? new Date(value) : value;
    if (Number.isNaN(date.getTime())) return 'Date à définir';
    return date.toLocaleDateString('fr-FR', { day: 'numeric', month: 'short', year: 'numeric' });
};

const formatPrice = (value?: number | null) =>
    typeof value === 'number' && !Number.isNaN(value) ? `${value} € / h` : 'Selon profil';

const urgencyColor: Record<string, string> = {
    LOW: 'bg-slate-100 text-slate-600',
    MEDIUM: 'bg-amber-100 text-amber-700',
    HIGH: 'bg-orange-100 text-orange-700',
    CRITICAL: 'bg-red-100 text-red-700',
};

export default async function NeedDetailPage({ params }: { params: { id: string } }) {
    const mission = await fetchMission(params.id);
    if (!mission) {
        notFound();
    }

    const establishment = mission.client?.establishment?.name || 'Établissement';
    const logoUrl = mission.client?.establishment?.logoUrl || null;
    const location = mission.client?.establishment?.city || mission.city || 'Lieu non renseigné';
    const urgency = mission.urgencyLevel || 'MEDIUM';
    const badgeClass = urgencyColor[urgency] || urgencyColor.MEDIUM;
    const startLabel = formatDate(mission.startDate);
    const endLabel = formatDate(mission.endDate);
    const applyHref = `/dashboard/missions/${mission.id}/apply`;
    const requiredSkills = Array.isArray(mission.requiredSkills) ? mission.requiredSkills.filter(Boolean) : [];

    return (
        <div className="min-h-screen bg-slate-50">
            <div className="max-w-5xl mx-auto px-4 py-10 space-y-6">
                <header className="bg-white rounded-2xl shadow-soft p-6 flex flex-col gap-4 md:flex-row md:items-center md:gap-6">
                    <div className="flex-shrink-0 w-16 h-16 rounded-xl bg-gradient-to-br from-blue-50 to-blue-100 flex items-center justify-center overflow-hidden ring-2 ring-white shadow">
                        {logoUrl ? (
                            <img src={logoUrl} alt={establishment} className="w-full h-full object-cover" />
                        ) : (
                            <span className="text-lg font-semibold text-blue-600">
                                {establishment.slice(0, 2).toUpperCase()}
                            </span>
                        )}
                    </div>
                    <div className="flex-1">
                        <p className="text-sm text-slate-500">{location}</p>
                        <h1 className="text-2xl font-semibold text-slate-900">{mission.title || mission.jobTitle}</h1>
                        <div className="flex items-center gap-2 mt-2">
                            <span className={`px-3 py-1 rounded-full text-xs font-semibold ${badgeClass}`}>
                                Urgence: {urgency}
                            </span>
                            {mission.isNightShift && (
                                <span className="px-3 py-1 rounded-full text-xs font-semibold bg-slate-100 text-slate-700">
                                    Poste de nuit
                                </span>
                            )}
                        </div>
                    </div>
                    <div className="hidden md:flex items-center gap-3">
                        <span className="text-xl font-semibold text-slate-900">{formatPrice(mission.hourlyRate)}</span>
                        <Link
                            href={applyHref}
                            className="inline-flex items-center justify-center px-4 py-2 rounded-xl bg-rose-500 text-white font-semibold hover:bg-rose-600 shadow-sm hover:shadow-md active:scale-95 transition-all"
                        >
                            Postuler
                        </Link>
                    </div>
                </header>

                <div className="grid grid-cols-1 lg:grid-cols-[2fr_1fr] gap-6">
                    <main className="bg-white rounded-2xl shadow-soft p-6 space-y-6">
                        <section className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                            <div className="p-4 rounded-xl bg-slate-50 border border-slate-100">
                                <p className="text-sm text-slate-500">Début</p>
                                <p className="text-base font-semibold text-slate-900">{startLabel}</p>
                            </div>
                            <div className="p-4 rounded-xl bg-slate-50 border border-slate-100">
                                <p className="text-sm text-slate-500">Fin</p>
                                <p className="text-base font-semibold text-slate-900">{endLabel}</p>
                            </div>
                            <div className="p-4 rounded-xl bg-slate-50 border border-slate-100">
                                <p className="text-sm text-slate-500">Lieu</p>
                                <p className="text-base font-semibold text-slate-900">{location}</p>
                            </div>
                            <div className="p-4 rounded-xl bg-slate-50 border border-slate-100">
                                <p className="text-sm text-slate-500">Rémunération estimée</p>
                                <p className="text-base font-semibold text-slate-900">{formatPrice(mission.hourlyRate)}</p>
                            </div>
                        </section>

                        <section className="space-y-2">
                            <h2 className="text-lg font-semibold text-slate-900">Description</h2>
                            <p className="text-slate-700 leading-relaxed">
                                {mission.description || 'Aucune description fournie.'}
                            </p>
                        </section>

                        {requiredSkills.length > 0 && (
                            <section className="space-y-3">
                                <h2 className="text-lg font-semibold text-slate-900">Compétences requises</h2>
                                <div className="flex flex-wrap gap-2">
                                    {requiredSkills.map((skill) => (
                                        <span
                                            key={skill}
                                            className="px-3 py-1 rounded-full bg-rose-50 text-rose-700 text-sm"
                                        >
                                            {skill}
                                        </span>
                                    ))}
                                </div>
                            </section>
                        )}
                    </main>

                    <aside className="hidden lg:block">
                        <div className="sticky top-6 space-y-4">
                            <div className="bg-white rounded-2xl shadow-soft p-5 space-y-4">
                                <div>
                                    <p className="text-sm text-slate-500">Rémunération estimée</p>
                                    <p className="text-2xl font-semibold text-slate-900">{formatPrice(mission.hourlyRate)}</p>
                                </div>
                                <Link
                                    href={applyHref}
                                    className="inline-flex w-full items-center justify-center px-4 py-3 rounded-xl bg-rose-500 text-white font-semibold hover:bg-rose-600 shadow-sm hover:shadow-md active:scale-95 transition-all"
                                >
                                    Postuler
                                </Link>
                            </div>
                        </div>
                    </aside>
                </div>
            </div>

            <div className="md:hidden fixed bottom-0 inset-x-0 bg-white border-t border-slate-200 shadow-lg p-4">
                <div className="flex items-center justify-between">
                    <div>
                        <p className="text-sm text-slate-500">Rémunération estimée</p>
                        <p className="text-lg font-semibold text-slate-900">{formatPrice(mission.hourlyRate)}</p>
                    </div>
                    <Link
                        href={applyHref}
                        className="inline-flex items-center justify-center px-4 py-2 rounded-xl bg-rose-500 text-white font-semibold hover:bg-rose-600 shadow-sm hover:shadow-md active:scale-95 transition-all"
                    >
                        Postuler
                    </Link>
                </div>
            </div>
        </div>
    );
}
