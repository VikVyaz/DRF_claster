from rest_framework import serializers

from .models import Course, Lesson


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"


class CourseDetailSerializer(serializers.ModelSerializer):
    lesson_counter = serializers.SerializerMethodField()

    def get_lesson_counter(self, obj):
        return obj.lessons.count()

    class Meta:
        model = Course
        fields = ('name', 'description', 'lesson_counter',)


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"
