import { useState } from 'react';
import { useRouter } from 'next/router';
import { motion } from 'framer-motion';
import { Loader2, Sparkles, CheckCircle2, Zap, Target, TrendingUp, ArrowRight } from 'lucide-react';
import FileUpload from '../components/FileUpload';
import ErrorMessage from '../components/ErrorMessage';
import SuccessMessage from '../components/SuccessMessage';
import { analyzeResume } from '../lib/api';

const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1,
      delayChildren: 0.2,
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

const floatingVariants = {
  animate: {
    y: [0, -10, 0],
    transition: {
      duration: 3,
      repeat: Infinity,
      ease: "easeInOut",
    },
  },
};

export default function Home() {
  const router = useRouter();
  const [resumeFile, setResumeFile] = useState(null);
  const [jobDescription, setJobDescription] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [fileError, setFileError] = useState(null);
  const [success, setSuccess] = useState(null);

  const handleFileSelect = (file, error) => {
    setResumeFile(file);
    setFileError(error);
    if (error) {
      setError(error);
    } else {
      setError(null);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);

    // Validation
    if (!resumeFile) {
      setError('Please upload a resume file');
      return;
    }

    if (!jobDescription.trim()) {
      setError('Please enter a job description');
      return;
    }

    if (jobDescription.trim().length < 10) {
      setError('Job description must be at least 10 characters long');
      return;
    }

    setLoading(true);
    setError(null);
    setSuccess(null);
    try {
      const result = await analyzeResume(resumeFile, jobDescription);
      
      // Show success message briefly before redirect
      setSuccess('Resume analyzed successfully! Redirecting to report...');
      
      // Redirect to report page after a brief delay
      setTimeout(() => {
        router.push(`/report/${result.report_id}`);
      }, 1000);
    } catch (err) {
      console.error('Analysis error:', err);
      // Use userMessage from API interceptor if available
      setError(err.userMessage || err.response?.data?.detail || err.message || 'Failed to analyze resume. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col relative overflow-hidden">
      {/* Animated Background Elements */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <motion.div
          className="absolute top-20 left-10 w-72 h-72 bg-blue-400 rounded-full mix-blend-multiply filter blur-3xl opacity-20"
          animate={{
            x: [0, 100, 0],
            y: [0, 50, 0],
          }}
          transition={{
            duration: 20,
            repeat: Infinity,
            ease: "easeInOut",
          }}
        />
        <motion.div
          className="absolute top-40 right-10 w-72 h-72 bg-purple-400 rounded-full mix-blend-multiply filter blur-3xl opacity-20"
          animate={{
            x: [0, -100, 0],
            y: [0, -50, 0],
          }}
          transition={{
            duration: 25,
            repeat: Infinity,
            ease: "easeInOut",
          }}
        />
        <motion.div
          className="absolute bottom-20 left-1/2 w-72 h-72 bg-indigo-400 rounded-full mix-blend-multiply filter blur-3xl opacity-20"
          animate={{
            x: [0, 50, 0],
            y: [0, -100, 0],
          }}
          transition={{
            duration: 30,
            repeat: Infinity,
            ease: "easeInOut",
          }}
        />
      </div>

      {/* Header */}
      <motion.header
        initial={{ y: -100, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ duration: 0.6, ease: [0.22, 1, 0.36, 1] }}
        className="relative bg-white/80 backdrop-blur-md shadow-sm border-b border-slate-200/50"
      >
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center space-x-3">
            <motion.div
              whileHover={{ scale: 1.1, rotate: 5 }}
              whileTap={{ scale: 0.95 }}
              className="p-2 bg-gradient-to-br from-blue-600 to-indigo-600 rounded-lg shadow-lg"
            >
              <Sparkles className="w-6 h-6 text-white" />
            </motion.div>
            <div>
              <h1 className="text-xl font-bold gradient-text">
                ATS Resume Analyzer
              </h1>
              <p className="text-xs text-slate-500">
                AI-Powered Resume Analysis
              </p>
            </div>
          </div>
        </div>
      </motion.header>

      {/* Main Content */}
      <main className="flex-1 max-w-4xl mx-auto w-full px-4 sm:px-6 lg:px-8 py-12 relative z-10">
        <motion.div
          variants={containerVariants}
          initial="hidden"
          animate="visible"
          className="space-y-8"
        >
          {/* Hero Section */}
          <motion.div variants={itemVariants} className="text-center mb-12">
            <motion.div
              variants={floatingVariants}
              animate="animate"
              className="inline-block mb-6"
            >
              <div className="relative">
                <div className="absolute inset-0 bg-gradient-to-r from-blue-600 to-indigo-600 rounded-2xl blur-xl opacity-30"></div>
                <h2 className="relative text-5xl md:text-6xl font-bold text-slate-800 mb-6">
                  Optimize Your Resume
                  <br />
                  <span className="gradient-text">for ATS Systems</span>
                </h2>
              </div>
            </motion.div>
            <motion.p
              variants={itemVariants}
              className="text-xl text-slate-600 max-w-2xl mx-auto leading-relaxed"
            >
              Upload your resume and job description to get instant AI-powered
              analysis, keyword matching, and actionable recommendations.
            </motion.p>
          </motion.div>

          {/* Upload Form */}
          <motion.form
            variants={itemVariants}
            onSubmit={handleSubmit}
            className="space-y-6"
          >
            {/* File Upload */}
            <motion.div
              whileHover={{ scale: 1.01 }}
              transition={{ duration: 0.2 }}
              className="card backdrop-blur-sm bg-white/90"
            >
              <label className="block text-sm font-semibold text-slate-700 mb-3">
                Upload Resume
              </label>
              <FileUpload
                onFileSelect={handleFileSelect}
                selectedFile={resumeFile}
                error={fileError}
              />
            </motion.div>

            {/* Job Description */}
            <motion.div
              whileHover={{ scale: 1.01 }}
              transition={{ duration: 0.2 }}
              className="card backdrop-blur-sm bg-white/90"
            >
              <label
                htmlFor="job-description"
                className="block text-sm font-semibold text-slate-700 mb-3"
              >
                Job Description
              </label>
              <textarea
                id="job-description"
                value={jobDescription}
                onChange={(e) => setJobDescription(e.target.value)}
                placeholder="Paste the job description here..."
                rows={8}
                className="input-field resize-none"
                disabled={loading}
              />
              <p className="text-xs text-slate-500 mt-2">
                {jobDescription.length} characters
              </p>
            </motion.div>

            {/* Success Message */}
            {success && (
              <SuccessMessage 
                message={success} 
                onDismiss={() => setSuccess(null)}
                autoDismiss={true}
              />
            )}

            {/* Error Message */}
            <ErrorMessage 
              error={error || fileError} 
              onDismiss={() => {
                setError(null);
                setFileError(null);
              }}
            />

            {/* Submit Button */}
            <motion.button
              type="submit"
              disabled={loading || !resumeFile || !jobDescription.trim()}
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              className="btn-primary w-full text-lg py-4 flex items-center justify-center space-x-2 relative overflow-hidden group"
            >
              <span className="absolute inset-0 bg-gradient-to-r from-blue-700 to-indigo-700 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></span>
              <span className="relative flex items-center space-x-2">
                {loading ? (
                  <>
                    <Loader2 className="w-5 h-5 animate-spin" />
                    <span>Analyzing Resume...</span>
                  </>
                ) : (
                  <>
                    <Sparkles className="w-5 h-5" />
                    <span>Analyze Resume</span>
                    <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
                  </>
                )}
              </span>
            </motion.button>
          </motion.form>

          {/* Features */}
          <motion.div
            variants={itemVariants}
            className="mt-16 grid grid-cols-1 md:grid-cols-3 gap-6"
          >
            {[
              {
                icon: Zap,
                title: 'AI-Powered Analysis',
                description: 'Advanced ML models analyze semantic similarity and keyword matching',
                color: 'blue',
              },
              {
                icon: Target,
                title: 'Instant Results',
                description: 'Get comprehensive ATS scores and recommendations in seconds',
                color: 'green',
              },
              {
                icon: TrendingUp,
                title: 'Actionable Insights',
                description: 'Receive specific recommendations to improve your resume',
                color: 'purple',
              },
            ].map((feature, index) => (
              <motion.div
                key={index}
                whileHover={{ y: -8, scale: 1.02 }}
                transition={{ duration: 0.2 }}
                className="card text-center group cursor-pointer"
              >
                <motion.div
                  whileHover={{ rotate: 360 }}
                  transition={{ duration: 0.6 }}
                  className={`p-3 bg-${feature.color}-100 rounded-lg w-fit mx-auto mb-4 group-hover:bg-${feature.color}-200 transition-colors`}
                >
                  <feature.icon className={`w-6 h-6 text-${feature.color}-600`} />
                </motion.div>
                <h3 className="font-semibold text-slate-800 mb-2">
                  {feature.title}
                </h3>
                <p className="text-sm text-slate-600">
                  {feature.description}
                </p>
              </motion.div>
            ))}
          </motion.div>
        </motion.div>
      </main>

      {/* Footer */}
      <motion.footer
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.8 }}
        className="relative bg-white/80 backdrop-blur-md border-t border-slate-200/50 mt-16"
      >
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <p className="text-center text-sm text-slate-500">
            © 2025 ATS Resume Analyzer. Powered by AI.
          </p>
        </div>
      </motion.footer>
    </div>
  );
}
