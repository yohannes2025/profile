// frontend/src/components/Hero.tsx
import { motion } from "framer-motion";
import { ArrowRight, Github, Linkedin, X, Instagram, Mail } from "lucide-react";
import { useTranslation } from "react-i18next";
import { useEffect } from "react";

export default function Hero() {
  const { t, i18n } = useTranslation();

  // Force re-render when language changes
  useEffect(() => {
    console.log("Hero - Language changed to:", i18n.language);
  }, [i18n.language]);

  // Get the correct button text based on language
  const getContactButtonText = () => {
    return i18n.language === "de" ? "Kontaktieren Sie mich" : "Contact Me";
  };

  return (
    <section id="home" className="min-h-screen flex items-center pt-16">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
        <div className="grid lg:grid-cols-2 gap-12 items-center">
          {/* Left Content */}
          <motion.div
            initial={{ opacity: 0, x: -50 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6 }}
          >
            <motion.p
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2 }}
              className="text-cyan-500 dark:text-cyan-400 font-semibold mb-4"
            >
              {t("hero.title")}
            </motion.p>

            <motion.h1
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.3 }}
              className="text-5xl sm:text-6xl lg:text-7xl font-bold mb-6 text-slate-900 dark:text-white"
            >
              {t("hero.heading")}
              <span className="text-cyan-500 dark:text-cyan-400">
                {" "}
                {t("hero.headingHighlight")}
              </span>
            </motion.h1>

            <motion.p
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.4 }}
              className="text-lg text-slate-600 dark:text-slate-400 mb-8 max-w-lg"
            >
              {t("hero.description")}
            </motion.p>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.5 }}
              className="flex flex-wrap gap-4 mb-8"
            >
              <motion.a
                href="#projects"
                className="px-6 py-3 bg-cyan-500 hover:bg-cyan-600 text-white rounded-xl font-medium transition-colors flex items-center gap-2"
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
              >
                {t("hero.viewProjects")} <ArrowRight size={18} />
              </motion.a>

              {/* Contact Me button with conditional text */}
              <motion.a
                href="#contact"
                className="px-6 py-3 bg-cyan-500 hover:bg-cyan-600 text-white rounded-xl font-medium transition-colors flex items-center gap-2"
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
              >
                {getContactButtonText()} <Mail size={18} />
              </motion.a>
            </motion.div>

            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.6 }}
              className="flex gap-4"
            >
              <a
                href="https://www.github.com/yohannes2025"
                target="_blank"
                rel="noopener noreferrer"
                className="p-2 rounded-full bg-slate-100 dark:bg-slate-800 hover:bg-cyan-100 dark:hover:bg-cyan-900 transition-colors"
              >
                <Github size={24} />
              </a>
              <a
                href="https://www.linkedin.com/in/yohannes-mebrahtu-tekle-98a01322a/"
                target="_blank"
                rel="noopener noreferrer"
                className="p-2 rounded-full bg-slate-100 dark:bg-slate-800 hover:bg-cyan-100 dark:hover:bg-cyan-900 transition-colors"
              >
                <Linkedin size={24} />
              </a>
              <a
                href="https://www.x.com/YohannesMT2025"
                target="_blank"
                rel="noopener noreferrer"
                className="p-2 rounded-full bg-slate-100 dark:bg-slate-800 hover:bg-cyan-100 dark:hover:bg-cyan-900 transition-colors"
              >
                <X size={24} />
              </a>
              <a
                href="https://www.instagram.com/yohannes.mebrahtu.5"
                target="_blank"
                rel="noopener noreferrer"
                className="p-2 rounded-full bg-slate-100 dark:bg-slate-800 hover:bg-cyan-100 dark:hover:bg-cyan-900 transition-colors"
              >
                <Instagram size={24} />
              </a>
            </motion.div>
          </motion.div>

          {/* Right Content - Professional Image */}
          <motion.div
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.6, delay: 0.2 }}
            className="relative flex justify-center"
          >
            <div className="relative w-80 h-80">
              <motion.div
                className="absolute inset-0 rounded-full bg-gradient-to-r from-cyan-400 to-blue-500 opacity-75"
                animate={{
                  scale: [1, 1.1, 1],
                  rotate: [0, 360],
                }}
                transition={{
                  duration: 8,
                  repeat: Infinity,
                  ease: "linear",
                }}
              />

              <div className="absolute inset-2 rounded-full overflow-hidden bg-gradient-to-br from-slate-700 to-slate-900 shadow-xl">
                <img
                  src="https://res.cloudinary.com/di2vmvljd/image/upload/v1782530163/profile_xyldtt.png"
                  alt="Yohannes Tekle - Full Stack Developer"
                  className="w-full h-full object-cover"
                  onError={(e) => {
                    e.currentTarget.src =
                      "https://ui-avatars.com/api/?background=0D9488&color=fff&size=300&name=Yohannes&font-size=0.5&rounded=true&bold=true&length=2";
                  }}
                />
              </div>

              <motion.div
                className="absolute -top-4 -right-4 bg-white dark:bg-slate-800 rounded-full px-4 py-2 shadow-lg z-10"
                animate={{ y: [0, -10, 0] }}
                transition={{ duration: 3, repeat: Infinity }}
              >
                <span className="text-sm font-semibold text-slate-800 dark:text-white">
                  ⚛️ {t("hero.reactExpert")}
                </span>
              </motion.div>

              <motion.div
                className="absolute -bottom-4 -left-4 bg-white dark:bg-slate-800 rounded-full px-4 py-2 shadow-lg z-10"
                animate={{ y: [0, 10, 0] }}
                transition={{ duration: 3, repeat: Infinity, delay: 1 }}
              >
                <span className="text-sm font-semibold text-slate-800 dark:text-white">
                  🐍 {t("hero.djangoPro")}
                </span>
              </motion.div>

              <motion.div
                className="absolute -top-2 -left-6 bg-cyan-500 rounded-full px-3 py-1 shadow-lg z-10"
                animate={{ x: [0, -5, 0] }}
                transition={{ duration: 2, repeat: Infinity, delay: 0.5 }}
              >
                <span className="text-xs font-semibold text-white">
                  💼 {t("hero.yearsExp")}
                </span>
              </motion.div>

              <motion.div
                className="absolute -bottom-2 -right-6 bg-green-500 rounded-full px-3 py-1 shadow-lg z-10"
                animate={{ x: [0, 5, 0] }}
                transition={{ duration: 2, repeat: Infinity, delay: 1.5 }}
              >
                <span className="text-xs font-semibold text-white">
                  ✅ {t("hero.available")}
                </span>
              </motion.div>
            </div>
          </motion.div>
        </div>
      </div>
    </section>
  );
}
