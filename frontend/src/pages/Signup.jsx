import React, { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { motion, AnimatePresence } from "framer-motion";
import {
  Mail,
  Lock,
  AlertCircle,
  CheckCircle,
  Camera,
  ArrowRight,
} from "lucide-react";
import toast from "react-hot-toast";

export default function Signup() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");
  const navigate = useNavigate();
  const { signup } = useAuth();

  const [passwordStrength, setPasswordStrength] = useState(0);

  const checkPasswordStrength = (pwd) => {
    let strength = 0;
    if (pwd.length >= 8) strength++;
    if (/[a-z]/.test(pwd) && /[A-Z]/.test(pwd)) strength++;
    if (/[0-9]/.test(pwd)) strength++;
    if (/[^a-zA-Z0-9]/.test(pwd)) strength++;
    setPasswordStrength(strength);
  };

  const handlePasswordChange = (e) => {
    const pwd = e.target.value;
    setPassword(pwd);
    checkPasswordStrength(pwd);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    if (password !== confirmPassword) {
      setError("Passwords do not match");
      return;
    }

    if (password.length < 8) {
      setError("Password must be at least 8 characters");
      return;
    }

    setIsLoading(true);

    try {
      await signup(email, password);
      toast.success("Account created! Please log in.");
      navigate("/login");
    } catch (err) {
      const errorMsg = err.response?.data?.error || "Signup failed";
      setError(errorMsg);
      toast.error(errorMsg);
    } finally {
      setIsLoading(false);
    }
  };

  const strengthLabels = ["", "Weak", "Fair", "Good", "Strong"];
  const strengthColors = [
    "",
    "bg-red-500",
    "bg-yellow-500",
    "bg-blue-500",
    "bg-green-500",
  ];

  return (
    <div className="min-h-screen flex">
      {/* Left - Branding */}
      <div className="hidden lg:flex lg:w-1/2 relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-[#09090b] via-[#18181b] to-[#09090b]" />

        {/* Animated elements */}
        <div className="absolute inset-0 overflow-hidden">
          <motion.div
            animate={{ scale: [1, 1.3, 1], x: [0, 50, 0] }}
            transition={{ duration: 18, repeat: Infinity }}
            className="absolute top-1/3 -right-20 w-96 h-96 bg-secondary/5 rounded-full blur-[120px]"
          />
          <motion.div
            animate={{ scale: [1, 1.4, 1], y: [0, -30, 0] }}
            transition={{ duration: 12, repeat: Infinity }}
            className="absolute bottom-1/4 -left-10 w-72 h-72 bg-primary/5 rounded-full blur-[100px]"
          />
        </div>

        {/* Content */}
        <div className="relative z-10 flex flex-col justify-center p-12">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
          >
            <div className="flex items-center gap-3 mb-8">
              <div className="w-12 h-12 bg-gradient-to-br from-primary to-secondary rounded-xl flex items-center justify-center shadow-glow">
                <Camera className="w-6 h-6 text-white" />
              </div>
              <span className="text-xl font-semibold text-foreground">
                Drishyamitra
              </span>
            </div>

            <h2 className="text-3xl font-semibold text-foreground mb-4 leading-tight">
              Get Started with
              <br />
              AI-Powered Photos
            </h2>
            <p className="text-muted-foreground text-sm max-w-sm mb-8">
              Join thousands of users who trust Drishyamitra to organize their
              precious memories.
            </p>

            <div className="space-y-3">
              {[
                {
                  icon: "👤",
                  title: "Face Recognition",
                  desc: "Auto-tag people",
                },
                {
                  icon: "🎯",
                  title: "Smart Organization",
                  desc: "AI sorts by events",
                },
                {
                  icon: "📤",
                  title: "Easy Sharing",
                  desc: "Email or WhatsApp",
                },
              ].map((feature, index) => (
                <motion.div
                  key={feature.title}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: 0.3 + index * 0.1 }}
                  className="flex items-center gap-3 p-3 bg-white/[0.02] border border-white/[0.04] rounded-xl"
                >
                  <span className="text-xl">{feature.icon}</span>
                  <div>
                    <h3 className="text-sm font-medium text-foreground">
                      {feature.title}
                    </h3>
                    <p className="text-xs text-muted-foreground">
                      {feature.desc}
                    </p>
                  </div>
                </motion.div>
              ))}
            </div>
          </motion.div>
        </div>
      </div>

      {/* Right - Form */}
      <div className="w-full lg:w-1/2 flex items-center justify-center p-8 bg-[#09090b]">
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.4 }}
          className="w-full max-w-sm"
        >
          {/* Mobile Logo */}
          <div className="lg:hidden flex items-center gap-3 mb-8 justify-center">
            <div className="w-10 h-10 bg-gradient-to-br from-primary to-secondary rounded-xl flex items-center justify-center shadow-glow">
              <Camera className="w-5 h-5 text-white" />
            </div>
            <span className="text-lg font-semibold text-foreground">
              Drishyamitra
            </span>
          </div>

          <div className="text-center mb-8">
            <h2 className="text-xl font-semibold text-foreground mb-2">
              Create account
            </h2>
            <p className="text-sm text-muted-foreground">
              Start organizing your photos
            </p>
          </div>

          {/* Error */}
          <AnimatePresence>
            {error && (
              <motion.div
                initial={{ opacity: 0, y: -10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -10 }}
                className="bg-red-500/5 border border-red-500/10 rounded-xl p-3 mb-5 flex items-start gap-2"
              >
                <AlertCircle className="w-4 h-4 text-red-400 flex-shrink-0 mt-0.5" />
                <p className="text-sm text-red-300">{error}</p>
              </motion.div>
            )}
          </AnimatePresence>

          {/* Form */}
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-muted-foreground mb-1.5">
                Email
              </label>
              <div className="relative">
                <Mail className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
                <input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="you@example.com"
                  className="input pl-10"
                  required
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-muted-foreground mb-1.5">
                Password
              </label>
              <div className="relative">
                <Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
                <input
                  type="password"
                  value={password}
                  onChange={handlePasswordChange}
                  placeholder="••••••••"
                  className="input pl-10"
                  required
                />
              </div>
              {password && (
                <div className="mt-2">
                  <div className="flex gap-1 h-1">
                    {[1, 2, 3, 4].map((i) => (
                      <div
                        key={i}
                        className={`flex-1 rounded-full transition-all ${
                          i <= passwordStrength
                            ? strengthColors[passwordStrength]
                            : "bg-muted"
                        }`}
                      />
                    ))}
                  </div>
                  <p className="text-xs text-muted-foreground mt-1.5">
                    Strength:{" "}
                    <span
                      className={
                        passwordStrength <= 1
                          ? "text-red-400"
                          : passwordStrength <= 2
                            ? "text-yellow-400"
                            : passwordStrength <= 3
                              ? "text-blue-400"
                              : "text-green-400"
                      }
                    >
                      {strengthLabels[passwordStrength]}
                    </span>
                  </p>
                </div>
              )}
            </div>

            <div>
              <label className="block text-sm font-medium text-muted-foreground mb-1.5">
                Confirm Password
              </label>
              <div className="relative">
                <Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
                <input
                  type="password"
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                  placeholder="••••••••"
                  className="input pl-10"
                  required
                />
              </div>
              {confirmPassword && password === confirmPassword && (
                <div className="flex items-center gap-1.5 text-green-400 text-xs mt-1.5">
                  <CheckCircle className="w-3 h-3" />
                  Passwords match
                </div>
              )}
            </div>

            <motion.button
              type="submit"
              disabled={isLoading || password !== confirmPassword}
              className="btn-primary w-full"
              whileHover={{ scale: 1.01 }}
              whileTap={{ scale: 0.99 }}
            >
              {isLoading ? (
                <span className="flex items-center justify-center gap-2">
                  <svg className="animate-spin w-4 h-4" viewBox="0 0 24 24">
                    <circle
                      className="opacity-25"
                      cx="12"
                      cy="12"
                      r="10"
                      stroke="currentColor"
                      strokeWidth="4"
                      fill="none"
                    />
                    <path
                      className="opacity-75"
                      fill="currentColor"
                      d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"
                    />
                  </svg>
                  Creating...
                </span>
              ) : (
                <span className="flex items-center justify-center gap-2">
                  Create account
                  <ArrowRight className="w-4 h-4" />
                </span>
              )}
            </motion.button>
          </form>

          <div className="mt-5 text-center">
            <p className="text-xs text-muted-foreground">
              By signing up, you agree to our{" "}
              <a href="#" className="text-foreground hover:underline">
                Terms
              </a>{" "}
              and{" "}
              <a href="#" className="text-foreground hover:underline">
                Privacy
              </a>
            </p>
          </div>

          <div className="mt-5 text-center">
            <p className="text-sm text-muted-foreground">
              Already have an account?{" "}
              <Link
                to="/login"
                className="text-foreground hover:text-primary font-medium transition-colors"
              >
                Sign in
              </Link>
            </p>
          </div>
        </motion.div>
      </div>
    </div>
  );
}
