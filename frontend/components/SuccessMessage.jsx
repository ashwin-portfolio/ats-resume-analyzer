import { motion, AnimatePresence } from 'framer-motion';
import { CheckCircle2, X } from 'lucide-react';

export default function SuccessMessage({ message, onDismiss, className = '', autoDismiss = false, duration = 5000 }) {
  if (!message) return null;

  // Auto-dismiss functionality
  if (autoDismiss && onDismiss) {
    setTimeout(() => {
      onDismiss();
    }, duration);
  }

  return (
    <AnimatePresence>
      <motion.div
        initial={{ opacity: 0, y: -10, scale: 0.95 }}
        animate={{ opacity: 1, y: 0, scale: 1 }}
        exit={{ opacity: 0, y: -10, scale: 0.95 }}
        transition={{ duration: 0.2 }}
        className={`bg-green-50 border border-green-200 rounded-lg p-4 flex items-start space-x-3 ${className}`}
      >
        <CheckCircle2 className="w-5 h-5 text-green-600 flex-shrink-0 mt-0.5" />
        <div className="flex-1 min-w-0">
          <p className="text-sm font-medium text-green-800">Success</p>
          <p className="text-sm text-green-700 mt-1 break-words">{message}</p>
        </div>
        {onDismiss && (
          <button
            onClick={onDismiss}
            className="text-green-600 hover:text-green-800 flex-shrink-0 transition-colors"
            aria-label="Dismiss message"
          >
            <X className="w-4 h-4" />
          </button>
        )}
      </motion.div>
    </AnimatePresence>
  );
}


