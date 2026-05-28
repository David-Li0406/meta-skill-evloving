import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({
  subsets: ["latin"],
  weight: ["300", "400", "500", "600", "700", "800"],
  variable: "--font-inter",
});


export const metadata = {
  title: "Master Microservices | Complete Learning Platform",
  description: "Learn microservices architecture from scratch. Master NestJS, Docker, Kubernetes, and production deployment with hands-on tutorials.",
  keywords: "microservices, nestjs, nodejs, docker, kubernetes, api gateway, distributed systems",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en" className={inter.variable}>
      <body className="antialiased bg-grid" style={{ fontFamily: "var(--font-inter), 'Inter', sans-serif" }}>
        <div className="noise-overlay"></div>
        {children}
      </body>
    </html>
  );
}
