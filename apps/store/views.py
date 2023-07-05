from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.views.generic import DetailView, ListView

from apps.cart.models import CartItem
from apps.cart.views import _get_session_id
from apps.category.models import Category

from .models import Product

# Create your views here.


def store(request, category_slug=None):
    if category_slug is not None:
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=category, is_available=True)
    else:
        products = Product.objects.filter(is_available=True)

    paginator = Paginator(products, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "products": products,
        "page_obj": page_obj,
    }

    return render(request, "store/store.html", context)


def product_detail(request, category_slug, product_slug):
    product = get_object_or_404(Product, category__slug=category_slug, slug=product_slug, is_available=True)
    in_cart = CartItem.objects.filter(cart__session_id=_get_session_id(request), product=product).exists()

    context = {
        "product": product,
        "in_cart": in_cart,
    }

    return render(request, "store/product_detail.html", context)


def search(request):
    if "keyword" in request.GET:
        if keyword := request.GET["keyword"]:
            products = Product.objects.filter(
                Q(description__icontains=keyword)
                | Q(name__icontains=keyword)
                | Q(category__description__icontains=keyword)
                | Q(category__name__icontains=keyword)
            ).filter(is_available=True)
        else:
            products = Product.objects.filter(is_available=True)

    context = {
        "products": products,
    }

    return render(request, "store/store.html", context)


######################################################################################################################
# Ejemplo de las mismas funciones en CBV
######################################################################################################################


class StoreView(ListView):
    model = Product
    template_name = "store/store.html"
    context_object_name = "products"
    paginate_by = 6

    def get_queryset(self):
        if "category_slug" in self.kwargs:
            category = get_object_or_404(Category, slug=self.kwargs["category_slug"])
            return Product.objects.filter(category=category, is_available=True)

        return Product.objects.filter(is_available=True).order_by("id")


class ProductDetailView(DetailView):
    model = Product
    template_name = "store/product_detail.html"
    context_object_name = "product"

    def get_object(self):
        return get_object_or_404(
            Product,
            category__slug=self.kwargs["category_slug"],
            slug=self.kwargs["product_slug"],
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        context["in_cart"] = CartItem.objects.filter(
            cart__session_id=_get_session_id(self.request), product=product
        ).exists()

        return context
