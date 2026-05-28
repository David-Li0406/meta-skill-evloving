/**
 * NotificationItem Component
 * 
 * A single notification row with read/unread state.
 * Uses motion for slide-in animation.
 */
import { motion } from 'motion/react';
import { Check } from 'lucide-react';

export default function NotificationItem({ 
  title, 
  description, 
  time, 
  read = false, 
  onMarkRead 
}) {
  return (
    <motion.div
      initial={{ opacity: 0, x: -20 }}
      animate={{ opacity: 1, x: 0 }}
      className={`p-4 border-b hover:bg-gray-50 cursor-pointer transition-colors
                  ${read ? 'opacity-60' : ''}`}
    >
      <div className="flex justify-between items-start">
        <div className="flex-1">
          <div className="flex items-center gap-2">
            {!read && (
              <span className="w-2 h-2 bg-blue-500 rounded-full" />
            )}
            <span className={`font-medium ${read ? 'text-gray-600' : 'text-gray-900'}`}>
              {title}
            </span>
          </div>
          <p className="text-sm text-gray-500 mt-1">{description}</p>
          <span className="text-xs text-gray-400 mt-2 block">{time}</span>
        </div>
        {!read && onMarkRead && (
          <button
            onClick={(e) => { e.stopPropagation(); onMarkRead(); }}
            className="p-1 hover:bg-gray-200 rounded text-gray-400 hover:text-gray-600"
            title="Mark as read"
          >
            <Check className="w-4 h-4" />
          </button>
        )}
      </div>
    </motion.div>
  );
}
