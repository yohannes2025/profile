// frontend/src/components/Blog.tsx
import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { Calendar, Clock, ArrowRight } from "lucide-react";
import { useTranslation } from "react-i18next";

interface BlogPost {
  id: number;
  title: string;
  slug: string;
  excerpt: string;
  featured_image: string;
  formatted_date: string;
  reading_time: string;
  tag_names: string[];
  author_name: string;
}

export default function Blog() {
  const { t } = useTranslation();
  const [posts, setPosts] = useState<BlogPost[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchPosts = async () => {
      try {
        // Fallback to localhost if the environment variable isn't configured during build time
        const baseUrl =
          import.meta.env.VITE_API_URL || "http://localhost:8000/api";

        // Use the correct endpoint: recent-posts (not recent-blog-posts)
        const response = await fetch(`${baseUrl}/recent-posts/`);
        const data = await response.json();
        const postsData = data.results || data || [];
        setPosts(Array.isArray(postsData) ? postsData : []);
      } catch (error) {
        console.error("Error fetching blog posts:", error);
        setPosts([]);
      } finally {
        setLoading(false);
      }
    };

    fetchPosts();
  }, []);

  return (
    <section
      id="blog"
      className="py-24 bg-slate-50 dark:bg-slate-900/50 scroll-mt-20"
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
            {t("blog.title")}
          </h2>
          <p className="text-slate-600 dark:text-slate-400 max-w-2xl mx-auto">
            {t("blog.subtitle")}
          </p>
        </motion.div>

        {loading ? (
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {[1, 2, 3].map((i) => (
              <div
                key={i}
                className="bg-white dark:bg-slate-800 rounded-2xl overflow-hidden shadow-lg animate-pulse"
              >
                <div className="h-48 bg-slate-200 dark:bg-slate-700" />
                <div className="p-6">
                  <div className="h-4 bg-slate-200 dark:bg-slate-700 rounded w-1/2 mb-3" />
                  <div className="h-6 bg-slate-200 dark:bg-slate-700 rounded w-3/4 mb-3" />
                  <div className="h-4 bg-slate-200 dark:bg-slate-700 rounded w-full mb-2" />
                  <div className="h-4 bg-slate-200 dark:bg-slate-700 rounded w-2/3" />
                </div>
              </div>
            ))}
          </div>
        ) : posts.length === 0 ? (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="text-center py-12 bg-white dark:bg-slate-800 rounded-2xl shadow-lg"
          >
            <div className="text-6xl mb-4">📝</div>
            <h3 className="text-2xl font-semibold mb-2 text-slate-900 dark:text-white">
              {t("blog.noPosts")}
            </h3>
            <p className="text-slate-600 dark:text-slate-400">
              {t("blog.noPostsText")}
            </p>
          </motion.div>
        ) : (
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {posts.slice(0, 3).map((post, index) => (
              <motion.article
                key={post.id}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
                viewport={{ once: true }}
                className="bg-white dark:bg-slate-800 rounded-2xl overflow-hidden shadow-lg hover:shadow-xl transition-all group"
              >
                <div className="relative h-48 overflow-hidden">
                  <img
                    src={
                      post.featured_image ||
                      `https://picsum.photos/seed/${post.id}/400/300`
                    }
                    alt={post.title}
                    className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-300"
                  />
                </div>
                <div className="p-6">
                  <div className="flex items-center gap-4 text-sm text-slate-500 dark:text-slate-400 mb-3">
                    <span className="flex items-center gap-1">
                      <Calendar size={14} /> {post.formatted_date}
                    </span>
                    <span className="flex items-center gap-1">
                      <Clock size={14} /> {post.reading_time}
                    </span>
                  </div>
                  <h3 className="text-xl font-semibold mb-2 line-clamp-2">
                    <a
                      href={`/blog/${post.slug}`}
                      className="text-slate-900 dark:text-white hover:text-cyan-500 transition"
                    >
                      {post.title}
                    </a>
                  </h3>
                  <p className="text-slate-600 dark:text-slate-400 mb-4 line-clamp-2">
                    {post.excerpt}
                  </p>
                  <div className="flex flex-wrap gap-2 mb-4">
                    {post.tag_names?.slice(0, 3).map((tag) => (
                      <span
                        key={tag}
                        className="px-2 py-1 text-xs rounded-full bg-cyan-100 dark:bg-cyan-900/30 text-cyan-600 dark:text-cyan-400"
                      >
                        #{tag}
                      </span>
                    ))}
                  </div>
                  <a
                    href={`/blog/${post.slug}`}
                    className="inline-flex items-center gap-2 text-cyan-500 hover:text-cyan-600 font-medium"
                  >
                    {t("blog.readMore")} <ArrowRight size={16} />
                  </a>
                </div>
              </motion.article>
            ))}
          </div>
        )}
      </div>
    </section>
  );
}
