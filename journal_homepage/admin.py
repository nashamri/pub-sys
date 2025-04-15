from django.contrib import admin
from .models import ResearchPaper

@admin.register(ResearchPaper)
class ResearchPaperAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'reviewer', 'submission_date', 'review_date')
    list_filter = ('status', 'reviewer')
    search_fields = ('title', 'abstract')
