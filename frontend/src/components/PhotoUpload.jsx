import React, { useState, useCallback } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Cloud, Upload, CheckCircle, FileImage, Loader2 } from "lucide-react";
import { photoAPI } from "../services/api";
import toast from "react-hot-toast";

export default function PhotoUpload({ onUploadComplete }) {
  const [isDragging, setIsDragging] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [uploadedFile, setUploadedFile] = useState(null);

  const handleDragEnter = useCallback((e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(true);
  }, []);

  const handleDragLeave = useCallback((e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
  }, []);

  const handleDragOver = useCallback((e) => {
    e.preventDefault();
    e.stopPropagation();
  }, []);

  const handleDrop = useCallback((e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);

    const files = e.dataTransfer.files;
    if (files && files.length > 0) {
      handleUpload(files[0]);
    }
  }, []);

  const handleFileSelect = (e) => {
    const files = e.target.files;
    if (files && files.length > 0) {
      handleUpload(files[0]);
    }
  };

  const handleUpload = async (file) => {
    if (!file.type.startsWith("image/")) {
      toast.error("Please select an image file");
      return;
    }

    if (file.size > 50 * 1024 * 1024) {
      toast.error("File size must be less than 50MB");
      return;
    }

    setIsUploading(true);
    setProgress(0);
    setUploadedFile({
      name: file.name,
      size: file.size,
      type: file.type,
    });

    try {
      const progressInterval = setInterval(() => {
        setProgress((prev) => Math.min(prev + Math.random() * 20, 85));
      }, 150);

      const response = await photoAPI.upload(file);
      clearInterval(progressInterval);
      setProgress(100);

      setTimeout(() => {
        onUploadComplete?.(response.data.photo);
        setIsUploading(false);
        setProgress(0);
        setUploadedFile(null);
      }, 600);
    } catch (error) {
      toast.error("Upload failed. Please try again.");
      setIsUploading(false);
      setProgress(0);
      setUploadedFile(null);
    }
  };

  const formatFileSize = (bytes) => {
    if (bytes < 1024) return bytes + " B";
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + " KB";
    return (bytes / (1024 * 1024)).toFixed(1) + " MB";
  };

  return (
    <div className="w-full">
      <div
        onDragEnter={handleDragEnter}
        onDragLeave={handleDragLeave}
        onDragOver={handleDragOver}
        onDrop={handleDrop}
        className={`upload-zone ${isDragging ? "upload-zone-active" : ""} ${isUploading ? "pointer-events-none" : ""}`}
      >
        <input
          type="file"
          id="photo-input"
          onChange={handleFileSelect}
          accept="image/*"
          className="hidden"
          disabled={isUploading}
        />

        <label htmlFor="photo-input" className="cursor-pointer block w-full">
          <AnimatePresence mode="wait">
            {isUploading ? (
              <motion.div
                key="uploading"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                className="space-y-5"
              >
                {/* File Info */}
                {uploadedFile && (
                  <div className="flex items-center gap-3 p-3 bg-white/[0.02] rounded-lg border border-white/[0.04]">
                    <div className="w-10 h-10 rounded-lg bg-white/[0.03] flex items-center justify-center">
                      <FileImage className="w-5 h-5 text-muted-foreground" />
                    </div>
                    <div className="flex-1 min-w-0">
                      <p className="text-sm text-foreground truncate">
                        {uploadedFile.name}
                      </p>
                      <p className="text-xs text-muted-foreground">
                        {formatFileSize(uploadedFile.size)}
                      </p>
                    </div>
                    {progress >= 100 ? (
                      <CheckCircle className="w-5 h-5 text-green-500" />
                    ) : (
                      <Loader2 className="w-5 h-5 text-muted-foreground animate-spin" />
                    )}
                  </div>
                )}

                {/* Progress */}
                <div className="space-y-2">
                  <div className="flex items-center justify-between text-sm">
                    <span className="text-muted-foreground">Uploading...</span>
                    <span className="text-foreground font-medium">
                      {Math.round(progress)}%
                    </span>
                  </div>
                  <div className="progress-bar">
                    <motion.div
                      className="progress-bar-fill"
                      initial={{ width: 0 }}
                      animate={{ width: `${progress}%` }}
                    />
                  </div>
                </div>

                {/* Icon */}
                <motion.div
                  animate={{ y: [0, -6, 0] }}
                  transition={{
                    repeat: Infinity,
                    duration: 2,
                    ease: "easeInOut",
                  }}
                  className="w-14 h-14 rounded-xl bg-white/[0.03] flex items-center justify-center mx-auto"
                >
                  <Upload className="w-6 h-6 text-muted-foreground" />
                </motion.div>
              </motion.div>
            ) : (
              <motion.div
                key="idle"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                className="space-y-5"
              >
                {/* Icon */}
                <motion.div
                  animate={{ y: isDragging ? -6 : 0 }}
                  className="w-16 h-16 rounded-xl bg-white/[0.03] flex items-center justify-center mx-auto"
                >
                  <Cloud className="w-7 h-7 text-muted-foreground" />
                </motion.div>

                {/* Text */}
                <div className="space-y-1">
                  <p className="text-sm font-medium text-foreground">
                    {isDragging
                      ? "Drop your photo here"
                      : "Drag and drop your photo"}
                  </p>
                  <p className="text-xs text-muted-foreground">
                    or click to browse files
                  </p>
                </div>

                {/* File Types */}
                <div className="flex flex-wrap justify-center gap-1.5">
                  {["JPG", "PNG", "GIF", "WEBP", "HEIC"].map((type) => (
                    <span key={type} className="badge-default text-2xs">
                      {type}
                    </span>
                  ))}
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </label>

        {/* Drag Overlay */}
        <AnimatePresence>
          {isDragging && !isUploading && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="absolute inset-0 bg-primary/5 border-2 border-dashed border-primary rounded-2xl flex items-center justify-center"
            >
              <div className="text-center">
                <motion.div
                  animate={{ scale: [1, 1.15, 1] }}
                  transition={{ repeat: Infinity, duration: 1.5 }}
                  className="w-12 h-12 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-3"
                >
                  <Upload className="w-5 h-5 text-primary" />
                </motion.div>
                <p className="text-sm font-medium text-primary">
                  Drop to upload
                </p>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
}
