from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    username = models.CharField(blank=True, null=True)
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


class Payment(models.Model):
    PAY_METHOD = [("cash", "Наличные"), ("transfer", "Перевод на счет")]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="payment",
        verbose_name="Пользователь",
    )
    payment_date = models.DateTimeField(
        default=timezone.now, verbose_name="Дата оплаты"
    )
    paid_lesson = models.ForeignKey(
        "materials.Lesson",
        on_delete=models.SET_NULL,
        null=True,
        related_name="lesson",
        verbose_name="Оплаченный урок",
    )
    paid_course = models.ForeignKey(
        "materials.Course",
        on_delete=models.SET_NULL,
        null=True,
        related_name="course",
        verbose_name="Оплаченный курс",
    )
    payment_amount = models.PositiveIntegerField(verbose_name="Сумма оплаты")
    payment_method = models.CharField(choices=PAY_METHOD, verbose_name="Метод оплаты")

    def __str__(self):
        return f"Оплата пользователя {self.user}"

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"
