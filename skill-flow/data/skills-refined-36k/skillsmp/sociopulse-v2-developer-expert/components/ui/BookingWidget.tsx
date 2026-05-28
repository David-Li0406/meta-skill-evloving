"use client";

import { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import * as z from "zod";

// ============================================
// 🎨 LES TALENTS - Design System 2026
// ============================================
// Brand: Coral (#F87171) + Cool Gray (#6B7280)
// Style: Zero Interface, Minimalist, Premium B2B
// ============================================

const bookingSchema = z.object({
    formule: z.string().min(1, "Sélectionnez une formule"),
    ageGroup: z.string().min(1, "Sélectionnez une tranche d'âge"),
    participantCount: z
        .number()
        .min(1, "Min. 1")
        .max(30, "Max. 30"),
    objectives: z
        .string()
        .min(10, "Minimum 10 caractères")
        .max(500, "Maximum 500 caractères"),
    sessionDate: z.string().refine(
        (date) => new Date(date) > new Date(),
        { message: "Date future requise" }
    ),
    sessionTime: z.string().min(1, "Sélectionnez un horaire"),
});

type BookingFormData = z.infer<typeof bookingSchema>;

const FORMULES = [
    { id: "decouverte", label: "Découverte", price: 89, duration: "1h", popular: false },
    { id: "standard", label: "Standard", price: 149, duration: "2h", popular: true },
    { id: "premium", label: "Premium", price: 249, duration: "3h30", popular: false },
];

const AGE_GROUPS = [
    { id: "kids", label: "6-12 ans" },
    { id: "teens", label: "13-17 ans" },
    { id: "adults", label: "18+ ans" },
    { id: "mixed", label: "Mixte" },
];

const TIME_SLOTS = ["09:00", "10:30", "14:00", "15:30", "17:00"];

export default function BookingWidget() {
    const [isQuoteOpen, setIsQuoteOpen] = useState(false);

    const {
        register,
        handleSubmit,
        formState: { errors, isSubmitting },
        watch,
    } = useForm<BookingFormData>({
        resolver: zodResolver(bookingSchema),
        defaultValues: { participantCount: 1 },
    });

    const watchedFormule = watch("formule");
    const selectedFormule = FORMULES.find((f) => f.id === watchedFormule);

    const onSubmit = async (data: BookingFormData) => {
        console.log("Booking:", data);
    };

    return (
        <>
            {/* ========================================
          WIDGET CONTAINER - Premium Glass Effect
          ======================================== */}
            <div className="w-full max-w-[380px] lg:sticky lg:top-6">
                <div className="bg-white/80 backdrop-blur-xl rounded-3xl border border-gray-100 shadow-2xl shadow-gray-200/40 overflow-hidden">

                    {/* === HEADER: Pricing Zone === */}
                    <div className="px-8 pt-8 pb-6">
                        <div className="flex items-start justify-between">
                            <div>
                                <p className="text-[11px] font-semibold tracking-[0.2em] uppercase text-gray-400 mb-1">
                                    Tarif
                                </p>
                                <div className="flex items-baseline gap-1">
                                    <span className="text-4xl font-light tracking-tight text-gray-900">
                                        {selectedFormule?.price || 89}
                                    </span>
                                    <span className="text-lg font-light text-gray-400">€</span>
                                </div>
                                {selectedFormule && (
                                    <p className="text-sm text-gray-500 mt-1">
                                        {selectedFormule.label} · {selectedFormule.duration}
                                    </p>
                                )}
                            </div>

                            {/* Live Badge */}
                            {selectedFormule?.popular && (
                                <span className="px-3 py-1 bg-brand-50 text-brand-600 text-[10px] font-semibold tracking-wider uppercase rounded-full">
                                    Populaire
                                </span>
                            )}
                        </div>

                        {/* Quick Quote CTA */}
                        <button
                            onClick={() => setIsQuoteOpen(true)}
                            className="w-full mt-6 py-3.5 px-5 border border-gray-200 rounded-2xl text-sm font-medium text-gray-600 
                         transition-all duration-300 ease-out
                         hover:border-brand-300 hover:text-brand-600 hover:bg-brand-50/50
                         focus:outline-none focus:ring-2 focus:ring-brand-200 focus:ring-offset-2"
                        >
                            Demander un devis personnalisé
                        </button>
                    </div>

                    {/* === SEPARATOR === */}
                    <div className="h-px bg-gradient-to-r from-transparent via-gray-200 to-transparent" />

                    {/* === FORM: Booking Zone === */}
                    <form onSubmit={handleSubmit(onSubmit)} className="px-8 py-7 space-y-6">

                        {/* Formule Selection - Pills Style */}
                        <div className="space-y-3">
                            <label className="block text-[11px] font-semibold tracking-[0.15em] uppercase text-gray-400">
                                Formule
                            </label>
                            <div className="grid grid-cols-3 gap-2">
                                {FORMULES.map((formule) => (
                                    <label
                                        key={formule.id}
                                        className={`
                      relative flex flex-col items-center py-3 px-2 rounded-xl cursor-pointer
                      border-2 transition-all duration-200
                      ${watchedFormule === formule.id
                                                ? "border-brand-500 bg-brand-50/80"
                                                : "border-gray-100 hover:border-gray-200 bg-gray-50/50"
                                            }
                    `}
                                    >
                                        <input
                                            type="radio"
                                            value={formule.id}
                                            {...register("formule")}
                                            className="sr-only"
                                        />
                                        <span className={`text-xs font-medium ${watchedFormule === formule.id ? "text-brand-600" : "text-gray-600"
                                            }`}>
                                            {formule.label}
                                        </span>
                                        <span className={`text-[10px] mt-0.5 ${watchedFormule === formule.id ? "text-brand-500" : "text-gray-400"
                                            }`}>
                                            {formule.price}€
                                        </span>
                                    </label>
                                ))}
                            </div>
                            {errors.formule && (
                                <p className="text-xs text-red-500">{errors.formule.message}</p>
                            )}
                        </div>

                        {/* Age Group - Compact Pills */}
                        <div className="space-y-3">
                            <label className="block text-[11px] font-semibold tracking-[0.15em] uppercase text-gray-400">
                                Tranche d'âge
                            </label>
                            <div className="flex flex-wrap gap-2">
                                {AGE_GROUPS.map((group) => {
                                    const isSelected = watch("ageGroup") === group.id;
                                    return (
                                        <label
                                            key={group.id}
                                            className={`
                        px-4 py-2 rounded-full text-xs font-medium cursor-pointer
                        border transition-all duration-200
                        ${isSelected
                                                    ? "border-brand-500 bg-brand-600 text-white"
                                                    : "border-gray-200 text-gray-600 hover:border-gray-300"
                                                }
                      `}
                                        >
                                            <input
                                                type="radio"
                                                value={group.id}
                                                {...register("ageGroup")}
                                                className="sr-only"
                                            />
                                            {group.label}
                                        </label>
                                    );
                                })}
                            </div>
                            {errors.ageGroup && (
                                <p className="text-xs text-red-500">{errors.ageGroup.message}</p>
                            )}
                        </div>

                        {/* Participants - Modern Number Input */}
                        <div className="space-y-3">
                            <label className="block text-[11px] font-semibold tracking-[0.15em] uppercase text-gray-400">
                                Participants
                            </label>
                            <div className="relative">
                                <input
                                    type="number"
                                    min={1}
                                    max={30}
                                    {...register("participantCount", { valueAsNumber: true })}
                                    className="w-full h-12 px-4 bg-gray-50/80 border border-gray-100 rounded-xl
                           text-gray-900 font-medium
                           transition-all duration-200
                           focus:outline-none focus:bg-white focus:border-brand-300 focus:ring-4 focus:ring-brand-100
                           [appearance:textfield] [&::-webkit-outer-spin-button]:appearance-none [&::-webkit-inner-spin-button]:appearance-none"
                                    placeholder="12"
                                />
                                <span className="absolute right-4 top-1/2 -translate-y-1/2 text-xs text-gray-400 pointer-events-none">
                                    max 30
                                </span>
                            </div>
                            {errors.participantCount && (
                                <p className="text-xs text-red-500">{errors.participantCount.message}</p>
                            )}
                        </div>

                        {/* Date & Time - Inline */}
                        <div className="grid grid-cols-2 gap-3">
                            <div className="space-y-2">
                                <label className="block text-[11px] font-semibold tracking-[0.15em] uppercase text-gray-400">
                                    Date
                                </label>
                                <input
                                    type="date"
                                    {...register("sessionDate")}
                                    className="w-full h-12 px-4 bg-gray-50/80 border border-gray-100 rounded-xl
                           text-gray-900 text-sm
                           transition-all duration-200
                           focus:outline-none focus:bg-white focus:border-brand-300 focus:ring-4 focus:ring-brand-100"
                                />
                                {errors.sessionDate && (
                                    <p className="text-xs text-red-500">{errors.sessionDate.message}</p>
                                )}
                            </div>
                            <div className="space-y-2">
                                <label className="block text-[11px] font-semibold tracking-[0.15em] uppercase text-gray-400">
                                    Heure
                                </label>
                                <select
                                    {...register("sessionTime")}
                                    className="w-full h-12 px-4 bg-gray-50/80 border border-gray-100 rounded-xl
                           text-gray-900 text-sm appearance-none cursor-pointer
                           transition-all duration-200
                           focus:outline-none focus:bg-white focus:border-brand-300 focus:ring-4 focus:ring-brand-100"
                                    style={{
                                        backgroundImage: `url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 20 20'%3e%3cpath stroke='%239ca3af' stroke-linecap='round' stroke-linejoin='round' stroke-width='1.5' d='m6 8 4 4 4-4'/%3e%3c/svg%3e")`,
                                        backgroundPosition: "right 12px center",
                                        backgroundSize: "16px",
                                        backgroundRepeat: "no-repeat",
                                    }}
                                >
                                    <option value="">--:--</option>
                                    {TIME_SLOTS.map((time) => (
                                        <option key={time} value={time}>{time}</option>
                                    ))}
                                </select>
                                {errors.sessionTime && (
                                    <p className="text-xs text-red-500">{errors.sessionTime.message}</p>
                                )}
                            </div>
                        </div>

                        {/* Objectives - Clean Textarea */}
                        <div className="space-y-2">
                            <label className="block text-[11px] font-semibold tracking-[0.15em] uppercase text-gray-400">
                                Objectifs
                            </label>
                            <textarea
                                rows={3}
                                {...register("objectives")}
                                placeholder="Décrivez votre projet..."
                                className="w-full px-4 py-3 bg-gray-50/80 border border-gray-100 rounded-xl
                         text-gray-900 text-sm resize-none
                         transition-all duration-200
                         focus:outline-none focus:bg-white focus:border-brand-300 focus:ring-4 focus:ring-brand-100
                         placeholder:text-gray-400"
                            />
                            {errors.objectives && (
                                <p className="text-xs text-red-500">{errors.objectives.message}</p>
                            )}
                        </div>

                        {/* === CTA BUTTON === */}
                        <button
                            type="submit"
                            disabled={isSubmitting}
                            className="
                w-full h-14 mt-2
                bg-brand-600 hover:bg-brand-700
                text-white text-sm font-semibold tracking-wide uppercase
                rounded-2xl
                transition-all duration-300 ease-out
                hover:shadow-lg hover:shadow-brand-600/25 hover:-translate-y-0.5
                active:translate-y-0 active:shadow-md
                focus:outline-none focus:ring-4 focus:ring-brand-200
                disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:translate-y-0
              "
                        >
                            {isSubmitting ? (
                                <span className="flex items-center justify-center gap-2">
                                    <svg className="animate-spin h-4 w-4" viewBox="0 0 24 24" fill="none">
                                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
                                    </svg>
                                    En cours...
                                </span>
                            ) : (
                                "Réserver"
                            )}
                        </button>

                        {/* Trust Signals - Minimal */}
                        <div className="flex items-center justify-center gap-6 pt-2 text-gray-400">
                            <span className="flex items-center gap-1.5 text-[10px] tracking-wide">
                                <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                                    <path strokeLinecap="round" strokeLinejoin="round" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                                </svg>
                                Paiement sécurisé
                            </span>
                            <span className="flex items-center gap-1.5 text-[10px] tracking-wide">
                                <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                                    <path strokeLinecap="round" strokeLinejoin="round" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                                </svg>
                                Annulation gratuite
                            </span>
                        </div>
                    </form>
                </div>
            </div>

            {/* ========================================
          QUOTE MODAL - Minimal Overlay
          ======================================== */}
            {isQuoteOpen && (
                <div
                    className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-gray-900/60 backdrop-blur-sm"
                    onClick={() => setIsQuoteOpen(false)}
                >
                    <div
                        className="w-full max-w-md bg-white rounded-3xl shadow-2xl p-8 animate-modal-in"
                        onClick={(e) => e.stopPropagation()}
                    >
                        <div className="flex items-center justify-between mb-8">
                            <h3 className="text-xl font-semibold text-gray-900 tracking-tight">
                                Demande de devis
                            </h3>
                            <button
                                onClick={() => setIsQuoteOpen(false)}
                                className="w-10 h-10 flex items-center justify-center rounded-full text-gray-400 hover:bg-gray-100 hover:text-gray-600 transition-colors"
                            >
                                <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                                    <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
                                </svg>
                            </button>
                        </div>

                        <form className="space-y-4">
                            <input
                                type="email"
                                placeholder="Email"
                                className="w-full h-12 px-4 bg-gray-50 border border-gray-100 rounded-xl text-gray-900 placeholder:text-gray-400
                         focus:outline-none focus:border-brand-300 focus:ring-4 focus:ring-brand-100"
                            />
                            <input
                                type="tel"
                                placeholder="Téléphone"
                                className="w-full h-12 px-4 bg-gray-50 border border-gray-100 rounded-xl text-gray-900 placeholder:text-gray-400
                         focus:outline-none focus:border-brand-300 focus:ring-4 focus:ring-brand-100"
                            />
                            <textarea
                                rows={3}
                                placeholder="Votre message..."
                                className="w-full px-4 py-3 bg-gray-50 border border-gray-100 rounded-xl text-gray-900 placeholder:text-gray-400 resize-none
                         focus:outline-none focus:border-brand-300 focus:ring-4 focus:ring-brand-100"
                            />
                            <button
                                type="submit"
                                className="w-full h-12 bg-brand-600 hover:bg-brand-700 text-white font-medium rounded-xl
                         transition-all duration-200 hover:shadow-lg hover:shadow-brand-600/20"
                            >
                                Envoyer
                            </button>
                        </form>
                    </div>
                </div>
            )}
        </>
    );
}

