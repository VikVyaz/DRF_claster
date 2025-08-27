from rest_framework import serializers

from .models import Course, Lesson
from .validators import UrlValidator


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"
        validators = [
            UrlValidator(url='lesson_link')
        ]


class CourseDetailSerializer(serializers.ModelSerializer):
    lesson_counter = serializers.SerializerMethodField()
    lessons_list = LessonSerializer(many=True, source="lessons")

    def get_lesson_counter(self, obj):
        return obj.lessons.count()

    class Meta:
        model = Course
        fields = (
            "name",
            "description",
            "lesson_counter",
            "lessons_list",
            "owner"
        )
