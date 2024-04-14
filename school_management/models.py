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

#Задача
class Task(models.Model):
    description = models.TextField()
    correct_answers = models.TextField()  # This could be JSONField in a real-world scenario
    formulas = models.TextField()  # Assuming multiple formulas could be linked
    solutions = models.TextField()
    hints = models.TextField()
    subtopic_id = models.ForeignKey(Subtopic, on_delete=models.CASCADE, related_name='tasks')
