// frontend/src/components/ProjectModal.tsx
import { motion, AnimatePresence } from "framer-motion";
import {
  X,
  Github,
  ExternalLink,
  Calendar,
  Folder,
  Star,
  Users,
} from "lucide-react";
import { useEffect } from "react";

interface ProjectModalProps {
  project: {
    id: number;
    title: string;
    description: string;
    image?: string;
    img?: string;
    technologies: string[];
    tags?: string[];
    github_link?: string;
    live_demo?: string;
    liveUrl?: string;
    created_at?: string;
    updated_at?: string;
    featured?: boolean;
    category?: string;
    stars?: number;
  };
  isOpen: boolean;
  onClose: () => void;
  t: (key: string) => string;
}

export default function ProjectModal({
  project,
  isOpen,
  onClose,
  t,
}: ProjectModalProps) {
  // Close on escape key
  useEffect(() => {
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === "Escape") onClose();
    };
    if (isOpen) {
      document.addEventListener("keydown", handleEscape);
      document.body.style.overflow = "hidden";
    }
    return () => {
      document.removeEventListener("keydown", handleEscape);
      document.body.style.overflow = "unset";
    };
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  const technologies = project.technologies || project.tags || [];
  const imageUrl =
    project.image ||
    project.img ||
    `https://picsum.photos/seed/${project.id}/800/400`;
  const liveUrl = project.live_demo || project.liveUrl;
  const githubUrl = project.github_link;

  return (
    <AnimatePresence>
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70 backdrop-blur-sm"
        onClick={onClose}
      >
        <motion.div
          initial={{ scale: 0.9, opacity: 0, y: 20 }}
          animate={{ scale: 1, opacity: 1, y: 0 }}
          exit={{ scale: 0.9, opacity: 0, y: 20 }}
          transition={{ type: "spring", damping: 25 }}
          className="bg-white dark:bg-slate-800 rounded-2xl max-w-3xl w-full max-h-[90vh] overflow-y-auto"
          onClick={(e) => e.stopPropagation()}
        >
          {/* Header with close button */}
          <div className="sticky top-0 z-10 bg-white dark:bg-slate-800 border-b border-slate-200 dark:border-slate-700 p-4 flex justify-between items-start">
            <div className="flex items-center gap-3 flex-wrap">
              <h2 className="text-2xl font-bold text-slate-900 dark:text-white">
                {project.title}
              </h2>
              {project.featured && (
                <span className="flex items-center gap-1 text-xs font-semibold bg-gradient-to-r from-cyan-500 to-blue-500 text-white px-3 py-1 rounded-full">
                  <Star size={12} fill="currentColor" />
                  Featured
                </span>
              )}
            </div>
            <button
              onClick={onClose}
              className="p-2 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-700 transition-colors flex-shrink-0"
              aria-label="Close modal"
            >
              <X size={24} className="text-slate-600 dark:text-slate-400" />
            </button>
          </div>

          <div className="p-6">
            {/* Project Image */}
            <div className="mb-6 rounded-xl overflow-hidden">
              <img
                src={imageUrl}
                alt={project.title}
                className="w-full h-64 object-cover"
                loading="lazy"
              />
            </div>

            {/* Description */}
            <p className="text-slate-600 dark:text-slate-400 mb-6 leading-relaxed">
              {project.description}
            </p>

            {/* Technologies - Using existing translation key */}
            {technologies.length > 0 && (
              <div className="mb-6">
                <h4 className="font-semibold mb-3 text-slate-900 dark:text-white flex items-center gap-2">
                  <Folder size={18} className="text-cyan-500" />
                  {t("skills.title")}
                </h4>
                <div className="flex flex-wrap gap-2">
                  {technologies.map((tech: string) => (
                    <span
                      key={tech}
                      className="px-3 py-1.5 rounded-full bg-cyan-100 dark:bg-cyan-900/30 text-cyan-600 dark:text-cyan-400 text-sm font-medium"
                    >
                      {tech}
                    </span>
                  ))}
                </div>
              </div>
            )}

            {/* Metadata */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-6">
              {project.created_at && (
                <div className="flex items-center gap-2 text-sm text-slate-600 dark:text-slate-400 bg-slate-50 dark:bg-slate-700/50 p-3 rounded-lg">
                  <Calendar size={16} className="text-cyan-500" />
                  <span>
                    Completed:{" "}
                    {new Date(project.created_at).toLocaleDateString()}
                  </span>
                </div>
              )}
              {project.category && (
                <div className="flex items-center gap-2 text-sm text-slate-600 dark:text-slate-400 bg-slate-50 dark:bg-slate-700/50 p-3 rounded-lg">
                  <Users size={16} className="text-cyan-500" />
                  <span>Category: {project.category}</span>
                </div>
              )}
            </div>

            {/* Action Buttons */}
            <div className="flex flex-wrap gap-4 pt-4 border-t border-slate-200 dark:border-slate-700">
              {githubUrl && (
                <a
                  href={githubUrl}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex items-center gap-2 px-4 py-2 bg-slate-100 dark:bg-slate-700 text-slate-700 dark:text-slate-300 rounded-lg hover:bg-cyan-100 dark:hover:bg-cyan-900 transition-all duration-200"
                >
                  <Github size={18} />
                  {t("projects.github")}
                </a>
              )}
              {liveUrl && (
                <a
                  href={liveUrl}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-cyan-500 to-blue-500 text-white rounded-lg hover:from-cyan-600 hover:to-blue-600 transition-all duration-200 shadow-md hover:shadow-lg"
                >
                  <ExternalLink size={18} />
                  {t("projects.liveDemo")}
                </a>
              )}
            </div>
          </div>
        </motion.div>
      </motion.div>
    </AnimatePresence>
  );
}
