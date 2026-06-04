// frontend/src/components/Footer.tsx
import { Github, Linkedin, X, Instagram, Heart } from "lucide-react";
import { useTranslation } from "react-i18next";

export default function Footer() {
  const { t } = useTranslation();
  const currentYear = new Date().getFullYear();

  return (
    <footer className="border-t border-slate-200 dark:border-slate-800 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex flex-col md:flex-row justify-between items-center gap-4">
          <p className="text-slate-500 dark:text-slate-400 text-sm">
            © {currentYear} Yohannes Tekle. {t("footer.rights")}
          </p>

          <div className="flex gap-4">
            <a
              href="https://www.github.com/yohannes2025"
              target="_blank"
              rel="noopener noreferrer"
              className="text-slate-500 hover:text-cyan-500 transition-colors"
            >
              <Github size={20} />
            </a>
            <a
              href="https://www.linkedin.com/in/yohannes-mebrahtu-tekle-98a01322a/"
              target="_blank"
              rel="noopener noreferrer"
              className="text-slate-500 hover:text-cyan-500 transition-colors"
            >
              <Linkedin size={20} />
            </a>
            <a
              href="https://www.x.com/YohannesMT2025"
              target="_blank"
              rel="noopener noreferrer"
              className="text-slate-500 hover:text-cyan-500 transition-colors"
            >
              <X size={20} />
            </a>
            <a
              href="https://www.instagram.com/yohannes.mebrahtu.5"
              target="_blank"
              rel="noopener noreferrer"
              className="text-slate-500 hover:text-cyan-500 transition-colors"
            >
              <Instagram size={20} />
            </a>
          </div>

          <p className="text-slate-500 dark:text-slate-400 text-sm flex items-center gap-1">
            {t("footer.madeWith")} <Heart size={14} className="text-red-500" />{" "}
            {t("footer.using")}
          </p>
        </div>
      </div>
    </footer>
  );
}
