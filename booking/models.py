from django.db import models
from django.conf import settings
from django.db.models import CASCADE
from stadiums.models import Stadium



PAYMENT_STATUS = [
    ("PAID", "paid"),
    ("PENDING", "pending"),
    ('CANCELED', "canceled")
]

class Booking(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=CASCADE,
        related_name='booking_user',
        verbose_name="book qilgan user"
    )
    stadium = models.ForeignKey(
        Stadium,
        on_delete=CASCADE,
        related_name="booking_stadium",
        verbose_name="book qilingan stadion"
    )

    start_time = models.DateTimeField(verbose_name="boshlanish vaqti", db_index=True)
    end_time = models.DateTimeField(verbose_name='tugash vaqti', db_index=True)

    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="o'yin narrxi")
    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS
    )

    class Meta:
        verbose_name = "booking"
        verbose_name_plural = "bookings"

    def __str__(self):
        return f"{self.stadium.name} booked by {self.user}"


