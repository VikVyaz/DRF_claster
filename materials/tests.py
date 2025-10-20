from django.urls import reverse
from django.contrib.auth.models import Group
from rest_framework.test import APITestCase

from users.models import User
from .models import Lesson, Course, CourseSubscribe

from rest_framework import status


class LessonTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='test@test.com')
        self.course = Course.objects.create(name='test_course')
        self.lesson = Lesson.objects.create(
            name='test_lesson',
            lesson_link='http://youtube.com/test/',
            course=self.course,
            owner=self.user
        )
        self.client.force_authenticate(user=self.user)

    def test_lesson_list(self):

        url = reverse('materials:lesson_list')
        response = self.client.get(url)

        result = {
            'count': Lesson.objects.all().count(),
            'next': None,
            'previous': None,
            'results': [
                {
                    'id': self.lesson.pk,
                    'name': self.lesson.name,
                    'description': None,
                    'preview': None,
                    'lesson_link': 'http://youtube.com/test/',
                    'course': self.course.pk,
                    'owner': self.user.pk
                }
            ]
        }

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(response.json(), result)

    def test_lesson_create(self):
        url = reverse('materials:lesson_create')
        data = {
            'name': 'test',
            'lesson_link': 'http://youtube.com/test/',
            'course': self.course.pk
        }

        response = self.client.post(url, data)

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            Lesson.objects.all().count(),
            2
        )

    def test_lesson_retrieve(self):
        """Retrieve-тест Lesson для user в и вне групп IsModer и IsOwner"""

        url = reverse('materials:lesson_detail', args=(self.lesson.pk,))

        # auth + IsOwner
        owner_response = self.client.get(url)

        self.assertEqual(
            owner_response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            owner_response.json(),
            {
                'course': self.course.id,
                'description': None,
                'id': self.lesson.id,
                'lesson_link': 'http://youtube.com/test/',
                'name': 'test_lesson',
                'owner': self.user.id,
                'preview': None
            }
        )

        # auth + IsModer
        self.lesson.owner = None
        self.lesson.save()

        self.moder_group, _ = Group.objects.get_or_create(name='Moder')
        self.user.groups.add(self.moder_group)

        moder_response = self.client.get(url)

        self.assertEqual(
            moder_response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            moder_response.json(),
            {
                'course': self.course.id,
                'description': None,
                'id': self.lesson.id,
                'lesson_link': 'http://youtube.com/test/',
                'name': 'test_lesson',
                'owner': None,
                'preview': None
            }
        )

        # только auth
        self.user.groups.clear()

        fail_response = self.client.get(url)

        self.assertEqual(
            fail_response.status_code,
            status.HTTP_403_FORBIDDEN
        )

    def test_url_validation_on_create(self):
        """Тест на инвалидный url при создании экземпляра Lesson"""

        response = self.client.post(
            reverse('materials:lesson_create'),
            data={
                'name': 'test',
                'lesson_link': 'http://wrong.com/test/',
                'course': self.course.id
            }
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertEqual(
            response.json()['non_field_errors'][0],
            'Ссылка должна вести на YouTube.com'
        )

    def test_url_validation_on_update(self):
        """Тест на инвалидный url при обновлении(put, patch) экземпляра Lesson"""

        url = reverse('materials:lesson_update', args=(self.lesson.pk,))

        put_response = self.client.put(
            url,
            data={
                'name': 'test',
                'lesson_link': 'http://wrong.com/test/',
                'course': self.course.id
            }
        )

        patch_response = self.client.patch(
            url,
            data={'lesson_link': 'http://wrong.com/test/'}
        )

        for resp in [put_response, patch_response]:
            self.assertEqual(
                resp.status_code,
                status.HTTP_400_BAD_REQUEST
            )

        for resp in [put_response, patch_response]:
            self.assertEqual(
                resp.json()['non_field_errors'][0],
                'Ссылка должна вести на YouTube.com'
            )

    def test_destroy_lesson(self):
        """"""

        url = reverse('materials:lesson_delete', args=(self.lesson.pk,))

        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

        self.assertEqual(
            Lesson.objects.all().count(),
            0
        )


class CourseSubscribeTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='test@test.com')
        self.course = Course.objects.create(name='test_course')
        self.subscribe = CourseSubscribe.objects.create(subscriber=self.user, course=self.course)

        self.client.force_authenticate(user=self.user)

    def test_subscribe_list(self):
        url = reverse('materials:course_subscribe_list')
        response = self.client.get(url)

        result = {
            'count': CourseSubscribe.objects.all().count(),
            'next': None,
            'previous': None,
            'results': [
                {
                    'subscriber':
                        {
                            'id': self.user.pk,
                            'email': self.user.email
                        },
                    'course':
                        {'id': self.course.pk,
                         'name': self.course.name
                         }
                }
            ]
        }

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(response.json(), result)

    def test_subscribe_ON(self):
        self.subscribe.delete()

        url = reverse('materials:course_subscribe', args=(self.course.pk,))
        response = self.client.post(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json()['message'],
            'Подписка добавлена'
        )

        self.assertEqual(
            CourseSubscribe.objects.all().count(),
            1
        )

    def test_subscribe_OFF(self):
        url = reverse('materials:course_subscribe', args=(self.course.pk,))
        response = self.client.post(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json()['message'],
            'Подписка удалена'
        )

        self.assertEqual(
            CourseSubscribe.objects.all().count(),
            0
        )
