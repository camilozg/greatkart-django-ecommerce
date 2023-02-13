from django.urls import path

from . import views

app_name = 'store'

urlpatterns = [
    path('', views.store, name='all_products'),
    path('<slug:category_slug>/', views.store, name='products_by_category'),
    path('<slug:category_slug>/<slug:product_slug>/', views.product, name='product_detail'),
]
