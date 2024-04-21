from rest_framework import serializers
from .models import Goal, Class, Section, Topic, Subtopic, KeyboardElement, Task, Test, TaskInTest
import json
from django.http import JsonResponse
import logging

logger = logging.getLogger(__name__)


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

class KeyboardElementSerializer(serializers.ModelSerializer):
    class Meta:
        model = KeyboardElement
        fields = ['id', 'symbol']

class TaskSerializer(serializers.ModelSerializer):
    subtopic = serializers.PrimaryKeyRelatedField(queryset=Subtopic.objects.all())
    keyboard_elements = serializers.PrimaryKeyRelatedField(many=True, queryset=KeyboardElement.objects.all())

    class Meta:
        model = Task
        fields = ['id', 'name', 'subtopic', 'description', 'correct_answers', 'solutions', 'hints', 'keyboard_elements']
        
class TaskInTestSerializer(serializers.ModelSerializer):
    task = TaskSerializer(read_only=True)
    next_task_correct = TaskSerializer(read_only=True)
    next_task_incorrect = TaskSerializer(read_only=True)

    task_id = serializers.PrimaryKeyRelatedField(
        queryset=Task.objects.all(), write_only=True, source='task', required=True)
    next_task_correct_id = serializers.PrimaryKeyRelatedField(
        queryset=Task.objects.all(), allow_null=True, write_only=True, source='next_task_correct')
    next_task_incorrect_id = serializers.PrimaryKeyRelatedField(
        queryset=Task.objects.all(), allow_null=True, write_only=True, source='next_task_incorrect')

    class Meta:
        model = TaskInTest
        fields = ['task', 'task_id', 'next_task_correct', 'next_task_correct_id', 'next_task_incorrect', 'next_task_incorrect_id']


# Обновляем сериализатор для модели Test
class TestSerializer(serializers.ModelSerializer):
    tasks = TaskInTestSerializer(source='taskintest_set', many=True)

    class Meta:
        model = Test
        fields = ['id', 'name', 'tasks']

    def create(self, validated_data):
        tasks_data = validated_data.pop('taskintest_set')
        test = Test.objects.create(**validated_data)
        for task_data in tasks_data:
            TaskInTest.objects.create(test=test, **task_data)
        return test

    def update(self, instance, validated_data):
        tasks_data = validated_data.pop('taskintest_set', [])

        # Обновляем сам тест
        instance.name = validated_data.get('name', instance.name)
        instance.save()

        # Обновляем связанные задачи
        if tasks_data:
            # Пересоздаем задачи для теста, можно также обновить, если у задач есть идентификаторы
            TaskInTest.objects.filter(test=instance).delete()
            for task_data in tasks_data:
                TaskInTest.objects.create(test=instance, **task_data)

        return instance
