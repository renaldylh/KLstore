from django.db import models
from django.core.validators import (
    MinValueValidator,
    MaxValueValidator,
    RegexValidator,
    DecimalValidator
)
from category.models import Category


class Antique(models.Model):
    title = models.CharField(
        max_length=150,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Z0-9\s]+$',
                message="Title can only contain letters, numbers, and spaces.",
                code='invalid_title'
            )
        ]
    )
    slug = models.SlugField(
        max_length=60,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^[a-z0-9-]+$',
                message="Slug can only contain lowercase letters, numbers, and hyphens.",
                code='invalid_slug'
            )
        ]
    )
    image = models.ImageField(upload_to="images/antiques/")
    maker = models.CharField(max_length=200, blank=True)
    description = models.TextField(max_length=3000, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    origin = models.CharField(max_length=200, blank=True)
    material = models.CharField(max_length=200, blank=True)
    year_made = models.IntegerField(
        blank=True,
        null=True,
        validators=[
            MinValueValidator(1000, message="Year must be at least 1000."),
            MaxValueValidator(9999, message="Year must be a valid 4-digit number.")
        ]
    )
    condition = models.CharField(max_length=100, blank=True)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[
            MinValueValidator(0.01, message="Price must be greater than 0."),
        ]
    )
    stocks = models.IntegerField(
        blank=False,
        validators=[
            MinValueValidator(0, message="Stocks cannot be negative.")
        ]
    )
    stocks_available = models.BooleanField(default=True)
    modified_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
