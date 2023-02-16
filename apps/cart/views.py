import contextlib

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, redirect, render

from apps.cart.models import Cart, CartItem
from apps.store.models import Product

# Create your views here.


def session_id(request):
    return request.session.session_key or request.session.create()


def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)

    try:
        cart = Cart.objects.get(cart_id=session_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=session_id(request))

    cart.save()

    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.quantity += 1
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(product=product, quantity=1, cart=cart)

    cart_item.save()

    return redirect('cart:cart')


def decrease_cart(request, product_id):
    cart = Cart.objects.get(cart_id=session_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    return redirect('cart:cart')


def remove_cart(request, product_id):
    cart = Cart.objects.get(cart_id=session_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)

    cart_item.delete()

    return redirect('cart:cart')


def cart(request, total=0, quantity=0, cart_items=None):
    total = 0
    subtotal = 0
    tax = 0

    with contextlib.suppress(ObjectDoesNotExist):
        cart = Cart.objects.get(cart_id=session_id(request))
        cart_items = CartItem.objects.all().filter(cart=cart, is_active=True)
        total = sum(cart_item.quantity * cart_item.product.price for cart_item in cart_items)
        tax = round(total * (1 / 16))
        subtotal = total - tax

    context = {
        'total': __formatting_price(total),
        'subtotal': __formatting_price(subtotal),
        'tax': __formatting_price(tax),
        'cart_items': cart_items,
    }

    return render(request, 'store/cart.html', context)


def __formatting_price(price):
    return f'${price:,}'.replace(',', '.')
