import { motion } from 'framer-motion';
import { FileText, Calendar, TrendingUp, Lightbulb, ArrowRight } from 'lucide-react';
import ScoreGauge from './ScoreGauge';
import KeywordList from './KeywordList';

const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1,
    },
  },
};

const itemVariants = {
  hidden: { opacity: 0, y: 20 },
  visible: {
    opacity: 1,
    y: 0,
    transition: {
      duration: 0.5,
      ease: [0.22, 1, 0.36, 1],
    },
  },
};

export default function ReportCard({ report, compact = false }) {
  if (!report) return null;

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
    });
  };

  if (compact) {
    return (
      <motion.div
        whileHover={{ scale: 1.02, y: -4 }}
        transition={{ duration: 0.2 }}
        className="card hover:shadow-xl transition-all duration-300 cursor-pointer"
      >
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <div className="p-3 bg-blue-100 rounded-lg">
              <FileText className="w-6 h-6 text-blue-600" />
            </div>
            <div>
              <p className="font-semibold text-slate-700">
                {report.resume_filename || 'Resume Analysis'}
              </p>
              <p className="text-sm text-slate-500 flex items-center space-x-1 mt-1">
                <Calendar className="w-3 h-3" />
                <span>{formatDate(report.created_at)}</span>
              </p>
            </div>
          </div>
          <div className="text-right">
            <ScoreGauge score={report.ats_score} label="ATS Score" size="small" />
          </div>
        </div>
      </motion.div>
    );
  }

  return (
    <motion.div
      variants={containerVariants}
      initial="hidden"
      animate="visible"
      className="space-y-6"
    >
      {/* Header with Scores */}
      <motion.div variants={itemVariants} className="card backdrop-blur-sm bg-white/90">
        <div className="flex items-center justify-between mb-6">
          <div>
            <motion.h1
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              className="text-3xl font-bold text-slate-800 mb-2"
            >
              Resume Analysis Report
            </motion.h1>
            {report.resume_filename && (
              <p className="text-slate-600 flex items-center space-x-2">
                <FileText className="w-4 h-4" />
                <span>{report.resume_filename}</span>
              </p>
            )}
          </div>
          {report.created_at && (
            <div className="text-right text-sm text-slate-500">
              <p className="flex items-center space-x-1">
                <Calendar className="w-4 h-4" />
                <span>{formatDate(report.created_at)}</span>
              </p>
            </div>
          )}
        </div>

        {/* Score Gauges */}
        <motion.div
          variants={itemVariants}
          className="grid grid-cols-1 md:grid-cols-2 gap-8 py-6 border-t border-slate-200"
        >
          <div className="flex justify-center">
            <ScoreGauge score={report.ats_score} label="ATS Score" />
          </div>
          <div className="flex justify-center">
            <ScoreGauge
              score={report.skill_match_percentage}
              label="Skill Match"
            />
          </div>
        </motion.div>
      </motion.div>

      {/* Summary */}
      {report.summary && (
        <motion.div
          variants={itemVariants}
          whileHover={{ scale: 1.01 }}
          className="card backdrop-blur-sm bg-white/90"
        >
          <h2 className="text-xl font-semibold text-slate-800 mb-4 flex items-center space-x-2">
            <motion.div
              animate={{ rotate: [0, 10, -10, 0] }}
              transition={{ duration: 2, repeat: Infinity, repeatDelay: 3 }}
            >
              <TrendingUp className="w-5 h-5 text-blue-600" />
            </motion.div>
            <span>Analysis Summary</span>
          </h2>
          <p className="text-slate-700 leading-relaxed">{report.summary}</p>
        </motion.div>
      )}

      {/* Keywords */}
      <motion.div
        variants={itemVariants}
        className="grid grid-cols-1 lg:grid-cols-2 gap-6"
      >
        <KeywordList
          keywords={report.matched_keywords}
          type="matched"
          title="Matched Keywords"
        />
        <KeywordList
          keywords={report.missing_keywords}
          type="missing"
          title="Missing Keywords"
        />
      </motion.div>

      {/* Recommendations */}
      {report.recommendations && report.recommendations.length > 0 && (
        <motion.div
          variants={itemVariants}
          whileHover={{ scale: 1.01 }}
          className="card backdrop-blur-sm bg-white/90"
        >
          <h2 className="text-xl font-semibold text-slate-800 mb-4 flex items-center space-x-2">
            <Lightbulb className="w-5 h-5 text-yellow-500" />
            <span>Recommendations</span>
          </h2>
          <motion.ul
            variants={containerVariants}
            initial="hidden"
            animate="visible"
            className="space-y-3"
          >
            {report.recommendations.map((recommendation, index) => (
              <motion.li
                key={index}
                variants={itemVariants}
                whileHover={{ x: 5 }}
                className="flex items-start space-x-3 p-4 bg-gradient-to-r from-blue-50 to-indigo-50 rounded-lg border border-blue-100 group"
              >
                <motion.span
                  whileHover={{ rotate: 360 }}
                  transition={{ duration: 0.5 }}
                  className="flex-shrink-0 w-7 h-7 bg-gradient-to-br from-blue-600 to-indigo-600 text-white rounded-full flex items-center justify-center text-sm font-semibold shadow-md"
                >
                  {index + 1}
                </motion.span>
                <p className="text-slate-700 flex-1">{recommendation}</p>
                <ArrowRight className="w-4 h-4 text-blue-600 opacity-0 group-hover:opacity-100 transition-opacity" />
              </motion.li>
            ))}
          </motion.ul>
        </motion.div>
      )}
    </motion.div>
  );
}
