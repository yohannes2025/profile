import { motion } from "framer-motion";
import {
  Briefcase,
  GraduationCap,
  Award,
  Heart,
  Code,
  Database,
  Cloud,
} from "lucide-react";
import { useQuery } from "@tanstack/react-query";
import { fetchExperiences, fetchEducation } from "../services/api";

export default function About() {
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
    { icon: Code, label: "Projects Completed", value: "10+" },
    { icon: Database, label: "Databases", value: "5+" },
    { icon: Cloud, label: "Cloud Deployments", value: "8+" },
    { icon: Award, label: "Certifications", value: "3" },
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
          <h2 className="text-4xl font-bold mb-4">About Me</h2>
          <p className="text-slate-600 dark:text-slate-400 max-w-2xl mx-auto">
            Get to know me better - my background, experience, and what drives
            me
          </p>
        </motion.div>

        <div className="grid lg:grid-cols-2 gap-12">
          {/* Left Column - Bio */}
          <motion.div
            initial={{ opacity: 0, x: -30 }}
            whileInView={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6 }}
            className="space-y-6"
          >
            <div>
              <h3 className="text-2xl font-semibold mb-4">Who Am I?</h3>
              <p className="text-slate-600 dark:text-slate-400 leading-relaxed">
                I'm a passionate full-stack developer with expertise in building
                modern, scalable web applications. I love solving complex
                problems and creating digital experiences that make a
                difference.
              </p>
            </div>

            <div>
              <h3 className="text-2xl font-semibold mb-4 flex items-center gap-2">
                <Briefcase className="text-cyan-500" /> Work Experience
              </h3>
              <div className="space-y-4">
                {experiences?.map((exp: any) => (
                  <div key={exp.id} className="border-l-4 border-cyan-500 pl-4">
                    <h4 className="font-semibold">{exp.title}</h4>
                    <p className="text-cyan-500">{exp.company}</p>
                    <p className="text-sm text-slate-500 dark:text-slate-400">
                      {exp.start_date} -{" "}
                      {exp.current ? "Present" : exp.end_date}
                    </p>
                    <p className="mt-2 text-slate-600 dark:text-slate-400 text-sm">
                      {exp.description}
                    </p>
                  </div>
                ))}
              </div>
            </div>
          </motion.div>

          {/* Right Column - Education & Stats */}
          <motion.div
            initial={{ opacity: 0, x: 30 }}
            whileInView={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6 }}
            className="space-y-6"
          >
            <div>
              <h3 className="text-2xl font-semibold mb-4 flex items-center gap-2">
                <GraduationCap className="text-cyan-500" /> Education
              </h3>
              <div className="space-y-4">
                {education?.map((edu: any) => (
                  <div key={edu.id} className="border-l-4 border-cyan-500 pl-4">
                    <h4 className="font-semibold">{edu.degree}</h4>
                    <p className="text-cyan-500">{edu.institution}</p>
                    <p className="text-sm text-slate-500 dark:text-slate-400">
                      {edu.start_year} - {edu.end_year}
                    </p>
                    {edu.description && (
                      <p className="mt-2 text-slate-600 dark:text-slate-400 text-sm">
                        {edu.description}
                      </p>
                    )}
                  </div>
                ))}
              </div>
            </div>

            {/* Stats Grid */}
            <div>
              <h3 className="text-2xl font-semibold mb-4">Quick Stats</h3>
              <div className="grid grid-cols-2 gap-4">
                {stats.map((stat, index) => (
                  <div
                    key={index}
                    className="bg-gradient-to-br from-cyan-50 to-blue-50 dark:from-cyan-950/20 dark:to-blue-950/20 rounded-xl p-4 text-center"
                  >
                    <stat.icon className="w-8 h-8 text-cyan-500 mx-auto mb-2" />
                    <div className="text-2xl font-bold">{stat.value}</div>
                    <div className="text-sm text-slate-600 dark:text-slate-400">
                      {stat.label}
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Passion Statement */}
            <div className="bg-gradient-to-r from-cyan-500 to-blue-500 rounded-2xl p-6 text-white">
              <Heart className="w-8 h-8 mb-2" />
              <h3 className="text-xl font-semibold mb-2">My Passion</h3>
              <p className="opacity-90">
                I'm passionate about creating technology that helps people and
                makes the web a better place.
              </p>
            </div>
          </motion.div>
        </div>
      </div>
    </section>
  );
}
