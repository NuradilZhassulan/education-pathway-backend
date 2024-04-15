from rest_framework import serializers
from .models import Goal, Class, Section, Topic, Subtopic, Task


class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = ['id', 'name']
        
class GoalSerializer(serializers.ModelSerializer):
    class_ = ClassSerializer(source='class_id', read_only=True)  # Детальная информация о классе

    class Meta:
        model = Goal
        fields = ['id', 'name', 'class_id', 'class_']  # Добавляем 'class_' в поля

    class_id = serializers.PrimaryKeyRelatedField(queryset=Class.objects.all())  

class SectionSerializer(serializers.ModelSerializer):
    class_ = ClassSerializer(source='class_id', read_only=True)
    goal_ = ClassSerializer(source='goal_id', read_only=True)

    class Meta:
        model = Section
        fields = ['id', 'name', 'class_id', 'class_', 'goal_id', 'goal_']

class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = '__all__'

class SubtopicSerializer(serializers.ModelSerializer):
    goals = serializers.SerializerMethodField()  # Изменяем на метод

    class Meta:
        model = Subtopic
        fields = ['id', 'name', 'topic_id', 'goals']

    def get_goals(self, obj):
        # Фильтрация goals в зависимости от параметра goal_id в запросе
        goals = obj.goals.all()
        goal_id = self.context['request'].query_params.get('goal_id')
        if goal_id:
            goals = goals.filter(id=goal_id)
        return GoalSerializer(goals, many=True).data

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
