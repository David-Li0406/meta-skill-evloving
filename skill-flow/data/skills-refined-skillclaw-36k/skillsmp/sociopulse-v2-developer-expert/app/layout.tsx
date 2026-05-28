import type { Metadata, Viewport } from "next";
import { Outfit } from "next/font/google";
import "./globals.css";
import { SonnerToaster } from "@/components/ui/SonnerToaster";
import { SocketProvider } from "@/components/providers";
import { ThemeProvider } from "@/components/providers/ThemeProvider";
import { currentBrand } from "@/lib/brand";

const outfit = Outfit({ subsets: ["latin"] });

export const metadata: Metadata = {
    title: currentBrand.metaTitle,
    description: currentBrand.metaDescription,
    keywords: ["médico-social", "EHPAD", currentBrand.appName, "renforts", "ateliers", "professionnels de santé"],
};

export const viewport: Viewport = {
    width: "device-width",
    initialScale: 1,
    maximumScale: 1,
    userScalable: false,
    viewportFit: "cover",
};

import { MobileNav } from "@/components/layout/MobileNav";

// ... imports

export default function RootLayout({
    children,
}: {
    children: React.ReactNode;
}) {
    // Determine initial theme from brand (SSR-safe)
    const initialTheme = currentBrand.mode === 'MEDICAL' ? 'medical' : 'social';

    return (
        <html lang="fr" className="smooth-scroll" data-theme={initialTheme}>
            <body className={`${outfit.className} pb-20 md:pb-0`}>
                <ThemeProvider>
                    <SocketProvider>
                        {children}
                    </SocketProvider>
                </ThemeProvider>
                <MobileNav />
                <SonnerToaster />
            </body>
        </html>
    );
}
