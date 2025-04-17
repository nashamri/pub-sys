from django.contrib import admin
from .models import Affiliation

# Register your models here.
@admin.register(Affiliation)
class AffiliationAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'phone')  # Fields to display in the list view
    search_fields = ('name', 'address', 'country')  # Fields that can be searched
    list_filter = ('country',)  # Add filtering by country
    ordering = ('name',)  # Default ordering by name