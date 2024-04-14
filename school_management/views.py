from rest_framework import viewsets
from .models import Goal, Class, Section, Topic, Subtopic, Task
from .serializers import GoalSerializer, ClassSerializer, SectionSerializer, TopicSerializer, SubtopicSerializer, TaskSerializer
from django_filters import rest_framework as filters

class GoalViewSet(viewsets.ModelViewSet):
    queryset = Goal.objects.all()
    serializer_class = GoalSerializer

class ClassFilter(filters.FilterSet):
    class Meta:
        model = Class
        fields = ['id']

class ClassViewSet(viewsets.ModelViewSet):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ClassFilter

class SectionFilter(filters.FilterSet):
    class Meta:
        model = Section
        fields = ['id', 'goal_id', 'class_id']

class SectionViewSet(viewsets.ModelViewSet):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = SectionFilter

class TopicFilter(filters.FilterSet):
    class Meta:
        model = Topic
        fields = ['section_id']

class TopicViewSet(viewsets.ModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = TopicFilter

class SubtopicFilter(filters.FilterSet):
    class Meta:
        model = Subtopic
        fields = ['topic_id']

class SubtopicViewSet(viewsets.ModelViewSet):
    queryset = Subtopic.objects.all()
    serializer_class = SubtopicSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = SubtopicFilter

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
