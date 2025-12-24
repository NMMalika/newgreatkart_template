from django.db import models
from category.models import Category
from django.urls import reverse

# Create your models here.
class Product(models.Model):
    product_name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(max_length=255, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    product_image = models.ImageField(upload_to='photos/products', blank=False, null=False)
    category = models.ForeignKey('category.Category', on_delete=models.CASCADE, related_name='products')

    class Meta:
        verbose_name = 'product'
        verbose_name_plural = 'products'
    
    def get_url(self):
        
        return reverse('product_detail', args=[self.category.slug, self.slug])

    def __str__(self):
        return self.product_name
 # Assuming SIZE_CHOICES is defined as before
SIZE_CHOICES = (
    ('small', 'Small'),
    ('medium', 'Medium'),
    ('large', 'Large'),
    ('extra_large', 'Extra Large'),
)

class variations(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    color = models.CharField(max_length=100) # e.g., 'Red', 'Blue'
    size = models.CharField(
        max_length=100,
        choices=SIZE_CHOICES 
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)   

    class Meta:
        # Enforce that the combination of product, color, and size must be unique.
        # This prevents, for example, two separate entries for 
        # (Product A, Red, Small).
        unique_together = ('product', 'color', 'size')

    def __str__(self):
        # Using get_size_display() gets the human-readable label (e.g., 'Small')
        return f"{self.product.product_name} - {self.color} - {self.get_size_display()}"