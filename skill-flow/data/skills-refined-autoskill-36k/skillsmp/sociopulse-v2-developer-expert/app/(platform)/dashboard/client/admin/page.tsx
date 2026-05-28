'use client';

import { motion } from 'framer-motion';
import Link from 'next/link';
import {
    FileSignature,
    FileText,
    AlertTriangle,
    Download,
    Pen,
    CheckCircle,
    Clock,
    ChevronRight,
    Shield
} from 'lucide-react';
import { Badge } from '@/components/ui';
import {
    mockContracts,
    formatCurrency,
    formatDate
} from '@/components/dashboard/client/mock-data';

const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
        opacity: 1,
        transition: { staggerChildren: 0.1 }
    }
};

const itemVariants = {
    hidden: { opacity: 0, y: 10 },
    visible: { opacity: 1, y: 0 }
};

export default function ClientAdminPage() {
    const pendingDocuments = mockContracts.filter(c => c.status === 'PENDING');
    const signedDocuments = mockContracts.filter(c => c.status === 'SIGNED');

    return (
        <motion.div
            variants={containerVariants}
            initial="hidden"
            animate="visible"
            className="p-6 space-y-6"
        >
            {/* Header */}
            <motion.div variants={itemVariants}>
                <h1 className="text-2xl font-bold text-slate-900">Administratif</h1>
                <p className="text-slate-500">
                    Contrats, devis et conformité légale
                </p>
            </motion.div>

            {/* Alert Banner */}
            {pendingDocuments.length > 0 && (
                <motion.div
                    variants={itemVariants}
                    className="flex items-center justify-between gap-4 rounded-xl border border-amber-200 bg-amber-50 p-4"
                >
                    <div className="flex items-center gap-3">
                        <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-amber-100">
                            <AlertTriangle className="h-5 w-5 text-amber-600" />
                        </div>
                        <div>
                            <p className="font-medium text-amber-800">
                                {pendingDocuments.length} document{pendingDocuments.length > 1 ? 's' : ''} requièrent votre attention immédiate
                            </p>
                            <p className="text-sm text-amber-600">
                                Les missions ne peuvent démarrer sans signature
                            </p>
                        </div>
                    </div>
                    <Link
                        href="#pending-docs"
                        className="inline-flex items-center gap-2 rounded-full bg-amber-600 px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-amber-700"
                    >
                        <Pen className="h-4 w-4" />
                        Signer maintenant
                    </Link>
                </motion.div>
            )}

            {/* Safety Lock Warning */}
            <motion.div
                variants={itemVariants}
                className="flex items-center gap-3 rounded-xl border border-slate-200 bg-slate-50 p-4"
            >
                <Shield className="h-5 w-5 text-slate-500" />
                <p className="text-sm text-slate-600">
                    <strong>Verrou de sécurité :</strong> Une mission ne peut être lancée que si le contrat correspondant est signé par les deux parties.
                </p>
            </motion.div>

            {/* Stats Row */}
            <motion.div variants={itemVariants} className="grid grid-cols-1 gap-4 sm:grid-cols-3">
                <StatCard
                    label="En attente"
                    value={pendingDocuments.length}
                    icon={Clock}
                    color="amber"
                />
                <StatCard
                    label="Signés"
                    value={signedDocuments.length}
                    icon={CheckCircle}
                    color="emerald"
                />
                <StatCard
                    label="Total documents"
                    value={mockContracts.length}
                    icon={FileText}
                    color="slate"
                />
            </motion.div>

            {/* Documents Table */}
            <motion.div
                variants={itemVariants}
                id="pending-docs"
                className="overflow-hidden rounded-xl border border-slate-200 bg-white shadow-sm"
            >
                <div className="border-b border-slate-200 px-6 py-4">
                    <h2 className="text-lg font-semibold text-slate-900">Documents</h2>
                </div>
                <div className="overflow-x-auto">
                    <table className="w-full">
                        <thead className="bg-slate-50 text-left text-sm text-slate-500">
                            <tr>
                                <th className="px-6 py-3 font-medium">Document</th>
                                <th className="px-6 py-3 font-medium">Type</th>
                                <th className="px-6 py-3 font-medium">Date</th>
                                <th className="px-6 py-3 font-medium">Montant</th>
                                <th className="px-6 py-3 font-medium">Statut</th>
                                <th className="px-6 py-3 font-medium text-right">Action</th>
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-slate-200">
                            {mockContracts.map((doc) => (
                                <DocumentRow key={doc.id} document={doc} />
                            ))}
                        </tbody>
                    </table>
                </div>
            </motion.div>

            {/* Quick Links */}
            <motion.div variants={itemVariants} className="grid grid-cols-1 gap-4 md:grid-cols-2">
                <QuickLink
                    title="Historique des contrats"
                    description="Consultez tous vos contrats passés"
                    href="/contracts"
                    icon={FileSignature}
                />
                <QuickLink
                    title="Paramètres facturation"
                    description="Configurer SIRET et Chorus Pro"
                    href="/dashboard/client/settings"
                    icon={FileText}
                />
            </motion.div>
        </motion.div>
    );
}

// Sub-components

interface StatCardProps {
    label: string;
    value: number;
    icon: React.ElementType;
    color: 'amber' | 'emerald' | 'slate';
}

function StatCard({ label, value, icon: Icon, color }: StatCardProps) {
    const colorClasses = {
        amber: 'bg-amber-50 text-amber-600',
        emerald: 'bg-emerald-50 text-emerald-600',
        slate: 'bg-slate-100 text-slate-600',
    };

    return (
        <div className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm">
            <div className="flex items-center gap-3">
                <div className={`rounded-lg p-2 ${colorClasses[color]}`}>
                    <Icon className="h-5 w-5" />
                </div>
                <div>
                    <p className="text-2xl font-bold text-slate-900">{value}</p>
                    <p className="text-sm text-slate-500">{label}</p>
                </div>
            </div>
        </div>
    );
}

interface DocumentRowProps {
    document: {
        id: string;
        reference: string;
        documentType: 'CONTRACT' | 'QUOTE';
        status: string;
        talentName: string;
        totalAmount: number;
        createdAt: Date;
        signedAt?: Date;
    };
}

function DocumentRow({ document }: DocumentRowProps) {
    const isPending = document.status === 'PENDING';
    const typeLabel = document.documentType === 'CONTRACT' ? 'Contrat' : 'Devis';

    return (
        <tr className="transition-colors hover:bg-slate-50">
            <td className="px-6 py-4">
                <div className="flex items-center gap-3">
                    <div className={`rounded-lg p-2 ${isPending ? 'bg-amber-50 text-amber-600' : 'bg-emerald-50 text-emerald-600'}`}>
                        <FileSignature className="h-4 w-4" />
                    </div>
                    <div>
                        <p className="font-medium text-slate-900">{document.reference}</p>
                        <p className="text-sm text-slate-500">{document.talentName}</p>
                    </div>
                </div>
            </td>
            <td className="px-6 py-4">
                <Badge variant={document.documentType === 'CONTRACT' ? 'default' : 'secondary'}>
                    {typeLabel}
                </Badge>
            </td>
            <td className="px-6 py-4 text-slate-600">
                {formatDate(document.createdAt)}
            </td>
            <td className="px-6 py-4 font-medium text-slate-900">
                {formatCurrency(document.totalAmount)}
            </td>
            <td className="px-6 py-4">
                <Badge variant={isPending ? 'warning' : 'success'}>
                    {isPending ? 'À signer' : 'Signé'}
                </Badge>
            </td>
            <td className="px-6 py-4 text-right">
                {isPending ? (
                    <button className="inline-flex items-center gap-2 rounded-full bg-amber-600 px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-amber-700">
                        <Pen className="h-4 w-4" />
                        Signer
                    </button>
                ) : (
                    <button className="inline-flex items-center gap-2 rounded-full border border-slate-200 bg-white px-4 py-2 text-sm font-medium text-slate-700 transition-colors hover:bg-slate-50">
                        <Download className="h-4 w-4" />
                        PDF
                    </button>
                )}
            </td>
        </tr>
    );
}

interface QuickLinkProps {
    title: string;
    description: string;
    href: string;
    icon: React.ElementType;
}

function QuickLink({ title, description, href, icon: Icon }: QuickLinkProps) {
    return (
        <Link
            href={href}
            className="group flex items-center justify-between rounded-xl border border-slate-200 bg-white p-4 shadow-sm transition-all hover:border-slate-300 hover:shadow-md"
        >
            <div className="flex items-center gap-3">
                <div className="rounded-lg bg-slate-100 p-2 text-slate-600">
                    <Icon className="h-5 w-5" />
                </div>
                <div>
                    <p className="font-medium text-slate-900">{title}</p>
                    <p className="text-sm text-slate-500">{description}</p>
                </div>
            </div>
            <ChevronRight className="h-5 w-5 text-slate-400 transition-transform group-hover:translate-x-0.5" />
        </Link>
    );
}
