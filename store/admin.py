from django.contrib import admin
from .models import Product, variations

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'slug', 'price', 'stock', 'available', 'created_at', 'updated_at')
    prepopulated_fields = {'slug': ('product_name',)}
    list_editable = ('price', 'stock', 'available')
    list_filter = ('available', 'created_at', 'updated_at')
    search_fields = ('product_name', 'description')
    list_per_page = 20
    
admin.site.register(Product, ProductAdmin)





