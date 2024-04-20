from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GoalViewSet, ClassViewSet, SectionViewSet, TopicViewSet, SubtopicViewSet, KeyboardElementViewSet, TaskViewSet, TestViewSet

router = DefaultRouter()
router.register(r'goals', GoalViewSet)
router.register(r'classes', ClassViewSet)
router.register(r'sections', SectionViewSet)
router.register(r'topics', TopicViewSet)
router.register(r'subtopics', SubtopicViewSet)
router.register(r'keyboardElements', KeyboardElementViewSet)
router.register(r'tasks', TaskViewSet)
router.register(r'tests', TestViewSet)
# router.register(r'test_questions', TestQuestionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
