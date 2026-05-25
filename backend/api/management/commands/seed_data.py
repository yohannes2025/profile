from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from api.models import Project, Skill, Testimonial, Experience, Education
from blog.models import BlogPost, Category, Tag

class Command(BaseCommand):
    help = 'Seed database with initial data'

    def handle(self, *args, **kwargs):
        # Create superuser if not exists
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
            self.stdout.write(self.style.SUCCESS('Superuser created'))

        # Seed skills
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
        
        self.stdout.write(self.style.SUCCESS(f'Created {len(skills_data)} skills'))