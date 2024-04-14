from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GoalViewSet, ClassViewSet, SectionViewSet, TopicViewSet, SubtopicViewSet, TaskViewSet

router = DefaultRouter()
router.register(r'goals', GoalViewSet)
router.register(r'classes', ClassViewSet)
router.register(r'sections', SectionViewSet)
router.register(r'topics', TopicViewSet)
router.register(r'subtopics', SubtopicViewSet)
router.register(r'tasks', TaskViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
