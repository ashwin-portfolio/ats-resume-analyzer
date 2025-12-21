import { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { motion, AnimatePresence } from 'framer-motion';
import { Upload, File, X, CheckCircle2, FileText } from 'lucide-react';

export default function FileUpload({ onFileSelect, selectedFile, error }) {
  const [dragActive, setDragActive] = useState(false);

  const onDrop = useCallback(
    (acceptedFiles) => {
      if (acceptedFiles.length > 0) {
        const file = acceptedFiles[0];
        // Validate file type
        const validTypes = ['.pdf', '.docx', '.doc'];
        const fileExtension = '.' + file.name.split('.').pop().toLowerCase();
        
        if (validTypes.includes(fileExtension)) {
          onFileSelect(file);
        } else {
          onFileSelect(null, 'Invalid file type. Please upload PDF or DOCX files only.');
        }
      }
    },
    [onFileSelect]
  );

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
      'application/msword': ['.doc'],
    },
    maxFiles: 1,
    maxSize: 10 * 1024 * 1024, // 10MB
  });

  const removeFile = () => {
    onFileSelect(null);
  };

  const formatFileSize = (bytes) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
  };

  return (
    <div className="w-full">
      <AnimatePresence mode="wait">
        {!selectedFile ? (
          <motion.div
            key="upload"
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.95 }}
            transition={{ duration: 0.2 }}
            {...getRootProps()}
            className={`
              relative border-2 border-dashed rounded-xl p-12
              transition-all duration-300 cursor-pointer
              ${isDragActive || dragActive
                ? 'border-blue-500 bg-gradient-to-br from-blue-50 to-indigo-50 shadow-lg'
                : 'border-slate-300 bg-white hover:border-blue-400 hover:bg-gradient-to-br hover:from-blue-50 hover:to-indigo-50 hover:shadow-md'
              }
              ${error ? 'border-red-400 bg-red-50' : ''}
            `}
            onMouseEnter={() => setDragActive(true)}
            onMouseLeave={() => setDragActive(false)}
            whileHover={{ scale: 1.01 }}
            whileTap={{ scale: 0.99 }}
          >
            <input {...getInputProps()} />
            <div className="flex flex-col items-center justify-center space-y-4">
              <motion.div
                animate={{
                  y: isDragActive || dragActive ? [-5, 5, -5] : 0,
                }}
                transition={{
                  duration: 2,
                  repeat: Infinity,
                  ease: "easeInOut",
                }}
                className={`
                  p-4 rounded-full transition-colors duration-300
                  ${isDragActive || dragActive
                    ? 'bg-blue-100 shadow-lg'
                    : 'bg-slate-100'
                  }
                `}
              >
                <Upload
                  className={`
                    w-10 h-10 transition-colors duration-300
                    ${isDragActive || dragActive ? 'text-blue-600' : 'text-slate-600'}
                  `}
                />
              </motion.div>
              <div className="text-center">
                <motion.p
                  animate={{
                    scale: isDragActive || dragActive ? [1, 1.05, 1] : 1,
                  }}
                  transition={{
                    duration: 1.5,
                    repeat: Infinity,
                    ease: "easeInOut",
                  }}
                  className="text-lg font-semibold text-slate-700"
                >
                  {isDragActive || dragActive
                    ? 'Drop your resume here'
                    : 'Drag & drop your resume'}
                </motion.p>
                <p className="text-sm text-slate-500 mt-2">
                  or click to browse
                </p>
                <p className="text-xs text-slate-400 mt-3 flex items-center justify-center space-x-1">
                  <FileText className="w-3 h-3" />
                  <span>Supports PDF, DOCX (Max 10MB)</span>
                </p>
              </div>
            </div>
            {/* Animated border effect */}
            {isDragActive || dragActive ? (
              <motion.div
                className="absolute inset-0 rounded-xl border-2 border-blue-500"
                initial={{ opacity: 0 }}
                animate={{ opacity: [0.5, 1, 0.5] }}
                transition={{
                  duration: 1.5,
                  repeat: Infinity,
                  ease: "easeInOut",
                }}
              />
            ) : null}
          </motion.div>
        ) : (
          <motion.div
            key="file"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ duration: 0.3 }}
            className="card flex items-center justify-between group"
          >
            <div className="flex items-center space-x-4 flex-1">
              <motion.div
                initial={{ scale: 0 }}
                animate={{ scale: 1 }}
                transition={{ type: "spring", stiffness: 200, damping: 15 }}
                className="p-3 bg-gradient-to-br from-green-100 to-emerald-100 rounded-lg shadow-md"
              >
                <CheckCircle2 className="w-6 h-6 text-green-600" />
              </motion.div>
              <div className="flex-1 min-w-0">
                <div className="flex items-center space-x-2">
                  <File className="w-5 h-5 text-slate-500" />
                  <p className="font-semibold text-slate-700 truncate">
                    {selectedFile.name}
                  </p>
                </div>
                <p className="text-sm text-slate-500 mt-1">
                  {formatFileSize(selectedFile.size)}
                </p>
              </div>
            </div>
            <motion.button
              whileHover={{ scale: 1.1, rotate: 90 }}
              whileTap={{ scale: 0.9 }}
              onClick={removeFile}
              className="p-2 hover:bg-slate-100 rounded-lg transition-colors"
              aria-label="Remove file"
            >
              <X className="w-5 h-5 text-slate-500" />
            </motion.button>
          </motion.div>
        )}
      </AnimatePresence>
      {error && (
        <motion.p
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          className="mt-2 text-sm text-red-600 flex items-center space-x-1"
        >
          <X className="w-4 h-4" />
          <span>{error}</span>
        </motion.p>
      )}
    </div>
  );
}
