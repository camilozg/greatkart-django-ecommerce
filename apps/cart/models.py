from django.db import models

from apps.store.models import Product

# Create your models here.


class Cart(models.Model):
    cart_id = models.CharField("id", max_length=250, blank=True)
    date_added = models.DateField("fecha de creación", auto_now_add=True)

    class Meta:
        verbose_name = "carrito"
        verbose_name_plural = "carritos"

    def __str__(self):
        return self.id


class CartItem(models.Model):
    product = models.ForeignKey(Product, verbose_name="item", on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, verbose_name="carrito", on_delete=models.CASCADE)
    quantity = models.IntegerField("cantidad")
    is_active = models.BooleanField("activo", default=True)

    class Meta:
        verbose_name = "item"
        verbose_name_plural = "items"

    def __str__(self):
        return self.product

    def total(self):
        return self.quantity * self.product.price
