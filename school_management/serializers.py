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
    goals = serializers.PrimaryKeyRelatedField(queryset=Goal.objects.all(), many=True, required=False)

    class Meta:
        model = Subtopic
        fields = ['id', 'name', 'topic_id', 'goals']

    def update(self, instance, validated_data):
        goals = validated_data.pop('goals', None)
        if goals is not None:
            instance.goals.set(goals)
        return super().update(instance, validated_data)

class KeyboardElementSerializer(serializers.ModelSerializer):
    class Meta:
        model = KeyboardElement
        fields = ['id', 'symbol']

class TaskSerializer(serializers.ModelSerializer):
    subtopic = serializers.PrimaryKeyRelatedField(queryset=Subtopic.objects.all())
    keyboard_elements = serializers.PrimaryKeyRelatedField(many=True, queryset=KeyboardElement.objects.all())

    class Meta:
        model = Task
        fields = ['id', 'name', 'subtopic', 'description', 'options', 'correct_option', 'solutions', 'hints', 'keyboard_elements']

    def validate_correct_option(self, value):
        if value not in ['A', 'B', 'C', 'D']:
            raise serializers.ValidationError("Invalid correct option. It must be one of 'A', 'B', 'C', 'D'.")
        return value
            
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
    goal = serializers.PrimaryKeyRelatedField(queryset=Goal.objects.all())

    class Meta:
        model = Test
        fields = ['id', 'name', 'tasks', 'goal']

    def create(self, validated_data):
        tasks_data = validated_data.pop('taskintest_set')
        test = Test.objects.create(**validated_data)
        for task_data in tasks_data:
            TaskInTest.objects.create(test=test, **task_data)
        return test

    def update(self, instance, validated_data):
        tasks_data = validated_data.pop('taskintest_set', [])
        instance.name = validated_data.get('name', instance.name)
        instance.goal = validated_data.get('goal', instance.goal)
        instance.save()
        TaskInTest.objects.filter(test=instance).delete()
        for task_data in tasks_data:
            TaskInTest.objects.create(test=instance, **task_data)
        return instance
