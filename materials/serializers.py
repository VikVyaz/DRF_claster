from rest_framework import serializers

from .models import Course, Lesson, CourseSubscribe
from .validators import UrlValidator


class CourseSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        return CourseSubscribe.objects.filter(subscriber=user, course=obj).exists()

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
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        return CourseSubscribe.objects.filter(subscriber=user, course=obj).exists()

    def get_lesson_counter(self, obj):
        return obj.lessons.count()

    class Meta:
        model = Course
        fields = "__all__"


class CourseSubscribeSerializer(serializers.ModelSerializer):
    subscriber = serializers.SerializerMethodField()
    course = serializers.SerializerMethodField()

    def get_subscriber(self, obj):
        return {
            "id": obj.subscriber.id,
            "email": obj.subscriber.email
        }

    def get_course(self, obj):
        return {
            "id": obj.course.id,
            "name": obj.course.name
        }

    class Meta:
        model = CourseSubscribe
        fields = ('subscriber', 'course',)
