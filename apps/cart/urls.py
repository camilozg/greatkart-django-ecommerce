from django.urls import path

from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart, name='cart'),
    path('add_cart/<int:product_id>', views.add_cart, name='add_cart'),
    path('add_cart/<int:product_id>/<int:cart_item_id>', views.add_cart, name='add_cart_plus_button'),
    path('substract_cart/<int:product_id>/<int:cart_item_id>', views.substract_cart, name='substract_cart'),
    path('remove_cart/<int:product_id>/<int:cart_item_id>', views.remove_cart, name='remove_cart'),
]
