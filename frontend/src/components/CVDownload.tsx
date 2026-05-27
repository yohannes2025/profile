// src/components/CVDownload.tsx
import { useTranslation } from "react-i18next";
import { motion } from "framer-motion";
import { Download, FileText } from "lucide-react";

export default function CVDownload() {
  const { t } = useTranslation();

  const cvFiles = [
    {
      lang: "en",
      name: t("cv.english"),
      path: "/cv/CV_Yohannes_Tekle_EN.pdf",
      flag: "🇬🇧",
    },
    {
      lang: "de",
      name: t("cv.german"),
      path: "/cv/CV_Yohannes_Tekle_DE.pdf",
      flag: "🇩🇪",
    },
  ];

  return (
    <div className="flex gap-4 justify-center my-8">
      {cvFiles.map((cv) => (
        <motion.a
          key={cv.lang}
          href={cv.path}
          download
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          className="flex items-center gap-2 px-6 py-3 bg-slate-100 dark:bg-slate-800 hover:bg-cyan-100 dark:hover:bg-cyan-900 rounded-xl transition-colors"
        >
          <FileText size={18} />
          <span>
            {cv.flag} {cv.name}
          </span>
          <Download size={16} />
        </motion.a>
      ))}
    </div>
  );
}
