from django.contrib import admin
from django.utils.html import format_html_join

from .models import Cart, CartItem

# Register your models here.


class CartAdmin(admin.ModelAdmin):
    list_display = (
        'session_id',
        'date_added',
    )


class CartItemAdmin(admin.ModelAdmin):
    list_display = (
        'cart',
        'product',
        'item_variations',
        'quantity',
        'is_active',
    )

    def item_variations(self, obj):
        return format_html_join(
            '',
            '{}: {}<br>',
            [(vrt.get_category_display(), vrt.value) for vrt in obj.variations.all().order_by('created_date')],
        )

    item_variations.short_description = 'variaciones'


admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
