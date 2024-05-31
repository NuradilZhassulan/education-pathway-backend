from django.db import models

#Цель
class Goal(models.Model):
    name = models.CharField(max_length=255)
    class_id = models.ForeignKey('Class', on_delete=models.CASCADE, related_name='goals')

#Класс
class Class(models.Model):
    name = models.CharField(max_length=255)

#Раздел
class Section(models.Model):
    name = models.CharField(max_length=255)
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='sections')
    goal_id = models.ForeignKey(Goal, on_delete=models.CASCADE, related_name='sections', null=True, blank=True)

#Тема
class Topic(models.Model):
    name = models.CharField(max_length=255)
    section_id = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='topics')

#Микротема
class Subtopic(models.Model):
    name = models.CharField(max_length=255)
    topic_id = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='subtopics')
    goals = models.ManyToManyField(Goal, blank=True, related_name='subtopics')  # ManyToMany связь с Goal

class KeyboardElement(models.Model):
    symbol = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.symbol

#Задача
class Task(models.Model):
    name = models.CharField(max_length=255)
    subtopic = models.ForeignKey(Subtopic, on_delete=models.CASCADE, related_name='tasks')
    description = models.TextField()
    options = models.JSONField(default=list)
    correct_option = models.CharField(max_length=1)  # Удалите значение по умолчанию, если нужно
    solutions = models.TextField()
    hints = models.TextField()
    keyboard_elements = models.ManyToManyField(KeyboardElement, related_name='tasks')

    def __str__(self):
        return self.name
    
#Тесты
class Test(models.Model):
    name = models.CharField(max_length=255)
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE, related_name='tests')

    def __str__(self):
        return self.name

class TaskInTest(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='taskintest_set')
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='test_tasks')
    next_task_correct = models.ForeignKey(Task, null=True, blank=True, on_delete=models.SET_NULL, related_name='next_correct_tasks')
    next_task_incorrect = models.ForeignKey(Task, null=True, blank=True, on_delete=models.SET_NULL, related_name='next_incorrect_tasks')