# Generated by Django 5.1 on 2024-11-15 15:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('expertiseMainFlow', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='expertisefolder',
            name='tags',
        ),
        migrations.DeleteModel(
            name='Tag',
        ),
    ]
