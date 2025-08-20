from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    email = models.EmailField(verbose_name="Email", unique=True)
    avatar = models.ImageField(
        verbose_name="Аватар", upload_to="users/avatars/", blank=True, null=True
    )
    phone_number = PhoneNumberField(
        verbose_name="Номер телефона", max_length=15, blank=True, null=True
    )
    city = models.CharField(verbose_name="Город")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.username} - {self.email}"

    class Meta:
        verbose_name = "Пользователи"
        verbose_name_plural = "Пользователь"
