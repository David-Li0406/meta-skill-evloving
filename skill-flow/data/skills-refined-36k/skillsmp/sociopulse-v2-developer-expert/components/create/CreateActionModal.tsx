'use client';

import type { ReactElement } from 'react';
import { useMemo, useState } from 'react';
import * as Dialog from '@radix-ui/react-dialog';
import { useRouter } from 'next/navigation';
import { ArrowLeft, Loader2, Plus, Siren, Sparkles, X } from 'lucide-react';
import { ToastContainer, useToasts } from '@/components/ui/Toast';
import { createSocialPost } from '@/app/(platform)/services/wall.service';

type UserRole = 'CLIENT' | 'TALENT' | 'ADMIN';

export interface CreateActionModalUser {
    id: string;
    email: string;
    role: UserRole;
    profile?: {
        firstName?: string;
        lastName?: string;
        avatarUrl?: string;
        city?: string;
        postalCode?: string;
    };
    establishment?: {
        name?: string;
        city?: string;
    };
}

type ModalStep = 'CHOICE' | 'POST_FORM';

const POST_ETHICS_LABEL =
    "Je certifie ne pas divulguer d'informations confidentielles ni de visages de bénéficiaires sans autorisation.";

function buildAuthorDisplayName(user: CreateActionModalUser): string {
    const first = user.profile?.firstName?.trim();
    const last = user.profile?.lastName?.trim();
    const full = [first, last].filter(Boolean).join(' ').trim();
    return user.establishment?.name?.trim() || full || user.email;
}

function normalizeMediaUrls(urls: string[]): string[] {
    return urls
        .map((url) => url.trim())
        .filter((url) => url.length > 0);
}

export function CreateActionModal({
    user,
    trigger,
}: {
    user: CreateActionModalUser;
    trigger?: ReactElement;
}) {
    const router = useRouter();
    const { toasts, addToast, removeToast } = useToasts();

    const [open, setOpen] = useState(false);
    const [step, setStep] = useState<ModalStep>('CHOICE');
    const [content, setContent] = useState('');
    const [mediaUrls, setMediaUrls] = useState<string[]>(['']);
    const [ethicsConfirmed, setEthicsConfirmed] = useState(false);
    const [isSubmitting, setIsSubmitting] = useState(false);

    const isTALENT = user.role === 'TALENT';
    const isClient = user.role === 'CLIENT';

    const postCategory = useMemo(() => {
        if (isTALENT) return 'EXPERIENCE' as const;
        return 'NEWS' as const;
    }, [isTALENT]);

    const postLabel = isTALENT ? 'Partager une expérience' : 'Partager une actu';
    const postSubtitle = isTALENT
        ? 'Valorisez votre savoir-faire (retour terrain, tips, apprentissages).'
        : 'Partagez une info utile (actualité, besoin, insight).';

    const resetForm = () => {
        setStep('CHOICE');
        setContent('');
        setMediaUrls(['']);
        setEthicsConfirmed(false);
        setIsSubmitting(false);
    };

    const closeModal = () => {
        setOpen(false);
        resetForm();
    };

    const onSubmitPost = async () => {
        const normalizedContent = content.trim();
        if (!normalizedContent) {
            addToast({ type: 'warning', message: 'Ajoutez un message avant de publier.' });
            return;
        }
        if (!ethicsConfirmed) {
            addToast({ type: 'warning', message: 'La validation éthique est obligatoire.' });
            return;
        }

        const normalizedUrls = normalizeMediaUrls(mediaUrls);
        const optimisticId = `optimistic-${Date.now()}`;
        const nowIso = new Date().toISOString();

        const optimisticItem = {
            id: optimisticId,
            type: 'POST' as const,
            postType: 'SOCIAL' as const,
            title: `${postCategory === 'EXPERIENCE' ? 'Expérience' : 'Actu'}: ${normalizedContent.slice(0, 60)}${normalizedContent.length > 60 ? '…' : ''}`,
            content: normalizedContent,
            category: postCategory,
            mediaUrls: normalizedUrls,
            createdAt: nowIso,
            authorId: user.id,
            authorName: buildAuthorDisplayName(user),
            authorAvatar: user.profile?.avatarUrl || null,
            authorRole: user.role,
            city: user.profile?.city || user.establishment?.city || null,
            postalCode: user.profile?.postalCode || null,
            tags: [],
            isOptimistic: true,
        };

        window.dispatchEvent(
            new CustomEvent('sociopulse:wall:feed-item', {
                detail: { status: 'optimistic', optimisticId, item: optimisticItem },
            }),
        );

        setIsSubmitting(true);
        try {
            const created = await createSocialPost({
                content: normalizedContent,
                category: postCategory,
                mediaUrls: normalizedUrls,
                ethicsConfirmed: true,
                city: user.profile?.city || undefined,
                postalCode: user.profile?.postalCode || undefined,
            });

            window.dispatchEvent(
                new CustomEvent('sociopulse:wall:feed-item', {
                    detail: { status: 'confirmed', optimisticId, item: created },
                }),
            );

            addToast({ type: 'success', message: 'Post publié.' });
            closeModal();
        } catch (error) {
            window.dispatchEvent(
                new CustomEvent('sociopulse:wall:feed-item', {
                    detail: { status: 'failed', optimisticId },
                }),
            );
            addToast({ type: 'error', message: "Impossible de publier pour l'instant." });
        } finally {
            setIsSubmitting(false);
        }
    };

    if (!isTALENT && !isClient) return null;

    return (
        <>
            <Dialog.Root
                open={open}
                onOpenChange={(nextOpen) => {
                    setOpen(nextOpen);
                    if (!nextOpen) resetForm();
                }}
            >
                <Dialog.Trigger asChild>
                    {trigger ? (
                        trigger
                    ) : (
                        <button
                            type="button"
                            className="inline-flex items-center gap-2 px-4 py-2 rounded-2xl bg-gradient-to-r from-indigo-600 to-teal-500 text-white font-semibold shadow-soft hover:shadow-soft-lg transition-shadow"
                        >
                            <Plus className="h-4 w-4" />
                            Publier
                        </button>
                    )}
                </Dialog.Trigger>

                <Dialog.Portal>
                    <Dialog.Overlay className="fixed inset-0 z-50 bg-black/40 backdrop-blur-sm" />
                    <Dialog.Content className="fixed left-1/2 top-1/2 z-50 w-[min(92vw,560px)] -translate-x-1/2 -translate-y-1/2 rounded-3xl bg-white shadow-2xl border border-white/60 p-6 animate-modal-in">
                        <div className="flex items-start justify-between gap-4">
                            <div>
                                <Dialog.Title className="text-lg font-semibold text-slate-900">
                                    ➕ Publier
                                </Dialog.Title>
                                <Dialog.Description className="mt-1 text-sm text-slate-600">
                                    {step === 'CHOICE'
                                        ? 'Choisissez une action.'
                                        : postSubtitle}
                                </Dialog.Description>
                            </div>
                            <Dialog.Close asChild>
                                <button
                                    type="button"
                                    className="p-2 rounded-xl hover:bg-slate-100 transition-colors"
                                    aria-label="Fermer"
                                >
                                    <X className="h-5 w-5 text-slate-500" />
                                </button>
                            </Dialog.Close>
                        </div>

                        {step === 'CHOICE' ? (
                            <div className="mt-6 grid grid-cols-1 sm:grid-cols-2 gap-4">
                                <button
                                    type="button"
                                    onClick={() => {
                                        closeModal();
                                        router.push(isClient ? '/dashboard/relief' : '/offer/new');
                                    }}
                                    className="group text-left rounded-2xl border border-slate-200 bg-white hover:bg-slate-50 transition-colors p-5"
                                >
                                    <div className="flex items-center gap-3">
                                        <span className="h-10 w-10 rounded-2xl bg-slate-900/5 flex items-center justify-center">
                                            <Siren className="h-5 w-5 text-slate-800" />
                                        </span>
                                        <div>
                                            <p className="text-sm font-semibold text-slate-900">
                                                {isClient ? 'Demander du Renfort' : 'Créer une Offre'}
                                            </p>
                                            <p className="text-xs text-slate-500">
                                                {isClient
                                                    ? 'Mission SOS en 30 secondes.'
                                                    : 'Publiez un service (atelier / visio).'}
                                            </p>
                                        </div>
                                    </div>
                                </button>

                                <button
                                    type="button"
                                    onClick={() => setStep('POST_FORM')}
                                    className="group text-left rounded-2xl border border-slate-200 bg-white hover:bg-slate-50 transition-colors p-5"
                                >
                                    <div className="flex items-center gap-3">
                                        <span className="h-10 w-10 rounded-2xl bg-brand-500/10 flex items-center justify-center">
                                            <Sparkles className="h-5 w-5 text-brand-600" />
                                        </span>
                                        <div>
                                            <p className="text-sm font-semibold text-slate-900">{postLabel}</p>
                                            <p className="text-xs text-slate-500">{postSubtitle}</p>
                                        </div>
                                    </div>
                                </button>
                            </div>
                        ) : (
                            <div className="mt-6 space-y-4">
                                <button
                                    type="button"
                                    onClick={() => setStep('CHOICE')}
                                    className="inline-flex items-center gap-2 text-sm font-medium text-slate-600 hover:text-slate-900 transition-colors"
                                >
                                    <ArrowLeft className="h-4 w-4" />
                                    Retour
                                </button>

                                <div className="space-y-2">
                                    <label className="label-sm">Message</label>
                                    <textarea
                                        value={content}
                                        onChange={(e) => setContent(e.target.value)}
                                        rows={5}
                                        className="input-premium resize-none"
                                        placeholder="Écrivez quelque chose d’utile pour la communauté…"
                                    />
                                </div>

                                <div className="space-y-2">
                                    <label className="label-sm">Images (URLs)</label>
                                    <div className="space-y-2">
                                        {mediaUrls.map((url, index) => (
                                            <div key={index} className="flex items-center gap-2">
                                                <input
                                                    value={url}
                                                    onChange={(e) => {
                                                        const next = [...mediaUrls];
                                                        next[index] = e.target.value;
                                                        setMediaUrls(next);
                                                    }}
                                                    className="input-premium"
                                                    placeholder="https://..."
                                                />
                                                {mediaUrls.length > 1 && (
                                                    <button
                                                        type="button"
                                                        onClick={() => {
                                                            setMediaUrls((prev) => prev.filter((_, i) => i !== index));
                                                        }}
                                                        className="btn-secondary !px-3"
                                                        aria-label="Supprimer l’URL"
                                                    >
                                                        <X className="h-4 w-4" />
                                                    </button>
                                                )}
                                            </div>
                                        ))}
                                    </div>
                                    <button
                                        type="button"
                                        onClick={() => setMediaUrls((prev) => [...prev, ''])}
                                        className="btn-secondary"
                                    >
                                        Ajouter une image
                                    </button>
                                </div>

                                <label className="flex items-start gap-3 rounded-2xl border border-slate-200 bg-slate-50 p-4">
                                    <input
                                        type="checkbox"
                                        checked={ethicsConfirmed}
                                        onChange={(e) => setEthicsConfirmed(e.target.checked)}
                                        className="mt-1 h-4 w-4 rounded border-slate-300 text-brand-600 focus:ring-brand-200"
                                    />
                                    <span className="text-sm text-slate-700">{POST_ETHICS_LABEL}</span>
                                </label>

                                <div className="flex items-center justify-end gap-3 pt-2">
                                    <button type="button" className="btn-secondary" onClick={closeModal} disabled={isSubmitting}>
                                        Annuler
                                    </button>
                                    <button
                                        type="button"
                                        className="btn-primary"
                                        onClick={onSubmitPost}
                                        disabled={isSubmitting}
                                    >
                                        {isSubmitting ? (
                                            <>
                                                <Loader2 className="h-4 w-4 animate-spin" />
                                                Publication…
                                            </>
                                        ) : (
                                            'Publier'
                                        )}
                                    </button>
                                </div>
                            </div>
                        )}
                    </Dialog.Content>
                </Dialog.Portal>
            </Dialog.Root>

            <ToastContainer toasts={toasts} onRemove={removeToast} />
        </>
    );
}


