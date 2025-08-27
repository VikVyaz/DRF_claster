from django.urls import path
from rest_framework.routers import DefaultRouter

from .apps import MaterialsConfig
from .views import (CourseViewSet, LessonCreateAPIView, LessonDestroyAPIView,
                    LessonListAPIView, LessonRetrieveAPIView,
                    LessonUpdateAPIView, CourseSubscribeAPIView, CourseSubscribeListAPIView)

app_name = MaterialsConfig.name

router = DefaultRouter()
router.register(r"courses", CourseViewSet, basename="courses")

urlpatterns = [
    path("lessons/", LessonListAPIView.as_view(), name="lesson_list"),
    path("lessons/create/", LessonCreateAPIView.as_view(), name="lesson_create"),
    path("lessons/<int:pk>/", LessonRetrieveAPIView.as_view(), name="lesson_detail"),
    path("lessons/update/<int:pk>/", LessonUpdateAPIView.as_view(), name="lesson_update"),
    path("lessons/delete/<int:pk>/", LessonDestroyAPIView.as_view(), name="lesson_delete"),

    path("courses/subscribe/", CourseSubscribeAPIView.as_view(), name="course_subscribe"),
    path("courses/subscribe/list/", CourseSubscribeListAPIView.as_view(), name="course_subscribe_list"),
] + router.urls
