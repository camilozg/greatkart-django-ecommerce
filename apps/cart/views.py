import collections
from contextlib import suppress

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, redirect, render

from apps.cart.models import Cart, CartItem
from apps.store.models import Product, Variation

# Create your views here.


def get_session_id(request):
    return request.session.session_key or request.session.create()


def add_cart(request, product_id, cart_item_id=None):
    product = Product.objects.get(id=product_id)
    cart, created = Cart.objects.get_or_create(session_id=get_session_id(request))
    input_variations = []

    if cart_item_id is not None:
        with suppress(ObjectDoesNotExist):
            cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
            cart_item.quantity += 1
            cart_item.save()
            return redirect('cart:cart')

    if request.method == 'POST':
        for item in request.POST:
            key = item
            value = request.POST[key]
            with suppress(ObjectDoesNotExist):
                input_variations.append(
                    Variation.objects.get(product=product, category__iexact=key, value__iexact=value)
                )

    if CartItem.objects.filter(product=product, cart=cart).exists():
        cart_items = CartItem.objects.filter(product=product, cart=cart)
        for item in cart_items:
            if collections.Counter(input_variations) == collections.Counter(list(item.variations.all())):
                item.quantity += 1
                item.save()
                return redirect('cart:cart')

    cart_item = CartItem.objects.create(product=product, cart=cart, quantity=1)
    cart_item.variations.add(*input_variations)
    cart_item.save()
    return redirect('cart:cart')


def substract_cart(request, product_id, cart_item_id):
    cart = Cart.objects.get(session_id=get_session_id(request))
    product = get_object_or_404(Product, id=product_id)

    with suppress(ObjectDoesNotExist):
        cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()

    return redirect('cart:cart')


def remove_cart(request, product_id, cart_item_id):
    cart = Cart.objects.get(session_id=get_session_id(request))
    product = get_object_or_404(Product, id=product_id)

    with suppress(ObjectDoesNotExist):
        cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
        cart_item.delete()

    return redirect('cart:cart')


def cart(request, total=0, quantity=0, cart_items=None):
    total = 0
    subtotal = 0
    tax = 0

    with suppress(ObjectDoesNotExist):
        cart = Cart.objects.get(session_id=get_session_id(request))
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

    return render(request, 'cart/cart.html', context)


def __formatting_price(price):
    return f'${price:,}'.replace(',', '.')
