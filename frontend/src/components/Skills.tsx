// src/components/Skills.tsx
import { motion } from "framer-motion";
import { useInView } from "react-intersection-observer";
import { useQuery } from "@tanstack/react-query";
import { useTranslation } from "react-i18next";
import { fetchSkills } from "../services/api";
import { Code, Database, Cloud, Wrench } from "lucide-react";

const categoryIcons: Record<string, React.ReactNode> = {
  frontend: <Code size={24} />,
  backend: <Code size={24} />,
  database: <Database size={24} />,
  devops: <Cloud size={24} />,
  tools: <Wrench size={24} />,
};

const categoryColors: Record<string, string> = {
  frontend: "from-rose-500 to-pink-500",
  backend: "from-blue-500 to-cyan-500",
  database: "from-emerald-500 to-teal-500",
  devops: "from-orange-500 to-red-500",
  tools: "from-purple-500 to-indigo-500",
};

export default function Skills() {
  const { t } = useTranslation();
  const { ref, inView } = useInView({ threshold: 0.1, triggerOnce: true });
  const { data: skills, isLoading } = useQuery({
    queryKey: ["skills"],
    queryFn: fetchSkills,
  });

  if (isLoading) {
    return (
      <div className="py-24 bg-slate-50 dark:bg-slate-900/50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="animate-pulse">
            <div className="h-8 bg-slate-200 dark:bg-slate-700 rounded w-48 mx-auto mb-12"></div>
          </div>
        </div>
      </div>
    );
  }

  const groupedSkills = skills?.reduce((acc: any, skill: any) => {
    if (!acc[skill.category]) acc[skill.category] = [];
    acc[skill.category].push(skill);
    return acc;
  }, {});

  const categoryNames: Record<string, string> = {
    frontend: t("skills.frontend"),
    backend: t("skills.backend"),
    database: t("skills.database"),
    devops: t("skills.devops"),
    tools: t("skills.tools"),
  };

  return (
    <section id="skills" className="py-24 bg-slate-50 dark:bg-slate-900/50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={inView ? { opacity: 1, y: 0 } : {}}
          transition={{ duration: 0.6 }}
          className="text-center mb-12"
        >
          <h2 className="text-4xl font-bold mb-4 text-slate-900 dark:text-white">
            {t("skills.title")}
          </h2>
          <p className="text-slate-600 dark:text-slate-400 max-w-2xl mx-auto">
            {t("skills.subtitle")}
          </p>
        </motion.div>

        <div ref={ref} className="space-y-12">
          {Object.entries(groupedSkills || {}).map(
            ([category, categorySkills]: [string, any]) => (
              <motion.div
                key={category}
                initial={{ opacity: 0, y: 30 }}
                animate={inView ? { opacity: 1, y: 0 } : {}}
                transition={{ duration: 0.5 }}
                className="bg-white dark:bg-slate-800 rounded-2xl p-6 shadow-lg"
              >
                <div className="flex items-center gap-3 mb-6">
                  <div
                    className={`p-2 rounded-lg bg-gradient-to-r ${categoryColors[category] || "from-gray-500 to-gray-600"} text-white`}
                  >
                    {categoryIcons[category] || <Code size={24} />}
                  </div>
                  <h3 className="text-2xl font-semibold text-slate-900 dark:text-white capitalize">
                    {categoryNames[category] || category}
                  </h3>
                </div>

                <div className="grid md:grid-cols-2 gap-6">
                  {categorySkills.map((skill: any, index: number) => (
                    <motion.div
                      key={skill.id}
                      initial={{ opacity: 0, x: -20 }}
                      animate={inView ? { opacity: 1, x: 0 } : {}}
                      transition={{ delay: index * 0.1 }}
                    >
                      <div className="flex justify-between mb-2">
                        <span className="font-medium text-slate-700 dark:text-slate-300">
                          {skill.name}
                        </span>
                        <span className="text-cyan-500">
                          {skill.proficiency}%
                        </span>
                      </div>
                      <div className="h-2 bg-slate-200 dark:bg-slate-700 rounded-full overflow-hidden">
                        <motion.div
                          initial={{ width: 0 }}
                          animate={
                            inView ? { width: `${skill.proficiency}%` } : {}
                          }
                          transition={{ duration: 1, delay: index * 0.1 }}
                          className={`h-full rounded-full bg-gradient-to-r ${categoryColors[skill.category] || "from-gray-500 to-gray-600"}`}
                        />
                      </div>
                    </motion.div>
                  ))}
                </div>
              </motion.div>
            ),
          )}
        </div>
      </div>
    </section>
  );
}
