from rest_framework import viewsets
from .models import Goal, Class, Section, Topic, Subtopic, KeyboardElement, Task, Test, TaskInTest
from .serializers import GoalSerializer, ClassSerializer, SectionSerializer, TopicSerializer, SubtopicSerializer, KeyboardElementSerializer, TaskSerializer, TestSerializer, TaskInTestSerializer
from django_filters import rest_framework as filters
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

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
    goal_id = filters.NumberFilter(method='filter_by_goal')

    class Meta:
        model = Section
        fields = ['id', 'class_id']

    def filter_by_goal(self, queryset, name, value):
        return queryset.filter(topics__subtopics__goals__id=value).distinct()

class SectionViewSet(viewsets.ModelViewSet):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = SectionFilter

class TopicFilter(filters.FilterSet):
    class Meta:
        model = Topic
        fields = ['id', 'section_id']

class TopicViewSet(viewsets.ModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = TopicFilter

class SubtopicFilter(filters.FilterSet):
    topic_id = filters.NumberFilter(field_name='topic_id')
    goal_id = filters.NumberFilter(field_name='goals__id')
    goals = filters.ModelMultipleChoiceFilter(queryset=Goal.objects.all(), field_name='goals', to_field_name='id')

    class Meta:
        model = Subtopic
        fields = ['id', 'topic_id', 'goal_id', 'goals']

class SubtopicViewSet(viewsets.ModelViewSet):
    queryset = Subtopic.objects.all()
    serializer_class = SubtopicSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = SubtopicFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        goal_id = self.request.query_params.get('goal_id', None)
        topic_id = self.request.query_params.get('topic_id', None)
        goals = self.request.query_params.getlist('goals', None)

        if goal_id and topic_id:
            queryset = queryset.filter(topic_id=topic_id, goals__id=goal_id)
        elif goal_id:
            queryset = queryset.filter(goals__id=goal_id)
        elif topic_id:
            queryset = queryset.filter(topic_id=topic_id)
        elif goals:
            queryset = queryset.filter(goals__id__in=goals)

        return queryset.distinct()

    def get_serializer_context(self):
        return {'request': self.request}

class KeyboardElementViewSet(viewsets.ModelViewSet):
    queryset = KeyboardElement.objects.all()
    serializer_class = KeyboardElementSerializer
    
class TaskFilter(filters.FilterSet):
    subtopic = filters.NumberFilter(field_name='subtopic')
    
    class Meta:
        model = Task
        fields = ['id', 'subtopic']

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = TaskFilter
    
class TestFilter(filters.FilterSet):
    goal_id = filters.NumberFilter(field_name='goal__id')
    
    class Meta:
        model = Test
        fields = ['id', 'goal_id'] 

class TestViewSet(viewsets.ModelViewSet):
    queryset = Test.objects.all()
    serializer_class = TestSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = TestFilter

# Представление для промежуточной модели TaskInTest (если необходимо)
class TaskInTestViewSet(viewsets.ModelViewSet):
    queryset = TaskInTest.objects.all()
    serializer_class = TaskInTestSerializer
    
@csrf_exempt
def upload_image(request):
    if request.method == 'POST' and request.FILES.get('file'):
        image = request.FILES['file']
        path = default_storage.save('images/' + image.name, ContentFile(image.read()))
        image_url = default_storage.url(path)
        return JsonResponse({'link': image_url})
    return JsonResponse({'error': 'Failed to upload image'}, status=400)