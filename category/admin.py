from django.contrib import admin
from .models import Category

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'slug', 'category_image')   # fields to display in list
    search_fields = ('category_name',)                       # add a search bar
    prepopulated_fields = {'slug': ('category_name',)}       # auto-fill slug

admin.site.register(Category, CategoryAdmin)
