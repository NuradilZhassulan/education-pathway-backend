# Generated by Django 5.0.4 on 2024-04-18 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school_management', '0011_rename_description_task_name_remove_task_hints_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='correct_answers',
            field=models.CharField(default='[]', max_length=1024),
        ),
        migrations.AddField(
            model_name='task',
            name='description',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='task',
            name='hints',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='task',
            name='keyboard_elements',
            field=models.ManyToManyField(blank=True, related_name='tasks', to='school_management.keyboardelement'),
        ),
        migrations.AddField(
            model_name='task',
            name='solutions',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
    ]