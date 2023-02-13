from django.shortcuts import get_object_or_404, render

from apps.category.models import Category

from .models import Product

# Create your views here.


def store(request, category_slug=None):
    category = None
    products = None

    if category_slug is not None:
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=category)
    else:
        products = Product.objects.filter(is_available=True)

    product_count = products.count

    context = {
        'products': products,
        'product_count': product_count,
    }

    return render(request, 'store/store.html', context)


def product(request, category_slug=None, product_slug=None):
    try:
        product = get_object_or_404(Product, category__slug=category_slug, slug=product_slug)
    except Exception as e:
        raise e

    context = {
        'product': product,
    }

    return render(request, 'store/product.html', context)
