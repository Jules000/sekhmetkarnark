from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    phone = models.CharField(max_length=20, blank=True)
    is_premium = models.BooleanField(default=False)
    botanical_points = models.PositiveIntegerField(default=0)
    newsletter_opt_in = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self):
        return self.email or self.username
