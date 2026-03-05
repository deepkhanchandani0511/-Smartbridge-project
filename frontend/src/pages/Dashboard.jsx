import React from "react";
import { motion } from "framer-motion";
import {
  Image,
  Users,
  Send,
  Clock,
  TrendingUp,
  ArrowRight,
  Upload,
  Sparkles,
} from "lucide-react";
import { useNavigate } from "react-router-dom";
import { usePhotos } from "../context/PhotoContext";

const stats = [
  {
    label: "Total Photos",
    value: "0",
    icon: Image,
    trend: "+12%",
    trendUp: true,
  },
  {
    label: "Recognized Faces",
    value: "0",
    icon: Users,
    trend: "+8%",
    trendUp: true,
  },
  {
    label: "Deliveries",
    value: "0",
    icon: Send,
    trend: "+24%",
    trendUp: true,
  },
  {
    label: "This Week",
    value: "0",
    icon: Clock,
    trend: "+5%",
    trendUp: true,
  },
];

const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: { staggerChildren: 0.05 },
  },
};

const itemVariants = {
  hidden: { opacity: 0, y: 8 },
  visible: { opacity: 1, y: 0 },
};

export default function Dashboard() {
  const navigate = useNavigate();
  const { photos } = usePhotos();

  const statsWithData = stats.map((stat, index) => {
    switch (index) {
      case 0:
        return { ...stat, value: photos.length.toString() };
      default:
        return stat;
    }
  });

  return (
    <motion.div
      variants={containerVariants}
      initial="hidden"
      animate="visible"
      className="space-y-6"
    >
      {/* Welcome Banner */}
      <motion.div
        variants={itemVariants}
        className="card p-6 relative overflow-hidden"
      >
        <div className="absolute top-0 right-0 w-96 h-96 bg-gradient-to-br from-primary/10 to-secondary/5 rounded-full blur-3xl -translate-y-1/2 translate-x-1/2" />
        <div className="relative">
          <h2 className="text-xl font-semibold text-foreground mb-2">
            Welcome back
          </h2>
          <p className="text-muted-foreground text-sm mb-5 max-w-lg">
            Your photos are being organized and faces are being recognized.
            Upload more to improve your gallery.
          </p>

          <div className="flex flex-wrap gap-2">
            <button
              onClick={() => navigate("/gallery")}
              className="btn-primary"
            >
              <Upload className="w-4 h-4" />
              Upload Photos
            </button>
            <button
              onClick={() => navigate("/gallery")}
              className="btn-secondary"
            >
              <Image className="w-4 h-4" />
              View Gallery
            </button>
          </div>
        </div>
      </motion.div>

      {/* Stats Grid */}
      <motion.div variants={itemVariants}>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {statsWithData.map((stat, index) => {
            const Icon = stat.icon;
            return (
              <motion.div
                key={stat.label}
                initial={{ opacity: 0, y: 8 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.05 }}
                className="card-elevated p-4"
              >
                <div className="flex items-start justify-between mb-3">
                  <div className="w-9 h-9 rounded-lg bg-white/[0.03] flex items-center justify-center">
                    <Icon className="w-4 h-4 text-muted-foreground" />
                  </div>
                  <span
                    className={`text-xs font-medium ${stat.trendUp ? "text-green-500" : "text-red-500"}`}
                  >
                    {stat.trend}
                  </span>
                </div>
                <h3 className="text-2xl font-semibold text-foreground">
                  {stat.value}
                </h3>
                <p className="text-sm text-muted-foreground mt-1">
                  {stat.label}
                </p>
              </motion.div>
            );
          })}
        </div>
      </motion.div>

      {/* Two Column Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Recent Activity */}
        <motion.div variants={itemVariants} className="lg:col-span-2">
          <div className="card p-5">
            <div className="flex items-center justify-between mb-4">
              <h3 className="font-semibold text-foreground">Recent Activity</h3>
              <button className="text-sm text-muted-foreground hover:text-foreground transition-colors">
                View all
              </button>
            </div>

            <div className="space-y-1">
              {[
                { action: "Photo uploaded", time: "2 min ago", icon: Image },
                { action: "Face recognized", time: "5 min ago", icon: Users },
                {
                  action: "Photo sent to email",
                  time: "1 hour ago",
                  icon: Send,
                },
              ].map((item, index) => (
                <div
                  key={index}
                  className="flex items-center gap-3 p-2.5 rounded-lg hover:bg-white/[0.02] transition-colors list-item"
                >
                  <div className="w-8 h-8 rounded-lg bg-white/[0.03] flex items-center justify-center">
                    <item.icon className="w-4 h-4 text-muted-foreground" />
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm text-foreground truncate">
                      {item.action}
                    </p>
                  </div>
                  <span className="text-xs text-muted-foreground">
                    {item.time}
                  </span>
                </div>
              ))}
            </div>
          </div>
        </motion.div>

        {/* Quick Upload */}
        <motion.div variants={itemVariants}>
          <div className="card p-5 h-full">
            <h3 className="font-semibold text-foreground mb-4">Quick Upload</h3>
            <div
              onClick={() => navigate("/gallery")}
              className="border border-dashed border-white/[0.08] rounded-xl p-6 text-center hover:border-white/15 hover:bg-white/[0.01] transition-all cursor-pointer"
            >
              <div className="w-12 h-12 rounded-xl bg-white/[0.03] flex items-center justify-center mx-auto mb-3">
                <Upload className="w-5 h-5 text-muted-foreground" />
              </div>
              <p className="text-sm text-foreground mb-1">Drop photos here</p>
              <p className="text-xs text-muted-foreground">
                or click to browse
              </p>
            </div>
            <div className="flex flex-wrap gap-1.5 mt-4">
              {["JPG", "PNG", "HEIC"].map((ext) => (
                <span key={ext} className="badge-default text-2xs">
                  {ext}
                </span>
              ))}
            </div>
          </div>
        </motion.div>
      </div>

      {/* Recent Uploads */}
      <motion.div variants={itemVariants}>
        <div className="card p-5">
          <div className="flex items-center justify-between mb-4">
            <h3 className="font-semibold text-foreground">Recent Uploads</h3>
            <button
              onClick={() => navigate("/gallery")}
              className="text-sm text-muted-foreground hover:text-foreground flex items-center gap-1 transition-colors"
            >
              View gallery
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </div>

          {photos.length > 0 ? (
            <div className="grid grid-cols-3 sm:grid-cols-4 md:grid-cols-6 gap-2">
              {photos.slice(0, 6).map((photo, index) => (
                <motion.div
                  key={photo.id}
                  initial={{ opacity: 0, scale: 0.95 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ delay: index * 0.03 }}
                  className="aspect-square rounded-lg bg-muted overflow-hidden hover:opacity-80 transition-opacity cursor-pointer"
                  onClick={() => navigate("/gallery")}
                >
                  <div className="w-full h-full flex items-center justify-center">
                    <Image className="w-6 h-6 text-muted-foreground" />
                  </div>
                </motion.div>
              ))}
            </div>
          ) : (
            <div className="text-center py-8">
              <div className="w-14 h-14 rounded-xl bg-white/[0.03] flex items-center justify-center mx-auto mb-3">
                <Image className="w-6 h-6 text-muted-foreground" />
              </div>
              <p className="text-sm text-muted-foreground mb-3">
                No photos yet
              </p>
              <button
                onClick={() => navigate("/gallery")}
                className="btn-primary text-sm"
              >
                Upload Photos
              </button>
            </div>
          )}
        </div>
      </motion.div>
    </motion.div>
  );
}
