from django.urls import path

from . import views

app_name = "cart"

urlpatterns = [
    path("", views.cart, name="cart"),
    path("add_cart/<int:product_id>", views.add_cart, name="add_cart"),
    path("plus_cart/<int:cart_item_id>", views.plus_cart, name="plus_cart"),
    path("minus_cart/<int:cart_item_id>", views.minus_cart, name="minus_cart"),
    path("remove_cart/<int:cart_item_id>", views.remove_cart, name="remove_cart"),
    path("checkout/", views.checkout, name="checkout"),
]
