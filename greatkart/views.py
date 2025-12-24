
from django.shortcuts import render
from category.models import Category
from store.models import Product


def home(request):
    product = Product.objects.all().filter(available=True).order_by('created_at')
    categories = Category.objects.all()
    context = {
        'products': product,
        'categories': categories,
    }
    return render(request, 'home.html', context)
