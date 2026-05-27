// frontend/src/components/Testimonials.tsx
import { motion } from "framer-motion";
import { Star, Quote } from "lucide-react";
import { useQuery } from "@tanstack/react-query";
import { useTranslation } from "react-i18next";
import { fetchTestimonials } from "../services/api";

export default function Testimonials() {
  const { t } = useTranslation();
  const { data: testimonials, isLoading } = useQuery({
    queryKey: ["testimonials"],
    queryFn: fetchTestimonials,
  });

  if (isLoading) {
    return (
      <section id="testimonials" className="py-24">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="animate-pulse">
            <div className="h-8 bg-slate-200 dark:bg-slate-700 rounded w-48 mx-auto mb-4"></div>
            <div className="h-4 bg-slate-200 dark:bg-slate-700 rounded w-96 mx-auto"></div>
          </div>
        </div>
      </section>
    );
  }

  const testimonialsArray = Array.isArray(testimonials) ? testimonials : [];

  return (
    <section
      id="testimonials"
      className="py-24 bg-gradient-to-br from-cyan-50 to-blue-50 dark:from-cyan-950/20 dark:to-blue-950/20"
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          viewport={{ once: true }}
          className="text-center mb-12"
        >
          <h2 className="text-4xl font-bold mb-4 text-slate-900 dark:text-white">
            {t("testimonials.title")}
          </h2>
          <p className="text-slate-600 dark:text-slate-400 max-w-2xl mx-auto">
            {t("testimonials.subtitle")}
          </p>
        </motion.div>

        {testimonialsArray.length === 0 ? (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="text-center py-12 bg-white dark:bg-slate-800 rounded-2xl shadow-lg"
          >
            <div className="text-6xl mb-4">⭐</div>
            <h3 className="text-2xl font-semibold mb-2 text-slate-900 dark:text-white">
              {t("testimonials.noTestimonials")}
            </h3>
            <p className="text-slate-600 dark:text-slate-400">
              {t("testimonials.noTestimonialsText")}
            </p>
          </motion.div>
        ) : (
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {testimonialsArray.map((testimonial: any, index: number) => (
              <motion.div
                key={testimonial.id}
                initial={{ opacity: 0, scale: 0.9 }}
                whileInView={{ opacity: 1, scale: 1 }}
                transition={{ delay: index * 0.1 }}
                viewport={{ once: true }}
                className="bg-white dark:bg-slate-800 rounded-2xl p-6 shadow-lg relative"
              >
                <Quote className="absolute top-6 right-6 text-cyan-200 dark:text-cyan-800 w-12 h-12" />
                <div className="flex items-center gap-4 mb-4">
                  {testimonial.image ? (
                    <img
                      src={testimonial.image}
                      alt={testimonial.name}
                      className="w-16 h-16 rounded-full object-cover"
                    />
                  ) : (
                    <div className="w-16 h-16 rounded-full bg-gradient-to-r from-cyan-400 to-blue-500 flex items-center justify-center text-white text-xl font-bold">
                      {testimonial.name?.charAt(0) || "?"}
                    </div>
                  )}
                  <div>
                    <h4 className="font-semibold text-lg text-slate-900 dark:text-white">
                      {testimonial.name}
                    </h4>
                    <p className="text-sm text-slate-500 dark:text-slate-400">
                      {testimonial.position}{" "}
                      {testimonial.company &&
                        `${t("testimonials.at")} ${testimonial.company}`}
                    </p>
                  </div>
                </div>
                <div className="flex mb-3">
                  {[...Array(5)].map((_, i) => (
                    <Star
                      key={i}
                      size={16}
                      className={
                        i < (testimonial.rating || 5)
                          ? "text-yellow-400 fill-yellow-400"
                          : "text-gray-300 dark:text-gray-600"
                      }
                    />
                  ))}
                </div>
                <p className="text-slate-600 dark:text-slate-300 italic">
                  "{testimonial.feedback}"
                </p>
              </motion.div>
            ))}
          </div>
        )}
      </div>
    </section>
  );
}
