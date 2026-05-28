/**
 * ThemeToggle Component
 * 
 * An animated toggle switch for dark/light mode.
 * Uses motion for smooth transitions and lucide-react for icons.
 */
import { motion } from 'motion/react';
import { Sun, Moon } from 'lucide-react';

export default function ThemeToggle({ dark, onToggle }) {
  return (
    <button
      onClick={onToggle}
      className={`relative w-16 h-9 rounded-full transition-colors ${
        dark ? 'bg-indigo-600' : 'bg-amber-400'
      }`}
      aria-label={dark ? 'Switch to light mode' : 'Switch to dark mode'}
    >
      <motion.span
        layout
        transition={{ type: 'spring', stiffness: 500, damping: 30 }}
        className={`absolute top-1 w-7 h-7 bg-white rounded-full shadow-md 
                    flex items-center justify-center ${
                      dark ? 'left-8' : 'left-1'
                    }`}
      >
        {dark ? (
          <Moon className="w-4 h-4 text-indigo-600" />
        ) : (
          <Sun className="w-4 h-4 text-amber-500" />
        )}
      </motion.span>
    </button>
  );
}
