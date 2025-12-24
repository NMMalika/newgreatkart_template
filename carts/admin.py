from django.contrib import admin
from store.models import variations
from .models import Cart, CartItem
# Register your models here.



admin.site.register(Cart)
admin.site.register(CartItem)

class VariationsAdmin(admin.ModelAdmin):
    list_display = ('product', 'color', 'size', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('product__product_name', 'color', 'size')
    list_per_page = 20
    list_editable = ('is_active',)
    
admin.site.register(variations, VariationsAdmin)