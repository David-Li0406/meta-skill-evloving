import Link from 'next/link';
import { notFound } from 'next/navigation';
import { getApiBaseWithVersion } from '@/lib/config';

type ServiceWithProfile = {
    id: string;
    name: string;
    description?: string | null;
    shortDescription?: string | null;
    basePrice?: number | null;
    tags?: string[] | null;
    category?: string | null;
    imageUrl?: string | null;
    galleryUrls?: string[] | null;
    profile?: {
        id: string;
        firstName?: string | null;
        lastName?: string | null;
        city?: string | null;
        avatarUrl?: string | null;
        averageRating?: number | null;
        totalReviews?: number | null;
        user?: {
            id: string;
            email?: string | null;
        } | null;
    } | null;
};

const API_BASE = getApiBaseWithVersion();

async function fetchService(id: string): Promise<ServiceWithProfile | null> {
    const res = await fetch(`${API_BASE}/wall/services/${id}`, {
        cache: 'no-store',
    });

    if (res.status === 404) {
        return null;
    }

    if (!res.ok) {
        throw new Error(`Failed to load service ${id}`);
    }

    return res.json();
}

const formatPrice = (value?: number | null) =>
    typeof value === 'number' && !Number.isNaN(value) ? `${value} € / h` : 'Tarif sur devis';

const getInitials = (value?: string | null) => {
    if (!value) return 'LX';
    const parts = value.split(' ').filter(Boolean);
    if (parts.length === 0) return 'LX';
    return parts.map((p) => p[0]?.toUpperCase()).join('').slice(0, 2);
};

export default async function OfferDetailPage({ params }: { params: { id: string } }) {
    const service = await fetchService(params.id);
    if (!service) {
        notFound();
    }

    const profile = service.profile;
    const fullName = profile
        ? `${profile.firstName || ''} ${profile.lastName || ''}`.trim() || 'Prestataire'
        : 'Prestataire';
    const city = profile?.city || 'Ville non renseignée';
    const avatarUrl = profile?.avatarUrl || null;
    const rating = profile?.averageRating ?? 4.8;
    const reviews = profile?.totalReviews ?? 12;
    const tags = Array.isArray(service.tags) ? service.tags.filter(Boolean) : [];
    const priceLabel = formatPrice(service.basePrice);
    const bookingHref = `/bookings/new?serviceId=${service.id}`;

    return (
        <div className="min-h-screen bg-slate-50">
            <div className="max-w-5xl mx-auto px-4 py-10 space-y-6">
                <header className="bg-white rounded-2xl shadow-soft p-6 flex flex-col gap-4 md:flex-row md:items-center md:gap-6">
                    <div className="flex-shrink-0 w-16 h-16 rounded-full bg-gradient-to-br from-brand-100 to-brand-50 flex items-center justify-center overflow-hidden ring-2 ring-white shadow">
                        {avatarUrl ? (
                            <img src={avatarUrl} alt={fullName} className="w-full h-full object-cover" />
                        ) : (
                            <span className="text-lg font-semibold text-orange-600">{getInitials(fullName)}</span>
                        )}
                    </div>
                    <div className="flex-1">
                        <p className="text-sm text-slate-500">{city}</p>
                        <h1 className="text-2xl font-semibold text-slate-900">{service.name}</h1>
                        <div className="flex items-center gap-2 text-sm text-slate-600 mt-1">
                            <span className="font-semibold text-amber-600">{rating.toFixed(1)}</span>
                            <span className="text-slate-400">({reviews} avis)</span>
                            {service.category && (
                                <span className="px-3 py-1 rounded-full bg-orange-50 text-orange-700 text-xs font-medium">
                                    {service.category}
                                </span>
                            )}
                        </div>
                    </div>
                    <div className="hidden md:flex items-center gap-3">
                        <span className="text-xl font-semibold text-slate-900">{priceLabel}</span>
                        <Link
                            href={bookingHref}
                            className="inline-flex items-center justify-center px-4 py-2 rounded-xl bg-brand-600 text-white font-semibold hover:bg-brand-700 transition-colors"
                        >
                            Réserver ce talent
                        </Link>
                    </div>
                </header>

                <div className="grid grid-cols-1 lg:grid-cols-[2fr_1fr] gap-6">
                    <main className="bg-white rounded-2xl shadow-soft p-6 space-y-6">
                        <section className="space-y-2">
                            <h2 className="text-lg font-semibold text-slate-900">Description</h2>
                            <p className="text-slate-700 leading-relaxed">
                                {service.description || service.shortDescription || 'Aucune description fournie.'}
                            </p>
                        </section>

                        <section className="space-y-3">
                            <h2 className="text-lg font-semibold text-slate-900">Tarifs</h2>
                            <div className="p-4 rounded-xl border border-slate-100 bg-slate-50">
                                <p className="text-base font-semibold text-slate-900">{priceLabel}</p>
                                <p className="text-sm text-slate-500">Tarif indicatif, ajustable selon le besoin.</p>
                            </div>
                        </section>

                        {tags.length > 0 && (
                            <section className="space-y-3">
                                <h2 className="text-lg font-semibold text-slate-900">Compétences</h2>
                                <div className="flex flex-wrap gap-2">
                                    {tags.map((tag) => (
                                        <span
                                            key={tag}
                                            className="px-3 py-1 rounded-full bg-slate-100 text-slate-700 text-sm"
                                        >
                                            {tag}
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
                                    <p className="text-sm text-slate-500">Tarif horaire</p>
                                    <p className="text-2xl font-semibold text-slate-900">{priceLabel}</p>
                                </div>
                                <Link
                                    href={bookingHref}
                                    className="inline-flex w-full items-center justify-center px-4 py-3 rounded-xl bg-brand-600 text-white font-semibold hover:bg-brand-700 transition-colors"
                                >
                                    Réserver ce talent
                                </Link>
                            </div>
                        </div>
                    </aside>
                </div>
            </div>

            <div className="md:hidden fixed bottom-0 inset-x-0 bg-white border-t border-slate-200 shadow-lg p-4">
                <div className="flex items-center justify-between">
                    <div>
                        <p className="text-sm text-slate-500">Tarif horaire</p>
                        <p className="text-lg font-semibold text-slate-900">{priceLabel}</p>
                    </div>
                    <Link
                        href={bookingHref}
                        className="inline-flex items-center justify-center px-4 py-2 rounded-xl bg-brand-600 text-white font-semibold hover:bg-brand-700 transition-colors"
                    >
                        Réserver
                    </Link>
                </div>
            </div>
        </div>
    );
}
