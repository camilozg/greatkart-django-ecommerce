from django.urls import path

from . import views

app_name = 'store'

urlpatterns = [
    path('', views.store, name='all_products'),
    path('category/<slug:category_slug>/', views.store, name='products_by_category'),
    path('<slug:category_slug>/<slug:product_slug>/', views.product_detail, name='product_detail'),
    path('search/', views.search, name='search')
    ##################################################################################################################
    # Ejemplo de las mismas url en CBV
    ##################################################################################################################
    # path('', views.StoreView.as_view(), name='all_products'),
    # path('category/<slug:category_slug>/', views.StoreView.as_view(), name='products_by_category'),
    # path('<slug:category_slug>/<slug:product_slug>/', views.ProductDetailView.as_view(), name='product_detail'),
]
