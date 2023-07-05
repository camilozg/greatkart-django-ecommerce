import collections
from contextlib import suppress

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, render

from apps.cart.models import Cart, CartItem
from apps.store.models import Product, Variation

# Create your views here.


def _get_session_id(request):
    return request.session.session_key or request.session.create()


def add_cart(request, product_id):
    if request.method == "POST":
        cart, created = Cart.objects.get_or_create(session_id=_get_session_id(request))
        product = Product.objects.get(id=product_id)
        product_variations = []

        for item in request.POST:
            key = item
            value = request.POST[key]
            with suppress(ObjectDoesNotExist):
                product_variations.append(
                    Variation.objects.get(product=product, category__iexact=key, value__iexact=value)
                )

        if request.user.is_authenticated:
            if CartItem.objects.filter(product=product, user=request.user).exists():
                cart_items = CartItem.objects.filter(product=product, user=request.user)
                for item in cart_items:
                    if collections.Counter(list(item.variations.all())) == collections.Counter(product_variations):
                        item.quantity += 1
                        item.save()
                        return redirect("cart:cart")

            cart_item = CartItem.objects.create(product=product, cart=cart, user=request.user, quantity=1)

        else:
            if CartItem.objects.filter(product=product, cart=cart).exists():
                cart_items = CartItem.objects.filter(product=product, cart=cart)
                for item in cart_items:
                    if collections.Counter(list(item.variations.all())) == collections.Counter(product_variations):
                        item.quantity += 1
                        item.save()
                        return redirect("cart:cart")

            cart_item = CartItem.objects.create(product=product, cart=cart, quantity=1)

        cart_item.variations.add(*product_variations)
        cart_item.save()

    return redirect("cart:cart")


def plus_cart(request, cart_item_id):
    with suppress(ObjectDoesNotExist):
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(id=cart_item_id, user=request.user)
        else:
            cart = Cart.objects.get(session_id=_get_session_id(request))
            cart_item = CartItem.objects.get(id=cart_item_id, cart=cart)
        cart_item.quantity += 1
        cart_item.save()

    return redirect("cart:cart")


def minus_cart(request, cart_item_id):
    with suppress(ObjectDoesNotExist):
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(id=cart_item_id, user=request.user)
        else:
            cart = Cart.objects.get(session_id=_get_session_id(request))
            cart_item = CartItem.objects.get(id=cart_item_id, cart=cart)

        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()

    return redirect("cart:cart")


def remove_cart(request, cart_item_id):
    with suppress(ObjectDoesNotExist):
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(id=cart_item_id, user=request.user)
        else:
            cart = Cart.objects.get(session_id=_get_session_id(request))
            cart_item = CartItem.objects.get(id=cart_item_id, cart=cart)
        cart_item.delete()

    return redirect("cart:cart")


def cart(request, total=0, quantity=0, cart_items=None):
    total = 0
    subtotal = 0
    tax = 0

    with suppress(ObjectDoesNotExist):
        if request.user.is_authenticated:
            cart_items = CartItem.objects.all().filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(session_id=_get_session_id(request))
            cart_items = CartItem.objects.all().filter(cart=cart, is_active=True)

        total = sum(cart_item.quantity * cart_item.product.price for cart_item in cart_items)
        tax = round(total * (1 / 16))
        subtotal = total - tax

    context = {
        "total": _formatting_price(total),
        "subtotal": _formatting_price(subtotal),
        "tax": _formatting_price(tax),
        "cart_items": cart_items,
    }

    return render(request, "cart/cart.html", context)


@login_required(login_url="accounts:login")
def checkout(request):
    total = 0
    subtotal = 0
    tax = 0

    with suppress(ObjectDoesNotExist):
        if request.user.is_authenticated:
            cart_items = CartItem.objects.all().filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(session_id=_get_session_id(request))
            cart_items = CartItem.objects.all().filter(cart=cart, is_active=True)
        total = sum(cart_item.quantity * cart_item.product.price for cart_item in cart_items)
        tax = round(total * (1 / 16))
        subtotal = total - tax

    context = {
        "total": _formatting_price(total),
        "subtotal": _formatting_price(subtotal),
        "tax": _formatting_price(tax),
        "cart_items": cart_items,
    }

    return render(request, "cart/checkout.html", context)


def _formatting_price(price):
    return f"${price:,}".replace(",", ".")
