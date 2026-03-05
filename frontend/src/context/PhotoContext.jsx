import React, { createContext, useContext, useState, useCallback } from "react";

const PhotoContext = createContext();

export const PhotoProvider = ({ children }) => {
  const [photos, setPhotos] = useState([]);
  const [selectedPhoto, setSelectedPhoto] = useState(null);
  const [people, setPeople] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const addPhoto = useCallback((newPhoto) => {
    setPhotos((prev) => [newPhoto, ...prev]);
  }, []);

  const removePhoto = useCallback((photoId) => {
    setPhotos((prev) => prev.filter((p) => p.id !== photoId));
  }, []);

  const updatePhoto = useCallback((photoId, updates) => {
    setPhotos((prev) =>
      prev.map((p) => (p.id === photoId ? { ...p, ...updates } : p)),
    );
  }, []);

  const addPerson = useCallback((newPerson) => {
    setPeople((prev) => [newPerson, ...prev]);
  }, []);

  const value = {
    photos,
    setPhotos,
    selectedPhoto,
    setSelectedPhoto,
    people,
    setPeople,
    isLoading,
    setIsLoading,
    error,
    setError,
    addPhoto,
    removePhoto,
    updatePhoto,
    addPerson,
  };

  return (
    <PhotoContext.Provider value={value}>{children}</PhotoContext.Provider>
  );
};

export const usePhotos = () => {
  const context = useContext(PhotoContext);
  if (!context) {
    throw new Error("usePhotos must be used within PhotoProvider");
  }
  return context;
};
