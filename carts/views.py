from django.http import JsonResponse
from django.shortcuts import redirect, render,get_object_or_404
from .models import Cart, CartItem
from store.models import Product, variations

# Create your views here.
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    product_variation = []

    if request.method == 'POST':
        # Get color and size from POST
        color = request.POST.get('color')
        size = request.POST.get('size')
        
        try:
            # Find the specific variation objects
            variation_color = variations.objects.get(product=product, color__iexact=color, size__iexact=size)
            product_variation.append(variation_color)
        except:
            pass

    # Get or create the cart
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_cart_id(request))
    cart.save()

    # Check if a CartItem with this EXACT variation exists
    cart_items = CartItem.objects.filter(product=product, cart=cart)
    
    if cart_items.exists():
        existing_variation_list = []
        id_list = []
        for item in cart_items:
            existing_variation_list.append(list(item.variations.all()))
            id_list.append(item.id)

        if product_variation in existing_variation_list:
            # Increase quantity of the specific variation
            index = existing_variation_list.index(product_variation)
            item_id = id_list[index]
            item = CartItem.objects.get(id=item_id)
            item.quantity += 1
            item.save()
        else:
            # Create a new row for the new variation
            item = CartItem.objects.create(product=product, quantity=1, cart=cart)
            if len(product_variation) > 0:
                item.variations.add(*product_variation)
            item.save()
    else:
        # No cart items for this product at all, create first one
        item = CartItem.objects.create(product=product, quantity=1, cart=cart)
        if len(product_variation) > 0:
            item.variations.add(*product_variation)
        item.save()

    return redirect('cart')

def remove_cart(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id = product_id)
    cart_item = CartItem.objects.get(product = product,cart = cart)
    
    if cart_item.quantity > 1:
       cart_item.quantity -= 1
       cart_item.save()
    else:
        cart_item.delete()
    return redirect("cart")

def remove_cart_item(request,product_id):
    cart = Cart.objects.get(cart_id =_cart_id(request))
    product = get_object_or_404(Product, id = product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    cart_item.delete()
    return redirect("cart")


def cart(request, total=0,quantity=0,cart_items=None):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request)) #get the cart using the cart_id present in the session
        cart_items = CartItem.objects.filter(cart=cart, is_active=True) #get the cart items from the cart
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        
        tax =(2*total)/100
        grand_total= total + tax
        
    except Cart.DoesNotExist:
        pass #just ignore
    
    context={
        "total":total,
        "quantity":quantity,
        "cart_items":cart_items,
        "tax":tax,
        "grand_total":grand_total,
    }
    return render(request, 'store/cart.html',context)

def check_cart(request):
    product_id = request.GET.get('product_id')
    color = request.GET.get('color')
    size = request.GET.get('size')
    
    in_cart = False
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        # Look for a cart item that matches the product AND the specific variations
        cart_item = CartItem.objects.filter(
            cart=cart, 
            product_id=product_id, 
            variations__color__iexact=color, 
            variations__size__iexact=size
        ).exists()
        in_cart = cart_item
    except:
        pass
        
    return JsonResponse({'in_cart': in_cart})
