# Generated by Django 5.0.4 on 2024-04-17 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school_management', '0004_keyboardelement_task_keyboard_elements'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='formulas',
        ),
        migrations.AlterField(
            model_name='task',
            name='correct_answers',
            field=models.TextField(default='[]'),
        ),
    ]