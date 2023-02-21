from .models import Cart, CartItem
from .views import get_session_id


def counter(request):
    try:
        cart = Cart.objects.get(session_id=get_session_id(request))
        cart_items = CartItem.objects.all().filter(cart=cart, is_active=True)
        cart_count = sum(cart_item.quantity for cart_item in cart_items)
    except Cart.DoesNotExist:
        cart_count = 0

    return dict(cart_count=cart_count)
