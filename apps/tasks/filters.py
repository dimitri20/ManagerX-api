import django_filters

from apps.tasks.models import Task, SubTask


class TaskListFilter(django_filters.FilterSet):
    subtask_assign_to = django_filters.CharFilter(method='filter_by_subtask_assign_to')
    subtask_assigned_by_user = django_filters.CharFilter(method='filter_subtask_assigned_by_user')
    status = django_filters.CharFilter(method='filter_by_status')

    class Meta:
        model = Task
        fields = '__all__'
        exclude = ['comment']

    def filter_by_subtask_assign_to(self, queryset, name, value):
        return queryset.filter(subtasks__assign_to__id=value)

    def filter_subtask_assigned_by_user(self, queryset, name, value):
        return queryset.filter(subtasks__creator__id=value)

    def filter_by_status(self, queryset, name, value):
        # Split the comma-separated list of statuses
        status_list = value.split(',')
        return queryset.filter(status__in=status_list)

class SubtaskListFilter(django_filters.FilterSet):
    status = django_filters.CharFilter(method='filter_by_status')

    class Meta:
        model = SubTask
        fields = '__all__'
        exclude = ['comment']

    def filter_by_status(self, queryset, name, value):
        # Split the comma-separated list of statuses
        status_list = value.split(',')
        return queryset.filter(status__in=status_list)