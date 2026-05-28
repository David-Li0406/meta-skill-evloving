'use client';

import { useParams, useRouter } from 'next/navigation';
import { motion } from 'framer-motion';
import {
    ArrowLeft,
    Star,
    MapPin,
    Clock,
    Video,
    Shield,
    Award,
    Calendar
} from 'lucide-react';
import Link from 'next/link';
import { SlotPicker } from '@/components/video';

// Mock service data
const MOCK_SERVICE = {
    id: 'service_video_1',
    type: 'COACHING_VIDEO',
    name: 'Coaching Bien-être & Relaxation',
    description: 'Séances individuelles de relaxation et gestion du stress. Techniques de respiration, méditation guidée et conseils personnalisés pour améliorer votre bien-être au quotidien.',
    provider: {
        id: 'provider_1',
        name: 'Dr. Marie Dupont',
        title: 'Psychologue clinicienne',
        avatar: null,
        rating: 4.9,
        reviewCount: 47,
        city: 'Paris',
        verified: true,
        yearsExperience: 12,
    },
    duration: 60,
    price: 65,
    features: [
        'Séance 100% en visio',
        'Enregistrement disponible',
        'Support par chat 48h après',
        'Programme personnalisé',
    ],
};

export default function ServiceVideoDetailPage() {
    const params = useParams();
    const router = useRouter();
    const serviceId = params.id as string;

    const service = MOCK_SERVICE;
    const provider = service.provider;

    const handleSlotConfirm = (date: Date, time: string) => {
        // In production, create booking and redirect to payment
        console.log('Booking confirmed:', { date, time, serviceId });

        // Navigate to checkout or live session
        router.push(`/checkout?service=${serviceId}&date=${date.toISOString()}&time=${time}`);
    };

    return (
        <div className="min-h-screen bg-slate-50">
            {/* Header */}
            <header className="bg-white border-b border-slate-100 sticky top-0 z-40">
                <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="flex items-center h-16 gap-4">
                        <Link
                            href="/services"
                            className="p-2 rounded-lg hover:bg-slate-100 text-slate-400 hover:text-slate-600 transition-colors"
                        >
                            <ArrowLeft className="w-5 h-5" />
                        </Link>
                        <div className="flex items-center gap-2">
                            <Video className="w-5 h-5 text-purple-500" />
                            <span className="text-sm font-medium text-slate-600">Consultation Vidéo</span>
                        </div>
                    </div>
                </div>
            </header>

            <main className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                    {/* Left Column - Service Details */}
                    <div className="lg:col-span-2 space-y-6">
                        {/* Service Card */}
                        <motion.div
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            className="bg-white rounded-2xl shadow-soft overflow-hidden"
                        >
                            {/* Gradient Header */}
                            <div className="h-32 bg-gradient-to-br from-purple-600 via-indigo-600 to-purple-700 relative">
                                <div className="absolute inset-0 opacity-10">
                                    <div className="absolute inset-0" style={{
                                        backgroundImage: `radial-gradient(circle at 2px 2px, white 1px, transparent 0)`,
                                        backgroundSize: '24px 24px',
                                    }} />
                                </div>
                            </div>

                            <div className="px-6 py-6 -mt-12 relative">
                                {/* Provider Avatar */}
                                <div className="flex items-end gap-4 mb-6">
                                    <div className="w-24 h-24 rounded-2xl bg-white shadow-lg border-4 border-white overflow-hidden">
                                        {provider.avatar ? (
                                            <img src={provider.avatar} alt={provider.name} className="w-full h-full object-cover" />
                                        ) : (
                                            <div className="w-full h-full bg-gradient-to-br from-purple-500 to-indigo-500 flex items-center justify-center">
                                                <span className="text-3xl font-bold text-white">
                                                    {(provider.name || '?').charAt(0)}
                                                </span>
                                            </div>
                                        )}
                                    </div>

                                    <div className="pb-1">
                                        <div className="flex items-center gap-2 mb-1">
                                            <h2 className="text-xl font-bold text-slate-900">{provider.name}</h2>
                                            {provider.verified && (
                                                <Shield className="w-5 h-5 text-blue-500" />
                                            )}
                                        </div>
                                        <p className="text-sm text-slate-500">{provider.title}</p>
                                        <div className="flex items-center gap-3 mt-2">
                                            <div className="flex items-center gap-1">
                                                <Star className="w-4 h-4 text-amber-400 fill-amber-400" />
                                                <span className="text-sm font-semibold text-slate-900">{provider.rating}</span>
                                                <span className="text-sm text-slate-400">({provider.reviewCount} avis)</span>
                                            </div>
                                            <div className="flex items-center gap-1 text-sm text-slate-500">
                                                <MapPin className="w-4 h-4" />
                                                {provider.city}
                                            </div>
                                        </div>
                                    </div>
                                </div>

                                {/* Service Title */}
                                <h1 className="text-2xl font-bold text-slate-900 mb-4">{service.name}</h1>

                                {/* Meta Info */}
                                <div className="flex flex-wrap items-center gap-4 mb-6">
                                    <div className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-purple-50 text-purple-700">
                                        <Clock className="w-4 h-4" />
                                        <span className="text-sm font-medium">Durée : {service.duration} min</span>
                                    </div>
                                    <div className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-green-50 text-green-700">
                                        <Video className="w-4 h-4" />
                                        <span className="text-sm font-medium">100% Visio</span>
                                    </div>
                                    <div className="px-3 py-1.5 rounded-lg bg-slate-100">
                                        <span className="text-lg font-bold text-slate-900">{service.price}€</span>
                                        <span className="text-sm text-slate-500"> / séance</span>
                                    </div>
                                </div>

                                {/* Description */}
                                <div className="mb-6">
                                    <h3 className="font-semibold text-slate-900 mb-2">Description</h3>
                                    <p className="text-slate-600 leading-relaxed">{service.description}</p>
                                </div>

                                {/* Features */}
                                <div>
                                    <h3 className="font-semibold text-slate-900 mb-3">Ce qui est inclus</h3>
                                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                                        {service.features.map((feature, index) => (
                                            <div key={index} className="flex items-center gap-2">
                                                <div className="w-5 h-5 rounded-full bg-green-100 flex items-center justify-center">
                                                    <svg className="w-3 h-3 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 13l4 4L19 7" />
                                                    </svg>
                                                </div>
                                                <span className="text-sm text-slate-600">{feature}</span>
                                            </div>
                                        ))}
                                    </div>
                                </div>
                            </div>
                        </motion.div>

                        {/* Experience Badge */}
                        <motion.div
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ delay: 0.1 }}
                            className="bg-white rounded-2xl shadow-soft p-5 flex items-center gap-4"
                        >
                            <div className="w-14 h-14 rounded-xl bg-amber-100 flex items-center justify-center">
                                <Award className="w-7 h-7 text-amber-600" />
                            </div>
                            <div>
                                <p className="font-semibold text-slate-900">{provider.yearsExperience} ans d'expérience</p>
                                <p className="text-sm text-slate-500">Professionnel certifié et vérifié</p>
                            </div>
                        </motion.div>
                    </div>

                    {/* Right Column - Slot Picker */}
                    <div className="lg:col-span-1">
                        <div className="sticky top-24">
                            <SlotPicker
                                providerId={provider.id}
                                providerName={provider.name}
                                duration={service.duration}
                                price={service.price}
                                onConfirm={handleSlotConfirm}
                            />
                        </div>
                    </div>
                </div>
            </main>
        </div>
    );
}
