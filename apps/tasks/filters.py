import django_filters

from apps.tasks.models import Task, SubTask


class TaskListFilter(django_filters.FilterSet):
    subtask_assign_to = django_filters.CharFilter(method='filter_by_subtask_assign_to')
    subtask_assigned_by_user = django_filters.CharFilter(method='filter_by_subtask_assigned_by_user')

    class Meta:
        model = Task
        fields = '__all__'
        exclude = ['comment']

    def filter_by_subtask_assign_to(self, queryset, name, value):
        return queryset.filter(subtasks__assign_to__id=value)

    def filter_subtask_assigned_by_user(self, queryset, name, value):
        return queryset.filter(subtasks__creator__id=value)

class SubtaskListFilter(django_filters.FilterSet):
    class Meta:
        model = SubTask
        fields = '__all__'
        exclude = ['comment']
