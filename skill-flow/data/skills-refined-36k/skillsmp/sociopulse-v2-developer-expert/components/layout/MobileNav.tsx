"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { Home, Calendar, MessageCircle, User, BellRing } from "lucide-react";
import { isMedical } from "@/lib/brand";
import { useAuth } from "@/lib/useAuth";

export function MobileNav() {
    const pathname = usePathname();
    const medical = isMedical();
    const { isAuthenticated } = useAuth();

    // Brand-specific colors - matching DesktopTopNav SOS button
    const activeColor = medical ? "text-rose-500" : "text-teal-500";
    const activeBg = medical ? "bg-rose-50" : "bg-teal-50";
    const sosBg = "bg-gradient-to-r from-rose-500 via-rose-500 to-pink-500";
    const sosShadow = "shadow-rose-500/25";

    const navItems = [
        { label: "Accueil", href: "/wall", icon: Home },
        { label: "Agenda", href: "/schedule", icon: Calendar, requiresAuth: true },
        { label: "SOS", href: "/create-mission", icon: BellRing, isSos: true, requiresAuth: true },
        { label: "Messages", href: "/messages", icon: MessageCircle, requiresAuth: true },
        { label: "Profil", href: "/menu", icon: User, requiresAuth: true },
    ];

    // Determine link destination - redirect to login if auth required but not authenticated
    const getHref = (item: typeof navItems[0]) => {
        if (item.requiresAuth && !isAuthenticated) {
            return "/auth/login";
        }
        return item.href;
    };

    return (
        <div className="md:hidden fixed bottom-0 left-0 right-0 z-50 bg-white/95 backdrop-blur-xl border-t border-slate-200/80 safe-area-pb">
            <nav className="h-[68px] max-w-md mx-auto px-2 flex justify-around items-end relative">
                {navItems.map((item) => {
                    if (item.isSos) {
                        return (
                            <div key={item.label} className="relative -top-3 flex flex-col items-center">
                                <Link
                                    href={getHref(item)}
                                    className={`
                                        flex items-center justify-center gap-2 px-5 py-3 rounded-full 
                                        ${sosBg} text-white shadow-xl ${sosShadow}
                                        transform transition-all duration-200 active:scale-95 hover:shadow-2xl
                                        ring-4 ring-white
                                    `}
                                    aria-label="SOS Renfort"
                                >
                                    <BellRing className="w-5 h-5" />
                                    <span className="font-bold text-sm tracking-wide">SOS</span>
                                </Link>
                            </div>
                        );
                    }

                    const isActive = pathname === item.href || pathname?.startsWith(item.href + "/");

                    return (
                        <Link
                            key={item.label}
                            href={getHref(item)}
                            className={`
                                flex flex-col items-center justify-center py-2 px-3 rounded-xl
                                transition-all duration-200 min-w-[60px]
                                ${isActive ? `${activeColor} ${activeBg}` : "text-slate-500 hover:text-slate-700"}
                            `}
                        >
                            <item.icon
                                className={`w-5 h-5 mb-0.5 ${isActive ? "stroke-[2.5]" : "stroke-[1.8]"}`}
                            />
                            <span className={`text-[10px] font-medium ${isActive ? "font-semibold" : ""}`}>
                                {item.label}
                            </span>
                        </Link>
                    );
                })}
            </nav>
        </div>
    );
}
