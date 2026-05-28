/**
 * NotificationBell Component
 * 
 * A bell icon with unread count badge.
 * Uses lucide-react for the icon and motion for animations.
 */
import { Bell } from 'lucide-react';
import { motion, AnimatePresence } from 'motion/react';

export default function NotificationBell({ count = 0, onClick }) {
  return (
    <button 
      onClick={onClick}
      className="relative p-2 hover:bg-gray-100 rounded-full transition-colors"
    >
      <Bell className="w-6 h-6 text-gray-600" />
      <AnimatePresence>
        {count > 0 && (
          <motion.span
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            exit={{ scale: 0 }}
            className="absolute -top-1 -right-1 bg-red-500 text-white text-xs 
                       rounded-full min-w-[20px] h-5 flex items-center justify-center 
                       px-1 font-medium"
          >
            {count > 99 ? '99+' : count}
          </motion.span>
        )}
      </AnimatePresence>
    </button>
  );
}
