from django.contrib import admin
from .models import Reviewer,Submission,Review
# Register your models here.
admin.site.register(Submission)
#   admin.site.register(Review)
admin.site.register(Reviewer)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', )
