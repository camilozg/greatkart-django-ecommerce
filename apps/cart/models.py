from django.db import models

from apps.store.models import Product, Variation

# Create your models here.


class Cart(models.Model):
    session_id = models.CharField("id", max_length=250, blank=True)
    date_added = models.DateField("fecha de creación", auto_now_add=True)

    class Meta:
        verbose_name = "carrito"
        verbose_name_plural = "carritos"

    def __str__(self):
        return self.session_id


class CartItem(models.Model):
    product = models.ForeignKey(Product, verbose_name="producto", on_delete=models.CASCADE)
    variations = models.ManyToManyField(Variation, verbose_name="variations", blank=True)
    cart = models.ForeignKey(Cart, verbose_name="carrito", on_delete=models.CASCADE)
    quantity = models.IntegerField("cantidad")
    is_active = models.BooleanField("activo", default=True)

    class Meta:
        verbose_name = "item"
        verbose_name_plural = "items"

    def __str__(self):
        variations_to_str = ', '.join(
            [f'{variation.category}: {variation.value}' for variation in self.variations.all()]
        )
        return f'{self.product.name}, {variations_to_str}'

    def total(self):
        return self.quantity * self.product.price
