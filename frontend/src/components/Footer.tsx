// frontend/src/components/Footer.tsx
import { Github, Linkedin, Twitter, Mail, Heart } from "lucide-react";
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
              href="https://github.com/yohannes"
              target="_blank"
              rel="noopener noreferrer"
              className="text-slate-500 hover:text-cyan-500 transition-colors"
            >
              <Github size={20} />
            </a>
            <a
              href="https://linkedin.com/in/yohannes"
              target="_blank"
              rel="noopener noreferrer"
              className="text-slate-500 hover:text-cyan-500 transition-colors"
            >
              <Linkedin size={20} />
            </a>
            <a
              href="https://twitter.com/yohannes"
              target="_blank"
              rel="noopener noreferrer"
              className="text-slate-500 hover:text-cyan-500 transition-colors"
            >
              <Twitter size={20} />
            </a>
            <a
              href="mailto:yohannes.m.tekle@gmail.com"
              className="text-slate-500 hover:text-cyan-500 transition-colors"
            >
              <Mail size={20} />
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
