from decouple import config
from django.db import models

course_preview = config("COURSE_DIR", default="materials/course_preview/")
lesson_preview = config("LESSON_DIR", default="materials/lesson_preview/")


class Course(models.Model):
    name = models.CharField(verbose_name="Название")
    preview = models.ImageField(
        upload_to=course_preview, verbose_name="Превью", null=True, blank=True
    )
    description = models.TextField(verbose_name="Описание", null=True, blank=True)
    owner = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        related_name="course_owner",
        verbose_name="Создатель курса",
        null=True,
        blank=True
    )
    price = models.DecimalField(
        verbose_name='Цена курса в $',
        default=1.0,
        max_digits=10,
        decimal_places=2
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Lesson(models.Model):
    name = models.CharField(verbose_name="Название")
    description = models.TextField(verbose_name="Описание", null=True, blank=True)
    preview = models.ImageField(
        upload_to=lesson_preview, verbose_name="Превью", null=True, blank=True
    )
    lesson_link = models.URLField(verbose_name="Ссылка на видео")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lessons")
    owner = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        related_name="lesson_owner",
        verbose_name="Создатель урока",
        null=True,
        blank=True
    )
    price = models.DecimalField(
        verbose_name='Цена урока в $',
        default=1.0,
        max_digits=10,
        decimal_places=2
    )

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"


class CourseSubscribe(models.Model):
    subscriber = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="subscriber",
        verbose_name="Пользователь, подписанный на обновления курса"
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="subscribe_course",
        verbose_name="Пользователь, подписанный на обновления курса"
    )

    class Meta:
        verbose_name = "Подписка на обновление курсов"
        verbose_name_plural = "Подписки на обновление курсов"
