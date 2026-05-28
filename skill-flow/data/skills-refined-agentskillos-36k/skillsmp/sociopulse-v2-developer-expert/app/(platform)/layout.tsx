import type { ReactNode } from "react";
import Link from "next/link";
import { DesktopTopNav, MobileBottomNav } from "@/components/layout";

function PlatformFooter() {
    return (
        <footer className="bg-white border-t border-slate-200">
            <div className="max-w-7xl mx-auto px-6 py-6 flex justify-center">
                <div className="flex flex-wrap gap-6 text-sm text-slate-600">
                    <Link href="/fil-pro" className="hover:text-slate-900 transition-colors">Fil Pro</Link>
                    <Link href="/dashboard" className="hover:text-slate-900 transition-colors">Tableau de bord</Link>
                    <Link href="/bookings" className="hover:text-slate-900 transition-colors">Agenda</Link>
                    <Link href="/messages" className="hover:text-slate-900 transition-colors">Messages</Link>
                    <Link href="/settings" className="hover:text-slate-900 transition-colors">Paramètres</Link>
                </div>
            </div>
        </footer>
    );
}

export default function PlatformLayout({ children }: { children: ReactNode }) {
    // Note: SocketProvider is already in root layout, no need to duplicate
    return (
        <div className="min-h-screen bg-canvas flex flex-col">
            <DesktopTopNav />
            <div className="flex-1 flex flex-col has-bottom-nav lg:pb-0">
                <main className="flex-1">{children}</main>
                <PlatformFooter />
            </div>
            <MobileBottomNav />
        </div>
    );
}
