# 🚀 Professional Portfolio Website

A modern, full-stack portfolio website built with React, Django, and PostgreSQL. Features bilingual support (English/German), dark/light mode, contact form with auto-reply, and a fully responsive design.

![Portfolio Screenshot](https://via.placeholder.com/1200x630/0D9488/FFFFFF?text=Yohannes+Tekle+-+Portfolio)

## ✨ Live Demo

- **Website:** [www.yohannestekle.com](https://www.yohannestekle.com)
- **Backend API:** [profile-k2rv.onrender.com](https://profile-k2rv.onrender.com)
- **Admin Panel:** [profile-k2rv.onrender.com/admin](https://profile-k2rv.onrender.com/admin)

## 📋 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Environment Variables](#-environment-variables)
- [Deployment](#-deployment)
- [API Endpoints](#-api-endpoints)
- [Screenshots](#-screenshots)
- [Contributing](#-contributing)
- [License](#-license)
- [Contact](#-contact)

## 🎯 Features

### Frontend
- ✅ **Bilingual Support** - English and German with language switcher
- ✅ **Dark/Light Mode** - Theme toggle with localStorage persistence
- ✅ **Responsive Design** - Mobile-first approach, works on all devices
- ✅ **Smooth Animations** - Framer Motion animations throughout
- ✅ **Contact Form** - Email sending with auto-reply confirmation
- ✅ **Projects Showcase** - Dynamic project listing from API
- ✅ **Skills Section** - Progress bars with proficiency levels
- ✅ **Testimonials** - Client feedback carousel
- ✅ **Blog System** - Full CMS with categories and tags
- ✅ **CV Download** - Bilingual CV (EN/DE) download
- ✅ **SEO Optimized** - Meta tags, sitemap, and Open Graph
- ✅ **Accessibility** - WCAG compliant

### Backend
- ✅ **RESTful API** - Django REST Framework with JWT authentication
- ✅ **Database** - PostgreSQL with SQLite for development
- ✅ **Email System** - Auto-reply with HTML templates
- ✅ **Admin Dashboard** - Full CMS for managing content
- ✅ **API Documentation** - Swagger/OpenAPI at `/api/docs/`
- ✅ **Rate Limiting** - Protection against spam
- ✅ **Caching** - Redis for performance optimization
- ✅ **Background Tasks** - Celery for async email processing
- ✅ **Security** - CORS, CSRF, and JWT authentication
- ✅ **Cloud Storage** - Cloudinary for image optimization

### DevOps
- ✅ **CI/CD Pipeline** - GitHub Actions for automated deployments
- ✅ **Container Support** - Docker and Docker Compose
- ✅ **Monitoring** - Health checks and logging
- ✅ **SSL/HTTPS** - Automatic with Vercel and Render

## 🛠 Tech Stack

### Frontend
| Technology | Version | Purpose |
|------------|---------|---------|
| React | 18.2.0 | UI Framework |
| TypeScript | 5.3.3 | Type Safety |
| Vite | 5.0.12 | Build Tool |
| Tailwind CSS | 3.4.0 | Styling |
| Framer Motion | 10.18.0 | Animations |
| React Router | 6.22.0 | Routing |
| TanStack Query | 5.18.1 | Data Fetching |
| React Hook Form | 7.49.3 | Form Handling |
| Zod | 3.22.4 | Validation |
| i18next | 23.7.11 | Internationalization |
| Lucide React | 0.263.1 | Icons |

### Backend
| Technology | Version | Purpose |
|------------|---------|---------|
| Django | 5.0.2 | Web Framework |
| Django REST Framework | 3.14.0 | API |
| PostgreSQL | 16 | Database |
| Celery | 5.3.4 | Async Tasks |
| Redis | 7 | Cache & Message Broker |
| Cloudinary | 1.36.0 | Image Storage |
| Gunicorn | 21.2.0 | Production Server |
| JWT | 5.3.1 | Authentication |

### Deployment
| Platform | Purpose |
|----------|---------|
| Vercel | Frontend Hosting |
| Render | Backend Hosting |
| GitHub Actions | CI/CD |
| Docker | Containerization |

## 📁 Project Structure

```text
portfolio/
├── backend/                          # Django REST API
│   ├── api/                          # Main API app (projects, skills, contact)
│   ├── blog/                         # Blog app with CMS
│   ├── users/                        # User management & authentication
│   ├── config/                       # Django configuration
│   │   ├── settings.py               # Main settings
│   │   ├── urls.py                   # Root URL configuration
│   │   └── celery.py                 # Celery configuration
│   ├── requirements.txt              # Python dependencies
│   ├── Dockerfile                    # Docker containerization
│   └── docker-compose.yml            # Docker Compose configuration
│
├── frontend/                         # React + TypeScript
│   ├── src/
│   │   ├── components/               # React components
│   │   │   ├── Hero.tsx
│   │   │   ├── About.tsx
│   │   │   ├── Skills.tsx
│   │   │   ├── Projects.tsx
│   │   │   ├── Testimonials.tsx
│   │   │   ├── Blog.tsx
│   │   │   ├── Contact.tsx
│   │   │   ├── Navbar.tsx
│   │   │   └── Footer.tsx
│   │   ├── locales/
│   │   │   ├── en/
│   │   │   └── de/
│   │   ├── hooks/
│   │   ├── services/
│   │   ├── contexts/
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── public/
│   │   ├── images/
│   │   ├── cv/
│   │   └── favicon.svg
│   ├── package.json
│   ├── vite.config.ts
│   ├── tailwind.config.js
│   └── Dockerfile
│
├── .github/
│   └── workflows/
│       └── deploy.yml
│
├── .env.example                      # Environment variables template
├── .gitignore
└── README.md
```

## 🚀 Installation

### Prerequisites

- Python 3.12+
- Node.js 20+
- PostgreSQL (or SQLite for development)
- Redis (optional, for Celery)

### Backend Setup

```bash
# Clone the repository
git clone https://github.com/yohannes2025/profile.git
cd profile/backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start the server
python manage.py runserver

cd profile/frontend

# Install dependencies
npm install

# Set up environment variables
cp .env.example .env.local
# Edit .env.local with your configuration

# Start development server
npm run dev

# Build and run all services
docker-compose up --build

# Services will be available at:
# - Frontend: http://localhost:5173
# - Backend: http://localhost:8000
# - Admin: http://localhost:8000/admin

# Django Settings
SECRET_KEY=your-super-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_NAME=portfolio_db
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432

# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=your-email@gmail.com
CONTACT_EMAIL=your-email@gmail.com

# Redis (for Celery)
REDIS_URL=redis://localhost:6379/0

# Cloudinary (for images)
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret

# Frontend URL
FRONTEND_URL=http://localhost:5173

VITE_API_URL=http://localhost:8000/api
VITE_EMAILJS_SERVICE_ID=your-service-id
VITE_EMAILJS_TEMPLATE_ID=your-template-id
VITE_EMAILJS_PUBLIC_KEY=your-public-key
VITE_GA_MEASUREMENT_ID=G-XXXXXXXXXX

🚀 Deployment Frontend (Vercel) Push your code to GitHub

Go to Vercel

Import your repository

Configure environment variables

Deploy

Backend (Render) Push your code to GitHub

Go to Render

Create a new Web Service

Connect your repository

Set environment variables

Deploy

GitHub Actions CI/CD The project includes a GitHub Actions workflow that:

Runs tests on push

Deploys frontend to Vercel

Deploys backend to Render

📡 **API** Endpoints
Endpoint	Method	Description
/api/projects/	**GET**	List all projects
/api/skills/	**GET**	List all skills
/api/testimonials/	**GET**	List testimonials
/api/experiences/	**GET**	List work experiences
/api/education/	**GET**	List education
/api/blog/	**GET**	List blog posts
/api/contact/	**POST**	Submit contact form
/api/users/	**POST**	User registration
/api/users/login/	**POST**	User login
/api/docs/	**GET**	**API** documentation (Swagger)
📸 Screenshots
Homepage
[https://via.placeholder.com/800x400/**0D9488**/**FFFFFF**?text=Homepage](https://via.placeholder.com/800x400/**0D9488**/**FFFFFF**?text=Homepage)

### Dark Mode

[https://via.placeholder.com/800x400/1a2021a202c/**FFFFFF**?text=Darkc/**FFFFFF**?text=Dark+Mode](https://via.placeholder.com/800x400/1a2021a202c/**FFFFFF**?text=Darkc/**FFFFFF**?text=Dark+Mode)

### Contact Form

![Contact+Mode)

### Contact Form

![Contact Form](https:// Form](https://via.placeholder.com/800x400via.placeholder.com/800x400/**0D9488**/**FFFFFF**/**0D9488**/**FFFFFF**?text=Contact+Form)

###?text=Contact+Form)

### Admin Dashboard

![Admin Dashboard](https://via Admin Dashboard [https://via.placeholder.com/800x400/0.placeholder.com/800x400/**0D9488**/**FFFFFF**?textD9488/**FFFFFF**?text=Admin+Dashboard](https://via.placeholder.com/800x400/0.placeholder.com/800x400/**0D9488**/**FFFFFF**?textD9488/**FFFFFF**?text=Admin+Dashboard)

🤝 Contributing 1=Admin+Dashboard)

🤝 Contributing Fork the repository

Create your feature branch (git checkout -b feature/amazing-feature)

Commit your changes (`git commit -m 'Add some. Fork the repository

Create your feature branch (git checkout -b feature/amazing-feature)

Commit your changes (git commit -m 'Add some amazing feature') amazing feature'`)

Push to the branch (git4. Push to the branch (git push origin feature/ push origin feature/amazing-featureamazing-feature`)

Open`)

Open a Pull Request

Development a Pull Request ### Development Guidelines Follow **PEP** Guidelines

Follow **PEP8** for Python code

Follow **ESL** 8 for Python code

Follow ESLint rules for TypeScript/React

Write meaningful commit messages

Update documentation asint rules for TypeScript/React

Write meaningful commit messages

Update documentation as needed needed

Add tests for new features

##- Add tests for new features

📄 License This project is licensed under the 📄 License

This project **MIT** License - see the [**LICENSE** is licensed under the **MIT** License - see the **LICENSE** file for details.

📬](**LICENSE**) file for details. 📬 Contact Yohannes M Contact

### Yohannes Mebrahtu Tekle

ebrahtu Tekle

Email:- Email: yohannes.m [yohannes.m.tekle@gmail.com](mailto:yohannes.m.tekle@gmail.com)

**[Linked.tekle@gmail.com](mailto:Linked.tekle@gmail.com)

LinkedIn: [yohannes-mebrahtu-tekle](https://[www.lIn:**](https://www.lIn:**) yohannes-mebrahtu-tekle -01322a/)

GitHub: GitHub: yohannes2025

Website: [www.yohannestekle.com](https://www.yohannestekle.com)

yohannes2025

Website: [www.yohannestekle.com](https://www.yohannestekle.com)

Location: Cologne, Germany

🙏 Acknowledgements Vercel - Frontend hosting

Render - Backend hosting

Cloudinary - Image storage

EmailJS - Email service

Google Analytics - Analytics Location: Cologne, Germany

🙏 Acknowledgements Vercel - Frontend hosting

Render - Backend hosting

Cloudinary - Image storage

EmailJS - Email service

Google Analytics - Analytics

📊 Project Status This project is actively maintained and used as a professional portfolio. Feature requests and bug reports are welcome!

⭐ If you find this project useful, please give it a star on GitHub!

**

📊 Project Status This project is actively maintained and used as a professional portfolio. Feature requests and bug reports are welcome!

⭐ If you find this project useful, please give it a star on GitHub!

Built with ❤️ by YBuilt with ❤️ by Yohannes Tekle

Here's a comprehensive **README**.md file for your entire portfolio project:

markdown # 🚀 Professional Portfolio Website

A modern, full-stack portfolio website built with React, Django, and PostgreSQL. Features bilingual support (English/German), dark/light mode, contact form with auto-reply, and a fully responsive design.

![Portfolio Screenshot](https://via.placeholder.com/1200x630/**0D9488**/**FFFFFF**?text=Yohannes+Tekle+-+Portfolio)

## ✨ Live Demo

- **Website:** [www.yohannestekle.com](https://www.yohannestekle.com)
- **Backend **API**:** [profile-k2rv.onrender.com](https://profile-k2rv.onrender.com)
- **Admin Panel:** [profile-k2rv.onrender.com/admin](https://profile-k2rv.onrender.com/admin)

## 📋 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Environment Variables](#-environment-variables)
- [Deployment](#-deployment)
- [**API** Endpoints](#-api-endpoints)
- [Screenshots](#-screenshots)
- [Contributing](#-contributing)
- [License](#-license)
- [Contact](#-contact)

## 🎯 Features

### Frontend

- ✅ **Bilingual Support** - English and German with language switcher
- ✅ **Dark/Light Mode** - Theme toggle with localStorage persistence
- ✅ **Responsive Design** - Mobile-first approach, works on all devices
- ✅ **Smooth Animations** - Framer Motion animations throughout
- ✅ **Contact Form** - Email sending with auto-reply confirmation
- ✅ **Projects Showcase** - Dynamic project listing from **API**
- ✅ **Skills Section** - Progress bars with proficiency levels
- ✅ **Testimonials** - Client feedback carousel
- ✅ **Blog System** - Full **CMS** with categories and tags
- ✅ **CV Download** - Bilingual CV (EN/DE) download
- ✅ ****SEO** Optimized** - Meta tags, sitemap, and Open Graph
- ✅ **Accessibility** - **WCAG** compliant

### Backend

- ✅ **RESTful **API**** - Django **REST** Framework with **JWT** authentication
- ✅ **Database** - PostgreSQL with SQLite for development
- ✅ **Email System** - Auto-reply with **HTML** templates
- ✅ **Admin Dashboard** - Full **CMS** for managing content
- ✅ ****API** Documentation** - Swagger/OpenAPI at `/api/docs/`
- ✅ **Rate Limiting** - Protection against spam
- ✅ **Caching** - Redis for performance optimization
- ✅ **Background Tasks** - Celery for async email processing
- ✅ **Security** - **CORS**, **CSRF**, and **JWT** authentication
- ✅ **Cloud Storage** - Cloudinary for image optimization

### DevOps

- ✅ **CI/CD Pipeline** - GitHub Actions for automated deployments
- ✅ **Container Support** - Docker and Docker Compose
- ✅ **Monitoring** - Health checks and logging
- ✅ ****SSL**/**HTTPS**** - Automatic with Vercel and Render

## 🛠 Tech Stack

### Frontend

| Technology | Version | Purpose |
|------------|---------|---------|
| React | 18.2.0 | UI Framework |
| TypeScript | 5.3.3 | Type Safety |
| Vite | 5.0.12 | Build Tool |
| Tailwind CSS | 3.4.0 | Styling |
| Framer Motion | 10.18.0 | Animations |
| React Router | 6.22.0 | Routing |
| TanStack Query | 5.18.1 | Data Fetching |
| React Hook Form | 7.49.3 | Form Handling |
| Zod | 3.22.4 | Validation |
| i18next | 23.7.11 | Internationalization |
| Lucide React | 0.263.1 | Icons |

### Backend

| Technology | Version | Purpose |
|------------|---------|---------|
| Django | 5.0.2 | Web Framework |
| Django REST Framework | 3.14.0 | API |
| PostgreSQL | 16 | Database |
| Celery | 5.3.4 | Async Tasks |
| Redis | 7 | Cache & Message Broker |
| Cloudinary | 1.36.0 | Image Storage |
| Gunicorn | 21.2.0 | Production Server |
| JWT | 5.3.1 | Authentication |

### Deployment

| Platform | Purpose |
|----------|---------|
| Vercel | Frontend Hosting |
| Render | Backend Hosting |
| GitHub Actions | CI/CD |
| Docker | Containerization |

## 📁 Project Structure

portfolio/ ├── backend/ # Django **REST** **API** │ ├── api/ # Main **API** app (projects, skills, contact) │ ├── blog/ # Blog app with **CMS** │ ├── users/ # User management & authentication │ ├── config/ # Django configuration │ │ ├── settings.py # Main settings │ │ ├── urls.py # Root **URL** configuration │ │ └── celery.py # Celery configuration │ ├── requirements.txt # Python dependencies │ ├── Dockerfile # Docker containerization │ └── docker-compose.yml # Docker compose configuration │ ├── frontend/ # React + TypeScript │ ├── src/ │ │ ├── components/ # All React components │ │ │ ├── Hero.tsx # Homepage hero section │ │ │ ├── About.tsx # About section with CV download │ │ │ ├── Skills.tsx # Skills with progress bars │ │ │ ├── Projects.tsx # Projects showcase │ │ │ ├── Testimonials.tsx │ │ │ ├── Blog.tsx # Blog section │ │ │ ├── Contact.tsx # Contact form │ │ │ ├── Navbar.tsx # Navigation with theme & language │ │ │ └── Footer.tsx │ │ ├── locales/ # Translations (EN/DE) │ │ │ ├── en/ # English translations │ │ │ └── de/ # German translations │ │ ├── hooks/ # Custom React hooks │ │ ├── services/ # **API** service layer │ │ ├── contexts/ # React contexts │ │ ├── App.tsx # Main app component │ │ └── main.tsx # Entry point │ ├── public/ │ │ ├── images/ # Static images │ │ ├── cv/ # CV files (EN/DE) │ │ └── favicon.svg # Favicon │ ├── package.json # Node dependencies │ ├── vite.config.ts # Vite configuration │ ├── tailwind.config.js # Tailwind **CSS** configuration │ └── Dockerfile # Docker containerization │ ├── .github/ │ └── workflows/ # GitHub Actions CI/CD │ └── deploy.yml │ ├── .env.example # Environment variables template ├── .gitignore # Git ignore file └── **README**.md # This file

text

## 🚀 Installation

### Prerequisites

- Python 3.12+
- Node.js 20+
- PostgreSQL (or SQLite for development)
- Redis (optional, for Celery)

### Backend Setup

```bash # Clone the repository git clone [https://github.com/yohannes2025/profile.git](https://github.com/yohannes2025/profile.git) cd profile/backend

# Create virtual environment

python -m venv venv source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies

pip install -r requirements.txt

# Set up environment variables

cp .env.example .env # Edit .env with your configuration

# Run migrations

python manage.py migrate

# Create superuser

python manage.py createsuperuser

# Start the server

python manage.py runserver ### Frontend Setup bash cd profile/frontend

# Install dependencies

npm install

# Set up environment variables

cp .env.example .env.local # Edit .env.local with your configuration

# Start development server

npm run dev Running with Docker bash # Build and run all services docker-compose up --build

# Services will be available at:

# - Frontend: [http://localhost:5173](http://localhost:5173) # - Backend: [http://localhost:8000](http://localhost:8000) # - Admin: [http://localhost:8000/admin](http://localhost:8000/admin) 🔧 Environment Variables Backend (.env) env # Django Settings SECRET_KEY=your-super-secret-key **DEBUG**=True ALLOWED_HOSTS=localhost,**127**.0.0.1

# Database

DB_NAME=portfolio_db DB_USER=postgres DB_PASSWORD=postgres DB_HOST=localhost DB_PORT=**5432**

# Email

EMAIL_HOST=smtp.gmail.com EMAIL_PORT=**587** EMAIL_USE_TLS=True EMAIL_HOST_USER=[your-email@gmail.com](mailto:your-email@gmail.com) EMAIL_HOST_PASSWORD=your-app-password DEFAULT_FROM_EMAIL=[your-email@gmail.com](mailto:your-email@gmail.com) CONTACT_EMAIL=[your-email@gmail.com](mailto:your-email@gmail.com)

# Redis (for Celery)

REDIS_URL=redis://localhost:**6379**/0

# Cloudinary (for images)

CLOUDINARY_CLOUD_NAME=your-cloud-name CLOUDINARY_API_KEY=your-api-key CLOUDINARY_API_SECRET=your-api-secret

# Frontend URL

FRONTEND_URL=[http://localhost:**5173**](http://localhost:**5173**) Frontend (.env.local) env VITE_API_URL=[http://localhost:**8000**/api](http://localhost:**8000**/api) VITE_EMAILJS_SERVICE_ID=your-service-id VITE_EMAILJS_TEMPLATE_ID=your-template-id VITE_EMAILJS_PUBLIC_KEY=your-public-key VITE_GA_MEASUREMENT_ID=G-**XXXXXXXXXX** 🚀 Deployment Frontend (Vercel) Push your code to GitHub

Go to Vercel

Import your repository

Configure environment variables

Deploy

Backend (Render) Push your code to GitHub

Go to Render

Create a new Web Service

Connect your repository

Set environment variables

Deploy

GitHub Actions CI/CD The project includes a GitHub Actions workflow that:

Runs tests on push

Deploys frontend to Vercel

Deploys backend to Render

📡 **API** Endpoints
Endpoint	Method	Description
/api/projects/	**GET**	List all projects
/api/skills/	**GET**	List all skills
/api/testimonials/	**GET**	List testimonials
/api/experiences/	**GET**	List work experiences
/api/education/	**GET**	List education
/api/blog/	**GET**	List blog posts
/api/contact/	**POST**	Submit contact form
/api/users/	**POST**	User registration
/api/users/login/	**POST**	User login
/api/docs/	**GET**	**API** documentation (Swagger)
📸 Screenshots
Homepage
[https://via.placeholder.com/800x400/**0D9488**/**FFFFFF**?text=Homepage](https://via.placeholder.com/800x400/**0D9488**/**FFFFFF**?text=Homepage)

### Dark Mode

[https://via.placeholder.com/800x400/1a2021a202c/**FFFFFF**?text=Darkc/**FFFFFF**?text=Dark+Mode](https://via.placeholder.com/800x400/1a2021a202c/**FFFFFF**?text=Darkc/**FFFFFF**?text=Dark+Mode)

### Contact Form

![Contact+Mode)

### Contact Form

![Contact Form](https:// Form](https://via.placeholder.com/800x400via.placeholder.com/800x400/**0D9488**/**FFFFFF**/**0D9488**/**FFFFFF**?text=Contact+Form)

###?text=Contact+Form)

### Admin Dashboard

![Admin Dashboard](https://via Admin Dashboard [https://via.placeholder.com/800x400/0.placeholder.com/800x400/**0D9488**/**FFFFFF**?textD9488/**FFFFFF**?text=Admin+Dashboard](https://via.placeholder.com/800x400/0.placeholder.com/800x400/**0D9488**/**FFFFFF**?textD9488/**FFFFFF**?text=Admin+Dashboard)

🤝 Contributing 1=Admin+Dashboard)

🤝 Contributing Fork the repository

Create your feature branch (git checkout -b feature/amazing-feature)

Commit your changes (`git commit -m 'Add some. Fork the repository

Create your feature branch (git checkout -b feature/amazing-feature)

Commit your changes (git commit -m 'Add some amazing feature') amazing feature'`)

Push to the branch (git4. Push to the branch (git push origin feature/ push origin feature/amazing-featureamazing-feature`)

Open`)

Open a Pull Request

Development a Pull Request ### Development Guidelines Follow **PEP** Guidelines

Follow **PEP8** for Python code

Follow **ESL** 8 for Python code

Follow ESLint rules for TypeScript/React

Write meaningful commit messages

Update documentation asint rules for TypeScript/React

Write meaningful commit messages

Update documentation as needed needed

Add tests for new features

##- Add tests for new features

📄 License This project is licensed under the 📄 License

This project **MIT** License - see the [**LICENSE** is licensed under the **MIT** License - see the **LICENSE** file for details.

📬](**LICENSE**) file for details. 📬 Contact Yohannes M Contact

### Yohannes Mebrahtu Tekle

ebrahtu Tekle

Email:- Email: yohannes.m [yohannes.m.tekle@gmail.com](mailto:yohannes.m.tekle@gmail.com)

**[Linked.tekle@gmail.com](mailto:Linked.tekle@gmail.com)

LinkedIn: [yohannes-mebrahtu-tekle](https://[www.lIn:**](https://www.lIn:**) yohannes-mebrahtu-tekle -01322a/)

GitHub: GitHub: yohannes2025

Website: [www.yohannestekle.com](https://www.yohannestekle.com)

yohannes2025

Website: [www.yohannestekle.com](https://www.yohannestekle.com)

Location: Cologne, Germany

🙏 Acknowledgements Vercel - Frontend hosting

Render - Backend hosting

Cloudinary - Image storage

EmailJS - Email service

Google Analytics - Analytics Location: Cologne, Germany

🙏 Acknowledgements Vercel - Frontend hosting

Render - Backend hosting

Cloudinary - Image storage

EmailJS - Email service

Google Analytics - Analytics

📊 Project Status This project is actively maintained and used as a professional portfolio. Feature requests and bug reports are welcome!

⭐ If you find this project useful, please give it a star on GitHub!

**

📊 Project Status This project is actively maintained and used as a professional portfolio. Feature requests and bug reports are welcome!

⭐ If you find this project useful, please give it a star on GitHub!

Built with ❤️ by YBuilt with ❤️ by Yohannes Tekle

text

This **README** covers:
- ✅ Project overview and features
- ✅ Full tech stack
- ✅ Installation instructions
- ✅ Environment variables
- ✅ Deployment guides
- ✅ APIohannes Tekle**
This **README** covers:

✅ Project overview and features

✅ Full tech stack

✅ Installation instructions

✅ Environment variables

✅ Deployment guides

✅ **API** documentation

✅ Contributing guidelines

✅ Project structure

✅ Contact information
