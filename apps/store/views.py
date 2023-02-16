from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render

from apps.cart.models import CartItem
from apps.cart.views import session_id
from apps.category.models import Category

from .models import Product

# Create your views here.


def store(request, category_slug=None):
    category = None
    products = None

    if category_slug is not None:
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=category, is_available=True)
    else:
        products = Product.objects.filter(is_available=True).order_by('id')

    product_count = products.count
    paginator = Paginator(products, 6)
    page_number = request.GET.get('page')
    paged_products = paginator.get_page(page_number)

    context = {
        'products': paged_products,
        'product_count': product_count,
    }

    return render(request, 'store/store.html', context)


def product_detail(request, category_slug=None, product_slug=None):
    try:
        product = get_object_or_404(Product, category__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=session_id(request), product=product).exists()
    except Exception as e:
        raise e

    context = {
        'product': product,
        'in_cart': in_cart,
    }

    return render(request, 'store/product_detail.html', context)
