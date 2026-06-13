from django.db import models
from imagekit.models import ProcessedImageField, ImageSpecField
from imagekit.processors import ResizeToFit, SmartResize


class HeroSlide(models.Model):
    PAGE_CHOICES = [
        ("home", "Page d'accueil"),
        ("login", "Connexion"),
        ("register", "Inscription"),
        ("forgot_password", "Mot de passe oublié"),
        ("otp_verify", "Vérification OTP"),
    ]

    page = models.CharField(
        max_length=30,
        choices=PAGE_CHOICES,
        default="home",
        verbose_name="Page",
        help_text="Page sur laquelle ce hero sera affiché",
    )
    image = ProcessedImageField(
        upload_to="hero/%Y/%m/",
        processors=[ResizeToFit(1920, 1080)],
        format="WEBP",
        options={"quality": 88},
        help_text="Image de fond du hero (idealement 1920x1080px ou ratio 16:9)",
    )
    image_thumb = ImageSpecField(
        source="image",
        processors=[SmartResize(400, 225)],
        format="WEBP",
        options={"quality": 70},
    )
    title = models.CharField(
        max_length=200,
        blank=True,
        help_text="Titre affiché sur le hero (laissez vide pour utiliser le titre par défaut)",
    )
    subtitle = models.CharField(
        max_length=300,
        blank=True,
        help_text="Sous-titre affiché sur le hero (laissez vide pour utiliser le sous-titre par défaut)",
    )
    cta_text = models.CharField(
        max_length=100,
        blank=True,
        default="Explorer nos remèdes",
        help_text="Texte du bouton d'appel à l'action",
    )
    cta_url = models.CharField(
        max_length=200,
        blank=True,
        default="/boutique/",
        help_text="URL du bouton d'appel à l'action",
    )
    is_active = models.BooleanField(default=True, verbose_name="Actif")
    sort_order = models.PositiveSmallIntegerField(default=0, verbose_name="Ordre")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["page", "sort_order", "-created_at"]
        verbose_name = "Hero - Slide"
        verbose_name_plural = "Hero - Slides"

    def __str__(self):
        page_label = dict(self.PAGE_CHOICES).get(self.page, self.page)
        return f"[{page_label}] {self.title or 'Slide #' + str(self.pk)}"
