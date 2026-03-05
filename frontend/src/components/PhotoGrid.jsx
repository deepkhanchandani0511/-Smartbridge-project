import React, { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  Trash2,
  Download,
  Eye,
  Tag,
  Share2,
  X,
  User,
  Check,
  Loader2,
  Mail,
  Phone,
} from "lucide-react";
import { formatDate } from "../utils/helpers";
import { faceAPI } from "../services/api";
import toast from "react-hot-toast";

export default function PhotoGrid({ photos, onDelete, viewMode = "grid" }) {
  const [labelingFaceId, setLabelingFaceId] = useState(null);
  const [labelName, setLabelName] = useState("");
  const [activePhoto, setActivePhoto] = useState(null);

  const handleLabelFace = async (photoId, faceIndex) => {
    if (!labelName.trim()) return;

    try {
      await faceAPI.labelFace(photoId, faceIndex, labelName);
      toast.success(`Face labeled as ${labelName}`);
      setLabelingFaceId(null);
      setLabelName("");
    } catch (error) {
      toast.error("Failed to label face");
    }
  };

  const PhotoCard = ({ photo, index }) => {
    return (
      <motion.div
        layout
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        exit={{ opacity: 0, scale: 0.95 }}
        transition={{ delay: index * 0.02 }}
        onClick={() => setActivePhoto(photo)}
        className="photo-card group cursor-pointer"
      >
        {/* Image Placeholder */}
        <div className="absolute inset-0 bg-muted flex items-center justify-center">
          <User className="w-8 h-8 text-muted-foreground" />
        </div>

        {/* Status Badge */}
        <div className="absolute top-2 left-2">
          <span
            className={`px-2 py-0.5 rounded-md text-[10px] font-medium backdrop-blur-sm ${
              photo.processed === 2
                ? "bg-green-500/10 text-green-400 border border-green-500/20"
                : photo.processed === 1
                  ? "bg-blue-500/10 text-blue-400 border border-blue-500/20"
                  : "bg-white/5 text-muted-foreground border border-white/5"
            }`}
          >
            {photo.processed === 2 ? "✓" : photo.processed === 1 ? "⧖" : "○"}{" "}
            {photo.processed === 2
              ? "Processed"
              : photo.processed === 1
                ? "Processing"
                : "Pending"}
          </span>
        </div>

        {/* Face Count */}
        {photo.faces_detected > 0 && (
          <div className="absolute top-2 right-2">
            <span className="flex items-center gap-1 px-2 py-0.5 rounded-md text-[10px] font-medium bg-secondary/10 text-secondary border border-secondary/20 backdrop-blur-sm">
              <User className="w-2.5 h-2.5" />
              {photo.faces_detected}
            </span>
          </div>
        )}

        {/* Hover Overlay */}
        <div className="photo-card-overlay">
          <div className="flex items-center gap-1.5">
            <motion.button
              whileHover={{ scale: 1.1 }}
              whileTap={{ scale: 0.9 }}
              onClick={(e) => {
                e.stopPropagation();
                setActivePhoto(photo);
              }}
              className="p-1.5 bg-white/10 rounded-md hover:bg-white/20 transition-colors"
            >
              <Eye className="w-3.5 h-3.5 text-white" />
            </motion.button>
            <motion.button
              whileHover={{ scale: 1.1 }}
              whileTap={{ scale: 0.9 }}
              onClick={(e) => {
                e.stopPropagation();
              }}
              className="p-1.5 bg-white/10 rounded-md hover:bg-white/20 transition-colors"
            >
              <Download className="w-3.5 h-3.5 text-white" />
            </motion.button>
            <motion.button
              whileHover={{ scale: 1.1 }}
              whileTap={{ scale: 0.9 }}
              onClick={(e) => {
                e.stopPropagation();
                onDelete?.(photo.id);
              }}
              className="p-1.5 bg-red-500/20 rounded-md hover:bg-red-500/30 transition-colors"
            >
              <Trash2 className="w-3.5 h-3.5 text-red-400" />
            </motion.button>
          </div>
        </div>
      </motion.div>
    );
  };

  const PhotoModal = () => {
    if (!activePhoto) return null;

    return (
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        className="modal-overlay"
        onClick={() => setActivePhoto(null)}
      >
        <motion.div
          initial={{ scale: 0.95, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          exit={{ scale: 0.95, opacity: 0 }}
          onClick={(e) => e.stopPropagation()}
          className="modal-content"
        >
          {/* Header */}
          <div className="flex items-center justify-between p-4 border-b border-white/[0.06]">
            <div>
              <h3 className="font-medium text-foreground">
                {activePhoto.filename}
              </h3>
              <p className="text-xs text-muted-foreground">
                Uploaded {formatDate(activePhoto.upload_date)}
              </p>
            </div>
            <button
              onClick={() => setActivePhoto(null)}
              className="p-1.5 rounded-md text-muted-foreground hover:text-foreground hover:bg-white/5 transition-colors"
            >
              <X className="w-4 h-4" />
            </button>
          </div>

          {/* Image */}
          <div className="p-4">
            <div className="relative aspect-video bg-muted rounded-xl flex items-center justify-center mb-4">
              <User className="w-16 h-16 text-muted-foreground" />

              {/* Face Bounding Boxes */}
              {activePhoto.faces_detected > 0 && (
                <div className="absolute inset-8">
                  {Array.from({ length: activePhoto.faces_detected }).map(
                    (_, idx) => (
                      <div
                        key={idx}
                        className="absolute w-16 h-20 border-2 border-secondary/60 rounded-lg cursor-pointer hover:border-primary transition-colors"
                        style={{ left: `${20 + idx * 25}%`, top: "15%" }}
                        onClick={(e) => {
                          e.stopPropagation();
                          setLabelingFaceId(idx);
                        }}
                      >
                        <div className="absolute -top-2 -right-2 w-4 h-4 bg-secondary rounded-full flex items-center justify-center">
                          <Tag className="w-2 h-2 text-white" />
                        </div>
                      </div>
                    ),
                  )}
                </div>
              )}
            </div>

            {/* Face Labeling */}
            {activePhoto.faces_detected > 0 && (
              <div className="mb-4 p-3 bg-muted rounded-xl">
                <h4 className="text-xs font-medium text-muted-foreground mb-2">
                  Detected Faces
                </h4>
                <div className="space-y-1.5">
                  {Array.from({ length: activePhoto.faces_detected }).map(
                    (_, idx) => (
                      <div
                        key={idx}
                        className="flex items-center justify-between p-2 bg-card rounded-lg"
                      >
                        <div className="flex items-center gap-2">
                          <div className="w-6 h-6 bg-secondary/10 rounded-full flex items-center justify-center">
                            <User className="w-3 h-3 text-secondary" />
                          </div>
                          <span className="text-sm text-muted-foreground">
                            Face {idx + 1}
                          </span>
                        </div>
                        {labelingFaceId === idx ? (
                          <div className="flex items-center gap-1.5">
                            <input
                              type="text"
                              value={labelName}
                              onChange={(e) => setLabelName(e.target.value)}
                              placeholder="Name..."
                              className="h-6 px-2 bg-muted border border-white/5 rounded-md text-xs text-foreground placeholder:text-muted-foreground focus:outline-none focus:border-white/10"
                              autoFocus
                            />
                            <button
                              onClick={() =>
                                handleLabelFace(activePhoto.id, idx)
                              }
                              className="p-1 bg-green-500/10 text-green-400 rounded hover:bg-green-500/20"
                            >
                              <Check className="w-3 h-3" />
                            </button>
                            <button
                              onClick={() => {
                                setLabelingFaceId(null);
                                setLabelName("");
                              }}
                              className="p-1 text-muted-foreground hover:text-foreground"
                            >
                              <X className="w-3 h-3" />
                            </button>
                          </div>
                        ) : (
                          <button
                            onClick={() => setLabelingFaceId(idx)}
                            className="flex items-center gap-1 px-2 py-1 text-xs bg-muted border border-white/5 rounded-md text-muted-foreground hover:text-foreground hover:border-white/10 transition-colors"
                          >
                            <Tag className="w-3 h-3" />
                            Label
                          </button>
                        )}
                      </div>
                    ),
                  )}
                </div>
              </div>
            )}

            {/* Actions */}
            <div className="flex gap-2">
              <button className="btn-primary flex-1 text-sm">
                <Eye className="w-4 h-4" />
                View
              </button>
              <button className="btn-secondary flex-1 text-sm">
                <Download className="w-4 h-4" />
                Download
              </button>
              <button className="btn-secondary text-sm">
                <Share2 className="w-4 h-4" />
              </button>
            </div>

            {/* Quick Share */}
            <div className="mt-3 pt-3 border-t border-white/[0.06]">
              <p className="text-xs text-muted-foreground mb-2">Quick Share</p>
              <div className="flex gap-2">
                <button className="btn-ghost flex-1 text-sm justify-center">
                  <Mail className="w-3.5 h-3.5" />
                  Email
                </button>
                <button className="btn-ghost flex-1 text-sm justify-center">
                  <Phone className="w-3.5 h-3.5" />
                  WhatsApp
                </button>
              </div>
            </div>
          </div>
        </motion.div>
      </motion.div>
    );
  };

  return (
    <>
      <motion.div
        layout
        className={
          viewMode === "masonry"
            ? "columns-2 sm:columns-3 lg:columns-4 xl:columns-5 gap-3 space-y-3"
            : "photo-grid"
        }
      >
        {photos.map((photo, index) => (
          <PhotoCard key={photo.id} photo={photo} index={index} />
        ))}
      </motion.div>

      <AnimatePresence>{activePhoto && <PhotoModal />}</AnimatePresence>
    </>
  );
}
