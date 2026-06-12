from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from api.models import Project, Skill, Experience, Education
# Omit Testimonial if it's removed from your frontend layout flow

# Dynamically fetch your custom identity model (email-based)
User = get_user_model()

class Command(BaseCommand):
    help = 'Seed database with initial corporate profile and engineering data'

    def handle(self, *args, **kwargs):
        # 1. Create Enterprise Superuser using Email Identity
        # 1. Create Enterprise Superuser securely without duplication crashes
        admin_email = 'admin@yohannestekle.com'
        
        # We use get_or_create on the username to prevent SQLite constraint crashes
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': admin_email,
                'is_staff': True,
                'is_superuser': True,
                'is_active': True,
            }
        )

        if created:
            admin_user.set_password('admin_secure_password_123') # Sets and hashes password correctly
            admin_user.save()
            self.stdout.write(self.style.SUCCESS(f'Superuser account [{admin_email}] initialized successfully.'))
        else:
            self.stdout.write(self.style.WARNING(f'Superuser account [{admin_email}] already verified.'))

        # 2. Seed Skills Vector
        skills_data = [
            ('Python', 'backend', 95, 1),
            ('Django', 'backend', 92, 2),
            ('React', 'frontend', 90, 3),
            ('TypeScript', 'frontend', 85, 4),
            ('PostgreSQL', 'database', 82, 5),
            ('Docker', 'devops', 78, 6),
        ]
        
        for name, category, proficiency, order in skills_data:
            Skill.objects.get_or_create(
                name=name,
                defaults={
                    'category': category,
                    'proficiency': proficiency,
                    'order': order
                }
            )
        self.stdout.write(self.style.SUCCESS(f'Synchronized {len(skills_data)} skills.'))

        # 3. Seed Professional Project Matrix (Merged from Template)
        portfolio_highlights = [
            {
                "title": "Productivity Web Ecosystem",
                "description": "A premium task and resource management solution featuring secure cross-domain JWT authentication, localized state trees, and comprehensive dashboard tracking built for enterprise workflows.",
                "github_link": "https://github.com/yohannes2025/pp5-productivity-frontend2",
                "live_demo": "https://pp5-productivity-frontend2.onrender.com/",
                "technologies": ["React SPA", "Django REST Framework", "JWT Secure Auth", "PostgreSQL"],
                "order": 1
            },
            {
                "title": "Enterprise Booking Processor",
                "description": "An automated reservation processor built to handle concurrent input requests, dynamic structural table constraints, and immediate transactional verification states.",
                "github_link": "https://github.com/yohannes2025/pp4_restaurant_booking",
                "live_demo": "https://pp4-restaurant-reservations-c439c4476aa0.herokuapp.com/",
                "technologies": ["Python Core", "Django Framework", "Relational Database", "Heroku Engine"],
                "order": 2
            },
            {
                "title": "CLI Logic Matrix Simulator",
                "description": "A deep logic console strategy game executing dynamic multidimensional array structures, strict state memory matrices, and automated computer path configurations.",
                "github_link": "https://github.com/Code-Institute-Submissions/project-3-battleships-vscode",
                "live_demo": "https://project-3-battleships-vscode-2d16e43bc072.herokuapp.com/",
                "technologies": ["Pure Python", "CLI Matrix Logic", "Algorithms", "Input Validation"],
                "order": 3
            },
            {
                "title": "Mathematical Processing Engine",
                "description": "An isolated mathematical event application evaluating floating-point formulas smoothly across intricate standard priority constraints without system overhead.",
                "github_link": "https://github.com/yohannes2025/project-2-scientific-calculator",
                "live_demo": "https://yohannes2025.github.io/project-2-scientific-calculator/",
                "technologies": ["Vanilla JavaScript", "HTML5 Native", "CSS Variables", "DOM Manipulation"],
                "order": 4
            }
        ]

        for data in portfolio_highlights:
            slug = slugify(data["title"])
            Project.objects.get_or_create(
                slug=slug,
                defaults={
                    "title": data["title"],
                    "description": data["description"],
                    "github_link": data["github_link"],
                    "live_demo": data["live_demo"],
                    "technologies": data["technologies"],
                    "featured": True,
                    "order": data["order"],
                    "content": f"Architectural breakdown for the {data['title']} engine implementation."
                }
            )
        self.stdout.write(self.style.SUCCESS(f'Synchronized {len(portfolio_highlights)} production case studies.'))
        self.stdout.write(self.style.SUCCESS('Database data baseline operational.'))