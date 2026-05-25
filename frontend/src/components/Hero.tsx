// frontend/src/components/Hero.tsx
import { motion } from "framer-motion";
import { Download, ArrowRight, Github, Linkedin, Mail } from "lucide-react";

export default function Hero() {
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
              Full-Stack Developer
            </motion.p>

            <motion.h1
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.3 }}
              className="text-5xl sm:text-6xl lg:text-7xl font-bold mb-6 text-slate-900 dark:text-white"
            >
              Building modern
              <span className="text-cyan-500 dark:text-cyan-400">
                {" "}
                web experiences
              </span>
            </motion.h1>

            <motion.p
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.4 }}
              className="text-lg text-slate-600 dark:text-slate-400 mb-8 max-w-lg"
            >
              I design and develop scalable full-stack applications using React,
              Django, and modern web technologies. Focused on creating clean,
              responsive, and user-friendly digital experiences.
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
                View Projects <ArrowRight size={18} />
              </motion.a>

              <motion.a
                href="/resume.pdf"
                download
                className="px-6 py-3 border border-slate-300 dark:border-slate-700 rounded-xl font-medium hover:border-cyan-500 hover:text-cyan-500 transition-colors flex items-center gap-2"
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
              >
                Download CV <Download size={18} />
              </motion.a>
            </motion.div>

            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.6 }}
              className="flex gap-4"
            >
              <a
                href="https://github.com/yohannes"
                target="_blank"
                rel="noopener noreferrer"
                className="p-2 rounded-full bg-slate-100 dark:bg-slate-800 hover:bg-cyan-100 dark:hover:bg-cyan-900 transition-colors"
              >
                <Github size={24} />
              </a>
              <a
                href="https://linkedin.com/in/yohannes"
                target="_blank"
                rel="noopener noreferrer"
                className="p-2 rounded-full bg-slate-100 dark:bg-slate-800 hover:bg-cyan-100 dark:hover:bg-cyan-900 transition-colors"
              >
                <Linkedin size={24} />
              </a>
              <a
                href="mailto:yohannes.m.tekle@gmail.com"
                className="p-2 rounded-full bg-slate-100 dark:bg-slate-800 hover:bg-cyan-100 dark:hover:bg-cyan-900 transition-colors"
              >
                <Mail size={24} />
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
              {/* Animated Gradient Ring */}
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

              {/* Professional Avatar Image */}
              <div className="absolute inset-2 rounded-full overflow-hidden bg-gradient-to-br from-slate-700 to-slate-900">
                {/* Professional placeholder image - replace with your actual photo */}
                <img
                  src="https://ui-avatars.com/api/?background=0D9488&color=fff&size=300&name=Yohannes&font-size=0.5&rounded=true&bold=true&length=2"
                  alt="Yohannes Tekle"
                  className="w-full h-full object-cover"
                />
              </div>

              {/* Floating Badge - React Expert */}
              <motion.div
                className="absolute -top-4 -right-4 bg-white dark:bg-slate-800 rounded-full px-4 py-2 shadow-lg z-10"
                animate={{ y: [0, -10, 0] }}
                transition={{ duration: 3, repeat: Infinity }}
              >
                <span className="text-sm font-semibold text-slate-800 dark:text-white">
                  ⚛️ React Expert
                </span>
              </motion.div>

              {/* Floating Badge - Django Pro */}
              <motion.div
                className="absolute -bottom-4 -left-4 bg-white dark:bg-slate-800 rounded-full px-4 py-2 shadow-lg z-10"
                animate={{ y: [0, 10, 0] }}
                transition={{ duration: 3, repeat: Infinity, delay: 1 }}
              >
                <span className="text-sm font-semibold text-slate-800 dark:text-white">
                  🐍 Django Pro
                </span>
              </motion.div>

              {/* Floating Badge - 5+ Years Experience */}
              <motion.div
                className="absolute -top-2 -left-6 bg-cyan-500 rounded-full px-3 py-1 shadow-lg z-10"
                animate={{ x: [0, -5, 0] }}
                transition={{ duration: 2, repeat: Infinity, delay: 0.5 }}
              >
                <span className="text-xs font-semibold text-white">
                  5+ Years
                </span>
              </motion.div>

              {/* Floating Badge - Available */}
              <motion.div
                className="absolute -bottom-2 -right-6 bg-green-500 rounded-full px-3 py-1 shadow-lg z-10"
                animate={{ x: [0, 5, 0] }}
                transition={{ duration: 2, repeat: Infinity, delay: 1.5 }}
              >
                <span className="text-xs font-semibold text-white">
                  Available
                </span>
              </motion.div>
            </div>
          </motion.div>
        </div>
      </div>
    </section>
  );
}
