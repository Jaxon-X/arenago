from django.db import models
from django.contrib.gis.db import models as gis_models
from django.conf import settings
from django.db.models import CASCADE


class Stadium(models.Model):

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=CASCADE,
        related_name="owned_stadiums",
        limit_choices_to={'role': 'owner'},
        verbose_name="stadion egasi"
    )

    name = models.CharField(max_length=255, verbose_name="stadion nomi")
    address = models.CharField(max_length=500, verbose_name="stadion manzili")
    price_per_hour = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name="soatiga narxi (UZS)"
    )

    location = gis_models.PointField(
        srid=4326,
        verbose_name="stadion lokasiyasi"
    )
    is_active = models.BooleanField(default=True, verbose_name="Faol holati")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "stadion"
        verbose_name_plural = "stadionlar"

    def __str__(self):
        return self.name



