'use client';

import Link from 'next/link';
import { useProgress } from '@/hooks/useProgress';

// Lightweight path card that shows per-path progress based on completed modules
export default function LearningPathCard({ path }) {
  const { isCompleted } = useProgress();

  const modulesList = path.modules || [];
  const total = modulesList.length;
  let completedCount = 0;
  modulesList.forEach((slug) => {
    if (isCompleted(slug)) completedCount++;
  });
  const pct = total ? Math.round((completedCount / total) * 100) : 0;

  const firstIncomplete = modulesList.find((slug) => !isCompleted(slug));
  const href = firstIncomplete ? `/course/${firstIncomplete}` : (modulesList[0] ? `/course/${modulesList[0]}` : '#');

  
  const barStyle = {
    width: `${pct}%`,
    height: '8px',
    borderRadius: '999px',
    background: 'linear-gradient(90deg, #34d399, #10b981)'
  };

  return (
    <div className="card group w-full">
      <div className="flex items-center justify-between mb-2">
        <h3 className="text-lg font-semibold text-white">{path.name}</h3>
        <span className="badge badge-intermediate">{path.id}</span>
      </div>
      <p className="text-slate-400 mb-4">{path.description}</p>
      {/* Focus areas */}
      {(path.focuses && path.focuses.length > 0) && (
        <div className="flex flex-wrap gap-2 mb-3">
          {path.focuses.map((f, idx) => (
            <span key={idx} className="text-xs px-2 py-1 rounded-full bg-slate-800/60 text-slate-200 border border-slate-700/50">{f}</span>
          ))}
        </div>
      )}
      <div className="w-full bg-slate-800 rounded-full mb-3">
        <div style={barStyle} aria-valuenow={pct} aria-valuemin={0} aria-valuemax={100}></div>
      </div>
      <div className="flex items-center justify-between">
        <span className="text-sm text-slate-200">{completedCount}/{total} modules complete</span>
        <Link href={href} className="btn-primary text-sm px-3 py-2 inline-flex items-center gap-2">
          <span>Start Path</span>
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 12h14" />
          </svg>
        </Link>
      </div>
    </div>
  );
}
