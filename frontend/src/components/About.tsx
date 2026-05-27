// src/components/About.tsx
import { motion } from "framer-motion";
import { Award, Heart, Code, Database, Cloud } from "lucide-react";
import { useQuery } from "@tanstack/react-query";
import { useTranslation } from "react-i18next";
import { fetchExperiences, fetchEducation } from "../services/api";

export default function About() {
  const { t } = useTranslation();
  const { data: experiences, isLoading: expLoading } = useQuery({
    queryKey: ["experiences"],
    queryFn: fetchExperiences,
  });

  const { data: education, isLoading: eduLoading } = useQuery({
    queryKey: ["education"],
    queryFn: fetchEducation,
  });

  if (expLoading || eduLoading) {
    return (
      <section id="about" className="py-24">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="animate-pulse">
            <div className="h-8 bg-slate-200 dark:bg-slate-700 rounded w-48 mx-auto mb-4"></div>
            <div className="h-4 bg-slate-200 dark:bg-slate-700 rounded w-96 mx-auto"></div>
          </div>
        </div>
      </section>
    );
  }

  const stats = [
    { icon: Code, label: t("about.projectsCompleted"), value: "10+" },
    { icon: Database, label: t("about.databases"), value: "5+" },
    { icon: Cloud, label: t("about.cloudDeployments"), value: "8+" },
    { icon: Award, label: t("about.certifications"), value: "3" },
  ];

  return (
    <section id="about" className="py-24">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="text-center mb-12"
        >
          <h2 className="text-4xl font-bold mb-4 text-slate-900 dark:text-white">
            {t("about.title")}
          </h2>
          <p className="text-slate-600 dark:text-slate-400 max-w-2xl mx-auto">
            {t("about.subtitle")}
          </p>
        </motion.div>

        <div className="grid lg:grid-cols-2 gap-12">
          <motion.div
            initial={{ opacity: 0, x: -30 }}
            whileInView={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6 }}
            className="space-y-6"
          >
            <div>
              <h3 className="text-2xl font-semibold mb-4 text-slate-900 dark:text-white">
                {t("about.workExperience")}
              </h3>
              <div className="space-y-4">
                {experiences?.map((exp: any) => (
                  <div key={exp.id} className="border-l-4 border-cyan-500 pl-4">
                    <h4 className="font-semibold text-slate-900 dark:text-white">
                      {exp.title}
                    </h4>
                    <p className="text-cyan-500">{exp.company}</p>
                    <p className="text-sm text-slate-500 dark:text-slate-400">
                      {exp.start_date} -{" "}
                      {exp.current ? t("about.present") : exp.end_date}
                    </p>
                    <p className="mt-2 text-slate-600 dark:text-slate-400 text-sm">
                      {exp.description}
                    </p>
                  </div>
                ))}
              </div>
            </div>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, x: 30 }}
            whileInView={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6 }}
            className="space-y-6"
          >
            <div>
              <h3 className="text-2xl font-semibold mb-4 text-slate-900 dark:text-white">
                {t("about.education")}
              </h3>
              <div className="space-y-4">
                {education?.map((edu: any) => (
                  <div key={edu.id} className="border-l-4 border-cyan-500 pl-4">
                    <h4 className="font-semibold text-slate-900 dark:text-white">
                      {edu.degree}
                    </h4>
                    <p className="text-cyan-500">{edu.institution}</p>
                    <p className="text-sm text-slate-500 dark:text-slate-400">
                      {edu.start_year} - {edu.end_year}
                    </p>
                  </div>
                ))}
              </div>
            </div>

            <div>
              <h3 className="text-2xl font-semibold mb-4 text-slate-900 dark:text-white">
                {t("about.quickStats")}
              </h3>
              <div className="grid grid-cols-2 gap-4">
                {stats.map((stat, index) => (
                  <div
                    key={index}
                    className="bg-gradient-to-br from-cyan-50 to-blue-50 dark:from-cyan-950/20 dark:to-blue-950/20 rounded-xl p-4 text-center"
                  >
                    <stat.icon className="w-8 h-8 text-cyan-500 mx-auto mb-2" />
                    <div className="text-2xl font-bold text-slate-900 dark:text-white">
                      {stat.value}
                    </div>
                    <div className="text-sm text-slate-600 dark:text-slate-400">
                      {stat.label}
                    </div>
                  </div>
                ))}
              </div>
            </div>

            <div className="bg-gradient-to-r from-cyan-500 to-blue-500 rounded-2xl p-6 text-white">
              <Heart className="w-8 h-8 mb-2" />
              <h3 className="text-xl font-semibold mb-2">
                {t("about.myPassion")}
              </h3>
              <p className="opacity-90">{t("about.passionText")}</p>
            </div>
          </motion.div>
        </div>
      </div>
    </section>
  );
}
