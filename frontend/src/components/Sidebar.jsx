import React, { useState } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { motion, AnimatePresence } from "framer-motion";
import {
  Home,
  Image,
  MessageSquare,
  Settings,
  LogOut,
  Camera,
  Users,
  ChevronLeft,
  Menu,
  X,
} from "lucide-react";

export default function Sidebar() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const [isCollapsed, setIsCollapsed] = useState(false);
  const [isMobileOpen, setIsMobileOpen] = useState(false);

  const handleLogout = () => {
    logout();
    navigate("/login");
    setIsMobileOpen(false);
  };

  const navItems = [
    { label: "Dashboard", icon: Home, path: "/dashboard" },
    { label: "Gallery", icon: Image, path: "/gallery" },
    { label: "Chat", icon: MessageSquare, path: "/chatbot" },
    { label: "People", icon: Users, path: "/people" },
    { label: "Settings", icon: Settings, path: "/settings" },
  ];

  const NavContent = ({ isMobile = false }) => (
    <div className="flex flex-col h-full">
      {/* Logo */}
      <div className="p-4 border-b border-white/[0.06]">
        <div
          onClick={() => {
            navigate("/dashboard");
            if (isMobile) setIsMobileOpen(false);
          }}
          className="flex items-center gap-3 cursor-pointer group"
        >
          <div className="w-8 h-8 bg-gradient-to-br from-primary to-secondary rounded-lg flex items-center justify-center shadow-glow">
            <Camera className="w-4 h-4 text-white" />
          </div>
          <AnimatePresence>
            {(!isCollapsed || isMobile) && (
              <motion.div
                initial={{ opacity: 0, width: 0 }}
                animate={{ opacity: 1, width: "auto" }}
                exit={{ opacity: 0, width: 0 }}
                className="overflow-hidden"
              >
                <span className="text-sm font-semibold text-foreground whitespace-nowrap">
                  Drishyamitra
                </span>
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 p-3 space-y-0.5 overflow-y-auto">
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = location.pathname === item.path;
          return (
            <button
              key={item.path}
              onClick={() => {
                navigate(item.path);
                if (isMobile) setIsMobileOpen(false);
              }}
              className={`w-full relative flex items-center gap-3 px-3 py-2.5 rounded-lg transition-all duration-150 ${
                isActive
                  ? "bg-white/[0.06] text-foreground"
                  : "text-muted-foreground hover:bg-white/[0.03] hover:text-foreground"
              }`}
            >
              {isActive && (
                <div className="absolute left-0 top-1/2 -translate-y-1/2 w-0.5 h-4 bg-foreground rounded-full" />
              )}
              <Icon
                className={`w-4 h-4 flex-shrink-0 ${isActive ? "text-foreground" : ""}`}
              />
              <AnimatePresence>
                {(!isCollapsed || isMobile) && (
                  <motion.span
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    exit={{ opacity: 0 }}
                    className="text-sm font-medium whitespace-nowrap"
                  >
                    {item.label}
                  </motion.span>
                )}
              </AnimatePresence>
            </button>
          );
        })}
      </nav>

      {/* User Section */}
      <div className="p-3 border-t border-white/[0.06]">
        <div className="card p-3 mb-3">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 bg-gradient-to-br from-primary to-secondary rounded-full flex items-center justify-center text-white text-xs font-medium">
              {user?.email?.charAt(0).toUpperCase() || "U"}
            </div>
            <AnimatePresence>
              {(!isCollapsed || isMobile) && (
                <motion.div
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{ opacity: 0 }}
                  className="flex-1 min-w-0"
                >
                  <p className="text-sm font-medium text-foreground truncate">
                    {user?.email?.split("@")[0] || "User"}
                  </p>
                  <p className="text-xs text-muted-foreground">Online</p>
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        </div>

        <button
          onClick={handleLogout}
          className="w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-muted-foreground hover:bg-white/[0.03] hover:text-foreground transition-all duration-150"
        >
          <LogOut className="w-4 h-4" />
          <AnimatePresence>
            {(!isCollapsed || isMobile) && (
              <motion.span
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                className="text-sm font-medium"
              >
                Sign out
              </motion.span>
            )}
          </AnimatePresence>
        </button>
      </div>

      {/* Collapse Toggle (Desktop) */}
      {!isMobile && (
        <div className="p-3 border-t border-white/[0.06]">
          <button
            onClick={() => setIsCollapsed(!isCollapsed)}
            className="w-full flex items-center justify-center gap-2 px-3 py-2 rounded-lg text-muted-foreground hover:bg-white/[0.03] hover:text-foreground transition-all duration-150"
          >
            <ChevronLeft
              className={`w-4 h-4 transition-transform ${isCollapsed ? "rotate-180" : ""}`}
            />
            {!isCollapsed && <span className="text-xs">Collapse</span>}
          </button>
        </div>
      )}
    </div>
  );

  return (
    <>
      {/* Mobile Menu Button */}
      <button
        onClick={() => setIsMobileOpen(true)}
        className="lg:hidden fixed top-3 left-3 z-50 p-2 rounded-lg bg-card border border-white/[0.06] text-foreground"
      >
        <Menu className="w-5 h-5" />
      </button>

      {/* Mobile Overlay */}
      <AnimatePresence>
        {isMobileOpen && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="lg:hidden fixed inset-0 bg-black/50 backdrop-blur-sm z-40"
            onClick={() => setIsMobileOpen(false)}
          />
        )}
      </AnimatePresence>

      {/* Mobile Sidebar */}
      <AnimatePresence>
        {isMobileOpen && (
          <motion.aside
            initial={{ x: -280, opacity: 0 }}
            animate={{ x: 0, opacity: 1 }}
            exit={{ x: -280, opacity: 0 }}
            transition={{ type: "spring", damping: 25, stiffness: 200 }}
            className="lg:hidden fixed left-0 top-0 h-screen w-[280px] bg-card border-r border-white/[0.06] flex flex-col z-50"
          >
            <button
              onClick={() => setIsMobileOpen(false)}
              className="absolute top-4 right-4 p-1.5 rounded-lg text-muted-foreground hover:bg-white/5"
            >
              <X className="w-4 h-4" />
            </button>
            <NavContent isMobile />
          </motion.aside>
        )}
      </AnimatePresence>

      {/* Desktop Sidebar */}
      <motion.aside
        initial={false}
        animate={{ width: isCollapsed ? 72 : 280 }}
        transition={{ duration: 0.2 }}
        className="hidden lg:flex fixed left-0 top-0 h-screen bg-card border-r border-white/[0.06] flex-col z-40"
      >
        <NavContent />
      </motion.aside>
    </>
  );
}
