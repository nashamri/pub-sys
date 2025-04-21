from django.contrib import admin
from .models import Affiliation, Profile, Article, Review, AuthorResponse

# Register your models here.
admin.site.register(Affiliation)
admin.site.register(Profile)
admin.site.register(Article)
admin.site.register(Review)
admin.site.register(AuthorResponse)
