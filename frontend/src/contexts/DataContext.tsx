import { createContext, useContext, useState, ReactNode } from "react";

interface Service {
  id: number;
  icon: string;
  titleKey: string;
  descKey: string;
}

interface Project {
  id: number;
  titleKey: string;
  descKey: string;
  img: string;
  tags: string[];
  liveUrl: string;
  codeUrl?: string;
}

interface SocialLink {
  id: number;
  icon: string;
  url: string;
}

interface DataContextType {
  services: Service[];
  projects: Project[];
  socialLinks: SocialLink[];
}

const DataContext = createContext<DataContextType | undefined>(undefined);

export const DataProvider = ({ children }: { children: ReactNode }) => {
  const [services] = useState<Service[]>([
    {
      id: 1,
      icon: "fa-laptop-code",
      titleKey: "serTitle1",
      descKey: "serDesc1",
    },
    { id: 2, icon: "fa-cogs", titleKey: "serTitle2", descKey: "serDesc2" },
    {
      id: 3,
      icon: "fa-shield-alt",
      titleKey: "serTitle3",
      descKey: "serDesc3",
    },
    {
      id: 4,
      icon: "fa-tachometer-alt",
      titleKey: "serTitle4",
      descKey: "serDesc4",
    },
  ]);

  const [projects] = useState<Project[]>([
    {
      id: 1,
      titleKey: "projTitle1",
      descKey: "projDesc1",
      img: "https://images.unsplash.com/photo-1484480974693-6ca0a78fb36b?q=80&w=800&auto=format&fit=crop",
      tags: ["React SPA", "Django REST Framework", "JWT Secure Auth"],
      liveUrl: "#",
      codeUrl: "#",
    },
    {
      id: 2,
      titleKey: "projTitle2",
      descKey: "projDesc2",
      img: "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?q=80&w=800&auto=format&fit=crop",
      tags: ["Python Core", "Django Framework", "Relational Database"],
      liveUrl: "#",
      codeUrl: "#",
    },
    {
      id: 3,
      titleKey: "projTitle3",
      descKey: "projDesc3",
      img: "https://images.unsplash.com/photo-1511512578047-dfb367046420?q=80&w=800&auto=format&fit=crop",
      tags: ["Pure Python", "CLI Matrix Logic", "Algorithms"],
      liveUrl: "#",
      codeUrl: "#",
    },
    {
      id: 4,
      titleKey: "projTitle4",
      descKey: "projDesc4",
      img: "https://images.unsplash.com/photo-1587145820266-a5951ee6f620?q=80&w=800&auto=format&fit=crop",
      tags: ["Vanilla JavaScript", "HTML5 Native", "CSS Variables"],
      liveUrl: "#",
      codeUrl: "#",
    },
  ]);

  const [socialLinks] = useState<SocialLink[]>([
    { id: 1, icon: "fa-github", url: "https://github.com" },
    { id: 2, icon: "fa-linkedin", url: "https://linkedin.com" },
  ]);

  return (
    <DataContext.Provider value={{ services, projects, socialLinks }}>
      {children}
    </DataContext.Provider>
  );
};

export const useData = () => {
  const context = useContext(DataContext);
  if (!context) throw new Error("useData must be used within a DataProvider");
  return context;
};
