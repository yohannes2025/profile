// frontend/src/components/Projects.tsx
import { useState } from "react";
import { motion } from "framer-motion";
import { useInView } from "react-intersection-observer";
import { useQuery } from "@tanstack/react-query";
import { useTranslation } from "react-i18next";
import { fetchProjects } from "../services/api";
import { Github, ExternalLink, Code2 } from "lucide-react";
import ProjectModal from "./ProjectModal";

export default function Projects() {
  const { t } = useTranslation();
  const { ref, inView } = useInView({ threshold: 0.1, triggerOnce: true });

  // Modal tracking states
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedProject, setSelectedProject] = useState<any>(null);

  const {
    data: projects,
    isLoading,
    error,
  } = useQuery({
    queryKey: ["projects"],
    queryFn: fetchProjects,
  });

  // Unpacking the Django REST Framework pagination 'results' wrapper
  const projectsArray = Array.isArray(projects)
    ? projects
    : projects?.results || [];

  return (
    <section id="projects" className="py-24">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Title Section - Always visible */}
        <motion.div
          ref={ref}
          initial={{ opacity: 0, y: 20 }}
          animate={inView ? { opacity: 1, y: 0 } : {}}
          transition={{ duration: 0.6 }}
          className="text-center mb-12"
        >
          <h2 className="text-4xl font-bold mb-4 text-slate-900 dark:text-white">
            {t("projects.title")}
          </h2>
          <p className="text-slate-600 dark:text-slate-400 max-w-2xl mx-auto">
            {t("projects.subtitle")}
          </p>
        </motion.div>

        {/* Content Section */}
        {isLoading ? (
          // Loading skeleton
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {[1, 2, 3].map((i) => (
              <div
                key={i}
                className="h-96 bg-slate-200 dark:bg-slate-700 rounded-2xl animate-pulse"
              ></div>
            ))}
          </div>
        ) : error ? (
          // Error state
          <div className="text-center py-12 bg-white dark:bg-slate-800 rounded-2xl shadow-lg">
            <div className="text-6xl mb-4">⚠️</div>
            <h3 className="text-xl font-semibold mb-2 text-slate-900 dark:text-white">
              {t("projects.error")}
            </h3>
            <p className="text-slate-600 dark:text-slate-400">
              {t("projects.errorText") || "Please try again later."}
            </p>
          </div>
        ) : projectsArray.length === 0 ? (
          // Empty state - No projects
          <div className="text-center py-12 bg-white dark:bg-slate-800 rounded-2xl shadow-lg">
            <div className="text-6xl mb-4">📁</div>
            <h3 className="text-xl font-semibold mb-2 text-slate-900 dark:text-white">
              {t("projects.noProjects")}
            </h3>
            <p className="text-slate-600 dark:text-slate-400">
              {t("projects.noProjectsText") ||
                "Check back soon for new projects!"}
            </p>
          </div>
        ) : (
          // Projects grid
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {projectsArray.map((project: any, index: number) => (
              <motion.div
                key={project.id || index}
                initial={{ opacity: 0, y: 30 }}
                animate={inView ? { opacity: 1, y: 0 } : {}}
                transition={{ duration: 0.5, delay: index * 0.1 }}
                whileHover={{ y: -8 }}
                className="group bg-white dark:bg-slate-800 rounded-2xl overflow-hidden shadow-lg hover:shadow-2xl transition-all duration-300"
              >
                <div className="relative h-48 overflow-hidden">
                  <img
                    src={
                      project.image ||
                      `https://picsum.photos/seed/${project.id || index}/400/300`
                    }
                    alt={project.title}
                    className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500"
                  />
                  <div className="absolute inset-0 bg-gradient-to-t from-black/50 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
                </div>

                <div className="p-6">
                  <h3 className="text-xl font-semibold mb-2 text-slate-900 dark:text-white">
                    {project.title}
                  </h3>
                  <p className="text-slate-600 dark:text-slate-400 mb-4 line-clamp-2">
                    {project.description}
                  </p>

                  <div className="flex flex-wrap gap-2 mb-4">
                    {project.technologies?.slice(0, 4).map((tech: string) => (
                      <span
                        key={tech}
                        className="px-2 py-1 text-xs rounded-full bg-cyan-100 dark:bg-cyan-900/30 text-cyan-600 dark:text-cyan-400"
                      >
                        {tech}
                      </span>
                    ))}
                  </div>

                  <div className="flex gap-3">
                    {project.github_link && (
                      <a
                        href={project.github_link}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="p-2 rounded-lg bg-slate-100 dark:bg-slate-700 hover:bg-cyan-100 dark:hover:bg-cyan-900 transition-colors"
                        title={t("projects.github")}
                      >
                        <Github size={18} />
                      </a>
                    )}
                    {project.live_demo && (
                      <a
                        href={project.live_demo}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="p-2 rounded-lg bg-slate-100 dark:bg-slate-700 hover:bg-cyan-100 dark:hover:bg-cyan-900 transition-colors"
                        title={t("projects.liveDemo")}
                      >
                        <ExternalLink size={18} />
                      </a>
                    )}
                    <button
                      onClick={() => {
                        setSelectedProject(project);
                        setIsModalOpen(true);
                      }}
                      className="p-2 rounded-lg bg-slate-100 dark:bg-slate-700 hover:bg-cyan-100 dark:hover:bg-cyan-900 transition-colors"
                      title={t("projects.details")}
                    >
                      <Code2 size={18} />
                    </button>
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
        )}
      </div>

      {/* Global Project Modal Anchor Point */}
      {selectedProject && (
        <ProjectModal
          project={selectedProject}
          isOpen={isModalOpen}
          onClose={() => {
            setIsModalOpen(false);
            setSelectedProject(null);
          }}
          t={t}
        />
      )}
    </section>
  );
}
