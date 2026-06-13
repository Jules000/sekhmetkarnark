from django.conf import settings
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django_ckeditor_5.fields import CKEditor5Field
from imagekit.models import ProcessedImageField, ImageSpecField
from imagekit.processors import ResizeToFit, SmartResize


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, unique=True)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=60, unique=True)

    def __str__(self):
        return self.name


class Article(models.Model):
    STATUS_CHOICES = [
        ("draft", "Brouillon"),
        ("published", "Publié"),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=250, unique=True)
    excerpt = models.TextField(max_length=500, blank=True)
    content = CKEditor5Field(config_name="default")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="articles"
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True
    )
    tags = models.ManyToManyField(Tag, blank=True)
    featured_image = ProcessedImageField(
        upload_to="blog/featured/%Y/%m/",
        processors=[ResizeToFit(1200, 675)],
        format="WEBP",
        options={"quality": 85},
        blank=True,
        null=True,
    )
    featured_image_thumb = ImageSpecField(
        source="featured_image",
        processors=[SmartResize(600, 338)],
        format="WEBP",
        options={"quality": 75},
    )
    reading_time = models.PositiveSmallIntegerField(default=5)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="draft")
    published_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-published_at"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
