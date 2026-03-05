import React, { useState } from "react";
import { motion } from "framer-motion";
import Sidebar from "./Sidebar";
import { Search, Bell, Menu, X } from "lucide-react";
import { useLocation } from "react-router-dom";

const pageTitles = {
  "/dashboard": "Dashboard",
  "/gallery": "Gallery",
  "/chatbot": "AI Assistant",
  "/people": "People",
  "/settings": "Settings",
};

export default function Layout({ children }) {
  const location = useLocation();
  const [searchQuery, setSearchQuery] = useState("");
  const [isSearchOpen, setIsSearchOpen] = useState(false);

  const currentTitle = pageTitles[location.pathname] || "Dashboard";

  return (
    <div className="min-h-screen bg-background">
      {/* Sidebar */}
      <Sidebar />

      {/* Main Content */}
      <main className="lg:pl-64 min-h-screen flex flex-col">
        {/* Header */}
        <header className="sticky top-0 z-30 bg-background/80 backdrop-blur-xl border-b border-white/[0.06]">
          <div className="flex items-center justify-between px-6 h-16">
            {/* Left: Title */}
            <div className="flex items-center gap-4">
              <h1 className="text-lg font-semibold text-foreground">
                {currentTitle}
              </h1>
            </div>

            {/* Right: Search & Actions */}
            <div className="flex items-center gap-3">
              {/* Search */}
              <div className="hidden md:block relative">
                <input
                  type="text"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  placeholder="Search..."
                  className="w-56 h-9 pl-9 pr-4 bg-card border border-white/[0.06] rounded-lg text-sm text-foreground placeholder:text-muted-foreground focus:outline-none focus:border-white/10 focus:bg-elevated transition-all"
                />
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
              </div>

              {/* Mobile Search Toggle */}
              <button
                onClick={() => setIsSearchOpen(!isSearchOpen)}
                className="md:hidden p-2 rounded-lg bg-card border border-white/[0.06] text-muted-foreground hover:text-foreground transition-colors"
              >
                {isSearchOpen ? (
                  <X className="w-4 h-4" />
                ) : (
                  <Search className="w-4 h-4" />
                )}
              </button>

              {/* Notifications */}
              <button className="relative p-2 rounded-lg bg-card border border-white/[0.06] text-muted-foreground hover:text-foreground hover:border-white/10 transition-all">
                <Bell className="w-4 h-4" />
                <span className="absolute top-1.5 right-1.5 w-1.5 h-1.5 bg-destructive rounded-full" />
              </button>

              {/* User */}
              <div className="w-8 h-8 bg-gradient-to-br from-primary to-secondary rounded-full flex items-center justify-center text-white text-xs font-medium cursor-pointer hover:opacity-90 transition-opacity" />
            </div>
          </div>

          {/* Mobile Search */}
          {isSearchOpen && (
            <div className="md:hidden px-6 pb-4">
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Search..."
                className="w-full h-10 pl-10 pr-4 bg-card border border-white/[0.06] rounded-lg text-sm text-foreground placeholder:text-muted-foreground focus:outline-none focus:border-white/10"
              />
            </div>
          )}
        </header>

        {/* Page Content */}
        <div className="flex-1 p-6">
          <motion.div
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3 }}
          >
            {children}
          </motion.div>
        </div>
      </main>
    </div>
  );
}
