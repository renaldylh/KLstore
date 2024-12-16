from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator, RegexValidator
from django.core.exceptions import ValidationError


class Category(models.Model):
    category_name = models.CharField(
        max_length=100,
        unique=True,
        validators=[
            MinLengthValidator(3, "Category name must be at least 3 characters long."),
            RegexValidator(
                regex=r"^[a-zA-Z0-9\s]+$",
                message="Category name must contain only alphanumeric characters and spaces.",
            ),
        ],
        error_messages={
            "unique": "Category name must be unique.",
        },
    )
    slug = models.SlugField(
        max_length=20,
        unique=True,
        validators=[
            MinLengthValidator(3, "Slug must be at least 3 characters long."),
            RegexValidator(
                regex=r"^[a-z0-9-]+$",
                message="Slug must contain only lowercase letters, numbers, and hyphens.",
            ),
        ],
        error_messages={
            "unique": "Slug must be unique.",
        },
    )
    category_image = models.ImageField(
        upload_to="images/cat/",
        blank=True,
    )
    category_des = models.TextField(
        max_length=2000,
        blank=True,
        validators=[
            MaxLengthValidator(2000, "Description cannot exceed 2000 characters."),
        ],
    )

    def clean(self):
        if self.slug and self.slug.startswith("-"):
            raise ValidationError("Slug cannot start with a hyphen (-).")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.category_name
