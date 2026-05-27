// src/components/Contact.tsx
import { useState } from "react";
import { motion } from "framer-motion";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { toast } from "react-toastify";
import axios from "axios";
import { Send, Mail, Phone, MapPin } from "lucide-react";
import { useTranslation } from "react-i18next";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000/api";

const contactSchema = z.object({
  name: z.string().min(2, "Name must be at least 2 characters"),
  email: z.string().email("Invalid email address"),
  subject: z.string().min(5, "Subject must be at least 5 characters"),
  message: z.string().min(10, "Message must be at least 10 characters"),
});

type ContactForm = z.infer<typeof contactSchema>;

export default function Contact() {
  const { t, i18n } = useTranslation();
  const [isSubmitting, setIsSubmitting] = useState(false);
  const {
    register,
    handleSubmit,
    reset,
    formState: { errors },
  } = useForm<ContactForm>({
    resolver: zodResolver(contactSchema),
  });

  const onSubmit = async (data: ContactForm) => {
    setIsSubmitting(true);

    try {
      const response = await axios.post(
        `${API_URL}/contact/`,
        {
          name: data.name,
          email: data.email,
          subject: data.subject,
          message: data.message,
        },
        {
          headers: {
            "Content-Type": "application/json",
            "Accept-Language": i18n.language,
          },
        },
      );

      if (response.status === 201) {
        toast.success(t("contact.success"));
        reset();
      }
    } catch (error: any) {
      console.error("Error sending message:", error);
      if (error.response?.data?.error) {
        toast.error(error.response.data.error);
      } else {
        toast.error(t("contact.error"));
      }
    } finally {
      setIsSubmitting(false);
    }
  };

  const contactInfo = [
    {
      icon: Mail,
      label: t("contact.email"),
      value: "yohannes.m.tekle@gmail.com",
      link: "mailto:yohannes.m.tekle@gmail.com",
    },
    {
      icon: Phone,
      label: t("contact.phone"),
      value: "+49 176 45170168",
      link: "tel:+4917645170168",
    },
    {
      icon: MapPin,
      label: t("contact.location"),
      value: i18n.language === "de" ? "Köln, Deutschland" : "Cologne, Germany",
      link: null,
    },
  ];

  return (
    <section id="contact" className="py-24 bg-slate-50 dark:bg-slate-900/50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="text-center mb-12"
        >
          <h2 className="text-4xl font-bold mb-4 text-slate-900 dark:text-white">
            {t("contact.title")}
          </h2>
          <p className="text-slate-600 dark:text-slate-400 max-w-2xl mx-auto">
            {t("contact.subtitle")}
          </p>
        </motion.div>

        <div className="grid lg:grid-cols-2 gap-12">
          <motion.div
            initial={{ opacity: 0, x: -30 }}
            whileInView={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6 }}
            className="space-y-6"
          >
            <div className="bg-white dark:bg-slate-800 rounded-2xl p-8 shadow-lg">
              <h3 className="text-2xl font-semibold mb-6 text-slate-900 dark:text-white">
                {t("contact.getInTouch")}
              </h3>
              <div className="space-y-4">
                {contactInfo.map((item) => (
                  <div key={item.label} className="flex items-center gap-4">
                    <div className="p-3 rounded-xl bg-cyan-100 dark:bg-cyan-900/30 text-cyan-600 dark:text-cyan-400">
                      <item.icon size={20} />
                    </div>
                    <div>
                      <p className="text-sm text-slate-500 dark:text-slate-400">
                        {item.label}
                      </p>
                      {item.link ? (
                        <a
                          href={item.link}
                          className="font-medium hover:text-cyan-500 transition text-slate-900 dark:text-white"
                        >
                          {item.value}
                        </a>
                      ) : (
                        <p className="font-medium text-slate-900 dark:text-white">
                          {item.value}
                        </p>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </div>

            <div className="bg-gradient-to-r from-cyan-500 to-blue-500 rounded-2xl p-8 text-white">
              <h3 className="text-2xl font-semibold mb-2">
                {t("contact.availableForWork")}
              </h3>
              <p className="mb-4 opacity-90">{t("contact.availableText")}</p>
              <div className="flex gap-2">
                {["React", "Django", "TypeScript"].map((tech) => (
                  <span
                    key={tech}
                    className="px-3 py-1 bg-white/20 rounded-full text-sm"
                  >
                    {tech}
                  </span>
                ))}
              </div>
            </div>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, x: 30 }}
            whileInView={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6 }}
          >
            <form
              onSubmit={handleSubmit(onSubmit)}
              className="bg-white dark:bg-slate-800 rounded-2xl p-8 shadow-lg"
            >
              <div className="space-y-6">
                <div>
                  <label className="block text-sm font-medium mb-2 text-slate-700 dark:text-slate-300">
                    {t("contact.name")}
                  </label>
                  <input
                    {...register("name")}
                    className="w-full px-4 py-3 rounded-xl border border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-900 text-slate-900 dark:text-white focus:ring-2 focus:ring-cyan-500 focus:border-transparent transition"
                    placeholder={t("contact.yourName")}
                  />
                  {errors.name && (
                    <p className="mt-1 text-sm text-red-500">
                      {errors.name.message ===
                      "Name must be at least 2 characters"
                        ? t("contact.nameRequired")
                        : errors.name.message}
                    </p>
                  )}
                </div>

                <div>
                  <label className="block text-sm font-medium mb-2 text-slate-700 dark:text-slate-300">
                    {t("contact.emailLabel")}
                  </label>
                  <input
                    {...register("email")}
                    type="email"
                    className="w-full px-4 py-3 rounded-xl border border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-900 text-slate-900 dark:text-white focus:ring-2 focus:ring-cyan-500 focus:border-transparent transition"
                    placeholder={t("contact.yourEmail")}
                  />
                  {errors.email && (
                    <p className="mt-1 text-sm text-red-500">
                      {errors.email.message === "Invalid email address"
                        ? t("contact.emailRequired")
                        : errors.email.message}
                    </p>
                  )}
                </div>

                <div>
                  <label className="block text-sm font-medium mb-2 text-slate-700 dark:text-slate-300">
                    {t("contact.subject")}
                  </label>
                  <input
                    {...register("subject")}
                    className="w-full px-4 py-3 rounded-xl border border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-900 text-slate-900 dark:text-white focus:ring-2 focus:ring-cyan-500 focus:border-transparent transition"
                    placeholder={t("contact.yourSubject")}
                  />
                  {errors.subject && (
                    <p className="mt-1 text-sm text-red-500">
                      {errors.subject.message ===
                      "Subject must be at least 5 characters"
                        ? t("contact.subjectRequired")
                        : errors.subject.message}
                    </p>
                  )}
                </div>

                <div>
                  <label className="block text-sm font-medium mb-2 text-slate-700 dark:text-slate-300">
                    {t("contact.message")}
                  </label>
                  <textarea
                    {...register("message")}
                    rows={5}
                    className="w-full px-4 py-3 rounded-xl border border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-900 text-slate-900 dark:text-white focus:ring-2 focus:ring-cyan-500 focus:border-transparent transition resize-none"
                    placeholder={t("contact.yourMessage")}
                  />
                  {errors.message && (
                    <p className="mt-1 text-sm text-red-500">
                      {errors.message.message ===
                      "Message must be at least 10 characters"
                        ? t("contact.messageRequired")
                        : errors.message.message}
                    </p>
                  )}
                </div>

                <motion.button
                  type="submit"
                  disabled={isSubmitting}
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  className="w-full py-3 bg-gradient-to-r from-cyan-500 to-blue-500 text-white rounded-xl font-medium flex items-center justify-center gap-2 hover:shadow-lg transition-all disabled:opacity-50"
                >
                  {isSubmitting
                    ? t("contact.sending")
                    : t("contact.sendMessage")}
                  <Send size={18} />
                </motion.button>
              </div>
            </form>
          </motion.div>
        </div>
      </div>
    </section>
  );
}
