from rest_framework import generics, viewsets
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.response import Response

from .models import Course, Lesson, CourseSubscribe
from .paginators import MaterialsPaginator
from .permissions import IsModer, IsOwner
from .serializers import (CourseDetailSerializer, CourseSerializer,
                          LessonSerializer, CourseSubscribeSerializer)


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    pagination_class = MaterialsPaginator

    def get_queryset(self):
        user = self.request.user
        queryset = self.queryset

        if user.groups.filter(name='Moder').exists():
            return queryset
        return queryset.filter(owner=user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return CourseDetailSerializer
        return CourseSerializer

    def get_permissions(self):
        # moder - no destroy, no create , update, retrieve
        # owner - retrieve, update, destroy, create
        if self.action == "create":
            self.permission_classes = [IsAuthenticated, ~IsModer]
        elif self.action in ["retrieve", "update"]:
            self.permission_classes = [IsAuthenticated, IsOwner | IsModer]
        elif self.action == "destroy":
            self.permission_classes = [IsAuthenticated, ~IsModer | IsOwner]

        return super().get_permissions()


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ~IsModer]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    pagination_class = MaterialsPaginator

    def get_queryset(self):
        user = self.request.user
        queryset = Lesson.objects.all()

        if user.groups.filter(name='Moder').exists():
            return queryset
        return queryset.filter(owner=user)


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner | IsModer]


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner | IsModer]


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, ~IsModer | IsOwner]


class CourseSubscribeListAPIView(generics.ListAPIView):
    serializer_class = CourseSubscribeSerializer
    queryset = CourseSubscribe.objects.all()
    pagination_class = MaterialsPaginator


class CourseSubscribeAPIView(APIView):

    def post(self, request, pk):
        user = request.user
        course = get_object_or_404(Course, pk=pk)

        subs_item = CourseSubscribe.objects.filter(subscriber=user, course=course)

        if subs_item.exists():
            subs_item.delete()
            message = 'Подписка удалена'
        else:
            CourseSubscribe.objects.create(subscriber=user, course=course)
            message = 'Подписка добавлена'

        return Response({'message': message})
