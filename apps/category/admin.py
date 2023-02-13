from django.contrib import admin

from .models import Category

# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')

    # Automcompleta campos del formulario
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Category, CategoryAdmin)
