import django_filters

from apps.tasks.models import Task, SubTask


class TaskListFilter(django_filters.FilterSet):
    class Meta:
        model = Task
        fields = '__all__'
        exclude = ['comment']


class SubtaskListFilter(django_filters.FilterSet):
    class Meta:
        model = SubTask
        fields = '__all__'
        exclude = ['comment']
