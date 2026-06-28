from modeltranslation.translator import register, TranslationOptions
from .models import Project

@register(Project)
class ProjectTranslationOptions(TranslationOptions):
    fields = ('title', 'description') # 👈 Fields that need DE and EN versions