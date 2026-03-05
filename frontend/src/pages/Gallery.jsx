import React, { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  Upload,
  Trash2,
  Users,
  Search,
  Grid,
  LayoutGrid,
  Image as ImageIcon,
  Loader2,
} from "lucide-react";
import { photoAPI, faceAPI } from "../services/api";
import { usePhotos } from "../context/PhotoContext";
import toast from "react-hot-toast";
import PhotoUpload from "../components/PhotoUpload";
import PhotoGrid from "../components/PhotoGrid";

const filterOptions = [
  { id: "all", label: "All" },
  { id: "recent", label: "Recent" },
];

export default function Gallery() {
  const { photos, setPhotos, people, setPeople, isLoading, setIsLoading } =
    usePhotos();
  const [selectedFilter, setSelectedFilter] = useState("all");
  const [searchQuery, setSearchQuery] = useState("");
  const [viewMode, setViewMode] = useState("grid");
  const [showUpload, setShowUpload] = useState(true);

  useEffect(() => {
    loadPhotos();
    loadPeople();
  }, []);

  const loadPhotos = async () => {
    try {
      setIsLoading(true);
      const response = await photoAPI.list();
      setPhotos(response.data.photos || []);
    } catch (error) {
      toast.error("Failed to load photos");
    } finally {
      setIsLoading(false);
    }
  };

  const loadPeople = async () => {
    try {
      const response = await faceAPI.getAllPeople();
      setPeople(response.data.people || []);
    } catch (error) {
      console.error("Failed to load people");
    }
  };

  const handlePhotoUploaded = (newPhoto) => {
    setPhotos((prev) => [newPhoto, ...prev]);
    toast.success("Photo uploaded successfully!");
  };

  const handleDeletePhoto = async (photoId) => {
    if (!window.confirm("Are you sure you want to delete this photo?")) return;

    try {
      await photoAPI.delete(photoId);
      setPhotos((prev) => prev.filter((p) => p.id !== photoId));
      toast.success("Photo deleted");
    } catch (error) {
      toast.error("Failed to delete photo");
    }
  };

  const filteredPhotos = photos.filter((photo) => {
    const matchesFilter =
      selectedFilter === "all" ||
      (selectedFilter === "recent" &&
        new Date(photo.upload_date) >
          new Date(Date.now() - 7 * 24 * 60 * 60 * 1000));
    const matchesSearch =
      !searchQuery ||
      photo.filename?.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesFilter && matchesSearch;
  });

  return (
    <div className="space-y-5">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-lg font-semibold text-foreground">Photos</h2>
          <p className="text-sm text-muted-foreground">
            {filteredPhotos.length} photos · {people.length} people
          </p>
        </div>

        <div className="flex items-center gap-2">
          {/* Search */}
          <div className="relative">
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search photos..."
              className="input-search h-9 w-48 sm:w-64 text-sm"
            />
          </div>

          {/* View Toggle */}
          <div className="flex items-center bg-card border border-white/[0.06] rounded-lg p-0.5">
            <button
              onClick={() => setViewMode("grid")}
              className={`p-1.5 rounded-md transition-colors ${
                viewMode === "grid"
                  ? "bg-white/[0.06] text-foreground"
                  : "text-muted-foreground hover:text-foreground"
              }`}
            >
              <Grid className="w-4 h-4" />
            </button>
            <button
              onClick={() => setViewMode("masonry")}
              className={`p-1.5 rounded-md transition-colors ${
                viewMode === "masonry"
                  ? "bg-white/[0.06] text-foreground"
                  : "text-muted-foreground hover:text-foreground"
              }`}
            >
              <LayoutGrid className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>

      {/* Filters */}
      <div className="flex items-center gap-2">
        {filterOptions.map((filter) => (
          <button
            key={filter.id}
            onClick={() => setSelectedFilter(filter.id)}
            className={`filter-pill ${
              selectedFilter === filter.id ? "filter-pill-active" : ""
            }`}
          >
            {filter.label}
          </button>
        ))}

        {people.length > 0 && (
          <>
            <div className="w-px h-5 bg-white/[0.06]" />
            {people.map((person) => (
              <button
                key={person.id}
                onClick={() => setSelectedFilter(person.id)}
                className={`filter-pill flex items-center gap-1.5 ${
                  selectedFilter === person.id ? "filter-pill-active" : ""
                }`}
              >
                <div className="w-5 h-5 rounded-full bg-gradient-to-br from-primary to-secondary flex items-center justify-center text-[10px] text-white">
                  {person.name?.charAt(0).toUpperCase()}
                </div>
                {person.name}
              </button>
            ))}
          </>
        )}
      </div>

      {/* Upload Section */}
      <AnimatePresence>
        {showUpload && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: "auto" }}
            exit={{ opacity: 0, height: 0 }}
          >
            <PhotoUpload onUploadComplete={handlePhotoUploaded} />
          </motion.div>
        )}
      </AnimatePresence>

      {!showUpload && (
        <button onClick={() => setShowUpload(true)} className="btn-primary">
          <Upload className="w-4 h-4" />
          Upload Photos
        </button>
      )}

      {/* Photos Grid */}
      {isLoading ? (
        <div className="flex flex-col items-center justify-center py-20">
          <Loader2 className="w-8 h-8 text-muted-foreground animate-spin mb-3" />
          <p className="text-sm text-muted-foreground">Loading photos...</p>
        </div>
      ) : filteredPhotos.length > 0 ? (
        <PhotoGrid
          photos={filteredPhotos}
          onDelete={handleDeletePhoto}
          viewMode={viewMode}
        />
      ) : (
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          className="card p-10 text-center"
        >
          <div className="w-14 h-14 rounded-xl bg-white/[0.03] flex items-center justify-center mx-auto mb-4">
            <ImageIcon className="w-6 h-6 text-muted-foreground" />
          </div>
          <h3 className="text-base font-medium text-foreground mb-2">
            No photos found
          </h3>
          <p className="text-sm text-muted-foreground mb-5">
            {searchQuery
              ? `No photos match "${searchQuery}"`
              : "Upload your first photo to get started"}
          </p>
          <button
            onClick={() => setShowUpload(true)}
            className="btn-primary inline-flex text-sm"
          >
            <Upload className="w-4 h-4 mr-2" />
            Upload Photos
          </button>
        </motion.div>
      )}
    </div>
  );
}
