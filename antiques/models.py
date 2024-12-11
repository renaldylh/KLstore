from django.db import models
from django.shortcuts import get_object_or_404

class Antique(models.Model):
    name = models.CharField(max_length=255)
    creator = models.CharField(max_length=255, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to='antiques/')
    stocks = models.IntegerField(default=0)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
