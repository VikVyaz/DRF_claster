from django.core.management.base import BaseCommand
from users.models import Payment, User
from materials.models import Course, Lesson


class Command(BaseCommand):
    help = "Создаёт тестовый курс, урок и платеж"

    def handle(self, *args, **kwargs):
        user, created = User.objects.get_or_create(
            email="testuser@example.com",
            defaults={
                "username": "testuser",
                "city": "Test City",
            }
        )
        if created:
            user.set_password("testpass123")
            user.save()
            self.stdout.write(self.style.SUCCESS(f"Создан пользователь {user.email}"))

        # course, _ = Course.objects.get_or_create(name="Тестовый курс")
        # self.stdout.write(self.style.SUCCESS(f"Создан курс: {course.name}"))

        success = False
        name_num = 1
        while success:
            try:
                course, _ = Course.objects.get_or_create(name=f"Тестовый курс_{name_num}")
                self.stdout.write(self.style.SUCCESS(f"Создан курс: {course.name}"))
                success = True
            except Exception:
                name_num += 1

        # lesson, _ = Lesson.objects.get_or_create(
        #     name="Тестовый урок",
        #     course=course,
        #     defaults={
        #         "lesson_link": "https://test.com"
        #     }
        # )
        # self.stdout.write(self.style.SUCCESS(f"Создан урок: {lesson.name}"))

        success = False
        name_num = 1
        while success:
            try:
                lesson, _ = Lesson.objects.create(
                    name=f"Тестовый урок_{name_num}",
                    course=course,
                    lesson_link="https://test.com"
                )
                self.stdout.write(self.style.SUCCESS(f"Создан урок: {lesson.name}"))
                success = True
            except Exception:
                name_num += 1

        payment_course, _ = Payment.objects.get_or_create(
            user=user,
            paid_course=course,
            paid_lesson=None,
            defaults={
                "payment_amount": 1000,
                "payment_method": "cash"
            }
        )
        self.stdout.write(self.style.SUCCESS(f"Создан платеж на курс: {payment_course}"))

        payment_lesson, _ = Payment.objects.get_or_create(
            user=user,
            paid_course=None,
            paid_lesson=lesson,
            defaults={
                "payment_amount": 500,
                "payment_method": "transfer"
            }
        )
        self.stdout.write(self.style.SUCCESS(f"Создан платеж на урок: {payment_lesson}"))
