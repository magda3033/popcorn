from django.contrib import admin

from .models import Recipe, Vote

# Register your models here.
admin.site.register(Recipe)
admin.site.register(Vote)
