from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User

# Register your models here.


class CustomUserAdmin(UserAdmin):
    # Campos de lista
    list_display = (
        'email',
        'username',
        'first_name',
        'last_name',
        'phone_number',
        'date_joined',
        'last_login',
        'is_admin',
        'is_staff',
    )

    # Campos con link al formulario de edición
    list_display_links = ('email', 'username')

    # Campos de solo lectura
    readonly_fields = ('last_login', 'date_joined')

    # Orden de la lista, para que sea descentente se agrega un - antes del nombre del campo
    ordering = ('-date_joined',)

    # Campos en los que se realiza una busqueda, por defecto busca en todos
    search_fields = ('email', 'username', 'first_name', 'last_name')

    # Filtro de fecha en la parte superior de la lista
    # date_hierarchy = 'date_joined'

    # Campos de formulario con división de secciones
    fieldsets = (
        ('Account', {'fields': ('email', 'username', 'date_joined', 'last_login')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'phone_number')}),
        ('Permissions', {'fields': ('is_admin', 'is_staff')}),
    )

    # Se deben sobreescribir estas variables cuando se hereda de UserAdmin
    list_filter = ()  # Filtro a la derecha de la lista
    filter_horizontal = ()  # Filtro de selección para campos ManyToManyField


admin.site.register(User, CustomUserAdmin)
