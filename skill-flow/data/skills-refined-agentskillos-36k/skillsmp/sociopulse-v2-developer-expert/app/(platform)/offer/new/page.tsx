'use client';

import { useEffect, useMemo, useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { Loader2, Plus } from 'lucide-react';
import { useAuth } from '@/lib/useAuth';
import { createService, type ServiceType } from '@/app/(platform)/services/wall.service';
import { ToastContainer, useToasts } from '@/components/ui/Toast';

type CreatedService = { id: string };

const isCreatedService = (value: unknown): value is CreatedService => {
    if (!value || typeof value !== 'object') return false;
    const record = value as Record<string, unknown>;
    return typeof record.id === 'string' && record.id.length > 0;
};

const normalizeCsv = (value: string): string[] =>
    value
        .split(',')
        .map((part) => part.trim())
        .filter(Boolean);

export default function NewOfferPage() {
    const router = useRouter();
    const { user, isLoading } = useAuth();
    const { toasts, addToast, removeToast } = useToasts();

    const [name, setName] = useState('');
    const [type, setType] = useState<ServiceType>('WORKSHOP');
    const [category, setCategory] = useState('');
    const [shortDescription, setShortDescription] = useState('');
    const [description, setDescription] = useState('');
    const [basePrice, setBasePrice] = useState<string>('');
    const [imageUrl, setImageUrl] = useState('');
    const [tagsCsv, setTagsCsv] = useState('');
    const [galleryCsv, setGalleryCsv] = useState('');
    const [isSubmitting, setIsSubmitting] = useState(false);

    const canAccess = useMemo(() => user?.role === 'TALENT', [user?.role]);

    useEffect(() => {
        if (!isLoading && user && user.role !== 'TALENT') {
            addToast({ type: 'warning', message: 'Création d’offre réservée aux TALENTs.' });
        }
    }, [addToast, isLoading, user]);

    const handleSubmit = async () => {
        const normalizedName = name.trim();
        if (!normalizedName) {
            addToast({ type: 'warning', message: 'Le nom du service est requis.' });
            return;
        }

        const price =
            basePrice.trim().length > 0
                ? Number(basePrice.replace(',', '.'))
                : undefined;

        if (price !== undefined && Number.isNaN(price)) {
            addToast({ type: 'warning', message: 'Prix invalide.' });
            return;
        }

        setIsSubmitting(true);
        try {
            const created = await createService({
                name: normalizedName,
                type,
                category: category.trim() || undefined,
                shortDescription: shortDescription.trim() || undefined,
                description: description.trim() || undefined,
                basePrice: price,
                imageUrl: imageUrl.trim() || undefined,
                tags: normalizeCsv(tagsCsv),
                galleryUrls: normalizeCsv(galleryCsv),
            });

            if (!isCreatedService(created)) {
                throw new Error('Invalid createService response');
            }

            addToast({ type: 'success', message: 'Offre publiée.' });
            router.push(`/offer/${created.id}`);
        } catch (error) {
            addToast({ type: 'error', message: "Impossible de créer l’offre." });
        } finally {
            setIsSubmitting(false);
        }
    };

    if (isLoading) {
        return (
            <div className="max-w-3xl mx-auto px-4 py-10">
                <div className="card-surface p-6 flex items-center gap-3">
                    <Loader2 className="h-5 w-5 animate-spin text-slate-500" />
                    <p className="text-sm text-slate-600">Chargement…</p>
                </div>
            </div>
        );
    }

    if (!user) {
        return (
            <div className="max-w-3xl mx-auto px-4 py-10 space-y-4">
                <div className="card-surface p-6">
                    <h1 className="text-xl font-semibold text-slate-900">Créer une offre</h1>
                    <p className="mt-2 text-sm text-slate-600">Connectez-vous pour publier un service.</p>
                    <div className="mt-5 flex gap-3">
                        <Link href="/auth/login" className="btn-primary">Se connecter</Link>
                        <Link href="/fil-pro" className="btn-secondary">Retour au Fil Pro</Link>
                    </div>
                </div>
                <ToastContainer toasts={toasts} onRemove={removeToast} />
            </div>
        );
    }

    if (!canAccess) {
        return (
            <div className="max-w-3xl mx-auto px-4 py-10 space-y-4">
                <div className="card-surface p-6">
                    <h1 className="text-xl font-semibold text-slate-900">Créer une offre</h1>
                    <p className="mt-2 text-sm text-slate-600">Cette action est réservée aux profils TALENT.</p>
                    <div className="mt-5">
                        <Link href="/fil-pro" className="btn-secondary">Retour au Fil Pro</Link>
                    </div>
                </div>
                <ToastContainer toasts={toasts} onRemove={removeToast} />
            </div>
        );
    }

    return (
        <div className="max-w-3xl mx-auto px-4 py-10 space-y-6">
            <header className="space-y-1">
                <h1 className="text-2xl font-semibold text-slate-900">Créer une offre</h1>
                <p className="text-sm text-slate-600">Publiez un service (atelier ou visio) visible dans le Wall.</p>
            </header>

            <div className="card-surface p-6 space-y-5">
                <div className="space-y-2">
                    <label className="label-sm">Nom du service</label>
                    <input value={name} onChange={(e) => setName(e.target.value)} className="input-premium" placeholder="Ex: Atelier sensoriel" />
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                    <div className="space-y-2">
                        <label className="label-sm">Type</label>
                        <select
                            value={type}
                            onChange={(e) => setType(e.target.value as ServiceType)}
                            className="input-premium"
                        >
                            <option value="WORKSHOP">Atelier (présentiel)</option>
                            <option value="COACHING_VIDEO">Visio 1:1</option>
                        </select>
                    </div>
                    <div className="space-y-2">
                        <label className="label-sm">Catégorie</label>
                        <input value={category} onChange={(e) => setCategory(e.target.value)} className="input-premium" placeholder="Ex: Bien-être" />
                    </div>
                </div>

                <div className="space-y-2">
                    <label className="label-sm">Description courte</label>
                    <input value={shortDescription} onChange={(e) => setShortDescription(e.target.value)} className="input-premium" placeholder="1 phrase pour la carte" />
                </div>

                <div className="space-y-2">
                    <label className="label-sm">Description</label>
                    <textarea value={description} onChange={(e) => setDescription(e.target.value)} rows={5} className="input-premium resize-none" placeholder="Détails, déroulé, bénéfices…" />
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                    <div className="space-y-2">
                        <label className="label-sm">Prix de base (€)</label>
                        <input value={basePrice} onChange={(e) => setBasePrice(e.target.value)} className="input-premium" placeholder="Ex: 65" inputMode="decimal" />
                    </div>
                    <div className="space-y-2">
                        <label className="label-sm">Image principale (URL)</label>
                        <input value={imageUrl} onChange={(e) => setImageUrl(e.target.value)} className="input-premium" placeholder="https://..." />
                    </div>
                </div>

                <div className="space-y-2">
                    <label className="label-sm">Tags (séparés par des virgules)</label>
                    <input value={tagsCsv} onChange={(e) => setTagsCsv(e.target.value)} className="input-premium" placeholder="autisme, stimulation, motricité" />
                </div>

                <div className="space-y-2">
                    <label className="label-sm">Galerie (URLs, séparées par des virgules)</label>
                    <input value={galleryCsv} onChange={(e) => setGalleryCsv(e.target.value)} className="input-premium" placeholder="https://..., https://..." />
                </div>

                <div className="flex items-center justify-end gap-3 pt-2">
                    <Link href="/fil-pro" className="btn-secondary">Annuler</Link>
                    <button type="button" onClick={handleSubmit} className="btn-primary" disabled={isSubmitting}>
                        {isSubmitting ? (
                            <>
                                <Loader2 className="h-4 w-4 animate-spin" />
                                Publication…
                            </>
                        ) : (
                            <>
                                <Plus className="h-4 w-4" />
                                Publier l’offre
                            </>
                        )}
                    </button>
                </div>
            </div>

            <ToastContainer toasts={toasts} onRemove={removeToast} />
        </div>
    );
}


