from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from django.core.validators import RegexValidator

from accounts.managers import CustomUserManager

uzb_phone_validator = RegexValidator(
    regex=r'^\+998\d{9}$',
    message="Telefon raqam '+998901234567' formatida bo‘lishi kerak."
)


USER_ROLES = (
    ("user", "foydalanuvchi"),
    ("owner", "stadion egasi"),
    ("admin", "adminstrator")
)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    phone_number = models.CharField(
        max_length=13,
        unique=True,
        validators=[uzb_phone_validator],
        verbose_name="Telefon raqami"
    )

    name = models.CharField(max_length=255, blank=True, null=True, verbose_name="Ism")
    role = models.CharField(max_length=10, choices=USER_ROLES, default="user")

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['name']

    objects = CustomUserManager()

    class Meta:
        verbose_name = 'Foydalanuvchi'
        verbose_name_plural = 'Foydalanuvchilar'

    def __str__(self):
        return self.phone_number










