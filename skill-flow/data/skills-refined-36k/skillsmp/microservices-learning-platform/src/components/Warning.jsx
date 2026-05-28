'use client';

import Link from 'next/link';

/**
 * Warning - A warning/callout component for important notices
 * Supports different severity levels with distinct visual styling
 * 
 * @param {Object} props
 * @param {string} props.type - 'warning' | 'danger' | 'info' | 'success'
 * @param {string} props.title - Optional title for the warning
 * @param {React.ReactNode} props.children - Warning content
 */
export default function Warning({ 
  type = 'warning', 
  title, 
  children 
}) {
  const styles = {
    warning: {
      container: 'bg-yellow-500/10 border-yellow-500/50',
      icon: 'text-yellow-500',
      title: 'text-yellow-400',
      iconPath: 'M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z'
    },
    danger: {
      container: 'bg-red-500/10 border-red-500/50',
      icon: 'text-red-500',
      title: 'text-red-400',
      iconPath: 'M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z'
    },
    info: {
      container: 'bg-blue-500/10 border-blue-500/50',
      icon: 'text-blue-500',
      title: 'text-blue-400',
      iconPath: 'M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z'
    },
    success: {
      container: 'bg-green-500/10 border-green-500/50',
      icon: 'text-green-500',
      title: 'text-green-400',
      iconPath: 'M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z'
    }
  };

  const currentStyle = styles[type] || styles.warning;

  return (
    <div className={`rounded-xl border p-4 my-6 ${currentStyle.container}`}>
      <div className="flex items-start gap-3">
        {/* Icon */}
        <div className={`shrink-0 ${currentStyle.icon}`}>
          <svg 
            className="w-6 h-6" 
            fill="none" 
            stroke="currentColor" 
            viewBox="0 0 24 24"
          >
            <path 
              strokeLinecap="round" 
              strokeLinejoin="round" 
              strokeWidth={2} 
              d={currentStyle.iconPath} 
            />
          </svg>
        </div>
        
        {/* Content */}
        <div className="flex-1">
          {title && (
            <h4 className={`font-semibold mb-1 ${currentStyle.title}`}>
              {title}
            </h4>
          )}
          <div className="text-slate-300 text-sm leading-relaxed">
            {children}
          </div>
        </div>
      </div>
    </div>
  );
}

/**
 * Pre-built warning variants for common use cases
 */
export function DangerWarning({ title = "⚠️ Critical Warning", children }) {
  return <Warning type="danger" title={title}>{children}</Warning>;
}

export function InfoNote({ title = "💡 Note", children }) {
  return <Warning type="info" title={title}>{children}</Warning>;
}

export function SuccessTip({ title = "✅ Best Practice", children }) {
  return <Warning type="success" title={title}>{children}</Warning>;
}

// Cost warning specifically for microservices content
export function CostWarning({ children }) {
  return (
    <Warning type="danger" title="💰 Hidden Cost Warning">
      {children || (
        <>
          This approach adds significant operational complexity. Make sure you have 
          exhausted simpler solutions first. See{' '}
          <Link href="/course/should-you-use-microservices" className="text-red-400 underline hover:text-red-300">
            Module 0: Should You Use Microservices?
          </Link>
        </>
      )}
    </Warning>
  );
}

// Complexity warning for advanced patterns
export function ComplexityWarning({ pattern }) {
  return (
    <Warning type="warning" title="🔧 Complexity Alert">
      <strong>{pattern}</strong> is an advanced pattern that adds significant complexity. 
      Only use it when simpler solutions are insufficient. Most teams never need this.
    </Warning>
  );
}
