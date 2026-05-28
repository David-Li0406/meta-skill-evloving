"use client";

import { useState, useEffect } from "react";
import BookingWidget from "@/components/ui/BookingWidget";

export default function MobileBookingDrawer() {
    const [isOpen, setIsOpen] = useState(false);
    const [isMounted, setIsMounted] = useState(false);

    useEffect(() => {
        setIsMounted(true);
    }, []);

    if (!isMounted) return null;

    return (
        <>
            {/* === FLOATING CTA BUTTON (Mobile Only) === */}
            <div className="fixed bottom-6 left-4 right-4 z-40 lg:hidden">
                <button
                    onClick={() => setIsOpen(true)}
                    className="w-full h-14 bg-brand-600 text-white text-sm font-semibold tracking-wide uppercase rounded-2xl shadow-xl shadow-brand-600/30 flex items-center justify-center gap-2 transition-transform active:scale-95"
                >
                    <span>Réserver maintenant</span>
                    <svg
                        className="w-5 h-5"
                        fill="none"
                        viewBox="0 0 24 24"
                        stroke="currentColor"
                        strokeWidth={2}
                    >
                        <path
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"
                        />
                    </svg>
                </button>
            </div>

            {/* === DRAWER OVERLAY === */}
            {isOpen && (
                <div
                    className="fixed inset-0 z-50 bg-gray-900/60 backdrop-blur-sm lg:hidden transition-opacity"
                    onClick={() => setIsOpen(false)}
                />
            )}

            {/* === DRAWER CONTENT === */}
            <div
                className={`
          fixed inset-x-0 bottom-0 z-50 w-full bg-white rounded-t-3xl shadow-2xl lg:hidden
          transform transition-transform duration-300 ease-out
          ${isOpen ? "translate-y-0" : "translate-y-full"}
        `}
                style={{ maxHeight: "90vh" }}
            >
                {/* Handle Bar */}
                <div
                    className="w-full flex justify-center pt-3 pb-1 cursor-pointer"
                    onClick={() => setIsOpen(false)}
                >
                    <div className="w-12 h-1.5 bg-gray-200 rounded-full" />
                </div>

                {/* Header */}
                <div className="px-6 pb-4 border-b border-gray-100 flex justify-between items-center">
                    <h3 className="text-lg font-semibold text-gray-900">Réservation</h3>
                    <button
                        onClick={() => setIsOpen(false)}
                        className="p-2 bg-gray-50 rounded-full text-gray-400 hover:text-gray-600"
                    >
                        <svg
                            className="w-5 h-5"
                            fill="none"
                            viewBox="0 0 24 24"
                            stroke="currentColor"
                            strokeWidth={2}
                        >
                            <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
                        </svg>
                    </button>
                </div>

                {/* Scrollable Content */}
                <div className="overflow-y-auto p-4 pb-24" style={{ maxHeight: "calc(90vh - 80px)" }}>
                    <BookingWidget />
                </div>
            </div>
        </>
    );
}
