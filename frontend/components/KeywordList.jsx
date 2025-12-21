import { motion } from 'framer-motion';
import { CheckCircle2, XCircle, Tag } from 'lucide-react';

const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.05,
    },
  },
};

const itemVariants = {
  hidden: { opacity: 0, scale: 0.8, y: 20 },
  visible: {
    opacity: 1,
    scale: 1,
    y: 0,
    transition: {
      type: "spring",
      stiffness: 200,
      damping: 15,
    },
  },
};

export default function KeywordList({ keywords, type, title }) {
  if (!keywords || keywords.length === 0) {
    return (
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="card"
      >
        <h3 className="text-lg font-semibold text-slate-700 mb-4 flex items-center space-x-2">
          {type === 'matched' ? (
            <CheckCircle2 className="w-5 h-5 text-green-600" />
          ) : (
            <XCircle className="w-5 h-5 text-red-600" />
          )}
          <span>{title}</span>
        </h3>
        <p className="text-slate-500 text-sm">
          {type === 'matched'
            ? 'No matched keywords found.'
            : 'No missing keywords.'}
        </p>
      </motion.div>
    );
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="card"
    >
      <h3 className="text-lg font-semibold text-slate-700 mb-4 flex items-center space-x-2">
        {type === 'matched' ? (
          <motion.div
            animate={{ rotate: [0, 10, -10, 0] }}
            transition={{ duration: 0.5, delay: 0.2 }}
          >
            <CheckCircle2 className="w-5 h-5 text-green-600" />
          </motion.div>
        ) : (
          <XCircle className="w-5 h-5 text-red-600" />
        )}
        <span>{title}</span>
        <motion.span
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          transition={{ type: "spring", delay: 0.3 }}
          className="text-sm font-normal text-slate-500 bg-slate-100 px-2 py-0.5 rounded-full"
        >
          {keywords.length}
        </motion.span>
      </h3>
      <motion.div
        variants={containerVariants}
        initial="hidden"
        animate="visible"
        className="flex flex-wrap gap-2"
      >
        {keywords.map((keyword, index) => (
          <motion.span
            key={index}
            variants={itemVariants}
            whileHover={{ scale: 1.1, y: -2 }}
            whileTap={{ scale: 0.95 }}
            className={`
              inline-flex items-center space-x-1 px-3 py-1.5 rounded-lg text-sm font-medium
              transition-all duration-200 cursor-pointer
              ${
                type === 'matched'
                  ? 'bg-gradient-to-r from-green-100 to-emerald-100 text-green-700 border border-green-200 shadow-sm hover:shadow-md'
                  : 'bg-gradient-to-r from-red-100 to-pink-100 text-red-700 border border-red-200 shadow-sm hover:shadow-md'
              }
            `}
          >
            <Tag className="w-3 h-3" />
            <span>{keyword}</span>
          </motion.span>
        ))}
      </motion.div>
    </motion.div>
  );
}
