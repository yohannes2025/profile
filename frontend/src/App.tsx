// frontend/src/App.tsx
import { useEffect, useState } from "react";
import { BrowserRouter as Router } from "react-router-dom";
import { HelmetProvider } from "react-helmet-async";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

import Navbar from "./components/Navbar";
import Hero from "./components/Hero";
import About from "./components/About";
import Skills from "./components/Skills";
import Projects from "./components/Projects";
import Testimonials from "./components/Testimonials";
import Blog from "./components/Blog";
import Contact from "./components/Contact";
import Footer from "./components/Footer";
import ScrollToTop from "./components/ScrollToTop";
import LoadingSpinner from "./components/LoadingSpinner";
import { useTheme } from "./hooks/useTheme";

const queryClient = new QueryClient();

function App() {
  const [loading, setLoading] = useState(true);
  const { theme, toggleTheme } = useTheme();

  useEffect(() => {
    const timer = setTimeout(() => setLoading(false), 1000);
    return () => clearTimeout(timer);
  }, []);

  if (loading) {
    return <LoadingSpinner />;
  }

  return (
    <QueryClientProvider client={queryClient}>
      <HelmetProvider>
        <Router>
          <div className="min-h-screen bg-white dark:bg-slate-950 transition-colors duration-300">
            <ScrollToTop />
            <Navbar theme={theme} toggleTheme={toggleTheme} />

            <main>
              <section id="home">
                <Hero />
              </section>
              <section id="about">
                <About />
              </section>
              <section id="skills">
                <Skills />
              </section>
              <section id="projects">
                <Projects />
              </section>
              <section id="testimonials">
                <Testimonials />
              </section>
              <section id="blog">
                <Blog />
              </section>
              <section id="contact">
                <Contact />
              </section>
            </main>

            <Footer />
            <ToastContainer
              position="bottom-right"
              theme={theme === "dark" ? "dark" : "light"}
            />
          </div>
        </Router>
      </HelmetProvider>
    </QueryClientProvider>
  );
}

export default App;
