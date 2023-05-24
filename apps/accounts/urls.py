from django.urls import path, reverse_lazy
from django.views.generic import RedirectView

from . import views

app_name = 'accounts'

urlpatterns = [
    path('', RedirectView.as_view(url=reverse_lazy('accounts:profile'))),
    path('register/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('profile/', views.profile, name='profile'),
    path('password_reset/', views.password_reset, name='password_reset'),
    path('reset/<uidb64>/<token>/', views.password_reset_confirm, name='password_reset_confirm'),
]
