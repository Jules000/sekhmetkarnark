from django.db import models
from django.utils.text import slugify
from imagekit.models import ProcessedImageField, ImageSpecField
from imagekit.processors import ResizeToFit, SmartResize


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, unique=True)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, related_name="products"
    )
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=250, unique=True)
    description = models.TextField()
    short_description = models.CharField(max_length=300, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    compare_price = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    stock_quantity = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    benefits = models.TextField(blank=True)
    usage_instructions = models.TextField(blank=True)
    composition = models.TextField(blank=True)

    main_image = ProcessedImageField(
        upload_to="shop/products/%Y/%m/",
        processors=[ResizeToFit(1200, 1500)],
        format="WEBP",
        options={"quality": 85},
        blank=True,
        null=True,
    )
    main_image_thumb = ImageSpecField(
        source="main_image",
        processors=[SmartResize(600, 750)],
        format="WEBP",
        options={"quality": 75},
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="images"
    )
    image = ProcessedImageField(
        upload_to="shop/products/gallery/%Y/%m/",
        processors=[ResizeToFit(1200, 1500)],
        format="WEBP",
        options={"quality": 85},
    )
    image_thumb = ImageSpecField(
        source="image",
        processors=[SmartResize(150, 188)],
        format="WEBP",
        options={"quality": 70},
    )
    is_primary = models.BooleanField(default=False)
    sort_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["sort_order"]
