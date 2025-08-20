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

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
