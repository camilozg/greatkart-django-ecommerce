"""greatkart URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

"""
Para disponer de los archivos media cargados por los usuarios agregamos la configuración
+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT), esto solo se debe usar
en desarrlo con en el modo DEBUG = True. Para entornos de producción los archivos se deben
recolectar con el comando collecstatic.
"""

urlpatterns = [
    path("", include("apps.core.urls")),
    path("store/", include("apps.store.urls")),
    path("cart/", include("apps.cart.urls")),
    path("accounts/", include("apps.accounts.urls")),
    path("orders/", include("apps.orders.urls")),
    path("admin/", admin.site.urls),
    # path('accounts/', include('django.contrib.auth.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

"""
El include django.contrib.auth.urls agrega las siguientes rutas de autenticación por
defecto. La ruta de signup debemos crearla nosotros mismos:

    accounts/ login/ [name='login']
    accounts/ logout/ [name='logout']
    accounts/ password_change/ [name='password_change']
    accounts/ password_change/done/ [name='password_change_done']
    accounts/ password_reset/ [name='password_reset']
    accounts/ password_reset/done/ [name='password_reset_done']
    accounts/ reset/<uidb64>/<token>/ [name='password_reset_confirm']
    accounts/ reset/done/ [name='password_reset_complete']

Podemos sobreescribir las templates de autenticación por defecto creando templates con los
mismos nombres. Podemos encontrar los templates por defecto en el repositorio de django
https://github.com/django/django/tree/main/django/contrib/admin/templates/registration.
No existen templates por defecto para el login y el signup, siempre debemos crearlos en
un ruta llamada registration:

    registration/ logged_out.html
    registration/ password_change_done.html
    registration/ password_change_form.html
    registration/ password_reset_complete.html
    registration/ password_reset_confirm.html
    registration/ password_reset_done.html
    registration/ password_reset_email.html
    registration/ password_reset.html
"""
