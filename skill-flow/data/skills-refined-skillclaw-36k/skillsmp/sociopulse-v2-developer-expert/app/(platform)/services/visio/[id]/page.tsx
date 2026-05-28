'use client';

import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { ArrowLeft, Star, MapPin, Clock, Shield, Video } from 'lucide-react';
import { BookingCalendar } from '@/components/bookings';
import { Badge } from '@/components/ui';

// Mock service data - in production, fetch based on params.id
const mockService = {
    id: 'service-123',
    title: 'Supervision individuelle - Analyse de pratique',
    description: 'Séance de supervision individuelle pour professionnels du secteur social et médico-social. Analyse de pratique, soutien et accompagnement personnalisé.',
    price: 75,
    duration: 60,
    talent: {
        id: 'talent-456',
        name: 'Marie Dupont',
        title: 'Psychologue clinicienne',
        avatar: '/images/avatars/talent-1.jpg',
        rating: 4.9,
        reviewCount: 47,
        location: 'Paris, France',
        verified: true,
    },
    features: [
        'Visioconférence sécurisée',
        'Replay disponible 48h',
        'Support écrit post-session',
        'Annulation gratuite 24h avant',
    ],
    availableDays: [1, 2, 3, 4, 5], // Mon-Fri
};

export default function ServiceBookingPage({ params }: { params: { id: string } }) {
    const router = useRouter();

    const handleBookingComplete = (booking: any) => {
        console.log('Booking completed:', booking);
        // Redirect is handled inside BookingCalendar
    };

    return (
        <div className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-teal-50/20">
            <div className="max-w-6xl mx-auto px-4 py-8">
                {/* Back Button */}
                <Link
                    href="/services"
                    className="inline-flex items-center gap-2 text-slate-600 hover:text-slate-900 mb-6 group transition-colors"
                >
                    <ArrowLeft className="w-4 h-4 group-hover:-translate-x-1 transition-transform" />
                    <span className="text-sm font-medium">Retour aux services</span>
                </Link>

                <div className="grid lg:grid-cols-5 gap-8">
                    {/* Left Column: Service Details */}
                    <div className="lg:col-span-3 space-y-6">
                        {/* Service Header */}
                        <div className="bg-white rounded-2xl border border-slate-200 p-6 sm:p-8">
                            <div className="flex items-start gap-4">
                                {/* Talent Avatar */}
                                <div className="relative flex-shrink-0">
                                    <div className="w-16 h-16 sm:w-20 sm:h-20 rounded-full bg-gradient-to-br from-teal-400 to-teal-600 flex items-center justify-center text-white text-2xl font-bold">
                                        {mockService.talent.name.charAt(0)}
                                    </div>
                                    {mockService.talent.verified && (
                                        <div className="absolute -bottom-1 -right-1 w-6 h-6 bg-teal-500 rounded-full flex items-center justify-center border-2 border-white">
                                            <Shield className="w-3 h-3 text-white" />
                                        </div>
                                    )}
                                </div>

                                {/* Info */}
                                <div className="flex-1 min-w-0">
                                    <div className="flex items-center gap-2 flex-wrap mb-1">
                                        <Badge className="bg-teal-100 text-teal-700 hover:bg-teal-100">
                                            <Video className="w-3 h-3 mr-1" />
                                            Visio 1-to-1
                                        </Badge>
                                    </div>
                                    <h1 className="text-xl sm:text-2xl font-bold text-slate-900 mb-1">
                                        {mockService.title}
                                    </h1>
                                    <p className="text-slate-600 font-medium">
                                        {mockService.talent.name} · {mockService.talent.title}
                                    </p>
                                    <div className="flex items-center gap-4 mt-3 text-sm text-slate-500">
                                        <span className="flex items-center gap-1">
                                            <Star className="w-4 h-4 text-amber-400 fill-amber-400" />
                                            <span className="font-medium text-slate-700">{mockService.talent.rating}</span>
                                            <span>({mockService.talent.reviewCount} avis)</span>
                                        </span>
                                        <span className="flex items-center gap-1">
                                            <MapPin className="w-4 h-4" />
                                            {mockService.talent.location}
                                        </span>
                                    </div>
                                </div>
                            </div>
                        </div>

                        {/* Description */}
                        <div className="bg-white rounded-2xl border border-slate-200 p-6 sm:p-8">
                            <h2 className="text-lg font-semibold text-slate-900 mb-4">
                                À propos de cette séance
                            </h2>
                            <p className="text-slate-600 leading-relaxed mb-6">
                                {mockService.description}
                            </p>

                            {/* Session Details */}
                            <div className="grid sm:grid-cols-2 gap-4 p-4 bg-slate-50 rounded-xl">
                                <div className="flex items-center gap-3">
                                    <div className="w-10 h-10 rounded-lg bg-teal-100 flex items-center justify-center">
                                        <Clock className="w-5 h-5 text-teal-600" />
                                    </div>
                                    <div>
                                        <p className="text-sm text-slate-500">Durée</p>
                                        <p className="font-semibold text-slate-900">{mockService.duration} minutes</p>
                                    </div>
                                </div>
                                <div className="flex items-center gap-3">
                                    <div className="w-10 h-10 rounded-lg bg-teal-100 flex items-center justify-center">
                                        <Video className="w-5 h-5 text-teal-600" />
                                    </div>
                                    <div>
                                        <p className="text-sm text-slate-500">Format</p>
                                        <p className="font-semibold text-slate-900">Visioconférence</p>
                                    </div>
                                </div>
                            </div>
                        </div>

                        {/* Features */}
                        <div className="bg-white rounded-2xl border border-slate-200 p-6 sm:p-8">
                            <h2 className="text-lg font-semibold text-slate-900 mb-4">
                                Ce qui est inclus
                            </h2>
                            <ul className="space-y-3">
                                {mockService.features.map((feature, index) => (
                                    <li key={index} className="flex items-center gap-3 text-slate-600">
                                        <div className="w-5 h-5 rounded-full bg-teal-100 flex items-center justify-center flex-shrink-0">
                                            <svg className="w-3 h-3 text-teal-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={3}>
                                                <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
                                            </svg>
                                        </div>
                                        {feature}
                                    </li>
                                ))}
                            </ul>
                        </div>
                    </div>

                    {/* Right Column: Booking Calendar */}
                    <div className="lg:col-span-2">
                        <div className="lg:sticky lg:top-6">
                            <BookingCalendar
                                talentId={mockService.talent.id}
                                talentName={mockService.talent.name}
                                serviceName={mockService.title}
                                servicePrice={mockService.price}
                                serviceDuration={mockService.duration}
                                availableDays={mockService.availableDays}
                                onBookingComplete={handleBookingComplete}
                            />
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
