export interface VideoLayoutProps {
    children: React.ReactNode;
}

export function VideoLayout({ children }: VideoLayoutProps) {
    return (
        <div className="fixed inset-0 bg-slate-950 flex flex-col overflow-hidden">
            {children}
        </div>
    );
}
