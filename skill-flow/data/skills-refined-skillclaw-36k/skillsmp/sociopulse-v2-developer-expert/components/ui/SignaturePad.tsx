'use client';

import { useRef, useState } from 'react';
import SignatureCanvas from 'react-signature-canvas';

interface SignaturePadProps {
    onSave: (dataUrl: string) => void;
    height?: number;
}

export function SignaturePad({ onSave, height = 220 }: SignaturePadProps) {
    const sigCanvas = useRef<SignatureCanvas | null>(null);
    const [isEmpty, setIsEmpty] = useState(true);

    const handleClear = () => {
        sigCanvas.current?.clear();
        setIsEmpty(true);
    };

    const handleSave = () => {
        if (!sigCanvas.current || sigCanvas.current.isEmpty()) {
            return;
        }
        const dataUrl = sigCanvas.current.toDataURL('image/png');
        onSave(dataUrl);
    };

    return (
        <div className="space-y-3">
            <div className="rounded-lg border border-slate-200 bg-white shadow-sm">
                <SignatureCanvas
                    ref={(ref) => {
                        sigCanvas.current = ref;
                    }}
                    penColor="#111827"
                    backgroundColor="#ffffff"
                    canvasProps={{
                        className: 'w-full rounded-lg',
                        style: { height },
                    }}
                    onEnd={() => setIsEmpty(false)}
                />
            </div>
            <div className="flex items-center justify-between gap-2">
                <button
                    type="button"
                    onClick={handleClear}
                    className="px-3 py-2 rounded-lg text-sm font-semibold text-slate-600 bg-slate-100 hover:bg-slate-200 transition-colors"
                >
                    Effacer
                </button>
                <button
                    type="button"
                    onClick={handleSave}
                    disabled={isEmpty}
                    className={`px-4 py-2 rounded-lg text-sm font-semibold text-white transition-colors ${
                        isEmpty ? 'bg-slate-400 cursor-not-allowed' : 'bg-emerald-600 hover:bg-emerald-700'
                    }`}
                >
                    Valider
                </button>
            </div>
        </div>
    );
}
