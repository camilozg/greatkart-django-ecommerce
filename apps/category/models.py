from django.db import models
from django.urls import reverse

# Create your models here.


class Category(models.Model):
    name = models.CharField("categoría", max_length=50, unique=True)
    slug = models.SlugField("identificador", max_length=100, unique=True)
    description = models.TextField("descripción", max_length=255, blank=True)
    cat_image = models.ImageField("foto", upload_to='photos/categories', blank=True)

    class Meta:
        verbose_name = 'categoría'
        verbose_name_plural = 'categorías'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("store:products_by_category", args=[self.slug])
