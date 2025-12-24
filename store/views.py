from django.shortcuts import render, get_object_or_404
from .models import Product
from category.models import Category
from carts.models import CartItem  # Make sure CartItem is imported
from carts.views import _cart_id   # Import _cart_id function
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q  
from django.http import JsonResponse
from .models import variations

# Create your views here.
def store(request, category_slug=None):
    categories = None
    products = None
    
    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, available=True).order_by('-id')
        paginator = Paginator(products, 6)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
    else:
        products = Product.objects.all().filter(available=True).order_by('-id')
        paginator = Paginator(products, 6)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        products = paged_products
        product_count = paginator.count
    
    context = {
        'products': paged_products,
        "product_count": product_count
    }
    return render(request, 'store/store.html', context)

def product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(
            category__slug=category_slug,
            slug=product_slug
        )
        in_cart = CartItem.objects.filter(
            cart__cart_id=_cart_id(request),
            product=single_product
        ).exists()
    except Exception as e:
        raise e

    # ONLY get unique colors
    colors = single_product.variations_set.values_list('color', flat=True).distinct()

    context = {
        'single_product': single_product,
        'in_cart': in_cart,
        'colors': colors,
    }

    return render(request, 'store/product_detail.html', context)

def search(request):
    if "keyword" in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            from django.db.models import Q
            products = Product.objects.order_by('-created_at').filter(
                Q(description__icontains=keyword) | Q(product_name__icontains=keyword)
            )
            product_count = products.count()
    context = { 'products': products, 'product_count': product_count }

    return render(request, 'store/store.html', context)

def get_sizes_by_color(request):
    product_id = request.GET.get('product_id')
    color = request.GET.get('color')

    sizes = (
        variations.objects
        .filter(
            product_id=product_id,
            color=color,
            is_active=True
        )
        .values_list('size', flat=True)
        .distinct()
    )

    return JsonResponse({'sizes': list(sizes)})