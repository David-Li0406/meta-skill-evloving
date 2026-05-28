import type { ReactNode } from "react";
import { DesktopTopNav } from "@/components/layout/DesktopTopNav";
import { MobileBottomNav } from "@/components/layout/MobileBottomNav";

export default function AuthLayout({ children }: { children: ReactNode }) {
    return (
        <div className="min-h-screen flex flex-col bg-gradient-to-br from-slate-50 via-white to-slate-100">
            {/* Navbar - Visible on all pages */}
            <DesktopTopNav />
            <MobileBottomNav />

            {/* Main Content */}
            <main className="flex-1 relative overflow-hidden">
                {/* Mesh Gradient Background */}
                <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] rounded-full bg-indigo-100/40 blur-[120px] pointer-events-none" />
                <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] rounded-full bg-teal-100/40 blur-[120px] pointer-events-none" />

                <div className="relative z-10 w-full h-full">
                    {children}
                </div>
            </main>
        </div>
    );
}
