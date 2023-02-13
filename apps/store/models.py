from django.db import models
from django.urls import reverse

from apps.category.models import Category

# Create your models here.


class Product(models.Model):
    name = models.CharField("nombre", max_length=200, unique=True)
    slug = models.SlugField("identificador", max_length=255, unique=True)
    description = models.TextField("descripción", max_length=500, blank=True)
    price = models.IntegerField("precio")
    images = models.ImageField("fotos", upload_to='photos/products')
    stock = models.IntegerField("stock")
    is_available = models.BooleanField("disponibilidad", default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="categoría")
    created_date = models.DateTimeField("fecha de creación", auto_now_add=True)
    modified_date = models.DateTimeField("fecha de modificación", auto_now=True)

    """
    Se pueden agregar propiedades que funcionan como campos adicionales
    del modelo que no se elmacenan en la base de datos
    """

    @property
    def formatted_price(self):
        return f'${self.price:,}'.replace(',', '.')

    # Nombre de la propiedad, por defecto es el nombre del método
    formatted_price.fget.short_description = 'precio'

    class Meta:
        verbose_name = 'producto'
        verbose_name_plural = 'productos'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("store:product_detail", args=[self.category.slug, self.slug])
