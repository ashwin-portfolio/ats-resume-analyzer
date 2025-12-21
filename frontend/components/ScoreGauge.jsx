import { useEffect, useState } from 'react';
import { motion } from 'framer-motion';

export default function ScoreGauge({ score, label, size = 'large' }) {
  const [animatedScore, setAnimatedScore] = useState(0);

  useEffect(() => {
    const duration = 2000; // 2 seconds
    const steps = 60;
    const increment = score / steps;
    let current = 0;
    let step = 0;

    const timer = setInterval(() => {
      step++;
      current = Math.min(increment * step, score);
      setAnimatedScore(current);

      if (step >= steps) {
        clearInterval(timer);
        setAnimatedScore(score);
      }
    }, duration / steps);

    return () => clearInterval(timer);
  }, [score]);

  const getColor = (score) => {
    if (score >= 80) return 'text-green-600';
    if (score >= 65) return 'text-blue-600';
    if (score >= 50) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getBgColor = (score) => {
    if (score >= 80) return 'bg-green-100';
    if (score >= 65) return 'bg-blue-100';
    if (score >= 50) return 'bg-yellow-100';
    return 'bg-red-100';
  };

  const getRingColor = (score) => {
    if (score >= 80) return 'stroke-green-500';
    if (score >= 65) return 'stroke-blue-500';
    if (score >= 50) return 'stroke-yellow-500';
    return 'stroke-red-500';
  };

  const getGradient = (score) => {
    if (score >= 80) return 'from-green-500 to-emerald-500';
    if (score >= 65) return 'from-blue-500 to-indigo-500';
    if (score >= 50) return 'from-yellow-500 to-orange-500';
    return 'from-red-500 to-pink-500';
  };

  const isLarge = size === 'large';
  const radius = isLarge ? 60 : 40;
  const strokeWidth = isLarge ? 10 : 8;
  const fontSize = isLarge ? 'text-5xl' : 'text-3xl';
  const labelSize = isLarge ? 'text-xl' : 'text-base';
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (animatedScore / 100) * circumference;

  return (
    <motion.div
      initial={{ scale: 0, opacity: 0 }}
      animate={{ scale: 1, opacity: 1 }}
      transition={{
        type: "spring",
        stiffness: 200,
        damping: 20,
        delay: 0.2,
      }}
      className="flex flex-col items-center"
    >
      <div className="relative" style={{ width: radius * 2 + 30, height: radius * 2 + 30 }}>
        <svg
          className="transform -rotate-90"
          width={radius * 2 + 30}
          height={radius * 2 + 30}
        >
          {/* Background circle */}
          <circle
            cx={radius + 15}
            cy={radius + 15}
            r={radius}
            stroke="currentColor"
            strokeWidth={strokeWidth}
            fill="none"
            className="text-slate-200"
          />
          {/* Progress circle with gradient */}
          <defs>
            <linearGradient id={`gradient-${label}`} x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stopColor={score >= 80 ? '#10b981' : score >= 65 ? '#3b82f6' : score >= 50 ? '#f59e0b' : '#ef4444'} />
              <stop offset="100%" stopColor={score >= 80 ? '#059669' : score >= 65 ? '#2563eb' : score >= 50 ? '#d97706' : '#dc2626'} />
            </linearGradient>
          </defs>
          <motion.circle
            cx={radius + 15}
            cy={radius + 15}
            r={radius}
            stroke={`url(#gradient-${label})`}
            strokeWidth={strokeWidth}
            fill="none"
            strokeDasharray={circumference}
            strokeDashoffset={offset}
            strokeLinecap="round"
            initial={{ strokeDashoffset: circumference }}
            animate={{ strokeDashoffset: offset }}
            transition={{
              duration: 2,
              ease: [0.22, 1, 0.36, 1],
            }}
            style={{
              filter: 'drop-shadow(0 0 8px rgba(59, 130, 246, 0.5))',
            }}
          />
        </svg>
        {/* Score text */}
        <div className="absolute inset-0 flex items-center justify-center">
          <motion.div
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{
              type: "spring",
              stiffness: 200,
              damping: 15,
              delay: 0.5,
            }}
            className="text-center"
          >
            <motion.p
              key={Math.round(animatedScore)}
              initial={{ scale: 1.5, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              transition={{ duration: 0.3 }}
              className={`font-bold ${getColor(score)} ${fontSize}`}
            >
              {Math.round(animatedScore)}
            </motion.p>
            <p className="text-slate-500 text-xs">/100</p>
          </motion.div>
        </div>
        {/* Pulsing ring effect */}
        {animatedScore >= 80 && (
          <motion.div
            className={`absolute inset-0 rounded-full border-4 ${getRingColor(score)}`}
            animate={{
              scale: [1, 1.1, 1],
              opacity: [0.5, 0, 0.5],
            }}
            transition={{
              duration: 2,
              repeat: Infinity,
              ease: "easeInOut",
            }}
            style={{
              width: radius * 2 + 30,
              height: radius * 2 + 30,
            }}
          />
        )}
      </div>
      {/* Label */}
      <motion.p
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.8 }}
        className={`mt-4 font-semibold ${getColor(score)} ${labelSize}`}
      >
        {label}
      </motion.p>
    </motion.div>
  );
}
