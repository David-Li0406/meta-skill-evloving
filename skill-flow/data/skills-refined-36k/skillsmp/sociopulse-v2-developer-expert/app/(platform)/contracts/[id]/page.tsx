'use client';

import { useState, useEffect, useRef } from 'react';
import { useParams, useRouter } from 'next/navigation';
import Link from 'next/link';
import { motion } from 'framer-motion';
import Cookies from 'js-cookie';
import {
    ChevronLeft,
    FileCheck,
    Clock,
    CheckCircle,
    AlertTriangle,
    User,
    Building2,
    Calendar,
    Euro,
    Loader2,
    Download,
    PenTool,
    Shield,
    FileText,
    MapPin,
    Check,
    X,
} from 'lucide-react';

// ===========================================
// TYPES
// ===========================================

interface ContractDetail {
    id: string;
    reference?: string;
    type: 'MISSION_SOS' | 'SERVICE_BOOKING' | 'FRAMEWORK';
    status: string;
    title?: string;
    content: string;
    totalAmount?: number;
    platformFee?: number;
    startDate?: string;
    endDate?: string;
    deadlines?: { label: string; date: string; completed: boolean }[];
    signatureUrl?: string;
    TALENTSignedAt?: string;
    TALENTSignedIp?: string;
    clientSignature?: string;
    clientSignedAt?: string;
    clientSignedIp?: string;
    pdfUrl?: string;
    createdAt: string;
    TALENT: {
        id: string;
        email: string;
        profile?: { firstName: string; lastName: string; avatarUrl?: string };
    };
    client?: {
        id: string;
        email: string;
        establishment?: { name: string; address?: string; city?: string };
        profile?: { firstName: string; lastName: string };
    };
    mission?: {
        id: string;
        title: string;
        description: string;
        city: string;
        address: string;
        hourlyRate: number;
        startDate: string;
        endDate: string;
    };
    quote?: {
        id: string;
        reference: string;
    };
}

// ===========================================
// HELPERS
// ===========================================

const getApiBase = () => {
    const apiBase = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:4000';
    const normalized = apiBase.replace(/\/+$/, '');
    return normalized.endsWith('/api/v1') ? normalized : `${normalized}/api/v1`;
};

const getToken = () => Cookies.get('accessToken');

const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('fr-FR', {
        day: 'numeric',
        month: 'long',
        year: 'numeric',
    });
};

const formatDateTime = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('fr-FR', {
        day: 'numeric',
        month: 'short',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
    });
};

const formatCurrency = (cents: number) => {
    return new Intl.NumberFormat('fr-FR', {
        style: 'currency',
        currency: 'EUR',
    }).format(cents / 100);
};

// ===========================================
// SIGNATURE PAD COMPONENT
// ===========================================

function SignaturePad({
    onSign,
    isLoading,
}: {
    onSign: (signatureDataUrl: string) => void;
    isLoading: boolean;
}) {
    const canvasRef = useRef<HTMLCanvasElement>(null);
    const [isDrawing, setIsDrawing] = useState(false);
    const [hasSignature, setHasSignature] = useState(false);

    useEffect(() => {
        const canvas = canvasRef.current;
        if (!canvas) return;

        const ctx = canvas.getContext('2d');
        if (!ctx) return;

        ctx.fillStyle = '#f8fafc';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.strokeStyle = '#1e293b';
        ctx.lineWidth = 2;
        ctx.lineCap = 'round';
        ctx.lineJoin = 'round';
    }, []);

    const getCoordinates = (e: React.MouseEvent | React.TouchEvent) => {
        const canvas = canvasRef.current;
        if (!canvas) return { x: 0, y: 0 };

        const rect = canvas.getBoundingClientRect();
        const scaleX = canvas.width / rect.width;
        const scaleY = canvas.height / rect.height;

        if ('touches' in e) {
            return {
                x: (e.touches[0].clientX - rect.left) * scaleX,
                y: (e.touches[0].clientY - rect.top) * scaleY,
            };
        }
        return {
            x: (e.clientX - rect.left) * scaleX,
            y: (e.clientY - rect.top) * scaleY,
        };
    };

    const startDrawing = (e: React.MouseEvent | React.TouchEvent) => {
        const canvas = canvasRef.current;
        const ctx = canvas?.getContext('2d');
        if (!ctx) return;

        setIsDrawing(true);
        const { x, y } = getCoordinates(e);
        ctx.beginPath();
        ctx.moveTo(x, y);
    };

    const draw = (e: React.MouseEvent | React.TouchEvent) => {
        if (!isDrawing) return;
        const canvas = canvasRef.current;
        const ctx = canvas?.getContext('2d');
        if (!ctx) return;

        const { x, y } = getCoordinates(e);
        ctx.lineTo(x, y);
        ctx.stroke();
        setHasSignature(true);
    };

    const stopDrawing = () => {
        setIsDrawing(false);
    };

    const clear = () => {
        const canvas = canvasRef.current;
        const ctx = canvas?.getContext('2d');
        if (!ctx || !canvas) return;

        ctx.fillStyle = '#f8fafc';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        setHasSignature(false);
    };

    const handleSign = () => {
        const canvas = canvasRef.current;
        if (!canvas || !hasSignature) return;
        onSign(canvas.toDataURL('image/png'));
    };

    return (
        <div className="space-y-4">
            <div className="relative">
                <canvas
                    ref={canvasRef}
                    width={500}
                    height={200}
                    className="w-full border-2 border-dashed border-slate-300 rounded-xl cursor-crosshair touch-none"
                    onMouseDown={startDrawing}
                    onMouseMove={draw}
                    onMouseUp={stopDrawing}
                    onMouseLeave={stopDrawing}
                    onTouchStart={startDrawing}
                    onTouchMove={draw}
                    onTouchEnd={stopDrawing}
                />
                <p className="absolute bottom-2 left-1/2 -translate-x-1/2 text-xs text-slate-400">
                    Signez ici avec votre souris ou votre doigt
                </p>
            </div>

            <div className="flex gap-3">
                <button
                    onClick={clear}
                    className="flex-1 flex items-center justify-center gap-2 px-4 py-3 rounded-xl border border-slate-200 text-slate-600 font-medium hover:bg-slate-50 transition-colors"
                >
                    <X className="w-4 h-4" />
                    Effacer
                </button>
                <button
                    onClick={handleSign}
                    disabled={!hasSignature || isLoading}
                    className="flex-1 flex items-center justify-center gap-2 px-4 py-3 rounded-xl bg-green-500 text-white font-medium hover:bg-green-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                >
                    {isLoading ? (
                        <Loader2 className="w-4 h-4 animate-spin" />
                    ) : (
                        <>
                            <Check className="w-4 h-4" />
                            Signer le contrat
                        </>
                    )}
                </button>
            </div>
        </div>
    );
}

// ===========================================
// MAIN COMPONENT
// ===========================================

export default function ContractDetailPage() {
    const params = useParams();
    const router = useRouter();
    const contractId = params.id as string;

    const [contract, setContract] = useState<ContractDetail | null>(null);
    const [isLoading, setIsLoading] = useState(true);
    const [isSigning, setIsSigning] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [userId, setUserId] = useState<string | null>(null);
    const [userRole, setUserRole] = useState<'TALENT' | 'CLIENT'>('CLIENT');

    useEffect(() => {
        fetchContract();
    }, [contractId]);

    const fetchContract = async () => {
        setIsLoading(true);
        try {
            const token = getToken();
            const headers: Record<string, string> = { 'Content-Type': 'application/json' };
            if (token) {
                headers['Authorization'] = `Bearer ${token}`;
            }

            // Get user info
            const meRes = await fetch(`${getApiBase()}/auth/me`, { headers });
            if (meRes.ok) {
                const user = await meRes.json();
                setUserId(user.id);
                setUserRole(user.role === 'TALENT' ? 'TALENT' : 'CLIENT');
            }

            // Get contract
            const res = await fetch(`${getApiBase()}/contracts/${contractId}`, { headers });
            if (!res.ok) throw new Error('Contrat non trouvé');

            const data = await res.json();
            setContract(data);
        } catch (err: any) {
            setError(err.message);
            // Mock data
            setContract({
                id: contractId,
                reference: 'CTR-2024-001',
                type: 'MISSION_SOS',
                status: 'PENDING_CLIENT',
                title: 'Contrat de mission - Remplacement aide-soignant',
                content: `
# CONTRAT DE PRESTATION DE SERVICE

## ARTICLE 1 - OBJET
Le présent contrat a pour objet de définir les conditions dans lesquelles le Prestataire s'engage à réaliser une mission de remplacement au sein de l'établissement du Client.

## ARTICLE 2 - DURÉE
La mission débutera le **15 janvier 2024** et se terminera le **17 janvier 2024**.

## ARTICLE 3 - RÉMUNÉRATION
Le Prestataire percevra une rémunération de **25,00 € / heure**, soit un total estimé de **400,00 €** pour la durée de la mission.

## ARTICLE 4 - OBLIGATIONS
Le Prestataire s'engage à :
- Respecter le règlement intérieur de l'établissement
- Assurer les soins conformément aux protocoles en vigueur
- Maintenir la confidentialité des informations

## ARTICLE 5 - RESPONSABILITÉ
Le Prestataire déclare être titulaire d'une assurance responsabilité civile professionnelle.
                `,
                totalAmount: 40000,
                platformFee: 4000,
                startDate: new Date(Date.now() + 86400000).toISOString(),
                endDate: new Date(Date.now() + 259200000).toISOString(),
                TALENTSignedAt: new Date().toISOString(),
                createdAt: new Date(Date.now() - 86400000).toISOString(),
                TALENT: {
                    id: 'e1',
                    email: 'marie.dupont@email.com',
                    profile: { firstName: 'Marie', lastName: 'Dupont' },
                },
                client: {
                    id: 'c1',
                    email: 'contact@ehpad-lilas.fr',
                    establishment: { name: 'EHPAD Les Lilas', address: '12 rue des Fleurs', city: 'Lyon' },
                },
                mission: {
                    id: 'm1',
                    title: 'Remplacement weekend',
                    description: 'Remplacement aide-soignant pour le weekend',
                    city: 'Lyon',
                    address: '12 rue des Fleurs',
                    hourlyRate: 25,
                    startDate: new Date(Date.now() + 86400000).toISOString(),
                    endDate: new Date(Date.now() + 259200000).toISOString(),
                },
            });
        } finally {
            setIsLoading(false);
        }
    };

    const handleSign = async (signatureDataUrl: string) => {
        setIsSigning(true);
        try {
            const token = getToken();
            const signHeaders: Record<string, string> = {
                'Content-Type': 'application/json',
            };
            if (token) {
                signHeaders['Authorization'] = `Bearer ${token}`;
            }
            const res = await fetch(`${getApiBase()}/contracts/${contractId}/sign`, {
                method: 'POST',
                headers: signHeaders,
                body: JSON.stringify({ signature: signatureDataUrl }),
            });

            if (res.ok) {
                await fetchContract();
            } else {
                throw new Error('Erreur lors de la signature');
            }
        } catch (err: any) {
            setError(err.message);
        } finally {
            setIsSigning(false);
        }
    };

    // Determine if user needs to sign
    const needsToSign =
        contract &&
        ((userRole === 'CLIENT' && contract.status === 'PENDING_CLIENT') ||
            (userRole === 'TALENT' && contract.status === 'PENDING_TALENT') ||
            (contract.status === 'PENDING' && userRole === 'TALENT' && !contract.TALENTSignedAt));

    const isSigned =
        contract &&
        (contract.status === 'SIGNED' || contract.status === 'IN_PROGRESS' || contract.status === 'COMPLETED');

    if (isLoading) {
        return (
            <div className="min-h-screen bg-slate-50 flex items-center justify-center">
                <Loader2 className="w-8 h-8 animate-spin text-brand-600" />
            </div>
        );
    }

    if (!contract) {
        return (
            <div className="min-h-screen bg-slate-50 flex items-center justify-center">
                <div className="text-center">
                    <AlertTriangle className="w-12 h-12 text-red-500 mx-auto mb-4" />
                    <p className="text-slate-600">{error || 'Contrat non trouvé'}</p>
                    <Link href="/contracts" className="text-brand-600 hover:underline mt-4 inline-block">
                        Retour aux contrats
                    </Link>
                </div>
            </div>
        );
    }

    const TALENTName = contract.TALENT.profile
        ? `${contract.TALENT.profile.firstName} ${contract.TALENT.profile.lastName}`
        : contract.TALENT.email;

    const clientName = contract.client?.establishment?.name ||
        (contract.client?.profile ? `${contract.client.profile.firstName} ${contract.client.profile.lastName}` : contract.client?.email);

    return (
        <div className="min-h-screen bg-slate-50 pb-20">
            {/* Header */}
            <header className="bg-white border-b border-slate-200 sticky top-0 z-40">
                <div className="max-w-4xl mx-auto px-4">
                    <div className="flex items-center justify-between h-16">
                        <div className="flex items-center gap-4">
                            <button onClick={() => router.back()} className="p-2 rounded-xl hover:bg-slate-100">
                                <ChevronLeft className="w-5 h-5 text-slate-600" />
                            </button>
                            <div>
                                <h1 className="font-bold text-slate-900">
                                    {contract.reference || 'Contrat'}
                                </h1>
                                <p className="text-xs text-slate-500">{contract.title}</p>
                            </div>
                        </div>
                        {(contract.pdfUrl || contract.status === 'SIGNED') && (
                            <button
                                onClick={async () => {
                                    try {
                                        const token = getToken();
                                        const response = await fetch(`${getApiBase()}/contracts/${contract.id}/download`, {
                                            headers: token ? { Authorization: `Bearer ${token}` } : {},
                                        });
                                        if (!response.ok) throw new Error('Téléchargement échoué');
                                        const blob = await response.blob();
                                        const url = window.URL.createObjectURL(blob);
                                        const a = document.createElement('a');
                                        a.href = url;
                                        a.download = `contrat-${contract.reference || contract.id.slice(0, 8)}.pdf`;
                                        document.body.appendChild(a);
                                        a.click();
                                        window.URL.revokeObjectURL(url);
                                        document.body.removeChild(a);
                                    } catch (err) {
                                        console.error('Download error:', err);
                                        alert('Erreur lors du téléchargement du PDF');
                                    }
                                }}
                                className="flex items-center gap-2 px-4 py-2 rounded-xl bg-slate-100 text-slate-600 hover:bg-slate-200 shadow-sm hover:shadow-md active:scale-95 transition-all"
                            >
                                <Download className="w-4 h-4" />
                                PDF
                            </button>
                        )}
                    </div>
                </div>
            </header>

            <main className="max-w-4xl mx-auto px-4 py-6 space-y-6">
                {/* Status Banner */}
                {needsToSign && (
                    <motion.div
                        initial={{ opacity: 0, y: -10 }}
                        animate={{ opacity: 1, y: 0 }}
                        className="p-4 bg-gradient-to-r from-rose-500 to-rose-600 rounded-2xl text-white flex items-center gap-3"
                    >
                        <PenTool className="w-6 h-6" />
                        <div>
                            <p className="font-semibold">Signature requise</p>
                            <p className="text-sm opacity-90">Veuillez lire et signer ce contrat</p>
                        </div>
                    </motion.div>
                )}

                {isSigned && (
                    <motion.div
                        initial={{ opacity: 0, y: -10 }}
                        animate={{ opacity: 1, y: 0 }}
                        className="p-4 bg-green-500 rounded-2xl text-white flex items-center gap-3"
                    >
                        <CheckCircle className="w-6 h-6" />
                        <div>
                            <p className="font-semibold">Contrat signé</p>
                            <p className="text-sm opacity-90">
                                Signé le {contract.clientSignedAt ? formatDateTime(contract.clientSignedAt) : formatDateTime(contract.TALENTSignedAt!)}
                            </p>
                        </div>
                    </motion.div>
                )}

                {/* Parties */}
                <div className="bg-white rounded-2xl border border-slate-100 p-6">
                    <h2 className="font-semibold text-slate-900 mb-4">Parties au contrat</h2>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        {/* TALENT */}
                        <div className="p-4 bg-purple-50 rounded-xl">
                            <div className="flex items-center gap-3 mb-2">
                                <div className="w-10 h-10 rounded-full bg-purple-100 flex items-center justify-center">
                                    <User className="w-5 h-5 text-purple-600" />
                                </div>
                                <div>
                                    <p className="font-medium text-slate-900">{TALENTName}</p>
                                    <p className="text-xs text-slate-500">Prestataire (TALENT)</p>
                                </div>
                            </div>
                            {contract.TALENTSignedAt && (
                                <div className="flex items-center gap-2 mt-3 text-sm text-green-600">
                                    <CheckCircle className="w-4 h-4" />
                                    Signé le {formatDateTime(contract.TALENTSignedAt)}
                                </div>
                            )}
                        </div>

                        {/* Client */}
                        <div className="p-4 bg-indigo-50 rounded-xl">
                            <div className="flex items-center gap-3 mb-2">
                                <div className="w-10 h-10 rounded-full bg-indigo-100 flex items-center justify-center">
                                    <Building2 className="w-5 h-5 text-indigo-600" />
                                </div>
                                <div>
                                    <p className="font-medium text-slate-900">{clientName}</p>
                                    <p className="text-xs text-slate-500">Client</p>
                                </div>
                            </div>
                            {contract.clientSignedAt && (
                                <div className="flex items-center gap-2 mt-3 text-sm text-green-600">
                                    <CheckCircle className="w-4 h-4" />
                                    Signé le {formatDateTime(contract.clientSignedAt)}
                                </div>
                            )}
                        </div>
                    </div>
                </div>

                {/* Mission Details */}
                {contract.mission && (
                    <div className="bg-white rounded-2xl border border-slate-100 p-6">
                        <h2 className="font-semibold text-slate-900 mb-4">Détails de la mission</h2>
                        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                            <div className="p-3 bg-slate-50 rounded-xl">
                                <MapPin className="w-5 h-5 text-slate-400 mb-1" />
                                <p className="text-sm text-slate-500">Lieu</p>
                                <p className="font-medium text-slate-900">{contract.mission.city}</p>
                            </div>
                            <div className="p-3 bg-slate-50 rounded-xl">
                                <Calendar className="w-5 h-5 text-slate-400 mb-1" />
                                <p className="text-sm text-slate-500">Début</p>
                                <p className="font-medium text-slate-900">{formatDate(contract.mission.startDate)}</p>
                            </div>
                            <div className="p-3 bg-slate-50 rounded-xl">
                                <Calendar className="w-5 h-5 text-slate-400 mb-1" />
                                <p className="text-sm text-slate-500">Fin</p>
                                <p className="font-medium text-slate-900">{formatDate(contract.mission.endDate)}</p>
                            </div>
                            <div className="p-3 bg-slate-50 rounded-xl">
                                <Euro className="w-5 h-5 text-slate-400 mb-1" />
                                <p className="text-sm text-slate-500">Taux horaire</p>
                                <p className="font-medium text-slate-900">{contract.mission.hourlyRate}€/h</p>
                            </div>
                        </div>
                    </div>
                )}

                {/* Contract Content */}
                <div className="bg-white rounded-2xl border border-slate-100 p-6">
                    <h2 className="font-semibold text-slate-900 mb-4">Contenu du contrat</h2>
                    <div className="prose prose-slate max-w-none text-sm">
                        <div
                            className="whitespace-pre-wrap"
                            dangerouslySetInnerHTML={{
                                __html: contract.content
                                    .replace(/^# (.*$)/gm, '<h2 class="text-lg font-bold mt-6 mb-2">$1</h2>')
                                    .replace(/^## (.*$)/gm, '<h3 class="text-base font-semibold mt-4 mb-2">$1</h3>')
                                    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
                                    .replace(/- (.*$)/gm, '<li class="ml-4">$1</li>'),
                            }}
                        />
                    </div>
                </div>

                {/* Financial Summary */}
                {contract.totalAmount && (
                    <div className="bg-white rounded-2xl border border-slate-100 p-6">
                        <h2 className="font-semibold text-slate-900 mb-4">Récapitulatif financier</h2>
                        <div className="space-y-3">
                            <div className="flex justify-between text-sm">
                                <span className="text-slate-600">Montant total</span>
                                <span className="font-semibold text-slate-900">{formatCurrency(contract.totalAmount)}</span>
                            </div>
                            {contract.platformFee && (
                                <div className="flex justify-between text-sm">
                                    <span className="text-slate-600">Frais de service</span>
                                    <span className="text-slate-500">{formatCurrency(contract.platformFee)}</span>
                                </div>
                            )}
                            <div className="border-t border-slate-100 pt-3 flex justify-between">
                                <span className="font-semibold text-slate-900">Net à percevoir</span>
                                <span className="font-bold text-green-600">
                                    {formatCurrency(contract.totalAmount - (contract.platformFee || 0))}
                                </span>
                            </div>
                        </div>
                    </div>
                )}

                {/* Signature Area */}
                {needsToSign && (
                    <div className="bg-white rounded-2xl border-2 border-brand-200 p-6">
                        <div className="flex items-center gap-3 mb-4">
                            <div className="w-10 h-10 rounded-full bg-brand-100 flex items-center justify-center">
                                <PenTool className="w-5 h-5 text-brand-600" />
                            </div>
                            <div>
                                <h2 className="font-semibold text-slate-900">Votre signature</h2>
                                <p className="text-sm text-slate-500">
                                    En signant, vous acceptez les termes de ce contrat
                                </p>
                            </div>
                        </div>

                        <SignaturePad onSign={handleSign} isLoading={isSigning} />

                        <p className="text-xs text-slate-400 mt-4 text-center">
                            <Shield className="w-3 h-3 inline mr-1" />
                            Votre signature sera horodatée et votre adresse IP enregistrée pour garantir l'authenticité
                        </p>
                    </div>
                )}

                {/* Existing Signatures */}
                {(contract.signatureUrl || contract.clientSignature) && (
                    <div className="bg-white rounded-2xl border border-slate-100 p-6">
                        <h2 className="font-semibold text-slate-900 mb-4">Signatures</h2>
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                            {contract.signatureUrl && (
                                <div className="p-4 bg-slate-50 rounded-xl">
                                    <p className="text-sm text-slate-500 mb-2">Signature du prestataire</p>
                                    <img
                                        src={contract.signatureUrl}
                                        alt="Signature TALENT"
                                        className="max-h-20 bg-white rounded border border-slate-200 p-2"
                                    />
                                    {contract.TALENTSignedAt && (
                                        <p className="text-xs text-slate-400 mt-2">
                                            {formatDateTime(contract.TALENTSignedAt)}
                                        </p>
                                    )}
                                </div>
                            )}
                            {contract.clientSignature && (
                                <div className="p-4 bg-slate-50 rounded-xl">
                                    <p className="text-sm text-slate-500 mb-2">Signature du client</p>
                                    <img
                                        src={contract.clientSignature}
                                        alt="Signature Client"
                                        className="max-h-20 bg-white rounded border border-slate-200 p-2"
                                    />
                                    {contract.clientSignedAt && (
                                        <p className="text-xs text-slate-400 mt-2">
                                            {formatDateTime(contract.clientSignedAt)}
                                        </p>
                                    )}
                                </div>
                            )}
                        </div>
                    </div>
                )}
            </main>
        </div>
    );
}

