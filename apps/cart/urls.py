from django.urls import path

from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart, name='cart'),
    path('add_cart/<int:product_id>', views.add_cart, name='add_cart'),
    path('decrease_cart/<int:product_id>', views.decrease_cart, name='decrease_cart'),
    path('remove_cart/<int:product_id>', views.remove_cart, name='remove_cart'),
]
