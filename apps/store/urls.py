from django.urls import path

from . import views

app_name = 'store'

urlpatterns = [
    path('', views.store, name='all'),
    path('<slug:category_slug>/', views.store, name='category'),
    path('<slug:category_slug>/<slug:product_slug>/', views.product, name='product'),
]
